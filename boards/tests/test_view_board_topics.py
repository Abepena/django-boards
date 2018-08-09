from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Board
from ..views import TopicsListView

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
        self.assertEqual(view.func.view_class, TopicsListView)

    # ensures the topics page has a link back to the homepage
    def test_board_topics_view_contains_navigation_links(self):
        home_page_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={"pk": self.board.pk})

        self.assertContains(self.response, 'href="{0}"'.format(home_page_url))
        self.assertContains(self.response, 'href="{0}"'.format(new_topic_url))

