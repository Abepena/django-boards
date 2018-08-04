from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase

class PasswordResetMailTests(TestCase):
    """
    Tests to check the emails sent through the command line
    """
    
    def setUp(self):
        username = 'johndoe'
        email = 'johndoe@test.com'
        password = 'django123'
        User.objects.create_user(username=username, email=email, password=password)
        url = reverse('password_reset')
        self.response = self.client.post(url, data={'email': email})
        self.email = mail.outbox[0]
    
    def test_email_subject(self):
        self.assertEqual('[Django Boards] Password Reset Link', self.email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm',kwargs={
            "uidb64": uid,
            "token": token,
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('johndoe', self.email.body)
        self.assertIn('johndoe@test.com', self.email.body)
    
    def test_email_to(self):
        self.assertEqual(['johndoe@test.com'], self.email.to)

        
        
