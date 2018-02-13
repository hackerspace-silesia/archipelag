from rest_framework import serializers
from archipelag.market.models import Market


class MarketSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.organisation')

    class Meta:
        model = Market
        fields = ('id', 'owner', 'title', 'date_starting',
                  'date_ending', 'date_created', 'date_modified', 'hashtag')