from archipelag.message.models import Message
from archipelag.message.models import MessageType
from archipelag.message.serializers import MessageSerializer
from archipelag.message.serializers import MessageTypesSerializer
from archipelag.market.models import Market
from archipelag.event_log.models import SHARE

#from archipelag.notification.tasks import send_notification_for_event

from archipelag.event_log.models import EventLog
from archipelag.market.settings import POINTS_RULES
from archipelag.ngo.models import NgoUser

from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.response import Response


class MessagesList(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Message.objects.all()
        market_id = self.request.query_params.get('market_id', None)
        if market_id is not None:
            queryset = queryset.filter(market=market_id)
        return queryset

    def create(self, request):
        data = request.data['body']
        try:
            market = Market.objects.get(id=data['market'])
            message_type = MessageType.objects.get(id=data['type'])
        except Exception as ex:
            print(ex)
            return Response(dict(error='Problem z integralnością danych. Skontaktuj się z administratorem.'))
        try:
            Message.objects.create(market=market, type=message_type, content=data['content'])
        except Exception as ex:
            print(ex)
            return Response(dict(error="Błąd z bazą danych. Skontaktuj się z administratorem."))
        add_coins_if_rules_allow(request.user.ngouser, data['market'])
        return Response(dict(success="Dodano wiadomość"))


class MessagesTypesList(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageTypesSerializer
    queryset = MessageType.objects.all()


def get_statement_for_user(msg_market):
    service_name = msg_market.type.service
    return "Twoja wiadomość na {} została dodana, dodaj wiadomości na inne platformy".format(service_name)

def add_coins_if_rules_allow(ngo, market_id):
    messages = Message.objects.filter(market_id=market_id).count()
    if messages > 3:
        coins_to_add = POINTS_RULES['create_more_than_three_messages_format']
        ngo_model = NgoUser()
        ngo_model.add_coins(ngo, coins_to_add)


def add_coins_for_share(request, message_id):
    message = Message.objects.filter(id=message_id).first()
    current_ngo = request.user.ngouser
    save_log(message.id, current_ngo)
    current_ngo.add_coins(current_ngo, POINTS_RULES['for_share'])
    current_ngo.save()
    return redirect('market_details', market_id=message.market.id)


def save_log(msg_id, ngo):
    log = EventLog(type=SHARE, id_connected_object=msg_id, owner=ngo)
    log.save()
