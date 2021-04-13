from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import DetailView
from django.views import View
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.db.models import Q


# models
from .models import *
from products.models import Product
from users.models import Consumer

# forms
from .forms import *
from comments.forms import FarmerStoryCommentForm, FarmerStoryRecommentForm
from users.forms import SignUpForm
from addresses.forms import AddressForm


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
    template_name = "users/farmer_story_detail.html"
    context_object_name = "main_story"

    def get_context_data(self, **kwargs):
        ctx = super(DetailView, self).get_context_data(**kwargs)
        farmer = self.get_object().farmer
        story = Farmer_Story.objects.all().order_by("-id")

        paginator = Paginator(story, 3)
        page = self.request.GET.get("page")
        stories = paginator.get_page(page)

        comments = self.get_object().farmer_story_comments.order_by("-id")
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

    ctx = {
        "farmer": farmer,
        "tags": tags,
        "products": products,
        "stories": stories,
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
        print("get")
        form = FarmApplyForm()
        ctx = {
            "form": form,
        }
        return render(request, "farmers/farm_apply.html", ctx)


# 입점 등록 page
class FarmEnroll(View):
    def get(self, request, step):
        if step == "step_1":
            form = SignUpForm()
            addressform = AddressForm()
            ctx = {
                "form": form,
                "addressform": addressform,
            }
            return render(request, "farmers/farm_enroll_1.html", ctx)
        elif step == "step_2":
            farm_form = FarmEnrollForm()
            ctx = {
                "farm_form": farm_form,
            }
            return render(request, "farmers/farm_enroll_2.html", ctx)
        elif step == "step_3":
            return render(request, "farmers/farm_enroll_3.html")
        return redirect(reverse("core:main"))

    def post(self, request, step):
        print("----------farm enroll post-----------")
        form = SignUpForm(request.POST)
        addressform = AddressForm(request.POST)
        farmer_form = FarmEnrollForm(request.POST)

        # farm enroll step 1
        if form.is_valid():
            print("farm enroll 1 form valid")
            form.save(commit=False)
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # user = authenticate(request, username=username, password=password)
            # Consumer.objects.create(user=user, grade=1)

            address = addressform.save(commit=False)
            # address.user = user
            # address.is_default = True
            # address.save()
            return render(request, "farmers/farm_enroll_2.html")

        # farm enroll step 2
        if farmer_form.is_valid():
            print("farm enroll 2 form valid")
            farmer_form.save(commit=False)
            return render(request, "farmers/farm_enroll_3.html")

        # farm enroll step 3

        if user is not None:
            form.save()
            address.save()
            farmer_form.save()
            Consumer.objects.create(user=user, grade=1)
            login(request, user=user)
            return redirect(reverse("core:main"))

        ctx = {
            "form": form,
            "addressform": addressform,
        }
        return redirect(reverse("core:main"))
