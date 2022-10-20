from datetime import date, datetime
from email.policy import default
from django.db import models


class Languge (models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)


class Country(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255)
    native_languge = models.ForeignKey(
        Languge, null=True, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    profile_picture = models.CharField(max_length=255, null=True)


class Friend(models.Model):
    request_id = models.AutoField(primary_key=True, default=0)
    user = models.ForeignKey(User, related_name='user',
                             on_delete=models.CASCADE)
    friend = models.ForeignKey(
        User, related_name='friend', on_delete=models.CASCADE, default='null')
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
    message_send_date = models.DateTimeField(default=datetime.now())
    message_tex = models.CharField(max_length=255)


# Create your models here.
