from django.contrib import admin
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils.safestring import mark_safe

from izin.models import PengajuanIzin, JenisIzin, KelompokJenisIzin
from izin.controllers.siup import add_wizard_siup, formulir_siup

import json

class IzinAdmin(admin.ModelAdmin):
	list_display = ('pemohon','kelompok_jenis_izin','jenis_permohonan','status')

	def add_wizard(self, request):
		extra_context = {}

		template = loader.get_template("admin/izin/izin/add_wizard.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def option_namaizin(self, request):	
		jenis_izin = request.POST.get('param', None)
		if jenis_izin:
			jenisizin_list = JenisIzin.objects.filter(jenis_izin=jenis_izin)
		else:
			jenisizin_list = JenisIzin.objects.none()
		pilihan = "<option></option>"
		response = {
			"count": 0,
			"data": pilihan+"".join(x.as_option() for x in jenisizin_list)
		}

		return HttpResponse(json.dumps(response))
		# return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in jenisizin_list)));

		# pilihan = """
		# <option value=1>SIUP</option>
		# <option>HO</option>
		# <option>SIPA</option>
		# <option>Izin Pertambangan</option>
		# <option>TDP</option>
		# """
		# return HttpResponse(mark_safe(pilihan));

	def option_kelompokjenisizin(self, request):
		id_jenis_izin = request.POST.get('param', None)
		if id_jenis_izin:
			kelompokjenisizin_list = KelompokJenisIzin.objects.filter(jenis_izin__id=id_jenis_izin)
		else:
			kelompokjenisizin_list = KelompokJenisIzin.objects.none()
		pilihan = "<option></option>"
		response = {
			"count": len(kelompokjenisizin_list),
			"data": pilihan+"".join(x.as_option() for x in kelompokjenisizin_list)
		}

		return HttpResponse(json.dumps(response))
		# return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in kelompokjenisizin_list)));

		# pilihan = """
		# <option value=1>SIUP</option>
		# <option>HO</option>
		# <option>SIPA</option>
		# <option>Izin Pertambangan</option>
		# <option>TDP</option>
		# """
		# return HttpResponse(mark_safe(pilihan));

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(IzinAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^wizard/add/$', self.admin_site.admin_view(add_wizard_siup), name='add_wizard_izin'),
			url(r'^option/izin/$', self.admin_site.admin_view(self.option_namaizin), name='option_namaizin'),
			url(r'^option/kelompokizin/$', self.admin_site.admin_view(self.option_kelompokjenisizin), name='option_kelompokjenisizin'),
			url(r'^wizard/add/proses/siup/$', self.admin_site.admin_view(formulir_siup), name='izin_proses_siup'),
			)
		return my_urls + urls

	def save_model(self, request, obj, form, change):
		# clean the nomor_identitas
		obj.create_by = request.user
		obj.save()

admin.site.register(PengajuanIzin, IzinAdmin)