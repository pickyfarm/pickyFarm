from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Product_Comment)
class ProductCommentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Product_Recomment)
class ProductRecommentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Product_Comment_Image)
class ProductCommentImageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Editor_Review_Comment)
class EditorReviewCommentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Editor_Review_Recomment)
class EditorReviewRecommentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Farmer_Story_Comment)
class FarmerStoryCommentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Farmer_Story_Recomment)
class FarmerStoryRecommentAdmin(admin.ModelAdmin):
    pass