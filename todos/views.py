"""This module handles the users app views"""
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from .models import *
from users.models import *


class CreateTodoView(APIView):
    """Handle todo creation"""
    permission_classes = [IsAuthenticated]

    def post(self, request, user_pk, format=None):
        #create todo
        user = get_object_or_404(CustomUser, email=user_pk)
        serializer = TodoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            todo = serializer.save()
            todo.code = uuid.uuid4()
            todo.user = user
            todo.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class GetUserTodosView(APIView):
    """Handle todo retrieval"""
    permission_classes = [IsAuthenticated]

    def get(self, request, user_pk, format=None):
        #get todo
        user = get_object_or_404(CustomUser, email=user_pk)
        todos = Todo.objects.filter(user=user, delete=False).order_by("-date_created")
        serializer = TodoGetSerializer(todos, many=True)
        #additional check to ensure that requests are sent by resource owner
        if user == request.user:
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTodoDetailView(APIView):
    """Handle todo retrieval"""
    permission_classes = [IsAuthenticated]

    def get(self, request, user_pk, todo_pk, format=None):
        #get todo
        
        user = get_object_or_404(CustomUser, email=user_pk)
        todo = get_object_or_404(Todo, code=todo_pk, user=user, delete=False)
        serializer = TodoGetSerializer(todo)
        #additional check to ensure that requests are sent by resource owner
        if user == request.user:
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UpdateTodoDetailView(APIView):
    """Handle todo update"""
    permission_classes = [IsAuthenticated]

    def put(self, request, user_pk, todo_pk, format=None):
        #update todo
        user = get_object_or_404(CustomUser, email=user_pk)
        todo = get_object_or_404(Todo, code=todo_pk, user=user, delete=False)
        serializer = TodoSerializer(todo, data=request.data)
        #additional security check to ensure that requests are sent by resource owner
        if user == request.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeleteTodoDetailView(APIView):
    """Handle todo deletion"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_pk, todo_pk, format=None):
        #delete todo
        user = get_object_or_404(CustomUser, email=user_pk)
        todo = get_object_or_404(Todo, code=todo_pk, user=user)
        #additional check to ensure that requests are sent by resource owner
        if user == request.user:
            #hide data from user
            todo.delete = True
            todo.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)