from django.contrib import admin
from products import models

# Register your models here.


@admin.register(models.Product)
class CustomProductAdmin(admin.ModelAdmin):
	pass

@admin.register(models.Category)
class CustomCategoryAdmin(admin.ModelAdmin):
	pass