# Generated by Django 4.2.2 on 2023-12-04 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('signal_api', '0006_signal_mt5_lot'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discord_Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parse', models.BooleanField(default=False)),
                ('channel_chat_id', models.CharField(blank=True, max_length=15, null=True)),
                ('message_format', models.CharField(blank=True, max_length=500, null=True)),
                ('message_prefix', models.CharField(blank=True, max_length=200, null=True)),
                ('message_suffix', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MT5_Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mt5_login', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=30, null=True))),
                ('mt5_password', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=60, null=True))),
                ('mt5_server', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=30, null=True))),
                ('mt5_lot', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SignalWebhook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_extra', models.BooleanField(default=False)),
                ('daily_limit', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Telegram_Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parse', models.BooleanField(default=False)),
                ('channel_chat_id', models.CharField(blank=True, max_length=15, null=True)),
                ('message_format', models.CharField(blank=True, max_length=500, null=True)),
                ('message_prefix', models.CharField(blank=True, max_length=200, null=True)),
                ('message_suffix', models.CharField(blank=True, max_length=200, null=True)),
                ('webhook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signal_api.signalwebhook')),
            ],
        ),
        migrations.DeleteModel(
            name='Signal',
        ),
        migrations.AddField(
            model_name='mt5_link',
            name='webhook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signal_api.signalwebhook'),
        ),
        migrations.AddField(
            model_name='discord_link',
            name='webhook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signal_api.signalwebhook'),
        ),
    ]
