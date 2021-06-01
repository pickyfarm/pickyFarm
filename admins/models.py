from django.db import models

# Create your models here.
class FarmerNotice(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    attachments = models.FileField(upload_to="notice/%Y/%m/%d/", null=True, blank=True)

    important = models.BooleanField(default=False)

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class FarmerNotification(models.Model):
    TYPE = (
        ("review_noti", "상품 리뷰 알림"),
        ("qna_noti", "상품 문의 알림"),
        ("story_comment_noti", "파머 스토리 댓글 알림"),
        ("refund_noti", "반품 요청 알림"),
        ("proudct_noti", "상품 상태 변경 알림"),
        ("payment_noti", "정산 상태 변경 알림"),
    )
    farmer = models.ForeignKey(
        "farmers.Farmer", on_delete=models.CASCADE, related_name="farmer_notifications"
    )
    message = models.TextField()
    notitype = models.CharField(max_length=50, choices=TYPE)
    is_read = models.BooleanField(default=False)
    obj_pk = models.IntegerField()

    def __str__(self):
        return f"{self.message}"
