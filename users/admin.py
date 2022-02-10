from django.contrib import admin
from users import models

# Register your models here.


@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Consumer)
class CustomConsumerAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "consumer_name",
        "benefit_agree",
        "kakao_farmer_agree",
        "kakao_comment_agree",
    )

    list_filter = (
        "benefit_agree",
        "kakao_farmer_agree",
        "kakao_comment_agree",
    )

    @admin.display(description="소비자 이름")
    def consumer_name(self, consumer):
        return consumer.user.account_name

    @admin.display(description="소비자 전화번호")
    def consumer_phone_number(self, consumer):
        return consumer.user.phone_number

    search_fields = ["user__account_name"]


@admin.register(models.Editor)
class CustomEditorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Wish)
class CustomWishAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Cart)
class CustomCartAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PhoneNumberAuth)
class PhoneNumberAuthAdmin(admin.ModelAdmin):
    pass
