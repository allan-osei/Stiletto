# Generated by Django 4.2.2 on 2024-01-28 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signal_api', '0021_remove_alert_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='content',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
