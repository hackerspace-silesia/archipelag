from archipelag.market.settings import POINTS_RULES
from archipelag.market.models import Market
from archipelag.market.models import Image
from archipelag.market.serializers import MarketSerializer
from archipelag.market.serializers import MarketImageSerializer

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


class UploadedImagesViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MarketImageSerializer

    def create(self, request):
        """
        Create new market if user has enough number of coins.

        :return information about reason why he can't
                create market or id of new market
        """
        image_fields = request.data
        market_id = image_fields.get("market_id")
        newest_market = Market.objects.filter(id=market_id).first()
        if newest_market is None:
            return Response(dict(error="Prośba o dodanie obrazka do nieistniejącego marketu"))
        number_of_market_images = Image.objects.filter(market=newest_market).count()
        if number_of_market_images <= 3:
            Image.objects.create(
                image_path=request.FILES["file"],
                market=newest_market
            )
            return Response(dict(success="Przesłano poprawnie"))
        new_number_of_market_images = Image.objects.filter(market=newest_market).count()
        return Response(dict(error="Do marketu już dodano {} obrazków.".format(new_number_of_market_images)))
