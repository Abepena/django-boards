from django.test import TestCase
from django.urls import resolve, reverse
from .views import signup
# Create your tests here.

class SignUpTests(TestCase):
    def test_signup_response_status_code(self):
        url = reverse("signup")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_signup_url_resolves_to_signup_view(self):
        view = resolve("/signup/")
        self.assertEqual(view.func, signup)
