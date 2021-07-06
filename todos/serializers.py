"""this module handles todos app serializations"""

from rest_framework import serializers
from .models import *
from users.models import CustomUser


class TodoSerializer(serializers.ModelSerializer):
    """serialize todo data"""
    title = serializers.CharField(max_length=650)
    description = serializers.CharField(max_length=6050)
    class Meta:
        model = Todo
        fields = ['title', 'description'] 


class UserFieldSerializer(serializers.ModelSerializer):
    """serialize user fields"""
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name'] 


class TodoGetSerializer(serializers.ModelSerializer):
    """serialize todo data"""
    user = UserFieldSerializer()
    class Meta:
        model = Todo
        fields = ['code', 'user', 'title', 'description',
        'done', 'date_created'
        ] 
