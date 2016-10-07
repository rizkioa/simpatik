from django import template
from django import forms
import datetime

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