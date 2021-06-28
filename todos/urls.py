"""this module handles the todos app urls"""

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# API endpoints
urlpatterns = format_suffix_patterns([
    path('todo/<str:user_pk>/create/', views.CreateTodoView().as_view(), name="create-todo"),
    path('todo/<str:user_pk>/', views.GetUserTodosView().as_view(), name="get-user-todos"),
    path('todo/<str:user_pk>/<str:todo_pk>/', views.GetTodoDetailView().as_view(), name="get-todo-detail"),
    path('todo/<str:user_pk>/<str:todo_pk>/update/', views.UpdateTodoDetailView().as_view(), name="update-todo-detail"),
    path('todo/<str:user_pk>/<str:todo_pk>/delete/', views.DeleteTodoDetailView().as_view(), name="delete-todo-detail"),

    #extra/alternative code

    path('todo/', views.TodoView().as_view(), name="todo"),
    path('todo-detail/<str:pk>/', views.TodoDetailView().as_view(), name="todo-detail"),

])