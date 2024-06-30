from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from django.contrib import messages
from django.db.models.signals import pre_save

from .forms import (LoginForm, SignupForm)

from .models import(
    User
)


def login_view(request):
    form = LoginForm()
    if request.method=='POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)

        user = authenticate(request, username=username, password=password)
        if user:
            login(request,user)
            messages.success(request,('Logged in successfully!'))
            return redirect('/') 
        else:
            messages.error(request,('Incorrect credentials. Try again.'))
            return redirect('login')
    else:
        return render(request,'base/login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('/')

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
        user.save()
        return redirect('login')

    return render(request, 'base/signup.html', {'form':form}) 


    