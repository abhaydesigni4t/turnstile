# Generated by Django 5.0.1 on 2024-03-28 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_alter_exit_time_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exit',
            name='time_log',
            field=models.CharField(max_length=10),
        ),
    ]
