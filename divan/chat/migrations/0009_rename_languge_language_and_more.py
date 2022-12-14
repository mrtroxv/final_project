# Generated by Django 4.1.2 on 2022-10-24 16:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_alter_message_message_send_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Languge',
            new_name='language',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='native_languge',
            new_name='native_language',
        ),
        migrations.AlterField(
            model_name='friend',
            name='request_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_send_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 24, 19, 8, 19, 855934)),
        ),
    ]
