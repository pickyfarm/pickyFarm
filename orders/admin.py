from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db import transaction
from django.utils import translation
from kakaomessages.views import send_kakao_message
from kakaomessages.template import templateIdList
from django.utils.translation import ngettext
from django.contrib import messages
from django.db.models import Q, F, Aggregate, Sum, Value, IntegerField, FloatField
from . import models
from farmers.models import Farmer
from rangefilter.filters import DateRangeFilter
from orders.views import send_kakao_with_payment_complete

# Register your models here.


@admin.register(models.Order_Group)
class CustomOrderGroupAdmin(admin.ModelAdmin):
    list_display = (
        "consumer",
        "status",
        "total_price",
        "total_quantity",
        "order_at",
        "rev_address",
        "rev_name",
        "rev_loc_at",
        "rev_loc_detail",
        "rev_message",
        "update_at",
        "create_at",
    )

    actions = ["send_payment_complete_kakao_message"]

    # 농가, 소비자에게 결제완료 알림톡 전송
    def send_payment_complete_kakao_message(self, request, queryset):
        send_kakao_with_payment_complete(self.pk, "")

        self.message_user(
            request,
            f"{queryset_len}개의 주문에 대해 알림톡을 전송했습니다. receipt_id는 직접 넣어주시기 바랍니다.",
            messages.SUCCESS,
        )

    send_payment_complete_kakao_message.short_description = "[주문관리] 농가, 소비자에게 결제완료 알림톡 전송"

    list_filter = ("consumer_type", "order_type")


class OrderDetailFarmerFilter(SimpleListFilter):
    title = "농가 기준으로 필터링"
    parameter_name = "farmer"

    def lookups(self, request, model_admin):
        farmers = Farmer.objects.all()
        farmer_list = [(farm.farm_name, farm.farm_name) for farm in farmers]

        return farmer_list

    def queryset(self, request, queryset):
        return (
            queryset.filter(product__farmer__farm_name=self.value()) if self.value() else queryset
        )


@admin.register(models.Order_Detail)
class CustomOrderDetailAdmin(admin.ModelAdmin):
    list_display = (
        "status",
        "payment_status",
        "order_management_number",
        "product",
        "order_group",
        "delivery_service_company",
        "invoice_number",
        "quantity",
        "total_price",
        "cancel_reason",
        "update_at",
        "create_at",
    )

    list_filter = (
        "status",
        "payment_status",
        "product",
        OrderDetailFarmerFilter,
        ("create_at", DateRangeFilter),
    )

    search_fields = ["order_management_number"]

    actions = [
        "order_complete",
        "payment_status_progress",
        "payment_status_done",
        "calculate_amount",
        "send_delivery_start_message_to_consumer",
    ]

    # change_list_template = "admin/orders/order_detail/change_list.html"

    @transaction.atomic
    def order_complete(self, request, queryset):
        # order_Detail 돌면서 배송완료, 카카오알림톡 보내기
        print(queryset)
        queryset_len = len(queryset)

        all_success = True
        fail_list = list()
        idx = 0
        for order in list(queryset):
            idx += 1
            if order.status != "shipping":
                all_success = False
                fail_list.append(idx)
                continue

            order.status = "delivery_complete"

            order_group = order.order_group
            # 회원 구매인 경우
            if order_group.consumer_type == "user":
                user = order_group.consumer.user
                consumer_nickname = user.nickname
                phone_number = user.phone_number
            # 비회원 구매인 경우
            else:
                consumer_nickname = order_group.orderer_name
                phone_number = order_group.orderer_phone_number

            farmer = order.product.farmer
            farmer_pk = farmer.pk
            farmer_nickname = farmer.user.nickname

            order_pk = order.pk

            args = {
                "#{consumer_nickname}": consumer_nickname,
                "#{farmer_nickname}": farmer_nickname,
                "#{link_1}": f"www.pickyfarm.com/user/mypage/orders/{order_pk}/review/create",
                "#{link_2}": f"www.pickyfarm.com/farmer/farmer_detail/{farmer_pk}/",
            }

            send_kakao_message(phone_number, templateIdList["delivery_complete"], args)
            order.save()

        if all_success == True:
            self.message_user(request, f"{queryset_len}개의 주문이 배송 완료 처리 되었습니다", messages.SUCCESS)
        else:
            self.message_user(request, f"[배송중] 상태가 아닌 주문이 있습니다 : {fail_list}", messages.ERROR)

    @transaction.atomic
    def payment_status_progress(self, request, queryset):
        print(queryset)
        queryset_len = len(queryset)

        all_success = True
        fail_list = list()
        idx = 0
        for order in list(queryset):
            idx += 1
            if order.status != "delivery_complete" or order.payment_status == "none":
                all_success = False
                fail_list.append(idx)
                continue

            order.payment_status = "progress"
            order.save()

        if all_success == True:
            self.message_user(request, f"{queryset_len}개의 주문이 정산 진행 처리 되었습니다", messages.SUCCESS)
        else:
            self.message_user(
                request, f"[결제 이전] 이거나 [배송 완료] 상태가 아닌 주문이 있습니다. : {fail_list}", messages.ERROR
            )

    @transaction.atomic
    def payment_status_done(self, request, queryset):
        print(queryset)
        queryset_len = len(queryset)

        all_success = True
        fail_list = list()
        idx = 0
        for order in list(queryset):
            idx += 1
            if order.payment_status != "progress":
                all_success = False
                fail_list.append(idx)
                continue

            order.payment_status = "done"
            order.save()

        if all_success == True:
            self.message_user(request, f"{queryset_len}개의 주문이 정산 완료 처리 되었습니다", messages.SUCCESS)
        else:
            self.message_user(request, f"[정산 진행] 상태가 아닌 주문이 있습니다. : {fail_list}", messages.ERROR)

    # 농가에게 정산해주어야 할 금액 계산
    # 조건 : Product가 같아야함 / 정산 진행 중인 상태여야함 /
    @transaction.atomic
    def calculate_amount(self, request, queryset):
        print(queryset)
        queryset_len = len(queryset)

        all_success = True
        fail_list = list()
        idx = 0
        # for order in list(queryset):
        #     idx += 1
        #     if order.payment_status != "progress":
        #         all_success = False
        #         fail_list.append(idx)
        #         continue

        if all_success == True:
            # 전체금액: 매출 합계
            # PG 수수료: 매출 * 결제수단별 수수료율
            # 정산 금액: 매출 * (1- 상품별 수수료율) (0.82)
            # 피키팜 순이익: 전체금액 - (PG수수료 + 정산 금액)
            CARD_COMMISSION = 0.028
            VBANK_COMMISSION = 300
            KAKAO_COMMISSION = 0.03

            overall_amount = queryset.aggregate(total=Sum("total_price"))["total"]

            card_commission = (
                queryset.filter(order_group__payment_type="card").aggregate(
                    total=Sum(F("total_price") * Value(CARD_COMMISSION))
                )["total"]
                or 0
            )
            vbank_commission = (
                queryset.filter(order_group__payment_type="vbank").count()
            ) * VBANK_COMMISSION
            kakao_commission = (
                queryset.filter(order_group__payment_type="kakao").aggregate(
                    total=Sum(F("total_price") * Value(KAKAO_COMMISSION))
                )["total"]
                or 0
            )

            inicis_commission = card_commission + vbank_commission + kakao_commission

            progress_amount = queryset.aggregate(
                total=Sum(
                    (F("total_price") * ((Value(100.0) - F("commision_rate")) / Value(100.0))),
                    output_field=FloatField(),
                )
            )["total"]

            net_amount = overall_amount - (inicis_commission + progress_amount)
            self.message_user(
                request,
                f"""{queryset_len} 개의 항목 | 
                전체 금액: {overall_amount}원 | 
                정산 금액: {progress_amount}원 | 
                PG 수수료: {inicis_commission}원 | 
                피키팜 순이익: {net_amount}원""",
                messages.SUCCESS,
            )
        else:
            self.message_user(request, f"[정산 진행] 상태가 아닌 주문이 있습니다. : {fail_list}", messages.ERROR)

    def send_delivery_start_message_to_consumer(self, request, queryset):
        """소비자에게 배송시작 알림톡 재 전송 ADMIN ACTION"""
        passed_order = 0  # 전송하지 않은 주문 건수 카운트
        user_order = 0

        for order in queryset:
            if order.status != "shipping":
                passed_order += 1
                continue

            if order.order_group.consumer_type == "user":
                user_order += 1
                continue

            order_group = order.order_group

            # 카카오 알림톡 전송을 위한 결제자 번호
            phone_number_consumer = order_group.orderer_phone_number
            print(f"[송장 입력 팝업 - POST] Consumer phone number : {phone_number_consumer}")

            # 주문 상품
            product = order.product
            # 파머
            farmer = product.farmer

            kakao_msg_weight = (str)(product.weight) + product.weight_unit

            kakao_msg_quantity = (str)(order.quantity) + "개"

            args_consumer = {
                "#{order_detail_title}": product.title,
                "#{farmer_nickname}": farmer.user.nickname,
                "#{option_name}": product.option_name,
                "#{quantity}": kakao_msg_quantity,
                "#{shipping_company}": order.get_delivery_service_company_display(),
                "#{invoice_number}": order.invoice_number,
            }

            # 소비자 결제 완료 카카오 알림톡 전송
            send_kakao_message(
                phone_number_consumer,
                templateIdList["delivery_start"],
                args_consumer,
            )

            # 선물하기 결제인 경우 선물 받는 사람 번호
            if order_group.order_type == "gift":
                phone_number_gift_rev = order.rev_phone_number_gift
                send_kakao_message(
                    phone_number_gift_rev,
                    templateIdList["delivery_start"],
                    args_consumer,
                )

        self.message_user(
            request,
            f"총 주문 {len(queryset)}건, 배송중이 아닌 주문 {passed_order}건, 회원 주문 {user_order}건, 발송 {len(queryset) - passed_order}건",
            messages.SUCCESS,
        )

    order_complete.short_description = "[주문관리] 배송 완료 처리"
    payment_status_progress.short_description = "[정산관리] 정산 진행 처리"
    payment_status_done.short_description = "[정산관리] 정산 완료 처리"
    calculate_amount.short_description = "[정산 관리] 정산 진행 항목 정산 금액 계산"
    send_delivery_start_message_to_consumer.short_description = "[주문관리] 소비자에게 배송 시작 알림톡 전송"


@admin.register(models.RefundExchange)
class RefundExchangeAdmin(admin.ModelAdmin):
    pass
