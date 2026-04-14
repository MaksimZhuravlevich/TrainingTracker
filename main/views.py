from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'main/index.html')
def type(request):
    return render(request,'main/type.html')
def progress(request):
    return render(request,'main/progress.html')
def trainings(request):
    return render(request,'main/trainings.html')
def sport_fitnes(request):
    return render(request,'main/sport_fitness.html')
def sport_powerlifting(request):
    return render(request,'main/sport_powerlifting.html')
def sport_crossfit(request):
    return render(request, 'main/sport_crossfit.html')
def sport_weightlifting(request):
    return render(request, 'main/sport_weightlifting.html')

def sport_keeping_form(request):
    return render(request, 'main/sport_keeping_form.html')

def sport_athletics(request):
    return render(request, 'main/sport_athletics.html')