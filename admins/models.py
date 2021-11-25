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
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message}"


class Report(models.Model):
    TYPE = (
        ("editor's pick comment", "editor's pick 댓글"),
        ("editor's pick recomment", "editor's pick 대댓글"),
        ("farmer's story comment", "farmer's story 댓글"),
        ("farmer's story recomment", "farmer's story 대댓글"),
        ("product comment", "상품 리뷰"),
        ("product recomment", "상품 리뷰 댓글"),
    )

    STATUS = (
        ("recept", "신고 접수"),
        ("resolve", "처리 완료"),
    )

    report_type = models.CharField(max_length=30, choices=TYPE)

    editors_pick_comment = models.ForeignKey(
        "comments.Editor_Review_Comment", on_delete=models.PROTECT, null=True
    )
    editors_pick_recomment = models.ForeignKey(
        "comments.Editor_Review_Recomment", on_delete=models.PROTECT, null=True
    )
    farmers_story_comment = models.ForeignKey(
        "comments.Farmer_Story_Comment", on_delete=models.PROTECT, null=True
    )
    farmers_story_recomment = models.ForeignKey(
        "comments.Farmer_Story_Recomment", on_delete=models.PROTECT, null=True
    )
    product_comment = models.ForeignKey(
        "comments.Product_Comment", on_delete=models.PROTECT, null=True
    )
    product_recomment = models.ForeignKey(
        "comments.Product_Recomment", on_delete=models.PROTECT, null=True
    )

    reporter = models.ForeignKey("users.Consumer", on_delete=models.CASCADE, related_name="reports")
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS)
    result = models.TextField(null=True)

    create_at = models.DateTimeField(auto_now_add=True)
