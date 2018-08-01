from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, board_topics
from .models import Board
# Create your tests here.


class HomeTests(TestCase):
    # test for a 200 status code response when requesting the home url
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # Test that Django returns the correct view function
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


class BoardTopicsTests(TestCase):
    # Set up a temp board
    def setUp(self):
        Board.objects.create(name='Django', description="Django Board")

    def test_board_topics_view_status_code(self):
        url = reverse('board_topics', kwargs={"pk":1})
        response = self.client.get(url)        
        self.assertEqual(response.status_code, 200)
    
    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={"pk":99})
        response = self.client.get(url)        
        self.assertEqual(response.status_code, 404)        

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1')
        self.assertEqual(view.func, board_topics)
