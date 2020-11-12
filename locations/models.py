from django.db import models

# Create your models here.


class Location(models.Model):

    city = models.CharField(max_length=20)
    sigungu = models.CharField(max_length=30)
    dong = models.CharField(max_length=30, blank=True)
    ri = models.CharField(max_length=20, blank=True)
    doro = models.CharField(max_length=50)
    detail = models.CharField(max_length=50, blank=True)