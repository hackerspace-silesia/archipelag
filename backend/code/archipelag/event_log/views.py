from archipelag.event_log.models import EventLog
from archipelag.event_log.serializers import EventLogSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class EventLogList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventLogSerializer

    def get_queryset(self):
        """Get specific log for type and connected id."""
        type = self.kwargs['type']
        id_connected_object = self.kwargs['id_connected_object']
        return EventLog.objects.filter(type=type, id_connected_object=id_connected_object)