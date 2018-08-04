from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Board(models.Model):
    # unique = True enforces uniqueness at the database level
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="topics")
    starter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="topics")


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
    created_at = models.DateTimeField(auto_now=True)
    # null = True initializes the post with no updated_at attr populated yet
    updated_at = models.DateField(null=True)
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="posts")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    updated_by = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="+")
