from django.shortcuts import render, redirect, reverse
<<<<<<< HEAD
from .models import Farmer, Farm_Tag, Subscribe, Cart, Consumer, Wish, User
=======
from .models import Farmer, Farm_Tag, Farmer_Story, Subscribe, Cart, Consumer, Wish
>>>>>>> farmers_page_feature
from products.models import Category, Product
from django.db.models import Count
from math import ceil
from django.views import View
from .forms import LoginForm, SignUpForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
<<<<<<< HEAD
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
=======
from django.core.paginator import Paginator
from django.db.models import Q

>>>>>>> farmers_page_feature

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
    # farmer list
    farmer = Farmer.objects.all()
    paginator = Paginator(farmer, 3)
    page = request.GET.get('page')
    farmers = paginator.get_page(page)

    # weekly hot farmer
    best_farmers = farmer.order_by('-sub_count')[:1] # 조회수 대신 임의로

    # farmer's story list
    farmer_story = Farmer_Story.objects.all()
    paginator_2 = Paginator(farmer_story, 7)
    page_2 = request.GET.get('page_2')
    farmer_stories = paginator_2.get_page(page_2)

    ctx = {
        'best_farmers': best_farmers,
        'farmers': farmers,
        'farmer_stories': farmer_stories,
    }
    return render(request, 'users/farmers_page.html', ctx)

# farmer 검색 view
def farmer_search(request):
    search_key = request.GET.get('search_key') # 검색어 가져오기
    search_list = Farmer.objects.all()
    if search_key: # 검색어 존재 시
        search_list = search_list.filter(Q(farm_name__contains=search_key)|Q(user__nickname__contains=search_key)) 
    search_list = search_list.order_by('-id')
    paginator = Paginator(search_list, 10)
    page = request.GET.get('page')
    farmers = paginator.get_page(page)
    ctx = {
        'farmers':farmers,
    }
    return render(request, 'users/farmers_page.html', ctx)

# farmer story 검색 view
def farmer_story_search(request):
    search_key_2 = request.GET.get('search_key_2')
    search_list = Farmer_Story.objects.all()
    if search_key_2:
        search_list = search_list.filter(Q(farmer__contains=search_key)|Q(title__contains=search_key))
    search_list = search_list.order_by('-id')
    paginator = Paginator(search_list, 10)
    page_2 = request.GET.get('page_2')
    farmer_stories = paginator.get_page(page_2)
    ctx = {
        'farmer_stories':farmer_stories,
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