from django.contrib import admin
from admins import models

# Register your models here.
@admin.register(models.FarmerNotice)
class CustomFarmerNoticeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FarmerNotification)
class CustomFarmerNotificationAdmin(admin.ModelAdmin):
    pass
