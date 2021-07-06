"""this module handles users app tests"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import *


class CustomUserModelTestCase(TestCase):
    """Test CustomUser model"""

    def setUp(self):
        """Define the test client and other test variables."""
        self.user = CustomUser(
            email="test@test.com", first_name="Test",
            last_name="Test", password="testing456"
        )

    def test_model_can_create_a_user(self):
        """Test the CustomUser model can create a user."""
        old_count = CustomUser.objects.count()
        self.user.save()
        new_count = CustomUser.objects.count()
        self.assertNotEqual(old_count, new_count)



class UserAuthTestCase(TestCase):
    """Test suite for for account creation and authentication"""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user_data = {
            "email":"test@test.com", 
            "first_name":"Test",
            "last_name":"Test", 
            "password":"testing456"
        }
        self.response = self.client.post(
            reverse('register'),
            self.user_data,
            format="json"
        )

    def test_todo_api_can_create_a_user(self):
        """Test the api has user creation capability"""
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_todo_api_can_login_a_user(self):
        """Test the api has user login capability"""
        self.login_data = {
            "email":"test@test.com", 
            "password":"testing456"
        }
        self.login_response = self.client.post(
            reverse('login'),
            self.login_data,
            format="json"
        )
        self.assertEqual(self.login_response.status_code, status.HTTP_200_OK)





