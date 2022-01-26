from email.utils import quote
from .models import Order_Detail, Order_Group
from django.utils import timezone
import datetime



def delete_waiting_orders():
    now = timezone.localtime()
    order_groups = Order_Group.objects.filter(status="wait")
    pass


def auto_cancel_gift():

    now = timezone.now()
    print(now)
    hour_ago = now - datetime.timedelta(hours=48)
    # 새벽인 경우 
    # if 0<= now.hour <=6:
    #     return

    gift_order_details = Order_Detail.objects.filter(status="payment_complete_no_address", create_at__lte=hour_ago)

    for detail in gift_order_details:

        try:
            detail.order_cancel(cancel_reason="[선물하기] 장시간 주소미입력으로 인한 주문 취소", gift=True)
        except Exception as e:
            print("[ERROR] ", e)


    print(f"[CRONTAB] {now} auto_cancel_gift complete")


