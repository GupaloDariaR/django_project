from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from recipe_catalog.models import Recipe, Ingredient, RecipeIngredient
from recipe_catalog.forms import RecipeForm

User = get_user_model()

class TestRecipeCreation(TestCase):
    RECEIPT_STEPS = 'Процесс приготовления...'
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='chef', password = '12345')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)

        cls.recipe = Recipe.objects.create(name='Бутер', description='Шаги..', author = cls.user)
        cls.url = reverse('details', args=(cls.recipe.pk,))

        cls.add_recipe_url = reverse('recipe')
        cls.delete_url = reverse('recipe_delete', args=(cls.recipe.pk,))
        cls.url_to_recipes = reverse('home')
        cls.edit_url = reverse('recipe_edit', args=(cls.recipe.pk,))

        cls.COMMENT_TEXT = 'Новые шаги по приготовлению'
        cls.form_data = {'name': cls.recipe.name, 'description': cls.COMMENT_TEXT}

    def test_anonymous_user_cant_create_recipe(self):
        # Совершаем запрос от анонимного клиента
        self.client.post(self.add_recipe_url)
        # Считаем количество рецептов
        recipes_count = Recipe.objects.count()
        # Ожидаем, что рецептов в базе нет - сравниваем с нулём.
        self.assertEqual(recipes_count, 1)

    def test_author_can_delete_recipe(self):
        # От имени автора рецепта
        response = self.auth_client.delete(self.delete_url)
        # Проверяем, что редирект привёл к списку рецептов.
        self.assertRedirects(response, self.url_to_recipes)
        # Считаем количество рецептов в системе.
        recipes_count = Recipe.objects.count()
        self.assertEqual(recipes_count, 0)

    def test_author_can_edit_recipe(self):
        self.client.login(username='chef', password='12345')
        response = self.client.post(
            reverse('recipe_edit', kwargs={'pk': self.recipe.pk}),
            {'name': 'test'}
        )
        self.assertEqual(response.status_code, 302)
        # Проверяем, что поля обновлены
        self.recipe.refresh_from_db()
        name = str(Recipe.objects.filter(name='test'))
        self.assertEqual(name, 'test')