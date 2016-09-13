from django.contrib import admin
from master.models import Desa
from django.http import HttpResponse
from django.utils.safestring import mark_safe

import json

def get_desa(request):
	desa_list = Desa.objects.all()
	
	id_kecamatan = request.POST.get('kecamatan', None)	
	if id_kecamatan and not id_kecamatan is "":
		desa_list = desa_list.filter(kecamatan__id=id_kecamatan)
	nama_desa = request.POST.get('nama_desa', None)
	if nama_desa and not nama_desa is "":
		desa_list = desa_list.filter(nama_desa=nama_desa)

	return desa_list

class DesaAdmin(admin.ModelAdmin):
	list_display = ('nama_desa','kecamatan','keterangan')
	list_filter = ('kecamatan__kabupaten','kecamatan')
	search_fields = ('nama_desa', 'keterangan')

	def json_desa(self, request):		
		desa_list = get_desa(request)
		results = [ob.as_json() for ob in desa_list]
		return HttpResponse(json.dumps(results))

	def option_desa(self, request):		
		desa_list = get_desa(request)
		pilihan = "<option></option>"
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in desa_list)));

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DesaAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^json/$', self.admin_site.admin_view(self.json_desa), name='json_desa'),
			url(r'^option/$', self.admin_site.admin_view(self.option_desa), name='option_desa'),
			url(r'^option-front/$', self.option_desa, name='option_desa_front'),
			)
		return my_urls + urls