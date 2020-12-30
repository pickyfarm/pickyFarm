from django.shortcuts import render
from .models import Farmer, Farm_Tag, Farm_Image, Subscribe

def farmers_page(request):
    farmers = Farmer.objects.all()

    ctx = {
        'farmers':farmers,

    }
    return render(request, 'users/farmers_page.html', ctx)



def farmer_detail(request, pk):
    farmer = Farmer.objects.get(pk=pk)
    ctx = {
        'farmer':farmer,
    }
    return(request, 'users/farmer_detail.html', ctx)