from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from kepegawaian.models import *
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from kepegawaian.pegawai_admin import PegawaiAdmin
from kepegawaian.forms import BidangStrukturalForm
# Register your models here.

class JenisUnitKerjaAdmin(MPTTModelAdmin):
	mptt_level_indent = 20
	list_display = ('jenis_unit_kerja', 'keterangan', 'jenis_unit_kerja_induk' )

class UnitKerjaAdmin(MPTTModelAdmin):
	mptt_level_indent = 20
	list_display = ('nama_unit_kerja', 'keterangan', 'jenis_unit_kerja', 'unit_kerja_induk' )

class BidangStrukturalAdmin(MPTTModelAdmin):
	mptt_level_indent = 20
	list_display = ('nama_bidang', 'keterangan', 'unit_kerja', 'bidang_induk' )
	list_filter = ('unit_kerja', )
	form = BidangStrukturalForm

	def get_form(self, request, obj=None, **kwargs):
		form = super(BidangStrukturalAdmin, self).get_form(request, obj, **kwargs)
		form.request = request
		return form
		
	def option_bidangstruktural(self, request):		
		bidangstruktural_list = BidangStruktural.objects.all()
		unit_kerja = request.POST.get('unit_kerja', None)
		if unit_kerja:
			bidangstruktural_list = bidangstruktural_list.filter(unit_kerja__id=unit_kerja)
		else:
			bidangstruktural_list = BidangStruktural.objects.none()
		pilihan = "<option></option>"
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option(True) for x in bidangstruktural_list)));

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(BidangStrukturalAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^option/$', self.admin_site.admin_view(self.option_bidangstruktural), name='option_bidangstruktural'),
			)
		return my_urls + urls

admin.site.register(JenisUnitKerja, JenisUnitKerjaAdmin)
admin.site.register(UnitKerja, UnitKerjaAdmin)
admin.site.register(BidangStruktural, BidangStrukturalAdmin)
admin.site.register(Pegawai, PegawaiAdmin)
admin.site.register(Jabatan)