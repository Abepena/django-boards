from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Board
# Create your views here.


def home(request):
    boards = Board.objects.all()
    return render(request, "home.html", {"boards": boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, "topics.html", {"board": board})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    
    # naive implementation of view 
    # not taking into account empty fields or subjects that are too large
    if request.method == "POST":
        subject = request.POST["subject"]
        message = request.POTS["message"]

        user = User.objects.first()  # TODO: get the currently logged in user

        topic = Topic.objects.create(
            subject=subject,
            board=board
            starter=user,  # TODO: get the currently logged in user
        )

        post = Post.objects.create(
            message=message,
            topic=topic
            created_by=user
        )

        return redirect("board_topics", pk=board.pk)

    return render(request, "new_topic.html", {"board": board})
