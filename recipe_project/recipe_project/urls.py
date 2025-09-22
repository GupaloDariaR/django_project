"""
URL configuration for recipe_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from recipe_catalog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('favorite/', views.favorite, name='favorite'),
    path('recipe_details/<int:id>/', views.receipe_details, name='details'),
    path('about/', views.about, name='about'),
    path('save_to_favorite/<int:id>/', views.save_to_favorite),

    path('user_form_test/', views.form_user_test, name='create_user_test'),

    path('ingredient/', views.ingredient, name='ingredient'),
    path('ingredient/<int:pk>/edit/', views.ingredient_edit, name='ingredient_edit'),
    path('ingredient/<int:pk>/delete/',views.ingredient_delete, name='ingredient_delete'),
    path('ingredients/', views.ingredients, name='ingredients'),

    path('recipe/', views.recipe, name='recipe'),
    path('recipe/<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/<int:pk>/add/', views.add_recipe_ingredient, name='recipe_add'),
    path('recipe/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
    path('recipe/<int:pk>/delete/<int:ingredient_id>/', views.delete_recipe_ingredient, name='delete_recipe_ingredient'),

    path('auth/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('auth/logout/',auth_views.LogoutView.as_view(), name='logout'),
]
