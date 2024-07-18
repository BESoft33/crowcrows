from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from crowapp.models import User
from .utils import get_user_from_token

class IsAuthor(BaseAuthentication):
    def authenticate(self, request):
        authorization = request.headers.get('Authorization')
        if not authorization:
            return None
        
        user = get_user_from_token(authorization)
        if user is None:
            raise exceptions.AuthenticationFailed('No such user')
        
        if user.role == User.Role.AUTHOR:
            return user
        
        return None
    

class IsAdmin(BaseAuthentication):
    def authenticate(self, request):
        authorization = request.headers.get('Authorization')
        if not authorization:
            return None
        
        user = get_user_from_token(authorization)
        if user is None:
            raise exceptions.AuthenticationFailed('No such user')
        
        if user.is_superuser:
            return user
        
        return None
    

class IsModerator(BaseAuthentication):
    def authenticate(self, request):
        authorization = request.headers.get('Authorization')
        if not authorization:
            return None
        
        user = get_user_from_token(authorization)
        if user is None:
            raise exceptions.AuthenticationFailed('No such user')
        
        if user.is_superuser:
            return user
        
        return None
    

class IsEditor(BaseAuthentication):
    def authenticate(self, request):
        authorization = request.headers.get('Authorization')
        if not authorization:
            return None
        
        user = get_user_from_token(authorization)
        if user is None:
            raise exceptions.AuthenticationFailed('No such user')
        
        if user.role == User.Role.EDITOR:
            return user
        
        return None
