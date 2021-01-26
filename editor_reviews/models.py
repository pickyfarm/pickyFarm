from django.db import models
from products.models import Product, Category
from users.models import Editor
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.

class Editor_Reviews(models.Model):

    POST_CAT = (
        ('farm_cover','농가 취재기'),
        ('products','못난이 농산물'),
        ('recipe','요리/레시피'),
    )

    title = models.CharField(max_length=500, help_text="제목")
    main_image = models.ImageField(upload_to='editor_review_thumbnail/%%Y/%%m/%%d', help_text="썸네일")
    contents = RichTextUploadingField(blank=True, null=True, help_text="")
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    #author = models.ForeignKey(Editor, related_name="editor_reviews", on_delete=models.CASCADE)
    
    post_category = models.CharField(max_length=50, choices=POST_CAT, default='farm_cover', help_text="카테고리")

    product_category = models.ForeignKey(Category, related_name="editor_reviews", on_delete=models.CASCADE, null=True, blank=True, help_text="상품 종류")
    product = models.ForeignKey(Product, related_name="editor_reviews", on_delete=models.CASCADE, null=True, blank=True, help_text="상품")

    def get_preview(self):
        if len(self.contents) < 60:
            return self.contents
        else:
            return self.contents[:60]
    
    # def review_count(self):
    #     return Editor_Reviews.objects.filter(author=self.author.user.nickname).count()


class Editor_Reviews_Image(models.Model):

    image = models.ImageField(upload_to='editor_review_images')
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Editor_Reviews, related_name="editor_review_images", on_delete=models.CASCADE)