from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from ..models import Board, Topic, Post
from ..views import PostUpdateView
from ..forms import PostForm

class PostUpdateViewTestCase(TestCase):
    """
    Base Test case to be used in a ll 'PostUpdateView' tests
    """
    def setUp(self):
        self.board = Board.objects.create(name="Django", description="Django Board")
        self.username = "john"
        self.password = 'django123'
        user = User.objects.create_user(username=self.username, email='john@doe.com',password=self.password)
        self.topic = Topic.objects.create(subject="Test Topic", board=self.board, starter=user)
        self.post = Post.objects.create(message="Testing 1,2,3...", topic=self.topic, created_by=user)
        self.url = reverse('edit_post', kwargs={
            "board_pk": self.board.pk,
            "topic_pk": self.topic.pk,
            "post_pk": self.post.pk,
        })

class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
    def test_redirection(self):
        """
        Test if only logged in users can reach the edit_posts url
        """
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')
    
class UnauthorizedPostUpdateViewTests(PostUpdateViewTestCase):
    """
    create a new user different from the one who originally posted and try to edit
    """

    def setUp(self):
        super().setUp()
        username = "jane"
        password = "django123"
        user = User.objects.create_user(username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        """
        posts should only be editable by the owner
        other users should get a 404 response
        """
        self.assertEquals(self.response.status_code, 404)

class PostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_response_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_view_function(self):
        view = resolve('/boards/1/topics/1/posts/1/edit/')
        self.assertEqual(view.func.view_class, PostUpdateView)
    
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


class SuccessfulPostUpdateViewTests(PostUpdateViewTestCase):
    # Same or very similar to ReplyTopic tests, left out for brevity
    pass

class InvalidPostUpdateViewTests(PostUpdateViewTestCase):
    # Same or very similar to ReplyTopic tests, left out for brevity
    pass

