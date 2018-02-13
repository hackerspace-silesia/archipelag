from decimal import Decimal
from rest_framework import serializers
from archipelag.ngo.models import NgoUser
from django.core.validators import MinValueValidator


class NgoUserSerializer(serializers.Serializer):
    email = serializers.ReadOnlyField(source='user.email')
    password = serializers.ReadOnlyField(source='user.password')
    username = serializers.ReadOnlyField(source='user.username')
    organisation = serializers.CharField(max_length=100)
    coins = serializers.DecimalField(max_digits=100, decimal_places=1, default=10.0, validators=[MinValueValidator(Decimal('0.00'))])
    id = serializers.IntegerField(required=False)

    class Meta:
        model = NgoUser
        fields = ('id', 'user', 'name', 'coins', 'username', 'password', 'email')


class NgoUserSerializerForList(serializers.Serializer):
    organisation = serializers.CharField(max_length=100)
    id = serializers.IntegerField()

    class Meta:
        model = NgoUser
        fields = ('id', 'organisation')
