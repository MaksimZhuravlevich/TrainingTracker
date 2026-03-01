from django.shortcuts import render

# Create your views here.
def help(request):
    return render(request,'core/help.html')
def knowledge(request):
    return render(request,'core/knowledge.html')
def settings(request):
    return render(request,'core/settings.html')
