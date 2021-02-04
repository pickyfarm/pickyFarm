from django.db import models

# Create your models here.


class Main_Slider_Image(models.Model):

    image = models.ImageField(upload_to='main_slider_images/%%Y/%%m/%%d')
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)


class NoQuerySet(Exception):
    pass

class AuthorNotMatched(Exception):
    pass