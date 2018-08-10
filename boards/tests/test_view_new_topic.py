from django.contrib.auth.models import User 
from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Board, Topic, Post
from ..views import new_topic
from ..forms import NewTopicForm


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django Board')
        User.objects.create_user(username="john", email="johndoe@example.com", password="django123")
        self.client.login(username='john', password='django123')
    
    def test_new_topic_view_status_code(self):
        print(Board.objects.get(pk=1))
        url = reverse("new_topic", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

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
        url = reverse("new_topic", kwargs={"pk": 1})
        board_topics_url = reverse("board_topics", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))
    
    def test_new_topic_view_contains_link_to_home_page(self):
        home_url = reverse("home")
        response = self.client.get(home_url)
        self.assertContains(response, 'href="{0}"'.format(home_url))
    
    #make sure theres a csrf token on the page
    def test_csrf(self):
        url = reverse('new_topic', kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertContains(response, "csrfmiddlewaretoken")
    
    
    def test_new_topic_valid_post_data(self):
        """
        Test that posting invalid data with self.client.post 
        does not create a new topic and post 
        """        
        url = reverse("new_topic", kwargs={"pk": 1})
        data = {
            "subject": "Test Topic",
            "message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        }
        response = self.client.post(url, data=data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())


    def test_new_topic_invalid_post_data(self):
        """
        Invalid post data should not redirect
        The response should show the form again
        """
        url = reverse("new_topic", kwargs={"pk": 1})
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 200)


    def test_new_topic_invalid_post_data_empty_fields(self):
        """
        Invalid post data should not redirect
        The response should show the form again due to empty fields
        Topic and Post should not have been created
        """
        url = reverse("new_topic", kwargs={"pk": 1})
        data = {
            "subject": "",
            "message": "",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())
    
    def test_contains_form(self):
        url= reverse("new_topic", kwargs={"pk": 1})
        response = self.client.get(url)
        form = response.context.get("form")
        self.assertIsInstance(form, NewTopicForm)
    
    def test_new_topic_invalid_post_data(self):
        """
        Invalid Post data will not redirect
        Instead the form will be shown again
        """
        url = reverse("new_topic", kwargs={"pk": 1})
        response = self.client.post(url, data={})
        form = response.context.get("form")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)

class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name="Django Board", description="Django Board")
        self.url = reverse("new_topic", kwargs={"pk": 1})
        self.response = self.client.get(self.url)
    
    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, f'{login_url}?next={self.url}')

