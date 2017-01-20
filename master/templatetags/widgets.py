from django import template
from django import forms
import datetime
import os
register = template.Library()


@register.filter(name='add_date')
def add_date(datetime_, addDays=0):

	if (addDays!=0):
		anotherTime = datetime_ + datetime.timedelta(days=addDays)
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
	if len(y) <= 3 :
		return y     
	else :
		p = y[-3:]
		q = y[:-3]
		return   formatrupiah(q) + '.' + p