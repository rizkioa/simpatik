from django.contrib import admin
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils.safestring import mark_safe

from izin.models import PengajuanIzin
from izin.controllers.siup import add_wizard_siup, formulir_siup

class IzinAdmin(admin.ModelAdmin):
	list_display = ('pemohon','kelompok_jenis_izin','jenis_permohonan','status')

	def add_wizard(self, request):
		extra_context = {}

		template = loader.get_template("admin/izin/izin/add_wizard.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def option_izin(self, request):		
		pilihan = """
		<option value=1>SIUP</option>
		<option>HO</option>
		<option>SIPA</option>
		<option>Izin Pertambangan</option>
		<option>TDP</option>
		"""
		return HttpResponse(mark_safe(pilihan));

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(IzinAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^wizard/add/$', self.admin_site.admin_view(add_wizard_siup), name='add_wizard_izin'),
			url(r'^option/izin/$', self.admin_site.admin_view(self.option_izin), name='option_izin'),
			url(r'^wizard/add/proses/1/$', self.admin_site.admin_view(formulir_siup), name='option_izin_proses_1'),
			)
		return my_urls + urls

	def save_model(self, request, obj, form, change):
		# clean the nomor_identitas
		obj.create_by = request.user
		obj.save()

admin.site.register(PengajuanIzin, IzinAdmin)