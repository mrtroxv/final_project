# Generated by Django 4.1.2 on 2022-10-20 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_alter_conversation_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='id',
        ),
        migrations.AddField(
            model_name='friend',
            name='request_id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
        ),
    ]