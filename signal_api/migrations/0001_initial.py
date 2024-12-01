# Generated by Django 4.2.2 on 2023-11-24 08:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_invite_link', models.CharField(max_length=25)),
                ('message_format', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_enabled', models.BooleanField()),
                ('parse', models.BooleanField()),
                ('telegram', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='signal_api.telegramalert')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
