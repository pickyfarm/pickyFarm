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
from orders.models import Order_Detail
from orders.views import payment_valid_farmer, farmer_search

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
    profile_image = CompressedImageField(
        upload_to="profile_image/%Y/%m/%d/",
        null=True,
        blank=True,
        default="mainlogo_small.svg",
    )
    nickname = models.CharField(max_length=100)
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

    def send_kakao_payment_valid(self, order_group, payment_type):
        """소비자 결제 완료 카카오 알림톡 전송 함수"""
        """order_group, payment_type을 받아 결제 완료 알림톡을 소비자에게 전송한다"""

        phone_number = order_group.consumer.user.phone_number
        order_details = Order_Detail.objects.filter(order_group=order_group)

        # [Process #1] 구독농가 여부 판별
        farmers = list(set(map(lambda u: u.product.farmer, order_details)))
        unsubscribed_farmers = list()
        subscribed_farmers = list()
        farmers_info = []

        for farmer in farmers:
            farmers_info.append(
                payment_valid_farmer(
                    farmer.pk,
                    farmer.farm_name,
                    farmer.user.nickname,
                    farmer.user.phone_number,
                )
            )
            if Subscribe.objects.filter(consumer=order_group.consumer, farmer=farmer).exists():
                subscribed_farmers.append(farmer)
            else:
                unsubscribed_farmers.append(farmer)

        farmers_info = sorted(farmers_info, key=lambda x: x.farmer_pk)
        farmers_info_len = len(farmers_info)

        # [Process #2] 결제 완료 알림톡 전송
        for detail in order_details:
            if payment_type == "vbank":  # 가상계좌 결제 시
                detail.status = "payment_complete"
                detail.payment_status = "incoming"
                detail.save()
            else:
                pass

            farmer = farmer_search(farmers_info, detail.product.farmer.pk, 0, farmers_info_len)
            target_farmer_pk = detail.product.farmer.pk

            args = {
                "#{farm_name}": farmer.farm_name,
                "#{order_detail_number}": detail.order_management_number,
                "#{order_detail_title}": detail.product.title,
                "#{farmer_nickname}": farmer.farmer_nickname,
                "#{option_name}": detail.product.option_name,
                "#{quantity}": (str)(detail.quantity) + "개",
                "#{link_1}": f"www.pickyfarm.com/farmer/farmer_detail/{target_farmer_pk}",
                "#{link_2}": "www.pickyfarm.com/user/mypage/orders",
            }
            send_kakao_message(phone_number, templateIdList["payment_complete"], args)
        return


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
