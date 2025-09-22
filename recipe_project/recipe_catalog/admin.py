from django.contrib import admin

# Register your models here.

from .models import Ingredient, Recipe, RecipeIngredient, FavoriteRecipes, Favorite

class IngredientInline (admin.StackedInline) :
    """В рецепте есть ингредиенты"""
    model = RecipeIngredient
    list_display = ["raw_weight"]
    list_display = ["weight"]
    list_display = ["cost"]
    extra = 5

class RecipeAdmin (admin.ModelAdmin) :
    """Настройка формы админки для рецепта"""
    list_display = ["description"]
    list_display = ["name"]
    inlines = [IngredientInline]
admin.site.register(Recipe, RecipeAdmin)

class IngredientAdmin (admin.ModelAdmin) :
    """Настройка формы админки для рецепта"""
    list_display = ["name"]
admin.site.register(Ingredient, IngredientAdmin)

class FavoriteInline (admin.StackedInline) :
    """У пользователя есть сохраненные рецепты"""
    model = FavoriteRecipes
    extra = 1

class FavoriteAdmin (admin.ModelAdmin) :
    """Настройка формы админки для сохраненных рецептов"""
    list_display = ["user_name"]
    inlines = [FavoriteInline]
admin.site.register(Favorite, FavoriteAdmin)


    



    

    

