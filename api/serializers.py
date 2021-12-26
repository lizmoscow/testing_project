from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    """
    Serializer for Room model
    """
    class Meta:
        model = Room
        fields = ('id', 'code', 'host', 'guest_can_pause',
                  'votes_to_skip', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    class Meta:
        model = User
        fields = ('username', 'password')


class CreateRoomSerializer(serializers.ModelSerializer):
    """
    Serializes data for CreateRoom view
    """
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')


class UpdateRoomSerializer(serializers.ModelSerializer):
    """
    Serializes data for UpdateRoom view
    """
    code = serializers.CharField(validators=[])

    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip', 'code')


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Serializes data for Register view
    """
    class Meta:
        model = User
        fields = ('username', 'password')
