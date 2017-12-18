from django.forms import ModelForm
from django.forms import DateTimeInput

from archipelag.market.models import Market
from archipelag.market.models import Image


class MarketForm(ModelForm):

    class Meta:
        model = Market
        exclude = ["owner"]
        fields = [
            'title',
            'url',
            'date_starting',
            'date_ending',
            'hashtag',
        ]

    def __init__(self, *args, **kwargs):
        super(MarketForm, self).__init__(*args, **kwargs)
        self.fields['url'].required = False
        self.fields['hashtag'].required = False


class PhotoForm(ModelForm):
    exclude = ["market"]
    class Meta:
        model = Image
        fields = ('image', )