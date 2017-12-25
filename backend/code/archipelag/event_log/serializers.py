from rest_framework import serializers
from archipelag.event_log.models import EventLog


class EventLogSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.name')

    class Meta:
        model = EventLog
        fields = ('id', 'owner', 'type', 'id_connected_object', 'date_created')
