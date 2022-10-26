from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Conversation)
admin.site.register(models.Country)
admin.site.register(models.FriendShip)
admin.site.register(models.language)
admin.site.register(models.Message)
# Register your models here.
