"""Расчёт калорий и макронутриентов (Mifflin–St Jeor)."""

ACTIVITY_FACTORS = {
    'sedentary': (1.2, 'Сидячий образ жизни'),
    'light': (1.375, 'Лёгкая активность (1–3 трен./нед.)'),
    'moderate': (1.55, 'Умеренная (3–5 трен./нед.)'),
    'active': (1.725, 'Высокая (6–7 трен./нед.)'),
    'very_active': (1.9, 'Очень высокая (2 трен./день)'),
}

GOAL_ADJUSTMENTS = {
    'lose': (-500, 'Похудение (−0.5 кг/нед.)'),
    'maintain': (0, 'Поддержание веса'),
    'gain': (500, 'Набор массы (+0.5 кг/нед.)'),
}


def bmr(weight_kg, height_cm, age, is_male):
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    return base + 5 if is_male else base - 161


def calculate_nutrition(weight_kg, height_cm, age, is_male, activity_key, goal_key):
    activity_factor, activity_label = ACTIVITY_FACTORS[activity_key]
    goal_delta, goal_label = GOAL_ADJUSTMENTS[goal_key]

    bmr_value = round(bmr(weight_kg, height_cm, age, is_male))
    tdee = round(bmr_value * activity_factor)
    target_calories = max(1200, tdee + goal_delta)

    protein_g = round(weight_kg * 1.8)
    fat_g = round(target_calories * 0.25 / 9)
    carbs_g = round((target_calories - protein_g * 4 - fat_g * 9) / 4)

    return {
        'bmr': bmr_value,
        'tdee': tdee,
        'calories': target_calories,
        'protein_g': protein_g,
        'fat_g': fat_g,
        'carbs_g': max(carbs_g, 0),
        'activity_label': activity_label,
        'goal_label': goal_label,
    }
