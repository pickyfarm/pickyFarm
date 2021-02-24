from django.core.management.base import BaseCommand
from django_seed import Seed
from faker import Faker
from users import models as user_models
from addresses import models as address_models
from products import models as product_models
from editor_reviews import models as review_models
from comments import models as comment_models
import random
import os, sys

class Command(BaseCommand):
    def handle(self, *args, **options):
        os.system("python manage.py seed_user")
        self.stdout.write(self.style.SUCCESS("Completely Seed 20 Users!"))
        os.system("python manage.py seed_farmer")
        self.stdout.write(self.style.SUCCESS("Completely Seed 5 Farmers!"))
        os.system("python manage.py seed_editors")
        self.stdout.write(self.style.SUCCESS("Completely Seed 5 Editors!"))
        os.system("python manage.py seed_address")
        self.stdout.write(self.style.SUCCESS("Completely Seed 5 Addresses!"))
        os.system("python manage.py seed_product")
        self.stdout.write(self.style.SUCCESS("Completely Seed 20 Products!"))
        os.system("python manage.py seed_editor_review")
        self.stdout.write(self.style.SUCCESS("Completely Seed 5 Editor Reviews!"))
        os.system("python manage.py seed_comment")
        self.stdout.write(self.style.SUCCESS("Completely Seed 10 Comments!"))
        os.system("python manage.py seed_recomment")
        self.stdout.write(self.style.SUCCESS("Completely Seed 10 Recomments!"))
        

def seed_user():
    seeder = Seed.seeder("ko_KR")
    seeder.add_entity(user_models.User, 20, {"is_staff": False, "is_superuser": False})
    seeder.execute()
    


def seed_farmer():
    seeder1 = Seed.seeder()
    seeder1.add_entity(user_models.Farmer, 5, {
        "sub_count": lambda x: random.randint(100, 1000),
        "farm_name": lambda x: seeder1.faker.bs(),
        "profile_title": lambda x: seeder1.faker.catch_phrase(),
        "farm_news": lambda x:seeder1.faker.sentence(nb_words=5)
    })
    seeder1.execute()

def seed_editor():
    seeder = Seed.seeder()
    seeder.add_entity(user_models.Editor, 5)
    seeder.execute()

def seed_address():
    seeder = Seed.seeder(locale="ko_KR")
    faker = Faker(locale="ko_KR")
    seeder.add_entity(address_models.Address, 20, {
        "full_address": lambda x: faker.road_address(),
        "sido": lambda x: faker.province(),
        "sigungu": lambda x: faker.city(),
        "user": lambda x: random.choice(user_models.User.objects.all())
    })

    seeder.execute()

def seed_product():
    seeder = Seed.seeder()
    seeder.add_entity(product_models.Product, 20, {
        "title": lambda x: seeder.faker.sentence(nb_words=2),
        "sub_title": lambda x: seeder.faker.sentence(nb_words=3),
        "open": True,
        "sell_price": lambda x: random.randint(1000, 50000),
        "sales_count": lambda x: random.randint(10, 100),
        "weight": lambda x: random.uniform(0.5, 5.0),
        "stock": lambda x: random.randint(1, 100),
        "farmer": lambda x: random.choice(user_models.Farmer.objects.all()),
        "category":lambda x:random.choice(product_models.Category.objects.exclude(parent__isnull=True))
    })
    seeder.execute()

def seed_editor_review():
    seeder = Seed.seeder()
    seeder.add_entity(review_models.Editor_Review, 5, {
        "title": lambda x: seeder.faker.sentence(nb_words=10),
        "sub_title": lambda x: seeder.faker.sentence(nb_words=5),
        "contents": lambda x: seeder.faker.paragraph(nb_sentences=50),
        "farm": lambda x: random.choice(user_models.Farmer.objects.all()),
        "author": lambda x: random.choice(user_models.Editor.objects.all())
    })
    seeder.execute()

    reviews = review_models.Editor_Review.objects.all()
    
    for review in reviews:
        review.product.set(product_models.Product.objects.order_by('?')[:3])

def seed_comment():
    seeder = Seed.seeder()
    
    seeder.add_entity(comment_models.Editor_Review_Comment, 10, {
        "text": lambda x: seeder.faker.sentence(nb_words=10),
        "editor_review": lambda x: random.choice(review_models.Editor_Review.objects.all()),
        "author": lambda x: random.choice(user_models.User.objects.all())
    })
    seeder.execute()


def seed_recomment():
    seeder2 = Seed.seeder()
    seeder2.add_entity(comment_models.Editor_Review_Recomment, 10, {
        "text": lambda x: seeder2.faker.sentence(nb_words=4),
        "comment": lambda x: random.choice(comment_models.Editor_Review_Comment.objects.all()),
        "author": lambda x: random.choice(user_models.User.objects.all())
    })
    seeder2.execute()