from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import (
    User
)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, ('Logged in successfully!'))
            return redirect('/')
        else:
            messages.error(request, ('Incorrect credentials. Try again.'))
            return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('/')

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data.get("firstname")
            last_name = data.get("lastname")
            email = data.get("email")
            password = data.get("password")
            password_confirm = data.get("passwordRepeat")
            if password == password_confirm:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
                user.save()
                return JsonResponse({'status': 'success', 'redirect_url': 'login'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})

    return JsonResponse({'status': 'error', 'message': 'Only post method is allowed'})
