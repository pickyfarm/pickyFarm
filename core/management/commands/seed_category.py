from django.core.management.base import BaseCommand
from products.models import Category

class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.objects.create(name='과일', slug='fruit', parent=None)
        Category.objects.create(name='야채', slug='vege', parent=None)
        Category.objects.create(name='기타', slug='etc', parent=None)
        Category.objects.create(name='사과', slug='apple', parent=Category.objects.get(name='과일'))
        Category.objects.create(name='포도', slug='grape', parent=Category.objects.get(name='과일'))
        Category.objects.create(name='딸기', slug='strawberry', parent=Category.objects.get(name='과일'))
        Category.objects.create(name='양파', slug='onion', parent=Category.objects.get(name='야채'))
        Category.objects.create(name='당근', slug='carrot', parent=Category.objects.get(name='야채'))
        Category.objects.create(name='감자', slug='potato', parent=Category.objects.get(name='야채'))
        Category.objects.create(name='버섯', slug='mushroom', parent=Category.objects.get(name='기타'))
        