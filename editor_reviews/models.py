from django.db import models


# Create your models here.

class Editor_Reviews(models.Model):

    title = models.TextField()
    contents = models.TextField()
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    #author = models.ForeignKey("staff")
    product = models.ForeignKey("product")


class Editor_Reviews_Image(models.Model):

    image = models.ImageField(upload_to='editor_review_images')
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey('Editor_Reviews', related_name="editor_reviews", on_delete=models.CASCADE)