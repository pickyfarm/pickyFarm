from django.shortcuts import render
from products.models import Product
from editor_reviews.models import Editor_Reviews
from .models import Main_Slider_Image
from datetime import date


def index(request):
    products = Product.objects.filter(open=True)

    today_pick_list = products.order_by("create_at")

    if len(products) < 4:
        best_product_list = products.order_by("sales_rate")[:len(products)]
    
    else:
        best_product_list = products.order_by("sale_rate")
    editor_pick_list = Editor_Reviews.objects.all()
    today_farmer_list = Product.objects.filter(create_at__date=date.today())
    main_slider_image = Main_Slider_Image.objects.all()
    

    if len(today_farmer_list) < 3:
        today_farmer_list = today_farmer_list | Product.objects.exclude(create_at__date=date.today())[: 3 - len(today_farmer_list)]
        
    ctx = {
        'today_pick_list': today_pick_list,
        'best_product_list': best_product_list,
        'editor_pick_list': editor_pick_list,
        'today_farmer_list': today_farmer_list,
        'main_slider_image': main_slider_image
    }

    return render(request, "base/index.html", )


# Create your views here.
