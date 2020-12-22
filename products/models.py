from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=200)
    main_image = models.ImageField()
    open = models.BooleanField()

    price = models.IntegerField()
    weight = models.FloatField()
    stock = models.IntegerField()
    instruction = models.TextField(blank=True)

    desc = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    #farmer = models.ForeignKey('Farmer', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    #editor_review = models.ForeignKey('editor_review')


class Product_Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    image = models.ImageField()

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    KIND_BIG = (
        ('vege', '채소'),
        ('fruit', '과일'),
        ('else', '기타'),
    )
    KIND_SMALL_VEGE = (
        ('potato', '감자'),
        ('union', '양파'),
        ('carrot', '당근'),
        ('sweetp', '고구마'),
    )
    KIND_SMALL_FRUIT = (
        ('apple', '사과'),
        ('tomato', '토마토'),
        ('banana', '바나나'),
        ('pear', '배'),
    )
    KIND_SMALL_ELSE = (
        ('amu', '아무'),
        ('nothing', '무엇'),
    )
    kind_big = models.CharField(max_length=10, choices=KIND_BIG)
    kind_small_vege = models.CharField(
        max_length=10, blank=True, choices=KIND_SMALL_VEGE)
    kind_small_fruit = models.CharField(
        max_length=10, blank=True, choices=KIND_SMALL_FRUIT)
    kind_small_else = models.CharField(
        max_length=10, blank=True, choices=KIND_SMALL_ELSE)


class Wish(models.Model):
    #consumer = models.ForeignKey('Consumer', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

#안녕
class QnA(models.Model):
    question = models.TextField()
    answer = models.TextField()
    
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    #consumer = models.ForeignKey('Consumer')
    #products = models.ForeignKey('Product', on_delete=models.CASCADE)


def get_delete_product():
    return Product.objects.get_or_create(title="삭제된 상품")[0]


class Purchase(models.Model):
    D_STATUS = (
        ('preparing', '배송 준비 중'),
        ('shipping', '배송 중'),
        ('complete', '완료'),
    )
    delivery_status = models.CharField(max_length=10, choices=D_STATUS)
    quantity = models.IntegerField()
    
    purchase_datetime = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey('Product', on_delete=models.SET(get_delete_product))
    #consumer = models.ForeignKey('Consumer')
