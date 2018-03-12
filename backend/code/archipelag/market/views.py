from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from archipelag.market.settings import POINTS_RULES
from archipelag.market.models import Market
from archipelag.market.models import Image
from archipelag.market.serializers import MarketSerializer
from archipelag.market.serializers import MarketImageSerializer
from archipelag.market.validators import CreateMarketValidator
from archipelag.market.validators import GetImagesListValidator
from archipelag.market.validators import CreateImageValidator
from archipelag.app.utils import get_proper_format_for_valid_exception


class MarketList(viewsets.ModelViewSet):
    queryset = Market.objects.order_by('-date_created')
    permission_classes = (IsAuthenticated, )
    serializer_class = MarketSerializer

    def create(self, request):
        """
        Create new market if user has enough number of coins.

        :return information about reason why he can't
                create market or id of new market
        """
        market_fields = request.data['body']
        current_ngo = request.user.ngouser
        errors = CreateMarketValidator.get_error(current_ngo, market_fields)
        if errors:
            return Response(dict(error=errors), status=400)
        new_market_id = self.create_market_with_user_pay(market_fields, current_ngo)
        return Response(dict(success={'market_id': new_market_id}))

    def create_market_with_user_pay(self, market_fields, current_ngo):
        market_fields["owner"] = current_ngo
        new_market = Market.objects.create(**market_fields)
        current_ngo.subtract_coins(POINTS_RULES['add_own_market'])
        return new_market.id


class UploadedImagesViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = MarketImageSerializer

    def list(self, request):
        market_id = request.query_params.get('market_id', None)
        error, error_status = GetImagesListValidator.get_error(market_id)
        if error:
            return Response(dict(error=error), status=error_status)
        queryset = Image.objects.filter(market=market_id)
        markets_list = MarketImageSerializer(queryset, many=True).data
        return Response(markets_list, status=200)

    def create(self, request):
        """
        Create new market if user has enough number of coins.

        :return information about reason why he can't
                create market or id of new market
        """
        market_id = request.data.get("market_id")
        fields = dict(
            image_path=request.FILES.get("file"),
            market_id=market_id)
        try:
            CreateImageValidator.validate_image(fields)
            market = Market.objects.filter(id=market_id).first()
            CreateImageValidator.validate_market(market)
        except ValidationError as error:
            error = get_proper_format_for_valid_exception(error)
            return Response(dict(error=error), status=400)
        Image.objects.create(
                image_path=fields["image_path"], market=market)
        return Response(dict(message="Przesłano poprawnie"))
