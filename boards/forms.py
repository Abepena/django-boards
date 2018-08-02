from django import forms
from .models import Topic

class NewTopicForm(forms.ModelForm):
    """
    This will eventually replace the naive implementation of the
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
