from archipelag.event_log.models import EventLog
from archipelag.event_log.serializers import EventLogSerializer
from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from archipelag.message.models import Message
from rest_framework.response import Response
from itertools import chain


class ShareLogList(views.APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, shared_message, format=None):
        messages = Message.objects.filter(market=shared_message).all()
        logs = []
        for message in messages:
            logs.append(EventLog.objects.filter(type=type, id_connected_object=message.id).all())
        serializer = EventLogSerializer(list(chain(*logs)), many=True)
        return Response(serializer.data)
