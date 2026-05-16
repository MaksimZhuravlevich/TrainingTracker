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

VALID_SPORT_KEYS = {key for key, _ in TrainingProgram.SPORT_TYPES}


@login_required
def choose_sport(request):
    sport_types = TrainingProgram.SPORT_TYPES

    if request.method == 'GET':
        sport = request.GET.get('sport')
        if sport in VALID_SPORT_KEYS:
            request.session['selected_sport'] = sport
            return redirect('generators:fill_data')

    if request.method == 'POST':
        sport = request.POST.get('sport_type')
        if sport in VALID_SPORT_KEYS:
            request.session['selected_sport'] = sport
            return redirect('generators:fill_data')
        messages.error(request, 'Пожалуйста, выберите вид спорта')

    selected_sport = request.GET.get('sport', '')
    return render(request, 'generators/choose_sport.html', {
        'sport_types': sport_types,
        'selected_sport': selected_sport,
    })


def _fill_data_context(phys_form, max_form, sport, has_maxes, show_maxes_form, user):
    return {
        'phys_form': phys_form,
        'max_form': max_form,
        'sport': sport,
        'has_maxes': has_maxes,
        'show_maxes_form': show_maxes_form,
        'exercises_with_maxes': ExerciseMax.objects.filter(user=user).select_related('exercise'),
    }


@login_required
def fill_data(request):
    user = request.user
    sport = request.session.get('selected_sport')

    if not sport:
        messages.warning(request, 'Сначала выберите вид спорта')
        return redirect('generators:choose_sport')

    programs = TrainingProgram.objects.filter(sport_type=sport, user__isnull=True)

    if not programs.exists():
        messages.error(request, f'Нет программ для вида спорта "{sport}"')
        return redirect('generators:choose_sport')

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
        keep_maxes = 'keep_maxes' in request.POST

        if not phys_form.is_valid():
            messages.error(request, 'Проверьте физические данные')
            return render(
                request, 'generators/fill_data.html',
                _fill_data_context(phys_form, max_form, sport, has_maxes, show_maxes_form, user),
            )

        phys_form.save()

        if not keep_maxes:
            if not max_form.is_valid():
                messages.error(request, 'Проверьте введённые веса')
                return render(
                    request, 'generators/fill_data.html',
                    _fill_data_context(phys_form, max_form, sport, has_maxes, show_maxes_form, user),
                )
            if not ExerciseMax.objects.filter(user=user).exists():
                messages.error(request, 'Укажите хотя бы один рабочий максимум или сохраните текущие')
                return render(
                    request, 'generators/fill_data.html',
                    _fill_data_context(phys_form, max_form, sport, has_maxes, True, user),
                )
            for exercise in exercises:
                weight = max_form.cleaned_data.get(f'max_{exercise.id}')
                reps = max_form.cleaned_data.get(f'reps_{exercise.id}')
                if weight and reps:
                    ExerciseMax.objects.update_or_create(
                        user=user,
                        exercise=exercise,
                        defaults={'max_weight': int(weight), 'reps': reps},
                    )

        program = select_program(sport, 'beginner')
        if not program:
            messages.error(request, 'Не найдена подходящая программа')
            return redirect('generators:choose_sport')

        day = request.session.get(f'workout_day_{program.id}', 1)
        workout_template = ProgramWorkout.objects.filter(
            program=program,
            day_number=day,
        ).first()

        if not workout_template:
            messages.error(request, 'В программе нет тренировок')
            return redirect('generators:choose_sport')

        workout_log = generate_workout_log(user, program, workout_template)

        next_day = day + 1
        has_next = ProgramWorkout.objects.filter(program=program, day_number=next_day).exists()
        request.session[f'workout_day_{program.id}'] = next_day if has_next else 1

        messages.success(request, 'Тренировка сгенерирована!')
        return redirect('generators:workout_detail', workout_log_id=workout_log.id)

    phys_form = UserPhysicalDataForm(instance=user)
    initial_data = {}
    for exercise in exercises:
        max_obj = ExerciseMax.objects.filter(user=user, exercise=exercise).first()
        if max_obj:
            initial_data[f'max_{exercise.id}'] = max_obj.max_weight
            initial_data[f'reps_{exercise.id}'] = max_obj.reps

    max_form = ExerciseMaxForm(initial=initial_data, exercises=exercises)

    return render(request, 'generators/fill_data.html', {
        **_fill_data_context(phys_form, max_form, sport, has_maxes, show_maxes_form, user),
        'exercises_count': exercises.count(),
    })


@login_required
def workout_detail(request, workout_log_id):
    workout_log = get_object_or_404(
        WorkoutLog.objects.select_related('workout', 'program'),
        id=workout_log_id,
        user=request.user,
    )
    exercises = workout_log.exerciselog_set.all().order_by('order')
    return render(request, 'generators/workout_detail.html', {
        'workout_log': workout_log,
        'exercises': exercises,
    })


@login_required
def workout_history(request):
    workouts = WorkoutLog.objects.filter(
        user=request.user,
    ).select_related('program', 'workout').order_by('-date', '-id')
    return render(request, 'generators/workout_history.html', {'workouts': workouts})


@login_required
def regenerate_workout(request, workout_log_id):
    workout_log = get_object_or_404(WorkoutLog, id=workout_log_id, user=request.user)
    workout_log.exerciselog_set.all().delete()

    program_exercises = ProgramExercise.objects.filter(
        workout=workout_log.workout,
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
            notes='Обновлено',
        )

    messages.success(request, 'Тренировка обновлена с учётом новых данных!')
    return redirect('generators:workout_detail', workout_log_id=workout_log.id)


@login_required
def delete_workout(request, workout_log_id):
    workout_log = get_object_or_404(WorkoutLog, id=workout_log_id, user=request.user)

    if request.method == 'POST':
        workout_log.delete()
        messages.success(request, 'Тренировка удалена')
        return redirect('generators:workout_history')

    return render(request, 'generators/confirm_delete.html', {'workout_log': workout_log})


@login_required
def exercise_progress(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    logs = ExerciseLog.objects.filter(
        exercise=exercise,
        workout_log__user=request.user,
    ).select_related('workout_log').order_by('workout_log__date')

    dates = []
    weights = []
    volumes = []
    for log in logs:
        dates.append(log.workout_log.date.strftime('%Y-%m-%d'))
        weights.append(log.weight)
        volumes.append(log.weight * log.reps * log.sets)
        log.volume = log.weight * log.reps * log.sets

    return render(request, 'generators/exercise_progress.html', {
        'exercise': exercise,
        'logs': logs,
        'dates': dates,
        'weights': weights,
        'volumes': volumes,
    })
