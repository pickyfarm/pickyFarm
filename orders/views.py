from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import Order_Group_Form
# Create your views here.


def orderingCart(request):
    pass


@login_required
def payment_create(request):
    consumer = request.user.consumer
    if request.method == 'GET':
        form = Order_Group_Form()
        ctx = {
            'form':form,
            'consumer':consumer,
        }
        return render(request, 'orders/payment.html', ctx)


    pass
