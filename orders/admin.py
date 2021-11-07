from django.contrib import admin
from django.db import transaction
from django.utils import translation
from kakaomessages.views import send_kakao_message
from kakaomessages.template import templateIdList
from django.utils.translation import ngettext
from django.contrib import messages
from django.db.models import Q, F, Aggregate, Sum, Value, IntegerField, FloatField
from . import models

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




@admin.register(models.Order_Detail)
class CustomOrderDetailAdmin(admin.ModelAdmin):
    list_display = (
        "status",
        'payment_status',
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

    list_filter = ('status', 'payment_status', 'product')

    search_fields = ['order_management_number']

    actions = ['order_complete', 'payment_status_progress', 'payment_status_done', 'calculate_amount']

    @transaction.atomic
    def order_complete(self, request, queryset):
         # order_Detail 돌면서 배송완료, 카카오알림톡 보내기
        print(queryset)
        queryset_len = len(queryset)

        all_success = True
        fail_list = list()
        idx = 0
        for order in list(queryset):
            idx +=1
            if order.status != 'shipping':
                all_success = False
                fail_list.append(idx)
                continue
                

            order.status = "delivery_complete"
            user = order.order_group.consumer.user

            consumer_nickname = user.nickname
            phone_number = user.phone_number

            farmer = order.product.farmer
            farmer_pk = farmer.pk
            farmer_nickname = farmer.user.nickname

            order_pk = order.pk

            args = {
                "#{consumer_nickname}" : consumer_nickname,
                "#{farmer_nickname}" : farmer_nickname,
                "#{link_1}" : f"www.pickyfarm.com/user/mypage/orders/{order_pk}/review/create",
                "#{link_2}" : f"www.pickyfarm.com/farmer/farmer_detail/{farmer_pk}/"
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
            idx +=1
            if order.status != "delivery_complete" or order.payment_status == 'none':
                all_success = False
                fail_list.append(idx)
                continue
                

            order.payment_status = "progress"
            order.save()

        if all_success == True:
            self.message_user(request, f"{queryset_len}개의 주문이 정산 진행 처리 되었습니다", messages.SUCCESS)
        else:
            self.message_user(request, f"[결제 이전] 이거나 [배송 완료] 상태가 아닌 주문이 있습니다. : {fail_list}", messages.ERROR)

    @transaction.atomic
    def payment_status_done(self, request, queryset):
        print(queryset)
        queryset_len = len(queryset)

        all_success = True
        fail_list = list()
        idx = 0
        for order in list(queryset):
            idx +=1
            if order.payment_status != 'progress':
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
        for order in list(queryset):
            idx +=1
            if order.payment_status != 'progress':
                all_success = False
                fail_list.append(idx)
                continue
        

        if all_success == True:
            progress_amount = queryset.filter(payment_status="progress").aggregate(
            total=Sum(
                (
                    F("total_price")
                    * ((Value(100.0) - F("commision_rate")) / Value(100.0))
                ), output_field=FloatField()
            )
        )["total"]
            self.message_user(request, f"{queryset_len} 개의 항목 정산 금액 : {progress_amount}원", messages.SUCCESS)
        else:
            self.message_user(request, f"[정산 진행] 상태가 아닌 주문이 있습니다. : {fail_list}", messages.ERROR)


    order_complete.short_description = "[주문관리] 배송 완료 처리"
    payment_status_progress.short_description = "[정산관리] 정산 진행 처리"
    payment_status_done.short_description = "[정산관리] 정산 완료 처리"
    calculate_amount.short_description = "[정산 관리] 정산 진행 항목 정산 금액 계산"






@admin.register(models.RefundExchange)
class RefundExchangeAdmin(admin.ModelAdmin):
    pass
