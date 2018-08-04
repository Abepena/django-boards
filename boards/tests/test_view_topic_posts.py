from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Board, Topic, Post
from ..views import topic_posts

class 