# Generated by Django 4.2.2 on 2024-03-06 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signal_api', '0028_mt5_webhook_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='closeorder',
            name='discord_webhook',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='signal_api.discord_webhook'),
        ),
        migrations.AddField(
            model_name='closeorder',
            name='telegram_webhook',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='signal_api.telegram_webhook'),
        ),
        migrations.AddField(
            model_name='modifyorder',
            name='discord_webhook',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='signal_api.discord_webhook'),
        ),
        migrations.AddField(
            model_name='modifyorder',
            name='telegram_webhook',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='signal_api.telegram_webhook'),
        ),
        migrations.AddField(
            model_name='order',
            name='discord_webhook',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='signal_api.discord_webhook'),
        ),
        migrations.AddField(
            model_name='order',
            name='telegram_webhook',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='signal_api.telegram_webhook'),
        ),
        migrations.AlterField(
            model_name='order',
            name='mt5_webhook',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='signal_api.mt5_webhook'),
        ),
    ]
