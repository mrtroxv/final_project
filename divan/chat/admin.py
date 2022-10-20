from django.contrib import admin
from . import models
admin.site.register(models.User)
admin.site.register(models.Conversation)
admin.site.register(models.Country)
admin.site.register(models.Friend)
admin.site.register(models.Languge)
admin.site.register(models.Message)
# Register your models here.
