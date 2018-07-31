from django.test import TestCase
from django.urls import reverse, resolve
from .views import home
# Create your tests here.


class HomeTests(TestCase):
    #test for a 200 status code response when requesting the home url
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    # Test that Django returns the correct view function
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)