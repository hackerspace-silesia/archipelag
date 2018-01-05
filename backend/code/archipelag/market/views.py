from json import loads

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from archipelag.event_log.models import EventLog
from archipelag.market.settings import POINTS_RULES
from archipelag.market.models import Market
from archipelag.market.serializers import MarketSerializer
from archipelag.message.models import Message

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response


class MarketList(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MarketSerializer

    def create(self, request):
        market_fields = request.data['body']
        current_ngo = request.user.ngouser
        if not current_ngo.is_user_can_add_market():
            return Response(dict(error="Za mało punktów."))
        current_ngo.subtract_coins(POINTS_RULES['add_own_market'])
        new_market = get_new_market(current_ngo, market_fields)
        return Response(dict(success={'market_id': new_market.id}))

def is_fields_are_valid(market_fields):
    form = MarketSerializer(data=market_fields)
    return form.is_valid()


def get_new_market(current_ngo, body_data):
    new_market = Market.objects.create(
        owner=current_ngo,
        title=body_data["title"],
        description=body_data["description"],
        date_starting=body_data["date_starting"],
        date_ending=body_data["date_ending"],
        hashtag=body_data["hashtag"]
    )
    return new_market


def get_messages(request, market_id):

    market = Market.objects.filter(id=market_id)
    messages = Message.objects.filter(market=market_id).all()

    template_name = 'market/message_list.html'
    return render(
            request, template_name,
            {
                'messages': Message.objects.filter(market=market).all(),
                'logs_for_share': get_logs_iterator(messages)
            })


def get_logs_iterator(messages):
    for message in messages:
        logs = EventLog.objects.filter(id_connected_object=message.id).all()
        if not logs:
            break
        for log in logs:
            yield log.get_share_log()
