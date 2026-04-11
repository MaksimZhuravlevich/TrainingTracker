from django.db import models
from django.conf import settings
from programs.models import ProgramWorkout ,TrainingProgram
from exercises.models import Exercise
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


class ExerciseMax(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,

    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE
    )
    max_weight=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(300)])
    reps=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(100)])

    class Meta:
        unique_together = ('user', 'exercise')
class WorkoutLog(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    workout=models.ForeignKey(
        ProgramWorkout,
        on_delete=models.CASCADE
    )
    program=models.ForeignKey(
        TrainingProgram,
        on_delete=models.CASCADE
    )

    date=models.DateField(default=date.today)
    duration=models.DurationField(blank=True,null=True)
    notes=models.TextField(blank=True,null=True)
    def __str__(self):
        return f"{self.workout}-{self.date}"



class ExerciseLog(models.Model):
    workout_log=models.ForeignKey(
        WorkoutLog,
        on_delete=models.CASCADE,

    )
    exercise=models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE
    )
    weight=models.FloatField(validators=[MinValueValidator(1),
                                         MaxValueValidator(300)])
    reps = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                         MaxValueValidator(300)])
    sets = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                         MaxValueValidator(30)])
    order = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    performed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.exercise.name}-{self.workout_log.date}"

class CalendarEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    workout_log = models.ForeignKey(
        WorkoutLog,
        on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('done','Выполнено'),('skipped','Пропущено')])
    notes = models.TextField(blank=True, null=True)
class UserProgress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_program = models.ForeignKey('programs.TrainingProgram', null=True, blank=True, on_delete=models.SET_NULL)
    current_day = models.PositiveIntegerField(default=1)
    started_at = models.DateTimeField(auto_now_add=True)
class ExerciseProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE)
    start_weight = models.FloatField(null=True, blank=True)
    current_weight = models.FloatField(null=True, blank=True)
    start_reps = models.PositiveIntegerField(null=True, blank=True)
    current_reps = models.PositiveIntegerField(null=True, blank=True)
    progress_percentage = models.FloatField(null=True, blank=True)

    class UserWorkoutProgress(models.Model):
        """Отслеживает прогресс пользователя по программе"""
        user = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='workout_progress'
        )
        current_program = models.ForeignKey(
            'programs.TrainingProgram',
            on_delete=models.SET_NULL,
            null=True,
            blank=True
        )
        current_day = models.PositiveIntegerField(default=1)
        started_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return f"{self.user.email} - День {self.current_day}"