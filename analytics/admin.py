from django.contrib import admin
from .models import ExerciseMax, WorkoutLog, ExerciseLog, CalendarEntry, ExerciseProgress

@admin.register(ExerciseMax)
class ExerciseMaxAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise', 'max_weight', 'reps']
    list_filter = ['exercise']
    search_fields = ['user__email', 'exercise__name']
    autocomplete_fields = ['user', 'exercise']

@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'workout', 'program', 'date']
    list_filter = ['date', 'program']
    search_fields = ['user__email']
    date_hierarchy = 'date'

class ExerciseLogInline(admin.TabularInline):
    model = ExerciseLog
    extra = 0
    fields = ['exercise', 'weight', 'reps', 'sets', 'order']
    readonly_fields = ['performed_at']

@admin.register(ExerciseLog)
class ExerciseLogAdmin(admin.ModelAdmin):
    list_display = ['workout_log', 'exercise', 'weight', 'reps', 'sets']
    list_filter = ['workout_log__date']
    search_fields = ['exercise__name']
    autocomplete_fields = ['exercise']

@admin.register(CalendarEntry)
class CalendarEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'workout_log', 'status']
    list_filter = ['status']

@admin.register(ExerciseProgress)
class ExerciseProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise', 'current_weight', 'progress_percentage']
    search_fields = ['user__email', 'exercise__name']