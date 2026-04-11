from django.contrib import admin
from .models import TrainingProgram, ProgramWorkout, ProgramExercise

class ProgramWorkoutInline(admin.TabularInline):
    model = ProgramWorkout
    extra = 1
    fields = ['name', 'day_number', 'notes']

class ProgramExerciseInline(admin.TabularInline):
    model = ProgramExercise
    extra = 3
    fields = ['exercise', 'sets', 'reps', 'rest_time', 'order']

@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'sport_type', 'experience', 'weeks', 'user', 'created_at']
    list_filter = ['sport_type', 'experience']
    search_fields = ['name']
    inlines = [ProgramWorkoutInline]
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'sport_type', 'experience', 'weeks')
        }),
    )

@admin.register(ProgramWorkout)
class ProgramWorkoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'program', 'day_number']
    list_filter = ['program__sport_type']
    search_fields = ['name']
    inlines = [ProgramExerciseInline]

@admin.register(ProgramExercise)
class ProgramExerciseAdmin(admin.ModelAdmin):
    list_display = ['exercise', 'workout', 'sets', 'reps', 'rest_time', 'order']
    list_filter = ['workout__program__sport_type']
    search_fields = ['exercise__name']
    autocomplete_fields = ['exercise']  # удобно, если много упражнений