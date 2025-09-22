from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Ingredient (models.Model) :
    """Составная часть рецепта."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta :
        constraints = [
            models.UniqueConstraint (
                fields=['name'],
                name='unique ingredient name'
            )
        ]

class Recipe (models.Model) :
    """Вкусное делается по рецепту."""
    description = models.CharField(max_length=2000)
    name = models.CharField(max_length=300)
    author = models.CharField(max_length=300, default='admin')
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    

    def __str__(self):
        return self.name

class RecipeIngredient (models.Model) :
    """Один ингредиент может быть в нескольких рецептах, как и в одном рецепте может быть несколько ингредиентов"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    raw_weight = models.PositiveSmallIntegerField(default=0)
    weight = models.PositiveSmallIntegerField(default=0)
    cost = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.ingredient.name}'
    
    class Meta :
        constraints = [
            models.UniqueConstraint (
                fields=['recipe', 'ingredient'],
                name='unique recipes ingredients'
            )
        ]

class Favorite (models.Model) :
    """Сохраненные рецепты пользователя"""
    user_name = models.CharField(max_length=30, default='user')
    favorites = models.ManyToManyField(Recipe, through="FavoriteRecipes")

    def __str__(self):
        return self.user_name
    
    class Meta :
        constraints = [
            models.UniqueConstraint (
                fields=['user_name'],
                name='unique user name'
            )
        ]

class FavoriteRecipes (models.Model) :
    """Один рецепт может быть сохранен несколькими пользователями, как и один пользователь может сохранять несколько рецептов"""
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.recipe.name
    
    class Meta :
        constraints = [
            models.UniqueConstraint (
                fields=['favorite', 'recipe'],
                name='unique favorites recipes'
            )
        ]