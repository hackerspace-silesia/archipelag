from uuid import UUID

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from datetime import datetime

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
        errors = self.validate_create(current_ngo, market_fields)
        if errors:
            return Response(dict(error=errors), status=400)
        new_market_id = self.create_market_with_user_pay(market_fields, current_ngo)
        return Response(dict(success={'market_id': new_market_id}))

    def create_market_with_user_pay(self, market_fields, current_ngo):
        market_fields["owner"] = current_ngo
        new_market = Market.objects.create(**market_fields)
        current_ngo.subtract_coins(POINTS_RULES['add_own_market'])
        return new_market.id

    def validate_create(self, current_ngo, market_fields):
        try:
            self.user_validate(current_ngo, market_fields)
            self.validate_market(market_fields)
        except ValidationError as error:
            error = get_proper_format_for_valid_exception(error)
            return error

    def user_validate(self, current_ngo, market_fields):
        if not current_ngo.is_user_can_add_market():
            raise ValidationError("Za mało punktów.")
        return self.validate_market(market_fields)

    def validate_market(self, market_fields):
        form = MarketSerializer(data=market_fields)
        for key in market_fields.keys():
            if key not in ["title", "date_starting", "date_ending", "hashtag"]:
                raise ValidationError("Nieznane pole marketu: {}".format(key))
        return form.is_valid(raise_exception=True)


class UploadedImagesViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = MarketImageSerializer

    def list(self, request):
        market_id = request.query_params.get('market_id', None)
        errors = self.get_validation_error(market_id)
        if errors:
            return errors
        queryset = Image.objects.filter(market=market_id)
        markets_list = MarketImageSerializer(queryset, many=True).data
        return Response(markets_list, status=200)

    def get_validation_error(self, market_id):
        if market_id is None:
            return Response(dict(error="Brakuje marketu dla którego można by pobrać obrazki"), status=422)
        elif not self.validate_uuid4(market_id):
            return Response(dict(error="Niepoprawny format uuid marketu"), status=422)
        market_that_request_concern = Market.objects.filter(id=market_id).first()
        if market_that_request_concern is None:
            return Response(dict(error="Zapytanie prosi o obrazki do nieznanego marketu"), status=404)
        return None

    def validate_uuid4(self, uuid_string):
        """
        Validate that a UUID string is in fact a valid uuid4.
        """
        try:
            UUID(uuid_string, version=4)
        except (ValueError, AttributeError) as error:
            return False
        return True

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
        if number_of_market_images > 3:
            error = "Do marketu już dodano {} obrazki.".format(number_of_market_images)
            raise ValidationError(error)

    def validate_image(self, image_fields):
        form = MarketImageSerializer(data=image_fields)
        return form.is_valid(raise_exception=True)
