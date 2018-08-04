from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.core import mail
from django.contrib.auth.models import User

class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/reset/')
        self.assertEqual(view.func.view_class, PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_contains_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        """
        response needs to contain 2 inputs, 1 of them of type email
        """
        self.assertContains(self.response, '<input', 2)        
        self.assertContains(self.response, 'type="email"', 1)

    
class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'fake@fakeemail.com'
        User.objects.create_user(username='johndoe', email=email, password='django123')
        url = reverse('password_reset')
        self.response = self.client.post(url, data={'email': email})

    def test_redirection(self):
        """
        correct and incorrect emails should redirect to the
        password_reset_done page
        """
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)
    
    def test_reset_email_sent(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, data={'email':'incorrect@email.com'})

    def test_redirection(self):
        """
        invalid emails should still redirect to password_reset_done page
        """
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_reset_email(self):
        """
        mail outbox should have 0 entries
        """
        self.assertEqual(0, len(mail.outbox)) 

    

    