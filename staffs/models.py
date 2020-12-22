from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Staffs(AbstractUser):
    name = models.CharField()
    nickname = models.CharField()
    status = models.IntegerField()


class Staffs_Image(models.Model):
    image = models.ImageField(upload_to='/staffs_images')
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey('Staffs', on_delete=models.CASCADE)

