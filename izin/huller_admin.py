from django.contrib import admin
from izin.models import DetilHuller, Syarat, SKIzin, Riwayat
from kepegawaian.models import Pegawai
from accounts.models import NomorIdentitasPengguna
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
from django.http import HttpResponse
import base64
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, resolve
import datetime

class DetilHullerAdmin(admin.ModelAdmin):
	list_display = ('id','get_no_pengajuan', 'pemohon', 'get_kelompok_jenis_izin','jenis_permohonan', 'status')
	search_fields = ('no_izin', 'pemohon__nama_lengkap')

	def get_kelompok_jenis_izin(self, obj):
		return obj.kelompok_jenis_izin
	get_kelompok_jenis_izin.short_description = "Izin Pengajuan"

	def get_no_pengajuan(self, obj):
		no_pengajuan = mark_safe("""
			<a href="%s" target="_blank"> %s </a>
			""" % ("#", obj.no_pengajuan ))
		split_ = obj.no_pengajuan.split('/')
		# print split_
		if split_[0] == 'ITNH':
			no_pengajuan = mark_safe("""
				<a href="%s" target="_blank"> %s </a>
				""" % (reverse('admin:izin_informasitanah_change', args=(obj.id,)), obj.no_pengajuan ))
		return no_pengajuan
	get_no_pengajuan.short_description = "No. Pengajuan"


	def get_readonly_fields(self, request, obj=None):
		rf = ('verified_by', 'verified_at', 'created_by', 'created_at', 'updated_at')
		if obj:
			if not request.user.is_superuser:
				rf = rf+('status',)
		return rf

	def get_fieldsets(self, request, obj = None):
		if obj or request.user.is_superuser:
			add_fieldsets = (
				(None, {
					'classes': ('wide',),
					'fields': ('pemohon','perusahaan',)
					}
				),
				('Detail Izin', {'fields': ('kelompok_jenis_izin', 'jenis_permohonan','no_pengajuan', 'no_izin','legalitas')}),
				('Detail Kuasa', {'fields': ('nama_kuasa','no_identitas_kuasa','telephone_kuasa',) }),
				('Detail Huller', {'fields': ('pemilik_badan_usaha','pemilik_nama_perorangan','pemilik_alamat','pemilik_desa','pemilik_kewarganegaraan','pemilik_nama_badan_usaha','pengusaha_badan_usaha','pengusaha_nama_perorangan','pengusaha_alamat','pengusaha_desa','pengusaha_kewarganegaraan','pengusaha_nama_badan_usaha','hubungan_pemilik_pengusaha','kapasitas_potensial_giling_beras_per_jam','kapasitas_potensial_giling_beras_per_tahun') }),
				('Berkas & Keterangan', {'fields': ('berkas_tambahan', 'keterangan',)}),

				('Lain-lain', {'fields': ('status', 'created_by', 'created_at', 'verified_by', 'verified_at', 'updated_at')}),
			)

		else:
			add_fieldsets = (
				(None, {
					'classes': ('wide',),
					'fields': ('pemohon',)
					}
				),
				('Detail Izin', {'fields': ('kelompok_jenis_izin', 'jenis_permohonan','no_pengajuan', 'no_izin','legalitas')}),
				('Detail Kuasa', {'fields': ('nama_kuasa','no_identitas_kuasa','telephone_kuasa',) }),
				('Detail Huller', {'fields': ('pemilik_badan_usaha','pemilik_nama_perorangan','pemilik_alamat','pemilik_desa','pemilik_kewarganegaraan','pemilik_nama_badan_usaha','pengusaha_badan_usaha','pengusaha_nama_perorangan','pengusaha_alamat','pengusaha_desa','pengusaha_kewarganegaraan','pengusaha_nama_badan_usaha','hubungan_pemilik_pengusaha','kapasitas_potensial_giling_beras_per_jam','kapasitas_potensial_giling_beras_per_tahun') }),
				('Berkas & Keterangan', {'fields': ('berkas_tambahan', 'keterangan',)}),
			)
		return add_fieldsets

admin.site.register(DetilHuller, DetilHullerAdmin)