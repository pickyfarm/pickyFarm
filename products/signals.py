from django.db.models.signals import post_save
from django.dispatch import receiver
from admins.models import FarmerNotification
from .models import Question


@receiver(post_save, sender=Question)
def question_post_save(sender, instance, **kwargs):
    FarmerNotification.objects.create(
        farmer=instance.product.farmer,
        message="상품 " + "'" + instance.product.title + "'" + "의 문의가 등록되었습니다.",
        notitype="qna_noti",
        obj_pk=instance.pk,
    )
