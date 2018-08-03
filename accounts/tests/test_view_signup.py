from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase
from ..views import signup
from ..forms import SignUpForm
# Create your tests here.

class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_response_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_signup_url_resolves_to_signup_view(self):
        view = resolve("/signup/")
        self.assertEqual(view.func, signup)
    
    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")
    
    def test_contains_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, UserCreationForm)

class SignUpSuccessTests(TestCase):
    def setUp(self):
        url = reverse("signup")
        data = {
            'username': 'johndoe',
            'password1': 'django123',
            'password2': 'django123',

        }
        self.response = self.client.post(url, data=data)
        self.home_url = reverse('home')
    
    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_redirection(self):
        """
        A request to any new page should return a 'user'
        context variable after a successful signup
        """
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidSignUpTests(TestCase):
    """
    An invalid form submission should give the form again
    """
    def setUp(self):
        url = reverse("signup")
        self.response = self.client.post(url, data={})

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code,200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
    
    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())

class SignUpFormTests(TestCase):
    def test_form_has_fields(self):
        """
        Can be changed later if the fields you want on your sign up form change.
        More so for awareness about breaking things when form change
        """
        form = SignUpForm()
        expected = ['username', 'email', 'password1','password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

        