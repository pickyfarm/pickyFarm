from django.contrib import admin
from users import models

# Register your models here.

@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
	pass

@admin.register(models.Consumer)
class CustomConsumerAdmin(admin.ModelAdmin):
	pass

@admin.register(models.Farmer)
class CustomFarmerAdmin(admin.ModelAdmin):
	pass

@admin.register(models.Farm_Image)
class CustomFarm_ImageAdmin(admin.ModelAdmin):
	pass

@admin.register(models.Farm_Tag)
class CustomFarm_TagAdmin(admin.ModelAdmin):
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