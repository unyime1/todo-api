"""this module handles the users app model registrations"""

from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CustomUser)