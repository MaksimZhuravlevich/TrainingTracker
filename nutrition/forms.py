from django import forms

from .logic import ACTIVITY_FACTORS, GOAL_ADJUSTMENTS


class NutritionCalculatorForm(forms.Form):
    user_age = forms.IntegerField(
        label='Возраст (лет)',
        min_value=14,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    user_weight = forms.IntegerField(
        label='Вес (кг)',
        min_value=30,
        max_value=200,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    user_height = forms.IntegerField(
        label='Рост (см)',
        min_value=140,
        max_value=220,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    male = forms.ChoiceField(
        label='Пол',
        choices=[('male', 'Мужчина'), ('female', 'Женщина')],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    activity = forms.ChoiceField(
        label='Уровень активности',
        choices=[(k, v[1]) for k, v in ACTIVITY_FACTORS.items()],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    goal = forms.ChoiceField(
        label='Цель',
        choices=[(k, v[1]) for k, v in GOAL_ADJUSTMENTS.items()],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
