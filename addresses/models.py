from django.db import models
from users.models import User

# Create your models here.
class Address(models.Model):
    full_address = models.CharField(max_length=100)
    detail_address = models.CharField(max_length=100, blank=True)
    extra_address = models.CharField(max_length=100, blank=True)
    sido = models.CharField(max_length=10, blank=True)
    sigungu = models.CharField(max_length=30, blank=True)
    is_default = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.nickname}"

    def get_full_address(self):
        return f"{self.full_address} {self.detail_address if self.detail_address else ''} {self.extra_address if self.extra_address else ''}"
