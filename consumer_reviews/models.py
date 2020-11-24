from django.db import models

# Create your models here.
class Consumer_Reviews(models.Model):

    title = models.TextField()
    contents = models.TextField()
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("staff")


class Consumer_Reviews_Image(models.Model):

    image = models.ImageField(upload_to='/consumer_review_images')
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey('Consumer_Reviews')