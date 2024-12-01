# Generated by Django 4.2.2 on 2024-06-08 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signal_api', '0039_discord_webhook_pause_telegram_webhook_pause'),
    ]

    operations = [
        migrations.AddField(
            model_name='closeorder',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='signal_api.order'),
        ),
        migrations.AddField(
            model_name='modifyorder',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='signal_api.order'),
        ),
    ]
