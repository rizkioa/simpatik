from django.contrib import admin
from master.models import Provinsi
from django.http import HttpResponse
from django.utils.safestring import mark_safe

import json

def get_provinsi(request):
	provinsi_list = Provinsi.objects.all()
	
	id_negara = request.POST.get('negara', None)	
	if id_negara and not id_negara is "":
		provinsi_list = provinsi_list.filter(negara__id=id_negara)
	nama_provinsi = request.POST.get('nama_provinsi', None)
	if nama_provinsi and not nama_provinsi is "":
		provinsi_list = provinsi_list.filter(nama_provinsi=nama_provinsi)

	return provinsi_list

class ProvinsiAdmin(admin.ModelAdmin):
	list_display = ('nama_provinsi','negara','keterangan')
	list_filter = ('negara',)
	search_fields = ('nama_provinsi', 'keterangan')

	def json_provinsi(self, request):		
		provinsi_list = get_provinsi(request)
		results = [ob.as_json() for ob in provinsi_list]
		return HttpResponse(json.dumps(results))

	def option_provinsi(self, request):		
		provinsi_list = get_provinsi(request)
		pilihan = "<option></option>"
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in provinsi_list)));

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(ProvinsiAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^json/$', self.admin_site.admin_view(self.json_provinsi), name='json_provinsi'),
			url(r'^option/$', self.option_provinsi, name='option_provinsi'),
			)
		return my_urls + urls