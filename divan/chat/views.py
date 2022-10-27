from rest_framework.views import APIView
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from .token_process import TokenProcess
from .get_name_by_id import UserInformation
from . import serializers
from .auth_firebase import FirebaseAuth
from .models import Conversation, FriendShip, Message, User


#@@@@@@@@@@@@@@@@@@@@@@@@@ authorization function @@@@@@@@@@@@@@@@@@@@@@@@@@@@#

def token_required(func):
    def inner(cls, request: HttpRequest, *args, **kwargs):
        uid = args[0]
        auth = FirebaseAuth()
        is_valid_pro = TokenProcess()
        tokenid = request.headers.get('tokenid')
        user_id = auth.get_user_id_by_token(tokenid)
        if is_valid_pro.is_valid_token(tokenid) and uid == user_id:
            del is_valid_pro
            return func(request, *args, **kwargs)
        else:
            return Response("the user is not authorized", status=status.HTTP_403_FORBIDDEN)
    return inner


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ login Api @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class Login(APIView):
    def post(self, request: HttpRequest):
        email = request.data.get('email')
        password = request.data.get('password')
        auth = FirebaseAuth()
        try:
            credentials = auth.login(email, password)
        except Exception as e:
            return HttpResponse(e)
        return JsonResponse({"token": credentials}, status=status.HTTP_200_OK, safe=False)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ signup Api @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class Signup(APIView):
    def post(self, request: HttpRequest):
        email = request.data.get('email')
        password = request.data.get('password')
        auth = FirebaseAuth()
        id_pro = TokenProcess()
        req_data = request.data
        req_data['id'] = 'empty'
        serializer = serializers.UserSerializer(data=req_data)
        if serializer.is_valid():
            try:
                token = auth.signup(email, password)
            except:
                return Response("the user already exists", status=status.HTTP_400_BAD_REQUEST)
            uid = id_pro.get_user_id(email)
            del id_pro
            req_data['id'] = uid
            serializer = serializers.UserSerializer(data=req_data)
            if serializer.is_valid():
                serializer.save()
            return JsonResponse({"token": token}, status=status.HTTP_200_OK, safe=False)
        else:
            return Response('your data is not valid', status=status.HTTP_400_BAD_REQUEST)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ refresh token Api @@@@@@@@@@@@@@@@@@@@@@@@@@@#

class RefreshToken(APIView):
    def post(self, request: HttpRequest, uid):
        tokenid = request.headers.get('tokenid')
        auth = FirebaseAuth()
        user_id = auth.get_user_id_by_token(tokenid)
        if uid == user_id:
            try:
                refresh_token = request.headers['refreshToken']
            except:
                return Response("please insert refresh token", status=status.HTTP_400_BAD_REQUEST)
            try:
                refresh = auth.refresh_token(refresh_token)
            except:
                return Response("Invalid refresh token", status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse(refresh, status=status.HTTP_200_OK)
        else:
            return Response("invalid refresh token for user", status=status.HTTP_400_BAD_REQUEST)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ signout Api @@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class Signout(APIView):
    @token_required
    def sign_out(request: HttpRequest, uid):
        revoke_pro = TokenProcess()
        try:
            revoke_pro.revoke_token(uid)
            del revoke_pro
        except Exception as e:
            return HttpResponse(e)

        return Response('the user is sign out', status=status.HTTP_200_OK)

    def post(self, request: HttpRequest, uid):
        return self.sign_out(request, uid)


class Profile(APIView):
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@---view user profile---@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
    @token_required
    def view_profile(request: HttpRequest, uid):
        try:
            user_obj = User.objects.get(id=uid)
        except:
            return Response("the user id not found", status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.UserSerializer(user_obj)
        data = serializer.data
        user_info = UserInformation()
        country_name = user_info.get_country_name(data)
        language_name = user_info.get_native_languge_name(data)
        data["country"] = country_name
        data['native_language'] = language_name
        return Response(data, status=status.HTTP_200_OK)

    def get(self, request: HttpRequest, uid):
        return self.view_profile(request, uid)

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@--update user profile---@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
    @token_required
    def update_profile(request: HttpRequest, uid):
        try:
            user_obj = User.objects.get(id=uid)
        except:
            return Response("the user id not found", status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.UserSerializer(
            user_obj, data=request.query_params, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("ur profile is update", status=status.HTTP_200_OK)
        else:
            return Response("invalid data", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: HttpRequest, uid):
        return self.update_profile(request, uid)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@send friend request@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class FriendRequest(APIView):
    @token_required
    def send_request(request: HttpRequest, user1_id, user2_id):
        req = {}
        req['user1'] = user1_id
        req['user2'] = user2_id
        serializer = serializers.FriendSerializer(data=req)
        if serializer.is_valid():
            serializer.save()
            return Response("the friend request pending", status=status.HTTP_200_OK)
        else:
            return Response("invalid data", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request: HttpRequest, user1_id, user2_id):
        return self.send_request(request, user1_id, user2_id)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@view friend request@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class FriendRequestView(APIView):
    @token_required
    def view_request(request: HttpRequest, uid):
        res = []
        user_obj = FriendShip.objects.filter(
            (Q(user1=uid) | Q(user2=uid)) & Q(status=0))
        for i in user_obj:
            data = vars(i)

            def req_dict_maker(data_s):
                request_id = data_s.get("request_id")
                user_info = UserInformation()
                user_name = user_info.get_user1_name_from_friendship(
                    data_s)
                friend_name = user_info.get_user2_name_from_friendship(
                    data_s)
                statu = user_info.get_friend_request_status(data_s)
                req_dict = {}
                req_dict['request_id'] = request_id
                req_dict['status'] = statu
                req_dict['from'] = user_name
                req_dict['to'] = friend_name
                return req_dict
            serializer = serializers.FriendSerializer(i)
            data_s = serializer.data
            dict_req = req_dict_maker(data_s)
            res.append(dict_req)
        return Response(res, status=status.HTTP_200_OK)

    def get(self, request: HttpRequest, uid):
        return self.view_request(request, uid)

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@accept friend request@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#


class AcceptRequest(APIView):
    @token_required
    def accept_request(request: HttpRequest, uid, request_id):
        req_obj = FriendShip.objects.get(request_id=request_id)
        friend_id = serializers.FriendSerializer(
            req_obj).data.get("user2")
        serializer = serializers.FriendSerializer(
            req_obj, data={"status": 2}, partial=True)
        if serializer.is_valid() and friend_id == uid:
            serializer.save()
            return Response("friend request accepted", status=status.HTTP_200_OK)
        else:
            return Response("invalid data", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request: HttpRequest, uid, request_id):
        return self.accept_request(request, uid, request_id)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Refuse friend request @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class RefuseRequest(APIView):
    @token_required
    def refuse_request(request: HttpRequest, uid, request_id):
        req_obj = FriendShip.objects.get(request_id=request_id)
        friend_id = serializers.FriendSerializer(
            req_obj).data.get("user2")
        serializer = serializers.FriendSerializer(
            req_obj, data={"status": 1}, partial=True)
        if serializer.is_valid() and friend_id == uid:
            serializer.save()
            return Response("the request refused ", status=status.HTTP_200_OK)
        else:
            return Response("invalid data", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request: HttpRequest, uid, request_id):
        return self.refuse_request(request, uid, request_id)


#@@@@@@@@@@@@@@@@@@@@@@@@@create conversation@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class CreateCoversation(APIView):
    @token_required
    def create_conversation(request: HttpRequest, user1_id, user2_id):
        req = {}
        req['user1'] = user1_id
        req['user2'] = user2_id
        filter = FriendShip.objects.filter(
            (Q(user1=user1_id) & Q(user2=user2_id) & Q(status=2)) | (Q(user1=user2_id) & Q(user2=user1_id) & Q(status=2)))
        serializer = serializers.FriendSerializer(filter[0])
        data = serializer.data
        if data != {}:
            conversation_serializer = serializers.ConversationSerializer(
                data=req)
            if conversation_serializer.is_valid():
                conversation_serializer.save()
                return Response("conversation created", status=status.HTTP_200_OK)
            else:
                return Response("invalid data", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("no friend ship between this users", status=status.HTTP_404_NOT_FOUND)

    def post(self, request: HttpRequest, user1_id, user2_id):
        return self.create_conversation(request, user1_id, user2_id)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ view user @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class ViewUsers(APIView):
    @token_required
    def view_user(request: HttpRequest, uid):
        user_info = UserInformation()
        user_objs = User.objects.all()
        res = []
        for i in user_objs:
            serializer = serializers.UserSerializer(i)
            data = serializer.data
            country_name = user_info.get_country_name(data)
            language_name = user_info.get_native_languge_name(data)
            data["country"] = country_name
            data['native_language'] = language_name
            res.append(data)

        return Response(res, status=status.HTTP_200_OK)

    def get(self, request: HttpRequest, uid):
        return self.view_user(request, uid)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ view Friend @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class ViewFriend(APIView):
    @token_required
    def view_friend(request: HttpRequest, user_id):
        res = []
        user_info = UserInformation()
        filter = FriendShip.objects.filter(
            (Q(user1=user_id) | Q(user2=user_id)) & Q(status=2))
        for friend_ship in filter:
            friend_ship = vars(friend_ship)
            if user_id != friend_ship.get('user1_id'):
                user_obj = User.objects.get(id=friend_ship.get('user1_id'))
            elif user_id != friend_ship.get('user2_id'):
                user_obj = User.objects.get(id=friend_ship.get('user2_id'))
            serializer = serializers.UserSerializer(user_obj)
            data = serializer.data
            country_name = user_info.get_country_name(data)
            language_name = user_info.get_native_languge_name(data)
            data["country"] = country_name
            data['native_language'] = language_name
            res.append(data)

        return Response(res, status=status.HTTP_200_OK)

    def get(self, request: HttpRequest, user_id):
        return self.view_friend(request, user_id)


#@@@@@@@@@@@@@@@@@@@@@@@@@@send a message@@@@@@@@@@@@@@@@@@@@@#

class CreateMessage(APIView):
    @token_required
    def send_message(request: HttpRequest, user_id, conversation_id):
        req = {}
        req['text'] = request.query_params.get('message')
        req['conversation'] = conversation_id
        req['sender'] = user_id
        conver_obj = Conversation.objects.get(id=conversation_id)
        conver_data = serializers.ConversationSerializer(conver_obj).data
        user1 = conver_data.get("user1")
        user2 = conver_data.get("user2")
        serializer = serializers.MessageSerializer(data=req)
        if serializer.is_valid() and (user_id == user1 or user_id == user2):
            serializer.save()
            return Response('message sent', status=status.HTTP_200_OK)
        else:
            return Response("invalid data", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request: HttpRequest, user_id, conversation_id):
        return self.send_message(request, user_id, conversation_id)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@view conversation@@@@@@@@@@@@@@@@@@@@@@@@@@#

class ViewConversations(APIView):
    @token_required
    def view_conversation(request: HttpRequest, user_id):
        user_info = UserInformation()
        res = []
        conver_objs = Conversation.objects.filter(
            Q(user1=user_id) | Q(user2=user_id))
        for i in conver_objs:
            data = vars(i)
            serializer = serializers.ConversationSerializer(i)
            data = serializer.data
            dict = user_info.get_user_name_dict(data)
            data['user1'] = dict["user1"]
            data['user2'] = dict["user2"]
            res.append(data)
        return Response(res, status=status.HTTP_200_OK)

    def get(self, request: HttpRequest, user_id):
        return self.view_conversation(request, user_id)


#@@@@@@@@@@@@@@@@@@@@@view message@@@@@@@@@@@@@@@@@@@@@@@@#

class ViewConversationMessage(APIView):
    @token_required
    def view_message(request: HttpRequest, user_id, conversation_id):
        user_info = UserInformation()
        message_obj = Message.objects.filter(conversation_id=conversation_id)
        conver_obj = Conversation.objects.get(id=conversation_id)
        data_of_conver = vars(conver_obj)
        res = []
        if data_of_conver.get('user1_id') == user_id or data_of_conver.get('user2_id') == user_id:
            for i in message_obj:
                serializer = serializers.MessageSerializer(i)
                message_data = serializer.data
                sender_name = user_info.get_name(
                    message_data.get("sender"))
                message_data["sender"] = sender_name
                res.append(message_data)
            return Response(res, status=status.HTTP_200_OK)

    def get(self, request: HttpRequest, user_id, conversation_id):
        return self.view_message(request, user_id, conversation_id)
