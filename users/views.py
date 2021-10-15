from comments.forms import ProductCommentForm
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse, HttpResponse
from orders.models import Order_Detail
from django.db.models import Count
from django.utils import timezone
from django.utils.timezone import get_current_timezone, localtime
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.detail import DetailView
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from django.views.generic import DetailView

import datetime
from datetime import timedelta
import os
import requests
import pprint
import json
import string
import random
from math import ceil, log
from random import randint
from kakaomessages.template import templateIdList
from kakaomessages.views import send_kakao_message, send_sms
from config.settings import base

# models
from .models import Subscribe, Cart, Consumer, Wish, User, Editor, PhoneNumberAuth
from editor_reviews.models import Editor_Review
from comments.models import (
    Editor_Review_Comment,
    Product_Comment,
    Product_Comment_Image,
)
from farmers.models import Farmer
from products.models import Category, Product
from addresses.models import Address

# forms
from .forms import (
    LoginForm,
    SignUpForm,
    SocialSignupForm,
    MyPasswordResetForm,
    FindMyIdForm,
)
from addresses.forms import AddressForm

from kakaomessages.views import send_kakao_message

# Exception 선언 SECTION
class KakaoException(Exception):
    pass


class NoRelatedInstance(Exception):
    pass


# AJAX 통신 선언 SECTION (상품 장바구니/장바구니에서 제거하기, 상품 찜하기/찜하기 취소하기, 농가 구독/구독 취소하기)


@login_required
@require_POST
def CartInAjax(request):
    if request.method == "POST":
        pk = request.POST.get("pk", None)
        quantity = request.POST.get("quantity", 1)
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
            cart = Cart.objects.create(consumer=user.consumer, product=product, quantity=quantity)
            message = product.title + "를 장바구니에 담았습니다!"
        print(cart)

        message = str(message)
        data = {
            "message": message,
        }
        return JsonResponse(data)


@login_required
@require_POST
def cartOutAjax(request):
    if request.method == "POST":
        product_pk = request.POST.getlist("pkList[]", None)
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
            "success": True,
        }
        return JsonResponse(response)


@login_required
@require_POST
def cancelSubs(request):
    if request.method == "POST":
        print("진입")
        pk = request.POST.get("pk", None)
        print(pk)
        try:
            sub = Subscribe.objects.get(pk=pk)
        except ObjectDoesNotExist:
            msg = "구독 기록이 존재하지 않습니다. 다시 시도해주세요"
            data = {
                "success": "0",
                "msg": msg,
            }
            return JsonResponse(data)
        farm_name = sub.farmer.farm_name
        print(farm_name)
        sub.delete()
        msg = f"{farm_name} 구독 취소 했습니다"
        data = {
            "success": "1",
            "msg": msg,
        }
        print("전달 직전")
        # return HttpResponse(json.dumps(data), content_type='application/json')
        return JsonResponse(data)


@login_required
@require_POST
def subs(request):
    if request.method == "POST":
        farmer_pk = request.POST.get("farmer_pk", None)
        consumer = request.user.consumer
        if farmer_pk is None:
            data = {
                "status": -1,
            }
            return JsonResponse(data)
        try:
            sub = Subscribe.objects.get(farmer__pk=farmer_pk, consumer=consumer)
            data = {
                "status": 0,
            }
            return JsonResponse(data)
        except ObjectDoesNotExist:
            try:
                farmer = Farmer.objects.get(pk=farmer_pk)
            except ObjectDoesNotExist:
                data = {
                    "status": -1,
                }
                return JsonResponse(data)
            Subscribe.objects.create(farmer=farmer, consumer=consumer)
            data = {
                "status": 1,
            }
            return JsonResponse(data)


@login_required
@require_POST
def wish(request):
    if request.method == "POST":
        user = request.user.consumer
        product_pk = request.POST.get("pk", None)

        print("로그인이 안되는거?")

        try:
            wish = Wish.objects.get(consumer=user, product__pk=product_pk)
            response = {
                "status": 0,
            }
            return JsonResponse(response)
        except ObjectDoesNotExist:
            product = Product.objects.get(pk=product_pk)
            Wish.objects.create(consumer=request.user.consumer, product=product)
            response = {
                "status": 1,
            }
            return JsonResponse(response)


@login_required
@require_POST
def cancelWish(request):
    if request.method == "POST":
        product_pk = request.POST.getlist("pkList[]", None)
        print(product_pk)
        # print(request.POST)
        consumer = request.user.consumer

        for pk in product_pk:
            try:
                wish = Wish.objects.get(product__pk=pk, consumer=consumer)
            except ObjectDoesNotExist:
                print("없음")

            wish.delete()
        response = {
            "success": True,
        }
        return JsonResponse(response)


@login_required
@require_POST
def infoUpdate(request):
    if request.method == "POST":
        user = request.user

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        response = {
            "status": 1,
        }
        return JsonResponse(response)


@login_required
@require_POST
def profileUpdate(request):
    if request.method == "POST":
        user = request.user

        nickname = request.POST.get("nick_name")
        profile_image = request.FILES.get("profile_img")

        # 유져가 프로필 사진 수정하지 않고 완료 버튼을 눌렀을 경우
        if profile_image is None:
            user.nickname = nickname
            user.save()
        # 유져가 프로필 사진 수정 후 완료 버튼 누른 경우
        else:
            user.nickname = nickname
            user.profile_image = profile_image
            user.save()

        response = {
            "status": 1,
        }

        return JsonResponse(response)


# 회원 관련 view


class Login(View):
    def get(self, request):
        form = LoginForm()
        get_next = self.request.GET.get("next", None)
        print(f"[LOGIN GET] next url : {get_next}")
        ctx = {
            "next": get_next,
            "form": form,
        }
        return render(request, "users/login.html", ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        post_next = self.request.POST.get("next", None)
        print(f"[POST] get_next url : {post_next} / type : {type(post_next)}")

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                keep_login = self.request.POST.get("auto_login", False)
                print(keep_login)
                if keep_login:
                    base.SESSION_EXPIRE_AT_BROWSER_CLOSE = False

                login(request, user=user)

                if post_next != "None":
                    print("[POST] get next REDIRECT")
                    return redirect(post_next)
                else:
                    return redirect(reverse("core:main"))
        ctx = {
            "form": form,
        }
        return render(request, "users/login.html", ctx)


def log_out(request):
    logout(request)
    return redirect(reverse("core:main"))


def kakao_login(request):
    REST_API_KEY = os.environ.get("KAKAO_KEY")
    REDIRECT_URI = "https://www.pickyfarm.com/user/login/kakao/callback"

    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code"
    )


def kakao_callback(request):
    REST_API_KEY = os.environ.get("KAKAO_KEY")
    print()
    REDIRECT_URI = "https://www.pickyfarm.com/user/login/kakao/callback"

    try:
        code = request.GET.get("code")
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}"
        )

        token_json = token_request.json()
        error = token_json.get("error", None)

        if error is not None:
            raise KakaoException

        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        profile_json = profile_request.json()
        profile = profile_json.get("kakao_account")

        email = profile.get("email")
        nickname = profile.get("profile").get("nickname")
        phone_number = profile.get("phone_number")

        try:
            user = User.objects.get(username=f'kakao.{email}')
            login(request, user=user)
            return redirect(reverse("core:main"))

        except ObjectDoesNotExist:
            pass

        info = {
            "email": email,
            "nickname": nickname,
            "phone_number": f'0{"".join(phone_number.split()[1].split("-"))}',
            "username": f"kakao.{email}",
            "account_name": nickname,
            "password": "".join(
                random.choices(string.ascii_uppercase + string.digits, k=15)
            ),
        }

        return SocialSignup.as_view()(request, info)

    except KakaoException:
        return redirect("core:main")


class SocialSignup(View):
    def get(self, request, info=None):
        if info is None:
            return redirect("users:signup")

        form = SocialSignupForm(info)
        addressform = AddressForm()

        ctx = {"form": form, "addressform": addressform}

        return render(request, "users/signup_kakao.html", ctx)

    def post(self, request):
        form = SocialSignupForm(request.POST)
        addressform = AddressForm(request.POST)
        benefit_agree = True
        kakao_farmer_agree = True
        kakao_comment_agree = True

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            print(f"================{user}")
            consumer = Consumer.objects.create(
                user=user,
                grade=1,
                benefit_agree=benefit_agree,
                kakao_farmer_agree=kakao_farmer_agree,
                kakao_comment_agree=kakao_comment_agree,
            )

            if addressform.is_valid():
                address = addressform.save(commit=False)
                address.user = user
                address.is_default = True
                address.save()

                consumer.default_address = address
                consumer.save()

            if user is not None:
                login(request, user=user)
                return redirect(reverse("core:main"))

        ctx = {
            "form": form,
            "addressform": addressform,
        }
        return render(request, "users/signup_kakao.html", ctx)


class SignUp(View):
    def get(self, request, info=None):

        if info is not None:
            form = SignUpForm({"email": info["email"], "nickname": info["nickname"]})
        else:
            form = SignUpForm()

        addressform = AddressForm()

        ctx = {
            "form": form,
            "addressform": addressform,
        }
        return render(request, "users/signup.html", ctx)

    def post(self, request):
        form = SignUpForm(request.POST)
        addressform = AddressForm(request.POST)
        benefit_agree = True
        kakao_farmer_agree = True
        kakao_comment_agree = True
        print(form.is_valid())
        if form.is_valid():
            print("hello")
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            consumer = Consumer.objects.create(
                user=user,
                grade=1,
                benefit_agree=benefit_agree,
                kakao_farmer_agree=kakao_farmer_agree,
                kakao_comment_agree=kakao_comment_agree,
            )

            if addressform.is_valid():
                print(addressform.cleaned_data["is_jeju_mountain"])
                address = addressform.save(commit=False)
                address.user = user
                address.is_default = True
                address.save()

                consumer.default_address = address
                consumer.save()

            if user is not None:
                login(request, user=user)
                return redirect(reverse("core:main"))

        ctx = {
            "form": form,
            "addressform": addressform,
        }
        return render(request, "users/signup.html", ctx)


# id validation function for AJAX
def idValidation(request):
    target = request.GET.get("target")
    isValid = User.objects.filter(username=target).exists()
    print(target)
    print(isValid)

    ctx = {"target": target, "isValid": isValid}

    return JsonResponse(ctx)


# email validation function for AJAX
def emailValidation(request):
    target = request.GET.get("target")
    isValid = User.objects.filter(email=target).exists()
    print(target)
    print(isValid)

    ctx = {"target": target, "isValid": isValid}

    return JsonResponse(ctx)


# nickname validation function for AJAX
def nicknameValidation(request):
    target = request.GET.get("target")
    isValid = User.objects.filter(nickname=target).exists()

    ctx = {"target": target, "isValid": isValid}

    return JsonResponse(ctx)


def phoneNumberValidation(request):
    """phone number validation function for AJAX"""

    target = request.GET.get("target")  # 전화번호
    isValid = User.objects.filter(phone_number=target).exists()  # 유저 존재 여부

    if not isValid:
        try:  # 재발급
            userAuth = PhoneNumberAuth.objects.get(phone_num=target)
            timeOver = timezone.now() - userAuth.update_at > timezone.timedelta(minutes=5)
            if timeOver:
                auth_num = randint(100000, 1000000)
                message = {"#{인증번호}": auth_num}
                userAuth.auth_num = auth_num
                userAuth.update_at = timezone.localtime()
                userAuth.save()
                print("send sms", auth_num)
                send_sms(target, auth_num)
                # send_kakao_message(target, templateIdList["signup"], message)
            else:
                pass
        except PhoneNumberAuth.DoesNotExist:  # 신규발급
            auth_num = randint(100000, 1000000)
            message = {"#{인증번호}": auth_num}
            userAuth = PhoneNumberAuth.objects.create(phone_num=target, auth_num=auth_num)
            print("send sms", auth_num)
            send_sms(target, auth_num)
            # send_kakao_message(target, templateIdList["signup"], message)

    ctx = {"target": target, "isValid": isValid}
    return JsonResponse(ctx)


def phoneNumberAuthentication(request):
    """phone number authentication function for AJAX"""

    phone_num = request.GET.get("phone_num")  # 전화번호
    auth_num = request.GET.get("auth_num")  # 인증번호

    try:
        userAuth = PhoneNumberAuth.objects.get(phone_num=phone_num)
        timeOver = timezone.now() - userAuth.update_at > timezone.timedelta(minutes=5)
        print("현재 시간", timezone.now())
        print("마지막 수정 시간", userAuth.update_at)
        if auth_num != userAuth.auth_num:
            isValid = False
        elif (not timeOver) and (auth_num == userAuth.auth_num):
            timeOver = False
            isValid = True
        elif timeOver and auth_num == userAuth.auth_num:
            timeOver = True
            isValid = True
        print(timeOver)
        print(isValid)
        ctx = {
            "isValid": isValid,
            "timeOver": timeOver,
        }
        return JsonResponse(ctx)

    except PhoneNumberAuth.DoesNotExist:
        pass


def terms_of_service_popup(request):
    return render(request, "users/signup/terms_of_service_popup.html")


def personal_info_popup(request):
    return render()


user_email = ""


class MyPasswordResetView(PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")
    form_class = MyPasswordResetForm

    def form_valid(self, form):
        global user_email

        if User.objects.filter(email=self.request.POST.get("email")).exists() and User.objects.get(
            email=self.request.POST.get("email")
        ).username == self.request.POST.get("username"):
            user_email = form.cleaned_data.get("email")
            return super().form_valid(form)

        else:
            return render(self.request, "users/password_reset_done_fail.html")


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset_done.html"

    def get_context_data(self, **kwargs):
        global user_email
        ctx = super().get_context_data(**kwargs)
        ctx["email"] = user_email
        print(user_email)
        return ctx


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["new_password1"].widget.attrs = {"placeholder": "새 비밀번호를 입력해주세요"}
        form.fields["new_password2"].widget.attrs = {"placeholder": "새 비밀번호를 한번 더 입력해주세요"}

        return form

    def form_valid(self, form):
        return super().form_valid(form)


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"


@login_required
def mypage(request, cat):

    try:
        consumer = request.user.consumer
    except ObjectDoesNotExist:
        return redirect(reverse("core:main"))

    cat_name = str(cat)
    print(cat_name)

    if request.method == "GET":
        consumer_nickname = consumer.user.nickname
        sub_farmers = consumer.subs.all()  # pagenation 필요
        print(sub_farmers)
        if sub_farmers.exists() is False:
            print("구독자는 없다")
        questions = consumer.questions.order_by("-create_at")  # pagenation 필요
        print(questions)
        if questions.exists() is False:
            print("질문은 없다")
        try:
            groups = consumer.order_groups.all().exclude(status="waiting")
            print(groups)
            if groups.exists() is False:
                print("여기안와?")
                raise NoRelatedInstance
            for group in groups:
                details = group.order_details
                preparing_num = details.filter(status="preparing").count()
                print(preparing_num)
                delivery_num = details.filter(status="shipping").count()
                print(delivery_num)
                complete_num = details.filter(status="complete").count()
                print(complete_num)
                cancel_num = details.filter(status="cancel").count()
        except NoRelatedInstance:
            preparing_num = 0
            delivery_num = 0
            complete_num = 0
            cancel_num = 0

        # 구독 농가
        subs = consumer.subs.all().order_by("-create_at").all()
        if subs is None:
            subs_count = 0
        else:
            subs_count = subs.count()
        print("구독자 수 " + (str)(subs_count))

        # 상품 Q&A
        now = timezone.localtime()
        one_month_before = now + timedelta(days=-30)
        print(one_month_before)

        questions = (
            consumer.questions.filter(create_at__gt=one_month_before).order_by("-create_at").all()
        )
        print((type)(questions))

        for q in questions:
            print(type(q))

        ctx = {
            "consumer_nickname": consumer_nickname,
            "sub_farmers": sub_farmers,
            "questions": questions,
            "preparing_num": preparing_num,
            "delivery_num": delivery_num,
            "complete_num": complete_num,
            "cancel_num": cancel_num,
            "subs_count": subs_count,
            "subs": subs,
            "questions": questions,
        }

        if cat_name == "orders":
            page = int(request.GET.get("page", 1))
            start_date = request.GET.get("s_date", None)
            end_date = request.GET.get("e_date", None)
            page_size = 5

            if start_date == "None":
                start_date = None
            if end_date == "None":
                end_date = None

            print("start_date의 정체")
            print(start_date)
            print("end_date의 정체")
            print(end_date)

            if (start_date is None) and (end_date is None):
                # 주문관리 페이지에 처음 들어온 경우
                start_date = None
                end_date = None
                order_groups = groups.exclude(status="wait")
            else:
                # 날짜 필터링에서 조회 버튼을 누른 경우
                if start_date == "":
                    # filter start_date input에 아무런 value가 없을 경우
                    start_date = datetime.datetime.now(tz=get_current_timezone()).date()
                else:
                    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()

                if end_date == "":
                    # filter end_date input에 아무런 value가 없음 경우
                    end_date = datetime.datetime.now(tz=get_current_timezone()).date()
                    t = datetime.time(23, 59, 59)
                    converted_end_date = datetime.datetime.combine(end_date, t)

                else:
                    # end_date 23:59분까지 filter 해주기 위해서 시간까지 있는 converted_end_date로 변환
                    # ctx로 넘겨줄 때는 end_date를 넘겨주어야 함
                    converted_end_date = end_date + " 23:59:59"
                    print("바꾼 날짜는")
                    print(end_date)
                    converted_end_date = datetime.datetime.strptime(
                        converted_end_date, "%Y-%m-%d %H:%M:%S"
                    )

                order_groups = (
                    groups.filter(order_at__lte=converted_end_date, order_at__gte=start_date)
                    .exclude(status="wait")
                    .order_by("-order_at")
                )

            print(f"start_date : {start_date}")
            print(f"end_date : {end_date}")

            print(order_groups)
            if order_groups.exists():
                order_details = order_groups[0].order_details.all()
                print(order_groups.count())
                if order_groups.count() > 1:
                    for group in order_groups[1:]:
                        print(group.order_details.all())
                        order_details = order_details | group.order_details.all()
                order_details = order_details.order_by("-order_group__order_at")
            else:
                order_details = None

            print(order_details)
            if order_details is None:
                order_details_count = 0
                total_pages = 0
                offset = 0
            else:
                order_details_count = order_details.count()
                total_pages = ceil(order_details_count / page_size)
                offset = page * page_size - page_size
                order_details = order_details[offset : page * page_size]

            print("진짜")
            print(order_details)

            ctx_orders = {
                "total_pages": range(1, total_pages + 1),
                "order_details": order_details,
                "start_date": str(start_date),
                "end_date": str(end_date),
            }
            ctx.update(ctx_orders)
            return render(request, "users/mypage_orders.html", ctx)
        elif cat_name == "wishes":
            page = int(request.GET.get("page", 1))
            page_size = 5

            wishes = consumer.wishes.filter(product__open=True).order_by("-create_at")
            print(wishes)

            wishes_count = wishes.count()
            total_pages = ceil(wishes_count / page_size)
            offset = page * page_size - page_size
            wishes = wishes[offset : page * page_size]
            print(wishes)

            ctx_wishes = {
                "page": page,
                "total_pages": range(1, total_pages + 1),
                "wishes": wishes,
            }
            ctx.update(ctx_wishes)
            return render(request, "users/mypage_wishes.html", ctx)
        elif cat_name == "cart":
            carts = consumer.carts.all().order_by("-create_at").filter(product__open=True)
            print(carts)

            ctx_carts = {
                "carts": carts,
            }
            ctx.update(ctx_carts)
            return render(request, "users/mypage_carts.html", ctx)
        elif cat_name == "rev_address":
            print("왔댜")
            get_arg = request.GET.get("type", None)
            update_pk = request.GET.get("pk", None)
            if get_arg == "add":
                if request.method == "GET":
                    addressform = AddressForm()
                    ctx_add_rev_address = {
                        "addressform": addressform,
                    }
                    ctx.update(ctx_add_rev_address)
                    return render(request, "users/mypage_add_rev_address.html", ctx)
            elif get_arg == "update":
                address = Address.objects.get(pk=update_pk)
                addressform = AddressForm(instance=address)
                ctx_add_rev_address = {
                    "addressform": addressform,
                }
                ctx.update(ctx_add_rev_address)
                return render(request, "users/mypage_add_rev_address.html", ctx)
            else:
                rev_addresses = request.user.addresses.all().order_by("-create_at")
                ctx_rev_address = {
                    "rev_addresses": rev_addresses,
                }
                ctx.update(ctx_rev_address)
                return render(request, "users/mypage_rev_address.html", ctx)
        elif cat_name == "info":
            user = consumer.user

            info = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                # 'number':number,
                "email": user.email,
                "nickname": user.nickname,
                "profile_image": user.profile_image,
            }

            ctx.update(info)
            return render(request, "users/mypage_info.html", ctx)

    else:
        address_type = request.GET.get("type", None)
        print("post에 왔다")
        addressform = AddressForm(request.POST)
        user = request.user
        if addressform.is_valid():
            # [address UPDATE POST] 배송지 추가 페이지에서 새로운 배송지 등록 시, backend logic
            if address_type == "add":
                address = addressform.save(commit=False)
                address.user = user
                address.is_default = False
                address.save()
            # [address UPDATE POST] 기존에 등록된 배송지 수정 시, backend logic
            elif address_type == "update":
                update_pk = request.GET.get("pk", None)
                address = Address.objects.get(pk=update_pk)
                print(address)
                address.full_address = addressform.cleaned_data["full_address"]
                address.detail_address = addressform.cleaned_data["detail_address"]
                address.extra_address = addressform.cleaned_data["extra_address"]
                address.sido = addressform.cleaned_data["sido"]
                address.fsigungu = addressform.cleaned_data["sigungu"]
                address.save()
                print(address)

            return redirect(reverse("users:mypage", kwargs={"cat": "rev_address"}))
        else:
            # 404 페이지 제작 후 여기에 넣어야함
            return redirect(reverse("core:main"))


"""Order Popups"""


# def add_rev_address(request):
#     if request.method == 'GET':
#         addressform = AddressForm()
#         ctx = {
#             'addressform': addressform,
#         }
#         return render(request, 'users/mypage_add_rev_address.html', ctx)


class FindMyIdView(TemplateView):
    template_name = "users/find_my_id.html"  # to be added

    def get(self, request):
        form = FindMyIdForm()
        ctx = {
            "form": form,
        }

        return self.render_to_response(ctx)

    def post(self, request):
        form = FindMyIdForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print("hello")
            email = form.cleaned_data.get("email")

            try:
                user = User.objects.get(email=email)
                username = user.get_full_name()

                if form.cleaned_data.get("name") == username:
                    ctx = {"user": user}
                    return render(request, "users/find_my_id_complete.html", ctx)

                else:
                    raise User.DoesNotExist

            except User.DoesNotExist:
                return redirect(reverse("users:find_my_id_failed"))

        return redirect(reverse("users:find_my_id_failed"))


class FindMyIdFailView(TemplateView):
    template_name = "users/find_my_id_failed.html"


@method_decorator(login_required, name="dispatch")
class EditorMyPage(ListView):
    model = Editor_Review
    context_object_name = "reviews"
    template_name = "users/mypage/editor/editor_mypage_post_list.html"

    def get_queryset(self):
        user = self.request.user
        try:
            return Editor_Review.objects.filter(author=user.editor)

        except Editor.DoesNotExist:
            return None

    def render_to_response(self, context, **response_kwargs):
        if not Editor.objects.filter(user=self.request.user).exists():
            return redirect(reverse("core:main"))

        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editor"] = self.request.user.editor
        return context


@method_decorator(login_required, name="dispatch")
class EditorMyPage_Comments(ListView):
    model = Editor_Review_Comment
    context_object_name = "comments"
    template_name = "users/mypage/editor/editor_mypage_comments.html"

    def get_queryset(self):
        reviews = Editor_Review.objects.filter(author=self.request.user.editor)

        comments = Editor_Review_Comment.objects.filter(editor_review=reviews.first())

        for review in reviews:
            comments = comments.union(Editor_Review_Comment.objects.filter(editor_review=review))

        return comments.order_by("is_read")

    def render_to_response(self, context, **response_kwargs):
        if not Editor.objects.filter(user=self.request.user).exists():
            return redirect(reverse("core:main"))

        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editor"] = self.request.user.editor

        return context


@method_decorator(login_required, name="dispatch")
class EditorMypage_Info(TemplateView):
    template_name = "users/mypage/editor/editor_mypage_update.html"

    def render_to_response(self, context, **response_kwargs):
        if not Editor.objects.filter(user=self.request.user).exists():
            return redirect(reverse("core:main"))

        else:
            return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editor"] = Editor.objects.get(user=self.request.user)
        return context


def testview(request):
    return render(request, "users/mypage/user/order_cancel_popup.html")


def landing_test(request):
    """landing page AJAX before service open"""
    if request.method == "POST":
        user_pk = request.POST.get("user_pk", None)
        tester = User.objects.get(pk=user_pk)

        if (user_pk is not None) and (tester.username == "kakaotest"):
            data = {
                "status": 1,
            }
            return JsonResponse(data)
        else:
            data = {
                "status": 0,
            }
            return JsonResponse(data)


@method_decorator(login_required, name="dispatch")  ##loginrequired 안들어감
class ProductCommentCreate(TemplateView):
    template_name = "users/mypage/user/product_review_popup.html"

    def render_to_response(self, context, **response_kwargs):
        if not Consumer.objects.filter(user=self.request.user).exists():
            print("[GET] consumer has no user")
            return redirect(reverse("core:main"))
        else:
            return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consumer = Consumer.objects.get(user=self.request.user)
        print(f"[PRODUCT COMMENT GET] 사용자 : {consumer.user.account_name}")
        orderpk = self.kwargs["orderpk"]
        print(f"[PRODUCT COMMENT GET] orderpk : {orderpk}")
        detail = Order_Detail.objects.get(pk=self.kwargs["orderpk"])
        print(f"[PRODUCT COMMENT GET] Order Detail : {detail}")
        order_consumer = detail.order_group.consumer
        print(f"[PRODUCT COMMENT GET] order 사용자 : {order_consumer.user.account_name}")
        # 검증
        if order_consumer.pk != consumer.pk:
            print("[PRODUCT COMMENT GET] 올바르지 않은 사용자")
            return redirect(reverse("core:main"))
        form = ProductCommentForm()
        print("[PRODUCT COMMENT GET] form")
        context["detail"] = detail
        context["form"] = form
        print("[PRODUCT COMMENT GET] return 직전")
        return context

    def post(self, request, **kwargs):
        detail = self.get_context_data(**kwargs)["detail"]
        product_pk = detail.product.pk
        product_comment = ProductCommentForm(request.POST, request.FILES)
        consumer = Consumer.objects.get(pk=self.request.user.consumer.pk)
        product_eixst = Product_Comment.objects.filter(
            product=detail.product, consumer=consumer
        ).exists()
        print(f"[PRODUCT COMMENT POST] 사용자 : {consumer.user.account_name}")
        if product_comment.is_valid() and not product_eixst:
            text = product_comment.cleaned_data.get("text")
            freshness = product_comment.cleaned_data.get("freshness")
            flavor = product_comment.cleaned_data.get("flavor")
            cost_performance = product_comment.cleaned_data.get("cost_performance")
            product_comment = Product_Comment(
                text=text,
                freshness=int(freshness),
                flavor=int(flavor),
                cost_performance=int(cost_performance),
            )
            product_comment.consumer = consumer
            product_comment.product = detail.product
            product_comment.save()
            product_comment.product.reviews += 1

            product_comment.get_rating_avg()

            # Product_Comment_Image
            product_comment_imgs = request.FILES.getlist("product_image")
            img_valid = True

            if len(product_comment_imgs) == 1 and product_comment_imgs[0] == "":
                img_valid = False

            if img_valid == True:
                for img in product_comment_imgs:
                    images = Product_Comment_Image.objects.create(
                        product_comment=product_comment, image=img
                    )
                    images.save()

            # freshness
            if product_comment.freshness == 1:
                detail.product.freshness_1 += 1
            elif product_comment.freshness == 3:
                detail.product.freshness_3 += 1
            else:
                detail.product.freshness_5 += 1

            # flavor
            if product_comment.flavor == 1:
                detail.product.flavor_1 += 1
            elif product_comment.flavor == 3:
                detail.product.flavor_3 += 1
            else:
                detail.product.flavor_5 += 1

            # cost_performance
            if product_comment.cost_performance == 1:
                detail.product.cost_performance_1 += 1
            elif product_comment.cost_performance == 3:
                detail.product.cost_performance_3 += 1
            else:
                detail.product.cost_performance_5 += 1

            # total rating calculate
            detail.product.calculate_total_rating_sum(product_comment.avg)
            detail.product.calculate_total_rating_avg()

            # specific rating calculate
            detail.product.calculate_specific_rating(
                int(freshness), int(flavor), int(cost_performance)
            )
            print("[PRODUCT COMMENT POST] Post view 마지막")
            return redirect("core:popup_callback")

        return redirect("core:main")


def product_refund(request):
    addresses = [
        "서울 동작구 장승배기로 11가길 11(상도파크자이) 105동 1901호",
        "서울 동작구 장승배기로 11가길 11(상도파크자이) 104동 1102호",
        "서울 동작구 장승배기로 11가길 11(상도파크자이) 104동 1102호",
        "서울 동작구 장승배기로 11가길 11(상도파크자이) 104동 1102호",
        "서울 동작구 장승배기로 11가길 11(상도파크자이) 104동 1102호",
    ]
    return render(request, "users/mypage/user/product_refund_popup.html", {"addresses": addresses})
