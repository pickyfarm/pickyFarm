from .models import Order_Detail, Order_Group
from django.utils import timezone



def delete_waiting_orders():
    now = timezone.localtime()
    order_groups = Order_Group.objects.filter(status="wait")
    pass


def auto_cancel_gift():