# Generated by Django 4.1.2 on 2022-10-26 12:11

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0012_alter_message_message_send_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='user2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_2', to='chat.user'),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_send_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 26, 15, 11, 43, 656360)),
        ),
    ]
