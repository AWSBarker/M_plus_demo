# Generated by Django 4.0.5 on 2022-07-19 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eliot',
            name='measurements_device_serialnumber',
            field=models.TextField(blank=True, db_column='measurements_device_serialNumber', null=True),
        ),
    ]