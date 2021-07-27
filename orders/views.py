from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from .forms import Order_Group_Form
from .models import Order_Group, Order_Detail
from django.utils import timezone
from products.models import Product
from users.models import Subscribe
import requests, base64
import json
import os, datetime
from .BootpayApi import BootpayApi
import pprint

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

    order_group_management_number = (
        str(year) + "_" + month + "_" + day + "_PF" + str(pk)
    )

    print(order_group_management_number)
    return order_group_management_number


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

    order_detail_management_number = str(year) + month + day + str(pk) + "_" + farmer_id
    return order_detail_management_number


@login_required
@transaction.atomic
def payment_create(request):

    """결제 페이지로 이동 시, Order_Group / Order_Detail 생성"""
    
    user = request.user
    consumer = user.consumer
    # 이름 전화번호 주소지 정보 등
    user_ctx = {
        "account_name" : user.account_name,
        "phone_number" : user.phone_number,
        "default_address" : consumer.default_address.get_full_address(),
        "addresses" : user.addresses.all(),
    }

    print(f'기본배송지 : {consumer.default_address.get_full_address()} ')


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
        order_group_management_number = create_order_group_management_number(
            order_group_pk
        )

        # [PROCESS 3] Order_Group 주문 번호 저장 (결제 단위 구별용 - BootPay 전송)
        order_group.order_management_number = order_group_management_number
        order_group.save()

        # 부트페이 API로 보내기 위한 name parameter 뒤에 들어갈 숫자 정보 ex) 맛있는 딸기 외 3개
        order_detail_cnt = 0
        # 부트페이 API로 보내기 위한 name parameter
        order_group_name = ""

        # 전체 배송비 (기본 배송비 + 단위별 추가 배송비)
        total_delivery_fee = 0

        # [PROCESS 4] 소비자 주문목록에서 각 주문 사항 order_detail로 생성
        for order in orders:

            order_detail_cnt += 1

            pk = (int)(order["pk"])
            quantity = (int)(order["quantity"])

            # 주문 상품의 본래 상품 select
            product = Product.objects.get(pk=pk)

            # 기본 배송비 total_delivery_fee에 추가
            total_delivery_fee += product.default_delivery_fee

            # 단위별 추가 배송비 total_delivery_fee에 추가
            if product.additional_delivery_fee_unit != 0:
                quantity_per_unit = quantity / product.additional_delivery_fee_unit

                if (float)(quantity_per_unit) > 1:
                    if quantity % product.additional_delivery_fee_unit == 0:
                        total_delivery_fee += (
                            (int)(quantity_per_unit - 1)
                        ) * product.addtional_delivery_fee
                    else:
                        total_delivery_fee += (int)(
                            quantity / product.additional_delivery_fee_unit
                        ) * product.additional_delivery_fee
            # !!!!제주/산간 관련 추가 배송비 코드 추가해야!!!!

            # order_detail 구매 수량
            total_quantity += quantity
            # order_detail 구매 총액
            total_price = product.sell_price * quantity

            # [PROCESS 5] 결제 대기 상태의 order_detail 생성 및 Order_Group으로 묶어줌
            order_detail = Order_Detail(
                status="wait",
                quantity=quantity,
                total_price=total_price,
                product=product,
                order_group=order_group,
            )
            order_detail.save()

            order_detail_pk = order_detail.pk
            farmer_id = product.farmer.user.username

            # [PROCESS 6] Order_detail 주문 번호 저장
            # order_group pk와 주문날짜를 기반으로 order_group 주문 번호 생성
            order_detail_management_number = create_order_detail_management_number(
                order_group_pk, farmer_id
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

        # [PROCESS 2] Order_Group에 속한 Order_detail을 모두 가져와서 재고량 확인
        order_details = order_group.order_details.all()

        # 모든 주문 상품 재고량 확인 태그
        valid = True
        # 재고가 부족한 상품명 리스트
        invalid_products = list()

        # [PROCESS 3] 결제 전 최종 재고 확인
        for detail in order_details:
            print("[재고 확인 상품 재고] " + (str)(detail.product.stock))
            print("[재고 확인 주문양] " + (str)(detail.quantity))
            if detail.product.stock - detail.quantity < 0:
                valid = False
                # 재고가 부족한 경우 부족한 상품 title 저장 -> 추후 결제 실패 페이지의 오류 메시지로 출력
                invalid_products.append(detail.product.title)
                print(detail.product.title + "재고 부족")

        print(invalid_products)

        # [PROCESS 4] 재고 확인 성공인 경우, 각 상품 재고 차감 / status 변경
        if valid is True:
            for detail in order_details:
                # order_detail 재고 차감
                detail.product.stock -= detail.quantity
                # order_detail status - payment_complete로 변경
                detail.status = "payment_complete"
                detail.product.save()
                detail.save()

            # [PROCESS 5] 주문 정보 Order_Group에 등록
            rev_name = request.POST.get("rev_name")
            rev_phone_number = request.POST.get("rev_phone_number")
            rev_address = request.POST.get("rev_address")
            rev_loc_at = request.POST.get("rev_loc_at")
            rev_message = request.POST.get("rev_message")
            to_farm_message = request.POST.get("to_farm_message")
            payment_type = request.POST.get("payment_type")

            print(
                rev_name + rev_phone_number + rev_loc_at + rev_message + to_farm_message
            )

            print(order_group)
            # 배송 정보 order_group에 업데이트
            order_group.rev_name = rev_name
            order_group.rev_address = rev_address
            order_group.rev_phone_number = rev_phone_number
            order_group.rev_loc_at = rev_loc_at
            # order_group.rev_loc_detail=rev_loc_detail
            order_group.rev_message = rev_message
            order_group.to_farm_message = to_farm_message
            order_group.payment_type=payment_type
            order_group.order_at = timezone.now()

            # order_group status - payment complete로 변경
            order_group.status = "payment_complete"
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
            print("[valid 값]" + (str)(valid))
            print("[invalid_products]" + (str)(invalid_products))
            res_data = {
                "valid": valid,
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
    order_group_pk = request.GET.get("orderGroupPk", None)
    print(error_type)

    if error_type == "error_stock":
        errorMsg = "재고가 부족합니다"
    elif error_type == "error_valid":
        errorMsg = "결제 검증에 오류가 있습니다. 다시 시도해주세요"
    elif error_type == "error_server":
        errorMsg = "서버에 오류가 있었습니다. 다시 시도해주세요"
    else:
        errorMsg = "알 수 없는 오류가 있습니다. 다시 시도해주세요"

    order_group = Order_Group.objects.get(pk=order_group_pk)
    order_group.status = error_type
    order_details = order_group.order_details.all()

    for detail in order_details:
        detail.product.stock += detail.quantity
        print("[detail] - " + detail.product.title + " stock 복구")
        detail.status = error_type
        print("[detail] status - " + detail.status + "변경")
        detail.save()
    
    order_group.save()

    ctx = {"errorMsg": errorMsg}
    return render(request, "orders/payment_fail.html", ctx)


@login_required
@transaction.atomic
def payment_valid(request):
    if request.method == "POST":
        REST_API_KEY = os.environ.get("BOOTPAY_REST_KEY")
        PRIVATE_KEY = os.environ.get("BOOTPAY_PRIVATE_KEY")

        receipt_id = request.POST.get("receipt_id")
        order_group_pk = int(request.POST.get("orderGroupPk"))
        order = Order_Group.objects.get(pk=order_group_pk)
        total_price = order.total_price

        orders = Order_Detail.objects.filter(order_group=order)

        farmers = list(set(map(lambda u: u.product.farmer, orders)))
        unsubscribed_farmers = list()
        subscribed_farmers = list()

        for farmer in farmers:
            if Subscribe.objects.filter(consumer=order.consumer, farmer=farmer).exists():
                subscribed_farmers.append(farmer)
            else: 
                unsubscribed_farmers.append(farmer)
        
        print(subscribed_farmers)
        print(unsubscribed_farmers)

        bootpay = BootpayApi(application_id=REST_API_KEY, private_key=PRIVATE_KEY)
        result = bootpay.get_access_token()

        if result["status"] == 200:
            verify_result = bootpay.verify(receipt_id)

            if verify_result["status"] == 200:
                if (
                    verify_result["data"]["price"] == total_price
                    and verify_result["data"]["status"] == 1
                ):
                    ctx = {
                        "order_info": order,
                        "data": verify_result,
                        "orders": orders,
                        "sub_farmers": subscribed_farmers,
                        "unsub_farmers": unsubscribed_farmers,
                    }

                    nowDatetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"=== PAYMENT VALIDATION SUCCESS : {nowDatetime} ===")
                    print(f"=== RECIPT ID : {receipt_id} ===")

                    return render(request, "orders/payment_success.html", ctx)

        else:
            cancel_result = bootpay.cancel(
                receipt_id, total_price, request.user.nickname, "결제검증 실패로 인한 결제 취소"
            )

            if cancel_result["status"] == 200:
                ctx = {"cancel_result": cancel_result}
                return redirect(
                    reverse("orders:payment_fail", kwargs={"errorType": "error_valid", "orderGroupPk" : order_group_pk})
                )

            else:
                ctx = {
                    "cancel_result": "결제 검증에 실패하여 결제 취소를 시도하였으나 실패하였습니다. 고객센터에 문의해주세요"
                }
                return redirect(
                    reverse("orders:payment_fail", kwargs={"errorType": "error_server", "orderGroupPk" : order_group_pk})
                )

    return HttpResponse("잘못된 접근입니다", status=400)


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
