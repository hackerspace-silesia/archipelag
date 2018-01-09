from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from itertools import chain

from archipelag.share_log.models import ShareLog
from archipelag.share_log.serializers import ShareLogSerializer
from archipelag.market.settings import POINTS_RULES
from archipelag.message.models import Message


class ShareLogList(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get_list(self, request, market_id, *args, **kwargs):
        # market_id = self.kwargs['market_id']
        messages = Message.objects.filter(market=market_id).all()
        logs = []
        for message in messages:
            logs.append(ShareLog.objects.filter(message=message.id))
        serializer = ShareLogSerializer(list(chain(*logs)), many=True)
        print(serializer.data)
        return Response(serializer.data)

    def create(self, request, market_id=None):
        """To crete information about who and when share message."""
        current_ngo = request.user.ngouser
        message_id = market_id
        add_coins_for_share(current_ngo, message_id)
        return Response(dict(success="Dodano wiadomość"))


def add_coins_for_share(current_ngo , message_id):
    message = Message.objects.filter(id=message_id).first()
    save_log(message, current_ngo)
    if ShareLog.objects.filter(message=message, owner=current_ngo).count() > 3:
        current_ngo.add_coins(POINTS_RULES['share_more_than_three_messages_format'])
    else:
        current_ngo.add_coins(POINTS_RULES['for_share'])


def save_log(msg, ngo):
    log = ShareLog(message=msg, owner=ngo)
    log.save()
    return log
