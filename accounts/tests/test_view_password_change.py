from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


class PasswordChangeTests(TestCase):
    def setUp(self):
        username = "johndoe"
        email = 'john@doe.com'
        password = "django123"
        User.objects.create_user(username=username, email=email, password=password)
        url = reverse('password_change')
        self.client.login(username=username, password=password)
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_url_resolves_correct_view(self):
        view = resolve('/settings/password/')
        self.assertEqual(view.func.view_class, PasswordChangeView)
    
    def test_csrf(self):
        self.assertContains(self.response,"csrfmiddlewaretoken")
    
    def test_contains_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, PasswordChangeForm)
    
    def test_form_inputs(self):
        """
        PasswordChangeForm should result in 4 inputs,
        1. csrf
        2. old_password
        3. new_password1
        4. new_password2
        """
        self.assertContains(self.response, '<input',4)
        self.assertContains(self.response, 'type="password"', 3)

class LoginRequiredPasswordChangeTests(TestCase):
    def test_redirection(self):
        url = reverse('password_change')
        login_url = reverse('login')
        self.response = self.client.get(url)
        self.assertRedirects(self.response, f'{login_url}?next={url}')