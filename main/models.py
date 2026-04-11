from django.db import models
from django.contrib.auth.models import AbstractUser, \
    BaseUserManager
from django.conf import settings
from django.utils.html import strip_tags
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


# class UserTraining(models.Model):
#
#        user = models.ForeignKey(
#            settings.AUTH_USER_MODEL,
#            on_delete=models.CASCADE,
#            related_name='training',
#            verbose_name='User'
#
#        )
#        SPORT_TYPES = [
#             ('powerlifting', 'Пауэрлифтинг'),
#             ('weightlifting', 'Тяжелая атлетика'),
#             ('athletics', 'Легкая атлетика'),
#             ('fitness', 'Фитнес'),
#             ('crossfit', 'Кроссфит'),
#             ('keeping_form', 'Поддержание формы'),
#
#         ]
#
#        sport_type=models.CharField(
#            max_length=20,
#            choices=SPORT_TYPES,
#            default='keeping_form',
#            verbose_name='Спортивное направление'
#        )
#
#        name=models.CharField(
#            max_length=200,
#            verbose_name='Название тренировки'
#        )
#
#        date = models.DateField(
#             verbose_name='Дата тренировки',
#             default=date.today
#        )
#
#        duration=models.IntegerField(
#            verbose_name='Длительность тренировки',
#            null=True,
#            blank=True,
#            help_text='В минутах'
#        )
#
#        notes=models.TextField(
#            verbose_name='Заметки',
#            null=True,
#            blank=True,
#        )
#
#        created_at = models.DateTimeField(
#            auto_now_add=True,
#            verbose_name="Дата создания"
#        )
#
#        class Meta:
#            ordering = ['-date', '-created_at']
#            verbose_name = "Тренировка"
#            verbose_name_plural = "Тренировки"
#
#        def __str__(self):
#            return f"{self.name}-{self.date}"
#
#

