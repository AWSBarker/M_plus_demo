# random POST of ECG JSON dummy measures to webhook (../itasc/bp/)
# ENUSRE TO EDIT aurl to webhook
import requests
from requests import exceptions
from flatdict import FlatDict
import random, string
from datetime import datetime as dt
import json

with open("PM100PDF_MedisanteStandard_.json", 'r') as f:
	json_file = f.read()

data = json.loads(json_file)

# dummy data fields
rimei = random.randrange(358173054439512, 358173054439527)
rts = dt.now().strftime("%Y-%m-%dT%H:%M:%SZ")
mts = dt.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
cid1 = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
cid2 = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
cid3 = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
cid4 = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
cid5 = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
cid = '-'.join((cid1,cid2,cid3,cid4,cid5)).lower()

#aurl = 'https://demo.medisante-group.com/eliot/bp'
aurl = 'http://127.0.0.1:8000/eliot/bp'

data['metadata']['correlationId'] = cid
data['metadata']['receivedTime'] = mts
data['device']['IMEI'] = rimei
data['measurements']['timestamp'] = rts

flat_dict = FlatDict(data, delimiter='_')

#try:
response = requests.post(aurl, json= data, verify=False)
print(response.status_code)
#except requests.exceptions.SSLError as e:
#    print(f'ignored SSL {e}')

