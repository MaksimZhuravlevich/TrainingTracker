from django.urls import path
from . import views

urlpatterns = [
    path('nutrition',views.nutrition,name='nutrition'),


]