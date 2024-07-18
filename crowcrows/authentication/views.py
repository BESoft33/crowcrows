from django.shortcuts import redirect
from django.db.utils import IntegrityError

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import SignupSerializer
from django.db import IntegrityError

class SignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({'status': 'success', 'redirect_url': 'login', 'data':serializer.data}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'status': 'error', 'message': 'An account with the provided email address already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'status':'success', 'message':'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'error', 'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)