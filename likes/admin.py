from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.EditorReviewCommentLike)
class EditorReviewCommentLikeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.EditorReviewRecommentLike)
class EditorReviewRecommentLikeAdmin(admin.ModelAdmin):
    pass
