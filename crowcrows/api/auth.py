from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions, status
from crowapp.models import User
from rest_framework.response import Response

from .utils import get_user_from_token


def get_authorization_header(authorization=None):
    if not authorization:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    user = get_user_from_token(authorization)
    if user is None:
        raise exceptions.AuthenticationFailed('No such user')

    return user


class IsAuthor(BaseAuthentication):
    def authenticate(self, request):
        user = get_user_from_token(request.headers.get('Authorization'))
        if user.role == User.Role.AUTHOR:
            return user, None
        return exceptions.AuthenticationFailed('You are not authorized to view this page')


class IsAdmin(BaseAuthentication):
    def authenticate(self, request):
        user = get_user_from_token(request.headers.get('Authorization'))
        if user.is_superuser:
            print("Authenticated as Admin")
            return user, None
        return exceptions.AuthenticationFailed('You are not authorized to view this page')


class IsModerator(BaseAuthentication):
    def authenticate(self, request):
        user = get_user_from_token(request.headers.get('Authorization'))
        if user.is_superuser:
            print("Authenticated as Moderator")
            return user, None
        return exceptions.AuthenticationFailed('You are not authorized to view this page')


class IsEditor(BaseAuthentication):
    def authenticate(self, request):
        user = get_user_from_token(request.headers.get('Authorization'))
        if user.role == User.Role.EDITOR:
            print("Authenticated as Editor")
            return user, None
        return exceptions.AuthenticationFailed('You are not authorized to view this page')
