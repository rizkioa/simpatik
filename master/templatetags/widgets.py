from django import template
from django import forms
from master.models import ChatRoom, Chat
import datetime
import os
register = template.Library()

from kepegawaian.models import UnitKerja
from dateutil.relativedelta import relativedelta


@register.filter(name='add_date')
def add_date(datetime_, addDays=0):

	if (addDays!=0):
		anotherTime = datetime_ + datetime.timedelta(days=addDays)
	else:
		anotherTime = datetime_

	return anotherTime

@register.filter(name='add_year')
def add_year(datetime_, addDays=0):
	if (addDays!=0):
		anotherTime = datetime_ + relativedelta(years=addDays)
	else:
		anotherTime = datetime_

	return anotherTime

@register.filter(name='addcls')
def addcls(field, css):
	if hasattr(field, 'as_widget'):
		return field.as_widget(attrs={"class":css})
	else:
		return None

@register.filter(name='atribut')
def atribut(field_, attr_):
	if hasattr(field_, 'as_widget'):
		attrs = {}
		attrs_from_str = attr_.split("|")
		for attr in attrs_from_str:
			k_, v_ = attr.split(":")
			attrs.update({k_: v_})
		return field_.as_widget(attrs=attrs)
	else:
		return None

@register.filter('is_select')
def is_select(field):
	if isinstance(field.field.widget, forms.RadioSelect):
		return False
	return isinstance(field.field.widget, forms.Select) or str(field.field.widget.__class__.__name__) == 'RelatedFieldWidgetWrapper'

@register.filter('is_date')
def is_date(field):
	return isinstance(field.field.widget, forms.DateInput)

@register.filter('is_time')
def is_time(field):
	return isinstance(field.field.widget, forms.TimeInput)

@register.filter('is_datetime')
def is_datetime(field):
	return isinstance(field.field.widget, forms.SplitDateTimeWidget)
	
@register.filter('is_file')
def is_file(field):
	return isinstance(field.field.widget, forms.FileInput)

@register.filter('is_readonlypassword')
def is_readonlypassword(field):
	from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
	return isinstance(field.field.widget, ReadOnlyPasswordHashWidget)

@register.filter(name='joinby')
def joinby(value, arg):
	return arg.join(value)

@register.filter('extension')
def get_extension(value_):
	name, extension = os.path.splitext(os.path.basename(value_))
	return extension

@register.filter
def InList(value, list_):
	if value in list(list_.split(',')):
		return True
	return False

@register.filter(name='status')
def status(value):
	string = ''
	# print type(value)
	if value == 4:
		string = "Belum Disurvey"
	else:
		string = "Telah Disurvey"
	return string

@register.filter(name='hasil')
def hasil(value):
	string = '-'
	# print type(value)
	if value == 1:
		string = '<i class="fa fa-check"></i>'
	elif value == 3:
		string = '<i class="fa fa-times-circle"></i>'
	return string

@register.filter(name='true_or_false')
def true_false(args):
	string = '<i class="fa fa-times-circle" style="color: red"></i>'
	if args == True:
		string = '<i class="fa fa-check-circle" style="color: green"></i>'
	# elif arg == False:
	# 	string = '<i class="fa fa-times-circle" style="color: red"></i>'


	return string


@register.filter(name='get_rekomendasi')
def get_rekomendasi(qs_, user_):
	string = ''
	query = qs_.survey_rekomendiasi.filter(created_by_id=user_, status=1)
	
	if query.exists():
		query = query.last()
		string = query.rekomendasi

	return string

@register.filter(name='get_berkas')
def get_berkas(qs_, user_):
	string = ''
	url = ''
	query = qs_.survey_rekomendiasi.filter(created_by_id=user_, status=1)
	
	if query.exists():
		query = query.last()
		if query.berkas:
			if query.unit_kerja.url_simpatik:
				url = query.unit_kerja.url_simpatik
				
			string = '<a data-toggle="popover" data-trigger="hover" title="Preview Berkas" data-html="true" data-content="<img src=\''+str(url)+str(query.berkas.get_file_url())+'\' width=\'200\' />" data-placement="top" class="btn btn-rounded btn-success btn-sm" href="'+str(query.unit_kerja.url_simpatik)+str(query.berkas.get_file_url())+'" target="_blank"> <i class="fa fa-paperclip" ></i>'+str(query.berkas)+'</a>'

	return string

@register.filter(name='formatrupiah')
def formatrupiah(uang):
	y = str(uang)
	y = uang.replace(".", "")
	y = y.split('.')
	j = y[0]
	# y = y.replace(".00","")
	if len(j) <= 3 :
		return j  
	else :
		p = j[-3:]
		q = j[:-3]
		if len(y) > 1:
			return   formatrupiah(q) + '.' + p 
		else:
			return   formatrupiah(q) + '.' + p 

@register.filter(name='formatterbilang')
def formatterbilang(uang):
	from izin.utils import terbilang
	if uang:
		uang = uang.replace(".", "")
		return terbilang(int(uang)).upper()
	else:
		return '-'

@register.filter()
def get_alamat_lengkap(obj, filter):
	if filter == 'perusahaan':
		alamat_ = obj.alamat_perusahaan
	elif filter == 'pemohon':
		alamat_ = obj.alamat

	alamat_ = str(alamat_)+", Ds. "+str(obj.desa)+", Kec. "+str(obj.desa.kecamatan)+", "+str(obj.desa.kecamatan.kabupaten)
	return alamat_


@register.filter(name='get_logo_login')
def get_logo_login(args):
	string = '<h3 class="text-light text-white"><span class="text-lightred">SIM</span>PATIK</h3>'
	
	unit_kerja = UnitKerja.objects.filter(url_simpatik='http://'+str(args)+'/')
	if unit_kerja.exists():
		unit_kerja = unit_kerja.last()
		uk = unit_kerja.nama_unit_kerja
		if uk == 'PEMBANGUNAN':
			string = '<img src="/static/images/wwa.png" %}">'
		elif uk == 'DISBUDPAR':
			string = '<img src="/static/images/simpparis.png" %}">'
		
	return string

@register.filter(name='get_brand')
def get_brand(args):
	string = 'SIMPATIK'
	# print args
	unit_kerja = UnitKerja.objects.filter(url_simpatik='http://'+str(args)+'/')
	# print unit_kerja
	if unit_kerja.exists():
		unit_kerja = unit_kerja.last()
		string = unit_kerja.nama_unit_kerja
		
	return string


@register.filter(name='get_css')
def get_css(args):
	string = ''
	unit_kerja = UnitKerja.objects.filter(url_simpatik='http://'+str(args)+'/')
	if unit_kerja.exists():
		unit_kerja = unit_kerja.last()
		uk = unit_kerja.nama_unit_kerja
		# if uk == 'DISBUDPAR':
		# 	string = '/static/styles/css/budpar.css'
		uk = uk.lower()
		string = '/static/styles/css/'+str(uk)+'.css'

	return string

@register.filter(name='alfabet')
def atrialfabetbut(counter_):
    """Template Tags untuk menampilkan looping a-h"""
    list_alfabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'o', 'p', 'q', 'r']
    alfabet = list_alfabet[counter_]
    return alfabet

@register.filter(name='split_berkas')
def split_berkas(data):
	return (data[:50] + '...') if len(data) > 75 else data

@register.assignment_tag
def as_null():
	value = 0
	return value

@register.assignment_tag
def chatroom():
	chatroom_list = ChatRoom.objects.all().last()
	chatroom_nama_pemohon = chatroom_list.nama_pemohon
	id_ = chatroom_list.id
	chat_isi = Chat.objects.get(chat_room__id = id_).isi_pesan
	# for i in chatroom_list:
	# 	chatroom_id = i.id
	# 	chatroom_nama_pemohon = i.nama_pemohon
	# 	chat_list = Chat.objects.filter(chat_room=chatroom_id)


		

	c  = {
		'chatroom_nama_pemohon' : chatroom_nama_pemohon,
		'chat_isi_pesan' : chat_isi,
	}
	return c