from django.contrib import admin
from master.models import Kabupaten
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.db.models import Q

import json

def get_kabupaten(request):
	kabupaten_list = Kabupaten.objects.all()

	kode_negara = request.POST.get('kode_negara', None)
	kode_provinsi = request.POST.get('kode_provinsi', None)

	if kode_negara and kode_negara is not "" and kode_provinsi and kode_provinsi is not "":
		kabupaten_list = kabupaten_list.filter(provinsi__kode=kode_provinsi, provinsi__negara__kode=kode_negara)
	
	id_provinsi = request.POST.get('provinsi', None)	
	if id_provinsi and not id_provinsi is "":
		kabupaten_list = kabupaten_list.filter(provinsi__id=id_provinsi)
	nama_kabupaten = request.POST.get('nama_kabupaten', None)
	if nama_kabupaten and not nama_kabupaten is "":
		kabupaten_list = kabupaten_list.filter(nama_kabupaten=nama_kabupaten)

	return kabupaten_list

class KabupatenAdmin(admin.ModelAdmin):
	list_display = ('provinsi_kode', 'kode', 'nama_kabupaten','provinsi','keterangan')
	list_filter = ('provinsi',)
	search_fields = ('nama_kabupaten', 'keterangan')

	def provinsi_kode(self, obj):
		kode = ""
		if obj.provinsi:
			kode = obj.provinsi.kode
		return kode

	def json_kabupaten(self, request):		
		kabupaten_list = get_kabupaten(request)
		results = [ob.as_json() for ob in kabupaten_list]
		return HttpResponse(json.dumps(results))

	def option_kabupaten(self, request):		
		kabupaten_list = get_kabupaten(request)
		pilihan = "<option></option>"
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in kabupaten_list)));

	def option_kabupaten_complete(self, request):	
		kabupaten_list = Kabupaten.objects.all()
		q = request.POST.get('q', None)
		if q:
			kabupaten_list = kabupaten_list.filter(Q(nama_kabupaten__icontains=q)|Q(keterangan__icontains=q))
		else:
			kabupaten_list = Kabupaten.objects.none()	
		pilihan = "<option></option>"
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option_complete() for x in kabupaten_list)));

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(KabupatenAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^json/$', self.admin_site.admin_view(self.json_kabupaten), name='json_kabupaten'),
			url(r'^option/$', self.option_kabupaten, name='option_kabupaten'),
			url(r'^option/complete/$', self.admin_site.admin_view(self.option_kabupaten_complete), name='option_kabupaten_complete'),
			)
		return my_urls + urls