# Generated by Django 4.2.2 on 2023-11-29 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signal_api', '0003_rename_binance_enabled_signal_mt5_enabled_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signal',
            name='channel_invite_link',
        ),
        migrations.AddField(
            model_name='signal',
            name='channel_chat_id',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
