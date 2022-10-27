from rest_framework import serializers
from .models import Conversation, Country, FriendShip, Language, Message, User


class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendShip
        fields = ('user1', 'user2', 'status')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'
