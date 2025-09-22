from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from recipe_catalog.models import Recipe

User = get_user_model()

class TestCatalog(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаём пользователя.
        cls.user = User.objects.create(username='testUser')
        # Создаём объект клиента.
        cls.client_logged_in = Client()
        # Грубо "логинимся" в клиенте
        cls.client_logged_in.force_login(cls.user)

        cls.recipe = Recipe.objects.create (
            name="Яичница",
        )
    
    
    # проверка маршрута для главной страницы
    def test_home_page2(self):
        # Вместо прямого указания адреса
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # проверка маршрута для страницы с деталями рецепта
    def test_detail_page(self):
        url = reverse('detail', args=[self.recipe.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # проверка маршрута для страницы о нас
    def test_detail_page(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)