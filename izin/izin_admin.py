from django.contrib import admin
from django.http import HttpResponse
from django.template import RequestContext, loader
from izin.models import PengajuanIzin

class IzinAdmin(admin.ModelAdmin):
	list_display = ('pemohon','kelompok_jenis_izin','jenis_permohonan','status')

	def add_wizard(self, request):
		extra_context = {}

		template = loader.get_template("admin/izin/izin/add_wizard.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(IzinAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^wizard/add/$', self.admin_site.admin_view(self.add_wizard), name='add_wizard_izin'),
			)
		return my_urls + urls

	def save_model(self, request, obj, form, change):
		# clean the nomor_identitas
		obj.create_by = request.user
		obj.save()

admin.site.register(PengajuanIzin, IzinAdmin)