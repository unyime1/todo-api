from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractUser): 
    """custom user model"""
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    first_name = models.CharField(null=True, blank=True, max_length=700)
    last_name = models.CharField(null=True, blank=True, max_length=700)
    date_created =  models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.email  
