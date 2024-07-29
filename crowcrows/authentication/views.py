from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import exceptions
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, BlacklistMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import SignupSerializer, UserSerializer, PasswordResetSerializer
from django.db import IntegrityError
from .utils import get_tokens_for_user

User = get_user_model()


class SignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({'status': 'success', 'redirect_url': 'login', 'data': serializer.data},
                                status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {'status': 'error', 'message': 'An account with the provided email address already exists.'},
                    status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView, BlacklistMixin):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'status': 'success', 'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        response = Response()
        if not email or not password:
            raise exceptions.AuthenticationFailed('username and password required')

        user = authenticate(request, email=email, password=password)
        if user:
            refresh, access = get_tokens_for_user(user)
            data = UserSerializer(user).data
        else:
            raise exceptions.AuthenticationFailed("Email and password mismatch.")
        response.set_cookie(key='refresh', value=refresh, httponly=True)
        response.data = {
            'access': access,
            'refresh': refresh,
            'data': data
        }
        return response


class PasswordForgotView(APIView):
    pass


class PasswordResetView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user = authenticate(request, email=request.data['email'], password=request.data['password'])
            print(request.data)
            print(check_password(user, request.data['password']))
            if user:
                serializer = PasswordResetSerializer(user, request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(str(serializer))
            else:
                raise User.DoesNotExist(
                    "Please enter correct combination of email and password to change your password."
                )
        except Exception as e:
            return Response(str(e))



