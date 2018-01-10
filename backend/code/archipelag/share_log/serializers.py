from rest_framework import serializers
from archipelag.share_log.models import ShareLog


class ShareLogSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.name')
    owner_id = serializers.ReadOnlyField(source='owner.id')
    message = serializers.ReadOnlyField(source='message.type.service')

    class Meta:
        model = ShareLog
        fields = ('id', 'owner_name', 'owner_id', 'message', 'date_created', 'coins')
