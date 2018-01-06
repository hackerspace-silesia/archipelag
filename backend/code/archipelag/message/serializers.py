from rest_framework import serializers
from archipelag.message.models import Message
from archipelag.message.models import MessageType


class MessageSerializer(serializers.ModelSerializer):
    market = serializers.ReadOnlyField(source='market.id')
    type = serializers.ReadOnlyField(source='type.service')

    class Meta:
        model = Message
        fields = ('id', 'content', 'shared', 'market', 'type')


class MessageTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageType
        fields = ('id', 'service', 'count_hashtag', 'char_restriction')
