"""this module handles the todos app tests"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import *
from users.models import CustomUser

class TodoModelTestCase(TestCase):
    """Test Todo model"""

    def setUp(self):
        """Define the test client and other test variables."""
        self.user = CustomUser.objects.create(
            email="test@test.com", first_name="Test",
            last_name="Test", password="testing456"
        )
        self.todo = Todo(
            user=self.user, title="test", description="test"
        )

    def test_model_can_create_a_todo(self):
        """Test the Todo model can create a todo."""
        old_count = Todo.objects.count()
        self.todo.save()
        new_count = Todo.objects.count()
        self.assertNotEqual(old_count, new_count)



class TodoTestCase(TestCase):
    """Test todo creation and retrieval"""
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        #create user
        self.user = CustomUser.objects.create(
            email="test@test.com", first_name="Test",
            last_name="Test"
        )
        self.client.force_authenticate(user=self.user)

        #create todo
        self.todo_data = {
            "title":"test",
            "description":"test"
        }
        self.response = self.client.post(
            reverse('create_todo', kwargs={'user_pk': self.user.email}),
            self.todo_data,
            format="json"
        )

    def test_authorization_is_enforced(self):
        #Test that the api has user authorization.
        new_client = APIClient()
        response = new_client.get(
            reverse('create_todo', kwargs={'user_pk': self.user.email}),
            self.todo_data,
            format="json"
        )
        self.assertEqual(response.status_code, 401)

    def test_todo_api_can_create_todo(self):
        #Test the api can create a todo
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_todo_api_can_get_user_todos(self):
        #test that the todo api can get a user's todos
        response = self.client.get(
            reverse('get_user_todos', kwargs={'user_pk': self.user.email}),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TodoDetailTestCase(TestCase):
    """test todo details"""
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        #create user
        self.user = CustomUser.objects.create(
            email="test@test.com", first_name="Test",
            last_name="Test"
        )
        self.client.force_authenticate(user=self.user)
        #create todo
        self.todo = Todo.objects.create(
            user=self.user,
            title="test",
            description="test",
            code="test123"
        )

    def test_authorization_is_enforced(self):
        #Test that the api has user authorization.
        new_client = APIClient()
        response = new_client.get(
            reverse('get_todo_detail', kwargs={'user_pk': self.user.email, 'todo_pk':self.todo.code}),
            format="json"
        )
        self.assertEqual(response.status_code, 401)
    
    def test_api_can_return_todo_detail(self):
        response = self.client.get(
            reverse('get_todo_detail', kwargs={'user_pk': self.user.email, 'todo_pk':self.todo.code}),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_update_todo(self):
        changed_todo = {'title': 'Testing456',
            "description" : "Test"
        }
        response = self.client.put(
            reverse('update_todo_detail', kwargs={'user_pk': self.user.email, 'todo_pk':self.todo.code}),
            changed_todo, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_todo(self):
        response = self.client.delete(
            reverse('delete_todo_detail', kwargs={'user_pk': self.user.email, 'todo_pk':self.todo.code}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)