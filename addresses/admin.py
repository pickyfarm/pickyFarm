from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Address)
class AddressesAdmin(admin.ModelAdmin):
    pass