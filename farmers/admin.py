from django.contrib import admin
from farmers import models

# Register your models here.
@admin.register(models.Farmer)
class CustomFarmerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Farmer_Story)
class CustomFarmer_StoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Farm_Tag)
class CustomFarm_TagAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Farm_Apply)
class CustomFarm_ApplyAdmin(admin.ModelAdmin):
    pass
