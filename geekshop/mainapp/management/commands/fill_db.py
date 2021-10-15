from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product, StyleCategory
from authapp.models import ShopUser

import json, os

JSON_PATH = 'mainapp/jsons'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), mode='r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):

        categories = load_from_json('products_category')
        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()


        style_categories = load_from_json('style_category')
        StyleCategory.objects.all().delete()
        for category in style_categories:
            new_category = StyleCategory(**category)
            new_category.save()


        products = load_from_json('products')
        Product.objects.all().delete()
        for product in products:
            style_category_name = product["style_category"]
            _style_category = StyleCategory.objects.get(name=style_category_name)
            product['style_category'] = _style_category

            category_name = product["category"]
            _category = ProductCategory.objects.get(name=category_name)
            product['category'] = _category

            new_product = Product(**product)
            new_product.save()

        super_user = ShopUser.objects.create_superuser(
            'django',
            'django@geekshop.local',
            '123',
            age=20
        )
