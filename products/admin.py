from django.contrib import admin
from products import models

# Register your models here.


@admin.register(models.Product)
class CustomProductAdmin(admin.ModelAdmin):
	list_display = (
		'title', 'sell_price', 
	)

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



