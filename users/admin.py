from django.contrib import admin
from users import models

# Register your models here.


@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Consumer)
class CustomConsumerAdmin(admin.ModelAdmin):
    pass


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
class PhoneNumberAuth(admin.ModelAdmin):
    pass
