# Generated by Django 4.2.4 on 2023-09-21 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusStations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terminal_name', models.CharField(blank=True, max_length=256, null=True)),
                ('terminal_code', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
