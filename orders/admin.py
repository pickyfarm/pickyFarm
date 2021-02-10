from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Order_Group)
class CustomOrderGroupAdmin(admin.ModelAdmin):
    list_display = (
        'consumer',
        'status',
        'total_price',
        'total_quantity',
        'order_at',
        'rev_address', 
        'rev_name', 
        'rev_loc_at',
        'rev_loc_detail',
        'rev_message',
        'update_at',
        'create_at',
    )


@admin.register(models.Order_Detail)
class CustomOrderDetailAdmin(admin.ModelAdmin):
    list_display = (
        'status',
        'product',
        'order_group',
        'invoice_number',
        'quantity',
        'total_price',
        'cancel_reason',
        'update_at',
        'create_at',
    )
