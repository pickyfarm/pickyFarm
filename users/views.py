from django.shortcuts import render
from .models import Farmer, Farm_Tag, Farm_Image, Subscribe
from django.db.models import Count

def farmers_page(request):
    farmers = Farmer.objects.annotate(sub_counts=Count('subs')) # 구독자 수 필드 임의 추가
    best_farmers = farmers.order_by('-sub_counts')[:3]
    
    ctx = {
        'farmers': farmers,
        'best_farmers': best_farmers,
    }
    return render(request, 'users/farmers_page.html', ctx)


def farmer_detail(request, pk):
    farmer = Farmer.objects.get(pk=pk)
    ctx = {
        'farmer':farmer,
    }
    return render(request, 'users/farmer_detail.html', ctx)