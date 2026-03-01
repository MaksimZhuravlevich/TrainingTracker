from django.urls import path
from . import views

urlpatterns = [
    path('help',views.help,name="help"),
    path('knowledge',views.knowledge,name="knowledge"),
    path('settings',views.settings,name="settings")
]
