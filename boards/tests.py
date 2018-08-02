from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, board_topics, new_topic
from pprint import pprint
from .models import Board
# Create your tests here.


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(
            name='Django', description="Django Board")
        url = reverse('home')
        self.response = self.client.get(url)
        # print(pprint(self.response.content.decode("utf-8"))) << logs html page to console

    # test for a 200 status code response when requesting the home url
    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    # Test that Django returns the correct view function
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse(
            'board_topics', kwargs={"pk": self.board.pk})
        self.assertContains(
            self.response, 'href="{0}"'.format(board_topics_url))


class BoardTopicsTests(TestCase):
    # Set up a temp board, and a response that can be reached from other methods
    def setUp(self):
        self.board = Board.objects.create(
            name='Django', description="Django Board")
        url = reverse("board_topics", kwargs={"pk": self.board.pk})
        self.response = self.client.get(url)

    # ensure status code 200 after looking for the topic of pk=1 
    # (setUp in the previous method)
    def test_board_topics_view_status_code(self):
        url = reverse('board_topics', kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # ensure the board topic page for pk = 99 returns a 404 page
    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={"pk": 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # ensures that typing '/boards/1' after domain will resolve to the 
    # board_topics function in boards/views.py
    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEqual(view.func, board_topics)

    # ensures the topics page has a link back to the homepage
    def test_board_topics_view_contains_navigation_links(self):
        home_page_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={"pk": self.board.pk})

        self.assertContains(self.response, 'href="{0}"'.format(home_page_url))
        self.assertContains(self.response, 'href="{0}"'.format(new_topic_url))

class NewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="Django", description="Django Board")
        url = reverse("new_topic", kwargs={"pk": self.board.pk})
        self.response = self.client.get(url)
    
    def test_new_topic_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    # ensure the new_topic page for pk = 99 returns a 404 page
    def test_new_topic_view_not_found_status_code(self):
        url = reverse("new_topic", kwargs={"pk": 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    # ensures that typing '/boards/1/new' after domain will resolve to the 
    # new_topic function in boards/views.py
    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEqual(view.func, new_topic)

    # ensures the topics page has a link back to the homepage
    def test_new_topic_view_contains_link_to_board_topics(self):
        board_topics_url = reverse("board_topics", kwargs={"pk": self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))
    
    def test_new_topic_view_contains_link_to_home_page(self):
        home_url = reverse("home")
        self.assertContains(self.response, 'href="{0}"'.format(home_url))
