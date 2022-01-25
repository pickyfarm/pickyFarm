from django.shortcuts import render
from products.models import Product
from editor_reviews.models import Editor_Review
from farmers.models import Farmer
from .models import Main_Slider_Image
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.db.models import Q
from django.http import HttpResponse
import mimetypes
import urllib


# def index(request):
#     """siminwon landing"""
#     try:
#         siminwon = Farmer.objects.get(farm_name="시민원")
#     except ObjectDoesNotExist:
#         siminwon = None

#     # try:
#     #     products = Product.objects.filter(open=True)

#     # except ObjectDoesNotExist:
#     #     pass

#     # if len(products) < 5:
#     #     today_pick_list = products.order_by("create_at")[: len(products)]
#     #     best_product_list = products.order_by("sales_rate")[: len(products)]

#     # elif len(products) < 4:
#     #     today_pick_list = products.order_by("create_at")[: len(products)]
#     #     best_product_list = products.order_by("sales_rate")[: len(products)]

#     # else:
#     #     today_pick_list = products.order_by("create_at")[:5]
#     #     best_product_list = products.order_by("sales_rate")[0:4]

#     # try:
#     #     editor_pick_list = Editor_Review.objects.all()

#     # except Editor_Review.DoesNotExist:
#     #     pass

#     # today_farmer_list = Farmer.objects.all()
#     main_slider_image = Main_Slider_Image.objects.all()

#     # if len(today_farmer_list) < 3:
#     #     today_farmer_list = (
#     #         today_farmer_list | Farmer.objects.all()[: 3 - len(today_farmer_list)]
#     #     )

#     ctx = {
#         # "products": products,
#         # "today_pick_list": today_pick_list,
#         # "best_product_list": best_product_list,
#         # "editor_pick_list": editor_pick_list,
#         # "today_farmer_list": today_farmer_list,
#         "main_slider_image": main_slider_image,
#         "siminwon": siminwon,
#     }

#     return render(request, "base/landing/siminwon/siminwon_landing_page.html", ctx)


def index(request):
    farmers = Farmer.objects.filter(open=True)

    available_products = Product.objects.filter(status='sale', open=True)
    hot_crops = available_products.order_by('?')[:3]
    todays_crops = available_products.order_by('?')[:5]
    slider_images = Main_Slider_Image.objects.all()

    # print(f'-=-=---=--=-={farmers.get(farm_name="시민원")}')

    ctx = {
        "farmers": farmers,
        "main_slider_image": slider_images,
        "hot_crops": hot_crops,
        "todays_crops": todays_crops,
        "siminwon": farmers.get(farm_name="시민원"),
    }

    return render(request, "base/index_new/index_new.html", ctx)


def disclaimer(request):
    return render(request, "base/disclaimer.html")


def personal_info_usage(request):
    return render(request, "users/signup/personal_info_popup.html")


class PopupCallback(TemplateView):
    template_name = "base/popup_callback.html"


class CompletedAlert(TemplateView):
    template_name = "base/completed_alert.html"


def download_file(request, filepath):
    # fill these variables with real values

    fl_path = urllib.parse.unquote(filepath)
    filename = fl_path

    fl = open(fl_path, "rb")
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response
