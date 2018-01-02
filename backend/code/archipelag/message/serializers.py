from rest_framework import serializers
from archipelag.message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    market = serializers.ReadOnlyField(source='market.id')
    type = serializers.ReadOnlyField(source='type.service')

    class Meta:
        model = Message
        fields = ('content', 'shared', 'market', 'type')