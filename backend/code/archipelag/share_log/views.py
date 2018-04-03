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
        return Response(serializer.data)

    def create(self, request, market_id=None):
        """To crete information about who and when share message."""
        current_ngo = request.user.ngouser
        message_id = market_id
        response = add_coins_for_share(current_ngo, message_id)
        return Response(response)


def add_coins_for_share(current_ngo , message_id):
    shared_message = Message.objects.filter(id=message_id).first()
    if shared_message.market.owner == current_ngo:
        return dict(error="Zachłanność jest niedozwolona. Nie możesz udostępniać swojego wydarzenia.")
    elif ShareLog.objects.filter(message=shared_message, owner=current_ngo).first():
        return dict(error="Wiadomość juz udostępniono wcześniej.")
    elif get_number_of_all_messages_for_market_where_is_current_shared(shared_message, current_ngo) > 3:
        coins = POINTS_RULES['share_more_than_three_messages_format']
    else:
        coins = POINTS_RULES['for_share']
    current_ngo.add_coins(coins)
    save_share_log(shared_message, current_ngo, coins)
    return dict(success="Dziękujemy za udostępnienie. Naliczone punkty: {}".format(coins))


def get_number_of_all_messages_for_market_where_is_current_shared(shared_message, current_ngo):
    current_market_messages = Message.objects.filter(market=shared_message.market, ).all()
    logs = []
    for message in current_market_messages:
        logs.append(ShareLog.objects.filter(message=message.id, owner=current_ngo))
    return len(list(chain(*logs)))


def save_share_log(msg, ngo, coins):
    log = ShareLog(message=msg, owner=ngo, coins=coins)
    log.save()
    return log
