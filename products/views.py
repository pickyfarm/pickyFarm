from django.shortcuts import render, redirect
from django.http import request
from .models import Product, Category
from django.utils import timezone
from math import ceil
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def store_list_all(request):
    page = int(request.GET.get('page', 1))
    page_size = 15
    limit = page_size * page
    offset = limit - page_size
    products_count = Product.objects.filter(open=True).count()
    products = Product.objects.filter(
        open=True).order_by('-create_at')[offset:limit]
    categories = Category.objects.filter(parent=None).order_by('name')
    page_total = ceil(products_count/page_size)
    ctx = {
        "products": products,
        "categories": categories,
        "page": page,
        "page_total": page_total,
        "page_range": range(1, page_total),

    }
    return render(request, "products/products_list.html", ctx)


def store_list_cat(request, cat):
    big_cat = ['fruit', 'vege', 'others']
    products = []
    page = int(request.GET.get('page', 1))
    sort = request.GET.get('sort', '최신순')
    page_size = 15
    limit = page_size * page
    offset = limit - page_size
    if str(cat) in big_cat:
        big_category = Category.objects.get(slug=cat)
        print(big_category)
        categories = big_category.children.all().order_by('name')
        try:
            products = Product.objects.filter(
                category__parent__slug=cat, open=True).order_by('create_at')
        except ObjectDoesNotExist:
            ctx = {
                'big_category': big_category,
            }
            return render(request, "products/products_list.html", ctx)
    else:
        categories = Category.objects.get(slug=cat)
        try:
            products = categories.products.filter(open=True).order_by('-create_at')
            categories = categories.parent.children.all().order_by('name')
        except ObjectDoesNotExist:
            ctx = {
                "cateogries" : categories,
            }
            return render(request, "products/products_list.html", ctx)
        
    print(categories)
    print(products)
    if sort == '인기순':
        for product in products:
            product.calculate_sale_rate()
        products = products.order_by('sales_rate')
    elif sort == "마감임박순":
        products = products.order_by('-stock')
    print(products)
    print(page)
    products_count = products.count()
    products = products[offset:limit]
    if products_count == 0:
        page_total = 1
    else:
        page_total = ceil(products_count/page_size)

    ctx = {
        "products": products,
        "categories": categories,
        "page": page,
        "page_total": page_total,
        "page_range": range(1, page_total),
    }
    return render(request, "products/products_list.html", ctx)


def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product.calculate_total_rating_avg()
        farmer = product.farmer
        print(farmer)
        comments = product.product_comments.all()
        questions = product.questions.all()
        
        print(comments)
        print(questions)
        print(product.calculate_specific_rating())
        ctx = {
            'product': product,
            'farmer': farmer,
            'comments': comments,
            'questions': questions,
        }
        return render(request, "products/product_detail.html", ctx)
    except ObjectDoesNotExist:
        return redirect("/")
