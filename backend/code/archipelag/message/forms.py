from django.forms import ModelForm

from archipelag.message.models import Message


class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = [
            'content',
            'type',]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['max_length'].required = False
        self.fields['hashtag'].required = False