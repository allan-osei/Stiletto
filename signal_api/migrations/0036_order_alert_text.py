# Generated by Django 4.2.2 on 2024-05-09 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signal_api', '0035_alter_discord_webhook_chat_limit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='alert_text',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]