from django.test import TestCase
from users.models import User, Consumer
from addresses.models import Address
from .models import AddressMatchException

# Create your tests here.
class Adresstest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username="기윤", phone_number="01033688026", account_name="김기윤", nickname="스토디"
        )
        user2 = User.objects.create(
            username="인지", phone_number="01026080265", account_name="최인지", nickname="쳉지"
        )
        Consumer.objects.create(user=user)
        Consumer.objects.create(user=user2)
        Address.objects.create(full_address="서울시 서울시", user=user2)

    def test_set_default_address_other_user(self):
        """[POST] 마이페이지 기본 배송지 변경"""
        user = User.objects.get(username="기윤")
        address = Address.objects.get(user__username="인지")

        with self.assertRaises(AddressMatchException) as e:
            user.consumer.set_default_address(address.pk)
        print(e.exception)
        self.assertEqual(str(e.exception), "Address does not match")
