from rest_framework import viewsets
from rest_framework.response import Response
from django.db import IntegrityError
from django.db import transaction

from archipelag.market.settings import POINTS_RULES
from archipelag.ngo.models import NgoUser
from archipelag.ngo.models import User
from archipelag.ngo.serializers import NgoUserSerializerForList
from archipelag.ngo.serializers import NgoUserSerializer


class NgoUserList(viewsets.ModelViewSet):
    queryset = NgoUser.objects.all()
    permission_classes = ()
    serializer_class = NgoUserSerializerForList

    def create(self, request):
        """
        Create new market if user has enough number of coins.

        :return information about reason why he can't
                create market or id of new market
        """
        market_fields = request.data
        add_to_recommendator_coins(market_fields["ngo"])
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=market_fields["username"],
                    password=market_fields["password"],
                    email=market_fields["email"],
                )
                NgoUser.objects.create(
                    user=user,
                    organisation=market_fields["organisation"])
        except AttributeError as e:
            print("Attribute error ".format(e))
            return Response(dict(error="Błąd wewnętrzny."))
        except IntegrityError as e:
            error_msg = e.args[0]
            if "auth_user_username_key" in error_msg:
                return Response(dict(error="Nickame już istnieje."))
            elif "ngo_ngouser_name" in error_msg:
                return Response(dict(error="Organizacja już istnieje."))
        if not is_fields_are_valid(market_fields):
            return Response(dict(error="Błędne wartość pól."))
        return Response(dict(success={'market_id': 'created'}))


def is_fields_are_valid(market_fields):
    form = NgoUserSerializer(data=market_fields)
    return form.is_valid(raise_exception=True)


def add_to_recommendator_coins(name):
    recomendator = NgoUser.objects.filter(organisation=name).first()
    if recomendator:
        recomendator.add_coins(POINTS_RULES["recommend_app"])
        return True
    return False


def get_new_market(current_ngo, body_data):
    """Create market and return."""
    new_market = NgoUser.objects.create(
        owner=current_ngo,
        title=body_data["title"],
        date_starting=body_data["date_starting"],
        date_ending=body_data["date_ending"],
        hashtag=body_data["hashtag"]
    )
    return new_market