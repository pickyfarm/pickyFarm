from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .forms import Order_Group_Form
from .models import Order_Group
from django.utils import timezone
# Create your views here.


def orderingCart(request):
    pass


@login_required
def payment_create(request):
    consumer = request.user.consumer
    if request.method == 'GET':
        form = Order_Group_Form()
        ctx = {
            'form': form,
            'consumer': consumer,
        }
        return render(request, 'orders/payment.html', ctx)
    else:
        form = Order_Group_Form(request.POST)
        if form.is_valid():
            rev_name = form.cleaned_data.get('rev_name')
            rev_phone_number = form.cleaned_data.get('rev_phone_number')
            rev_loc_at = form.cleaned_data.get('rev_loc_at')
            rev_loc_detail = form.cleaned_data.get('rev_loc_detail')
            rev_message = form.cleaned_data.get('rev_message')
            to_farm_message = form.cleaned_data.get('to_farm_message')
            payment_type = form.cleaned_data.get('payment_type')

        order_at = timezone.now()
        consumer = request.user.consumer

        # rev address, total_price, total_quantity 추후 작업
        new_Order_Group = Order_Group(status='waiting', rev_address="추후작업", rev_name=rev_name,
                                      rev_phone_number=rev_phone_number, rev_loc_at=rev_loc_at, rev_loc_detail=rev_loc_detail, rev_message=rev_message, to_farm_message=to_farm_message, payment_type=payment_type, total_price=10, total_quantity=10, order_at=order_at, consumer=consumer)
        new_Order_Group.save()
        return redirect(reverse("users:mypage", kwargs={'cat': 'orders'}))

    pass
