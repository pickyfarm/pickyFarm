from django.test import TestCase
import json
from django.http import HttpRequest
from django.urls import resolve
from users.models import User, Consumer
from farmers.models import Farmer 
from addresses.models import Address
from products.models import Product, Category
from .views import order_cancel
from .models import Order_Detail, Order_Group

# Create your tests here.
class OrderTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="기윤", phone_number="01033688026", account_name="김기윤", nickname="스토디")
        Consumer.objects.create(user=user)
        address = Address.objects.create(full_address="서울시 서울시", user=user)
        farmer_user = User.objects.create(username="농사꾼", phone_number="01011111111", account_name = "이농장", nickname="농장농장")
        
        farmer = Farmer.objects.create(farm_name="농장", user=farmer_user, address=address)
        category = Category.objects.create(name="사과", slug="apple")
        Product.objects.create(title="상품상품", sub_title="상품서브", main_image="default", category=category, weight=3.0, stock=10, farmer=farmer)

    def test_payment_create_non_user(self):
        '''[GET] 비회원 결제하기창'''
        json_dict = {"orders":[{"pk" : "1","quantity" : "3"}]}
        json_data = json.dumps(json_dict)
        response = self.client.post('/order/payment/', json_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response, 'orders/payment_non_user.html')
        self.assertTrue(response.ctx["account_name"] == "")
        self.assertTrue(response.ctx["phone_number"] == "")
        self.assertTrue(response.ctx["phone_number"] == "")
        self.assertTrue(response.ctx["addressess"] == "")



