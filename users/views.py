"""This module handles the users app views"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import *


class HelloView(APIView):
    """Home View"""

    def get(self, request):
        content = {'message': 'Hello World'}
        return Response(content) 


class CreateUserView(CreateAPIView): 
    """User Registration Class"""
    model = get_user_model()
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            #make a user active by default
            user.is_active = True
            user.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Handle app logins"""
    def post(self, request, format=None): 
        serializer = LoginSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_object_or_404(CustomUser, email=email)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'token': token.key,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
