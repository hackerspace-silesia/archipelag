from rest_framework import serializers
from archipelag.market.models import Market
from archipelag.market.models import Image


class MarketSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.organisation')
    title = serializers.CharField(max_length=120, required=True)
    date_starting = serializers.DateTimeField(required=False)
    date_ending = serializers.DateTimeField(required=False)
    date_created = serializers.DateTimeField(required=False)
    date_modified = serializers.DateTimeField(required=False)
    hashtag = serializers.CharField(max_length=15, required=False)

    class Meta:
        model = Market
        fields = ('id', 'owner', 'title', 'date_starting',
                  'date_ending', 'date_created', 'date_modified', 'hashtag')


class MarketImageSerializer(serializers.ModelSerializer):
    market_id = serializers.ReadOnlyField(source='market.id')

    class Meta:
        model = Image
        fields = ('market_id', 'image_path',)
