from archipelag.share_log.models import ShareLog
from archipelag.share_log.serializers import ShareLogSerializer
from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from archipelag.message.models import Message
from rest_framework.response import Response
from itertools import chain


class ShareLogList(views.APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, market_id, format=None):
        messages = Message.objects.filter(market=market_id).all()
        logs = []
        for message in messages:
            logs.append(ShareLog.objects.filter(message=message.id))
        serializer = ShareLogSerializer(list(chain(*logs)), many=True)
        return Response(serializer.data)
