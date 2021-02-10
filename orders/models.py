from django.db import models

# Create your models here.


class Order_Group(models.Model):

    STATUS = (
        ('wating', '결제대기'),
        ('complete', '결제완료'),
    )

    status = models.CharField(max_length=20, choices=STATUS, default='wait')
    rev_address = models.TextField()
    rev_name = models.CharField(max_length=50)
    rev_loc_at = models.CharField(max_length=20)
    rev_loc_detail = models.TextField(null=True, blank=True)
    rev_message = models.TextField(null=True, blank=True)

    payment_type = models.CharField(max_length=20)

    total_price = models.IntegerField()
    total_quantity = models.IntegerField()
    order_at = models.DateTimeField(null=True, blank=True)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    consumer = models.ForeignKey(
        'users.Consumer', related_name='order_groups', on_delete=models.CASCADE)

    def __str__(self):
        name = []
        name.append(self.consumer.user.nickname)
        name.append(str(self.create_at) + ' 주문')
        return '-'.join(name)


class Order_Detail(models.Model):

    STATUS = (
        ('wait', '결제대기'),
        ('complete', '결제완료'),
        ('preparing', '배송 준비 중'),
        ('shipping', '배송 중'),
        ('complete', '배송완료'),
        ('cancel', '주문취소'),
    )

    status = models.CharField(max_length=20, choices=STATUS, default='wait')
    invoice_number = models.CharField(max_length=30, null=True, blank=True)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    cancel_reason = models.CharField(max_length=30, null=True, blank=True)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey(
        'products.Product', related_name='order_details', on_delete=models.CASCADE)
    order_group = models.ForeignKey(
        Order_Group, related_name='order_details', on_delete=models.CASCADE)

    def __str__(self):
        name = []
        name.append(str(self.product.title))
        name.append(str(self.quantity))
        name.append(str(self.status))
        return '-'.join(name)
