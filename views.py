# added ECG
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

import MySQLdb
import MySQLdb.cursors
import pandas as pd
from bokeh.embed import server_document, components, server_session
from bokeh.client import pull_session
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, CDSView, GroupFilter, BooleanFilter, Select, DatetimeTickFormatter, HoverTool, \
	NumeralTickFormatter, DateRangeSlider
from bokeh.plotting import figure, show
from bokeh.palettes import Category20c_20, Category20b_20
import datetime as dt
import requests
import json
from sqlalchemy import create_engine, exc

def home(request):

	def db(sql):
		connection = MySQLdb.connect(host='192.168.1.173', port=3306, user='pi',
									 password='7914920', db='Health', cursorclass=MySQLdb.cursors.DictCursor)
		conn = connection.cursor()  # setup the dropdowns dicts
		conn.execute(sql)  # "SELECT * FROM countries")
		r = conn.fetchall()  # tuple of dicts ({},{}..  ,)
		conn.close()
		connection.close()
		return r

	my_dict = {'basedir' : "", 'script' : "", 'div' : "", 'updated' : ""}
	return render(request, 'home/home.html', my_dict)

def iframe_view(request):
	bokeh_server_url = "https://awsb.ddns.net/flight"
	context = {"graphic":"Slider", "ifr": bokeh_server_url}
	return render(request, 'home/iframe.html' , context)

# /eliot/bp
'''

GW

[SQL: INSERT INTO eliot2 (`metadata_correlationId`, `metadata_receivedTime`, `metadata_deviceGroups`, `metadata_measurementType`, device_id, `device_serialNumber`, `device_IMEI`, device_manufacturer, device_model, device_timezone, `measurements_SpO2_value`, `measurements_SpO2_unit`, `measurements_SpO2_isInRange`, measurements_device_id, `measurements_device_serialNumber`, `measurements_device_IMEI`, measurements_device_manufacturer, measurements_device_model, measurements_device_timezone, measurements_pulse_value, measurements_pulse_unit, `measurements_pulse_isInRange`, measurements_timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)]
[parameters: ('8f8e12df-6bbb-4d8a-a4fe-f61ab48c5cb2', '2021-05-13T14:16:44.334477311Z', 'N/A', 'SpO2', 'Fora:GW9017:9017720280000026', '9017720280000026', '355442076664122', 'Fora', 'GW9017', 'UTC', 99, '%', 1, 'Fora:PO200:825522022026250B', '825522022026250B', '', 'Fora', 'PO200', 'UTC', 53, 'bmp', 1, '2021-05-13T14:16:44.334477666Z')]
(Background on this error at: http://sqlalche.me/e/13/e3q8) 

error with db (MySQLdb._exceptions.OperationalError) (1054, "Unknown column 'measurements_device_id' in 'field list'")
[SQL: INSERT INTO eliot2 (`metadata_correlationId`, `metadata_receivedTime`, `metadata_deviceGroups`, `metadata_measurementType`, device_id, `device_serialNumber`, `device_IMEI`, device_manufacturer, device_model, device_timezone, 
measurements_device_id, `measurements_device_serialNumber`, `measurements_device_IMEI`, measurements_device_manufacturer, measurements_device_model, measurements_device_timezone, 
`measurements_diastolicBloodPressure_value`, `measurements_diastolicBloodPressure_unit`, `measurements_diastolicBloodPressure_isInRange`, `measurements_meanBloodPressure_value`, `measurements_meanBloodPressure_unit`, `measurements_meanBloodPressure_isInRange`, measurements_pulse_value, measurements_pulse_unit, `measurements_pulse_isInRange`, `measurements_systolicBloodPressure_value`, `measurements_systolicBloodPressure_unit`, `measurements_systolicBloodPressure_isInRange`, measurements_timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)]
[parameters: ('b71879bd-eaa1-439c-bd8a-c8a7fcda1622', '2021-05-13T10:57:53.84001981Z', 'N/A', 'BloodPressure', 'Fora:GW9017:9017720280000026', '9017720280000026', '355442076664122', 'Fora', 'GW9017', 'UTC', 'Fora:P30:312942014000992E', '312942014000992E', '', 'Fora', 'P30', 'UTC', 91, 'mmHg', 1, 107, 'mmHg', 1, 78, 'bpm', 1, 141, 'mmHg', 1, '2021-05-13T10:57:53.840020013Z')]
(Background on this error at: http://sqlalche.me/e/13/e3q8) 
 id = head : {'Host': 'awsb.ddns.net', 'Connection': 'upgrade', 'X-Forwarded-Proto': 'https', 'X-Forwarded-For': '3.125.181.80, 192.168.1.173', 'X-Original-Uri': '/eliot/bp', 'X-Server-Port': '443', 'X-Server-Addr': '192.168.1.106', 'X-Real-Ip': '192.168.1.173', 'Content-Length': '787', 'X-Forwarded-Port': 'https', 'X-Correlation-Id': 'b71879bd-eaa1-439c-bd8a-c8a7fcda1622', 'X-Amzn-Trace-Id': 'Root=1-609d0631-2ea8ab10399c82ba0f9a6fc3;Parent=a01bc16546842cde;Sampled=1', 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Basic QVdTQjpBV1NC', 'Accept': 'application/json', 'Accept-Encoding': 'gzip', 'User-Agent': 'Go-http-client/2.0'}
type :  <class 'dict'> 
 
 data : {'metadata': {'correlationId': 'b71879bd-eaa1-439c-bd8a-c8a7fcda1622', 'receivedTime': '2021-05-13T10:57:53.84001981Z', 'deviceGroups': [], 'measurementType': 'BloodPressure'}, 
 'device': {'id': 'Fora:GW9017:9017720280000026', 'serialNumber': '9017720280000026', 'IMEI': '355442076664122', 'manufacturer': 'Fora', 'model': 'GW9017', 'timezone': 'UTC'}, 
 'measurements': {'device': {'id': 'Fora:P30:312942014000992E', 'serialNumber': '312942014000992E', 'IMEI': '', 'manufacturer': 'Fora', 'model': 'P30', 'timezone': 'UTC'}, 
 	'diastolicBloodPressure': {'value': 91, 'unit': 'mmHg', 'isInRange': True}, 'meanBloodPressure': {'value': 107, 'unit': 'mmHg', 'isInRange': True}, 'pulse': {'value': 78, 'unit': 'bpm', 'isInRange': True}, 'systolicBloodPressure': {'value': 141, 'unit': 'mmHg', 'isInRange': True}, 'timestamp': '2021-05-13T10:57:53.840020013Z'}}

Gtel
SQL: INSERT INTO eliot2 (`metadata_correlationId`, `metadata_receivedTime`, `metadata_deviceGroups`, `metadata_measurementType`, device_id, `device_serialNumber`, `device_IMEI`, `device_IMSI`, device_manufacturer, device_model, device_timezone, `device_additionalAttributes_deviceVer`, measurements_cholesterol_value, measurements_cholesterol_unit, `measurements_cholesterol_isInRange`, measurements_timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)]
[parameters: ('ac962b83-a9db-4e0a-bdb0-3e4e237fea22', '2021-05-08T09:10:20.922129883Z', 'N/A', 'Cholesterol', 'TaiDoc:GTEL:412222032002106B', '412222032002106B', '900000000000008', '354033090695159', 'TaiDoc', 'GTEL', 'UTC', 'V1 2020.09.02', 189, 'mg/dL', 1, '2021-05-08T09:10:20.922130108Z')]
(Background on this error at: http://sqlalche.me/e/13/e3q8) 

 id = head : {'Host': 'awsb.ddns.net', 'Connection': 'upgrade', 'X-Forwarded-Proto': 'https', 'X-Forwarded-For': '18.184.195.98, 192.168.1.173', 'X-Original-Uri': '/eliot/bp', 'X-Server-Port': '443', 'X-Server-Addr': '192.168.1.106', 'X-Real-Ip': '192.168.1.173', 'Content-Length': '529', 'X-Forwarded-Port': 'https', 'X-Correlation-Id': 'ac962b83-a9db-4e0a-bdb0-3e4e237fea22', 'X-Amzn-Trace-Id': 'Root=1-6096557d-75f768c76bea0a805aa294eb;Parent=7394bf22a5134547;Sampled=1', 'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Basic QVdTQjpBV1NC', 'Accept': 'application/json', 'Accept-Encoding': 'gzip', 'User-Agent': 'Go-http-client/2.0'}
type :  <class 'dict'> 
 data : {'metadata': {'correlationId': 'ac962b83-a9db-4e0a-bdb0-3e4e237fea22', 'receivedTime': '2021-05-08T09:10:20.922129883Z', 'deviceGroups': [], 'measurementType': 'Cholesterol'}, 
 'device': {'id': 'TaiDoc:GTEL:412222032002106B', 'serialNumber': '412222032002106B', 'IMEI': '900000000000008', 'IMSI': '354033090695159', 'manufacturer': 'TaiDoc', 'model': 'GTEL', 'timezone': 'UTC', 'additionalAttributes': {'deviceVer': 'V1 2020.09.02'}}, 
 'measurements': {'cholesterol': {'value': 189, 'unit': 'mg/dL', 'isInRange': True}, 'timestamp': '2021-05-08T09:10:20.922130108Z'}}

 measurements_bodyComposition_value, float
            measurements_bodyComposition_unit, smalltext
            measurements_bodyComposition_isInRange bool
 measurements_bodyComposition_bodyWeight, float
            measurements_bodyWeight_unit small text
            measurements_bodyWeight_isInRange bool
metadata_correlationId,metadata_receivedTime,metadata_deviceGroups,metadata_measurementType,
device_id,device_serialNumber,device_IMEI,device_IMSI,device_manufacturer,device_model,device_timezone,
device_additionalAttributes_currentDeviceTime,device_additionalAttributes_deviceType,device_additionalAttributes_deviceVer,
measurements_bodyComposition_value,measurements_bodyComposition_unit,measurements_bodyComposition_isInRange,
measurements_bodyWeight_value,measurements_bodyWeight_unit,measurements_bodyWeight_isInRange,measurements_timestamp
0,440e7d04-8fa7-47aa-a98b-86eba1a65b32,2020-09-27T11:23:39.869332582Z,[],BodyWeightComposition,EBMTech:BC800:003-204046206948494-25,003-204046206948494-25,900000000000003,204046206948494,EBMTech,BC800 3G,UTC,0.000000,BC800 3G,V1.0,517,Ω,True,64.7,kg,True,2020-09-27T11:23:39.869332689Z
'''

@csrf_exempt
#@require_POST
def eliot(request):
	engine = create_engine('mysql+mysqldb://pi:7914920@192.168.1.173:3306/Health?charset=utf8')

	if request.method == 'POST':
		head = request.headers
		jsondict = json.loads(request.body) #request.body) # dict {{metadata},{device },{measurements}}
		data_df = pd.json_normalize(jsondict, sep='_')  # field.ref_values
		data_df['metadata_deviceGroups'] = "N/A"
		#data.to_csv('/home/ab/data.csv', index=False)
		# determine device type "metadata_measurementType": "BloodPressure" or "BodyWeightComposition
		# actuall doest matter which other values = null
		# transtek'model': 'BS-2001-G1' remove 'measurements_annotations_measuredUnit'
		try:
			if data_df.metadata_measurementType[0] == 'BodyWeightComposition':
				with engine.connect() as con:
					data_df.to_sql('eliot2', con=con, if_exists='append', index=False)
			elif data_df.device_model[0] == 'BS-2001-G1':
				with engine.connect() as con:
				# remove col 'measurements_annotations_measuredUnit'
					data_df.drop(columns=['measurements_annotations_measuredUnit'], axis=1, inplace=True)
					data_df.to_sql('eliot2', con=con, if_exists='append', index=False)

			elif data_df.device_model[0] == 'PM100':
				if jsondict['measurements'].keys().__contains__('documents'): # a PDF
					base64_img = jsondict['measurements']['documents']['ecgReportBase64PDF']
					#base64_img_bytes = base64_img.encode('utf-8')
					jsondatatuple = (data_df.measurements_timestamp[0], base64_img.encode('utf-8'))
					data_df.drop(columns="measurements_documents_ecgReportBase64PDF", inplace=True)
				else: # RAW
					data_df.drop(columns="measurements_ecgSamples_samples", inplace=True)
					jsondatatuple = (data_df.measurements_timestamp[0], json.dumps(data_df['measurements']["ecgSamples"]['samples'])) #json.dumps(data['measurements']["ecgSamples"]['samples']))
				with engine.connect() as con:
					data_df.to_sql('eliot2', con=con, if_exists='append', index=False)
					sql = """INSERT INTO eliot2 (measurements_timestamp, measurements_ecgSamples_samples) VALUES(%s,%s) ON DUPLICATE KEY UPDATE measurements_timestamp = VALUES(measurements_timestamp), measurements_ecgSamples_samples = VALUES(measurements_ecgSamples_samples)""" #, metadata_correlationId = VALUES(metadata_correlationId)

				try:
					db = MySQLdb.connect(host='192.168.1.173', port=3306, user='pi', password='7914920', db='Health', charset='utf8')
					with db.cursor() as cur:# setup the dropdowns dicts
						a = cur.execute(sql, jsondatatuple) #"SELECT * FROM countries")
						db.commit()
						print(f'samples data updated {a}')
				except MySQLdb.Error as e:
						print(f'mysql error {e}')
				finally:
					if db.open:
						db.close()

			else: # BloodPessure (redundant but incase required)
				with engine.connect() as con:
					data_df.to_sql('eliot2', con=con, if_exists='append', index=False)

			with open('/home/ab/jsondata2.json', 'a') as j:
				json.dump(jsondict, j)

		except exc.SQLAlchemyError as e:
			with open('/home/ab/eliot2_error.log', 'a') as f:
				f.write(f'\n {dt.datetime.now().isoformat()}\n')
				f.write(f'\n error with db {e} \n id = ')
				f.write(f'head : {head}\n')
				f.write(f'type :  {type(jsondict)} \n data : {str(jsondict)}\n')
		except Exception as e:
			with open('/home/ab/eliot2_error.log', 'a') as f:
				f.write(f'\n {dt.datetime.now().isoformat()}\n')
				f.write(f'\n unknown error {e}\n ')
		finally:
			my_dict = {'intro' : 'ELIOT readings', 'script' : str(data_df)}
			return render(request, 'home/test_server.html', my_dict)

	else : # display the results : 5 limit ordered by ts

		sd = server_document('https://awsb.ddns.net/eliot/eliot')

		sql = f"SELECT device_IMEI, device_model, device_timezone," \
		   f"measurements_timestamp, measurements_pulse_value, measurements_systolicBloodPressure_value, " \
		   f"measurements_diastolicBloodPressure_value, measurements_glucose_value, measurements_glucose_unit, " \
		   f"measurements_bodyWeight_value, measurements_bodyWeight_unit, measurements_bodyComposition_value,measurements_cholesterol_value, " \
		   f"measurements_cholesterol_unit, measurements_uricacid_value, measurements_uricacid_unit, measurements_ketone_value, " \
		   f"measurements_ketone_unit, measurements_hematocrit_value, measurements_hematocrit_unit,measurements_SpO2_value, " \
		   f"measurements_SpO2_unit, measurements_temperature_value, measurements_temperature_unit,metadata_measurementType, "\
		   f"measurements_ecgSamples_samples " \
		   f"from eliot2 ORDER BY measurements_timestamp DESC LIMIT 7"

		cols = ['device_IMEI', 'device_model', 'device_timezone', 'measurements_timestamp',
				'measurements_pulse_value', 'measurements_systolicBloodPressure_value', 'measurements_diastolicBloodPressure_value',
				'measurements_glucose_value', 'measurements_glucose_unit', 'measurements_bodyWeight_value', 'measurements_bodyWeight_unit', 'r',
				'measurements_cholesterol_value', 'measurements_cholesterol_unit',
				'measurements_uricacid_value', 'measurements_uricacid_unit',
				'measurements_ketone_value', 'measurements_ketone_unit',
				'measurements_hematocrit_value', 'measurements_hematocrit_unit',
				'measurements_SpO2_value','measurements_SpO2_unit',
				'measurements_temperature_value', 'measurements_temperature_unit',
				'metadata_measurementType', 'measurements_ecgSamples_samples'
				]

		db = MySQLdb.connect(host='192.168.1.173', port=3306, user='pi', password='7914920', db='Health', charset='utf8')
		with db.cursor() as cur:# setup the dropdowns dicts
			cur.execute(sql) #"SELECT * FROM countries")
			r = cur.fetchall() # tuple of dicts ({},{}..  ,)
		db.close()

		df = pd.DataFrame([i for i in r], columns=cols)
		#df.set_index('measurements_timestamp', drop=True, inplace=True)
		#df = df.sort_index(ascending=True)
		# create val and measure fields
		k = {'cholesterol' : 'TCH', 'ketone' : 'bK', 'uricacid' : 'UA', 'glucose' : 'BG', 'SpO2' : 'SpO2', 'temperature' : 'Temp', 'bodyWeight' : 'weight'}
		for bm in k.keys() :    #['cholesterol', 'ketone', 'uricacid', 'glucose']:
			bmv = f'measurements_{bm}_value'
			bmu = f'measurements_{bm}_unit'
			df.loc[df[bmv].notnull(),'val'] = df[bmv].fillna(0).map(str) + ' ' + df[bmu]
			df.loc[df[bmu].notnull(),'measure'] = k[bm]

		# # backfill BS-2001-G1 into Kg if measurements_bm_unit == 'g' #some error with float and none, don't know why 7.1.22
		try:
			df.loc[df['device_model'] == 'BS-2001-G1', 'val'] = df['measurements_bodyWeight_value'].apply(lambda x: f'{x*0.001:.1f} Kg')
		except:
			df.loc[df['device_model'] == 'BS-2001-G1', 'val'] = df['measurements_bodyWeight_value']

		# backfill BP and Pulse
		sys = f'measurements_systolicBloodPressure_value'
		df.loc[df[sys].notnull(),'val'] = df.measurements_systolicBloodPressure_value.fillna(0).astype(int).map(str) +\
										'/'+ df.measurements_diastolicBloodPressure_value.fillna(0).astype(int).map(str)+\
										', Pulse ' + df.measurements_pulse_value.fillna(0).astype(int).map(str)
		df.loc[df[sys].notnull(),'measure'] = 'BP'

		# backfill Pulse into SpO2 vale
		sys = f'measurements_SpO2_value'
		df.loc[df[sys].notnull(), 'val'] += ', Pulse ' + df.measurements_pulse_value.fillna(0).astype(int).map(str)
		#df.loc[df[sys].notnull(), 'measure'] = 'BP'

		# backfill ECG
		# 1. Ch1 numberOfSamples = json.loads(df.measurements_ecgSamples_samples[0]
		# 2. PDF imag file with URL as link (val = https://
		# "measurements_ecgSamples_samples" is either str (PDF) or dict (raw)
		df.loc[df['device_model'] == 'PM100', 'measure'] = 'ECG'
		# detect type of measure raw or image
		df.loc[df['device_model'] == 'PM100', 'val'] = 'PDF' # raw =  f"Samples Ch1: {json.loads(df.measurements_ecgSamples_samples[0])[0]['numberOfSamples']} Ch2: {json.loads(df.measurements_ecgSamples_samples[0])[0]['numberOfSamples']}"

		df.val = df.measure + ' ' + df.val
		df.rename(columns={'measurements_timestamp': 'ts'}, inplace=True)

		df.ts = df.ts.dt.strftime('%d %b %X')
		df.drop(df.columns[df.columns.str.contains('measure')], axis=1, inplace=True)

		eliotdict = df.to_dict('records') # list of each measurement as dict
		my_dict = {'Intro' : 'M+ hub last 6 measurements (by device time):-', 'eliotdict' : eliotdict, 'script': sd}
		return render(request, 'home/eliot_server.html', my_dict)
def m1s(request):
	aurl = 'https://awsb.ddns.net/m1/m1'
	script = server_document(url=aurl) #, resources=None)
	my_dict={'Intro' : 'M+.... loading', 'script': script}
	return render(request, 'home/M+_server.html',my_dict)

def m2s(request):
	aurl = 'https://awsb.ddns.net/m2/m2'
	script = server_document(url=aurl) #, resources=None)
	my_dict={'Intro' : 'M++.... loading', 'script': script}
	return render(request, 'home/M+_server.html',my_dict)

def m3s(request):
	aurl = 'https://awsb.ddns.net/m3/m3'
	script = server_document(url=aurl) #, resources=None)
	my_dict={'Intro' : 'M+++.... loading', 'script': script}
	return render(request, 'home/M+_server.html',my_dict)

def app1(request):
	aurl = 'https://awsb.ddns.net/app1/app1'
	script = server_document(url=aurl) #, resources=None)
	my_dict={'Intro' : 'testing app1', 'script': script}
	return render(request, 'home/M+_server.html',my_dict)
