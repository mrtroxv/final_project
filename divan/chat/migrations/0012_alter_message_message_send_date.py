# Generated by Django 4.1.2 on 2022-10-26 12:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0011_alter_friendship_user1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_send_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 26, 15, 11, 10, 57181)),
        ),
    ]