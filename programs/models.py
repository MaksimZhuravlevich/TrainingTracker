from django.db import models
from django.conf import settings
from exercises.models import Exercise

class TrainingProgram(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='programs',
        null=True,
        blank=True
    )

    SPORT_TYPES=[
            ('powerlifting', 'Пауэрлифтинг'),
            ('weightlifting', 'Тяжелая атлетика'),
            ('athletics', 'Легкая атлетика'),
            ('fitness', 'Фитнес'),
            ('crossfit', 'Кроссфит'),
            ('keeping_form', 'Поддержание формы'),

    ]

    sport_type = models.CharField(
        max_length=20,
        choices=SPORT_TYPES,
        default='keeping_form',
        verbose_name='Спортивное направление'
    )
    experience = models.CharField(
        max_length=10,
        choices=[('beginner', 'Начинающий'), ('middle', 'Обычно'), ('pro', 'Опытный')],
        default='beginner'
    )
    name=models.CharField(max_length=100)
    weeks=models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProgramWorkout(models.Model):
    program=models.ForeignKey(
        TrainingProgram,
        on_delete=models.CASCADE,

    )
    name=models.CharField(max_length=100)
    day_number=models.PositiveIntegerField()
    notes=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['day_number']

class ProgramExercise(models.Model):
    workout=models.ForeignKey(
        ProgramWorkout,
        on_delete=models.CASCADE,
        related_name='programexercise',

    )
    exercise=models.ForeignKey(
        Exercise,
        on_delete=models.SET_NULL,
        blank=True,
        null=True

    )
    sets=models.PositiveIntegerField()
    reps=models.PositiveIntegerField()
    rest_time=models.PositiveIntegerField()
    order=models.PositiveIntegerField()

    class Meta:
        ordering = ['order']