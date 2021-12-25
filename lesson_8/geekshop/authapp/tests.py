from django.test import TestCase
from django.test.client import Client

from authapp.models import ShopUser
from mainapp.models import Product


class AuthUserTestCase(TestCase):
    status_ok = 200
    status_redirect = 302
    username = 'django'
    password = 'geekbrains'

    def setUp(self) -> None:
        self.client = Client()

        self.superuser = ShopUser.objects.create_superuser(
            username=self.username,
            password=self.password
        )

    def test_login(self):
        # главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_ok)

        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, 'пользователь', status_code=self.status_ok)

        # данные пользователя
        self.client.login(username=self.username, password=self.password)

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.status_code, self.status_ok)

        # главная после логина
        response = self.client.get('/')
        self.assertContains(response, 'пользователь', status_code=self.status_ok)

    # def test_redirect(self):
    #     product = Product.objects.first()
    #     response = self.client.get(f'/basket/add/{product.pk}/')
    #     self.assertEqual(response.status_code, self.status_redirect)
