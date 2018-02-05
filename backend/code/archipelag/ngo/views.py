from archipelag.ngo.models import NgoUser
from archipelag.ngo.serializers import NgoUserSerializerForList
from archipelag.ngo.serializers import NgoUserSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response


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
        roro = NgoUser.objects.create(username=market_fields["username"],
                                      password=market_fields["password"],
                                      email=market_fields["email"],
                                      name=market_fields["organisation"])
        print(roro)
        if not is_fields_are_valid(market_fields):
            return Response(dict(error="Błędne wartość pól."))
        print(market_fields)
        return Response(dict(success={'market_id': 'yolo'}))


def is_fields_are_valid(market_fields):
    form = NgoUserSerializer(data=market_fields)
    print(form)
    print(form.is_valid(raise_exception=True))
    return form.is_valid(raise_exception=True)

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