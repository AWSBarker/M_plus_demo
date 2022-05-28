# Generated by Django 4.0 on 2022-05-25 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('imei', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Devices',
                'verbose_name_plural': 'Devices',
                'db_table': 'Devices',
                'ordering': ['-imei'],
            },
        ),
        migrations.CreateModel(
            name='Measurements',
            fields=[
                ('measurements_timestamp', models.DateTimeField(null=True)),
                ('metadata_correlationid', models.CharField(db_column='metadata_correlationId', max_length=36, primary_key=True, serialize=False)),
                ('metadata_receivedtime', models.DateTimeField(blank=True, db_column='metadata_receivedTime', null=True)),
                ('metadata_devicegroups', models.TextField(blank=True, db_column='metadata_deviceGroups', null=True)),
                ('metadata_measurementtype', models.TextField(blank=True, db_column='metadata_measurementType', null=True)),
                ('device_id', models.TextField(blank=True, null=True)),
                ('device_serialnumber', models.TextField(blank=True, db_column='device_serialNumber', null=True)),
                ('device_imei', models.PositiveBigIntegerField(db_column='device_IMEI', null=True)),
                ('device_imsi', models.TextField(blank=True, db_column='device_IMSI', null=True)),
                ('device_manufacturer', models.TextField(blank=True, null=True)),
                ('device_model', models.TextField(blank=True, null=True)),
                ('device_timezone', models.TextField(blank=True, null=True)),
                ('measurements_annotations_averagemeasurement', models.BooleanField(blank=True, db_column='measurements_annotations_averageMeasurement', null=True)),
                ('measurements_annotations_irregularheartbeat', models.IntegerField(blank=True, db_column='measurements_annotations_irregularHeartBeat', null=True)),
                ('measurements_diastolicbloodpressure_value', models.IntegerField(blank=True, db_column='measurements_diastolicBloodPressure_value', null=True)),
                ('measurements_diastolicbloodpressure_unit', models.TextField(blank=True, db_column='measurements_diastolicBloodPressure_unit', null=True)),
                ('measurements_diastolicbloodpressure_isinrange', models.BooleanField(blank=True, db_column='measurements_diastolicBloodPressure_isInRange', null=True)),
                ('measurements_meanbloodpressure_value', models.IntegerField(blank=True, db_column='measurements_meanBloodPressure_value', null=True)),
                ('measurements_meanbloodpressure_unit', models.TextField(blank=True, db_column='measurements_meanBloodPressure_unit', null=True)),
                ('measurements_meanbloodpressure_isinrange', models.BooleanField(blank=True, db_column='measurements_meanBloodPressure_isInRange', null=True)),
                ('measurements_pulse_value', models.IntegerField(blank=True, null=True)),
                ('measurements_pulse_unit', models.TextField(blank=True, null=True)),
                ('measurements_pulse_isinrange', models.BooleanField(blank=True, db_column='measurements_pulse_isInRange', null=True)),
                ('measurements_systolicbloodpressure_value', models.BigIntegerField(blank=True, db_column='measurements_systolicBloodPressure_value', null=True)),
                ('measurements_systolicbloodpressure_unit', models.TextField(blank=True, db_column='measurements_systolicBloodPressure_unit', null=True)),
                ('measurements_systolicbloodpressure_isinrange', models.BooleanField(blank=True, db_column='measurements_systolicBloodPressure_isInRange', null=True)),
                ('measurements_ambienttemperature_value', models.FloatField(blank=True, db_column='measurements_ambientTemperature_value', null=True)),
                ('measurements_ambienttemperature_unit', models.TextField(blank=True, db_column='measurements_ambientTemperature_unit', null=True)),
                ('measurements_ambienttemperature_isinrange', models.BooleanField(blank=True, db_column='measurements_ambientTemperature_isInRange', null=True)),
                ('measurements_annotations_codenumber', models.TextField(blank=True, db_column='measurements_annotations_codeNumber', null=True)),
                ('measurements_annotations_mealtag', models.TextField(blank=True, db_column='measurements_annotations_mealTag', null=True)),
                ('measurements_glucose_value', models.FloatField(blank=True, null=True)),
                ('measurements_glucose_unit', models.TextField(blank=True, null=True)),
                ('measurements_glucose_isinrange', models.BooleanField(blank=True, db_column='measurements_glucose_isInRange', null=True)),
                ('measurements_bodycomposition_value', models.FloatField(blank=True, db_column='measurements_bodyComposition_value', null=True)),
                ('measurements_bodycomposition_unit', models.TextField(blank=True, db_column='measurements_bodyComposition_unit', null=True)),
                ('measurements_bodycomposition_isinrange', models.BooleanField(blank=True, db_column='measurements_bodyComposition_isInRange', null=True)),
                ('measurements_bodyweight_value', models.FloatField(blank=True, db_column='measurements_bodyWeight_value', null=True)),
                ('measurements_bodyweight_unit', models.TextField(blank=True, db_column='measurements_bodyWeight_unit', null=True)),
                ('measurements_bodyweight_isinrange', models.BooleanField(blank=True, db_column='measurements_bodyWeight_isInRange', null=True)),
                ('measurements_cholesterol_value', models.FloatField(blank=True, null=True)),
                ('measurements_cholesterol_unit', models.TextField(blank=True, null=True)),
                ('measurements_cholesterol_isinrange', models.BooleanField(blank=True, db_column='measurements_cholesterol_isInRange', null=True)),
                ('measurements_uricacid_value', models.FloatField(blank=True, null=True)),
                ('measurements_uricacid_unit', models.TextField(blank=True, null=True)),
                ('measurements_uricacid_isinrange', models.BooleanField(blank=True, db_column='measurements_uricacid_isInRange', null=True)),
                ('measurements_ketone_value', models.FloatField(blank=True, null=True)),
                ('measurements_ketone_unit', models.TextField(blank=True, null=True)),
                ('measurements_ketone_isinrange', models.BooleanField(blank=True, db_column='measurements_ketone_isInRange', null=True)),
                ('measurements_hematocrit_value', models.FloatField(blank=True, null=True)),
                ('measurements_hematocrit_unit', models.TextField(blank=True, null=True)),
                ('measurements_hematocrit_isinrange', models.BooleanField(blank=True, db_column='measurements_hematocrit_isInRange', null=True)),
                ('measurements_temperature_value', models.FloatField(blank=True, null=True)),
                ('measurements_temperature_unit', models.TextField(blank=True, null=True)),
                ('measurements_temperature_isinrange', models.BooleanField(blank=True, db_column='measurements_temperature_isInRange', null=True)),
                ('measurements_spo2_value', models.IntegerField(blank=True, db_column='measurements_SpO2_value', null=True)),
                ('measurements_spo2_unit', models.TextField(blank=True, db_column='measurements_SpO2_unit', null=True)),
                ('measurements_spo2_isinrange', models.BooleanField(blank=True, db_column='measurements_SpO2_isInRange', null=True)),
                ('measurements_device_id', models.TextField(blank=True, null=True)),
                ('measurements_device_serialnumber', models.IntegerField(blank=True, db_column='measurements_device_serialNumber', null=True)),
                ('measurements_device_imei', models.IntegerField(blank=True, db_column='measurements_device_IMEI', null=True)),
                ('measurements_device_manufacturer', models.TextField(blank=True, null=True)),
                ('measurements_device_model', models.TextField(blank=True, null=True)),
                ('measurements_device_timezone', models.TextField(blank=True, null=True)),
                ('measurements_ecgsamples_minvalue', models.SmallIntegerField(db_column='measurements_ecgSamples_minValue', null=True)),
                ('measurements_ecgsamples_maxvalue', models.SmallIntegerField(db_column='measurements_ecgSamples_maxValue', null=True)),
                ('measurements_ecgsamples_samplerate', models.SmallIntegerField(db_column='measurements_ecgSamples_sampleRate', null=True)),
                ('measurements_ecgsamples_samplerateunit', models.TextField(db_column='measurements_ecgSamples_sampleRateUnit', null=True)),
                ('measurements_ecgsamples_factor', models.FloatField(db_column='measurements_ecgSamples_factor', null=True)),
                ('measurements_ecgsamples_factorunit', models.TextField(db_column='measurements_ecgSamples_factorUnit', null=True)),
                ('measurements_ecgsamples_samples', models.TextField(db_column='measurements_ecgSamples_samples', null=True)),
                ('device_additionalattributes_currentdevicetime', models.FloatField(blank=True, db_column='device_additionalAttributes_currentDeviceTime', null=True)),
                ('device_additionalattributes_devicetype', models.TextField(blank=True, db_column='device_additionalAttributes_deviceType', null=True)),
                ('device_additionalattributes_devicever', models.TextField(blank=True, db_column='device_additionalAttributes_deviceVer', null=True)),
                ('patientid', models.CharField(max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'Measurements',
                'verbose_name_plural': 'Measurements',
                'db_table': 'Measurements',
                'ordering': ['-measurements_timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Patients',
            fields=[
                ('patientid', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Patients',
                'verbose_name_plural': 'Patients',
                'db_table': 'Patients',
                'ordering': ['-patientid'],
            },
        ),
        migrations.CreateModel(
            name='Pairings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('device', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='itasc.devices')),
                ('subject', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='itasc.patients')),
            ],
            options={
                'verbose_name': 'Pairings',
                'verbose_name_plural': 'Parings',
                'db_table': 'Pairings',
                'ordering': ['-subject'],
            },
        ),
    ]