# Generated by Django 4.1.2 on 2022-10-20 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_conversation_id_alter_conversation_user1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
