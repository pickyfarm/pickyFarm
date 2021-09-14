from django.db import models
from core.models import CompressedImageField


# Create your models here.


class Order_Group(models.Model):

    STATUS = (
        ("wait", "결제대기"),
        ("payment_complete", "결제완료"),
        ("cancel", "결제취소"),
        ("error_stock", "결제오류(재고부족)"),
        ("error_valid", "결제오류(검증)"),
        ("error_server", "결제오류(서버)"),
    )

    status = models.CharField(max_length=20, choices=STATUS, default="wait")
    order_management_number = models.CharField(max_length=20, null=True, blank=True)
    receipt_number = models.CharField(max_length=60, null=True, blank=True)
    rev_address = models.TextField(null=True, blank=True)
    rev_name = models.CharField(max_length=50, null=True, blank=True)
    rev_phone_number = models.CharField(max_length=30, null=True, blank=True)
    rev_loc_at = models.CharField(max_length=20, null=True, blank=True)
    rev_loc_detail = models.TextField(null=True, blank=True)
    rev_message = models.TextField(null=True, blank=True)
    to_farm_message = models.TextField(null=True, blank=True)

    payment_type = models.CharField(max_length=20, null=True, blank=True)

    total_price = models.IntegerField(null=True, blank=True)
    total_quantity = models.IntegerField(null=True, blank=True)
    order_at = models.DateTimeField(null=True, blank=True)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    consumer = models.ForeignKey(
        "users.Consumer", related_name="order_groups", on_delete=models.CASCADE
    )

    def __str__(self):
        name = []
        name.append(self.consumer.user.nickname)
        name.append(str(self.create_at) + " 주문")
        return "-".join(name)


class Order_Detail(models.Model):

    STATUS = (
        ("wait", "결제대기"),
        ("payment_complete", "결제완료"),
        ("preparing", "배송 준비 중"),
        ("shipping", "배송 중"),
        ("delivery_complete", "배송완료"),
        ("cancel", "주문취소"),
        ("re_recept", "환불 접수"),
        ("ex_recept", "교환 접수"),
        ("re_ex_approve", "환불/교환 승인"),
        ("re_ex_deny", "환불/교환 거절"),
        ("error_stock", "결제오류(재고부족)"),
        ("error_valid", "결제오류(검증)"),
        ("error_server", "결제오류(서버)"),
    )

    PAYMENT_STATUS = (("incoming", "정산예정"), ("progress", "정산 진행"), ("done", "정산 완료"))

    # LOGIS_COMPANY = (
    #     ()
    # )

    status = models.CharField(max_length=20, choices=STATUS, default="wait")
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default="incoming")
    order_management_number = models.CharField(max_length=20, null=True, blank=True)
    invoice_number = models.CharField(max_length=30, null=True, blank=True)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    cancel_reason = models.CharField(max_length=30, null=True, blank=True)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey(
        "products.Product", related_name="order_details", on_delete=models.CASCADE
    )
    order_group = models.ForeignKey(
        Order_Group, related_name="order_details", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        name = []
        name.append(str(self.product.title))
        name.append(str(self.quantity))
        name.append(str(self.status))
        return "-".join(name)




class RefundExchange(models.Model):
    TYPE = (
        ("refund", "환불"),
        ("exchange", "교환"),
    )
    STATUS = (
        ("recept", "환불/교환 접수"),
        ("approve", "환불/교환 승인"),
        ("deny", "환불/교환 거절"),
    )
    claim_type = models.CharField(max_length=20, choices=TYPE)
    claim_status = models.CharField(max_length=20, choices=STATUS)

    order_detail = models.ForeignKey(
        "Order_Detail", on_delete=models.PROTECT, related_name="refund_exchanges"
    )
    reason = models.TextField()
    image = CompressedImageField(upload_to="RefundExchange/%Y/%m/%d/", null=True, blank=True)

    farmer_answer = models.TextField(null=True, blank=True)

    rev_address = models.TextField(null=True, blank=True)
    rev_loc_at = models.CharField(max_length=20, null=True, blank=True)
    rev_loc_detail = models.TextField(null=True, blank=True)
    rev_message = models.TextField(null=True, blank=True)

    refund_exchange_delivery_fee = models.IntegerField(null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
