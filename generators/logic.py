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
    last_logs = ExerciseLog.objects.filter(
        exercise=exercise,
        workout_log_user=user
    ).order_by('-performed_at')[:3]
    if last_logs:
        last_log=last_logs.first()
        all_successful = all(
            log.reps >= program_exercise.reps for log in last_logs
        ) and len(last_logs) >= 3
        if all_successful:

            new_weight = last_log.weight + 2.5
            return round(new_weight, 1)
        else:

            return last_log.weight
    try:
        max_obj = ExerciseMax.objects.get(user=user, exercise=exercise)
        return round(max_obj.max_weight * 0.7, 1)
    except ExerciseMax.DoesNotExist:
        return base_weight


def generate_workout_log(user, program, workout_template):
    with transaction.atomic():

        workout_log = WorkoutLog.objects.create(
            user=user,
            workout=workout_template,
            program=program,
            date=date.today(),
            notes='Сгенерировано автоматически'
        )

        program_exercises = ProgramExercise.objects.filter(
            workout=workout_template
        ).order_by('order')

        for prog_ex in program_exercises:
            if not prog_ex.exercise:
                continue

            weight = calculate_working_weight(user, prog_ex.exercise, prog_ex)

            ExerciseLog.objects.create(
                workout_log=workout_log,
                exercise=prog_ex.exercise,
                weight=weight,
                reps=prog_ex.reps,
                sets=prog_ex.sets,
                order=prog_ex.order,
                notes=''
            )

        return workout_log