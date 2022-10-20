from email import message
from rest_framework.views import APIView
from django.http import HttpRequest, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from . import serializers
from . import auth_firebase
from . import token_process
from .models import Conversation, Friend, Message, User, Country


class Login(APIView):
    def post(self, request: HttpRequest):
        email = request.query_params.get('email')
        password = request.query_params.get('password')
        try:
            token = auth_firebase.login(email, password)
        except:
            return Response("Your email or password is incorrect, please try again", status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"token": token}, status=status.HTTP_200_OK, safe=False)


class Signup (APIView):
    def post(self, request: HttpRequest):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            token = auth_firebase.signup(email, password)
        except:
            return Response("the user already exists", status=status.HTTP_400_BAD_REQUEST)
        req_data = request.data
        uid = token_process.get_user_id(email)
        req_data['id'] = uid
        print(req_data)
        serializer = serializers.UserSerializer(data=req_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"token": token}, status=status.HTTP_200_OK, safe=False)
        else:
            return Response('your data is not valid', status=status.HTTP_400_BAD_REQUEST)


class RefreshToken(APIView):
    def post(self, request: HttpRequest):
        refresh_token = request.headers['refreshToken']
        try:
            refresh = auth_firebase.refresh_token(refresh_token)
        except:
            return Response("INVALID_REFRESH_TOKEN", status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(refresh, status=status.HTTP_200_OK)


class Signout(APIView):
    def post(self, request: HttpRequest, uid):
        try:
            token_process.revoke_token(uid)
        except:
            return Response("user id invalid ", status=status.HTTP_400_BAD_REQUEST)
        return Response('the user is sign out', status=status.HTTP_200_OK)


class Profile(APIView):
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@---view user profile---@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
    def get(self, request: HttpRequest, uid):
        token_id = request.headers.get('tokenid')
        if token_process.is_valid_token(token_id):
            try:
                user_obj = User.objects.get(id=uid)
            except:
                return Response("the user id not found", status=status.HTTP_400_BAD_REQUEST)
            serializer = serializers.UserSerializer(user_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("the user is not authorized", status=status.HTTP_403_FORBIDDEN)

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@--update user profile---@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

    def put(self, request: HttpRequest, uid):
        token_id = request.headers.get('tokenid')
        if token_process.is_valid_token(token_id):
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
        else:
            return Response("the user is not authorized", status=status.HTTP_403_FORBIDDEN)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@send friend request@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class FriendRequest(APIView):
    def post(self, request: HttpRequest, user_id, friend_id):
        token_id = request.headers.get('tokenid')
        if token_process.is_valid_token(token_id):
            req = {}
            req['user'] = user_id
            req['friend'] = friend_id
            serializer = serializers.FriendSerializer(data=req)
            if serializer.is_valid():
                serializer.save()
                return Response("the friend request pending", status=status.HTTP_200_OK)
            else:
                return Response("invalid data", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("the user is not authorized", status=status.HTTP_403_FORBIDDEN)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@view friend request@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class RequestView(APIView):
    def get(self, request: HttpRequest, uid):
        token_id = request.headers.get('tokenid')
        if token_process.is_valid_token(token_id):
            res = []
            user_obj = Friend.objects.all()
            for i in user_obj:
                data = vars(i)
                if data.get('user_id') == uid:
                    serializer = serializers.FriendSerializer(i)
                    res.append(serializer.data)

            if res == []:
                return Response('user not found', status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(res, status=status.HTTP_200_OK)
        else:
            return Response("the user is not authorized", status=status.HTTP_403_FORBIDDEN)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@accept friend request@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class AcceptRequest(APIView):
    def post(self, request: HttpRequest, request_id):
        token_id = request.headers.get('tokenid')
        if token_process.is_valid_token(token_id):
            req_obj = Friend.objects.get(request_id=request_id)
            serializer = serializers.FriendSerializer(
                req_obj, data={"status": 2}, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response("invalid data", status=status.HTTP_200_OK)
        else:
            return Response("the user is not authorized", status=status.HTTP_403_FORBIDDEN)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Refuse friend request @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class RefuseRequest(APIView):
    def post(self, request: HttpRequest, request_id):
        token_id = request.headers.get('tokenid')
        if token_process.is_valid_token(token_id):
            req_obj = Friend.objects.get(request_id=request_id)
            serializer = serializers.FriendSerializer(
                req_obj, data={"status": 1}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response("the request refused ", status=status.HTTP_200_OK)
            else:
                return Response("invalid data", status=status.HTTP_200_OK)
        else:
            return Response("the user is not authorized", status=status.HTTP_403_FORBIDDEN)


#@@@@@@@@@@@@@@@@@@@@@@@@@create conversation@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class CreateCoversation(APIView):
    def post(self, request: HttpRequest, user1_id, user2_id):
        token_id = request.headers.get('tokenid')
        if token_process.is_valid_token(token_id):
            req = {}
            req['user1'] = user1_id
            req['user2'] = user2_id
            conversation_serializer = serializers.ConversationSerializer(
                data=req)
            if conversation_serializer.is_valid():
                conversation_serializer.save()
                return Response("conversation created", status=status.HTTP_200_OK)
            else:
                return Response("invalid data", status=status.HTTP_200_OK)
        else:
            return Response("the user is not authorized", status=status.HTTP_403_FORBIDDEN)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@view user @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class ViewUser(APIView):
    def get(self, request: HttpRequest):
        token_id = request.headers.get('tokenid')
        if token_process.is_valid_token(token_id):
            user_objs = User.objects.all()
            res = []
            for i in user_objs:
                serializer = serializers.UserSerializer(i)
                res.append(serializer.data)
            if res == []:
                return Response("non user in the system", status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(res, status=status.HTTP_200_OK)
        else:
            return Response("the user is not authorized", status=status.HTTP_403_FORBIDDEN)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ view Friend @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class ViewFriend(APIView):
    def get(self, request: HttpRequest, user_id):
        token_id = request.headers.get('tokenid')
        if token_process.is_valid_token(token_id):
            res = []
            user_objs = Friend.objects.all()
            for user in user_objs:
                data = vars(user)
                print(data)
                if (data.get('user_id') == user_id or data.get('friend_id') == user_id) and data.get('status') == 2:
                    serializer = serializers.FriendSerializer(user)
                    res.append(serializer.data)
            if res == []:
                return Response("no friend found", status=status.HTTP_404_NOT_FOUND)
            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response("the user is not authorized", status=status.HTTP_403_FORBIDDEN)


#@@@@@@@@@@@@@@@@@@@@@@@@@@send a message@@@@@@@@@@@@@@@@@@@@@#

class CreateMessage(APIView):
    def post(self, request: HttpRequest, user_id, conversation_id):
        token_id = request.headers.get('tokenid')
        if token_process.is_valid_token(token_id):
            req = {}
            req['message_tex'] = request.query_params.get('message')
            req['conversation'] = conversation_id
            req['sender'] = user_id
            print(req)
            serializer = serializers.MessageSerializer(data=req)
            if serializer.is_valid():
                serializer.save()
                return Response('message sent', status=status.HTTP_200_OK)
            else:
                return Response("invalid data", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("the user is not authorized", status=status.HTTP_403_FORBIDDEN)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@view conversation@@@@@@@@@@@@@@@@@@@@@@@@@@#

class ViewConversation(APIView):
    def get(self, request: HttpRequest, user_id):
        token_id = request.headers.get('tokenid')
        if token_process.is_valid_token(token_id):
            res = []
            conver_objs = Conversation.objects.all()
            for i in conver_objs:
                data = vars(i)
                if data.get('user1_id') == user_id or data.get('user2_id'):
                    serializer = serializers.ConversationSerializer(i)
                    res.append(serializer.data)
            if res == []:
                return Response('the user not have a conversation yet', status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(res, status=status.HTTP_200_OK)
        else:
            return Response("the user is not authorized", status=status.HTTP_403_FORBIDDEN)


#@@@@@@@@@@@@@@@@@@@@@view message@@@@@@@@@@@@@@@@@@@@@@@@#

class ViewConversationMessage(APIView):
    def get(self, request: HttpRequest, conversation_id):
        token_id = request.headers.get('tokenid')
        if token_process.is_valid_token(token_id):
            message_obj = Message.objects.all()
            res = []
            for i in message_obj:
                data = vars(i)
                if data.get('conversation_id') == conversation_id:
                    serializer = serializers.MessageSerializer(i)
                    res.append(serializer.data)
            if res == []:
                return Response("no message found", status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(res, status=status.HTTP_200_OK)
        else:
            return Response("the user is not authorized", status=status.HTTP_403_FORBIDDEN)
