from django.db import models
from products.models import Product

# Create your models here.

# def get_delete_product():
#     return Product.objects.get_or_create(title="삭제된 상품")[0]


class Purchase(models.Model):
    D_STATUS = (
        ('preparing', '배송 준비 중'),
        ('shipping', '배송 중'),
        ('complete', '완료'),
    )
    delivery_status = models.CharField(max_length=10, choices=D_STATUS)
    quantity = models.IntegerField()
    
    purchase_datetime = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    # product = models.ForeignKey('products.Product', on_delete=models.SET(get_delete_product))
    #consumer = models.ForeignKey('Consumer', on_delete=models.CASCADE)