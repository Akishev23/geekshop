import os
import json
from django.core.management.base import BaseCommand

from products.models import Category, Products

JSON_PATH = 'products/fixtures'


def load_from_json(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        return json.load(file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json(os.path.join(JSON_PATH, 'categories.json'))

        Category.objects.all().delete()
        for category in categories:
            cat = category.get('fields')
            cat['id'] = category.get('pk')
            new_category = Category(**cat)
            new_category.save()

        products = load_from_json(os.path.join(JSON_PATH, 'products.json'))

        Products.objects.all().delete()
        for product in products:
            prod = product.get('fields')
            category = prod.get('category')
            _category = Category.objects.get(id=category)
            prod['category'] = _category
            new_product = Products(**prod)
            new_product.save()
