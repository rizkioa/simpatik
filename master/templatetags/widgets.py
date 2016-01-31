from django import template
register = template.Library()
from django import forms

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
	return isinstance(field.field.widget, forms.Select)

@register.filter('is_file')
def is_file(field):
	return isinstance(field.field.widget, forms.FileInput)

@register.filter('is_readonlypassword')
def is_readonlypassword(field):
	from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
	return isinstance(field.field.widget, ReadOnlyPasswordHashWidget)