from django.core.management.base import BaseCommand
import core.management.commands.seed as base


class Command(BaseCommand):
    def handle(self, *args, **options):
        base.seed_product()