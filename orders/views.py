from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import Order_Group_Form
from .models import Order_Group, Order_Detail
from django.utils import timezone
from products.models import Product
import requests, base64
import json
import os
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
def payment_create(request):
    consumer = request.user.consumer
    if request.method == "POST":
        form = Order_Group_Form()
        orders = json.loads(request.POST.get("orders"))
        print(orders)
        # 주문 상품 list (주문 수량, 주문 수량 고려한 가격, 주문 수량 고려한 무게)
        products = []
        # 총 주문 상품 개수
        total_quantity = 0
        # 총 주문 상품 무게
        total_weight = 0
        # 총 주문 상품 가격의 합
        price_sum = 0

        order_group = Order_Group(status="wait", consumer=consumer)
        order_group.save()
        order_group_pk = order_group.pk

        # order_group pk와 주문날짜를 기반으로 order_group 주문 번호 생성
        order_group_management_number = create_order_group_management_number(
            order_group_pk
        )
        order_group.order_management_number = order_group_management_number
        order_group.save()

        # 부트페이 API로 보내기 위한 name parameter 뒤에 들어갈 숫자 정보 ex) 맛있는 딸기 외 3개
        order_detail_cnt = 0
        # 부트페이 API로 보내기 위한 name parameter
        order_group_name = ""

        for order in orders:

            order_detail_cnt += 1

            pk = (int)(order["pk"])
            quantity = (int)(order["quantity"])
            print(f"{pk}:{quantity}")

            product = Product.objects.get(pk=pk)
            # order_detail 구매 수량
            total_quantity += quantity
            # order_detail 구매 총액
            total_price = product.sell_price * quantity

            # 결제 대기 상태의 order_detail 생성
            # order_group으로 묶어줌
            # (수정 사항) order_detail 주문 관리 번호 들어가야 함
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

        delivery_fee = 0  # 추후 배송비 관련 전략 생길 시 작성
        discount = 0  # 추후 할인 전략 도입 시 작성
        print(total_weight)
        # 최종 주문 금액
        final_price = price_sum + delivery_fee + discount

        order_group.total_price = final_price
        order_group.total_quantity = total_quantity
        order_group.save()
        print(order_group.pk)
        ctx = {
            "order_group_name": order_group_name,
            "form": form,
            "consumer": consumer,
            "products": products,
            "total_quantity": total_quantity,
            "price_sum": price_sum,
            "discount": discount,
            "delivery_fee": delivery_fee,
            "final_price": final_price,
            "total_weight": round(total_weight, 2),
            "order_group_pk": int(order_group.pk),
        }

        return render(request, "orders/payment.html", ctx)


@login_required
@require_POST
# 배송 정보가 입력된 후 oreder_group에 update
def payment_update(request, pk):
    consumer = request.user.consumer

    # if request.method == 'GET':
    #     form = Order_Group_Form()
    #     order_products = json.loads(request.GET.get('orders'))
    #     print("왔다")
    #     print(order_products)
    #     ctx = {
    #         'form': form,
    #         'consumer': consumer,
    #     }
    #     print("여기까지 오니?")
    #     return render(request, 'orders/payment.html', ctx)
    if request.method == "POST":
        # form = Order_Group_Form(request.POST)
        # GET Parameter에 있는 order_group pk를 가져옴
        order_group_pk = pk

        # Order_Group DB에서 찾아서 가져옴
        order_group = Order_Group.objects.get(pk=order_group_pk)

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

        rev_name = request.POST.get("rev_name")
        rev_phone_number = request.POST.get("rev_phone_number")
        rev_loc_at = request.POST.get("rev_loc_at")
        rev_message = request.POST.get("rev_message")
        to_farm_message = request.POST.get("to_farm_message")

        print(rev_name + rev_phone_number + rev_loc_at + rev_message + to_farm_message)

        order_at = timezone.now()
        print(order_group)
        # 배송 정보 order_group에 업데이트
        # rev address, total_price, total_quantity 추후 작업
        order_group.rev_name = rev_name
        order_group.rev_address = "추후작업"
        order_group.rev_phone_number = rev_phone_number
        order_group.rev_loc_at = rev_loc_at
        # order_group.rev_loc_detail=rev_loc_detail
        order_group.rev_message = rev_message
        order_group.to_farm_message = to_farm_message
        # order_group.payment_type=payment_type
        order_group.save()

        # return redirect(reverse("users:mypage", kwargs={'cat': 'orders'}))
        return JsonResponse(
            {"orderId": "temp", "orderName": "temp", "customerName": "nameTemp"}
        )

    pass


@login_required
def payment_success(request):

    if request.method == "GET":
        # 결제 승인을 위해 사용되는 키값
        # 이 키를 http header에 넣어서 결제 승인 api를 요청
        payment_key = request.GET.get("paymentKey", None)
        print(f"페이먼트 키 : {payment_key}")
        # 주문 고유 id
        order_id = request.GET.get("orderId", None)
        # 결제할 금액 (비교 금액)
        amount_ready = request.GET.get("amount_ready")
        # 실제 결제한 금액
        amount_paid = request.GET.get("amount")
        if (payment_key is not None) and (order_id is not None):
            if amount_ready == amount_paid:
                data = {
                    "orderId": order_id,
                    "amount": amount_paid,
                }
                # PG사에서 제공해주는 client ID and Client Passwords
                usr_pass = b"test_sk_BE92LAa5PVb64R41qaPV7YmpXyJj:"
                # b64로 암호화
                b64_val = base64.b64encode(usr_pass).decode("utf-8")

                auth_request = requests.post(
                    f"https://api.tosspayments.com/v1/payments/{payment_key}",
                    headers={
                        # 추후 authorization token이 들어가야 함
                        "Authorization": f"Basic {b64_val}",
                        "Content-Type": "application/json",
                    },
                    json=data,
                )
                print(auth_request.json())
                if auth_request:
                    # 여기서 order group 과 order detail의 결제 상태를 완료로 변경해주어야함
                    ctx = {
                        "order_id": order_id,
                        "amount": amount_paid,
                    }
                    return render(request, "orders/payment_success.html", ctx)
                else:
                    return redirect(reverse("orders:payment_fail"))
            else:
                return redirect(reverse("orders:payment_fail"))
        else:
            return redirect(reverse("orders:payment_fail"))


@login_required
def payment_fail(request):
    ctx = {"msg": "실패"}
    return render(request, "orders/payment_fail.html", ctx)


@login_required
def payment_valid(request):
    if request.method == "POST":
        REST_API_KEY = os.environ.get("BOOTPAY_REST_KEY")
        PRIVATE_KEY = os.environ.get("BOOTPAY_PRIVATE_KEY")
        receipt_id = request.POST.get("receipt_id")
        total_price = int(request.POST.get("price"))
        print(REST_API_KEY, PRIVATE_KEY)

        bootpay = BootpayApi(
            application_id=REST_API_KEY, private_key=PRIVATE_KEY, mode="development"
        )
        print("--- atfer call BootpayApi() ---")
        result = bootpay.get_access_token()
        print("--- atfer get access token ---")
        pprint.pprint(result)

        if result["status"] == 200:
            verify_result = bootpay.verify(receipt_id)
            pprint.pprint(verify_result)

            if verify_result["status"] == 200:
                if (
                    verify_result["data"]["price"] == total_price
                    and verify_result["data"]["status"] == 1
                ):
                    ctx = {"data": verify_result}

                    return render(request, "orders/payment_success.html", ctx)

        while True:
            cancel_result = bootpay.cancel(
                receipt_id, total_price, request.user.nickname, "결제검증 실패로 인한 결제 취소"
            )

            if cancel_result["status"] == 200:
                ctx = {"cancel_result": cancel_result}
                return render(request, "orders/payment_fail.html", ctx)

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
