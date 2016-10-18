from django.contrib import admin
from django.core.urlresolvers import reverse, resolve
from izin.models import PengajuanIzin, DetilSIUP, DetilReklame, Pemohon
from perusahaan.models import Perusahaan
from django.utils.safestring import mark_safe
from django.http import HttpResponse
import json
from django.db.models import Q
from datetime import date

class DetilSIUPAdmin(admin.ModelAdmin):
	list_display = ('get_no_pengajuan', 'pemohon', 'get_kelompok_jenis_izin','jenis_permohonan', 'status')
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
		if split_[0] == 'SIUP':
			no_pengajuan = mark_safe("""
				<a href="%s" target="_blank"> %s </a>
				""" % (reverse('admin:izin_detilsiup_change', args=(obj.id,)), obj.no_pengajuan ))
		return no_pengajuan
	get_no_pengajuan.short_description = "No. Pengajuan"

	def get_fieldsets(self, request, obj=None):
		fields = ('pemohon', 'kelompok_jenis_izin', 'jenis_permohonan', 'no_pengajuan', 'no_izin', 'nama_kuasa', 'no_identitas_kuasa', 'telephone_kuasa', 'berkas_tambahan', 'perusahaan', 'berkas_foto', 'berkas_npwp_pemohon', 'berkas_npwp_perusahaan', 'legalitas', 'kbli', 'kelembagaan', 'produk_utama', 'bentuk_kegiatan_usaha', 'jenis_penanaman_modal', 'kekayaan_bersih', 'total_nilai_saham', 'presentase_saham_nasional', 'presentase_saham_asing')
		fields_admin = ('status', 'created_by', 'verified_by', 'rejected_by')
		if obj:
			if request.user.is_superuser:
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': fields+fields_admin
						}),
				)
			elif request.user.groups.filter(name='Operator') or request.user.groups.filter(name='Kabid') or request.user.groups.filter(name='Kadin') or request.user.groups.filter(name='Pembuat Surat') or request.user.groups.filter(name='Penomoran'):
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': fields
						}),
				)
			else:
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': ('no_pengajuan',)
						}),
					)
		else:
			pass
		return add_fieldsets

	def get_readonly_fields(self, request, obj=None):
		rf = ('pemohon', 'kelompok_jenis_izin', 'jenis_permohonan', 'no_pengajuan', 'no_izin', 'nama_kuasa', 'no_identitas_kuasa', 'telephone_kuasa', 'berkas_tambahan', 'perusahaan', 'berkas_foto', 'berkas_npwp_pemohon', 'berkas_npwp_perusahaan', 'legalitas', 'kbli', 'kelembagaan', 'produk_utama', 'bentuk_kegiatan_usaha', 'jenis_penanaman_modal', 'kekayaan_bersih', 'total_nilai_saham', 'presentase_saham_nasional', 'presentase_saham_asing')
		rf_admin = ('status', 'created_by', 'verified_by', 'rejected_by')
		rf_superuser = (None,)
		# if request.user.is_superuser:
		# 	return rf
		if request.user.groups.filter(name='Penomoran'):
			rf = ('no_pengajuan')
			return rf
		elif request.user.groups.filter(name='Operator'):
			rf = rf_admin
		elif request.user.groups.filter(name='Kabid') or request.user.groups.filter(name='Kadin') or request.user.groups.filter(name='Pembuat Surat') or request.user.groups.filter(name='Penomoran'):
			rf = rf + rf_admin
		else:
			return rf_superuser
		return rf

	def ajax_dashboard(self, request):
		tahun_sekarang = date.today().year
		pemohon = len(Pemohon.objects.all())
		perusahaan = len(Perusahaan.objects.all())
		pengajuan_selesai = len(PengajuanIzin.objects.filter(status=1))
		pengajuan_proses = len(PengajuanIzin.objects.filter(~Q(status=1)))
		# pengajuan_proses = len(PengajuanIzin.objects.filter(status=1))
		pengajuan_siup = len(DetilSIUP.objects.filter(created_at__year=tahun_sekarang))
		pengajuan_reklame = len(DetilReklame.objects.filter(created_at__year=tahun_sekarang))
		data = { 'success': True, 'pemohon': pemohon, 'perusahaan': perusahaan, 'pengajuan_selesai': pengajuan_selesai, 'pengajuan_proses': pengajuan_proses, 'pengajuan_siup': pengajuan_siup, 'pengajuan_reklame': pengajuan_reklame }
		return HttpResponse(json.dumps(data))

	def ajax_load_pengajuan_siup(self, request, id_pengajuan_):
		data = ""
		if id_pengajuan_:
			pengajuan_list = PengajuanIzin.objects.filter(id=id_pengajuan_)

		return HttpResponse(json.dumps(data))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilSIUPAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^ajax-dashboard/$', self.admin_site.admin_view(self.ajax_dashboard), name='ajax_dashboard'),
			url(r'^ajax-load-pengajuan-siup/(?P<id_pengajuan_>[0-9]+)/$', self.admin_site.admin_view(self.ajax_load_pengajuan_siup), name='ajax_load_pengajuan_siup'),
			)
		return my_urls + urls

admin.site.register(DetilSIUP, DetilSIUPAdmin)