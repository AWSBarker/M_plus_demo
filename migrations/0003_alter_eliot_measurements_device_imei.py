# Generated by Django 4.0.5 on 2022-07-19 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_eliot_measurements_device_serialnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eliot',
            name='measurements_device_imei',
            field=models.CharField(blank=True, db_column='measurements_device_IMEI', max_length=60, null=True),
        ),
    ]