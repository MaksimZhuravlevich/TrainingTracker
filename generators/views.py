from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from datetime import date

from programs.models import TrainingProgram, ProgramWorkout, ProgramExercise
from analytics.models import ExerciseMax, WorkoutLog, ExerciseLog
from exercises.models import Exercise
from .forms import UserPhysicalDataForm, ExerciseMaxForm
from .logic import select_program, calculate_working_weight, generate_workout_log


@login_required
def choose_sport(request):
    sport_types = TrainingProgram.SPORT_TYPES

    if request.method == 'POST':
        sport = request.POST.get('sport_type')
        print(f"Выбран спорт: {sport}")  # ← отладка
        if sport:
            request.session['selected_sport'] = sport
            print(f"Сессия после сохранения: {request.session.items()}")  # ← отладка
            return redirect('/generators/fill-data/')
        else:
            messages.error(request, 'Пожалуйста, выберите вид спорта')

    return render(request, 'generators/choose_sport.html', {
        'sport_types': sport_types
    })


@login_required
def fill_data(request):
    print("=== fill_data START ===")
    user = request.user
    sport = request.session.get('selected_sport')
    print(f"Спорт из сессии: {sport}")

    if not sport:
        messages.warning(request, 'Сначала выберите вид спорта')
        return redirect('/generators/choose-sport/')  # ← абсолютный путь

    programs = TrainingProgram.objects.filter(
        sport_type=sport,
        user__isnull=True
    )

    if not programs.exists():
        messages.error(request, f'Нет программ для вида спорта "{sport}"')
        return redirect('/generators/choose-sport/')  # ← абсолютный путь

    exercise_ids = ProgramExercise.objects.filter(
        workout__program__in=programs
    ).values_list('exercise_id', flat=True).distinct()

    exercises = Exercise.objects.filter(id__in=exercise_ids)

    if exercises.count() == 0:
        exercises = Exercise.objects.all()[:10]

    has_maxes = ExerciseMax.objects.filter(user=user).exists()
    show_maxes_form = 'edit_maxes' in request.POST or not has_maxes

    if request.method == 'POST':
        phys_form = UserPhysicalDataForm(request.POST, instance=user)
        max_form = ExerciseMaxForm(request.POST, exercises=exercises)

        if 'keep_maxes' in request.POST:
            pass
        elif phys_form.is_valid() and max_form.is_valid():
            phys_form.save()

            for exercise in exercises:
                weight = max_form.cleaned_data.get(f'max_{exercise.id}')
                reps = max_form.cleaned_data.get(f'reps_{exercise.id}')
                if weight and reps:
                    ExerciseMax.objects.update_or_create(
                        user=user,
                        exercise=exercise,
                        defaults={'max_weight': weight, 'reps': reps}
                    )
        else:
            if not phys_form.is_valid():
                messages.error(request, 'Проверьте физические данные')
            if not max_form.is_valid():
                messages.error(request, 'Проверьте введённые веса')
            return render(request, 'generators/fill_data.html', {
                'phys_form': phys_form,
                'max_form': max_form,
                'sport': sport,
                'has_maxes': has_maxes,
                'show_maxes_form': show_maxes_form,
                'exercises_with_maxes': ExerciseMax.objects.filter(user=user).select_related('exercise'),
            })

        program = select_program(sport, 'beginner')
        if not program:
            messages.error(request, 'Не найдена подходящая программа')
            return redirect('/generators/choose-sport/')  # ← абсолютный путь

        day = request.session.get(f'workout_day_{program.id}', 1)
        workout_template = ProgramWorkout.objects.filter(
            program=program,
            day_number=day
        ).first()

        if not workout_template:
            messages.error(request, 'В программе нет тренировок')
            return redirect('/generators/choose-sport/')  # ← абсолютный путь

        workout_log = generate_workout_log(user, program, workout_template)

        next_day = day + 1
        has_next = ProgramWorkout.objects.filter(
            program=program,
            day_number=next_day
        ).exists()
        request.session[f'workout_day_{program.id}'] = next_day if has_next else 1

        messages.success(request, 'Тренировка сгенерирована!')
        return redirect(f'/generators/workout/{workout_log.id}/')  # ← абсолютный путь

    else:
        phys_form = UserPhysicalDataForm(instance=user)

        initial_data = {}
        for exercise in exercises:
            max_obj = ExerciseMax.objects.filter(user=user, exercise=exercise).first()
            if max_obj:
                initial_data[f'max_{exercise.id}'] = max_obj.max_weight
                initial_data[f'reps_{exercise.id}'] = max_obj.reps

        max_form = ExerciseMaxForm(initial=initial_data, exercises=exercises)

    return render(request, 'generators/fill_data.html', {
        'phys_form': phys_form,
        'max_form': max_form,
        'sport': sport,
        'exercises_count': exercises.count(),
        'has_maxes': has_maxes,
        'show_maxes_form': show_maxes_form,
        'exercises_with_maxes': ExerciseMax.objects.filter(user=user).select_related('exercise'),
    })


@login_required
def workout_detail(request, workout_log_id):
    workout_log = get_object_or_404(
        WorkoutLog.objects.select_related('workout', 'program'),
        id=workout_log_id,
        user=request.user
    )

    exercises = workout_log.exerciselog_set.all().order_by('order')

    return render(request, 'generators/workout_detail.html', {
        'workout_log': workout_log,
        'exercises': exercises,
    })


@login_required
def workout_history(request):
    workouts = WorkoutLog.objects.filter(
        user=request.user
    ).select_related('program', 'workout').order_by('-date')

    return render(request, 'generators/workout_history.html', {
        'workouts': workouts
    })


@login_required
def regenerate_workout(request, workout_log_id):
    workout_log = get_object_or_404(
        WorkoutLog,
        id=workout_log_id,
        user=request.user
    )

    workout_log.exerciselog_set.all().delete()

    program_exercises = ProgramExercise.objects.filter(
        workout=workout_log.workout
    ).order_by('order')

    for prog_ex in program_exercises:
        if not prog_ex.exercise:
            continue

        weight = calculate_working_weight(request.user, prog_ex.exercise, prog_ex)

        ExerciseLog.objects.create(
            workout_log=workout_log,
            exercise=prog_ex.exercise,
            weight=weight,
            reps=prog_ex.reps,
            sets=prog_ex.sets,
            order=prog_ex.order,
            notes='Обновлено'
        )

    messages.success(request, 'Тренировка обновлена с учётом новых данных!')
    return redirect(f'/generators/workout/{workout_log.id}/')  # ← абсолютный путь


@login_required
def delete_workout(request, workout_log_id):
    workout_log = get_object_or_404(
        WorkoutLog,
        id=workout_log_id,
        user=request.user
    )

    if request.method == 'POST':
        workout_log.delete()
        messages.success(request, 'Тренировка удалена')
        return redirect('/generators/history/')  # ← абсолютный путь

    return render(request, 'generators/confirm_delete.html', {'workout_log': workout_log})

@login_required
def workout_history(request):
    workouts=WorkoutLog.objects.filter(user=request.user).order_by('date')
    return render(request,'generators/workout_history.html',{'workouts':workouts})










