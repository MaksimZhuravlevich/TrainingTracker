from django.contrib import admin
from .models import MuscleGroup, Equipment, Exercise

@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'equipment']
    list_filter = ['muscles', 'equipment']
    search_fields = ['name', 'description']
    filter_horizontal = ['muscles']  # удобный виджет для ManyToMany
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'muscles', 'equipment')
        }),
    )