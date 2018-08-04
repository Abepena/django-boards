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
    

class PasswordChangeDoneTests(TestCase):
    """
    Base Test for form processing
    accepts data dictionary to POST to the view
    """
    def setUp(self, data={}):
        self.user = User.objects.create_user(
            username='johndoe',
            email='john@doe.com',
            password='django123'
        )
        self.url = reverse('password_change')
        self.client.login(username='johndoe', password='django123')
        self.response = self.client.post(self.url, data)

class SuccessfulPasswordChangeTests(PasswordChangeDoneTests):
    def setUp(self):
        """
        Inherits the setUp of the Base Test above and adds a data dict
        """
        super().setUp(data={
            'old_password': 'django123',
            'new_password1': 'django124',
            'new_password2': 'django124',
        })
    
    def test_redirection(self):
        password_change_done_url = reverse('password_change_done')
        self.assertRedirects(self.response, password_change_done_url)
    
    def test_password_changed(self):
        """
        Refresh user instance from DB to get the new password hash updated
        in the setUp (the change password view)
        """
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('django124'))

    def test_user_authentication(self):
        """
        Create a new request to any page
        Response should now have a 'user' in its context, after a sign in
        """
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidPasswordChangeTests(PasswordChangeDoneTests):
    def test_status_code(self):
        """
        No change to setUP therefore data sent in request.client.post is empty
        The POST request with empty data should return the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
    
    def test_didnt_change_password(self):
        """
        Similar to the test_password_changed in the SuccessfulPasswordChangeTests
        except now check that the password remains the same as the old passoword
        ie. password should still be django123
        """
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('django123'))