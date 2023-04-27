# random POST of D40g JSON dummy measures to webhook (../itasc/bp/)
# ENUSRE TO EDIT aurl to webhook
import requests
from requests import exceptions
from flatdict import FlatDict
import random, string
from datetime import datetime as dt

# dummy data fields
#  unknown post save error in eliot ['“2022-07-19 18:34:00+01:0” value has an invalid format. It must be in YYYY-MM-DD HH:MM[:ss[.uuuuuu
rsys = random.randrange(125, 155)
rdia = random.randrange(75, 89)
rpulse = random.randrange(55, 100)
rimei = random.randrange(358173054439512, 358173054439527)
#rts = dt.now().strftime("%Y-%m-%dT%H:%M:%SZ")
#mts = dt.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        # 'measurements_timestamp': '2022-07-17T16:16:39+01:00' normallly except "2022-03-01T07:26:00Z"
        # 'metadata_receivedTime': '2022-07-17T16:16:39.791797Z' normally
mts = dt.now().strftime("%Y-%m-%d %H:%M:%S.%fZ") # BC800 2022-07-19 20:11:13.464097332+00:00
rts = dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")
cid1 = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
cid2 = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
cid3 = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
cid4 = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
cid5 = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
cid = '-'.join((cid1,cid2,cid3,cid4,cid5)).lower()

aurl = 'https://demo.medisante-group.com/eliot/bp'
burl = 'https://demo.medisante-group.com/itasc/bp/'
curl = 'https://awsb.ddns.net/eliot/bp'
allurl = [aurl,burl, curl]

#aurl = 'http://127.0.0.1:8000/eliot/bp'

load = {"metadata":
            {"correlationId": cid,
             "receivedTime": mts,
             "deviceGroups": "",
             "measurementType": "BloodPressure"},
        "device": {"id": "TaiDoc:BP800:001-326171744000070A-47",
                   "serialNumber": "001-326171744000070A-47",
                   "IMEI": rimei,
                   "IMSI": "204046206994346",
                   "manufacturer": "TaiDoc",
                   "model": "BP800",
                   "timezone": "Europe/London"},
        "measurements": {"annotations": {"averageMeasurement": 'false', "irregularHeartBeat": 'false'},
                         "diastolicBloodPressure": {"value": rdia, "unit": "mmHg", "isInRange": 'false'},
                         "meanBloodPressure": {"value": 99, "unit": "mmHg", "isInRange": 'true'},
                         "pulse": {"value": rpulse, "unit": "bpm", "isInRange": 'true'},
                         "systolicBloodPressure": {"value": rsys, "unit": "mmHg", "isInRange": 'false'},
                         "timestamp": rts}
        }
flat_dict = FlatDict(load, delimiter='_')
try :
    for u in allurl:
        response = requests.post(u, json= load, verify=False)
        print(f'{u}, with response {response.status_code}')
except requests.exceptions.SSLError as e:
    print(f'ignored SSL {e}')
    pass

"""
load = {"metadata":
            {"correlationId": "c418e0b5-8d6e-4237-accf-e30c40a9b5b9",
             "receivedTime": "2022-05-18T12:46:25.383136859Z",
             "deviceGroups": "",
             "measurementType": "BloodPressure"},
        "device": {"id": "TaiDoc:BP800:001-326171744000070A-47",
                   "serialNumber": "001-326171744000070A-47",
                   "IMEI": "358173054439511",
                   "IMSI": "204046206994346",
                   "manufacturer": "TaiDoc",
                   "model": "BP800",
                   "timezone": "Europe/London"},
        "measurements": {"annotations": {"averageMeasurement": 'false', "irregularHeartBeat": 'false'},
                         "diastolicBloodPressure": {"value": 76, "unit": "mmHg", "isInRange": 'true'},
                         "meanBloodPressure": {"value": 91, "unit": "mmHg", "isInRange": 'true'},
                         "pulse": {"value": 65, "unit": "bpm", "isInRange": 'true'},
                         "systolicBloodPressure": {"value": 131, "unit": "mmHg", "isInRange": 'true'},
                         "timestamp": "2022-05-18T13:45:00+01:00"}
        }
#load = {"correlationId": "c418e0b5-8d6e-4237-accf-e30c40a9b5c1", "IMEI": 358173054439520, "timestamp": "2022-05-18T13:46:01+01:00"}

# json "99999" seems to 'convert' to 99999 with BigInteger
# mariadb takes Boolean as tinyint so False is 0
"""
