from rest_framework import serializers
from archipelag.market.models import Market
from archipelag.market.models import Image


class MarketSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.organisation')

    class Meta:
        model = Market
        fields = ('id', 'owner', 'title', 'date_starting',
                  'date_ending', 'date_created', 'date_modified', 'hashtag')


class MarketImageSerializer(serializers.ModelSerializer):
    market_id = serializers.ReadOnlyField(source='market.id')

    class Meta:
        model = Image
        fields = ('market_id', 'image_path',)
