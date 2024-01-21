from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from django.contrib import messages

from .forms import (LoginForm, SignupForm)

from .models import(
     User, Article
)
from api.serializer import (
    BloggerSerializer,
    ArticleSerializer,
)

#general views
def home(request):
    art = Article.objects.all()
    # print(article.title)
    return render(request,'base/home.html', {"article": art})

def article(request, slug):
    return render(request, 'base/article.html',{"article":Article.objects.get(slug=slug)})

def login_view(request):
    form = LoginForm()
    if request.method=='POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)

        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            print("Logged in")
            messages.success(request,('Logged in successfully!'))
            login(request,user)
            return redirect('/') 
        else:
            print("error")
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
        # form = SignupForm()
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(first_name,last_name,email,password)
        user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=str(last_name)+'.'+str(first_name))
        user.save()
        return redirect('login')

    return render(request, 'base/signup.html', {'form':form}) 

