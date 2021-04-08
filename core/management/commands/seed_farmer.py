from django.core.management.base import BaseCommand
from users import models as user_models
from farmers import models as farmer_models
from faker import Faker
import random


class Command(BaseCommand):
    def handle(self, *args, **options):

        users = user_models.User.objects.order_by('?')[:5]
        faker = Faker("ko-KR")
        for user in users:
            farmer_models.Farmer.objects.create(
                user=user,
                farm_name=faker.bs(),
                farm_profile=faker.file_name(),
                farmer_profile=faker.file_name(),
                profile_title=faker.catch_phrase(),
                profile_desc=faker.paragraph(),
                sub_count=random.randint(100, 1000),
                farm_news=faker.sentence(nb_words=5),
                farm_cat=random.choice(farmer_models.Farmer.CAT_CHOICES)
            )