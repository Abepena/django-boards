from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve

from ..models import Board, Topic, Post
from ..forms import PostForm
from ..views import reply_topic

class ReplyTopicTestCase(TestCase):
    """
    Base Test for all other Test Cases with this page
    The setUp will persist through all other Tests that inherit from this
    """
    def setUp(self):
        self.board = Board.objects.create(name="Django", description="Django Board")
        self.username = 'john'
        self.password = 'django123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.topic = Topic.objects.create(subject="Test", board=self.board, starter=user)
        self.post = Post(message="Hello world!", topic=self.topic, created_by=user)
        self.url = reverse('reply_topic', kwargs={"board_pk": self.board.pk, "topic_pk": self.topic.pk})

class LoginRequiredReplyTopicTest(ReplyTopicTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')

class ReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_response_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_view_function(self):
        view = resolve('/boards/1/topics/1/reply/')
        self.assertEqual(view.func, reply_topic)
    
    def test_contains_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, PostForm) 

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_form_inputs(self):
        """
        form should have 2 inputs, 1 hidden csrf 1 message
        """
        self.assertContains(self.response, "<input", 1)
        self.assertContains(self.response, "<textarea", 1)


class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, data={"message":"Hello"})
    
    def test_redirection(self):
        url = reverse('topic_posts', kwargs={
            "board_pk": self.board.pk,
            "topic_pk": self.topic.pk
        })
        topic_posts_url= "{url}?page=1#2".format(url=url)
        self.assertRedirects(self.response, topic_posts_url)
    
    def test_reply_created(self):
        """
        total posts created should be 2, one in the setup of the ReplyTopicTestCase
        another in the data passed in within this TestCase
        """
        self.assertTrue(Post.objects.count(), 2)


class InvalidReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, data={})
    
    def test_response_status_code(self):
        """ 
        Invalid data should just show the reply_topic view again and not redirect
        """
        self.assertEqual(self.response.status_code, 200)
    
    def test_form_errors(self):
        form = self.response.context.get("form")
        self.assertTrue(form.errors)
