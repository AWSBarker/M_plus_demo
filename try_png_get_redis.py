# get ECG im data (longtext - bae64 image as string) in redis
# redis key = filename.

import redis
import pickle
import sys
sys.path.append("/home/bitnami/sharepoint")
sys.path.append("..")
import base64
import time

st = time.time()
r = redis.Redis()

df = pickle.loads(r.get("eliot_dfbc"))

print(df.tail())
exit()


base64_im1 = r.get("im1") #base64 image as bytes

with open('a.pdf', 'wb') as f:
    decoded_image_data = base64.decodebytes(base64_im1)
    f.write(decoded_image_data)

print(f'finished in {time.time() - st}s')


#dfecg['aurl'] = dfecg[dfecg['format'] == 'pdf'].apply(lambda x: TempFileURL(x.samples, x.ucid, x.ts, r).png, axis=1)
