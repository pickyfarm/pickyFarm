from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from .models import Address
from django.http import JsonResponse
from .zipcode import ZIPCODE_LIST
from bisect import bisect_left

# Create your views here.


class deleteError(Exception):
    pass


@login_required
@require_POST
def delete(request):
    if request.method == "POST":
        pk = int(request.POST.get("pk"))
        try:
            address = Address.objects.get(pk=pk)
        except ObjectDoesNotExist:
            success = False
            data = {
                "success": success,
            }
            return JsonResponse(data)

    try:
        address.delete()
    except deleteError:
        success = False
        data = {
            "success": success,
        }
        return JsonResponse(data)

    success = True
    data = {
        "success": success,
    }
    return JsonResponse(data)


def check_address_by_zipcode(zipcode):
    idx = bisect_left(ZIPCODE_LIST, zipcode)

    return True if ZIPCODE_LIST[idx] == zipcode else False
