from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('progress',views.progress,name='progress'),
    path('type',views.type,name='type'),
    path('trainings',views.trainings,name='trainings'),
    path('sport_fitness',views.sport_fitnes,name='sport_fitness'),
    path('sport_powerlifting',views.sport_powerlifting,name='sport_powerlifting'),
    path('sport_crossfit', views.sport_crossfit, name='sport_crossfit'),
    path('sport/weightlifting/', views.sport_weightlifting, name='sport_weightlifting'),
    path('sport/keeping-form/', views.sport_keeping_form, name='sport_keeping_form'),
    path('sport/athletics/', views.sport_athletics, name='sport_athletics'),
    ]