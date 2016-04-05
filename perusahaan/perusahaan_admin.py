from django.contrib import admin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe

from perusahaan.models import Perusahaan

class PerusahaanAdmin(admin.ModelAdmin):
	list_display = ('nama_perusahaan', 'alamat_perusahaan', 'telepon', 'fax','email',)
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