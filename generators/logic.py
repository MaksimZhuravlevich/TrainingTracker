from datetime import date
from django.db import transaction
from programs.models import TrainingProgram, ProgramWorkout, ProgramExercise
from analytics.models import ExerciseMax, WorkoutLog, ExerciseLog

def select_program(sport_type, experience='beginner'):
    program = TrainingProgram.objects.filter(
        sport_type=sport_type,
        experience=experience,
        user__isnull=True
    ).first()

    if not program:
        program = TrainingProgram.objects.filter(
            sport_type=sport_type,
            user__isnull=True
        ).first()

    if not program:
        program = TrainingProgram.objects.filter(user__isnull=True).first()

    return program


def calculate_working_weight(user, exercise, program_exercise, base_weight=20.0):
    # 1. Рассчитываем вес из ExerciseMax (текущий рекорд, с учётом повторений)
    try:
        max_obj = ExerciseMax.objects.get(user=user, exercise=exercise)
        if max_obj.reps == 1:
            one_rep_max = max_obj.max_weight
        else:
            one_rep_max = max_obj.max_weight * (1 + max_obj.reps / 30)
        weight_from_max = round(one_rep_max * 0.7, 1)
    except ExerciseMax.DoesNotExist:
        weight_from_max = base_weight

    # 2. Смотрим последние логи (история тренировок)
    last_logs = ExerciseLog.objects.filter(
        exercise=exercise,
        workout_log__user=user
    ).order_by('-performed_at')[:3]

    if not last_logs:
        return weight_from_max

    last_log = last_logs.first()
    # Проверяем, были ли 3 последние тренировки успешными
    all_successful = all(
        log.reps >= program_exercise.reps for log in last_logs
    ) and len(last_logs) >= 3

    if all_successful:
        weight_from_history = last_log.weight + 2.5
    else:
        weight_from_history = last_log.weight

    # --- Главное изменение ---
    # Если новый максимум меньше последнего веса из истории → пользователь снизил силу
    # Тогда используем новый, меньший вес. Иначе – максимальный из двух (чтобы не терять прогресс)
    if weight_from_max < weight_from_history:
        return weight_from_max
    else:
        return max(weight_from_history, weight_from_max)

def generate_workout_log(user, program, workout_template):

    with transaction.atomic():
        # Создаём основную запись о тренировке
        workout_log = WorkoutLog.objects.create(
            user=user,
            workout=workout_template,
            program=program,
            date=date.today(),
            notes='Сгенерировано автоматически'
        )

        program_exercises = ProgramExercise.objects.filter(
            workout=workout_template
        ).order_by('order').select_related('exercise')

        for prog_ex in program_exercises:
            if not prog_ex.exercise:
                continue  # пропускаем, если упражнение удалено

            # Рассчитываем рабочий вес (использует текущий 1ПМ или базовый вес)
            weight = calculate_working_weight(user, prog_ex.exercise, prog_ex)

            # Создаём запись о выполнении упражнения
            log = ExerciseLog.objects.create(
                workout_log=workout_log,
                exercise=prog_ex.exercise,
                weight=weight,
                reps=prog_ex.reps,
                sets=prog_ex.sets,
                order=prog_ex.order,
                notes=''
            )
        return workout_log
