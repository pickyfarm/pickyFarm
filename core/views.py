from django.shortcuts import render


def index(request):
    return render(request, "base/base.html")
# Create your views here.
