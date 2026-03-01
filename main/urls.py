from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('progress',views.progress,name='progress'),
    path('type',views.type,name='type'),
    path('trainings',views.trainings,name='trainings'),

]