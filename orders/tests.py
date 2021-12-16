from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve
from .views import order_cancel
from .models import Order_Detail, Order_Group

# Create your tests here.
class OrderTest(TestCase):
    def setUp(self):
        pass

    def test_order_cancel(self):
        response = self.client.get()
