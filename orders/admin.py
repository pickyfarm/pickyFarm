from django.contrib import admin
from django.db import transaction
from django.utils import translation
from kakaomessages.views import send_kakao_message
from kakaomessages.template import templateIdList
from django.utils.translation import ngettext
from django.contrib import messages
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

    actions = ['order_complete']

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

        

    order_complete.short_description = "배송 완료 처리"





@admin.register(models.RefundExchange)
class RefundExchangeAdmin(admin.ModelAdmin):
    pass
