from rest_framework import serializers
from .models import Eliot

class EliotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Eliot
        fields = (
                  "device_model", "device_imei" ,  "device_timezone",
                  "measurements_timestamp" ,  "metadata_correlationid" , "metadata_receivedtime" ,
                  "measurements_annotations_irregularheartbeat" ,
                  "measurements_systolicbloodpressure_value",
                  "measurements_diastolicbloodpressure_value" ,
                  "measurements_pulse_value",
                  "measurements_glucose_value",
                  "measurements_bodycomposition_value",
                  "measurements_bodyweight_value", "measurements_bodyweight_unit",
                  "measurements_cholesterol_value", "measurements_cholesterol_unit",
                  "measurements_uricacid_value", "measurements_uricacid_unit",
                  "measurements_ketone_value", "measurements_ketone_unit",
                  "measurements_hematocrit_value", "measurements_hematocrit_unit",
                  "measurements_temperature_value", "measurements_temperature_unit",
                  "measurements_spo2_value", "measurements_spo2_unit" )

#        fields = '__all__' #('metadata_correlationid','measurements_timestamp','device_imei') #, 'device_imsi') #'__all__'

#        fields = ("measurements_timestamp" ,  "metadata_correlationid" , "metadata_receivedtime" ,
#          "device_imei" , "measurements_annotations_irregularheartbeat" , "measurements_systolicbloodpressure_value",
#          "measurements_diastolicbloodpressure_value" ,  "measurements_pulse_value")

#        fields = ('metadata_correlationid','measurements_timestamp','device_imei') #, 'device_imsi') #'__all__'

