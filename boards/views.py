from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Board, Topic, Post
from .forms import BoardForm, NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import View, UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class BoardListView(ListView):
    model = Board
    context_object_name = "boards"
    template_name = 'home.html'

# Side by side refactored FBV to Generic CBV List view
# def home(request):
    # boards = Board.objects.all()
    # return render(request, "home.html", {"boards": boards})

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


class TopicsListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20 #adds paginator similar to FBV below

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(
            replies=Count('posts')-1
        )
        return queryset

    def get_context_data(self, **kwargs):
        """ 
        add board to context objects kwargs 
        with the ListView model specified as Topic and topics as the 
        context_object_name, the only thing passed into the context is `topics`

        This method passes another kwarg `board` to the context when rendering
        the page similar to the FBV so that the template will have all the 
        necessary variables to render the page as we intended.

        The code below will pass `board` to the context_data of the render func
        ex. render(request, 'topics.html', {"board": self.board, "topics": topics})
        """
        kwargs['board'] = self.board 
        return super().get_context_data(**kwargs)
    

    




#Side by side refactored FBV to Generic CBV ListView 
# def board_topics(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
#     page = request.GET.get('page', 1)

#     paginator = Paginator(queryset, 20)

#     try:
#         topics = paginator.page(page)
#     except PageNotAnInteger:
#         topics = paginator.page(1)
#     except EmptyPage:
#         topics = paginator.page(paginator.num_pages)
#     return render(request, "topics.html", {"board": board, "topics": topics})

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
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updates_at = timezone.now()
        return redirect('topic_posts', board_pk=post.topic.board.pk, topic_pk=post.topic.pk)