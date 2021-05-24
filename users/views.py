from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
from .models import (
    Subscribe,
    Cart,
    Consumer,
    Wish,
    User,
    Editor,
)
from farmers.models import Farmer
from products.models import Category, Product
from editor_reviews.models import Editor_Review
from comments.models import Editor_Review_Comment
from farmers.models import Farmer
from django.db.models import Count
from math import ceil
from datetime import timedelta
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from .forms import LoginForm, SignUpForm, MyPasswordResetForm, FindMyIdForm
from django.views.decorators.http import require_POST
from django.views.generic.detail import DetailView
from .forms import (
    LoginForm,
    SignUpForm,
    MyPasswordResetForm,
)
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from addresses.forms import AddressForm
from addresses.models import Address
from math import ceil
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.views.generic import DetailView
import datetime


# Exception 선언 SECTION


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
def CancelSubs(request):
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
        ctx = {
            "form": form,
        }
        return render(request, "users/login.html", ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                keep_login = self.request.POST.get("auto_login", False)
                print(keep_login)
                if keep_login:
                    settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False

                login(request, user=user)
                return redirect(reverse("core:main"))
        ctx = {
            "form": form,
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
            "form": form,
            "addressform": addressform,
        }
        return render(request, "users/signup.html", ctx)

    def post(self, request):
        form = SignUpForm(request.POST)
        addressform = AddressForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            Consumer.objects.create(user=user, grade=1)

            address = addressform.save(commit=False)
            address.user = user
            address.is_default = True
            address.save()

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
                    start_date = datetime.datetime.now().date()
                else:
                    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()

                if end_date == "":
                    # filter end_date input에 아무런 value가 없음 경우
                    end_date = datetime.datetime.now().date()
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

                print("날짜 필드 알아보기")
                print(groups[0].order_at)

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
            get_arg = request.GET.get("add", None)
            if get_arg == "go":
                if request.method == "GET":
                    addressform = AddressForm()
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
        get_arg = request.GET.get("add", None)
        print("post에 왔다")
        addressform = AddressForm(request.POST)
        if addressform.is_valid():
            user = request.user
            address = addressform.save(commit=False)
            address.user = user
            address.is_default = False
            address.save()
            return redirect(reverse("users:mypage", kwargs={"cat": "rev_address"}))


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


class FindMyIdFailView(TemplateView):
    template_name = "users/find_my_id_failed.html"


@method_decorator(login_required, name="dispatch")
class EditorMyPage(ListView):
    model = Editor_Review
    context_object_name = "reviews"
    template_name = "users/editor_mypage_post_list.html"

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
    template_name = "users/editor_mypage_comments.html"

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
    template_name = "users/editor_mypage_update.html"

    def render_to_response(self, context, **response_kwargs):
        if not Editor.objects.filter(user=self.request.user).exists():
            return redirect(reverse("core:main"))

        else:
            return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editor"] = Editor.objects.get(user=self.request.user)
        return context
