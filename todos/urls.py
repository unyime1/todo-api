"""this module handles the todos app urls"""

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# API endpoints
urlpatterns = format_suffix_patterns([
    path('todo/<str:user_pk>/create/', views.CreateTodoView().as_view(), name="create_todo"),
    path('todo/<str:user_pk>/', views.GetUserTodosView().as_view(), name="get_user_todos"),
    path('todo/<str:user_pk>/<str:todo_pk>/', views.GetTodoDetailView().as_view(), name="get_todo_detail"),
    path('todo/<str:user_pk>/<str:todo_pk>/update/', views.UpdateTodoDetailView().as_view(), name="update_todo_detail"),
    path('todo/<str:user_pk>/<str:todo_pk>/delete/', views.DeleteTodoDetailView().as_view(), name="delete_todo_detail"),
])