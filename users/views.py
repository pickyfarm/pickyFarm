from django.shortcuts import render
from .models import Farmer, Farm_Tag, Subscribe
from products.models import Category
from django.db.models import Count
from math import ceil

def farmers_page(request):
    page=int(request.GET.get('page', 1))
    page_size = 6
    limit = page_size * page
    offset = limit - page_size
    farmers_count = Farmer.objects.all().count()
    tags = Farm_Tag.objects.all()
    farmers = Farmer.objects.annotate(sub_counts=Count('subs')) # 구독자 수 필드 임의 추가
    best_farmers = farmers.order_by('-sub_counts')[:3]
    # farmers = Farmer.objects.all()
    # best_farmers = farmers.order_by('-sub_count')[:3]
    
    page_total = ceil(farmers_count/page_size)
    categories = Category.objects.filter(parent=None)
    # best_farmer.user.profile_image.url
    ctx = {
        'tags':tags,
        'page':page,
        'page_total':page_total,
        'page_range':range(1, page_total),
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
        'farmer':farmer,
    }
    return render(request, 'users/farmer_detail.html', ctx)