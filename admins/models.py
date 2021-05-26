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
        return f'{self.title}'



