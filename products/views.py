from django.shortcuts import render, redirect
from django.http import request
from .models import Product, Category
from django.utils import timezone
from math import ceil

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
    big_category = Category.objects.filter(slug=cat)
    categories = big_category.children.all().order_by('name')
    products = categories.filter(open=True).order_by('-create_at')

    page = request.GET.get('page', 1)
    page_size = 15
    limit = page_size * page
    offset = limit - page
    products_count = products.count()
    products = products[offset:limit]
    page_total = ceil(products_count/page_size)
    ctx = {
        "products" : products,
        "categories": categories,
        "page" : page,
        "page_total": page_total,
        "page_range": range(1, page_total),
    }
    return render(request, "products/products_list.html", ctx)

def product_detail(request):

    pass