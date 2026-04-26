from django.urls import path
from . import views

app_name = 'generators'

urlpatterns = [
    path('choose-sport/', views.choose_sport, name='choose_sport'),
    path('fill-data/', views.fill_data, name='fill_data'),
    path('workout/<int:workout_log_id>/', views.workout_detail, name='workout_detail'),
    path('history/', views.workout_history, name='workout_history'),
    path('regenerate/<int:workout_log_id>/', views.regenerate_workout, name='regenerate_workout'),
    path('delete/<int:workout_log_id>/', views.delete_workout, name='delete_workout'),
    path('progress/exercise/<int:exercise_id>/', views.exercise_progress, name='exercise_progress'),
]