from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.views import (RegisterView)
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