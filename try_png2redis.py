# try store ECG im data (longtext - bae64 image as string) in redis
# redis key = filename.

import redis
import pandas as pd
import sys
sys.path.append("/home/bitnami/sharepoint")
sys.path.append("..")
from Mapi2 import DBconx
import base64

# ECG data DataTable ***** NOTE eliot2_bk for testing ********
sql = """SELECT device_IMEI, device_model, device_timezone, measurements_timestamp, metadata_measurementType, metadata_correlationid,
measurements_ecgSamples_minValue, measurements_ecgSamples_maxValue, measurements_ecgSamples_sampleRate, 
measurements_ecgSamples_sampleRateUnit, measurements_ecgSamples_factor, measurements_ecgSamples_factorUnit, 
measurements_ecgSamples_samples from eliot2 WHERE metadata_measurementType = 'ECG'"""

cols = ['IMEI', 'model', 'tz', 'ts', 'type', 'ucid', 'min', 'max', 'rate', 'rateunit', 'factor', 'factorunit',
        'samples']

dfecg = pd.DataFrame([i for i in DBconx('T').query(sql)], columns=cols)
dfecg['format'] = 'pdf'
dfecg.loc[dfecg.samples.str.startswith('[{'), 'format'] = 'raw'

r = redis.Redis()
r.set('im1.png', dfecg.samples[-1:].values[0], 60)

base64_im1 = r.get("im1") #base64 image as bytes

with open('a.pdf', 'wb') as f:
    decoded_image_data = base64.decodebytes(base64_im1)
    f.write(decoded_image_data)


#dfecg['aurl'] = dfecg[dfecg['format'] == 'pdf'].apply(lambda x: TempFileURL(x.samples, x.ucid, x.ts, r).png, axis=1)
