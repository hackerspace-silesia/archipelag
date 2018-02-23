from archipelag.market.settings import POINTS_RULES
from archipelag.market.models import Market
from archipelag.market.models import Image
from archipelag.market.serializers import MarketSerializer
from archipelag.market.serializers import MarketImageSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidatorException
from uuid import UUID


class MarketList(viewsets.ModelViewSet):
    queryset = Market.objects.order_by('-date_created')
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
        errors = self.get_errors_during_validate(current_ngo, market_fields)
        if errors is not None:
           return errors
        try:
            new_market = self.get_new_market(current_ngo, market_fields)
        except TypeError as error:
            return Response(dict(error=str(error)))
        current_ngo.subtract_coins(POINTS_RULES['add_own_market'])
        return Response(dict(success={'market_id': new_market.id}))

    def get_errors_during_validate(self, current_ngo, market_fields):
        if not current_ngo.is_user_can_add_market():
            return Response(dict(error="Za mało punktów."))
        try:
            self.validate_market(market_fields)
        except ValidationError as error:
            return Response(dict(error=error.detail))
        return None

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
    permission_classes = (IsAuthenticated,)
    serializer_class = MarketImageSerializer

    def create(self, request):
        """
        Create new market if user has enough number of coins.

        :return information about reason why he can't
                create market or id of new market
        """
        image_fields = request.data
        fields = dict(image_path=request.FILES.get("file"),
                      market_id=image_fields.get("market_id"))
        try:
            self.validate_image(fields)
        except ValidationError as error:
            return Response(dict(error=error.detail))
        newest_market = Market.objects.filter(id=fields["market_id"]).first()
        if newest_market is None:
            return Response(dict(error="Prośba o dodanie obrazka do nieistniejącego marketu"))
        number_of_market_images = Image.objects.filter(market=newest_market).count()
        if number_of_market_images <= 3:
            Image.objects.create(
                image_path=fields["image_path"],
                market=newest_market
            )
            return Response(dict(success="Przesłano poprawnie"))
        return Response(dict(error="Do marketu już dodano {} obrazki.".format(number_of_market_images)))

    def validate_image(self, image_fields):
        market_id=image_fields.get("market_id")
        try:
            if market_id:
                UUID(market_id, version=4)
        except (ValueError, AttributeError) as error:
            raise ValidationError(dict(market_id=error))
        form = MarketImageSerializer(data=image_fields)
        return form.is_valid(raise_exception=True)
