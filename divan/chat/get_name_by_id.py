from . import serializers, models


class UserInformation:
    def get_country_name(self, data) -> str:
        id = data.get("country")
        country = models.Country.objects.get(id=id)
        country_serializer = serializers.CountrySerializer(country)
        return country_serializer.data.get("name")

    def get_native_languge_name(self, data) -> str:
        id = data.get("native_language")
        language = models.Language.objects.get(id=id)
        language_serializer = serializers.LanguageSerializer(language)
        return language_serializer.data.get("name")

    def get_user1_name_from_friendship(self, data) -> str:
        id = data.get("user1")
        user = models.User.objects.get(id=id)
        user_serializer = serializers.UserSerializer(user)
        return user_serializer.data.get("name")

    def get_user2_name_from_friendship(self, data) -> str:
        id = data.get("user2")
        user = models.User.objects.get(id=id)
        user_serializer = serializers.UserSerializer(user)
        return user_serializer.data.get("name")

    def get_friend_request_status(self, data) -> str:
        st_no = data.get("status")
        if st_no == 2:
            return "accept"
        elif st_no == 1:
            return "reject"
        else:
            return "pending"

    def get_name(self, id) -> str:
        user = models.User.objects.get(id=id)
        user_serializer = serializers.UserSerializer(user)
        return user_serializer.data.get("name")

    def get_user_name_dict(self, data) -> dict:
        id_user1 = data.get('user1')
        id_user2 = data.get("user2")
        user1 = self.get_name(id_user1)
        user2 = self.get_name(id_user2)
        dict = {
            "user1": user1,
            "user2": user2
        }
        return dict
