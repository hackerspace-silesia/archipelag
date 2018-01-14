from archipelag.message.models import Message
from archipelag.message.models import MessageType
from archipelag.message.serializers import MessageSerializer
from archipelag.message.serializers import MessageTypesSerializer
from archipelag.market.models import Market

#from archipelag.notification.tasks import send_notification_for_event

from archipelag.market.settings import POINTS_RULES
from archipelag.market.settings import NUMBER_OF_CREATED_MESSAGES_WHEN_USER_GET_COINS

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response


class MessagesList(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        Get messages filter by market_id
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
            new_message = Message.objects.create(market=market, type=message_type, content=data['content'])
        except Exception as ex:
            print(ex)
            return Response(dict(error="Błąd z bazą danych. Skontaktuj się z administratorem."))
        add_coins_if_rules_allow(request.user.ngouser, data['market'])
        return Response(dict(success=get_statement_for_user(new_message)))


class MessagesTypesList(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageTypesSerializer
    queryset = MessageType.objects.all()


def get_statement_for_user(msg_market):
    service_name = msg_market.type.service
    return "Twoja wiadomość na {} została dodana poprawnie.".format(service_name)


def add_coins_if_rules_allow(ngo, market_id):
    """Add coins to user if number of messages is bigger than defined number."""
    messages = Message.objects.filter(market_id=market_id).count()
    if messages >= NUMBER_OF_CREATED_MESSAGES_WHEN_USER_GET_COINS:
        coins_to_add = POINTS_RULES['create_more_than_three_messages_format']
        ngo.add_coins(coins_to_add)
