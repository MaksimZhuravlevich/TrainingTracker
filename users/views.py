from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm
from .models import CustomUser



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user,backend='django.contrib.backends.ModelBackend')
            return redirect('user:profile')
        else:
            form=CustomUserCreationForm()
        return render(request,'users/register.html',
                      {'form':form})

def login_view(request):
    if request.method=='POST':
        form = CustomUserLoginForm(request=request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user,backend='django.contrib.backends.ModelBackend')
            return redirect('users:profile')
        else:
            form=CustomUserLoginForm()
        return render(request,'users/login.html',{'form':form})


@login_required
def profile_views(request):
    return render(request,'user/profile.html',{'user':request.user})