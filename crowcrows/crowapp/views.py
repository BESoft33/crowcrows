from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
import json

from .models import (
    User
)
from rest_framework_simplejwt.tokens import RefreshToken


@csrf_exempt
def logout_view(request):
    token = RefreshToken(request.headers['Authorization'])
    return redirect(f'/token/blacklist/')



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
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                                password=password)
                user.save()
                return JsonResponse({'status': 'success', 'redirect_url': 'login'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})
        except json.JSONDecodeError as je:
            return JsonResponse({'status': 'error', 'message': 'Could not read the provided data.'})
        except IntegrityError:
            return JsonResponse(
                {'status': 'error', 'message': 'An account with provided email address already exists.'})

    return JsonResponse({'status': 'error', 'message': 'Only post method is allowed'})
