from uuid import UUID
from rest_framework.exceptions import ValidationError

from archipelag.market.serializers import MarketSerializer
from archipelag.app.utils import get_proper_format_for_valid_exception
from archipelag.market.models import Market
from archipelag.market.models import Image
from archipelag.market.serializers import MarketSerializer
from archipelag.market.serializers import MarketImageSerializer


class CreateMarketValidator(object):
    @classmethod
    def get_error(cls, current_ngo, market_fields):
        try:
            cls.user_validate(current_ngo, market_fields)
            cls.market_validate(market_fields)
        except ValidationError as error:
            error = get_proper_format_for_valid_exception(error)
            return error

    @classmethod
    def user_validate(cls, current_ngo, market_fields):
        if not current_ngo.is_user_can_add_market():
            raise ValidationError("Za mało punktów.")
        return cls.market_validate(market_fields)

    @classmethod
    def market_validate(cls, market_fields):
        form = MarketSerializer(data=market_fields)
        for key in market_fields.keys():
            if key not in ["title", "date_starting", "date_ending", "hashtag", "owner"]:
                raise ValidationError("Nieznane pole marketu: {}".format(key))
        return form.is_valid(raise_exception=True)


class GetImagesListValidator(object):
    @classmethod
    def get_error(cls, market_id):
        if market_id is None:
            return ("Brakuje marketu dla którego można by pobrać obrazki", 422)
        elif not cls.validate_uuid4(market_id):
            return ("Niepoprawny format uuid marketu", 422)
        market_that_request_concern = Market.objects.filter(id=market_id).first()
        if market_that_request_concern is None:
            return ("Zapytanie prosi o obrazki do nieznanego marketu", 404)
        return (None, None)

    @classmethod
    def validate_uuid4(cls, uuid_string):
        """
        Validate that a UUID string is in fact a valid uuid4.
        """
        try:
            UUID(uuid_string, version=4)
        except (ValueError, AttributeError) as error:
            return False
        return True


class CreateImageValidator(object):
    @classmethod
    def validate_market(cls, market, image_name):
        if market is None:
            raise ValidationError("Prośba o dodanie obrazka do nieistniejącego marketu")
        number_of_market_images = Image.objects.filter(
            market=market).count()
        print("NUMBERS", number_of_market_images)
        if number_of_market_images > 3:
            error = "Nie przesłano {}. Market przekroczył maksymalną liczbę obrazków: {}.".format(image_name, number_of_market_images)
            raise ValidationError(error)
        return market

    @classmethod
    def validate_image(cls, image_fields):
        form = MarketImageSerializer(data=image_fields)
        return form.is_valid(raise_exception=True)