# Generated by Django 4.0.5 on 2022-07-19 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_eliot_measurements_device_imei'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eliot',
            name='measurements_device_serialnumber',
            field=models.CharField(blank=True, db_column='measurements_device_serialNumber', max_length=60, null=True),
        ),
    ]