from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Board
from ..views import BoardListView

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
        self.assertEquals(view.func_view_class, BoardListView)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse(
            'board_topics', kwargs={"pk": self.board.pk})
        self.assertContains(
            self.response, 'href="{0}"'.format(board_topics_url))

