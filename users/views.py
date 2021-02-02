from django.shortcuts import render, redirect, reverse
from .models import Farmer, Farm_Tag, Subscribe, Cart, Consumer, Wish, User
from products.models import Category, Product
from django.db.models import Count
from math import ceil
from django.views import View
from .forms import LoginForm, SignUpForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

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
                login(request, user=user)
                return redirect(reverse("core:main"))
        ctx = {
            'form': form,
        }
        return render(request, "users/login.html", ctx)


def log_out(request):
    logout(request)
    return redirect(reverse("core:main"))


class SignUp(View):

    def get(self, request):
        form = SignUpForm()
        ctx = {
            'form': form,
        }
        return render(request, 'users/signup.html', ctx)

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            Consumer.objects.create(user=user, grade=1)
            if user is not None:
                login(request, user=user)
                return redirect(reverse('core:main'))
        ctx = {
            'form': form,
        }
        return render(request, 'users/signup.html', ctx)


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


@login_required
def cart_in(request, product_pk):
    try:
        cart = Cart.objects.get(
            consumer=request.user.consumer, product__id=product_pk)
        cart.quantitiy += 1
        messages.warning(request, "무난이를 장바구니에 +1 하였습니다")
    except ObjectDoesNotExist:
        product = Product.objects.get(pk=product_pk)
        cart = Cart.objects.create(
            product=product, consumer=request.user.consumer, quantitiy=1)
        messages.warning(request, "무난이를 장바구니에 담았습니다")
    # return redirect(reverse("products:product_detail", args=[product_pk]))
    return redirect(request.GET['next'])

@login_required
def wish(request, product_pk):
    try:
        wish = Wish.objects.get(
            consumer=request.user.consumer, product__id=product_pk)
        messages.warning(request, "이미 찜한 무난이입니다")
    except ObjectDoesNotExist:
        product = Product.objects.get(pk=product_pk)
        wish = Wish.objects.create(
            consumer=request.user.consumer, product=product)
        messages.warning(request, "찜하였습니다")
    # return redirect(reverse("products:product_detail", args=[product_pk]))
    return redirect(request.GET['next'])


class MyPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')

    def form_valid(self, form):

        if User.objects.filter(email=self.request.POST.get('email')).exists():
            return super().form_valid(form)
        
        else:
            return render(self.request, 'users/password_reset_done_fail.html')


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

    def form_valid(self, form):
        return super().form_valid(form)


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'