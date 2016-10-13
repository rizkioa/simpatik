from django.contrib import admin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe

from perusahaan.models import Perusahaan,ProdukUtama
import json

class PerusahaanAdmin(admin.ModelAdmin):
	# list_display = ('nama_perusahaan', 'alamat_perusahaan', 'telepon', 'fax','email',)
	list_filter = ('status',)
	search_fields = ('nama_perusahaan', 'alamat_perusahaan', 'telepon','fax', 'email')
	ordering = ('id',)

	def get_fieldset():
		fieldsets = (
			(' Alamat Perusahaan', {
				'fields': ('nama_perusahaan', 'alamat_perusahaan', 'lt','lg','kode_pos','telepon','fax','email')
				}),

			('Informasi', {
				'fields': ('jenis_perusahaan','kbli','nama_kelompok_perusahaan','nasabah_utama_bank1','nasabah_utama_bank2','jumlah_bank','npwp')
				}),

			('Pendirian', {
				'fields': ('tgl_pendirian', 'tgl_mulai_kegiatan', 'merk_dagang','pemegang_hak_paten','pemegang_hak_cipta')
				}),

			(None, {
				'fields': ('penanaman_modal', 'status_perusahaan', 'kerjasama','badan_usaha')
				}),	

			(None, {
				'fields': ('status', 'created_at', 'updated_at')
				}),
		)

		if request.user.is_superuser:
			
			fieldsets = fieldsets;

		else:

			fieldsets = (

				(' Alamat Perusahaan', {
				'fields': ('nama_perusahaan', 'alamat_perusahaan', 'lt','lg','kode_pos','telepon','fax','email')
				}),

			('Administrasi', {
				'fields': ('jenis_perusahaan','kbli','nama_kelompok_perusahaan','nasabah_utama_bank1','nasabah_utama_bank2','jumlah_bank','npwp')
				}),

			('Pendirian', {
				'fields': ('tgl_pendirian', 'tgl_mulai_kegiatan', 'merk_dagang','pemegang_hak_paten','pemegang_hak_cipta')
				}),

			(None, {
				'fields': ('penanaman_modal', 'status_perusahaan', 'kerjasama','badan_usaha')
				}),	
				)

			return fieldsets

	def get_readonly_fields(self, request, obj=None):
		rf = ('nama_perusahaan', 'alamat_perusahaan', 'lt','lg','kode_pos','telepon','fax','email')
		rf_superuser = (None,)
		if request.user.groups.filter(name='Kabid') or request.user.groups.filter(name='Kadin') or request.user.groups.filter(name='Pembuat Surat') or request.user.groups.filter(name='Penomoran') or request.user.groups.filter(name='Cetak') or request.user.groups.filter(name='Selesai'):
			return rf
		else:
			return rf_superuser
		return rf

	def perusahaan_terdaftar(self, request, extra_context={}):
		self.request = request
		return super(PerusahaanAdmin, self).changelist_view(request, extra_context=extra_context)

	def get_list_display(self, request):
		func_view, func_view_args, func_view_kwargs = resolve(request.path)
		list_display = ('nama_perusahaan', 'alamat_perusahaan', 'telepon', 'fax','email',)
		if func_view.__name__ == 'perusahaan_terdaftar':
			list_display = ('npwp', 'nama_perusahaan', 'get_alamat', 'created_at')
		return list_display

	def get_list_display_links(self, request, list_display):
		if request.user.groups.filter(name='Kabid') or request.user.groups.filter(name='Kadin') or request.user.groups.filter(name='Pembuat Surat') or request.user.groups.filter(name='Penomoran') or request.user.groups.filter(name='Cetak') or request.user.groups.filter(name='Selesai'):
			list_display_links = None
		else:
			list_display_links = ('nama_perusahaan',)
		return list_display_links

	def get_alamat(self, obj):
		alamat_ = obj.alamat_perusahaan
		if obj.desa:
			alamat_ = str(obj.alamat_perusahaan)+", "+str(obj.desa)+", Kec. "+str(obj.desa.kecamatan)+", "+str(obj.desa.kecamatan.kabupaten)
		return alamat_
	get_alamat.short_description = "Alamat"

	def ajax_autocomplete(self, request):
		pilihan = "<option></option>"
		perusahaan_list = Perusahaan.objects.all()
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in perusahaan_list)));

	def ajax_perusahaan(self, request, perusahaan_id=None):
		perusahaan_get = Perusahaan.objects.filter(id=perusahaan_id)
		results = [ob.as_json() for ob in perusahaan_get]
		return HttpResponse(json.dumps(results))

	# def ajax_legalitas_perusahaan(self, request, perusahaan_id=None):
	# 	aktanotaris_get = AktaNotaris.objects.filter( id=perusahaan_id )
	# 	results = [ob.as_json() for ob in aktanotaris_get]
	# 	return HttpResponse(json.dumps(results))

	# def ajax_kegiatan_usaha(self, request, perusahaan_id=None):
	# 	kegiatan_get = DataRincianPerusahaan.objects.filter( id=perusahaan_id )
	# 	results = [ob.as_json() for ob in kegiatan_get]
	# 	return HttpResponse(json.dumps(results))

	def ajax_produk_utama(self, request, perusahaan_id=None):
		produkutama_get = ProdukUtama.objects.filter( id=perusahaan_id )
		results = [ob.as_json() for ob in produkutama_get]
		return HttpResponse(json.dumps(results))


	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(PerusahaanAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^ajax/autocomplete/$', self.admin_site.admin_view(self.ajax_autocomplete), name='perusahaan_ajax_autocomplete'),
			url(r'^ajax/perusahaan/(?P<perusahaan_id>\w+)/$', self.admin_site.admin_view(self.ajax_perusahaan), name='ajax_perusahaan'),
			# url(r'^ajax/legalitas/(?P<perusahaan_id>\w+)/$', self.admin_site.admin_view(self.ajax_legalitas_perusahaan), name='ajax_legalitas_perusahaan'),
			# url(r'^ajax/kegiatan_usaha/(?P<perusahaan_id>\w+)/$', self.admin_site.admin_view(self.ajax_kegiatan_usaha), name='ajax_kegiatan_usaha'),
			url(r'^ajax/produk_utama/(?P<perusahaan_id>\w+)/$', self.admin_site.admin_view(self.ajax_produk_utama), name='ajax_produk_utama'),
			url(r'^perusahaan-terdaftar/$', self.admin_site.admin_view(self.perusahaan_terdaftar), name='perusahaan_terdaftar'),
			)
		return my_urls + urls