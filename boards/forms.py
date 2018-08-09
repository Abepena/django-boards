from django import forms
from .models import Board, Topic, Post

class BoardForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter the name of your new board"}),
        max_length=50,
        help_text="Max length: 50"
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={"placholder": "Brief description of your board"}),
        max_length=80,
    )

    class Meta:
        model = Board
        fields = ["name", "description"]

class NewTopicForm(forms.ModelForm):
    """
    This will replaces the naive implementation of the
    new_topic form using the Django Forms API
    """
    # message to be cleaned and later passed into a Post object
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "Message to start the topic off",
            }
        ),
        max_length=4000,
        help_text="The max length of this box is 4000",
    )

    class Meta:
        model = Topic
        # The subject field refers to the subject field in the Topic 
        # model and message will refer to the message later cleaned and created in a Post object
        fields = ['subject', 'message']

class PostForm(forms.ModelForm):
    message = forms.CharField(
        widget = forms.Textarea(
            attrs={"rows": 5,"placeholder": "Reply Message"}
        ),
        help_text="max length: 4000 characters"
    )
    class Meta:
        model = Post
        fields = ['message', ]
