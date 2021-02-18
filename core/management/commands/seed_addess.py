from django.core.management.base import BaseCommand
import core.management.commands.seed_base as base


class Commnad(BaseCommand):
    def handle(self, *args, **options):
        base.seed_address()