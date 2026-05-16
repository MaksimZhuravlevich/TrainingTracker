from django.shortcuts import render

from .forms import NutritionCalculatorForm
from .logic import calculate_nutrition


def _profile_defaults(user):
    if not user.is_authenticated:
        return {}
    data = {}
    if user.user_age:
        data['user_age'] = user.user_age
    if user.user_weight:
        data['user_weight'] = user.user_weight
    if user.user_height:
        data['user_height'] = user.user_height
    if user.male:
        data['male'] = user.male
    return data


def nutrition(request):
    result = None
    profile_incomplete = False

    if request.method == 'POST':
        form = NutritionCalculatorForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            result = calculate_nutrition(
                weight_kg=cd['user_weight'],
                height_cm=cd['user_height'],
                age=cd['user_age'],
                is_male=cd['male'] == 'male',
                activity_key=cd['activity'],
                goal_key=cd['goal'],
            )
    else:
        initial = _profile_defaults(request.user)
        if request.user.is_authenticated:
            missing = {'user_age', 'user_weight', 'user_height'} - set(initial)
            profile_incomplete = bool(missing)
        form = NutritionCalculatorForm(initial=initial)

    return render(request, 'nutrition/nutrition.html', {
        'form': form,
        'result': result,
        'profile_incomplete': profile_incomplete,
    })
