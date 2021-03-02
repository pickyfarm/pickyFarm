from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
from .models import Farmer, Farm_Tag, Farmer_Story, Subscribe, Cart, Consumer, Wish, User
from products.models import Category, Product
from django.db.models import Count
from math import ceil
from datetime import timedelta
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView
from .forms import LoginForm, SignUpForm, MyPasswordResetForm, FindMyIdForm
from django.views.decorators.http import require_POST
from .forms import LoginForm, SignUpForm, MyPasswordResetForm, FarmApplyForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from addresses.forms import AddressForm
from addresses.models import Address
from math import ceil
from django.conf import settings


# Exception 선언 SECTION

class NoRelatedInstance(Exception):
    pass


# AJAX 통신 선언 SECTION (상품 장바구니/장바구니에서 제거하기, 상품 찜하기/찜하기 취소하기, 농가 구독/구독 취소하기)

@login_required
@require_POST
def CartInAjax(request):
    if request.method == 'POST':
        pk = request.POST.get('pk', None)
        quantity = request.POST.get('quantity', 1)
        print(quantity)
        print(pk)
        user = request.user
        product = Product.objects.get(pk=pk)
        if (product is None) or (product.open is False):
            message = "존재하지 않는 상품입니다"
            return JsonResponse(message)

        try:
            cart = Cart.objects.get(consumer=user.consumer, product=product)
            message = "이미 장바구니에 있는 무난이 입니다"
        except ObjectDoesNotExist:
            cart = Cart.objects.create(
                consumer=user.consumer, product=product, quantity=quantity)
            message = product.title + "를 장바구니에 담았습니다!"
        print(cart)

        data = {
            "message": message,
        }
        return JsonResponse(data)


@login_required
@require_POST
def cartOutAjax(request):
    if request.method == 'POST':
        product_pk = request.POST.getlist('pkList[]', None)
        print(product_pk)
        # print(request.POST)
        consumer = request.user.consumer

        for pk in product_pk:
            try:
                cart = Cart.objects.get(product__pk=pk, consumer=consumer)
            except ObjectDoesNotExist:
                print("없음")

            cart.delete()
        response = {
            'success': True,
        }
        return JsonResponse(response)


@login_required
@require_POST
def CancelSubs(request):
    if request.method == 'POST':
        print("진입")
        pk = request.POST.get('pk', None)
        print(pk)
        try:
            sub = Subscribe.objects.get(pk=pk)
        except ObjectDoesNotExist:
            msg = "구독 기록이 존재하지 않습니다. 다시 시도해주세요"
            data = {
                'success': "0",
                'msg': msg,
            }
            return JsonResponse(data)
        farm_name = sub.farmer.farm_name
        print(farm_name)
        sub.delete()
        msg = f'{farm_name} 구독 취소 했습니다'
        data = {
            "success": "1",
            'msg': msg,
        }
        print("전달 직전")
        # return HttpResponse(json.dumps(data), content_type='application/json')
        return JsonResponse(data)


@login_required
@require_POST
def subs(request):
    if request.method == 'POST':
        farmer_pk = request.POST.get('farmer_pk', None)
        consumer = request.user.consumer
        if farmer_pk is None:
            data = {
                'success': -1,

            }
            return JsonResponse(data)
        try:
            sub = Subscribe.objects.get(
                farmer__pk=farmer_pk, consumer=consumer)
            data = {
                'success': 0,
            }
            return JsonResponse(data)
        except ObjectDoesNotExist:
            try:
                farmer = Farmer.objects.get(pk=farmer_pk)
            except ObjectDoesNotExist:
                data = {
                    'success': -1,
                }
                return JsonResponse(data)
            Subscribe.objects.create(farmer=farmer, consumer=consumer)
            data={
                'success': 1,
            }
            return JsonResponse(data)


@login_required
@require_POST
def wish(request):
    if request.method == 'POST':
        user = request.user.consumer
        product_pk = request.POST.get('pk', None)

        print("로그인이 안되는거?")

        try:
            wish = Wish.objects.get(
                consumer=user, product__pk=product_pk)
            response = {
                'status': 0,
            }
            return JsonResponse(response)
        except ObjectDoesNotExist:
            product = Product.objects.get(pk=product_pk)
            Wish.objects.create(
                consumer=request.user.consumer, product=product)
            response = {
                'status': 1,
            }
            return JsonResponse(response)


# 회원 관련 view

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
                keep_login = self.request.POST.get('auto_login', False)
                print(keep_login)
                if keep_login:
                    settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False

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
        addressform = AddressForm()

        ctx = {
            'form': form,
            'addressform': addressform,
        }
        return render(request, 'users/signup.html', ctx)

    def post(self, request):
        form = SignUpForm(request.POST)
        addressform = AddressForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            Consumer.objects.create(user=user, grade=1)

            address = addressform.save(commit=False)
            address.user = user
            address.is_default = True
            address.save()

            if user is not None:
                login(request, user=user)
                return redirect(reverse('core:main'))

        ctx = {
            'form': form,
            'addressform': addressform,
        }
        return render(request, 'users/signup.html', ctx)


# id validation function for AJAX
def idValidation(request):
    target = request.GET.get('target')
    isValid = User.objects.filter(username=target).exists()
    print(target)
    print(isValid)

    ctx = {
        'target': target,
        'isValid': isValid
    }

    return JsonResponse(ctx)

# email validation function for AJAX


def emailValidation(request):
    target = request.GET.get('target')
    isValid = User.objects.filter(email=target).exists()
    print(target)
    print(isValid)

    ctx = {
        'target': target,
        'isValid': isValid
    }

    return JsonResponse(ctx)

# nickname validation function for AJAX


def nicknameValidation(request):
    target = request.GET.get('target')
    isValid = User.objects.filter(nickname=target).exists()

    ctx = {
        'target': target,
        'isValid': isValid
    }

    return JsonResponse(ctx)


def farmers_page(request):
    # farmer list
    farmer = Farmer.objects.all().order_by('-id')
    paginator = Paginator(farmer, 3)
    page = request.GET.get('page')
    farmers = paginator.get_page(page)

    # weekly hot farmer
    best_farmers = farmer.order_by('-sub_count')[:1]  # 조회수 대신 임의로

    # farmer's story list
    farmer_story = Farmer_Story.objects.all()
    paginator_2 = Paginator(farmer_story, 7)
    page_2 = request.GET.get('page_2')
    farmer_stories = paginator_2.get_page(page_2)

    print(farmer.first().user)
    ctx = {
        'best_farmers': best_farmers,
        'farmers': farmers,
        'farmer_stories': farmer_stories,
    }
    return render(request, 'users/farmers_page.html', ctx)

# farmer input 검색 view - for AJAX
def farmer_search(request):
    search_key = request.GET.get('search_key')  # 검색어 가져오기
    search_list = Farmer.objects.all()
    if search_key:  # 검색어 존재 시
        search_list = search_list.filter(
            Q(farm_name__contains=search_key) | Q(user__nickname__contains=search_key))
    search_list = search_list.order_by('-id')
    paginator = Paginator(search_list, 10)
    page = request.GET.get('page')
    farmers = paginator.get_page(page)
    ctx = {
        'farmers': farmers,
    }
    return render(request, 'users/farmer_search.html', ctx)

# farmer category(채소, 과일, E.T.C) 검색 view - for AJAX
def farm_cat_search(request):
    search_cat = request.GET.get('search_cat')
    farmer = Farmer.objects.filter(farm_cat=search_cat).order_by('-id')
    paginator = Paginator(farmer, 3)
    page = request.GET.get('page')
    farmers = paginator.get_page(page)
    ctx = {
        'farmers': farmers,
    }
    return render(request, 'users/farmer_search.html', ctx)

# farmer story 검색 view - for AJAX
def farmer_story_search(request):
    select_val = request.GET.get('select_val')
    search_key_2 = request.GET.get('search_key_2')
    search_list = Farmer_Story.objects.all()
    if search_key_2:
        if select_val == 'title':
            search_list = search_list.filter(Q(title__contains=search_key_2))
        elif select_val == 'farm':
            search_list = search_list.filter(
                Q(farmer__farm_name__contains=search_key_2))
        elif select_val == 'farmer':
            search_list = search_list.filter(
                Q(farmer__user__nickname__contains=search_key_2))
    search_list = search_list.order_by('-id')
    paginator = Paginator(search_list, 10)
    page_2 = request.GET.get('page_2')
    farmer_stories = paginator.get_page(page_2)
    ctx = {
        'farmer_stories': farmer_stories,
    }
    return render(request, 'users/farmer_story_search.html', ctx)

# farmer's story detail page
def farmer_story_detail(request, pk):
    main_story = Farmer_Story.objects.get(pk=pk)
    farmer = main_story.farmer
    stories = Farmer_Story.objects.all().filter(farmer=farmer)
    ctx = {
        'main_story': main_story,
        'farmer': farmer,
        'stories': stories,
    }
    return render(request, 'users/farmer_story_detail.html', ctx)

def farmer_sub_inc(request):
    return render(request, 'users/farmers_page.html',)

# 농가 세부 페이지
def farmer_detail(request, pk):
    farmer = Farmer.objects.get(pk=pk)
    tags = Farm_Tag.objects.all().filter(farmer=farmer)
    products = Product.objects.all().filter(farmer=farmer)
    stories = Farmer_Story.objects.all().filter(farmer=farmer)

    ctx = {
        'farmer': farmer,
        'tags': tags,
        'products': products,
        'stories': stories,
    }
    return render(request, 'users/farmer_detail.html', ctx)

# 입점 신청
def farm_apply(request):
    if request.method =='POST':
        form = FarmApplyForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users/farm_apply_complete.html')
        else:
            return redirect(reverse("core:main"))
    else:
        print('get')
        form = FarmApplyForm()
        ctx = {
            'form':form,
        }
        return render(request, 'users/farm_apply.html', ctx)


user_email = ''


class MyPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    form_class = MyPasswordResetForm

    def form_valid(self, form):
        global user_email

        if User.objects.filter(email=self.request.POST.get('email')).exists() and User.objects.get(email=self.request.POST.get('email')).username == self.request.POST.get('username'):
            user_email = form.cleaned_data.get("email")
            print(user_email)
            return super().form_valid(form)

        else:
            return render(self.request, 'users/password_reset_done_fail.html')


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

    def get_context_data(self, **kwargs):
        global user_email
        ctx = super().get_context_data(**kwargs)
        ctx['email'] = user_email
        print(user_email)
        return ctx


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['new_password1'].widget.attrs = {
            'placeholder': '새 비밀번호를 입력해주세요'}
        form.fields['new_password2'].widget.attrs = {
            'placeholder': '새 비밀번호를 한번 더 입력해주세요'}

        return form

    def form_valid(self, form):
        return super().form_valid(form)


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


@login_required
def mypage(request, cat):

    try:
        consumer = request.user.consumer
    except ObjectDoesNotExist:
        return redirect(reverse('core:main'))

    cat_name = str(cat)
    print(cat_name)

    if request.method == 'GET':
        consumer_nickname = consumer.user.nickname
        sub_farmers = consumer.subs.all()  # pagenation 필요
        print(sub_farmers)
        if sub_farmers.exists() is False:
            print("구독자는 없다")
        questions = consumer.questions.order_by('-create_at')  # pagenation 필요
        print(questions)
        if questions.exists() is False:
            print("질문은 없다")
        try:
            groups = consumer.order_groups.all()
            print(groups)
            if groups.exists() is False:
                print("여기안와?")
                raise NoRelatedInstance
            for group in groups:
                details = group.order_details
                preparing_num = details.filter(status='preparing').count()
                print(preparing_num)
                delivery_num = details.filter(status='shipping').count()
                print(delivery_num)
                complete_num = details.filter(status='complete').count()
                print(complete_num)
                cancel_num = details.filter(status='cancel').count()
        except NoRelatedInstance:
            preparing_num = 0
            delivery_num = 0
            complete_num = 0
            cancel_num = 0

        # 구독 농가
        subs = consumer.subs.all().order_by('-create_at').all()
        if subs is None:
            subs_count = 0
        else:
            subs_count = subs.count()
        print("구독자 수 " + (str)(subs_count))

        # 상품 Q&A
        now = timezone.localtime()
        one_month_before = now + timedelta(days=-30)
        print(one_month_before)

        questions = consumer.questions.filter(
            create_at__gt=one_month_before).order_by('-create_at').all()
        print((type)(questions))

        for q in questions:
            print(type(q))

        ctx = {
            'consumer_nickname': consumer_nickname,
            'sub_farmers': sub_farmers,
            'questions': questions,
            'preparing_num': preparing_num,
            'delivery_num': delivery_num,
            'complete_num': complete_num,
            'cancel_num': cancel_num,
            'subs_count': subs_count,
            'subs': subs,
            'questions': questions,
        }

        if cat_name == 'orders':
            page = int(request.GET.get('page', 1))
            page_size = 5

            order_groups = groups.filter(
                status='complete').order_by('-create_at')
            print(order_groups)
            if order_groups.exists():
                order_details = order_groups[0].order_details.all()
                print(order_groups.count())
                if order_groups.count() > 1:
                    for group in order_groups[1:]:
                        print(group.order_details.all())
                        order_details = order_details | group.order_details.all()
                order_details = order_details.order_by(
                    '-order_group__create_at')
            else:
                order_details = None

            print(order_details)
            if order_details is None:
                order_details_count = 0
                total_pages = 0
                offset = 0
            else:
                order_details_count = order_details.count()
                total_pages = ceil(order_details_count/page_size)
                offset = page * page_size - page_size
                order_details = order_details[offset:page*page_size]

            ctx_orders = {
                'total_pages': range(1, total_pages+1),
                'order_details': order_details,
            }
            ctx.update(ctx_orders)
            return render(request, 'users/mypage_orders.html', ctx)
        elif cat_name == 'wishes':
            page = int(request.GET.get('page', 1))
            page_size = 5

            wishes = consumer.wishes.filter(
                product__open=True).order_by('-create_at')
            print(wishes)

            wishes_count = wishes.count()
            total_pages = ceil(wishes_count/page_size)
            offset = page * page_size - page_size
            wishes = wishes[offset:page*page_size]
            print(wishes)

            ctx_wishes = {
                'page': page,
                'total_pages': range(1, total_pages+1),
                'wishes': wishes,
            }
            ctx.update(ctx_wishes)
            return render(request, 'users/mypage_wishes.html', ctx)
        elif cat_name == 'cart':
            carts = consumer.carts.all().order_by('-create_at').filter(product__open=True)
            print(carts)

            ctx_carts = {
                'carts': carts,
            }
            ctx.update(ctx_carts)
            return render(request, 'users/mypage_carts.html', ctx)
        elif cat_name == 'rev_address':
            pass
        elif cat_name == 'info':
            user = consumer.user
            if request.is_ajax():
                info = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    # 'number':number,
                    'email': user.email,
                    'nickname': user.nickname,
                    'profile_image': user.profile_image.url,
                }
                return JsonResponse(info)
            ctx_info = {
                'user': user,
            }
            ctx.update(ctx_info)
            return render(request, 'users/mypage.html', ctx)


class FindMyIdView(TemplateView):
    template_name = 'users/find_my_id.html'  # to be added

    def get(self, request):
        form = FindMyIdForm()
        ctx = {
            'form': form,
        }

        return self.render_to_response(ctx)

    def post(self, request):
        form = FindMyIdForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")

            try:
                user = User.objects.get(email=email)
                username = user.get_full_name()

                if form.cleaned_data.get("name") == username:
                    ctx = {
                        'user': user
                    }
                    return render(request, "users/find_my_id_complete.html", ctx)

                else:
                    raise User.DoesNotExist

            except User.DoesNotExist:
                return redirect(reverse('users:find_my_id_failed'))


class FindMyIdFailView(TemplateView):
    template_name = 'users/find_my_id_failed.html'
