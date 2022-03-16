from django.test import TestCase, Client
from unittest import mock
from django.urls import resolve, reverse
from django.db import models
from .models import Category, Product, Product_Group
from farmers.models import Farmer
from users.models import User
from addresses.models import Address

# Create your tests here.


class ProductTest(TestCase):

    """product 관련 test"""

    def setUp(self):
        user = User.objects.create(phone_number="010332345", account_name="김기윤", nickname="스토디")
        address = Address.objects.create(full_address="서울시", user=user)
        category = Category.objects.create(name="카테고리", slug="slug")
        farmer = Farmer.objects.create(
            farm_name="농장이름", profile_title="title", user=user, address=address
        )
        Product.objects.create(
            title="제목",
            sub_title="부제목",
            main_image="image",
            weight=3.0,
            weight_unit="kg",
            additional_delivery_fee_unit=3,
            additional_delivery_fee=1000,
            farmer=farmer,
            category=category,
        )

    def test_get_addtional_delivery_fee_by_unit(self):
        """단위별 추가 배송비 계산 메소드 테스트"""

        """quantity 변수 임의 설정하여 test 실행
        assertTrue를 통해 unit test 가능"""
        p = Product.objects.get(pk=1)
        quantity = 6
        add_fee = p.get_additional_delivery_fee_by_unit(quantity)
        self.assertEqual(add_fee, 2000)


class ProductListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(phone_number="010332345", account_name="김기윤", nickname="스토디")
        address = Address.objects.create(full_address="서울시", user=user)
        farmer = Farmer.objects.create(
            farm_name="농장이름", profile_title="title", user=user, address=address
        )

        category_fruit = Category.objects.create(name="과일", slug="fruit")
        category_vege = Category.objects.create(name="채소", slug="vege")
        category_apple = Category.objects.create(name="사과", slug="apple", parent=category_fruit)
        category_potato = Category.objects.create(name="감자", slug="potato", parent=category_vege)

        product1 = Product_Group.objects.create(
            title="무난이사과그룹",
            kinds="ugly",
            category=category_apple,
            open=True,
            main_image="product_img",
        )
        product2 = Product_Group.objects.create(
            title="일반사과그룹",
            kinds="normal",
            category=category_apple,
            open=True,
            main_image="product_img",
        )
        product3 = Product_Group.objects.create(
            title="혼합사과그룹",
            kinds="mix",
            category=category_apple,
            open=True,
            main_image="product_img",
        )

        product4 = Product.objects.create(
            title="무난이사과",
            kinds="ugly",
            category=category_potato,
            open=True,
            main_image="product_img",
            weight=1.0,
            weight_unit="kg",
            product_group=product1,
            main_product=True,
            farmer=farmer,
        )
        product5 = Product.objects.create(
            title="일반사과",
            kinds="normal",
            category=category_potato,
            open=True,
            main_image="product_img",
            weight=1.0,
            weight_unit="kg",
            product_group=product2,
            main_product=True,
            farmer=farmer,
        )
        product6 = Product.objects.create(
            title="혼합사과",
            kinds="mix",
            category=category_potato,
            open=True,
            main_image="product_img",
            weight=1.0,
            weight_unit="kg",
            product_group=product3,
            main_product=True,
            farmer=farmer,
        )

    def test_product_list_url_resolves_correctly(self):
        found = resolve("/product/list/")
        self.assertEqual(found.view_name, "products:store_list")

    def test_list_all_products(self):
        res = self.client.get(reverse("products:store_list"))

        self.assertEqual(len(res.context["products"]), 3)

    def test_list_ugly_products(self):
        res = self.client.get(f'{reverse("products:store_list")}?kind=ugly')

        products = res.context["products"]
        self.assertEqual(products.first().kinds, "ugly")

    def test_list_normal_products(self):
        res = self.client.get(f'{reverse("products:store_list")}?kind=normal')

        products = res.context["products"]
        self.assertEqual(products.first().kinds, "normal")
