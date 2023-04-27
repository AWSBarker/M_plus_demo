# TODO dash or home warning if M+daily > today
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import numpy as np
from bokeh.embed import server_document, components, server_session
from bokeh.layouts import row, column
from bokeh.plotting import figure
from bokeh.models import CDSView, HoverTool, LabelSet, \
	DatetimeTickFormatter, ColumnDataSource, \
	LinearColorMapper, BasicTicker, ColorBar, HoverTool, \
	PrintfTickFormatter, FixedTicker, IndexFilter
from bokeh.transform import transform
import datetime as dt
from datetime import timedelta
from mdaily.models import MDaily, MOrg
from django.db.models import Count, Max
from slick_reporting.views import SlickReportView
from trials.models import Ctgov1, Contacts
from .models import Eliot
from rest_framework.parsers import JSONParser
from flatdict import FlatDict
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView

from django.conf import settings
from .serializers import EliotSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from home.forms import ImeiForm
from django.views.generic.edit import FormView
import json
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import os
from Mdb2 import MonthlyReportGM, GetIMEI, VSReport
from Mapi2 import Org, Dev, Mapi, DBconx

from .eliot_update import run_redis

class QS_AnyMeasure():
	"""
	For response : Return asdict of measures (val) as text for context display of Queryset from any device like:
    For Admin : Return object :
     device_imei, device_model, device_timezone, ... ts, val
	"""
	# kout is keys to show display units for Gtel and GW
	kout = {'cholesterol' : 'TCH', 'ketone' : 'bK', 'uricacid' : 'UA', 'glucose' : 'BG',
		 'spo2' : 'SpO2', 'temperature' : 'Temp', 'bodyweight' : 'weight'}

	def __init__(self, aqs):
		self.recs = aqs #a QuerySet object like Eliot.objects.all()[:10] or Obj x.device_model

	def asobj(self):
		# return str as val for measured values in Admin for eliot, itasc
		if self.recs.device_model in ['BP800', 'D40G', 'LS802-GP']:
			if self.recs.metadata_measurementtype.lower() == 'bloodpressure':
				return f"{self.recs.measurements_systolicbloodpressure_value}/{self.recs.measurements_diastolicbloodpressure_value} {self.recs.measurements_pulse_value} ({self.recs.measurements_annotations_irregularheartbeat})"
			else:
				return f"{self.recs.measurements_glucose_value} {self.recs.measurements_glucose_unit}"
		elif self.recs.device_model == 'BS-2001-G1':
			return f"{self.recs.measurements_bodyweight_value*0.001:.1f} Kg"
		elif self.recs.device_model == 'BC800':
			return f"{self.recs.measurements_bodyweight_value} Kg"
		elif self.recs.device_model == 'PM100':
			return "PDF"
		elif self.recs.device_model == 'GTEL':
			mt = self.recs.metadata_measurementtype.lower() #self.kin.get(self.recs.metadata_measurementtype.lower(), 'None')
			try :
				mv = getattr(self.recs, f"measurements_{mt}_value")
				mu = getattr(self.recs, f"measurements_{mt}_unit")
				return f"{mt} {mv} {mu}"
			except:
				return 'some error'
		elif self.recs.device_model == 'GW9017':
			#SpO2 (pulse), bodytemperature, bloodpressure (dia/sys/pulse)
			if self.recs.metadata_measurementtype.lower() == 'bloodpressure':
				return f"{self.recs.measurements_systolicbloodpressure_value}/{self.recs.measurements_diastolicbloodpressure_value} {self.recs.measurements_pulse_value}"
			elif self.recs.metadata_measurementtype.lower() == 'bodytemperature':
				return f"{self.recs.measurements_temperature_value} {self.recs.measurements_temperature_unit}"
			elif self.recs.metadata_measurementtype.lower() == 'spo2':
				return f"{self.recs.measurements_spo2_value}{self.recs.measurements_spo2_unit} {self.recs.measurements_pulse_value}bpm"
			else: # weight, glucose
				mt = self.recs.metadata_measurementtype.lower() #self.kin.get(self.recs.metadata_measurementtype.lower(), 'None')
				try :
					mv = getattr(self.recs, f"measurements_{mt}_value")
					mu = getattr(self.recs, f"measurements_{mt}_unit")
					return f"{mv} {mu}"
				except:
					return 'gw data error'

	def asdict(self):
		# return dict for display in eliot and itasc
		self.cols = list(self.recs.model().__dict__.keys())[1:] # _state is removed
		df = pd.DataFrame(self.recs.values_list(*self.cols), columns= self.cols)
		for bm in self.kout.keys() :    #['cholesterol', 'ketone', 'uricacid', 'glucose']:
			bmv = f'measurements_{bm}_value'
			bmu = f'measurements_{bm}_unit'
			df.loc[df[bmv].notnull(),'val'] = df[bmv].fillna(0).map(str) + ' ' + df[bmu]
			df.loc[df[bmu].notnull(),'measure'] = self.kout[bm]
		try:
			df.loc[df['device_model'] == 'BS-2001-G1', 'val'] = df['measurements_bodyweight_value'].apply(lambda x: f'{x*0.001:.1f} Kg')
		except:
			df.loc[df['device_model'] == 'BS-2001-G1', 'val'] = df['measurements_bodyweight_value']

		# backfill BP and Pulse
		sys = f'measurements_systolicbloodpressure_value'
		df.loc[df[sys].notnull(),'val'] = df.measurements_systolicbloodpressure_value.fillna(0).astype(int).map(str) +\
										'/'+ df.measurements_diastolicbloodpressure_value.fillna(0).astype(int).map(str)+\
										', Pulse ' + df.measurements_pulse_value.fillna(0).astype(int).map(str)
		df.loc[df[sys].notnull(),'measure'] = 'BP'
		# backfill Pulse into SpO2 vale
		sys = f'measurements_spo2_value'
		df.loc[df[sys].notnull(), 'val'] += ', Pulse ' + df.measurements_pulse_value.fillna(0).astype(int).map(str)
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
#		print(df.head())
		return df.to_dict('records') # list of each measurement as dict

class Tool_IMEI(FormView):
	"""
	ask for IMEI, return Mapi2 resful json details
	keep list of last IMEIs beside the input box for copy/paste
	"""
	template_name = 'home/getimei.html'
	form_class = ImeiForm
	initial = {'imei' :358244086394972}
	list_imei = set()

	def get(self, request, *args, **kwargs):
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, {'form': form, 'list_imei': self.list_imei})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid(): # <process form cleaned data>
			self.list_imei.add(form.cleaned_data['imei'])
			self.d = Dev(form.cleaned_data['imei']).get_device_details() # dict. 'owner'
			if 'message' in self.d:
				messages.error(request, f"Error {self.d['message']} in M+hub\n")
				return render(request, self.template_name, {'form': form, 'list_imei': self.list_imei})
			else:
				#messages.success(request, f"Found {form.cleaned_data['imei']} in API\n")
				o = Org(self.d['owner']).get_org_name()
				self.d['owner'] = self.d['owner'] + ' (' + o + ')'
				jso = json.dumps(self.d, indent=4, sort_keys=True)
				script, div = self.imei_display()
				#return JsonResponse(d, safe=False)
				return render(request, "home/json_out.html", {'form': form, 'list_imei': self.list_imei, 'jsondata' : jso, 'script':script, 'div':div})
		else:
			messages.error(request, '*')

		storage = messages.get_messages(request)
		storage.used = True
		return render(request, self.template_name, {'form': form, 'list_imei': self.list_imei})

	def imei_display(self):
		i = GetIMEI((int(self.d['imei']))).imeidf()
		if type(i) == str or len(i) ==0:
			return ('no recorded measures', 'in M+ daily, check Org is in M+ Orgs')
		else:
			i['d'] = i['count'].diff()
			imax = i['count'].max()
			source1 = ColumnDataSource(i)
			p = figure(title=f"{self.d['imei']} Measures (total {imax})",width=600, height=100,
					   x_axis_type='datetime', y_range=(0,1), x_range=(i.index.min(), i.index.max()),
					   tools = "pan,wheel_zoom,reset", toolbar_location="above") #, toolbar_location=None)
			p.add_tools(HoverTool(tooltips=[('N measures', "@d"), ('dated', "@last_measure_at{%d%b%y}")],
					  formatters = {"@last_measure_at": "datetime"},
						mode='vline'))
			p.circle(x='last_measure_at', y=0.5, size='d', source=source1)
			p.yaxis.visible = False
			p.ygrid.visible = False
			p.xaxis[0].formatter = DatetimeTickFormatter(days='%d%b%y')
			p.title.text_font_size = "16px"
			return components(p)

class CTView1(SlickReportView):
	report_model = Ctgov1
	date_field = 'updated'
	columns = ['nct_id', 'updated', 'brief_title', 'drank_final', 'alloc__username']

class Home(TemplateView):
	template_name = 'home/home.html'

class Library(TemplateView):
	template_name = 'home/library.html'

@method_decorator(cache_page(90), name='get')
class Home2(LoginRequiredMixin, TemplateView):
	"""
	- Dash  	KPIs : last updates to db.
	- measures by client this week (daystack) !!! If ZERO !!!
	- total measures by clients by month stack
	- total measures by device type
	- new devices (by org)
"""
	template_name = 'home/home2.html'
	login_url = '/admin/login'
	redirect_field_name = 'redirect_to'
	model= Eliot

	def get(self, request, *args, **qargs):
		fleet_dict = MOrg.objects.fleet_size() # MDevOwn now owner__showas NOT org__showas, fleetsize
		mtw = MDaily.objects.measured_this_week().values('org_id__showas').annotate(c=Count('imei', distinct=True))
		mtd = MDaily.objects.measured_today().values('org_id__showas').annotate(c=Count('imei', distinct=True))
		#test1 = MDaily.objects.measured_since()
		#print(test1.info())
		#print(test1.head())
		dmax =mtw.aggregate(dmax=Max('c')).get('dmax')
		last_record = MDaily.objects.latest_measure()
		dffs=pd.DataFrame(list(fleet_dict))
		dffs.rename(columns={'owner__showas': 'org__showas'}, inplace=True)
		dfmtw = pd.DataFrame(list(mtw))
		dfmtw.rename(columns={'org_id__showas': 'org__showas'}, inplace=True)
		df = dffs.merge(dfmtw, how='left', on='org__showas') #, right_on=['org_id__showas'])
		df.fillna(0, axis=0, inplace=True)
		df = df.astype(str)
		df.reset_index(inplace=True)
		df2 = pd.DataFrame(list(mtd))
		df3 = MDaily.objects.measure1st_d().loc['2022-01-01':dt.datetime.now()] # 11thNov start of MDaily
		# need list of X_range outside CDS
		source1 = ColumnDataSource(df) # showas, sum wk measures, fs
		source2 = ColumnDataSource(df2)
		source3 = ColumnDataSource(df3)

		plot1 = figure(width = 480, height = 360, x_range=df.org__showas.to_list(),y_range=(-99,dmax+50),
					   y_axis_label = 'Fleet size       Active devices (wk / day )   ',
					   title='Active Devices by Org: last week, yesterday. Fleet size',
					   toolbar_location=None)
		plot1.vbar(x='org__showas', top='c', width=0.9, source=source1)
		plot1.vbar(x='org_id__showas', top='c', width=0.1, source=source2, color = 'white')

		fslabels = LabelSet(x='index', y= -30, text='fs', source=source1, angle =-0.7,
							x_offset=0, y_offset=0, render_mode='canvas',
							text_font_size='9pt', text_color='black')
		plot1.toolbar.active_drag = None
		plot1.add_layout(fslabels)
		plot1.xaxis.major_label_orientation = 'vertical'

		plot2 = figure(width = 480, height = 360, x_axis_type='datetime',
					   title='New devices (1st measure) by day, for all Orgs shown  ', toolbar_location='right')
		plot2.vbar(x='xax', top='imei', width=24*60*60*1000*1, source=source3)
		plot2.line(x='xax', y='roll', color='red', line_width=3, legend_label = 'monthly rolling average', source=source3)
		plot2.xaxis.formatter = DatetimeTickFormatter(months="%d %b %y")
		plot2.toolbar.active_drag = None

		script, div = ('hello', request.user.username) #components(plot1)
		script2, div2 = components(row(plot1,plot2)) #,row(plot1,plot2)))
		my_dict = {'fleet_dict' : fleet_dict, 'script' : script, 'div' : div, 'daily' : mtw, 'last_record' : last_record, 'script2' : script2, 'div2' : div2}

		return render(request, self.template_name, my_dict)

@login_required(login_url='/admin/login')
def help(request):
	with DBconx() as d:
		adata = d.data_folder
	my_dict = {'user' : request.user.username, 'session' :  request.session, 'adata' : adata}
	return render(request, 'home/help.html', my_dict)

@login_required(login_url='/admin/login')
def tools(request):
	last_mon = (dt.datetime.today().replace(day=1)-timedelta(days=1)).strftime('%B')
	return render(request, 'home/tools.html', {'last_mon': last_mon})

@cache_page(300)
@login_required(login_url='/admin/login')
def tools_orgs(request):
	all_orgs = Org().get_all_orgs()
	return render(request, 'home/all_orgs.html', {'all_orgs': all_orgs})

@cache_page(300)
@login_required(login_url='/admin/login')
def tools_bad_date(request):
	bd = MDaily.objects.wrong_date()
	return render(request, 'home/bad_date.html', {'bad_dates': bd})

@cache_page(60) #turn off cache - need refresh
@login_required(login_url='/admin/login')
def tools_uptime(request):
	# p0 produces the 24hr heatmap, crontab injects past2hour.png into uptime.html
	#lookback = 90
	#now = dt.datetime.now()

	df1 = MDaily.objects.measured_1d()
	df1.columns = ['last', 'count']
	df1.astype({'count' : np.int16}) # no effect 'last' : '<M8[s]'})
	df1.set_index('last', drop=True, inplace=True)
	last_measure = MDaily.objects.latest_measure().get('last_measure_at').strftime('%y-%m-%d %H:%M:%S')
	last_checked = MDaily.objects.last_checked().get('checked_on').strftime('%y-%m-%d %H:%M:%S') # {'checked_on' :dt.dt}

#-- cut here from try.alarms
	df1 = df1.resample('H').count()
	df1.fillna(0, inplace=True)
	#yrange = df1.index.date
	xrange = [0, 24] #dt(2022,10,16,0).hour,dt(2022,10,16,23).hour]
	df1['hour'] = df1.index.hour
	df1['date'] = df1.index.date #.astype('category')
	dfgb = df1.groupby(['date', 'hour']).sum().reset_index()
	source = ColumnDataSource(dfgb)

	today_view = CDSView(source=source, filters=[IndexFilter(dfgb[dfgb.date==dt.datetime.now().date()].index.to_list())]) #dt.now().strftime('%Y-%m-%d'))])
	print(today_view.filters[0].indices)
	colors = ["red", "gold", "yellowgreen", "green"]
	mapper = LinearColorMapper(palette=colors, low=0, high=len(colors), nan_color='red')

	p0 = figure(title=f"Last measure @ {last_measure}", height= 120, width=840,
			   x_range=xrange,x_axis_label =None, x_axis_location ='above', #, x_axis_type='datetime'
			   y_axis_label =f'Today', y_axis_type='datetime',
			   tools="", toolbar_location=None
			   )

	p0.rect(y='date', x='hour', width=0.99, height=0.99, source=source, view=today_view,
			   fill_color=transform('count', mapper), line_color=None,
		   )
	p0.xaxis.ticker = FixedTicker(ticks=[0,2,4,6,8,10,12,14,16,18,20,22,24])
	p0.xaxis.formatter = PrintfTickFormatter(format="%02s:00")
	p0.xaxis.major_label_orientation = 0.6
	p0.yaxis.major_tick_line_color = None
	p0.yaxis.major_label_text_color = None

	hovertool= HoverTool(tooltips=[("date", "@date{%y-%m-%d}"), ("hour", "@hour"), ("measures", "@count"),], formatters={"@date" : 'datetime'})
	p0.add_tools(hovertool)

	# p = figure(title=f"", width=840,
	# 		   x_range=xrange, x_axis_label =None, x_axis_location = None,
	# 		   y_axis_label =f'Last {lookback} days',y_axis_type='datetime',
	# 		   tools="", toolbar_location=None,
	# 		   )
	#
	# p.rect(y='date', x='hour', width=1, height=3600*24*1000, source=source,
	# 		   fill_color=transform('count', mapper), line_color="darkgreen",
	# 	   )
	# p.yaxis.major_tick_line_color = None
	# p.yaxis.major_label_text_color = None
	# color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="10px",
    #                  ticker=BasicTicker(desired_num_ticks=len(colors)),
    #                  label_standoff=5, border_line_color=None,
    #                  title='Zero measures (system down?)                              very low 1                          '
    #                        '                low  2                                   normal > 3',
    #                  height=10
    #                  )
	# p.add_layout(color_bar, 'below')
	#
	# hovertool1= HoverTool(tooltips=[("date", "@date{%y-%m-%d}"), ("hour", "@hour"), ("measures", "@count"),], formatters={"@date" : 'datetime'})
	# p.add_tools(hovertool1)

#-- cut here from try.alarms
	script, div = components(p0) #,row(plot1,plot2)))
	return render(request, 'home/uptime.html', {'script': script, 'div': div, 'last_checked' : last_checked})

def scanfiles():
	with DBconx() as d:
		apath = d.data_folder
	td = (dt.datetime.now() - dt.timedelta(hours=24)).timestamp()
	return sorted((f for f in os.scandir(apath) if f.name.endswith(".xlsx") and f.stat().st_ctime > td), key=lambda f: f.stat().st_ctime, reverse=True)
# def get_today_xlsx():
# 	path = os.path.dirname(settings.MEDIA_ROOT) # '/mnt/bitnami/home/bitnami/sharepoint/data'
# 	td = (dt.datetime.now() - timedelta(days=1)).timestamp()
# 	for root, _, files in os.walk(path):
# 		for file in files:
# 			if file.endswith('.xlsx'):
# 				if os.path.getctime(os.path.join(root, file)) > td:
# 					yield (file, os.path.join(root, file))
#@cache_page(300)
@login_required(login_url='/admin/login')
def tools_file_download(request):
	# nginx server media for download in website/data/ so URL needs data prefix
	filelist = [(f.name, f.path, dt.datetime.fromtimestamp(f.stat().st_ctime).isoformat()) for f in scanfiles()]
	return render(request, 'home/files_list.html', {'files': filelist})

@login_required(login_url='/admin/login')
def tools_gmon(request):
	# before monthly report run update owner
	# save               self.filename = f"{DBconx.data_folder}/GM_rep_{dt.now().strftime('%y%m%d_%H%M')}.xlsx"
	# nginx server demo.medisante-group.com/data/
	# BELOW OWNER UPDATE NOW DONE IN GETDF FOR GM
	# allorgs = Mapi().getOrgs()
	# iodict= Org.getOrg_ID_dict()
	# for o in allorgs:
	# 	adevs = Org(o).getalldevs()
	# 	own = iodict.get(o)
	# 	#messages.error(request, f"Calculating ownership {own} from M+hub\n")
	# 	try :
	# 		LoT_imei_owner = [(int(i['imei']),own) for i in adevs if i['imei'] != '-'] # bad device
	# 		Dev.update_owner(LoT_imei_owner)
	# 	except Exception as e:
	# 		print(f'update_owner error in {own} : {e}')
	try:
		d = MonthlyReportGM()
		dfile = f"{settings.MEDIA_URL}{d.filename.replace(DBconx.data_folder, 'data')}"
		last_mon = (dt.datetime.today().replace(day=1)-timedelta(days=1)).strftime('%B')
		my_dict = {'filesaved' : dfile, 'last_mon':last_mon}
	except Exception as e:
		my_dict = {'filesaved' : f"Try again, Is file open? {e}"}
	return render(request, 'home/tools_gmon_ok.html', my_dict)

@login_required(login_url='/admin/login')
def tools_vs_rep(request):
	try:
		r = VSReport()
		r.makereport()
		dfile = f"{settings.MEDIA_URL}{r.filename.replace(DBconx.data_folder, 'data')}"
		my_dict = {'filesaved' : dfile}
	except Exception as e:
		my_dict = {'filesaved' : f"Some error, {e}"}
	return render(request, 'home/tools_vs_ok.html', my_dict)

@api_view(['GET'])
@login_required(login_url='/admin/login')
def tools_json(request):
	last1 = Eliot.objects.all().order_by('-metadata_receivedtime')[:10] #latest('metadata_receivedtime') # [:5] .latest() metadata_receivedtime
	serializer = EliotSerializer(last1, many=True)
	return JsonResponse(serializer.data, safe=False)

# /eliot/bpn
#@cache_page(300) # this cache slows live data feed
@csrf_exempt
#@require_POST
def eliot(request):  # redis data needs update in post

	if request.method == 'POST':
		flatdict = FlatDict(JSONParser().parse(request), delimiter='_')
		flatdict['metadata_deviceGroups'] = "N/A"# field.ref_values
		post = Eliot()
		for (k,v) in flatdict.items(): # convert o/1 to False/True
			if v in ('true', 'True', 1, True):
				v = True
			if v in ('false', 'False', 0, False):
				v = False
			setattr(post, k.lower(), v)
		try:
			post.save()
			# after save OK, run eliot/create_data.py
			run_redis(flatdict['device_model']) # on the relevant df
		except Exception as e:
			with open('eliot2_error.log', 'a') as f:
				f.write(f'\n {dt.datetime.now().isoformat()}\n')
				f.write(f'\n unknown post save error in eliot {e}\n ')
				for k,v in post.__dict__.items():
					f.write(f"{k} {v}\n")
		finally:
			my_dict = {'intro' : 'ELIOT readings', 'script' : str(flatdict)}
			return render(request, 'home/test_server.html', my_dict)

	else : # display the results : 5 limit ordered by ts
		sd = server_document('https://demo.medisante-group.com/eliot/eliot', resources=None)
		eliotdict = QS_AnyMeasure(Eliot.objects.all()[:10]).asdict()
		my_dict = {'Intro' : 'M+ hub last 6 measurements (by device time):-', 'eliotdict' : eliotdict, 'script': sd}
		return render(request, 'home/eliot_server.html', my_dict)

@cache_page(300)
@login_required(login_url='/admin/login')
def m1s(request):
	aurl = 'https://demo.medisante-group.com/m1/m1'
	script = server_document(url=aurl) #, resources=None)
	my_dict={'Intro' : 'M+.... loading', 'script': script}
	return render(request, 'home/M+_server.html',my_dict)

@login_required(login_url='/admin/login')
def m2s(request):
	aurl = 'https://demo.medisante-group.com/m2/m2'
	#aurl = 'http://localhost:5006/main'
	#aurl = 'http://127.0.0.1:5014/m2/m2'
	script = server_document(url=aurl) #, resources=None)
	my_dict={'Intro' : 'M++.... loading', 'script': script}
	return render(request, 'home/M+_server.html',my_dict)


@cache_page(300)
@login_required(login_url='/admin/login')
def m3s(request):
	aurl = 'https://demo.medisante-group.com/m3/m3'
	#aurl = 'http://localhost:5006/main'
	script = server_document(url=aurl) #, resources=None)
	filelist = [(f.name, f.path, dt.datetime.fromtimestamp(f.stat().st_ctime).isoformat()) for f in scanfiles()]
	my_dict={'Intro' : 'M+++.... loading data', 'script': script, 'files' : filelist, 'settings' : settings.MEDIA_ROOT}
	return render(request, 'home/M+++_server.html',my_dict)

@cache_page(300)
#@login_required(login_url='/admin/login')
def m4s(request):
	aurl = 'https://demo.medisante-group.com/m4/m4'
	script = server_document(url=aurl) #, resources=None)
	my_dict={'Intro' : 'M+.... loading', 'script': script}
	return render(request, 'home/M+++_server.html',my_dict)


@cache_page(300)
@login_required(login_url='/admin/login')
def alarms(request):
	aurl = 'https://demo.medisante-group.com/alarm/alarm'
	script = server_document(url=aurl) #, resources=None)
	my_dict={'Intro' : 'Pick an Org to see possible alarm profiles based on historic and theoretical data',
			 'footer' : 'Ideally a zero measure alarm will trigger just a few times per year i.e. look for periods with probability ~<0.01 zero measures.<br/> '
						'Two alarms (2 periods shows as dual peaks/trough) might be required to cover an Org i.e. night 03:00-09:00 day 0800-1700. <br/>'
						'If the Theoretical does match the Actual (+/- 10%) there might be an error in the model(a), so:- <br/>'
			 				'1. Check to see if there are enough measures, ideally these should be ~100 x days <br/>'
			 				'2. Try adjusting the start date of analysis (start date = default 3 months) <br/>'
	 		 '<br/>'
			 'a. Theoretical data analysis based on single Org poisson distribution and includes any outages! <br/>'
				'See below for full analysis'
			,
			 'script': script
			 }
	return render(request, 'home/alarms.html',my_dict)


def send_alert_email(request):
	from smtplib import SMTP
	from bokeh.io import export_png
	from email.mime.image import MIMEImage
	from email.mime.text import MIMEText
	from email.mime.multipart import MIMEMultipart
	from selenium import webdriver
	from selenium.webdriver.firefox.options import Options

	x = [1, 2, 3, 4, 5]
	y = [4, 5, 5, 7, 2]
	p = figure(width=350, height=250)
	p.circle(x, y, fill_color="red", size=15)

	options = Options()
	options.headless = True
	filepath = export_png(p, filename="plot.png", webdriver=webdriver.Firefox(options=options))  # /mnt/bitnami/home/bitnami/sharepoint/data/

	to_email = 'barker@bluewin.ch'
	msg = MIMEMultipart('related')
	msg['Subject'] = "test"
	msg['From'] = 'andrew.barker@medisante-group.com'
	msg['To'] = to_email

	msg.attach(MIMEText("""
	                <html>
	                    <body>
	                        <h1 style="text-align: center;">Simple Data Report</h1>
	                        <p>Here could be a short description of the data.</p>
	                        <p><img src="cid:0" alt = "pic"></p>
	                        <p><img src=a></p>
	                    </body>
	                </html>""", 'html', 'utf-8'))

	with open('plot.png', 'rb') as fp:
		img = MIMEImage(fp.read())
		img.add_header('Content-Disposition', 'inline', filename='plot.png')
		#            img.add_header('X-Attachment-Id', '0')
		img.add_header('Content-ID', '<0>')
		msg.attach(img)

	try:
		with SMTP("smtp.office365.com", 587) as server:
			server.starttls()
			server.login('andrew.barker@medisante-group.com', 'Ulusaba@128')
			server.send_message(msg)

	except Exception as e:
		print(f"write error to emailed_studies file : {e}")
	return render(request, 'home/tools.html')