from django.contrib import auth
from django.contrib.messages import get_messages
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.form import RegisterCustomerForm
from accounts.views import (RegisterView, authenticate_user_and_login, login)
from django.test import Client

class TestRegisterView(TestCase):
    def setUp(self):
        # Define self.factory
        self.factory = RequestFactory()
        self.client = Client()
        self.client.login(username='test', password='testpassword')
        self.user = get_user_model().objects.create_user(
            username='test',
            email='test@email.com',
            password='testpassword'
        )
        self.view = RegisterView()

        # Creates a mock request instance
        self.view.request = self.factory.get('/')
        self.view.request.user = self.user

    def test_form_invalid(self):
        form_data = {}
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'testymctestface@email.com',
            'password1': 'Testpassword1',
            'password2': 'Testpassword1',
        }

        response = self.client.post(reverse('register'), data=form_data)

        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Registration successful')


class LoginTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='Testpassword1'
        )
        self.client.login(username='testuser', password='Testpassword1')

    def test_login_get(self):
        request = self.factory.get(reverse('login'))
        request.user = self.user
        response = login(request)
        self.assertEqual(response.status_code, 200)

    def test_authenticate_user_and_login_invalid(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'testuser', 'password': 'wrong'}
        )
        self.assertEqual(response.status_code, 200)
        messages = list(map(str, get_messages(response.wsgi_request)))
        self.assertIn('Invalid email or password.', messages)

    def test_authenticate_user_and_login_valid(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'testuser', 'password': 'Testpassword1'}
        )
        self.assertEqual(response.status_code, 302)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)