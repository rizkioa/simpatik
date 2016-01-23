from django import template
register = template.Library()
from django import forms

@register.filter(name='addcls')
def addcls(field, css):
	if hasattr(field, 'as_widget'):
		return field.as_widget(attrs={"class":css})
	else:
		return None


@register.filter('is_select')
def is_select(field):
	return isinstance(field.field.widget, forms.Select)