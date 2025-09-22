from django.test import TestCase
from recipe_catalog.models import Ingredient, Recipe, RecipeIngredient
from django.urls import reverse

class TestOneDB (TestCase):
    INGREDIENT_NAME = 'Ананасы'
    INGREDIENT_NAME_2 = 'Сыр моцарелла'
    RECIPE_NAME = 'Гавайская пицца'
    RECIPE_NAME_2= 'Данго'

    @classmethod
    def setUpTestData(cls):
        cls.ingredient_1 = Ingredient.objects.create (
            name=cls.INGREDIENT_NAME,
        )
        cls.ingredient_2 = Ingredient.objects.create (
            name=cls.INGREDIENT_NAME_2,
        )

        cls.recipe = Recipe.objects.create (
            name=cls.RECIPE_NAME,
        )
        cls.recipe_2 = Recipe.objects.create (
            name=cls.RECIPE_NAME_2,
        )

        cls.recipe.ingredients.set([cls.ingredient_2, cls.ingredient_1])
    
    # проверка что Ингредиент создан
    def test_successful_creation_ingredient(self):
        ingredients_count = Ingredient.objects.count()
        self.assertEqual(ingredients_count, 2)
    
    # проверка что Рецепт создан 
    def test_successful_creation_recipe(self):
        recipe_count = Recipe.objects.count()
        self.assertEqual(recipe_count, 2)

    # проверка что связь между Resipe и Ingredient существует
    def test_successful_create_recipe_ingredient(self):
        counts = [
            (self.recipe.ingredients.count(), 2, "Рецепт"),
            (RecipeIngredient.objects.count(), 2, "Ингредиент-Рецепт"),
        ]
        for cnt in counts:
            with self.subTest(msg='Рецепты-ингредиенты'):
                self.assertEqual(cnt[0], cnt[1], cnt[2])
    
    # проверка на корректное создание атрибутов объектов
    def test_titles(self):
        titles = [
            (self.ingredient_1.name, self.INGREDIENT_NAME, 'Ингредиент'),
            (self.recipe.name, self.RECIPE_NAME, 'Рецепт'),
        ]
        for name in titles:
            with self.subTest(msg=f'Название {name[2]}'):
                self.assertEqual(name[0], name[1])

    # вывод списка рецептов - в порядке алфавита
    def test_catalog_page_ordering(self):
        response = self.client.get(reverse('home'))
        recipes = response.context['recipe_list']
        self.assertEqual(str(recipes), str(Recipe.objects.all().order_by('name')))

    # # вывод списка ингредиентов - в порядке алфавита
    def test_catalog_page_ordering(self):
        response = self.client.get(reverse('details', args=[self.recipe.pk]))
        ingredients = response.context['ingredients_list']
        ingredient_names = [ingredient.ingredient.name for ingredient in ingredients]
        self.assertEqual(ingredient_names, sorted(ingredient_names))
    