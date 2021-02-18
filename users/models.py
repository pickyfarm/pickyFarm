from django.db import models
from django.contrib.auth.models import AbstractUser
from config import settings
import os
import shutil
# Create your models here.

#image default 파일 생성하기 <- 배포전
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

    profile_image = models.ImageField(
        upload_to='profile_image/%Y/%m/%d/', null=True, blank=True)
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
        full_name = '%s%s' % (self.last_name, self.first_name)
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

    user = models.OneToOneField(
        User, related_name='consumer', on_delete=models.CASCADE)

    grade = models.IntegerField(choices=grade, default=1)

    def __str__(self):
        return self.user.nickname


class Editor(models.Model):
    user = models.OneToOneField(
        User, default=None, null=True, blank=True, related_name='editor', on_delete=models.CASCADE)


class Farmer(models.Model):
    CAT_CHOICES = (
        ("vege", "채소"),
        ("fruit", "과일"),
        ("etc", "기타"),
    )
    farm_name = models.CharField(max_length=50) # 농장 이름
    farmer_profile = models.ImageField(upload_to='farmer_profile/%Y/%m/%d/', null=True, blank=True) # 농장주 사진 default icon 설정
    farm_profile = models.ImageField(upload_to='farm_profile/%Y/%m/%d/') # 농장 대표사진 or 로고
    profile_title = models.CharField(max_length=200) # 농가 한 줄 소개
    profile_desc = models.TextField() # 농가 상세 소개
    sub_count = models.IntegerField(default=0) # 구독자 수
    farm_news = models.CharField(max_length=500, null=True, blank=True) # 농가 뉴스
    farm_cat = models.CharField(choices=CAT_CHOICES, max_length=20, default="vege")
    user = models.OneToOneField(
        User, related_name='farmer', on_delete=models.CASCADE)

    def __str__(self):
        return self.farm_name

    def inc_sub(self):
        self.sub_count += 1
        return


class Farmer_Story(models.Model):
    farmer = models.ForeignKey(
        'Farmer', related_name='farmer_stories', on_delete=models.CASCADE) # 작성자
    title = models.CharField(max_length=50) # 제목
    content = models.TextField() # 내용
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.farmer} story - {self.title}'
    


class Farm_Tag(models.Model):
    tag = models.CharField(max_length=30)
    farmer = models.ManyToManyField(
        Farmer, related_name='farm_tags')

    def __str__(self):
        return self.tag


class Wish(models.Model):
    consumer = models.ForeignKey(
        'Consumer', related_name="wishes", on_delete=models.CASCADE)
    product = models.ForeignKey(
        "products.Product", related_name='wishes', on_delete=models.CASCADE)
    
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.consumer.user.nickname} -> {self.product.title}'


class Cart(models.Model):
    consumer = models.ForeignKey(
        'Consumer', related_name="carts", on_delete=models.CASCADE)
    product = models.ForeignKey(
        "products.Product", related_name='carts', on_delete=models.CASCADE)
    quantitiy = models.IntegerField(default=1, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.consumer.user.nickname} -> {self.product.title}'

# class Staffs_Image(models.Model):
#     image = models.ImageField(upload_to='/staffs_images')
#     update_at = models.DateTimeField(auto_now=True)
#     create_at = models.DateTimeField(auto_now_add=True)
#     review = models.ForeignKey('Staffs', on_delete=models.CASCADE)


class Subscribe(models.Model):
    farmer = models.ForeignKey(
        'Farmer', related_name="subs", on_delete=models.CASCADE)
    consumer = models.ForeignKey(
        'Consumer', related_name="subs", on_delete=models.CASCADE)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.consumer.user.nickname} -> {self.farmer.farm_name}'

