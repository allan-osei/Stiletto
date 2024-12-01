# Generated by Django 4.2.2 on 2024-04-01 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('signal_api', '0030_delete_binance_webhook_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='discord_webhook',
            name='status',
            field=models.CharField(default='inactive', max_length=10),
        ),
        migrations.AlterField(
            model_name='mt5_webhook',
            name='status',
            field=models.CharField(default='inactive', max_length=10),
        ),
        migrations.AlterField(
            model_name='telegram_webhook',
            name='status',
            field=models.CharField(default='inactive', max_length=10),
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('webhook_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('subscription_id', models.UUIDField(blank=True, null=True)),
                ('product_id', models.UUIDField(blank=True, null=True)),
                ('variant_id', models.UUIDField(blank=True, null=True)),
                ('renews_at', models.DateTimeField(blank=True, null=True)),
                ('ends_at', models.DateTimeField(blank=True, null=True)),
                ('hits', models.IntegerField(default=0)),
                ('status', models.CharField(default='inactive', max_length=10)),
                ('hit_limit', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]