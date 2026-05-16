from django.shortcuts import render
from analytics.models import WorkoutLog


def index(request):
    return render(request, 'main/index.html')


def type(request):
    return render(request, 'main/type.html')


def progress(request):
    context = {
        'workout_count': 0,
        'recent_workouts': [],
    }
    if request.user.is_authenticated:
        logs = WorkoutLog.objects.filter(user=request.user).select_related('workout', 'program')
        context['workout_count'] = logs.count()
        context['recent_workouts'] = logs.order_by('-date', '-id')[:5]
    return render(request, 'main/progress.html', context)


def trainings(request):
    return render(request, 'main/trainings.html')


def sport_fitnes(request):
    return render(request, 'main/sport_fitness.html')


def sport_powerlifting(request):
    return render(request, 'main/sport_powerlifting.html')


def sport_crossfit(request):
    return render(request, 'main/sport_crossfit.html')


def sport_weightlifting(request):
    return render(request, 'main/sport_weightlifting.html')


def sport_keeping_form(request):
    return render(request, 'main/sport_keeping_form.html')


def sport_athletics(request):
    return render(request, 'main/sport_athletics.html')
