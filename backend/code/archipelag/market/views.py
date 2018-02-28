from uuid import UUID

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from archipelag.market.settings import POINTS_RULES
from archipelag.market.models import Market
from archipelag.market.models import Image
from archipelag.market.serializers import MarketSerializer
from archipelag.market.serializers import MarketImageSerializer
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
        try:
            self.validate(current_ngo, market_fields)
        except ValidationError as error:
            error = get_proper_format_for_valid_exception(error)
            return Response(dict(error=error), status=400)
        try:
            new_market = self.get_new_market(current_ngo, market_fields)
        except TypeError as error:
            return Response(dict(error=str(error)), status=400)
        current_ngo.subtract_coins(POINTS_RULES['add_own_market'])
        return Response(dict(success={'market_id': new_market.id}))

    def validate(self, current_ngo, market_fields):
        if not current_ngo.is_user_can_add_market():
            raise ValidationError("Za mało punktów.")
        return self.validate_market(market_fields)

    def validate_market(self, market_fields):
        form = MarketSerializer(data=market_fields)
        return form.is_valid(raise_exception=True)

    def get_new_market(self, current_ngo, body_data):
        """Create market and return."""
        body_data["owner"] = current_ngo
        new_market = Market.objects.create(**body_data)
        return new_market


class UploadedImagesViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = MarketImageSerializer

    def create(self, request):
        """
        Create new market if user has enough number of coins.

        :return information about reason why he can't
                create market or id of new market
        """
        image_fields = request.data
        fields = dict(
            image_path=request.FILES.get("file"),
            market_id=image_fields.get("market_id"))
        try:
            self.validate_image(fields)
            newest_market = Market.objects.filter(id=fields["market_id"]).first()
            self.validate_market(newest_market)
        except ValidationError as error:
            error = get_proper_format_for_valid_exception(error)
            return Response(dict(error=error), status=400)
        Image.objects.create(
                image_path=fields["image_path"], market=newest_market)
        return Response(dict(message="Przesłano poprawnie"))

    def validate_market(self, newest_market):
        if newest_market is None:
            raise ValidationError("Prośba o dodanie obrazka do nieistniejącego marketu")
        number_of_market_images = Image.objects.filter(
            market=newest_market).count()
        if number_of_market_images >= 3:
            error = "Do marketu już dodano {} obrazki.".format(number_of_market_images)
            raise ValidationError(error)

    def validate_image(self, image_fields):
        market_id = image_fields.get("market_id")
        try:
            if market_id:
                UUID(market_id, version=4)
        except (ValueError, AttributeError) as error:
            raise ValidationError(dict(market_id=error))
        form = MarketImageSerializer(data=image_fields)
        return form.is_valid(raise_exception=True)
