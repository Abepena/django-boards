from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown
import math
# Create your models here.


class Board(models.Model):
    # unique = True enforces uniqueness at the database level
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()
    
    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by("-created_at").first()
    
    def get_topics_count(self):
        return Topic.objects.filter(board=self).count()


class Topic(models.Model):
    """
    Topics should be instantiated with  

    - attr:subject
    - attr:board (foreign key --> Board)
    - attr:starter (foreign key --> User)  

    Model for Topic instance within a board
    related_name is optional, Django will auto-generate the related name as
    <class_name>_set if nothing is specified
    ex. Topic --> related_name = topic_set by default unless otherwise specified
    """
    subject = models.CharField(max_length=255)

    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="topics")
    starter = models.ForeignKey(User, on_delete=models.CASCADE,related_name="topics")
    views = models.PositiveIntegerField(default=0)
    
    
    def __str__(self):
        return self.subject

    
    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)
    
    
    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        # arbitrary number representing many pages
        return count > 6
    
    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)





class Post(models.Model):
    """
    Model for Post instance within a Topic should be instantiated with at least  

    - attr: message
    - attr: topic (foreign key --> Topic)
    - attr: created_by (foreign_key --> User) 
    
    The updated_by attribute has a related_name of '+', this just tells Django 
    that we dont need this reverse relationship so it will ignore it

    ex. created_by relationship is needed
        updated_by relationship isnt necessary information for us to display
    """
    message = models.CharField(max_length=4000)
    # auto_now_add ensures that when a post is created the created datetime is now
    created_at = models.DateTimeField(auto_now_add=True)
    # null = True initializes the post with no updated_at attr populated yet
    updated_at = models.DateField(null=True)
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="posts")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    updated_by = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="+")
    
    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
    
    def created_at_pretty(self):
        return self.created_at.strftime("%D, %r")

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))