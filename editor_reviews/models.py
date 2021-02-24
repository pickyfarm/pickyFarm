from django.db import models
from products.models import Product, Category
from django_summernote import fields as summer_fields


class Editor_Review(models.Model):

    POST_CAT = (
        ('farm_cover', '농가 취재기'),
        ('products', '못난이 농산물'),
        ('recipe', '요리/레시피'),
    )

    title = models.CharField(max_length=500)
    sub_title = models.CharField(max_length=500)
    main_image = models.ImageField(
        upload_to='editor_review_thumbnail/%Y/%m/%d')
    contents = models.TextField()
    hits = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(
        "users.Editor", related_name="editor_reviews", on_delete=models.CASCADE)

    post_category = models.CharField(
        max_length=50, choices=POST_CAT, default='farm_cover')

    product = models.ManyToManyField(
        Product, related_name="editor_reviews", blank=True)
    farm = models.ForeignKey('users.Farmer', related_name="editor_reviews",
                             on_delete=models.SET_NULL, null=True, blank=True)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def get_preview(self):
        if len(self.contents) < 60:
            return self.contents
        else:
            return self.contents[:60]



class Editor_Review_Image(models.Model):

    image = models.ImageField(upload_to='editor_review_images')
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(
        Editor_Review, related_name="editor_review_images", on_delete=models.CASCADE)
