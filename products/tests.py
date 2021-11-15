from django.test import TestCase
from django.test.client import Client

# Create your tests here.
from products.models import Category, Products


class TestMainSmokeTest(TestCase):
    status_code_success = 200

    def setUp(self) -> None:
        category = Category.objects.create(name='Test_cat')
        Products.objects.create(category=category, name='product_test', price=100)
        Products.objects.create(category=category, name='product_test_1', price=50)
        Products.objects.create(category=category, name='product_test_4', price=30)

        self.client = Client()

    def test_products_pages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)

    def test_products_product(self):
        for product_item in Products.objects.all():
            response = self.client.get(f'/products/detail/{product_item.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)

    def test_products_basket(self):
        response = self.client.get('/users/profile/')
        self.assertEqual(response.status_code, 302)

    def tearDown(self) -> None:
        pass
