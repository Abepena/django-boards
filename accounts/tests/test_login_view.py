from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

class LoginViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='johndoe',
            email='john@doe.com',
            password = 'django123',
        
        )
        url = reverse('login')
        self.response = self.client.get(url)
    
    def test_login_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_login_url_resolves_to_login_view(self):
        view = resolve('/login/')
        self.assertEqual(view.func.view_class, LoginView)
    
    def test_login_view_contains_link_to_signup_page(self):
        signup_url = reverse('signup')
        self.assertContains(self.response, 'href="{0}"'.format(signup_url))
    
    def test_login_view_contains_link_to_password_reset_page(self):
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))

class SuccessfulLoginTests(TestCase):
    def setUp(self):
        username = 'johndoe'
        email ='john@doe.com'
        password = 'django123'
        User.objects.create_user(
            username=username,
            email=email,
            password =password,
        
        )
        url = reverse('login')
        data = {"username": username, "password": password}
        self.response = self.client.post(url, data)
    
    def test_redirection(self):
        """
        correct username and password will redirect to the homepage
        """
        home_url = reverse('home')
        self.assertRedirects(self.response, home_url)

class InvalidLoginTests(TestCase):
    def setUp(self):
        username = 'johndoe'
        email ='john@doe.com'
        password = 'django123'
        User.objects.create_user(
            username=username,
            email=email,
            password =password,
        
        )
        url = reverse('login')
        data = {"username": 'wrongusername', "password": 'wrongpassword'}
        self.response = self.client.post(url, data)
    
    def test_invalid_username_and_password(self):
        """
        incorrect username and password will not redirect to the login page again but instead show the login page again
        """
        form = self.response.context.get('form')
        self.assertEqual(self.response.status_code, 200)
        self.assertIsInstance(form, AuthenticationForm)