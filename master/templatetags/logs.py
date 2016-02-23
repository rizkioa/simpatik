from django import template
register = template.Library()

from django.contrib.admin.models import LogEntry

import datetime
from dateutil.relativedelta import relativedelta

@register.assignment_tag
def get_riwayat_admin(user_, waktu_):
	if not user_.is_superuser:
		logs = LogEntry.objects.filter(user=user_)
	else:
		logs = LogEntry.objects.all()
	now = datetime.datetime.now()
	if waktu_ == 'bulan ini':
		return logs.filter(action_time__gte=str(now.year)+'-'+str(now.month)+'-01')
	elif waktu_ == 'bulan kemaren':
		bulan_ini = datetime.date(now.year, now.month, 1)
		bulan_kemaren = bulan_ini-relativedelta(months=1)
		return logs.filter(action_time__gte=str(bulan_kemaren.year)+'-'+str(bulan_kemaren.month)+'-01', action_time__lt=str(bulan_ini.year)+'-'+str(bulan_ini.month)+'-01')
	elif waktu_ == 'tahun ini':
		if now.month > 2:
			bulan_ini = datetime.date(now.year, now.month, 1)
			bulan_kemaren = bulan_ini-relativedelta(months=1)
			return logs.filter(action_time__gte=str(bulan_ini.year)+'-01-01', action_time__lt=str(bulan_kemaren.year)+'-'+str(bulan_kemaren.month)+'-01')
		else:
			return LogEntry.objects.none()
	return logs