from rest_framework import serializers
from archipelag.event_log.models import EventLog


class EventLogSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.name')
    owner_id = serializers.ReadOnlyField(source='owner.id')
    message = serializers.ReadOnlyField(source='message.type.service')

    class Meta:
        model = EventLog
        fields = ('id', 'owner_name', 'owner_id', 'message', 'date_created',)
