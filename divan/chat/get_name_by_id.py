import re
from . import serializers, models


def get_country_name(data):
    id = data.get("country")
    country = models.Country.objects.get(id=id)
    country_serializer = serializers.CountrySerializer(country)
    return country_serializer.data.get("name")


def native_languge_name(data):
    id = data.get("native_language")
    language = models.language.objects.get(id=id)
    language_serializer = serializers.LanguageSerializer(language)
    return language_serializer.data.get("name")


def user_name(data):
    id = data.get("user1")
    user = models.User.objects.get(id=id)
    user_serializer = serializers.UserSerializer(user)
    return user_serializer.data.get("name")


def friend_name(data):
    id = data.get("user2")
    user = models.User.objects.get(id=id)
    user_serializer = serializers.UserSerializer(user)
    return user_serializer.data.get("name")


def get_status(data):
    st_no = data.get("status")
    if st_no == 2:
        return "accept"
    elif st_no == 1:
        return "reject"
    else:
        return "pending"


def get_name(id):
    user = models.User.objects.get(id=id)
    user_serializer = serializers.UserSerializer(user)
    return user_serializer.data.get("name")


def user_name_dict(data):
    id_user1 = data.get('user1')
    id_user2 = data.get("user2")
    user1 = get_name(id_user1)
    user2 = get_name(id_user2)
    dict = {
        "user1": user1,
        "user2": user2
    }
    return dict
