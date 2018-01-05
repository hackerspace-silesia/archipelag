from rest_framework import serializers
from archipelag.ngo.models import NgoUser


class NgoUserSerializer(serializers.Serializer):
    user = serializers.ReadOnlyField(source='user.email')
    name = serializers.CharField(max_length=100)
    coins = serializers.DecimalField(max_digits=100, decimal_places=1,)
    id = serializers.IntegerField()

    class Meta:
        model = NgoUser
        fields = ('id', 'user', 'name', 'coins')
