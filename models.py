from django.db import models
import json
from datetime import datetime as dt
import pandas as pd

class Eliot(models.Model):
    measurements_timestamp = models.DateTimeField(null=True)
    metadata_correlationid = models.CharField(db_column='metadata_correlationId', primary_key=True, max_length=36, null=False)  # Field name made lowercase.
    metadata_receivedtime = models.DateTimeField(db_column='metadata_receivedTime', blank=True, null=True)  # Field name made lowercase.
    metadata_devicegroups = models.TextField(db_column='metadata_deviceGroups', blank=True, null=True)  # Field name made lowercase.
    metadata_measurementtype = models.TextField(db_column='metadata_measurementType', blank=True, null=True)  # Field name made lowercase.
    device_id = models.TextField(blank=True, null=True)
    device_serialnumber = models.TextField(db_column='device_serialNumber', blank=True, null=True)  # Field name made lowercase.
    device_imei = models.PositiveBigIntegerField(db_column='device_IMEI', null=True)  # Field name made lowercase.
    device_imsi = models.TextField(db_column='device_IMSI', blank=True, null=True)  # Field name made lowercase.
    device_manufacturer = models.TextField(blank=True, null=True)
    device_model = models.TextField(blank=True, null=True)
    device_timezone = models.TextField(blank=True, null=True)

    measurements_annotations_averagemeasurement = models.BooleanField(db_column='measurements_annotations_averageMeasurement', blank=True, null=True)  # Field name made lowercase.
    measurements_annotations_irregularheartbeat = models.IntegerField(db_column='measurements_annotations_irregularHeartBeat', blank=True, null=True)  # Field name made lowercase.
    measurements_diastolicbloodpressure_value = models.IntegerField(db_column='measurements_diastolicBloodPressure_value', blank=True, null=True)  # Field name made lowercase.
    measurements_diastolicbloodpressure_unit = models.TextField(db_column='measurements_diastolicBloodPressure_unit', blank=True, null=True)  # Field name made lowercase.
    measurements_diastolicbloodpressure_isinrange = models.BooleanField(db_column='measurements_diastolicBloodPressure_isInRange', blank=True, null=True)  # Field name made lowercase.
    measurements_meanbloodpressure_value = models.IntegerField(db_column='measurements_meanBloodPressure_value', blank=True, null=True)  # Field name made lowercase.
    measurements_meanbloodpressure_unit = models.TextField(db_column='measurements_meanBloodPressure_unit', blank=True, null=True)  # Field name made lowercase.
    measurements_meanbloodpressure_isinrange = models.BooleanField(db_column='measurements_meanBloodPressure_isInRange', blank=True, null=True)  # Field name made lowercase.
    measurements_pulse_value = models.IntegerField(blank=True, null=True)
    measurements_pulse_unit = models.TextField(blank=True, null=True)
    measurements_pulse_isinrange = models.BooleanField(db_column='measurements_pulse_isInRange', blank=True, null=True)  # Field name made lowercase.
    measurements_systolicbloodpressure_value = models.BigIntegerField(db_column='measurements_systolicBloodPressure_value', blank=True, null=True)  # Field name made lowercase.
    measurements_systolicbloodpressure_unit = models.TextField(db_column='measurements_systolicBloodPressure_unit', blank=True, null=True)  # Field name made lowercase.
    measurements_systolicbloodpressure_isinrange = models.BooleanField(db_column='measurements_systolicBloodPressure_isInRange', blank=True, null=True)  # Field name made lowercase.
    measurements_ambienttemperature_value = models.FloatField(db_column='measurements_ambientTemperature_value', blank=True, null=True)  # Field name made lowercase.
    measurements_ambienttemperature_unit = models.TextField(db_column='measurements_ambientTemperature_unit', blank=True, null=True)  # Field name made lowercase.
    measurements_ambienttemperature_isinrange = models.BooleanField(db_column='measurements_ambientTemperature_isInRange', blank=True, null=True)  # Field name made lowercase.
    measurements_annotations_codenumber = models.TextField(db_column='measurements_annotations_codeNumber', blank=True, null=True)  # Field name made lowercase.
    measurements_annotations_mealtag = models.TextField(db_column='measurements_annotations_mealTag', blank=True, null=True)  # Field name made lowercase.
    measurements_glucose_value = models.FloatField(blank=True, null=True)
    measurements_glucose_unit = models.TextField(blank=True, null=True)
    measurements_glucose_isinrange = models.BooleanField(db_column='measurements_glucose_isInRange', blank=True, null=True)  # Field name made lowercase.
    measurements_bodycomposition_value = models.FloatField(db_column='measurements_bodyComposition_value', blank=True, null=True)  # Field name made lowercase.
    measurements_bodycomposition_unit = models.TextField(db_column='measurements_bodyComposition_unit', blank=True, null=True)  # Field name made lowercase.
    measurements_bodycomposition_isinrange = models.BooleanField(db_column='measurements_bodyComposition_isInRange', blank=True, null=True)  # Field name made lowercase.
    measurements_bodyweight_value = models.FloatField(db_column='measurements_bodyWeight_value', blank=True, null=True)  # Field name made lowercase.
    measurements_bodyweight_unit = models.TextField(db_column='measurements_bodyWeight_unit', blank=True, null=True)  # Field name made lowercase.
    measurements_bodyweight_isinrange = models.BooleanField(db_column='measurements_bodyWeight_isInRange', blank=True, null=True)  # Field name made lowercase.
    measurements_cholesterol_value = models.FloatField(blank=True, null=True)
    measurements_cholesterol_unit = models.TextField(blank=True, null=True)
    measurements_cholesterol_isinrange = models.BooleanField(db_column='measurements_cholesterol_isInRange', blank=True, null=True)  # Field name made lowercase.
    measurements_uricacid_value = models.FloatField(blank=True, null=True)
    measurements_uricacid_unit = models.TextField(blank=True, null=True)
    measurements_uricacid_isinrange = models.BooleanField(db_column='measurements_uricacid_isInRange', blank=True, null=True)  # Field name made lowercase.
    measurements_ketone_value = models.FloatField(blank=True, null=True)
    measurements_ketone_unit = models.TextField(blank=True, null=True)
    measurements_ketone_isinrange = models.BooleanField(db_column='measurements_ketone_isInRange', blank=True, null=True)  # Field name made lowercase.
    measurements_hematocrit_value = models.FloatField(blank=True, null=True)
    measurements_hematocrit_unit = models.TextField(blank=True, null=True)
    measurements_hematocrit_isinrange = models.BooleanField(db_column='measurements_hematocrit_isInRange', blank=True, null=True)  # Field name made lowercase.
    measurements_temperature_value = models.FloatField(blank=True, null=True)
    measurements_temperature_unit = models.TextField(blank=True, null=True)
    measurements_temperature_isinrange = models.BooleanField(db_column='measurements_temperature_isInRange', blank=True, null=True)  # Field name made lowercase.
    measurements_spo2_value = models.IntegerField(db_column='measurements_SpO2_value', blank=True, null=True)  # Field name made lowercase.
    measurements_spo2_unit = models.TextField(db_column='measurements_SpO2_unit', blank=True, null=True)  # Field name made lowercase.
    measurements_spo2_isinrange = models.BooleanField(db_column='measurements_SpO2_isInRange', blank=True, null=True)  # Field name made lowercase.
    measurements_device_id = models.TextField(blank=True, null=True)
    measurements_device_serialnumber = models.CharField(max_length=60,db_column='measurements_device_serialNumber', blank=True, null=True)  # text for GW devices Field name made lowercase.
    measurements_device_imei = models.CharField(max_length=60, db_column='measurements_device_IMEI', blank=True, null=True)  # Field name made lowercase.
    measurements_device_manufacturer = models.TextField(blank=True, null=True)
    measurements_device_model = models.TextField(blank=True, null=True)
    measurements_device_timezone = models.TextField(blank=True, null=True)
    measurements_ecgsamples_minvalue = models.SmallIntegerField(db_column='measurements_ecgSamples_minValue', null=True)  # Field name made lowercase.
    measurements_ecgsamples_maxvalue = models.SmallIntegerField(db_column='measurements_ecgSamples_maxValue', null=True)  # Field name made lowercase.
    measurements_ecgsamples_samplerate = models.SmallIntegerField(db_column='measurements_ecgSamples_sampleRate', null=True)  # Field name made lowercase.
    measurements_ecgsamples_samplerateunit = models.TextField(db_column='measurements_ecgSamples_sampleRateUnit', null=True)  # Field name made lowercase.
    measurements_ecgsamples_factor = models.FloatField(db_column='measurements_ecgSamples_factor', null=True)  # Field name made lowercase.
    measurements_ecgsamples_factorunit = models.TextField(db_column='measurements_ecgSamples_factorUnit', null=True)  # Field name made lowercase.
    measurements_ecgsamples_samples = models.TextField(db_column='measurements_ecgSamples_samples', null=True)  # Field name made lowercase.
    device_additionalattributes_currentdevicetime = models.FloatField(db_column='device_additionalAttributes_currentDeviceTime', blank=True, null=True)  # Field name made lowercase.
    device_additionalattributes_devicetype = models.TextField(db_column='device_additionalAttributes_deviceType', blank=True, null=True)  # Field name made lowercase.
    device_additionalattributes_devicever = models.TextField(db_column='device_additionalAttributes_deviceVer', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False - removed to let django manage
        db_table = 'eliot2'
        verbose_name = 'eliot'
        verbose_name_plural = "eliot"
        ordering = ['-measurements_timestamp']

    def save(self, *args, **kwargs):
        # 'measurements_timestamp': '2022-07-17T16:16:39+01:00' normallly except "2022-03-01T07:26:00Z"
        # 'metadata_receivedTime': '2022-07-17T16:16:39.791797Z' normally
        # PM100 PDF (img) and RAW (string) to measurements_ecgSamples_samples
        # D40g / BP800 should be mts = "2022-07-19T18:49:00+01:00"
        # measurements_timestamp 2022-07-19 18:34:00+01:0 ERROR t must be in YYYY-MM-DD HH:MM[:ss[.uuuuuu
        # metadata_receivedtime 2022-07-19 17:35:16.262063073
# BC800
#         measurements_timestamp 2022-07-19 20:11:13.464097332+00:00
# metadata_receivedtime 2022-07-19 20:11:13.464097128
        try:
            self.measurements_timestamp = pd.to_datetime(self.measurements_timestamp, format='%Y-%m-%dT%H:%M:%S%Z').replace(tzinfo=None)
        except Exception as e:
            #"2022-03-01T07:26:00Z"
            self.measurements_timestamp = pd.to_datetime(self.measurements_timestamp, format='%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=None)
        else :
            self.measurements_timestamp = pd.to_datetime(self.measurements_timestamp, format='%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=None)

        try :
            self.metadata_receivedtime = pd.to_datetime(self.metadata_receivedtime, format='%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=None)
        except Exception as e:
            with open('eliot2_error.log', 'a') as f:
                f.write(f'\n unknown format receivedtime in eliot {e}\n  {self.metadata_receivedtime}')

        if self.device_model == 'BS-2001-G1': # remove col 'measurements_annotations_measuredUnit'
            self.measurements_annotations_measuredunit = None

        elif self.device_model == 'PM100': # convert PDF to img, RAW to string save to measurements_ecgSamples_samples)
            if self.measurements_documents_ecgreportbase64pdf:
                base64_img = self.measurements_documents_ecgreportbase64pdf
                self.measurements_ecgsamples_samples = base64_img #.encode('utf-8')
                #self.measurements_documents_ecgreportbase64pdf = None
            else: # RAW
                self.measurements_ecgsamples_samples = json.dumps(self.measurements_ecgsamples_samples) #json.dumps(data['measurements']["ecgSamples"]['samples']))
        elif self.device_model == 'GW9017':
            # 'measurements_device_serialnumber' expected a number but got '312942014000992E' - textfield
            #TextField
            #'measurements_device_serialnumber' expected a number but got '825522022026250B'
            pass

# GW error  Field 'measurements_device_serialnumber' expected a number but got '825522022026250B'.
        with open('eliot.json', 'a') as f:
            f.write(f'\n db hit @ {dt.now().isoformat()}\n')
            f.write(f'Recieved @: {self.metadata_receivedtime}  Measured @ {self.measurements_timestamp}\n')
            for k,v in self.__dict__.items():
                f.write(f"{k} {v}\n")

        super().save(*args, **kwargs)  # Call the "real" save() method.


""" 
(base) ab@awsb:~$ jq ".metadata.receivedTime, .measurements.timestamp, .device.model" jsondata2.json > rt_ms_device.txt

mts = "2021-10-27T11:31:17.584462798Z"
pd.to_datetime(mts, format='%Y-%m-%dT%H:%M:%S%Z')
Timestamp('2021-10-27 11:31:17.584462798+0000', tz='UTC')

receivedtime
mts = '2022-07-19T17:35:16.262063073Z'
pd.to_datetime(mts, format='%Y-%m-%dT%H:%M:%S.%fZ')
Timestamp('2022-07-19 17:35:16.262063073')

mts = "2022-07-19T18:49:00+01:00"
pd.to_datetime(mts, format='%Y-%m-%dT%H:%M:%S%Z')


2022-07-05T16:12:08.201604909Z"
"2022-07-05T16:09:37Z"
"PM100"
"2022-07-05T21:02:13.264989099Z"
"2022-07-05T14:38:00+02:00"
"GW9017"
"2022-07-05T21:03:16.995518972Z"
"2022-07-05T23:03:00+02:00"
"GW9017"
"2022-07-05T21:05:25.861796272Z"
"2022-07-05T23:05:00+02:00"
"GW9017"
"2022-07-05T21:09:13.805799407Z"
"2022-07-05T21:06:54Z"
"PM100"
"2022-07-06T03:29:11.438077923Z"
"2022-07-06T05:28:00+02:00"
"BP800"
"2022-07-06T06:07:55.631430708Z"
"2022-07-06T08:07:13+02:00"
"BC800"
"2022-07-06T11:06:26.91523343Z"
"2022-07-06T13:05:00+02:00"
"2021-12-22T21:57:20.03923015Z"
"2021-12-22T21:57:20.039230263Z"
"BS-2001-G1"
"2021-12-28T07:32:40.754381973Z"
"2021-12-28T08:28:01+01:00"
"BP800"
"2021-12-28T07:32:46.692390116Z"
"2021-12-28T08:25:00+01:00"
"BP800"
"2021-12-28T07:33:16.034609664Z"
"2021-12-28T08:22:00+01:00"
"BP800"
"2021-12-29T13:29:56.218123814Z"
"2021-12-29T08:28:00-05:00"
"D40G"


"""
