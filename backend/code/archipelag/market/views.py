from archipelag.market.settings import POINTS_RULES
from archipelag.market.models import Market
from archipelag.market.serializers import MarketSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response


class MarketList(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MarketSerializer

    def create(self, request):
        """
        Create new market if user has enough number of coins.

        :return information about reason why he can't
                create market or id of new market
        """
        market_fields = request.data['body']
        current_ngo = request.user.ngouser
        if not current_ngo.is_user_can_add_market():
            return Response(dict(error="Za mało punktów."))
        if not is_fields_are_valid(market_fields):
            return Response(dict(error="Błędne wartość pól."))
        current_ngo.subtract_coins(POINTS_RULES['add_own_market'])
        new_market = get_new_market(current_ngo, market_fields)
        return Response(dict(success={'market_id': new_market.id}))


def is_fields_are_valid(market_fields):
    form = MarketSerializer(data=market_fields)
    print(form.is_valid(raise_exception=True))
    return form.is_valid(raise_exception=True)


def get_new_market(current_ngo, body_data):
    """Create market and return."""
    new_market = Market.objects.create(
        owner=current_ngo,
        title=body_data["title"],
        date_starting=body_data["date_starting"],
        date_ending=body_data["date_ending"],
        hashtag=body_data["hashtag"]
    )
    return new_market

