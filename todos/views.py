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
            code = uuid.uuid4()
            serializer.save(code=code, user=user)
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
        #additional security check to ensure that requests are sent by resource owner
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
        #additional security check to ensure that requests are sent by resource owner
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
        #additional security check to ensure that requests are sent by resource owner
        if user == request.user:
            #hide data from user
            todo.delete = True
            todo.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)





"""
    In a bid to reduce code size and avoid excessive repetitions, below is how I would normally 
    build a similar API. Since this is for demonstrative purposes only, accompanying unit tests 
    will not be created. In the example below, only 2 endpoints are needed instead of 5. 
    'todo/' handles the creation and retrieval of user's todolists with 'post' and 
    'get' requests respectively, while the updates, deletions,
    and detail retrievals are handled by 'todo_detail/' utilizing 'put', 'delete', and 'get'
    requests respectively.

"""




class TodoView(APIView):
    """handle the creation and retrieval of todo lists"""
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        #get todo lists related to user sending the request
        user = request.user
        todos = Todo.objects.filter(user=user, delete=False).order_by("-date_created")
        serializer = TodoGetSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        #create todo list for user making the request
        user = request.user
        serializer = TodoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            code = uuid.uuid4()
            serializer.save(code=code, user=user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TodoDetailView(APIView):
    """handle the retrieval, update and deletion of individual todo-lists"""
    permission_classes = [IsAuthenticated]
    
    def get_todo(self, request, pk):
        #retrieve todo
        user = request.user
        todo = get_object_or_404(Todo, code=pk, user=user, delete=False)
        return todo

    def get(self, request, pk, format=None):
        #get a specific todo
        todo = self.get_todo(request, pk)
        serializer = TodoGetSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        #update a specific todo
        todo = self.get_todo(request, pk)
        serializer = TodoSerializer(todo, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        #delete a specific todo
        #this actually hides the todo instead of an outright deletion
        todo = self.get_todo(request, pk)        
        todo.delete = True
        todo.save()
        return Response(status=status.HTTP_200_OK)

    