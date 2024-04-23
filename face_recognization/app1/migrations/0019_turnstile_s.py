# Generated by Django 5.0.1 on 2024-04-22 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0018_upload_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turnstile_S',
            fields=[
                ('sr_no', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('turnstile_id', models.IntegerField(unique=True)),
                ('location', models.CharField(max_length=100)),
                ('safety_confirmation', models.BooleanField(default=False)),
            ],
        ),
    ]
