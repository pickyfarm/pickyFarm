from django.contrib import admin
from core import models

# Register your models here.

@admin.register(models.Main_Slider_Image)
class CustomMain_Slider_ImageAdmin(admin.ModelAdmin):
    pass