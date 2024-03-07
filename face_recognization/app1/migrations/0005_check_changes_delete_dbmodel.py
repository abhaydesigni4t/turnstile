# Generated by Django 5.0.1 on 2024-02-28 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_dbmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='check_changes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='dbmodel',
        ),
    ]
