from archipelag.ngo.serializers import NgoUserSerializer
from archipelag.ngo.models import NgoUser


def jwt_response_payload_handler(token, user=None, request=None):

    ngo = NgoUser.objects.filter(user=user.id).first()

    return {
        'token': token,
        'user': NgoUserSerializer(ngo).data
    }