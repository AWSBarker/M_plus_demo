# Generated by Django 4.0 on 2022-06-11 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trials', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='contacts',
            table='CTgovContacts',
        ),
        migrations.AlterModelTable(
            name='ctgov1',
            table='CTgov1',
        ),
    ]
