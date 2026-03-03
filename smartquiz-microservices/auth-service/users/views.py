from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUserRole

from rest_framework_simplejwt.views import TokenObtainPairView
from .token_serializer import CustomTokenObtainPairSerializer


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "JWT is working!",
            "user": request.user.username,
            "role": request.user.role
        })


class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get(self, request):
        return Response({
            "message": "Welcome Admin!",
            "user": request.user.username
        })



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer