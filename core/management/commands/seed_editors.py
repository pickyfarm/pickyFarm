from django.core.management.base import BaseCommand
from users import models as user_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = user_models.User.objects.filter(editor__isnull=True)[:5]
        for user in users:
            user_models.Editor.objects.create(user=user)
