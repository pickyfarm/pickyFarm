from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        seeder = Seed.seeder()
        seeder.add_entity(user_models.User, 20, {"is_staff": False, "is_superuser": False})
        seeder.execute()