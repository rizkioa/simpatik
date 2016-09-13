from django.contrib import admin
from master.models import Kecamatan
from django.http import HttpResponse
from django.utils.safestring import mark_safe

import json

def get_kecamatan(request):
	kecamatan_list = Kecamatan.objects.all()
	
	id_kabupaten = request.POST.get('kabupaten', None)	
	if id_kabupaten and not id_kabupaten is "":
		kecamatan_list = kecamatan_list.filter(kabupaten__id=id_kabupaten)
	nama_kecamatan = request.POST.get('nama_kecamatan', None)
	if nama_kecamatan and not nama_kecamatan is "":
		kecamatan_list = kecamatan_list.filter(nama_kecamatan=nama_kecamatan)

	return kecamatan_list

class KecamatanAdmin(admin.ModelAdmin):
	list_display = ('nama_kecamatan','kabupaten','keterangan')
	list_filter = ('kabupaten__provinsi','kabupaten')
	search_fields = ('nama_kecamatan', 'keterangan')

	def json_kecamatan(self, request):		
		kecamatan_list = get_kecamatan(request)
		results = [ob.as_json() for ob in kecamatan_list]
		return HttpResponse(json.dumps(results))

	def option_kecamatan(self, request):		
		kecamatan_list = get_kecamatan(request)
		pilihan = "<option></option>"
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in kecamatan_list)));

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(KecamatanAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^json/$', self.admin_site.admin_view(self.json_kecamatan), name='json_kecamatan'),
			url(r'^option/$', self.admin_site.admin_view(self.option_kecamatan), name='option_kecamatan'),
			url(r'^option-front-end/$', self.option_kecamatan, name='option_kecamatan_front'),
			)
		return my_urls + urls