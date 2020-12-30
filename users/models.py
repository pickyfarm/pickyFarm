from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    GENDER_CHOICES = {
        ("male", "남자"),
        ("female", "여자"),
    }

    profile_image = models.ImageField(
        upload_to='profile_image/%Y/%m/%d/', null=True, blank=True)
    nickname = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    birth = models.DateField(null=True)
    # location = models.ForeignKey(Product,
    #                              related_name="consumers", on_delete=models.SET_NULL)
    superhost = models.BooleanField(default=False)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     if self.consumer is not None:
    #         return self.name.join(" ", "(소비자)")
    #     elif self.farmer is not None:
    #         return self.name.join(" ", "(농가)")
    #     elif self.editor is not None:
    #         return self.name.join(" ", "(에디터)")
    #     else:
    #         return self.name.join(" ", "(Staff)")


class Consumer(models.Model):
    grade = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    user = models.OneToOneField(
        User, default=None, null=True, blank=True, related_name='consumer', on_delete=models.CASCADE)

    grade = models.IntegerField(choices=grade)

    def __str__(self):
        return self.user.nickname


class Farmer(models.Model):
    farm_name = models.CharField(max_length=50)
    farm_news = models.CharField(max_length=500, blank=True)
    profile_title = models.CharField(max_length=200)
    profile_desc = models.TextField()

    contact = models.CharField(max_length=20, blank=True)

    user = models.OneToOneField(
        User, default=None, null=True, blank=True, related_name='farmer', on_delete=models.CASCADE)


class Editor(models.Model):

    user = models.OneToOneField(
        User, default=None, null=True, blank=True, related_name='editor', on_delete=models.CASCADE)


class Farm_Image(models.Model):
    image = models.ImageField(upload_to='farm_image/%Y/%m/%d/')

    farmer = models.ForeignKey(
        Farmer, on_delete=models.CASCADE, related_name='farm_images')


class Farm_Tag(models.Model):
    tag = models.CharField(max_length=30)

    farmer = models.ManyToManyField(
        Farmer)


class Wish(models.Model):
    consumer = models.ForeignKey(
        'Consumer', related_name="wishes", on_delete=models.CASCADE)
    product = models.ForeignKey(
        "products.Product", related_name='wishes', on_delete=models.CASCADE)

    def __str__(self):
        return self.consumer.name.join(" ", '찜하기')


class Cart(models.Model):
    consumer = models.ForeignKey(
        'Consumer', related_name="carts", on_delete=models.CASCADE)
    product = models.ForeignKey(
        "products.Product", related_name='carts', on_delete=models.CASCADE)

    def __str__(self):
        return self.consumer.name.join(" ", '장바구니')

# class Staffs_Image(models.Model):
#     image = models.ImageField(upload_to='/staffs_images')
#     update_at = models.DateTimeField(auto_now=True)
#     create_at = models.DateTimeField(auto_now_add=True)
#     review = models.ForeignKey('Staffs', on_delete=models.CASCADE)

class Subscribe(models.Model):
    farmer = models.ForeignKey('Farmer', related_name="subs", on_delete=models.CASCADE)
    consumer = models.ForeignKey('Consumer', related_name="subs", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.consumer.user.nickname} -> {self.farmer.farm_name}'