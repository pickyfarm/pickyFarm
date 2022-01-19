from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .forms import Order_Group_Form
from .models import Order_Group, Order_Detail, RefundExchange
from .utils import payment_complete_notification
from django.utils import timezone
from products.models import Product
from farmers.models import Farmer
from django.apps import apps  # for prevent Circular Import Error
from addresses.views import check_address_by_zipcode, calculate_jeju_delivery_fee
import requests, base64
import json
import os
from datetime import datetime
from .BootpayApi import BootpayApi
import pprint
import cryptocode
from kakaomessages.views import send_kakao_message
from kakaomessages.template import templateIdList
from urllib import parse
from core import url_encryption
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest

# Create your views here.


def orderingCart(request):
    pass


# order_group 주문 관리 번호 생성 function
def create_order_group_management_number(pk):
    month_dic = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sept",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }

    now = timezone.localtime()
    year = now.year % 100
    print(year)

    month = now.month
    print(month)
    print(month_dic[month])
    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)

    print(month)
    day = now.day
    print(day)

    if day < 10:
        day = "0" + str(day)
    else:
        day = str(day)

    print(day)

    order_group_management_number = str(year) + month + day + "_PF" + str(pk)

    print(order_group_management_number)
    return order_group_management_number


# order_detail 주문 관리 번호 생성 function
def create_order_detail_management_number(pk, farmer_id):
    now = timezone.localtime()
    year = now.year % 100
    print(year)

    month = now.month
    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)

    print(month)
    day = now.day
    print(day)

    if day < 10:
        day = "0" + str(day)
    else:
        day = str(day)

    order_detail_management_number = str(year) + month + day + "_" + str(pk) + "_" + farmer_id
    return order_detail_management_number


# 결제 진행 페이지에서 주소 전환 시, 서버 반영 Ajax
@login_required
@require_POST
@transaction.atomic
def changeAddressAjax(request):
    if request.method == "POST":
        order_group_pk = int(request.POST.get("order_group_pk", None))
        print("zip_code", int(request.POST.get("zip_code")))
        zip_code = int(request.POST.get("zip_code", 1))

        order_group = Order_Group.objects.get(pk=order_group_pk)

        delivery_fee = 0  # 기본 배송비
        total_price = 0

        for detail in order_group.order_details.all():
            detail_fee = calculate_jeju_delivery_fee(zip_code, detail.product)
            delivery_fee += detail_fee
            quantity = (int)(detail.quantity)
            detail.total_price = detail_fee + detail.product.sell_price
            detail.save()
            total_price += detail.product.sell_price * quantity

        order_group.total_price = total_price + delivery_fee
        order_group.save()
        print("order.total_price", order_group.total_price)

        data = {
            "delivery_fee": delivery_fee,
            "total_price": order_group.total_price,
        }

        return JsonResponse(data)


@login_required
@transaction.atomic
def payment_create(request):

    if request.method == "GET":
        return redirect(reverse("core:main"))

    """결제 페이지로 이동 시, Order_Group / Order_Detail 생성"""

    user = request.user
    consumer = user.consumer
    # 이름 전화번호 주소지 정보 등
    user_ctx = {
        "account_name": user.account_name,
        "phone_number": user.phone_number,
        "default_address": consumer.default_address.get_full_address(),
        "default_zipcode": consumer.default_address.zipcode,
        "addresses": user.addresses.all(),
    }

    print(f"기본배송지 : {consumer.default_address.get_full_address()} ")

    if request.method == "POST":
        form = Order_Group_Form()
        orders = json.loads(request.POST.get("orders"))
        print(orders)
        # (변수) 주문 상품 list (주문 수량, 주문 수량 고려한 가격, 주문 수량 고려한 무게)
        products = []
        # (변수) 총 주문 상품 개수
        total_quantity = 0
        # (변수) 총 주문 상품 무게
        total_weight = 0
        # (변수) 총 주문 상품 가격의 합
        price_sum = 0

        # [PROCESS 1] 결제 대기 상태인 Order_Group 생성
        order_group = Order_Group(status="wait", consumer=consumer)
        order_group.save()
        order_group_pk = order_group.pk

        # [PROCESS 2] order_group pk와 주문날짜를 기반으로 order_group 주문 번호 생성
        order_group_management_number = create_order_group_management_number(order_group_pk)

        # [PROCESS 3] Order_Group 주문 번호 저장 (결제 단위 구별용 - BootPay 전송)
        order_group.order_management_number = order_group_management_number

        # 부트페이 API로 보내기 위한 name parameter 뒤에 들어갈 숫자 정보 ex) 맛있는 딸기 외 3개
        order_detail_cnt = 0
        # 부트페이 API로 보내기 위한 name parameter
        order_group_name = ""

        # 전체 배송비 (기본 배송비 + 단위별 추가 배송비)
        total_delivery_fee = 0

        # [PROCESS 4] 소비자 주문목록에서 각 주문 사항 order_detail로 생성
        for order in orders:

            delivery_fee = 0

            order_detail_cnt += 1

            pk = (int)(order["pk"])
            quantity = (int)(order["quantity"])

            # 주문 상품의 본래 상품 select
            product = Product.objects.get(pk=pk)

            # 기본 배송비 total_delivery_fee에 추가
            # delivery_fee += product.default_delivery_fee
            # total_delivery_fee += product.default_delivery_fee

            # 단위별 추가 배송비 total_delivery_fee에 추가
            if product.additional_delivery_fee_unit != 0:
                quantity_per_unit = quantity / product.additional_delivery_fee_unit

                if (float)(quantity_per_unit) > 1:
                    if quantity % product.additional_delivery_fee_unit == 0:
                        delivery_fee += (
                            (int)(quantity_per_unit - 1)
                        ) * product.addtional_delivery_fee

                        # total_delivery_fee += (
                        #     (int)(quantity_per_unit - 1)
                        # ) * product.addtional_delivery_fee
                    else:
                        delivery_fee += (int)(
                            quantity / product.additional_delivery_fee_unit
                        ) * product.additional_delivery_fee

                        # total_delivery_fee += (int)(
                        #     quantity / product.additional_delivery_fee_unit
                        # ) * product.additional_delivery_fee

            # consumer의 기본 배송비의 ZIP 코드를 파라미터로 전달해서 제주산간인지 여부를 파악
            consumer_zipcode = int(consumer.default_address.zipcode)
            is_jeju_mountain = check_address_by_zipcode(consumer_zipcode)

            print("is jeju: ", is_jeju_mountain)
            # 제주 산간이면 order_group is_jeju_mountain
            if is_jeju_mountain:
                order_group.is_jeju_mountain = True
            detail_fee = calculate_jeju_delivery_fee(consumer_zipcode, product)
            total_delivery_fee += detail_fee  # 제주/도서산간 배송비
            total_delivery_fee += delivery_fee  # 단위별 추가 배송비
            # 제주 산간이 아니면 total_delivery_fee에 안더하기

            # order_detail 구매 수량
            total_quantity += quantity
            # order_detail 구매 총액
            total_price = product.sell_price * quantity

            # [PROCESS 5] 결제 대기 상태의 order_detail 생성 및 Order_Group으로 묶어줌
            order_detail = Order_Detail(
                status="wait",
                quantity=quantity,
                commision_rate=product.commision_rate,
                total_price=delivery_fee + total_price + detail_fee,
                product=product,
                order_group=order_group,
            )
            order_detail.save()

            order_detail_pk = order_detail.pk
            farmer_id = product.farmer.user.username

            # [PROCESS 6] Order_detail 주문 번호 저장
            # order_group pk와 주문날짜를 기반으로 order_group 주문 번호 생성
            order_detail_management_number = create_order_detail_management_number(
                order_detail_pk, farmer_id
            )
            order_detail.order_management_number = order_detail_management_number
            order_detail.save()

            price_sum += total_price

            # 구매하는 첫번째 상품인 경우 order_group name으로 추가 ex) 맛있는 딸기 외 2개
            if order_detail_cnt == 1:
                order_group_name = product.title

            print(f"product_weight : {product.weight}")
            print(f"product_quantity : {quantity}")
            total_weight += (product.weight) * quantity
            print(f"중간 결과 {total_weight}")
            products.append(
                {
                    "order_number": order_detail_management_number,
                    "product": product,
                    "order_quantity": quantity,
                    "order_price": product.sell_price * quantity,
                    "weight": product.weight * quantity,
                }
            )

        # 구매하는 상품 개수가 1을 초과 시, **외 2개** 식으로 표기하기 위함
        if order_detail_cnt > 1:
            rest_cnt = order_detail_cnt - 1
            order_group_name = order_group_name + " 외 " + str(rest_cnt) + "개"

        print(order_group_name)

        # [PROCESS 7] 할인 관련 logic (예정)
        discount = 0  # 추후 할인 전략 도입 시 작성
        print(total_weight)

        # [PROCESS 8] 최종 결제 금액 계산
        final_price = price_sum + total_delivery_fee + discount

        order_group.total_price = final_price
        order_group.total_quantity = total_quantity
        order_group.save()
        print(order_group.pk)
        ctx = {
            "order_group_management_number": order_group_management_number,
            "order_group_pk": order_group_pk,
            "order_group_name": order_group_name,
            "form": form,
            "consumer": consumer,
            "products": products,
            "total_quantity": total_quantity,
            "price_sum": price_sum,
            "discount": discount,
            "delivery_fee": total_delivery_fee,
            "final_price": final_price,
            "total_weight": round(total_weight, 2),
            "order_group_pk": int(order_group.pk),
        }

        ctx = {**ctx, **user_ctx}

        return render(request, "orders/payment.html", ctx)


@login_required
@require_POST
@transaction.atomic
# 배송 정보가 입력된 후 oreder_group에 update
def payment_update(request, pk):

    """결제 전, 주문 재고 확인"""
    """Order_Group 주문 정보 등록"""

    consumer = request.user.consumer

    if request.method == "POST":
        # [PROCESS 1] GET Parameter에 있는 pk 가져와서 Order_Group select
        order_group_pk = pk
        order_group = Order_Group.objects.get(pk=order_group_pk)

        # [PROCESS 2] 클라이언트에서 보낸 total_price와 서버의 total price 비교
        client_total_price = int(request.POST.get("total_price"))
        if order_group.total_price != client_total_price:
            order_group.status = "error_price_match"
            for detail in order_group.order_details:
                detail.status = "error_price_match"
                detail.save()
            order_group.save()

            res_data = {"valid": False, "error_type": "error_price_match"}

            return JsonResponse(res_data)

        # [PROCESS 3] Order_Group에 속한 Order_detail을 모두 가져와서 재고량 확인
        order_details = order_group.order_details.all()

        # 모든 주문 상품 재고량 확인 태그
        valid = True
        # 재고가 부족한 상품명 리스트
        invalid_products = list()

        # [PROCESS 4] 결제 전 최종 재고 확인
        for detail in order_details:
            print("[재고 확인 상품 재고] " + (str)(detail.product.stock))
            print("[재고 확인 주문양] " + (str)(detail.quantity))
            if detail.product.stock - detail.quantity < 0:
                valid = False
                # 재고가 부족한 경우 부족한 상품 title 저장 -> 추후 결제 실패 페이지의 오류 메시지로 출력
                invalid_products.append(detail.product.title)
                print(detail.product.title + "재고 부족")

        print(invalid_products)

        # [PROCESS 5] 재고 확인 성공인 경우
        if valid is True:

            # [PROCESS 6] 주문 정보 Order_Group에 등록
            rev_name = request.POST.get("rev_name")
            rev_phone_number = request.POST.get("rev_phone_number")
            rev_address = request.POST.get("rev_address")
            rev_loc_at = request.POST.get("rev_loc_at")
            rev_message = request.POST.get("rev_message")
            to_farm_message = request.POST.get("to_farm_message")
            payment_type = request.POST.get("payment_type")

            print(rev_name + rev_phone_number + rev_loc_at + rev_message + to_farm_message)

            print(order_group)
            # 배송 정보 order_group에 업데이트
            order_group.rev_name = rev_name
            order_group.rev_address = rev_address
            order_group.rev_phone_number = rev_phone_number
            order_group.rev_loc_at = rev_loc_at
            # order_group.rev_loc_detail=rev_loc_detail
            order_group.rev_message = rev_message
            order_group.to_farm_message = to_farm_message
            order_group.payment_type = payment_type
            order_group.order_at = timezone.now()

            order_group.save()

            res_data = {
                "valid": valid,
                "orderId": "temp",
                "orderName": "temp",
                "customerName": "nameTemp",
            }

            return JsonResponse(res_data)

        # 재고 확인 실패의 경우 부족한 재고 상품 리스트 및 valid값 전송
        else:
            order_group.status = "error_stock"
            for detail in order_details:
                detail.status = "error_stock"
                detail.save()
            order_group.save()
            print("[valid 값]" + (str)(valid))
            print("[invalid_products]" + (str)(invalid_products))
            res_data = {
                "valid": valid,
                "error_type": "error_stock",
                "invalid_products": invalid_products,
            }

            return JsonResponse(res_data)

        # !!!rev_address 추가 필요
        # rev_loc_detail 지우기
        # payment type은 잠시 보류
        # if form.is_valid():
        #     rev_name = form.cleaned_data.get('rev_name')
        #     rev_phone_number = form.cleaned_data.get('rev_phone_number')
        #     rev_loc_at = form.cleaned_data.get('rev_loc_at')
        #     # rev_loc_detail = form.cleaned_data.get('rev_loc_detail')
        #     rev_message = form.cleaned_data.get('rev_message')
        #     to_farm_message = form.cleaned_data.get('to_farm_message')
        #     # payment_type = form.cleaned_data.get('payment_type')


# @login_required
# def payment_success(request):

#     if request.method == "GET":
#         # 결제 승인을 위해 사용되는 키값
#         # 이 키를 http header에 넣어서 결제 승인 api를 요청
#         payment_key = request.GET.get("paymentKey", None)
#         print(f"페이먼트 키 : {payment_key}")
#         # 주문 고유 id
#         order_id = request.GET.get("orderId", None)
#         # 결제할 금액 (비교 금액)
#         amount_ready = request.GET.get("amount_ready")
#         # 실제 결제한 금액
#         amount_paid = request.GET.get("amount")
#         if (payment_key is not None) and (order_id is not None):
#             if amount_ready == amount_paid:
#                 data = {
#                     "orderId": order_id,
#                     "amount": amount_paid,
#                 }
#                 # PG사에서 제공해주는 client ID and Client Passwords
#                 usr_pass = b"test_sk_BE92LAa5PVb64R41qaPV7YmpXyJj:"
#                 # b64로 암호화
#                 b64_val = base64.b64encode(usr_pass).decode("utf-8")

#                 auth_request = requests.post(
#                     f"https://api.tosspayments.com/v1/payments/{payment_key}",
#                     headers={
#                         # 추후 authorization token이 들어가야 함
#                         "Authorization": f"Basic {b64_val}",
#                         "Content-Type": "application/json",
#                     },
#                     json=data,
#                 )
#                 print(auth_request.json())
#                 if auth_request:
#                     # 여기서 order group 과 order detail의 결제 상태를 완료로 변경해주어야함
#                     ctx = {
#                         "order_id": order_id,
#                         "amount": amount_paid,
#                     }
#                     return render(request, "orders/payment_success.html", ctx)
#                 else:
#                     return redirect(reverse("orders:payment_fail"))
#             else:
#                 return redirect(reverse("orders:payment_fail"))
#         else:
#             return redirect(reverse("orders:payment_fail"))


@login_required
@transaction.atomic
def payment_fail(request):
    error_type = str(request.GET.get("errorType", None))
    # order_group_pk = request.GET.get("orderGroupPk", None)
    stock_error_msg = str(request.GET.get("errorMsg", None))
    print(error_type)

    if error_type == "error_stock":
        errorMsg = stock_error_msg
    elif error_type == "error_valid":
        errorMsg = "결제 검증에 오류가 있습니다. 다시 시도해주세요"
    elif error_type == "error_server":
        errorMsg = "서버에 오류가 있었습니다. 다시 시도해주세요"
    else:
        errorMsg = "알 수 없는 오류가 있습니다. 다시 시도해주세요"

    ctx = {"errorMsg": errorMsg}
    return render(request, "orders/payment_fail.html", ctx)


class payment_valid_farmer:
    farmer_pk = None
    farm_name = None
    farmer_nickname = None
    farmer_phone_number = None

    def __init__(self, pk, farm_name, nicknae, phone_number):
        self.farmer_pk = pk
        self.farm_name = farm_name
        self.farmer_nickname = nicknae
        self.farmer_phone_number = phone_number


def farmer_search(farmers, pk, start, end):
    mid = (start + end) // 2
    if farmers[mid].farmer_pk == pk:
        return farmers[mid]
    if farmers[mid].farmer_pk < pk:
        return farmer_search(farmers, pk, mid + 1, end)
    else:
        return farmer_search(farmers, pk, start, mid - 1)


def send_kakao_with_payment_complete(order_group_pk, receipt_id):
    order_group = Order_Group.objects.get(pk=order_group_pk)
    order_details = order_group.order_details.all()
    farmers = list(set(map(lambda u: u.product.farmer, order_details)))
    phone_number_consumer = order_group.consumer.user.phone_number

    farmers_info = []
    for farmer in farmers:
        farmers_info.append(
            payment_valid_farmer(
                farmer.pk,
                farmer.farm_name,
                farmer.user.nickname,
                farmer.user.phone_number,
            )
        )

    farmers_info = sorted(farmers_info, key=lambda x: x.farmer_pk)
    farmers_info_len = len(farmers_info)
    # print(f"Farmer_INFO len : {farmers_info_len}")
    order_group.receipt_number = receipt_id

    for detail in order_details:
        product = detail.product
        detail.status = "payment_complete"
        detail.payment_status = "incoming"  # 정산상태 정산예정으로 변경
        detail.save()

        kakao_msg_quantity = (str)(detail.quantity) + "개"

        target_farmer_pk = product.farmer.pk
        target_farmer = farmer_search(farmers_info, target_farmer_pk, 0, farmers_info_len)
        # print("Farmer!!!" + target_farmer.farm_name)

        args_consumer = {
            "#{farm_name}": target_farmer.farm_name,
            "#{order_detail_number}": detail.order_management_number,
            "#{order_detail_title}": detail.product.title,
            "#{farmer_nickname}": target_farmer.farmer_nickname,
            "#{option_name}": detail.product.option_name,
            "#{quantity}": kakao_msg_quantity,
            "#{link_1}": f"www.pickyfarm.com/farmer/farmer_detail/{target_farmer_pk}",  # 임시
            "#{link_2}": "www.pickyfarm.com/user/mypage/orders",  # 임시
        }

        # 소비자 결제 완료 카카오 알림톡 전송
        send_kakao_message(
            phone_number_consumer,
            templateIdList["payment_complete"],
            args_consumer,
        )

        # order_management_number 인코딩
        url_encoded_order_detail_number = url_encryption.encode_string_to_url(
            detail.order_management_number
        )

        args_farmer = {
            "#{order_detail_title}": detail.product.title,
            "#{order_detail_number}": detail.order_management_number,
            "#{option_name}": detail.product.option_name,
            "#{quantity}": kakao_msg_quantity,
            "#{rev_name}": order_group.rev_name,
            "#{rev_phone_number}": phone_number_consumer,
            "#{rev_address}": order_group.rev_address,
            "#{rev_loc_at}": order_group.rev_loc_at,
            "#{rev_detail}": order_group.rev_message,
            "#{rev_message}": order_group.to_farm_message,
            "#{link_1}": f"www.pickyfarm.com/farmer/mypage/orders/check?odmn={url_encoded_order_detail_number}",  # 임시
            "#{link_2}": f"www.pickyfarm.com/farmer/mypage/orders/cancel?odmn={url_encoded_order_detail_number}",  # 임시
            "#{link_3}": f"www.pickyfarm.com/farmer/mypage/orders/invoice?odmn={url_encoded_order_detail_number}",  # 임시
        }

        print(f'주문확인 url : {args_farmer["#{link_1}"]}')

        send_kakao_message(
            target_farmer.farmer_phone_number,
            templateIdList["order_recept"],
            args_farmer,
        )

    order_group.status = "payment_complete"
    order_group.save()


@login_required
@transaction.atomic
def payment_valid(request):
    if request.method == "POST":
        REST_API_KEY = os.environ.get("BOOTPAY_REST_KEY")
        PRIVATE_KEY = os.environ.get("BOOTPAY_PRIVATE_KEY")

        receipt_id = request.POST.get("receipt_id")
        order_group_pk = int(request.POST.get("orderGroupPk"))
        order_group = Order_Group.objects.get(pk=order_group_pk)
        total_price = order_group.total_price

        order_details = Order_Detail.objects.filter(order_group=order_group)

        farmers = list(set(map(lambda u: u.product.farmer, order_details)))
        unsubscribed_farmers = list()
        subscribed_farmers = list()

        farmers_info = []

        for farmer in farmers:
            farmers_info.append(
                payment_valid_farmer(
                    farmer.pk,
                    farmer.farm_name,
                    farmer.user.nickname,
                    farmer.user.phone_number,
                )
            )
            Subscribe = apps.get_model("users", "Subscribe")  # for prevent Circular Import Error
            if Subscribe.objects.filter(consumer=order_group.consumer, farmer=farmer).exists():
                subscribed_farmers.append(farmer)
            else:
                unsubscribed_farmers.append(farmer)

        farmers_info = sorted(farmers_info, key=lambda x: x.farmer_pk)
        farmers_info_len = len(farmers_info)
        print(f"Farmer_INFO len : {farmers_info_len}")

        order_group.receipt_number = receipt_id

        bootpay = BootpayApi(application_id=REST_API_KEY, private_key=PRIVATE_KEY)
        result = bootpay.get_access_token()

        if result["status"] == 200:
            verify_result = bootpay.verify(receipt_id)

            if verify_result["status"] == 200:
                if (
                    verify_result["data"]["price"] == total_price
                    and verify_result["data"]["status"] == 1
                ):

                    phone_number_consumer = order_group.consumer.user.phone_number
                    # Model Method Apply
                    # order_group.consumer.send_kakao_payment_valid(order_group, "")

                    for detail in order_details:

                        product = detail.product
                        # order_detail 재고 차감
                        product.sold(detail.quantity)
                        # order_detail status - payment_complete로 변경
                        detail.status = "payment_complete"
                        detail.payment_status = "incoming"  # 정산상태 정산예정으로 변경
                        detail.product.save()
                        detail.save()

                        # kakao_msg_weight = (str)(product.weight) + product.weight_unit

                        kakao_msg_quantity = (str)(detail.quantity) + "개"

                        target_farmer_pk = product.farmer.pk

                        target_farmer = farmer_search(
                            farmers_info, target_farmer_pk, 0, farmers_info_len
                        )
                        print("Farmer!!!" + target_farmer.farm_name)

                        args_consumer = {
                            "#{farm_name}": target_farmer.farm_name,
                            "#{order_detail_number}": detail.order_management_number,
                            "#{order_detail_title}": detail.product.title,
                            "#{farmer_nickname}": target_farmer.farmer_nickname,
                            "#{option_name}": detail.product.option_name,
                            "#{quantity}": kakao_msg_quantity,
                            "#{link_1}": f"www.pickyfarm.com/farmer/farmer_detail/{target_farmer_pk}",  # 임시
                            "#{link_2}": "www.pickyfarm.com/user/mypage/orders",  # 임시
                        }

                        # 소비자 결제 완료 카카오 알림톡 전송
                        send_kakao_message(
                            phone_number_consumer,
                            templateIdList["payment_complete"],
                            args_consumer,
                        )

                        # order_management_number 인코딩
                        url_encoded_order_detail_number = url_encryption.encode_string_to_url(
                            detail.order_management_number
                        )

                        args_farmer = {
                            "#{order_detail_title}": detail.product.title,
                            "#{order_detail_number}": detail.order_management_number,
                            "#{option_name}": detail.product.option_name,
                            "#{quantity}": kakao_msg_quantity,
                            "#{rev_name}": order_group.rev_name,
                            "#{rev_phone_number}": phone_number_consumer,
                            "#{rev_address}": order_group.rev_address,
                            "#{rev_loc_at}": order_group.rev_loc_at,
                            "#{rev_detail}": order_group.rev_message,
                            "#{rev_message}": order_group.to_farm_message,
                            "#{link_1}": f"www.pickyfarm.com/farmer/mypage/orders/check?odmn={url_encoded_order_detail_number}",  # 임시
                            "#{link_2}": f"www.pickyfarm.com/farmer/mypage/orders/cancel?odmn={url_encoded_order_detail_number}",  # 임시
                            "#{link_3}": f"www.pickyfarm.com/farmer/mypage/orders/invoice?odmn={url_encoded_order_detail_number}",  # 임시
                        }

                        print(f'주문확인 url : {args_farmer["#{link_1}"]}')

                        send_kakao_message(
                            target_farmer.farmer_phone_number,
                            templateIdList["order_recept"],
                            args_farmer,
                        )

                    # order_group status - payment complete로 변경
                    order_group.status = "payment_complete"
                    order_group.save()

                    ctx = {
                        "order_group": order_group,
                        "data": verify_result,
                        "order_details": order_details,
                        "sub_farmers": subscribed_farmers,
                        "unsub_farmers": unsubscribed_farmers,
                    }

                    nowDatetime = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"=== PAYMENT VALIDATION SUCCESS : {nowDatetime} ===")
                    print(f"=== RECIPT ID : {receipt_id} ===")

                    payment_complete_notification(order_group.pk)

                    return render(request, "orders/payment_success.html", ctx)

        else:
            cancel_result = bootpay.cancel(
                receipt_id, total_price, request.user.nickname, "결제검증 실패로 인한 결제 취소"
            )

            if cancel_result["status"] == 200:
                # order_group status - 에러 검증실패로 변경
                order_group.status = "error_valid"
                order_group.save()

                # order_detail status - 에러 검증실패로 변경
                for detail in order_details:
                    detail.status = "error_valid"
                    detail.save()

                ctx = {"cancel_result": cancel_result}
                return redirect(
                    f'{reverse("orders:payment_fail")}?errorType=error_validk&orderGroupPK={order_group_pk}'
                )

            else:
                order_group.status = "error_server"
                order_group.save()
                # order_detail status - 에러 서버로 변경
                for detail in order_details:
                    detail.status = "error_server"
                    detail.save()
                ctx = {"cancel_result": "결제 검증에 실패하여 결제 취소를 시도하였으나 실패하였습니다. 고객센터에 문의해주세요"}
                return redirect(
                    f'{reverse("orders:payment_fail")}?errorType=error_server&orderGroupPK={order_group_pk}'
                )

    return HttpResponse("잘못된 접근입니다", status=400)


class priceMatchError(Exception):
    def __str__(self):
        return "클라이언트 요청 금액과 DB에 저장된 금액이 일치하지 않습니다."


class stockLackError(Exception):
    def __str__(self):
        return "재고가 부족합니다."


@login_required
@require_POST
def vbank_progess(request):

    user = request.user

    if request.method == "POST":
        # [PROCESS 1] GET Parameter에 있는 pk 가져와서 Order_Group select / 구독 리스트 추출
        order_group_pk = int(request.POST.get("order_group_pk"))
        order_group = Order_Group.objects.get(pk=order_group_pk)
        order_details = order_group.order_details.all()

        farmers = list(set(map(lambda u: u.product.farmer, order_details)))
        unsubscribed_farmers = list()
        subscribed_farmers = list()

        farmers_info = []

        for farmer in farmers:
            farmers_info.append(
                payment_valid_farmer(
                    farmer.pk,
                    farmer.farm_name,
                    farmer.user.nickname,
                    farmer.user.phone_number,
                )
            )
            Subscribe = apps.get_model("users", "Subscribe")  # for prevent Circular Import Error
            if Subscribe.objects.filter(consumer=order_group.consumer, farmer=farmer).exists():
                subscribed_farmers.append(farmer)
            else:
                unsubscribed_farmers.append(farmer)

        farmers_info = sorted(farmers_info, key=lambda x: x.farmer_pk)
        farmers_info_len = len(farmers_info)

        # [PROCESS 2] 클라이언트에서 보낸 total_price와 서버의 total price 비교
        client_total_price = int(request.POST.get("total_price"))

        print(f"--------total_price : {client_total_price} ---------")

        try:
            if order_group.total_price != client_total_price:
                raise priceMatchError

        except priceMatchError:
            print(priceMatchError)
            order_group.status = "error_price_match"
            for detail in order_group.order_details:
                detail.status = "error_price_match"
                detail.save()
            order_group.save()
            return redirect(
                f'{reverse("orders:payment_fail")}?errorType=error_price_match&orderGroupPK={order_group_pk}'
            )

        # [PROCESS 3] Order_Group에 속한 Order_detail을 모두 가져와서 재고량 확인

        # 모든 주문 상품 재고량 확인 태그
        valid = True
        # 재고가 부족한 상품명 리스트
        invalid_products = list()

        # [PROCESS 4] 결제 전 최종 재고 확인
        for detail in order_details:
            print("[재고 확인 상품 재고] " + (str)(detail.product.stock))
            print("[재고 확인 주문양] " + (str)(detail.quantity))
            if detail.product.stock - detail.quantity < 0:
                valid = False
                # 재고가 부족한 경우 부족한 상품 title 저장 -> 추후 결제 실패 페이지의 오류 메시지로 출력
                invalid_products.append(detail.product.title)
                print(detail.product.title + "재고 부족")
            else:
                # 재고가 있는 경우 재고 차감
                detail.product.sold(detail.quantity)
                detail.save()

        print(invalid_products)

        try:
            # 재고가 없어서 valid가 False인경우 Exception 발생
            if valid is False:
                print(f"--------재고 부족 ---------")
                raise stockLackError
        except stockLackError:
            print(stockLackError)
            order_group.status = "error_stock"
            for detail in order_details:
                detail.status = "error_stock"
                detail.save()
            order_group.save()
            print("[valid 값]" + (str)(valid))
            print("[invalid_products]" + (str)(invalid_products))
            res_data = {
                "valid": valid,
                "error_type": "error_stock",
                "invalid_products": invalid_products,
            }

            return redirect(
                f'{reverse("orders:payment_fail")}?errorType=error_stock&orderGroupPK={order_group_pk}&errorMsg={(str)(invalid_products)}의 재고가 부족합니다'
            )

        # [PROCESS 5] 재고 확인 성공인 경우
        if valid is True:
            print(f"--------재고 확인 성공 ---------")
            # [PROCESS 6] 주문 정보 Order_Group에 등록
            rev_name = request.POST.get("rev_name")
            rev_phone_number = request.POST.get("rev_phone_number")
            rev_address = request.POST.get("rev_address")
            rev_loc_at = request.POST.get("rev_loc_at")
            rev_message = request.POST.get("rev_message")
            to_farm_message = request.POST.get("to_farm_message")
            payment_type = request.POST.get("payment_type")
            order_group_name = request.POST.get("order_group_name")

            # 가상계좌 관련 정보
            v_bank = request.POST.get("v_bank")
            v_bank_account = request.POST.get("v_bank_account")
            v_bank_account_holder = request.POST.get("v_bank_account_holder")
            v_bank_expire_date_str = request.POST.get("v_bank_expire_date")
            receipt_id = request.POST.get("receipt_id")
            print(f"--------vbank : {v_bank} account : {v_bank_account}---------")
            # 가상계좌 입금 마감 기한 datetime 변환
            v_bank_expire_date = datetime.strptime(v_bank_expire_date_str, "%Y-%m-%d %H:%M:%S")
            v_bank_expire_date = timezone.make_aware(v_bank_expire_date)
            print(f"-----가상계좌 마감 기한 시간 변환 완료 : {v_bank_expire_date}---------")

            print(rev_name + rev_phone_number + rev_loc_at + rev_message + to_farm_message)

            print(order_group)
            # 배송 정보 order_group에 업데이트
            order_group.rev_name = rev_name
            order_group.rev_address = rev_address
            order_group.rev_phone_number = rev_phone_number
            order_group.rev_loc_at = rev_loc_at
            # order_group.rev_loc_detail=rev_loc_detail
            order_group.rev_message = rev_message
            order_group.to_farm_message = to_farm_message
            order_group.payment_type = payment_type

            order_group.v_bank = v_bank
            order_group.v_bank_account = v_bank_account
            order_group.v_bank_account_holder = v_bank_account_holder
            order_group.v_bank_expire_date = v_bank_expire_date
            order_group.receipt_number = receipt_id

            order_group.order_at = timezone.now()

            order_group.status = "wait_vbank"

            order_group.save()

            print(f"------order_group v_bank_expire_date {order_group.v_bank_expire_date}")

            # 카카오 알림톡 전송
            args_kakao = {
                "#{order_title}": order_group_name,
                "#{v_bank}": v_bank,
                "#{v_bank_account}": v_bank_account,
                "#{v_bank_account_holder}": v_bank_account_holder,
                "#{total_price}": str(client_total_price) + "원",
                "#{v_bank_expire_date}": v_bank_expire_date_str,
            }

            # 소비자 결제 완료 카카오 알림톡 전송
            send_kakao_message(user.phone_number, templateIdList["vbank_info"], args_kakao)

            ctx = {
                "order_group": order_group,
                "order_details": order_details,
                "sub_farmers": subscribed_farmers,
                "unsub_farmers": unsubscribed_farmers,
                # "v_bank" : v_bank,
                # "v_bank_account" : v_bank_account,
                # "v_bank_account_holder" : v_bank_account_holder,
                # "v_bank_expire_date" : str(v_bank_expire_date),
            }

            nowDatetime = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"=== V_BANK_PROGRESS SUCCESS : {nowDatetime} ===")

            return render(request, "orders/payment_success.html", ctx)


@csrf_exempt
def vbank_deposit(request):
    receipt_id = json.loads(request.body)["receipt_id"]
    method = json.loads(request.body)["method"]
    status = int(json.loads(request.body)["status"])

    order_group = Order_Group.objects.get(receipt_number=receipt_id)
    if order_group.payment_type == "vbank":
        # 만료기간 내에 입금 완료한 경우
        if status == 1:
            payment_complete_notification(order_group.pk)
            send_kakao_with_payment_complete(order_group.pk, receipt_id)

        # 계좌 만료된 경우
        elif status == 20:  # 코드 이거 맞는지 확인해야함
            # 팔렸던 거 재고 되돌려놓기
            for detail in order_group.order_details.all():
                detail.product.sold(-detail.quantity)

    return HttpResponse("OK", content_type="text/plain")


def vbank_template_test(request):
    # return render(request, 'orders/vbank/payment_success_vbank.html')
    return render(request, "orders/vbank/payment_success_vbank.html")


# 주문/결제 완료 프론트단을 작업하기 위한 임시 view
# def temporary_payment_success(request):

#     return render(request, 'orders/payment_success.html',{})


# @login_required
# def payment_cancel_by_verification_fail(receiptID, price):
#     REST_API_KEY = os.environ.get("BOOTPAY_REST_KEY")
#     PRIVATE_KEY = os.environ.get("BOOTPAY_PRIVATE_KEY")

#     cancel_reason = "결제 검증 실패로 인한 결제 취소"

#     bootpay = BootpayApi(REST_API_KEY, PRIVATE_KEY)

#     while True:
#         result = bootpay.get_access_token()
#         if result["status"] == 200:
#             while True:
#                 cancel_result = bootpay.cancel(
#                     receiptID, price, request.user.nickname, cancel_reason
#                 )

#     if result["status"] == 200:
#         cancel_result = bootpay.cancel(
#             receiptID, price, request.user.nickname, cancel_reason
#         )
#         if cancel_result["status"] == 200:
#             return

# 결제취소 창 테스트용 view
# def fail_test(request):
#     errorMsg = request.GET.get("errorType", None)
#     return render(request, "orders/payment_fail.html", {"errorMsg": errorMsg})


@transaction.atomic
def order_cancel(request, pk):
    # http referer 참고해서 임의 접근 막는 코드 넣을 예정
    order = Order_Detail.objects.get(pk=pk)
    print(pk)

    if request.method == "GET":
        ctx = {
            "order": order,
        }

        return render(request, "users/mypage/user/order_cancel_popup.html", ctx)

    elif request.method == "POST":
        cancel_reason = request.POST.get("cancel_reason")
        order.cancel_reason = cancel_reason

        REST_API_KEY = os.environ.get("BOOTPAY_REST_KEY")
        PRIVATE_KEY = os.environ.get("BOOTPAY_PRIVATE_KEY")

        bootpay = BootpayApi(application_id=REST_API_KEY, private_key=PRIVATE_KEY)
        result = bootpay.get_access_token()

        if result["status"] == 200:
            cancel_result = bootpay.cancel(
                order.order_group.receipt_number,
                order.total_price,
                order.order_group.consumer.user.account_name,
                cancel_reason,
            )

            if cancel_result["status"] == 200:
                order.status = "cancel"
                order.order_group.status = "cancel"
                product = order.product
                product.stock += order.quantity
                product.save()
                order.save()

                args_kakao = {
                    "#{cancel_reason}": order.cancel_reason,
                    "#{order_detail_title}": order.product.title,
                    "#{order_detail_number}": order.order_management_number,
                    "#{option_name}": order.product.option_name,
                    "#{quantity}": order.quantity,
                    "#{rev_name}": order.order_group.rev_name,
                    "#{rev_phone_number}": order.order_group.rev_phone_number,
                }

                send_kakao_message(
                    order.product.farmer.user.phone_number,
                    templateIdList["order_cancel_by_user"],
                    args_kakao,
                )

                return redirect(reverse("core:popup_callback"))

        return HttpResponse("주문 취소를 실패하였습니다. 고객센터에 문의해주시기 바랍니다.", status=200)

    else:
        return redirect(reverse("core:main"))


@login_required
@transaction.atomic
def create_change_or_refund(request, pk):
    user = request.user
    if request.method == "GET":
        user = request.user
        addresses = user.addresses.all
        ctx = {"addresses": addresses}
        return render(request, "users/mypage/user/product_refund_popup.html", ctx)
    elif request.method == "POST":
        order_detail = Order_Detail.objects.get(pk=pk)

        claim_type = request.POST.get("change_or_refund", None)
        print(claim_type)

        # order_detail status 변경 (환불/반품 접수)
        if claim_type == "refund":
            order_detail.status = "re_recept"
        elif claim_type == "exchange":
            order_detail.status = "ex_recept"
        else:
            return redirect(reverse("core:main"))
        order_detail.save()

        claim_reason = request.POST.get("reason_txt", None)
        print(claim_reason)
        image = request.FILES.get("product_image", None)
        print(image)
        rev_loc_at = request.POST.get("rev_loc_at", None)
        print(rev_loc_at)
        rev_address = request.POST.get("address", None)

        refundExchange = RefundExchange(
            claim_type=claim_type,
            claim_status="recept",
            order_detail=order_detail,
            reason=claim_reason,
            image=image,
            rev_address=rev_address,
            rev_loc_at=rev_loc_at,
        )

        # 주문 일시
        order_detail_create_at = order_detail.create_at.date().strftime("%Y.%m.%d")
        # Product
        product = order_detail.product
        # product kinds (무난이, 일반작물)
        product_kinds = product.kinds
        # 농장 이름
        order_detail_farm_name = product.farmer.farm_name
        # product 이름
        product_title = product.title
        # product가격
        product_price = product.sell_price
        # product weight
        product_weight = (str)(product.weight) + (str)(product.weight_unit)
        # order_detail quantity
        order_detail_quantity = order_detail.quantity

        ctx = {
            "order_date": order_detail_create_at,
            "farm_name": order_detail_farm_name,
            "product_kinds": product_kinds,
            "product_title": product_title,
            "product_price": product_price,
            "product_weight": product_weight,
            "order_detail_quantity": order_detail_quantity,
            "refundExchange": refundExchange,
        }

        farmer_phone_number = order_detail.product.farmer.user.phone_number
        consumer_phone_number = order_detail.order_group.consumer.user.phone_number

        weight = order_detail.product.weight
        weight_unit = order_detail.product.weight_unit
        quantity = order_detail.quantity

        # kakao_msg_weight = (str)(weight) + weight_unit
        kakao_msg_quantity = (str)(quantity) + "개"

        order_management_number = order_detail.order_management_number

        url_encoded_order_management_number = url_encryption.encode_string_to_url(
            order_management_number
        )

        product_title = order_detail.product.title

        farmer_args = {
            "#{order_detail_title}": product_title,
            "#{order_detail_number}": order_management_number,
            "#{option_name}": order_detail.product.option_name,
            "#{quantity}": kakao_msg_quantity,
            "#{consumer_nickname}": user.nickname,
            "#{reason}": claim_reason,
        }

        consumer_args = {
            "#{order_detail_title}": product_title,
            "#{order_detail_number}": order_management_number,
            "#{quantity}": kakao_msg_quantity,
        }

        if claim_type == "refund":
            refundExchange.refund_exchange_delivery_fee = product.refund_delivery_fee
            refundExchange.save()
            farmer_args[
                "#{link}"
            ] = f"www.pickyfarm.com/farmer/mypage/orders/refund/request/check?odmn={url_encoded_order_management_number}"
            send_kakao_message(
                farmer_phone_number,
                templateIdList["refund_recept_for_farmer"],
                farmer_args,
            )
            send_kakao_message(
                consumer_phone_number,
                templateIdList["refund_recept_for_consumer"],
                consumer_args,
            )
            return render(request, "users/mypage/user/product_refund_complete.html", ctx)
        elif claim_type == "exchange":
            refundExchange.refund_exchange_delivery_fee = product.exchange_delivery_fee
            refundExchange.save()
            farmer_args[
                "#{link}"
            ] = f"www.pickyfarm.com/farmer/mypage/orders/exchange/request/check?odmn={url_encoded_order_management_number}"
            send_kakao_message(
                farmer_phone_number,
                templateIdList["exchange_recept_for_farmer"],
                farmer_args,
            )
            send_kakao_message(
                consumer_phone_number,
                templateIdList["exchange_recept_for_consumer"],
                consumer_args,
            )
            return render(request, "users/mypage/user/product_exchange_complete.html", ctx)
        else:
            return redirect(reverse("core:main"))

    else:
        return redirect(reverse("core:main"))


def update_jeju_mountain_delivery_fee(order_group_pk):
    order = Order_Group.get(pk=order_group_pk)
    order_details = Order_Detail.filter(order_group__pk=order_group_pk)
    farmers = list(set(map(lambda u: u.product.farmer, order_details)))


################
# 결제 완료 페이지 - 구독 독려 모달 Ajax View
################
@require_POST
def sub_modal(request):
    unsub_farmer_pk_list = request.POST.getlist(
        "farmer_pk[]",
    )[0]
    unsub_farmer_pk_list = json.loads(unsub_farmer_pk_list)[0]
    cnt = len(unsub_farmer_pk_list)
    if unsub_farmer_pk_list == []:
        return HttpResponse(status=404)
    ctx = dict()
    ctx["count"] = cnt

    farmers = []
    for pk in unsub_farmer_pk_list:
        try:
            farmer = Farmer.objects.get(pk=pk)
            farmers.append(farmer)
        except ObjectDoesNotExist:
            ctx = {"success": False, "message": f"farmer_pk - {pk} 존재하지 않음"}

    ctx["farmers"] = farmers

    return render(request, "orders/modal/payment_success_subs_modal.html", ctx)
