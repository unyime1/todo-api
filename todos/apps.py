"""this module handles the todos app apps"""
from django.apps import AppConfig


class TodosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todos'
