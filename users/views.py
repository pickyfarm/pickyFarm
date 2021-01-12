from django.shortcuts import render, redirect, reverse
from .models import Farmer, Farm_Tag, Subscribe, Cart
from products.models import Category, Product
from django.db.models import Count
from math import ceil
from django.views import View
from .forms import LoginForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout


class Login(View):

    def get(self, request):
        form = LoginForm()
        ctx = {
            'form': form,
        }
        return render(request, "users/login.html", ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(user)
                return redirect(reverse("core:main"))
        ctx = {
            'form': form,
        }
        return render(request, "users/login.html", ctx)


def log_out(request):
    logout(request.user)
    return redirect(reverse("core:home"))


def farmers_page(request):
    page = int(request.GET.get('page', 1))
    page_size = 6
    limit = page_size * page
    offset = limit - page_size
    farmers_count = Farmer.objects.all().count()
    tags = Farm_Tag.objects.all()
    farmers = Farmer.objects.annotate(
        sub_counts=Count('subs'))  # 구독자 수 필드 임의 추가
    best_farmers = farmers.order_by('-sub_counts')[:3]
    # farmers = Farmer.objects.all()
    # best_farmers = farmers.order_by('-sub_count')[:3]

    page_total = ceil(farmers_count/page_size)
    categories = Category.objects.filter(parent=None)
    # best_farmer.user.profile_image.url
    ctx = {
        'tags': tags,
        'page': page,
        'page_total': page_total,
        'page_range': range(1, page_total),
        'farmers': farmers,
        'best_farmers': best_farmers,
        "categories": categories,
    }
    return render(request, 'users/farmers_page.html', ctx)


def farmer_sub_inc(request):
    return render(request, 'users/farmers_page.html',)


def farmer_detail(request, pk):
    farmer = Farmer.objects.get(pk=pk)
    ctx = {
        'farmer': farmer,
    }
    return render(request, 'users/farmer_detail.html', ctx)


def cart_in(request, product_pk):
    try:
        cart = Cart.objects.get(
            consumer=request.user.consumer, product__id=product_pk)
    except ObjectDoesNotExist:
        product = Product.objects.get(pk=product_pk)
        cart = Cart.objects.create(
            product=product, consumer=request.user.consumer, quantitiy=1)
        cart.save()
    return redirect(reverse("products:product_detail", args=[product_pk]))
