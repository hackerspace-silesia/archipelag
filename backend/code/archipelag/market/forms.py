from django.forms import ModelForm
from django.forms import DateTimeInput

from archipelag.market.models import Market


class MarketForm(ModelForm):

    class Meta:
        model = Market
        exclude = ["owner"]
        fields = [
            'title',
            'description',
            'date_starting',
            'date_ending',
            'hashtag',
        ]

    def __init__(self, *args, **kwargs):
        super(MarketForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['hashtag'].required = False
