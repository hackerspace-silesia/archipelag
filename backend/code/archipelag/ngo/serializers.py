from rest_framework import serializers
from archipelag.ngo.models import NgoUser


class NgoUserSerializer(serializers.Serializer):
    email = serializers.ReadOnlyField(source='user.email')
    password = serializers.ReadOnlyField(source='user.password')
    username = serializers.ReadOnlyField(source='user.username')
    name = serializers.CharField(max_length=100)
    coins = serializers.DecimalField(max_digits=100, decimal_places=1,)
    id = serializers.IntegerField()

    class Meta:
        model = NgoUser
        fields = ('id', 'user', 'name', 'coins', 'username', 'password', 'email')


class NgoUserSerializerForList(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    id = serializers.IntegergitField()

    class Meta:
        model = NgoUser
        fields = ('id', 'name')
