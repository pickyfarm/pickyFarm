from pickle import FALSE
from django.db.models import Q
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, redirect, reverse
from django.http import request, JsonResponse, HttpResponse
from django.views.generic import ListView
from django.core import serializers
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Product_Group, Product, Category, Question, Answer
from users.models import Subscribe
from comments.models import Product_Comment
from .forms import Question_Form, Answer_Form
from comments.forms import ProductRecommentForm
from django.utils import timezone, dateformat
from .utils import get_product_db, get_product_db_daum
from math import ceil
from django.core.exceptions import ObjectDoesNotExist
from django import template
from datetime import date
import locale
import json


# ajax 이용시, http Fail status 장착한 response 생성
class FailedJsonResponse(JsonResponse):
    def __init__(self, data):
        super().__init__(data)
        data.status_code = 400


class StoreList(ListView):
    model = Product_Group
    context_object_name = "products"
    template_name = "products/product_list_new.html"

    def get_queryset(self):
        qs = super().get_queryset().exclude(title="피키팜 테스트 상품그룹").order_by("-open", "-create_at")
        cat_name = self.request.GET.get("cat", "all")
        kind = self.request.GET.get("kind", "all")

        if kind == "ugly" or kind == "normal":
            qs = qs.filter(Q(kinds=kind) | Q(kinds="mix"))

        if cat_name == "fruit" or cat_name == "vege" or cat_name == "etc":
            qs = qs.filter(category__parent__slug=cat_name)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["cat"] = self.request.GET.get("cat", "all")
        context["kind"] = self.request.GET.get("kind", "all")

        return context


def store_list_all(request):
    cat_name = "all"
    page = int(request.GET.get("page", 1))
    sort = request.GET.get("sort", "최신순")
    kind = request.GET.get("kind", "all")
    page_size = 15
    limit = page_size * page
    offset = limit - page_size
    products_count = Product_Group.objects.all().count()
    products = Product_Group.objects.exclude(title="피키팜 테스트 상품그룹").order_by("-open", "-create_at")

    if sort == "인기순":
        for product in products:
            product.calculate_sales_rate()
        products = products.order_by("-open", "-sales_rate")
    elif sort == "마감임박순":
        products = products.order_by("-open", "stock")

    if (kind == "ugly") or (kind == "normal"):
        products = products.filter(Q(kinds=kind) | Q(kinds="mix"))

    products = products[offset:limit]

    categories = Category.objects.filter(parent=None).order_by("name")
    page_total = ceil(products_count / page_size)
    ctx = {
        "cat_name": cat_name,
        "products": products,
        "categories": categories,
        "page": page,
        "page_total": page_total,
        "page_range": range(1, page_total),
    }
    return render(request, "products/products_list.html", ctx)


def store_list_cat(request, cat):
    big_cat = ["fruit", "vege", "others"]
    cat_name = str(cat)
    products = []
    page = int(request.GET.get("page", 1))
    sort = request.GET.get("sort", "최신순")
    kind = request.GET.get("kind", "all")
    page_size = 15
    limit = page_size * page
    offset = limit - page_size
    if cat_name in big_cat:
        big_category = Category.objects.get(slug=cat)

        categories = big_category.children.all().order_by("name")
        try:
            products = (
                Product_Group.objects.filter(category__parent__slug=cat)
                .exclude(title="피키팜 테스트 상품그룹")
                .order_by("-open", "create_at")
            )
        except ObjectDoesNotExist:
            ctx = {
                "cat_name": cat_name,
                "big_category": big_category,
            }
            return render(request, "products/products_list.html", ctx)
    else:
        big_cat_name = {"과일": "fruit", "야채": "vege", "기타": "others"}
        categories = Category.objects.get(slug=cat)

        cat_name = big_cat_name[categories.parent.name]

        try:
            products = categories.product_groups.exclude(title="피키팜 테스트 상품그룹").order_by(
                "-open", "-create_at"
            )
            categories = categories.parent.children.all().order_by("name")
        except ObjectDoesNotExist:
            ctx = {
                "cat_name": cat_name,
                "cateogries": categories,
            }
            return render(request, "products/products_list.html", ctx)

    if sort == "인기순":
        for product in products:
            product.calculate_sales_rate()
        products = products.order_by("-open", "sales_rate")
    elif sort == "마감임박순":
        products = products.order_by("-open", "stock")

    if (kind == "ugly") or (kind == "normal"):
        products = products.filter(Q(kinds=kind) | Q(kinds="mix"))

    products_count = products.count()
    products = products[offset:limit]

    if products_count == 0:
        page_total = 1
    else:
        page_total = ceil(products_count / page_size)

    ctx = {
        "products": products,
        "cat_name": cat_name,
        "categories": categories,
        "page": page,
        "page_total": page_total,
        "page_range": range(1, page_total + 1),
    }
    return render(request, "products/products_list.html", ctx)


register = template.Library()


@register.filter(name="range")
def _range(_min, args=None):
    _max, _step = None, None
    if args:
        if not isinstance(args, int):
            _max, _step = map(int, args.split(","))
        else:
            _max = args
    args = filter(None, (_min, _max, _step))
    return range(*args)


def product_detail(request, pk):
    try:
        product_pk = pk
        product = Product.objects.get(pk=pk)

        kinds = product.kinds
        farmer = product.farmer
        subscribed = False
        if request.user.is_authenticated:
            subscribed = Subscribe.objects.filter(
                consumer=request.user.consumer, farmer=farmer
            ).exists()

        # 상품 리뷰
        siblings = product.get_sibling_products()
        print(siblings[1:])
        comments = Product_Comment.objects.filter(product=siblings[0])
        for p in siblings[1:]:
            comments = comments | p.product_comments.all()

        comments = comments.order_by("-create_at")
        total_comments = comments.count()
        page = request.GET.get("page")
        paginator = Paginator(comments, 5)
        comments = paginator.get_page(page)

        # 파머의 다른 상품 그룹 리뷰
        other_comments = Product_Comment.objects.filter(product__farmer=farmer).exclude(
            product__product_group=product.product_group
        )
        page1 = request.GET.get("page1")
        paginator1 = Paginator(other_comments, 2)
        other_comments = paginator1.get_page(page1)

        # 상품 문의
        questions = product.questions.all().order_by("-create_at")
        total_questions = questions.count()
        page2 = request.GET.get("page2")
        paginator2 = Paginator(questions, 5)
        questions = paginator2.get_page(page2)
        # product.calculate_total_rating_avg()
        total_score = product.product_group.total_avg
        total_percent = format(total_score / 5 * 100, ".1f")
        total_range = range(0, 5)

        recomment_form = ProductRecommentForm()

        # 연관 일반 작물
        related_product = product.related_product

        # freshness
        if product.product_group.total_reviews != 0:
            freshness_per = product.product_group.calculate_freshness_rating_avg()
        else:
            freshness_per = [0, 0, 0]

        # flavor
        if product.product_group.total_reviews != 0:
            flavor_per = product.product_group.calculate_flavor_rating_avg()
        else:
            flavor_per = [0, 0, 0]

        # cost_performance
        if product.product_group.total_reviews != 0:
            cost_performance_per = product.product_group.calculate_cost_rating_avg()
        else:
            cost_performance_per = [0, 0, 0]

        # 상세 정보
        product_harvest_start_date = dateformat.format(product.harvest_start_date, "Y년 m월 d일")
        product_harvest_end_date = dateformat.format(product.harvest_end_date, "Y년 m월 d일")
        product_shelf_life_date = product.shelf_life_date

        if product.related_product is not None:
            rel_product_harvest_start_date = dateformat.format(
                product.related_product.harvest_start_date, "Y년 m월 d일"
            )
            rel_product_harvest_end_date = dateformat.format(
                product.related_product.harvest_end_date, "Y년 m월 d일"
            )
            rel_product_shelf_life_date = product.related_product.shelf_life_date
        else:
            rel_product_harvest_start_date = None
            rel_product_harvest_end_date = None
            rel_product_shelf_life_date = None

        ctx = {
            "product_pk": product_pk,
            "product": product,
            "siblings": siblings,
            "subscribed": subscribed,
            "kinds": kinds,
            "farmer": farmer,
            "comments": comments,
            "other_comments": other_comments,
            "total_comments": total_comments,
            "questions": questions,
            "total_questions": total_questions,
            "total_score": range(int(total_score)),
            "remainder_score": range(5 - int(total_score)),
            "total_percent": total_percent,
            "total_range": total_range,
            "recomment_form": recomment_form,
            "freshness_1": freshness_per[0],
            "freshness_3": freshness_per[1],
            "freshness_5": freshness_per[2],
            "flavor_1": flavor_per[0],
            "flavor_3": flavor_per[1],
            "flavor_5": flavor_per[2],
            "cost_1": cost_performance_per[0],
            "cost_3": cost_performance_per[1],
            "cost_5": cost_performance_per[2],
            "related_product": related_product,
            "product_harvest_start_date": product_harvest_start_date,
            "product_harvest_end_date": product_harvest_end_date,
            "product_shelf_life_date": product_shelf_life_date,
            "rel_product_harvest_start_date": rel_product_harvest_start_date,
            "rel_product_harvest_end_date": rel_product_harvest_end_date,
            "rel_product_shelf_life_date": rel_product_shelf_life_date,
        }
        return render(request, "products/product_detail.html", ctx)
    except ObjectDoesNotExist:
        return redirect("/")


def comment_ajax(request, pk):
    """상품 리뷰 Pagination"""
    product = Product.objects.get(pk=pk)
    siblings = Product.objects.filter(product_group=product.product_group)
    comments = Product_Comment.objects.filter(product=siblings[0])
    for product in siblings[1:]:
        comments = comments | product.product_comments.all()
    comments = comments.order_by("-create_at")
    total_comments = comments.count()
    page = request.GET.get("page")
    paginator = Paginator(comments, 5)
    comments = paginator.get_page(page)
    ctx = {
        "product": product,
        "comments": comments,
        "total_comments": total_comments,
    }
    return render(request, "products/pagination/product_comment_ajax.html", ctx)


def question_ajax(request, pk):
    """상품 문의 Pagination"""
    product = Product.objects.get(pk=pk)
    questions = product.questions.all().order_by("-create_at")
    total_questions = questions.count()
    page = request.GET.get("page2")
    paginator2 = Paginator(questions, 5)
    questions = paginator2.get_page(page)
    ctx = {
        "product": product,
        "questions": questions,
        "total_questions": total_questions,
    }
    return render(request, "products/pagination/product_question_ajax.html", ctx)


# 상품 문의 pagination with ajax (수정 전)
def question_paging(request):
    product_pk = request.POST.get("product_pk", None)
    page_num = (int)(request.POST.get("page_num", None))

    try:
        product = Product.objects.get(pk=product_pk)
        questions = product.questions.all().order_by("-create_at")
    except ObjectDoesNotExist:
        data = {
            "status": 0,
        }
        return JsonResponse(data)

    offset = 5
    questions_limit = page_num * offset
    questions = questions[questions_limit - 5 : questions_limit]
    questions_list = []
    locale.setlocale(locale.LC_TIME, "ko_KR.UTF-8")
    for q in questions:
        q_dict = {"status": q.status}
        print(q_dict)
        q_dict["pk"] = q.pk
        q_dict["title"] = q.title
        print(q_dict)
        q_dict["consumer"] = q.consumer.user.nickname
        print(q_dict)
        q_dict["create_at"] = q.create_at.strftime("%Y년%m월%d일")
        print(q_dict)
        questions_list.append(q_dict)
        del q_dict

    print(questions_list)
    data = {"status": 1, "questions": questions_list}

    return JsonResponse(data)


@login_required
def create_question(request):
    product_pk = None
    consumer = request.user.consumer

    # GET 방식을 통해 product의 pk 값을 전달
    product_pk = int(request.GET.get("product"))
    print(f"싱품 pk : {product_pk}")

    # 문의 작성 GET - 문의 작성 가능한 form render
    if request.method == "GET":
        form = Question_Form()
        ctx = {
            "form": form,
        }
        return render(request, "products/create_question.html", ctx)
    else:
        # 문의 작성 POST - 제목, 글, 이미지 전달 받음
        form = Question_Form(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            image = form.cleaned_data.get("image")
            status = False
            try:
                product = Product.objects.get(pk=product_pk)
            except ObjectDoesNotExist:
                print("존재하지 않는 상품 pk")
                return redirect(reverse("core:main"))
            # 상품 문의 등록
            new_question = Question(
                title=title,
                content=content,
                image=image,
                status=status,
                consumer=consumer,
                product=product,
            )
            new_question.save()
            return redirect(reverse("products:product_detail", args=[product_pk]))
        else:
            # 상품 question create form validation 오류
            print("상품 question create form validation 오류")
            return redirect(reverse("core:main"))


@login_required
def read_qna(request, pk):

    # url pattern으로 전달 받은 Question pk 값으로 Question record 가져오기
    question = Question.objects.get(pk=pk)

    ctx = {
        "question": question,
        "answer": 0,
    }

    # 답변 완료된 문의라면 ctx의 answer에 answer record 넣기
    if question.status is True:
        print("상품 문의에 답변 있음")
        ctx["answer"] = question.answer

    # 답변 대기 중인 상태면 ctx의 answer에는 0이 전달됨
    return render(request, "products/read_question.html", ctx)


# 농가 마이페이지 - 문의/리뷰 관리 > 답변하기/답변수정 누를 시
@login_required
def create_answer(request, pk):

    question = Question.objects.get(pk=pk)
    product = question.product

    # 접근하는 유져가 농가 계정임을 확인
    try:
        farmer = request.user.farmer
    except:
        return redirect(reverse("core:main"))

    # 접근하는 농가 계정이 문의와 관련있는 농가 계정임을 확인
    if farmer is not product.farmer:
        return redirect(reverse("core:main"))

    # GET : 문의 내용과 답변 입력 form 반환
    if request.method == "GET":
        form = Answer_Form()
        ctx = {
            "question": question,
            "form": form,
        }
        return render(request, "farmers/mypage_create_answer.html", ctx)
    # POST : 답변 등록 완료 예정
    else:
        form = Answer_Form(request.POST)
        if form.is_valid():
            answer = Answer(
                content=form.cleaned_data.get("content"),
                question=question,
                farmer=farmer,
            )
            answer.save()
        else:
            return redirect(reverse("core:main"))
        return redirect(reverse("core:main"))  # 추후 파머스 마이페이지 리뷰/문의 관리로 이동 하도록 수정


def get_product_EP(request):
    get_product_db()
    return HttpResponse("EP 생성 완료")


def get_product_daum_EP(request):
    get_product_db_daum()
    return HttpResponse("Daum EP 생성 완료")


# @login_required
# def update_answer(request, pk):
