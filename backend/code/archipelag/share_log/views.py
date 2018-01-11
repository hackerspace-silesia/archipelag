from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from itertools import chain

from archipelag.share_log.models import ShareLog
from archipelag.share_log.serializers import ShareLogSerializer
from archipelag.market.settings import POINTS_RULES
from archipelag.message.models import Message
from archipelag.message.models import MessageType


class ShareLogList(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get_list(self, request, market_id, *args, **kwargs):
        # market_id = self.kwargs['market_id']
        messages = Message.objects.filter(market=market_id).all()
        logs = []
        for message in messages:
            logs.append(ShareLog.objects.filter(message=message.id))
        serializer = ShareLogSerializer(list(chain(*logs)), many=True)
        return Response(serializer.data)

    def create(self, request, market_id=None):
        """To crete information about who and when share message."""
        current_ngo = request.user.ngouser
        message_id = market_id
        response = add_coins_for_share(current_ngo, message_id)
        return Response(response)


def add_coins_for_share(current_ngo , message_id):
    shared_message = Message.objects.filter(id=message_id).first()
    if ShareLog.objects.filter(message=shared_message).first():
        return dict(error="Wiadomość juz udostępniono wcześniej.")
    if shared_message.type.service == 'Facebook' or shared_message.type.service == 'Instagram' or shared_message.type.service == 'Twitter':
        coins = POINTS_RULES['share_for_fb_twitter_insta']
    else:
        coins = POINTS_RULES['for_share']
    current_ngo.add_coins(coins)
    save_log(shared_message, current_ngo, coins)
    return dict(success="Dziękujemy za udostępnienie. Naliczone punkty: {}".format(coins))


def save_log(msg, ngo, coins):
    log = ShareLog(message=msg, owner=ngo, coins=coins)
    log.save()
    return log
