from addresses.models import Address
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.utils import timezone
from editor_reviews.models import Editor_Review
from core.models import CompressedImageField
from config import settings
import comments
import os
import shutil
import datetime
from random import randint
from kakaomessages.template import templateIdList
from kakaomessages.views import send_kakao_message


# Create your models here.

# image default 파일 생성하기 <- 배포전
# def default_profile_image():

#     if not os.path.exists(os.path.join(settings.BASE_DIR, 'media/default/profile_default.png')):
#         # os.makedirs(os.path.join(settings.BASE_DIR, 'media/default'))
#         print("media/default 폴더 생성 완료")
#         shutil.copy(os.path.join(settings.STATIC_ROOT, 'images/default/profile_default.png'),
#                os.path.join(settings.MEDIA_ROOT, 'default/profile_default.png'))


class User(AbstractUser):
    GENDER_CHOICES = (
        ("male", "남자"),
        ("female", "여자"),
    )

    phone_number = models.CharField(max_length=11)
    account_name = models.CharField(max_length=10)
    profile_image = CompressedImageField(upload_to="profile_image/%Y/%m/%d/", null=True, blank=True)
    nickname = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    birth = models.DateField(null=True)
    # location = models.ForeignKey(Product,
    #                              related_name="consumers", on_delete=models.SET_NULL)
    # number = models.CharField(max_length=20)
    superhost = models.BooleanField(default=False)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def FindMyIdInAsterisk(self):
        src = self.username[:-3]
        src = src + "***"

        return src

    def get_full_name(self):
        full_name = "%s%s" % (self.last_name, self.first_name)
        return full_name.strip()

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

    user = models.OneToOneField(User, related_name="consumer", on_delete=models.CASCADE)
    grade = models.IntegerField(choices=grade, default=1)
    default_address = models.OneToOneField(
        "addresses.Address",
        related_name="consumer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    benefit_agree = models.BooleanField(default=False)
    kakao_farmer_agree = models.BooleanField(default=False)
    kakao_comment_agree = models.BooleanField(default=False)

    def __str__(self):
        return self.user.nickname


class Editor(models.Model):
    user = models.OneToOneField(
        User,
        default=None,
        null=True,
        blank=True,
        related_name="editor",
        on_delete=models.CASCADE,
    )

    def review_count(self):
        return Editor_Review.objects.filter(author=self).count()

    def review_hit_count(self):
        reviews = Editor_Review.objects.filter(author=self)
        count = 0

        for review in reviews:
            count += review.hits

        return count

    def unread_comment_count(self):
        count = 0

        try:
            reviews = Editor_Review.objects.filter(author=self)

            for review in reviews:
                try:
                    unread_comments = comments.models.Editor_Review_Comment.objects.filter(
                        editor_review=review, is_read=False
                    ).count()

                    count += unread_comments
                except ObjectDoesNotExist:
                    pass

        except ObjectDoesNotExist:
            pass

        return count

    def __str__(self):
        return self.user.nickname


class Wish(models.Model):
    consumer = models.ForeignKey("Consumer", related_name="wishes", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", related_name="wishes", on_delete=models.CASCADE)

    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.consumer.user.nickname} -> {self.product.title}"


class Cart(models.Model):
    consumer = models.ForeignKey("Consumer", related_name="carts", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", related_name="carts", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.consumer.user.nickname} -> {self.product.title}"


# class Staffs_Image(models.Model):
#     image = CompressedImageField(upload_to='/staffs_images')
#     update_at = models.DateTimeField(auto_now=True)
#     create_at = models.DateTimeField(auto_now_add=True)
#     review = models.ForeignKey('Staffs', on_delete=models.CASCADE)


class Subscribe(models.Model):
    farmer = models.ForeignKey("farmers.Farmer", related_name="subs", on_delete=models.CASCADE)
    consumer = models.ForeignKey("users.Consumer", related_name="subs", on_delete=models.CASCADE)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.consumer.user.nickname} -> {self.farmer.farm_name}"


class PhoneNumberAuth(models.Model):
    phone_num = models.CharField(max_length=11, verbose_name="전화번호")
    auth_num = models.CharField(max_length=6, verbose_name="인증번호")
    create_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.phone_num
