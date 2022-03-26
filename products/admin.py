from django.contrib import admin, messages
from django.db import transaction
from products import models
from users.models import Subscribe
from kakaomessages.views import send_kakao_message
from kakaomessages.template import templateIdList

# Register your models here.


@admin.register(models.Product)
class CustomProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "sell_price",
    )

    actions = ["change_product_commission_rate", "apply_discount"]

    @transaction.atomic
    def change_product_commission_rate(self, request, queryset):
        for product in queryset:
            product.commision_rate = 18.0
            product.save()

        self.message_user(request, f"{len(queryset)}개의 상품의 수수료율을 변경하였습니다.", messages.SUCCESS)

    def apply_discount(self, request, queryset):
        for product in queryset:
            if product.modify_count:
                self.message_user(request, f"{product.title}은 이미 변경되었습니다!", messages.ERROR)
                return

            if product.discount_price == 0:
                self.message_user(request, f"{product.title}의 할인 금액이 설정되지 않았습니다!", messages.ERROR)
                return

            product.sell_price -= product.discount_price
            product.save()

    apply_discount.short_description = "상품 할인가 적용하기"


@admin.register(models.Product_Group)
class CustomProductGroupAdmin(admin.ModelAdmin):
    actions = ["send_product_open_message"]

    @transaction.atomic
    def send_product_open_message(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(request, "두개 이상의 농가의 상품에 대해 메세지를 보낼 수 없습니다.", messages.ERROR)
            return

        farmer = queryset.first().products.first().farmer

        product = queryset.first()

        if product.open:
            self.message_user(request, "승인 대기중인 상품이 아닙니다.", messages.ERROR)
            return

        product.open = True
        siblings = product.products.all()

        main_product = siblings.first()
        main_product.main_product = True
        main_product.save()

        product.save()
        for sibling in siblings:
            sibling.open = True
            sibling.status = "sale"
            sibling.save()

        sub_users = list(farmer.subs.all().values_list("consumer__user__phone_number", flat=True))

        args_kakao = {
            "#{farm_name}": farmer.farm_name,
            "#{link_1}": f"www.pickyfarm.com/product/detail/{main_product.pk}",
            "#{link_2}": f"www.pickyfarm.com/farmer/farmer_detail/{farmer.pk}",
        }

        send_kakao_message(sub_users, templateIdList["new_product"], args_kakao)
        self.message_user(request, f"{len(sub_users)}명에게 메세지를 보냈습니다.", messages.SUCCESS)


@admin.register(models.Product_Image)
class CustomProduct_ImageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CustomCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Question)
class CustomQnAAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Answer)
class CustomQnAAdmin(admin.ModelAdmin):
    pass
