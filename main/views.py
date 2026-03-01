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