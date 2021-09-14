from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView, RedirectView
from django.core import exceptions
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.templatetags.static import static
from requests.api import get
from math import ceil
import datetime
import json

# models
from .models import *
from products.models import Product, Question
from users.models import Consumer, Subscribe, User
from editor_reviews.models import Editor_Review
from orders.models import Order_Detail, Order_Group, RefundExchange
from comments.models import Farmer_Story_Comment, Product_Comment
from admins.models import FarmerNotice, FarmerNotification

# forms
from .forms import *
from comments.forms import FarmerStoryCommentForm, FarmerStoryRecommentForm
from users.forms import SignUpForm, LoginForm
from addresses.forms import AddressForm

from config import settings


# farmer's page
def farmers_page(request):
    # farmer list
    farmer = Farmer.objects.all().order_by("-id")
    paginator = Paginator(farmer, 3)
    page = request.GET.get("page")
    farmers = paginator.get_page(page)

    # weekly hot farmer
    best_farmers = farmer.order_by("-sub_count")[:1]  # 조회수 대신 임의로

    # farmer's story list
    farmer_story = Farmer_Story.objects.all()
    paginator_2 = Paginator(farmer_story, 7)
    page_2 = request.GET.get("page_2")
    farmer_stories = paginator_2.get_page(page_2)

    ctx = {
        "best_farmers": best_farmers,
        "farmers": farmers,
        "farmer_stories": farmer_stories,
    }
    return render(request, "farmers/farmers_page.html", ctx)


# farmer input 검색 view - for AJAX
def farmer_search(request):
    search_key = request.GET.get("search_key")  # 검색어 가져오기
    search_list = Farmer.objects.all()
    if search_key:  # 검색어 존재 시
        search_list = search_list.filter(
            Q(farm_name__contains=search_key) | Q(user__nickname__contains=search_key)
        )
    search_list = search_list.order_by("-id")
    paginator = Paginator(search_list, 10)
    page = request.GET.get("page")
    farmers = paginator.get_page(page)
    ctx = {
        "farmers": farmers,
    }
    return render(request, "farmers/farmer_search.html", ctx)


# farmer category(채소, 과일, E.T.C) 검색 view - for AJAX
def farm_cat_search(request):
    search_cat = request.GET.get("search_cat")
    farmer = Farmer.objects.filter(farm_cat=search_cat).order_by("-id")
    paginator = Paginator(farmer, 3)
    page = request.GET.get("page")
    farmers = paginator.get_page(page)
    ctx = {
        "farmers": farmers,
    }
    return render(request, "farmers/farmer_search.html", ctx)


# farmer tag 검색 view - for AJAX
def farm_tag_search(request):
    search_tag = request.GET.get("search_tag")
    farmer = Farm_Tag.objects.get(tag=search_tag).farmer.all().order_by("-id")
    paginator = Paginator(farmer, 3)
    page = request.GET.get("page")
    farmers = paginator.get_page(page)
    ctx = {
        "farmers": farmers,
    }
    return render(request, "farmers/farmer_search.html", ctx)


# farmer story 검색 view - for AJAX
def farmer_story_search(request):
    select_val = request.GET.get("select_val")
    search_key_2 = request.GET.get("search_key_2")
    search_list = Farmer_Story.objects.all()
    if search_key_2:
        if select_val == "title":
            search_list = search_list.filter(Q(title__contains=search_key_2))
        elif select_val == "farm":
            search_list = search_list.filter(Q(farmer__farm_name__contains=search_key_2))
        elif select_val == "farmer":
            search_list = search_list.filter(Q(farmer__user__nickname__contains=search_key_2))
    search_list = search_list.order_by("-id")
    paginator = Paginator(search_list, 10)
    page_2 = request.GET.get("page_2")
    farmer_stories = paginator.get_page(page_2)
    ctx = {
        "farmer_stories": farmer_stories,
    }
    return render(request, "farmers/farmer_story_search.html", ctx)


# farmer's story create page
def farmer_story_create(request):
    try:
        user = request.user.farmer
    except ObjectDoesNotExist:
        return redirect(reverse("core:main"))
    if request.method == "POST":
        form = FarmerStoryForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            # sub_title = form.cleaned_data.get('sub_title')
            content = form.cleaned_data.get("content")
            farmer_story = Farmer_Story(
                title=title,
                # sub_title=sub_title,
                content=content,
            )
            farmer_story.farmer = user
            farmer_story.save()
            return redirect(reverse("farmers:farmer_story_detail", args=[farmer_story.pk]))
        else:
            return redirect(reverse("core:main"))
    elif request.method == "GET":
        form = FarmerStoryForm()
        ctx = {
            "form": form,
        }
        return render(request, "farmers/farmer_story_create.html", ctx)


# farmer's story detail page
class Story_Detail(DetailView):
    model = Farmer_Story
    template_name = "farmers/farmer_story_detail.html"
    context_object_name = "main_story"

    def get_context_data(self, **kwargs):
        ctx = super(DetailView, self).get_context_data(**kwargs)
        farmer = self.get_object().farmer
        story = Farmer_Story.objects.all().order_by("-id")

        paginator = Paginator(story, 3)
        page = self.request.GET.get("page")
        stories = paginator.get_page(page)

        comments = self.get_object().farmer_story_comments.all()
        form = FarmerStoryCommentForm()

        ctx["farmer"] = farmer
        ctx["stories"] = stories
        ctx["tags"] = Farm_Tag.objects.all().filter(farmer=farmer)
        ctx["comments"] = comments
        ctx["form"] = form

        if self.request.user != AnonymousUser():
            ctx["user"] = self.request.user

        else:
            ctx["user"] = None

        return ctx

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)

        if self.request.session.get("_auth_user_id") is None:
            cookie_name = "farmer_story_hit"
        else:
            cookie_name = f'farmer_story_hit:{self.request.session["_auth_user_id"]}'

        if self.request.COOKIES.get(cookie_name) is None:
            response.set_cookie(cookie_name, self.kwargs["pk"], 3600)
            main_story = self.get_object()
            main_story.hits += 1
            main_story.save()
        else:
            cookie = self.request.COOKIES.get(cookie_name)
            cookies = cookie.split("|")

            if str(self.kwargs["pk"]) not in cookies:
                response.set_cookie(cookie_name, cookie + f'|{self.kwargs["pk"]}')
                main_story = self.get_object()
                main_story.hits += 1
                main_story.save()

        return response


# farmer detail page
def farmer_detail(request, pk):
    farmer = Farmer.objects.get(pk=pk)
    tags = Farm_Tag.objects.all().filter(farmer=farmer)
    products = Product.objects.all().filter(farmer=farmer)
    stories = Farmer_Story.objects.all().filter(farmer=farmer)
    editor_reviews = Editor_Review.objects.filter(farm=farmer)
    try:
        sub = Subscribe.objects.get(farmer__pk=farmer.pk, consumer=request.user.consumer)
    except:
        sub = False
    ctx = {
        "farmer": farmer,
        "tags": tags,
        "products": products,
        "stories": stories,
        "editor_reviews": editor_reviews,
        "sub": sub,
    }
    return render(request, "farmers/farmer_detail.html", ctx)


# 입점 신청 page
def farm_apply(request):
    if request.method == "POST":
        form = FarmApplyForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "farmers/farm_apply_complete.html")
        else:
            return redirect(reverse("core:main"))
    else:
        form = FarmApplyForm()
        ctx = {
            "form": form,
        }
        return render(request, "farmers/farm_apply.html", ctx)


def enroll_page1(request):
    """입점 등록 1단계 (회원가입)"""

    if request.method == "GET":
        form = SignUpForm()
        addressform = AddressForm()
        ctx = {
            "form": form,
            "addressform": addressform,
        }
        return render(request, "farmers/enroll/farm_enroll_1.html", ctx)

    elif request.method == "POST":
        form = SignUpForm(request.POST)
        addressform = AddressForm(request.POST)
        if form.is_valid() and addressform.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            address = addressform.save(commit=False)
            address.user = user
            address.is_default = True
            address.save()
            consumer = Consumer.objects.create(user=user, grade=1, default_address=address)
            if user is not None:
                login(request, user=user)
                return redirect("farmers:enroll_page2", consumer.pk)
        ctx = {
            "form": form,
            "addressform": addressform,
        }
        return render(request, "farmers/enroll/farm_enroll_1.html", ctx)


def enroll_page2(request, consumerpk):
    """입점 등록 2단계 (파머 정보 입력)"""

    if request.method == "GET":
        if request.user.consumer.pk == consumerpk:
            farm_form = FarmEnrollForm()
            ctx = {
                "farm_form": farm_form,
            }
            return render(request, "farmers/enroll/farm_enroll_2.html", ctx)
        else:
            return redirect("core:main")

    elif request.method == "POST":
        consumer = Consumer.objects.get(pk=consumerpk)
        farm_form = FarmEnrollForm(request.POST, request.FILES)
        farm_tags = request.POST.get("farm_tag[]")

        if farm_form.is_valid():
            # if farm_form.cleaned_data["farmer_profile"] is None:
            #     farm_form.farmer_profile = static("images/farm/farmer_default.svg")
            # if farm_form.cleaned_data["farm_profile"] is None:
            #     farm_form.farm_profile = static("images/farm/farm_default.svg")
            farmer = farm_form.save(commit=False)
            farmer.user = consumer.user
            farmer.address = consumer.default_address
            farmer.save()
            farm_tag_list = farm_tags.split(",")
            for tag in farm_tag_list:
                if tag != "":
                    farm_tag = Farm_Tag.objects.get_or_create(tag=tag)[0]
                    farm_tag.farmer.add(farmer)
            return redirect("farmers:enroll_page3", farmer.pk)

        ctx = {
            "farm_form": farm_form,
        }
        return render(request, "farmers/enroll/farm_enroll_2.html", ctx)


def enroll_page3(request, farmerpk):
    """입점 등록 3단계 (계약서 작성)"""

    farmer = Farmer.objects.get(pk=farmerpk)
    if request.method == "GET":
        if request.user.consumer.pk == farmer.user.consumer.pk:
            return render(request, "farmers/enroll/farm_enroll_3.html")
        else:
            return redirect("core:main")

    elif request.method == "POST":
        agree_1 = request.POST.get("agree-1")
        agree_2 = request.POST.get("agree-2")
        farmer = Farmer.objects.get(pk=farmerpk)
        if agree_1 is not None and agree_2 is not None:
            farmer.contract = True
            return redirect("farmers:farmer_mypage_product")
        return render(request, "farmers/enroll/farm_enroll_3.html")

    return render(request, "farmers/enroll/farm_enroll_3.html")


class FarmEnrollLogin(TemplateView):
    template_name = "farmers/enroll/farm_enroll_login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = LoginForm()
        return context

    def post(self, request, **kwargs):
        form = LoginForm(self.request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(self.request, username=username, password=password)
            if user is not None:
                keep_login = self.request.POST.get("auto_login", False)
                if keep_login:
                    settings.base.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                login(self.request, user=user)
                consumer = Consumer.objects.get(user=user)
                return redirect("farmers:enroll_page2", consumer.pk)
        return render(self.request, "farmers/enroll/farm_enroll_login.html")


"""
Farmer mypage section
"""


class FarmerMyPageBase(ListView):
    def dispatch(self, request, *args, **kwargs):
        """로그인한 farmer외의 접근을 막는 코드입니다. 절대 수정 금지"""

        if (
            self.request.user == AnonymousUser()
            or not Farmer.objects.filter(user=self.request.user).exists()
        ):
            return redirect("core:main")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """context에 필요한 내용은 각 클래스에서 overriding하여 추가"""

        context = super().get_context_data(**kwargs)
        context["farmer"] = Farmer.objects.get(user=self.request.user)

        orders = Order_Detail.objects.filter(product__farmer=self.request.user.farmer).exclude(
            status="wait"
        )
        context["overall_orders"] = orders
        context["new_orders"] = orders.filter(status="payment_complete")
        context["preparing_orders"] = orders.filter(status="preparing")
        context["shipping_orders"] = orders.filter(status="shipping")
        context["delivered_orders"] = orders.filter(status="delivery_complete")
        context["claimed_orders"] = orders.filter(
            Q(status="re_ex_recept") | Q(status="re_ex_approve") | Q(status="re_ex_deny")
        )

        return context


class FarmerMyPageOrderManage(FarmerMyPageBase):
    """농가 주문관리 페이지"""

    model = Order_Detail
    context_object_name = "orders"
    template_name = "farmers/mypage/order/farmer_mypage_order.html"
    paginate_by = 5

    def get_queryset(self):
        status = self.request.GET.get("status", None)
        q = self.request.GET.get("q", None)
        start_date = self.request.GET.get("start-date", None)
        end_date = self.request.GET.get("end-date", None)

        qs = (
            Order_Detail.objects.filter(product__farmer=self.request.user.farmer)
            .order_by("order_group")
            .exclude(status="wait")
        )

        print(qs)

        if status:
            qs = qs.filter(status=status)

        if q:
            qs = qs.filter(order_group__consumer__user__nickname__icontains=q)

        if start_date and end_date:
            converted_end_date = end_date + " 23:59:59"
            converted_end_date = datetime.datetime.strptime(converted_end_date, "%Y-%m-%d %H:%M:%S")

            qs = qs.filter(update_at__lte=converted_end_date, update_at__gte=start_date)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = self.request.GET.get("status", None)
        context["q"] = self.request.GET.get("q", None)
        return context


def farmer_mypage_order_state_update(request):
    if request.is_ajax():
        pk = request.POST.get("pk", None)
        state = request.POST.get("state", None)

        order = Order_Detail.objects.get(pk=pk)
        order.status = state
        order.save()

        return HttpResponse("주문을 수락하였습니다", status=200)


class FarmerMyPageProductManage(FarmerMyPageBase):
    """농가 상품관리 페이지"""

    model = Product
    context_object_name = "products"
    template_name = "farmers/mypage/product/farmer_mypage_product.html"

    def get_queryset(self):
        products = Product.objects.filter(farmer=self.request.user.farmer)
        q = self.request.GET.get("q", None)
        status = self.request.GET.get("status", None)

        if status:
            products = products.filter(status=status)

        if q:
            products = products.filter(title__icontains=q)

        return products

    def get_context_data(self, **kwargs):
        products = Product.objects.filter(farmer=self.request.user.farmer)

        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", None)
        context["status"] = self.request.GET.get("status", None)
        context["pending"] = products.filter(status="pending")
        context["sale"] = products.filter(status="sale")
        context["suspended"] = products.filter(status="suspended")
        context["soldout"] = products.filter(status="soldout")

        return context


class FarmerMyPagePaymentManage(FarmerMyPageBase):
    """농가 정산관리 페이지"""

    model = Order_Detail
    context_object_name = "orders"
    templagte_name = "farmers/mypage/payment/farmer_mypage_payment.html"

    def get_queryset(self):
        qs = Order_Detail.objects.filter(product__farmer=self.request.user.farmer)
        status = self.request.GET.get("status", None)
        q = self.request.GET.get("q", None)
        search_key = self.request.GET.get("searchKey", None)

        if status:
            qs = qs.filter(payment_status=status)

        if q:
            if search_key == "order_number":
                qs = qs.filter(order_management_number=q)

            elif search_key == "product_name":
                qs = qs.filter(product__contains=q)

        return qs


class FarmerMyPageReviewQnAManage(FarmerMyPageBase):
    """농가 문의/리뷰관리 페이지"""

    model = Farmer
    template_name = "farmers/mypage/farmer_mypage_review_qna.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = self.request.GET.get("start-date", None)
        end_date = self.request.GET.get("end-date", None)

        # 문의
        questions = Question.objects.filter(product__farmer=self.request.user.farmer).order_by(
            "-id"
        )
        if start_date and end_date:
            converted_end_date = end_date + " 23:59:59"
            converted_end_date = datetime.datetime.strptime(converted_end_date, "%Y-%m-%d %H:%M:%S")

            questions = questions.filter(
                create_at__lte=converted_end_date, create_at__gte=start_date
            )

        page = self.request.GET.get("page")
        paginator = Paginator(questions, 5)
        questions = paginator.get_page(page)
        context["questions"] = questions

        # 리뷰
        reviews = Product_Comment.objects.filter(product__farmer=self.request.user.farmer).order_by(
            "-id"
        )
        if start_date and end_date:
            converted_end_date = end_date + " 23:59:59"
            converted_end_date = datetime.datetime.strptime(converted_end_date, "%Y-%m-%d %H:%M:%S")
            reviews = reviews.filter(create_at__lte=converted_end_date, create_at__gte=start_date)

        page2 = self.request.GET.get("page2")
        paginator2 = Paginator(reviews, 5)
        reviews = paginator2.get_page(page2)
        context["total_range"] = range(0, 5)
        context["reviews"] = reviews

        return context


class FarmerMyPageNotificationManage(FarmerMyPageBase):
    """농가 알림 페이지"""

    model = Farmer
    template_name = "farmers/mypage/farmer_mypage_notification.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = FarmerNotification.objects.all().order_by("-id")
        new_notifications = []
        for noti in notifications:
            if noti.is_read == False:
                new_notifications.append(noti)

        page = self.request.GET.get("page")
        paginator = Paginator(notifications, 5)
        notifications = paginator.get_page(page)
        context["notifications"] = notifications
        context["new_notifications"] = len(new_notifications)

        # # query_set for first page
        # first_page = notifications.page(1).object_list
        # context["first_page"] = first_page
        # # range of page ex range(1, 3)
        # page_range = notifications.page_range
        # context["page_range"] = page_range

        return context


class FarmerMyPageInfoManage(FarmerMyPageBase):
    """농가 정보 수정 페이지"""

    model = Farmer
    template_name = "farmers/mypage/farmer_mypage_info_update.html"

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        if self.request.user != AnonymousUser():
            try:
                farmer = self.request.user.farmer
                if self.request.method == "POST":
                    farm_form = FarmEnrollForm(
                        self.request.POST, self.request.FILES, instance=farmer
                    )
                elif self.request.method == "GET":
                    farm_form = FarmEnrollForm(instance=farmer)
            except ObjectDoesNotExist:
                return redirect(reverse("core:main"))
        else:
            return redirect(reverse("core:main"))

        return response


def farm_news_update(request):
    if request.is_ajax():
        farmer = Farmer.objects.get(user=request.user)
        farm_news_content = request.POST.get("content")

        farmer.farm_news = farm_news_content
        farmer.save()

        ctx = {"content": farm_news_content}

        return JsonResponse(ctx)

    return HttpResponseBadRequest("잘못된 접근입니다.")


class FarmerMyPageNotice(FarmerMyPageBase):
    """농가 공지사항 페이지"""

    model = FarmerNotice
    template_name = "farmers/mypage/farmer_mypage_notice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notice = FarmerNotice.objects.all()
        notice_cnt = notice.count()

        page_num = self.request.GET.get("page", 1)
        page_size = 5

        total_pages = (ceil)(notice_cnt / page_size)

        # page_num이 이상한 값이 전달되면 첫번째 페이지로 초기화
        if page_num > total_pages or page_num <= 0:
            page_num = 1

        offset = page_num * page_size
        # notice = notice[offset-5:offset]

        context["object_list"] = context["object_list"][offset - 5 : offset]

        context["total_pages"] = range(1, total_pages + 1)
        context["page_num"] = page_num

        print(context)

        return context


"""
Farmer Mypage Popups
"""


class FarmerMyPagePopupBase(DetailView):
    model = Order_Detail
    context_object_name = "order"


class FarmerMyPageOrderCheckPopup(FarmerMyPagePopupBase):
    """주문 확인 팝업"""

    template_name = "farmers/mypage/order/order_confirm_popup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(order_details__pk=self.kwargs["pk"]).order_by(
            "kinds"
        )

        print(context["products"])
        return context

    def post(self, request, **kwargs):
        order = self.get_object()
        order.status = "preparing"
        order.save()

        return redirect("core:popup_callback")

    def render_to_response(self, ctx, **kwargs):
        order = self.get_object()
        if order.status != "payment_complete":
            return redirect("core:main")

        return super().render_to_response(ctx, **kwargs)


class FarmerMypPageProductStateUpdate(FarmerMyPagePopupBase):
    """상품 상태 수정 팝업"""

    model = Product
    template_name = "farmers/mypage/product/product_state_update_popup.html"
    context_object_name = "product"

    def get_queryset(self, **kwargs):
        return Product.objects.filter(pk=self.kwargs["pk"])

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().farmer != self.request.user.farmer:
            return redirect("core:main")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        product = self.get_queryset()

        state = request.POST.get("sell")
        weight = request.POST.get("weight", product[0].weight)
        weight_unit = request.POST.get("weight_unit", product[0].weight_unit)
        quantity = request.POST.get("quantity", product[0].stock)

        product.update(
            **{
                "status": state,
                "weight": weight,
                "weight_unit": weight_unit,
                "stock": quantity,
            }
        )

        return redirect("core:popup_callback")


class FarmerMypageInvoiceUpdatePopup(FarmerMyPagePopupBase):
    """주문 송장입력 팝업"""

    template_name = "farmers/mypage/order/invoice_info_popup.html"
    context_object_name = "order"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().product.farmer != self.request.user.farmer:
            return redirect("core:main")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        return Order_Detail.objects.filter(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(order_details__pk=self.kwargs["pk"]).order_by(
            "kinds"
        )
        return context

    def post(self, request, **kwargs):
        order = self.get_queryset()
        invoice_number = self.request.POST.get("invoice_number", None)
        logis_company = self.request.POST.get("invoice-select")

        order.update(**{"invoice_number": invoice_number})

        return redirect("core:popup_callback")


class FarmerMyPageRefundRequestCheckPopup(FarmerMyPagePopupBase):
    """반품 요청 확인 팝업"""

    template_name = "farmers/mypage/order/product_refund_request_commit.html"
    context_object_name = "order_detail"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().product.farmer != self.request.user.farmer:
            return redirect("core:main")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        return Order_Detail.objects.filter(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["refund"] = RefundExchange.objects.get(order_detail=self.kwargs["pk"])
        context["products"] = Product.objects.filter(order_details__pk=self.kwargs["pk"]).order_by(
            "kinds"
        )
        context["consumer"] = Consumer.objects.get(
            order_groups__order_details__pk=self.kwargs["pk"]
        )
        return context

    def post(self, request, **kwargs):
        refund = RefundExchange.objects.filter(order_detail=self.kwargs["pk"])
        farmer_answer = self.request.POST.get("farmer_answer", None)
        refund.update(farmer_answer=farmer_answer)
        if "deny" in self.request.POST:
            refund.update(claim_status="deny")
            return redirect("core:popup_callback")  # 추후 redirect 수정
        elif "approve" in self.request.POST:
            refund.update(claim_status="approve")
            return redirect("core:popup_callback")  # 추후 redirect 수정
        else:
            return redirect("core:popup_callback")


class FarmerMyPageExchangeRequestCheckPopup(FarmerMyPagePopupBase):
    """교환 요청 확인 팝업"""

    template_name = "farmers/mypage/order/product_exchange_request_commit.html"
    context_object_name = "order_detail"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().product.farmer != self.request.user.farmer:
            return redirect("core:main")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        return Order_Detail.objects.filter(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["exchange"] = RefundExchange.objects.get(order_detail=self.kwargs["pk"])
        context["products"] = Product.objects.filter(order_details__pk=self.kwargs["pk"]).order_by(
            "kinds"
        )
        context["consumer"] = Consumer.objects.get(
            order_groups__order_details__pk=self.kwargs["pk"]
        )
        return context

    def post(self, request, **kwargs):
        exchange = RefundExchange.objects.filter(order_detail=self.kwargs["pk"])
        farmer_answer = self.request.POST.get("farmer_answer", None)
        exchange.update(farmer_answer=farmer_answer)
        if "deny" in self.request.POST:
            exchange.update(claim_status="deny")
            return redirect("core:popup_callback")  # 추후 redirect 수정
        elif "approve" in self.request.POST:
            exchange.update(claim_status="approve")
            return redirect("core:popup_callback")  # 추후 redirect 수정
        else:
            return redirect("core:popup_callback")


class FarmerMypagePopupCallback(RedirectView):
    """팝업 페이지 확인 후 콜백"""

    pattern_name = "core:main"


"""
Mypage Pagination with AJAX
"""


def notification_ajax(request):
    """마이페이지 알림 Pagination"""

    page = request.GET.get("page")
    notifications = FarmerNotification.objects.all().order_by("-id")
    paginator = Paginator(notifications, 5)
    notifications = paginator.get_page(page)
    ctx = {
        "notifications": notifications,
    }
    return render(request, "farmers/mypage/farmer_mypage_notification_ajax.html", ctx)


def qna_ajax(request):
    """마이페이지 문의 Pagination"""

    page = request.GET.get("page")
    start_date = request.GET.get("start-date", None)
    end_date = request.GET.get("end-date", None)
    questions = Question.objects.filter(product__farmer=request.user.farmer).order_by("-id")

    if start_date and end_date:
        converted_end_date = end_date + " 23:59:59"
        converted_end_date = datetime.datetime.strptime(converted_end_date, "%Y-%m-%d %H:%M:%S")
        questions = questions.filter(create_at__lte=converted_end_date, create_at__gte=start_date)

    paginator = Paginator(questions, 5)
    questions = paginator.get_page(page)

    ctx = {
        "questions": questions,
    }
    return render(request, "farmers/mypage/farmer_mypage_qna_ajax.html", ctx)


def review_ajax(request):
    """마이페이지 리뷰 Pagination"""

    page = request.GET.get("page2")
    start_date = request.GET.get("start-date", None)
    end_date = request.GET.get("end-date", None)
    reviews = Product_Comment.objects.filter(product__farmer=request.user.farmer).order_by("-id")

    if start_date and end_date:
        converted_end_date = end_date + " 23:59:59"
        converted_end_date = datetime.datetime.strptime(converted_end_date, "%Y-%m-%d %H:%M:%S")
        reviews = reviews.filter(create_at__lte=converted_end_date, create_at__gte=start_date)

    paginator = Paginator(reviews, 5)
    reviews = paginator.get_page(page)
    ctx = {
        "reviews": reviews,
    }
    return render(request, "farmers/mypage/farmer_mypage_review_ajax.html", ctx)


def product_refund(request):
    addresses = [
        "서울 동작구 장승배기로 11가길 11(상도파크자이) 105동 1901호",
        "서울 동작구 장승배기로 11가길 11(상도파크자이) 104동 1102호",
        "서울 동작구 장승배기로 11가길 11(상도파크자이) 104동 1102호",
        "서울 동작구 장승배기로 11가길 11(상도파크자이) 104동 1102호",
        "서울 동작구 장승배기로 11가길 11(상도파크자이) 104동 1102호",
    ]
    return render(
        request,
        "farmers/mypage/order/product_refund_popup.html",
        {"addresses": addresses},
    )
