from django.shortcuts import render
from products.models import Product
from editor_reviews.models import Editor_Review
from users.models import Farmer
from .models import Main_Slider_Image
from datetime import date
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    
    try:
        products = Product.objects.filter(open=True)
        
    except ObjectDoesNotExist:
        pass

    if len(products) < 5:
        today_pick_list = products.order_by("create_at")[: len(products)]
        best_product_list = products.order_by("sales_rate")[:len(products)]
    
    elif len(products) < 4:
        today_pick_list = products.order_by("create_at")[:len(products)]
        best_product_list = products.order_by("sales_rate")[:len(products)]
    
    else:
        today_pick_list = products.order_by("create_at")[:5]
        best_product_list = products.order_by("sales_rate")[0:4]

    editor_pick_list = Editor_Review.objects.all()
    today_farmer_list = Farmer.objects.all()
    main_slider_image = Main_Slider_Image.objects.all()
    

    if len(today_farmer_list) < 3:
        today_farmer_list = today_farmer_list | Farmer.objects.all()[: 3 - len(today_farmer_list)]
        
    ctx = {
        'products': products,
        'today_pick_list': today_pick_list,
        'best_product_list': best_product_list,
        'editor_pick_list': editor_pick_list,
        'today_farmer_list': today_farmer_list,
        'main_slider_image': main_slider_image
    }

    return render(request, "base/index.html", ctx)


# Create your views here.
