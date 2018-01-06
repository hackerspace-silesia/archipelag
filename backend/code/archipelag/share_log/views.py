from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from itertools import chain

from archipelag.share_log.models import ShareLog
from archipelag.share_log.serializers import ShareLogSerializer
from archipelag.market.settings import POINTS_RULES
from archipelag.message.models import Message




class ShareLogList(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, market_id, format=None):
        messages = Message.objects.filter(market=market_id).all()
        logs = []
        for message in messages:
            logs.append(ShareLog.objects.filter(message=message.id))
        serializer = ShareLogSerializer(list(chain(*logs)), many=True)
        return Response(serializer.data)

    def create(self, request):
        current_ngo = request.user.ngouser
        print(request.market_id)
        print(request)
        return Response(dict(success="Dodano wiadomość"))

def add_coins_for_share(request, message_id):
    message = Message.objects.filter(id=message_id).first()
    current_ngo = request.user.ngouser
    save_log(message.id, current_ngo)
    current_ngo.add_coins(current_ngo, POINTS_RULES['for_share'])
    current_ngo.save()


def save_log(msg_id, ngo):
    log = ShareLog(message=msg_id, owner=ngo)
    log.save()
