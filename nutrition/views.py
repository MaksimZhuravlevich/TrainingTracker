from django.shortcuts import render

# Create your views here.
def nutrition(request):
    return render(request,'nutrition/nutrition.html')