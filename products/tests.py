from django.test import TestCase
from .models import Category, Product
from farmers.models import Farmer
from users.models import User
from addresses.models import Address

# Create your tests here.


class ProductTest(TestCase):

    '''product 관련 test'''

    def setUp(self):
        user = User.objects.create(phone_number="010332345", account_name="김기윤", nickname="스토디")
        address = Address.objects.create(full_address="서울시", user = user)
        category = Category.objects.create(name="카테고리", slug="slug")
        farmer = Farmer.objects.create(farm_name="농장이름", profile_title="title", user=user, address=address)
        Product.objects.create(title="제목", sub_title="부제목", main_image="image", weight=3.0, weight_unit="kg", additional_delivery_fee_unit=3, additional_delivery_fee = 1000, farmer=farmer, category=category)

    def test_get_addtional_delivery_fee_by_unit(self):
        '''단위별 추가 배송비 계산 메소드 테스트'''

        '''quantity 변수 임의 설정하여 test 실행
        assertTrue를 통해 unit test 가능'''
        p = Product.objects.get(pk=1)
        quantity = 6
        add_fee = p.get_additional_delivery_fee_by_unit(quantity)
        self.assertEqual(add_fee, 2000)