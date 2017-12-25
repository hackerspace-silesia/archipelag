from rest_framework import serializers
from archipelag.event_log.models import EventLog


class EventLogSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.name')
    owner_id = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = EventLog
        fields = ('id', 'owner_name', 'owner_id', 'type', 'id_connected_object', 'date_created')
