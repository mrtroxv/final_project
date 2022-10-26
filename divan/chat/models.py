from datetime import datetime
from email.policy import default
from django.db import models


class language (models.Model):
    def __str__(self) -> str:
        return self.name
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)


class Country(models.Model):
    def __str__(self) -> str:
        return self.name
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)


class User(models.Model):
    def __str__(self) -> str:
        return self.name
    id = models.CharField(primary_key=True, max_length=255)
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255, null=True)
    native_language = models.ForeignKey(
        language, null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    profile_picture = models.CharField(max_length=255, null=True)


class FriendShip(models.Model):
    request_id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(User, related_name='user_1',
                              on_delete=models.CASCADE)
    user2 = models.ForeignKey(
        User, related_name='user_2', on_delete=models.CASCADE)
    status = models.IntegerField(default=0)


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(
        User, related_name='user1', max_length=255, on_delete=models.CASCADE)
    user2 = models.ForeignKey(
        User, related_name='user2', max_length=255, on_delete=models.CASCADE)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    send_date = models.DateTimeField(default=datetime.now())
    text = models.CharField(max_length=255)


# Create your models here.
