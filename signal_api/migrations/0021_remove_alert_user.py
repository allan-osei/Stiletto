# Generated by Django 4.2.2 on 2024-01-28 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signal_api', '0020_alter_alert_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alert',
            name='user',
        ),
    ]