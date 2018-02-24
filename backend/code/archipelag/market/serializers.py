from rest_framework import serializers
from archipelag.market.models import Market
from archipelag.market.models import Image


class MarketSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.organisation')
    title = serializers.CharField(max_length=120, required=True, allow_null=False)
    date_starting = serializers.DateTimeField(required=False, allow_null=True)
    date_ending = serializers.DateTimeField(required=False, allow_null=True)
    date_created = serializers.DateTimeField(required=False, allow_null=True)
    date_modified = serializers.DateTimeField(required=False, allow_null=True)
    hashtag = serializers.CharField(max_length=15, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Market
        fields = ('id', 'owner', 'title', 'date_starting',
                  'date_ending', 'date_created', 'date_modified', 'hashtag')


class MarketImageSerializer(serializers.ModelSerializer):
    market_id = serializers.UUIDField(source='market.id', required=True)
    image_path = serializers.ImageField(required=True)

    class Meta:
        model = Image
        fields = ('market_id', 'image_path',)
