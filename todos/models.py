"""this module handles the todos app models"""

from django.db import models

# Create your models here.
class Todo(models.Model):
    """user todo model"""
    
    code = models.CharField(null=True, blank=True, max_length=700)
    user = models.ForeignKey("users.CustomUser", related_name="todo", null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(null=True, blank=True, max_length=700)
    description = models.CharField(null=True, blank=True, max_length=4000)
    done = models.BooleanField(default=False, null=True, blank=True)
    delete = models.BooleanField(default=False, null=True, blank=True)
    date_created =  models.DateTimeField(auto_now_add=True, null=True, blank=True)