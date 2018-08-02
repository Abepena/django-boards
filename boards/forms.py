from django import forms
from .models import Topic

class NewTopicForm(forms.ModelForm):
    """
    This will eventually replace the naive implementation of the
    new_topic form using the Django Forms API
    """
    message = forms.CharField(widget=forms.Textarea, max_length=4000)

    class Meta:
        model = Topic
        # The subject field refers to the subject field in the Topic 
        # model and message will refer to the message in Post model
        fields = ['subject', 'message']
