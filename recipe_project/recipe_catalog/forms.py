from django import forms
from .models import Ingredient, Recipe, RecipeIngredient

class UserForm(forms.Form):
    """Тестовая форма к теории."""
    first_name = forms.CharField(label='Имя',max_length=20)
    last_name = forms.CharField(label='Фамилия', required=False)
    user_email = forms.EmailField(label='Email', required=False)

class IngredientForm(forms.ModelForm):
    class Meta:
        fields = ('name',)
        labels = {
        'name': 'Название',
        }
        model = Ingredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('author',)
        fields = ('name', 'ingredients', 'description')
        labels = {
            'name': 'Название',
            'description': 'Описание',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'raw_weight', 'weight', 'cost')
        labels = {
            'ingredient': 'Название',
            'raw_weight': 'Сырой вес',
            'weight': 'Готовый вес',
            'cost': 'Цена',
        }

    def clean(self):
        cleaned_data = super().clean()
        raw_weight = cleaned_data.get('raw_weight')
        weight = cleaned_data.get('weight')
        count = cleaned_data.get('count')
        
        if raw_weight and weight and count:
            if raw_weight <= 0 or weight <= 0 or count <= 0:
                raise forms.ValidationError("Вес и количество должны быть положительными числами.")
        
        return cleaned_data