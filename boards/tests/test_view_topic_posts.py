from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Board, Topic, Post
from ..views import PostsListView

class TopicPostsViewTests(TestCase):
    def setUp(self):
        board = Board.objects.create(name="Django", description="Django Board")
        user = User.objects.create_user(username ='john', email='john@doe.com', password='django123')
        topic = Topic.objects.create(subject='Hello', board=board, starter=user)
        post = Post.objects.create(message="Hello, world", topic=topic, created_by=user)
        url = reverse("topic_posts", kwargs={"board_pk": board.pk, "topic_pk": topic.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_view_function(self):
        view = resolve('/boards/1/topics/1/')
        self.assertEqual(view.func.view_class, PostsListView)


    