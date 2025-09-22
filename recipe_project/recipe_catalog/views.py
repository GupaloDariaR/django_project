from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Recipe, Favorite, Ingredient, RecipeIngredient
from .forms import UserForm, IngredientForm, RecipeForm, RecipeIngredientForm

ADMIN_LOGIN = 'admin'

# Create your views here.
def index(request):
    recipe_list = Recipe.objects.all().order_by('name')

    context = {
        'recipe_list': recipe_list,
    }
    return render(request, 'recipes_catalog.html', context)

def favorite(request):
    favorite = Favorite.objects.get(user_name='user')
    favorite_list = favorite.favorites.all().order_by('name')

    context = {
        'favorite_list': favorite_list,
    }
    return render(request, 'recipes_favorite.html', context)

def receipe_details(request, id):
    template_name = 'recipe_details.html'

    recipe = Recipe.objects.get(id = id)
    ingredients = recipe.recipeingredient_set.all().order_by('ingredient__name')

    def calc_raw_weight():
        result_raw_weight = 0
        for ingredient in ingredients:
            result_raw_weight += ingredient.raw_weight
        return result_raw_weight

    def calc_weight():
        result_weight = 0
        for ingredient in ingredients:
            result_weight += ingredient.weight
        return result_weight
    
    def calc_cost():
        result_cost = 0
        for ingredient in ingredients:
            result_cost += ingredient.cost
        return result_cost

    context = {
        'title': recipe.name,
        'id': id,
        'ingredients_list': ingredients,
        'description': recipe.description,
        'calc_raw_weight': calc_raw_weight,
        'calc_weight': calc_weight,
        'calc_cost': calc_cost,
    }
    return render(request, template_name, context)


def about(request):
    return render(request, 'about.html')

def save_to_favorite(request, id):
    recipe = Recipe.objects.get(id = id)
    favorite = Favorite.objects.get(user_name='user')
    isAdd = favorite.favorites.filter(id=id).exists()
    # modelName.objects.filter(pk='id').exists()
    favorite.favorites.add(recipe)

    context = {
        'favorite_name': recipe.name,
        'id': id,
        'isAdd': isAdd,
    }
    return render(request, 'save_to_favorite.html', context)

def form_user_test(request):
    """Тестовая форма для пользователя."""
    if request.GET:
        # создаём форму на основе параметров запроса.
        form = UserForm(request.GET)
        # Если данные валидны...
        if form.is_valid():
            # это тест - ничего в БД не заносим
            pass
    else:
        # Создаём экземпляр класса формы.
        form = UserForm()

    # Добавляем форму в словарь контекста:
    context = {'form': form}
    # создаём страницу по шаблону
    return render(request, 'user_form_test.html', context)

# Редактировать ингредиенты

@login_required
def ingredient(request):
    """Форма для ингредиентов."""
    
    if request.user.username != ADMIN_LOGIN:
        # Выдаём ошибку прав
        raise PermissionDenied
    
    form = IngredientForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        form.save()
        context = {'form': form}
    return render(request, 'ingredient_form.html', context)

@login_required
def ingredient_edit(request, pk):
    """Форма для редактирования ингредиентов."""
    
    if request.user.username != ADMIN_LOGIN:
        # Выдаём ошибку прав
        raise PermissionDenied
    
    # сначала нужно взять объект (если он есть)
    instance = get_object_or_404(Ingredient, pk=pk)
    # связываем форму с найденным объектом
    form = IngredientForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, 'ingredient_form.html', context)

@login_required
def ingredient_delete(request, pk):
    """Форма для удаления ингредиента."""

    if request.user.username != ADMIN_LOGIN:
        # Выдаём ошибку прав
        raise PermissionDenied
    
    instance = get_object_or_404(Ingredient, pk=pk)
    # В форму передаём только объект модели (форму не отображаем)
    form = IngredientForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('ingredients')
    # Если был получен GET-запрос — отображаем форму.
    return render(request, 'ingredient_form.html', context)


def ingredients(request):
    """Сформировать список ингредиентов."""
    ingredients = Ingredient.objects.all().order_by('name')
    context = {
        'ingredients_list': ingredients,
    }
    return render(request, 'ingredients.html', context)

# Редактировать рецепты

@login_required
def recipe(request):
    """Форма для рецептов."""

    if request.user.username != ADMIN_LOGIN:
        # Выдаём ошибку прав
        raise PermissionDenied

    form = RecipeForm(request.POST or None) 
    context = {'form': form}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user.username
        instance.save()
    return render(request, 'recipe_form.html', context)

@login_required
def add_recipe_ingredient(request, pk):
    """Форма для добавления ингредиентов в рецепт."""

    # проверка что пользователь авторизован 
    if request.user.username != ADMIN_LOGIN:
        # Выдаём ошибку прав
        raise PermissionDenied
    
    # проверка что пользватель является автором рецепта
    try:
        recipe = Recipe.objects.get(id=pk, author=request.user.username)
    except Recipe.DoesNotExist:
        raise Http404("Рецепт не найден или у вас нет прав редактирования.")
    
    form = RecipeIngredientForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.recipe = recipe
        instance.save()
    return render(request, 'recipe_ingredient_form.html', context)


@login_required
def recipe_edit(request, pk):
    """Форма для редактирования рецепта."""
 
    if request.user.username != ADMIN_LOGIN:
        # Выдаём ошибку прав
        raise PermissionDenied
    
    # Получаем нужный объект.
    instance = get_object_or_404(Recipe, pk=pk)
    ingredients = instance.recipeingredient_set.all().order_by('ingredient__name')

    # проверка что пользватель является автором рецепта
    if instance.author != request.user.username:
        raise PermissionDenied
    
    form = RecipeForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'ingredients': ingredients,
    }
    if form.is_valid():
        print(form.data)
        instance = form.save(commit=False)
        instance.save()
        return redirect('home')

    return render(request, 'recipe_form.html', context)

@login_required
def recipe_delete(request, pk):
    """Форма для удаления рецепта."""
    # Получаем нужный объект.
    instance = get_object_or_404(Recipe, pk=pk)

    # # проверка что пользватель является автором рецепта
    if instance.author != request.user.username:
        raise PermissionDenied
    
    instance.delete()
    return redirect('home')

@login_required
def delete_recipe_ingredient(request, pk, ingredient_id):
    """Форма для удаления ингредиента из рецепта."""
    try:
        ingredient = RecipeIngredient.objects.get(
            id=ingredient_id, 
            recipe__id=pk, 
            recipe__author=request.user.username
        )
        ingredient.delete()
    except RecipeIngredient.DoesNotExist:
        raise Http404("Ингредиент не найден или недоступен.")

    return redirect('recipe_detail', pk=pk)


@login_required
def simple_view(request):
    return HttpResponse('Добро пожаловать на сайт с рецептиками!')