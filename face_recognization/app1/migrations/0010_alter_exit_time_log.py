# Generated by Django 5.0.1 on 2024-03-28 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_remove_exit_asset_exit_asset_id_exit_asset_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exit',
            name='time_log',
            field=models.TimeField(),
        ),
    ]
