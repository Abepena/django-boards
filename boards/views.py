from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Board, Topic, Post
from .forms import BoardForm, NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import View, UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
# Create your views here.


def home(request):
    boards = Board.objects.all()
    return render(request, "home.html", {"boards": boards})

@login_required
def create_board(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.save()
            return redirect("board_topics", pk=board.pk)
    else:
        form = BoardForm()
    return render(request, "create_board.html", {"form": form})



def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, "topics.html", {"board": board, "topics": topics})

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    # Django Forms API implementation of the New Topic Form
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message = form.cleaned_data.get("message"),
                topic=topic,
                created_by=topic.starter,
            )

            return redirect("topic_posts", board_pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, "new_topic.html", {"board": board, "form": form})

def topic_posts(request, board_pk, topic_pk):
    #Note the double underscore for foreignkey pk's
    topic = get_object_or_404(Topic, board__pk=board_pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {"topic":topic})

@login_required
def reply_topic(request, board_pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=board_pk, pk=topic_pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect("topic_posts", board_pk=board_pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, "reply_topic.html", {"topic": topic, "form": form})

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = "post_pk"
    context_object_name = "post"
    template_name  = 'edit_post.html'

    """
    Override UpdateView's get_queryset method with filter applied 
    of the current user. If the current user logged in is not the one who 
    originally created the post, the Post queryset will come up empty
    """
    def get_queryset(self):
        queryset= super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updates_at = timezone.now()
        return redirect('topic_posts', board_pk=post.topic.board.pk, topic_pk=post.topic.pk)