# update latest POST for eliot : Lightsail version Mapi2
# try redis as storage for png and pdf
import redis
import pickle
import pandas as pd
import numpy as np
import sys
sys.path.append("/home/bitnami/sharepoint")
sys.path.append("..")
from Mapi2 import DBconx
from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
import base64
from os.path import exists
from os import mknod

class TempFileURL:
    '''
    - save created pdf/png to share folder
    - input is a PDF page 1 of 2 from PIL image
    - in df and redis store file location URL relative to ../sharepoint so bokeh can display .png
    '''

    def __init__(self, im, cid, ts, r, static_folder):
        self.cid = cid
        self.ts = ts #2022-11-10 10:12:39
        self.static_folder = static_folder
        self.url = f'{self.static_folder}/PM100_{self.cid}_{self.ts}.pdf'
        self.png = f'{self.static_folder}/PM100_{self.cid}_{self.ts}.png'
        if not exists(self.url):
            mknod(self.url)
            #mknod(self.png)
            im_pages = convert_from_bytes(base64.b64decode(im))
            for i in im_pages:
                i.save(self.url, append=True)

            self.pngs =convert_from_path(self.url)
            self.stackPNG()
            print(f"Created a Named Temporary File {self.url} ")
        r.set(f'PM100_{self.cid}_{self.ts}.png', im)  # save image png with filename key

    def stackPNG(self):
        sz = 0.2
        resz = (int(self.pngs[0].width * sz), int(self.pngs[0].height * sz))
        hx2 = (int(self.pngs[0].width * sz), int(self.pngs[0].height * sz * 2))
        new = Image.new('RGB', (hx2))
        new.paste(self.pngs[0].resize(resz), (0,0))
        new.paste(self.pngs[1].resize(resz), (0, int(new.height * 0.5)))
        new.save(self.png, format='png')

def run_redis(device_model):

    r = redis.Redis()

    if device_model == 'PM100':
        # ECG data DataTable ***** NOTE eliot2_bk for testing ********
        sql = """SELECT device_IMEI, device_model, device_timezone, measurements_timestamp, metadata_measurementType, metadata_correlationid,
        measurements_ecgSamples_minValue, measurements_ecgSamples_maxValue, measurements_ecgSamples_sampleRate, 
        measurements_ecgSamples_sampleRateUnit, measurements_ecgSamples_factor, measurements_ecgSamples_factorUnit, 
        measurements_ecgSamples_samples from eliot2 WHERE metadata_measurementType = 'ECG'"""

        cols = ['IMEI', 'model', 'tz', 'ts', 'type', 'ucid', 'min', 'max', 'rate', 'rateunit', 'factor', 'factorunit',
                'samples']

        static_folder = '/home/bitnami/bokeh/app/eliot/static'  # PROD bokeh server = eliot/static
        # static_folder = 'static'  # DEV oC/eliot/static
        relative_folder = '/eliot/static'  # static_folder URL replaced by this value for bokeh display

        dfecg = pd.DataFrame([i for i in DBconx('T').query(sql)], columns=cols)
        dfecg['format'] = 'pdf'
        dfecg.loc[dfecg.samples.str.startswith('[{'), 'format'] = 'raw'

        r = redis.Redis()
        dfecg['aurl'] = dfecg[dfecg['format'] == 'pdf'].apply(
            lambda x: TempFileURL(x.samples, x.ucid, x.ts.strftime('%y%m%d_%H%M%S'), r, static_folder).png, axis=1)
        dfecg['aurl'] = dfecg['aurl'].str.replace(static_folder, relative_folder, regex=False)
        r.set("eliot_dfecg", pickle.dumps(dfecg))  #

    elif device_model in ('BC800', 'BS-2001-G1'):   #W550?
        # BC data incl transtek BS-2001 'BodyWeight'
        sql = "SELECT device_IMEI, device_model, measurements_bodyComposition_value," \
              " measurements_bodyWeight_value, measurements_timestamp, colour " \
              "FROM `eliot2` where device_model LIKE 'BS%' OR device_model LIKE 'BC%' "
        tuptup = DBconx('T').query(
            sql)  # "SELECT device_IMEI, measurements_bodyComposition_value, measurements_bodyWeight_value, measurements_timestamp, colour from eliot2 WHERE metadata_measurementType = 'BodyWeightComposition'")

        dfbc = pd.DataFrame([i for i in tuptup], columns=['device_IMEI', 'm', 'r', 'w', 'ts', 'colour'])
        dfbc.loc[dfbc.m == 'BS-2001-G1', 'w'] = dfbc.w * 0.001  # convert BS to Kg
        dfbc.loc[dfbc.m == 'BS-2001-G1', 'r'] = 0  # convert o
        dfbc.set_index('ts', drop=True, inplace=True)
        dfbc = dfbc.sort_index(ascending=True)
        dfbc.r.replace(0, pd.NA, inplace=True)
        dfbc = dfbc.assign(bmr=0, fat=0, h2o=0, bone=0,
                           id=np.arange(len(dfbc)))  # initial bmr line that will be overridden in BodyComp
        r.set("eliot_dfbc", pickle.dumps(dfbc))

    else : # all others TODO filter by device

        cols = ['device_IMEI', 'device_model','measurements_timestamp', 'measurements_pulse_value','measurements_pulse_unit', 'measurements_systolicBloodPressure_value',
                'measurements_diastolicBloodPressure_value', 'measurements_glucose_value', 'measurements_glucose_unit', 'measurements_bodyWeight_value', 'r',
                'measurements_cholesterol_value', 'measurements_cholesterol_unit',
                'measurements_uricacid_value', 'measurements_uricacid_unit',
                'measurements_ketone_value', 'measurements_ketone_unit',
                'measurements_temperature_value', 'measurements_temperature_unit',
                'measurements_SpO2_value', 'measurements_SpO2_unit',
                'metadata_measurementType'
                ]

        asql="SELECT device_IMEI, device_model, measurements_timestamp, " \
             "measurements_pulse_value, measurements_pulse_unit, measurements_systolicBloodPressure_value," \
        "measurements_diastolicBloodPressure_value, measurements_glucose_value, measurements_glucose_unit, " \
        "measurements_bodyWeight_value, measurements_bodyComposition_value, measurements_cholesterol_value, " \
        "measurements_cholesterol_unit, measurements_uricacid_value, measurements_uricacid_unit," \
                     "measurements_ketone_value, measurements_ketone_unit," \
                     "measurements_temperature_value, measurements_temperature_unit," \
                     "measurements_SpO2_value, measurements_SpO2_unit," \
                     "metadata_measurementType from eliot2"

        tuptup = DBconx('T').query(asql)
        dfall = pd.DataFrame([i for i in tuptup], columns=cols) #.astype({'imei': np.int64, 'count' : np.int16, 'org': np.int8})
        #dfall = pd.DataFrame([i for i in dba], columns=cols)
        dfall.set_index('measurements_timestamp', drop=True, inplace=True)
        dfall = dfall.sort_index(ascending=True)


        for bm in ['pulse','cholesterol', 'ketone', 'uricacid', 'glucose', 'temperature', 'SpO2']:
            bmv = f'measurements_{bm}_value'
            bmu = f'measurements_{bm}_unit'
            dfall.loc[dfall[bmv].notnull(),'value'] = dfall[bmv]
            dfall.loc[dfall[bmu].notnull(),'unit'] = dfall[bmu]


      # BP data incl transtek LS802-GP
        #dfbp = dfall.loc[dfall['metadata_measurementType'] != 'BodyWeightComposition']
        dfbp = dfall.loc[(dfall.device_model.str.contains('BP800')) |
                        (dfall.device_model.str.contains('D40')) |
                        (dfall.device_model.str.startswith('LS802'))
                        ]
        # Gtel data
        dfgtel = dfall.loc[dfall['device_model'] == 'GTEL']

        # GW data
        dfgw = dfall.loc[dfall['device_model'] == 'GW9017']


        r.set("eliot_dfbp", pickle.dumps(dfbp))  #
        r.set("eliot_dfall", pickle.dumps(dfall))  #
        r.set("eliot_dfgtel", pickle.dumps(dfgtel))  #
        r.set("eliot_dfgw", pickle.dumps(dfgw))  #
    r.close()

if __name__ == "__main__":

    run_redis()