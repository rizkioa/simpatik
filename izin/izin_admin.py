import json
import base64
import datetime
from izin.utils import terbilang_, terbilang, formatrupiah
from django.db.models import Q
from django.contrib import admin
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils.safestring import mark_safe
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from daterange_filter.filter import DateRangeFilter
from mobile.cors import CORSHttpResponse
from izin.models import PengajuanIzin, JenisIzin, KelompokJenisIzin, Syarat, DetilSIUP, SKIzin, Riwayat, DetilTDP, Survey
from kepegawaian.models import Pegawai
from master.models import Template
from izin.controllers.siup import add_wizard_siup, formulir_siup, cetak
from izin.controllers.reklame import formulir_reklame
from izin.controllers.imb_reklame import formulir_imb_reklame
from izin.controllers.imb_umum import formulir_imb_umum
from izin.controllers.imb_perumahan import formulir_imb_perumahan
from izin.controllers.tdp import *
from izin.controllers.tdup import formulir_tdup
from izin.controllers.izin_gangguan import formulir_izin_gangguan
from izin.controllers.penggunaan_kekayaan_daerah import formulir_informasi_kekayaan_daerah
from izin.controllers.izin_lokasi import formulir_izin_lokasi 
from izin.controllers.ippt_rumah import formulir_ippt_rumah 
from izin.controllers.huller import formulir_detilhuller 
from izin.controllers.ippt_usaha import formulir_ippt_usaha 

from izin.controllers.iujk import IUJKWizard
from izin_forms import UploadBerkasPenolakanIzinForm, PemohonForm, PerusahaanForm
from mobile.utils import get_model_detil

class IzinAdmin(admin.ModelAdmin):
	# list_display = ('get_no_pengajuan', 'get_tanggal_pengajuan', 'get_kelompok_jenis_izin', 'pemohon','jenis_permohonan', 'get_status_proses','status', 'button_cetak_pendaftaran')
	list_filter = ('kelompok_jenis_izin', ('created_at', DateRangeFilter))
	search_fields = ('no_izin', 'pemohon__nama_lengkap', 'no_pengajuan')
	

	def changelist_view(self, request, extra_context={}):
		self.request = request
		izin = KelompokJenisIzin.objects.all()
		extra_context.update({'izin': izin})
		return super(IzinAdmin, self).changelist_view(request, extra_context=extra_context)

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
			elif request.user.groups.filter(name='Operator') or request.user.groups.filter(name='Kabid'):
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
		if request.user.groups.filter(name='Kabid') or request.user.groups.filter(name='Kadin') or request.user.groups.filter(name='Pembuat Surat') or request.user.groups.filter(name='Penomoran') or request.user.groups.filter(name='Cetak') or request.user.groups.filter(name='Selesai'):
			return rf
		elif request.user.groups.filter(name='Penomoran'):
			rf = ('no_pengajuan')
			return rf
		else:
			return rf_superuser
		return rf

	def izinterdaftar(self, request, extra_context={}):
		self.request = request
		izin = KelompokJenisIzin.objects.all()
		extra_context.update({'izin': izin})
		return super(IzinAdmin, self).changelist_view(request, extra_context=extra_context)

	def verifikasi_operator(self, request, extra_context={}):
		self.request = request
		izin = KelompokJenisIzin.objects.all()
		extra_context.update({'izin': izin})
		return super(IzinAdmin, self).changelist_view(request, extra_context=extra_context)

	def verifikasi_kabid(self, request, extra_context={}):
		self.request = request
		izin = KelompokJenisIzin.objects.all()
		extra_context.update({'izin': izin})
		return super(IzinAdmin, self).changelist_view(request, extra_context=extra_context)

	def verifikasi_pembuat_surat(self, request, extra_context={}):
		self.request = request
		izin = KelompokJenisIzin.objects.all()
		extra_context.update({'izin': izin})
		return super(IzinAdmin, self).changelist_view(request, extra_context=extra_context)

	def survey(self, request, extra_context={}):
		self.request = request
		izin = KelompokJenisIzin.objects.all()
		extra_context.update({'izin': izin})
		return super(IzinAdmin, self).changelist_view(request, extra_context=extra_context)

	def verifikasi_skizin_kabid(self, request, extra_context={}):
		self.request = request
		izin = KelompokJenisIzin.objects.all()
		extra_context.update({'izin': izin})
		return super(IzinAdmin, self).changelist_view(request, extra_context=extra_context)

	def verifikasi_skizin_kadin(self, request, extra_context={}):
		self.request = request
		izin = KelompokJenisIzin.objects.all()
		extra_context.update({'izin': izin})
		return super(IzinAdmin, self).changelist_view(request, extra_context=extra_context)

	def verifikasi_skizin_bupati(self, request, extra_context={}):
		self.request = request
		izin = KelompokJenisIzin.objects.all()
		extra_context.update({'izin': izin})
		return super(IzinAdmin, self).changelist_view(request, extra_context=extra_context)

	def verifikasi_skizin_cetak(self, request, extra_context={}):
		self.request = request
		izin = KelompokJenisIzin.objects.all()
		extra_context.update({'izin': izin})
		return super(IzinAdmin, self).changelist_view(request, extra_context=extra_context)

	def semua_pengajuan(self, request, extra_context={}):
		self.request = request
		izin = KelompokJenisIzin.objects.all()
		extra_context.update({'izin': izin})
		return super(IzinAdmin, self).changelist_view(request, extra_context=extra_context)

	def penomoran_skizin(self, request, extra_context={}):
		self.request = request
		izin = KelompokJenisIzin.objects.all()
		extra_context.update({'izin': izin})
		return super(IzinAdmin, self).changelist_view(request, extra_context=extra_context)

	def stemple_izin(self, request, extra_context={}):
		self.request = request
		izin = KelompokJenisIzin.objects.all()
		extra_context.update({'izin': izin})
		return super(IzinAdmin, self).changelist_view(request, extra_context=extra_context)

	def kasir(self, request, extra_context={}):
		self.request = request
		izin = KelompokJenisIzin.objects.all()
		extra_context.update({'izin': izin})
		return super(IzinAdmin, self).changelist_view(request, extra_context=extra_context)

	def get_telephone_pemohon(self, obj):
		return obj.pemohon.telephone
	get_telephone_pemohon.short_description = "No. Telp"

	def get_list_display(self, request):
		func_view, func_view_args, func_view_kwargs = resolve(request.path)
		if request.user.is_superuser:
			list_display = ('get_no_pengajuan', 'get_tanggal_pengajuan', 'get_kelompok_jenis_izin', 'pemohon','jenis_permohonan','get_status_pengajuan', 'button_cetak_pendaftaran')
		elif func_view.__name__ == 'izinterdaftar':
			list_display = ('get_no_pengajuan', 'no_izin', 'get_kelompok_jenis_izin', 'pemohon', 'get_telephone_pemohon', 'jenis_permohonan')
		elif func_view.__name__ == 'semua_pengajuan':
			list_display = ('get_no_pengajuan', 'get_tanggal_pengajuan', 'get_kelompok_jenis_izin', 'pemohon','jenis_permohonan','get_status_pengajuan', 'button_cetak_pendaftaran')
		# elif func_view.__name__ == 'verifikasi_skizin_kadin':
		else:
			list_display = ('get_no_pengajuan', 'get_tanggal_pengajuan', 'get_kelompok_jenis_izin', 'pemohon', 'jenis_permohonan', 'get_status_pengajuan','button_cetak_pendaftaran')
		# else:
		# 	list_display = ('get_no_pengajuan', 'get_tanggal_pengajuan', 'button_cetak_pendaftaran')
		# else:
			# list_display = ('get_no_pengajuan', 'get_tanggal_pengajuan', 'get_kelompok_jenis_izin', 'pemohon','jenis_permohonan', 'get_status_proses')
		return list_display

	def get_status_pengajuan(self, obj):
		pengajuan = obj.id
		keterangan = '-'
		dibuat_oleh = '-'
		dibuat_tanggal = '-'
		if pengajuan:
			riwayat_ = Riwayat.objects.filter(pengajuan_izin_id=pengajuan).last()
			keterangan = riwayat_.keterangan
			dibuat_oleh = str(riwayat_.created_by.nama_lengkap)
			dibuat_tanggal = str(riwayat_.created_at.strftime("%d-%m-%Y"))
			status = mark_safe("""
				<button type="button" class="btn btn-blue btn-xs mb-10" title="" data-toggle="popover" data-content="Diverifikasi terakhir oleh %s pada tanggal %s" data-original-title="Detil Status" data-trigger="hover" data-placement="left">%s</button>
				""" % (dibuat_oleh, dibuat_tanggal, keterangan))
		return status
	get_status_pengajuan.short_description = "Status Data"


	def get_list_display_links(self, request, list_display):
		func_view, func_view_args, func_view_kwargs = resolve(request.path)
		list_display_links = None
		# list_display_links = ('get_no_pengajuan',)
		# if func_view.__name__ == 'izinterdaftar':
		# 	list_display_links = None
		return list_display_links

	def get_queryset(self, request):
		func_view, func_view_args, func_view_kwargs = resolve(request.path)
		qs = super(IzinAdmin, self).get_queryset(request)
		if func_view.__name__ == 'izinterdaftar':
			pengajuan_ = qs.filter(status=1)
		elif func_view.__name__ == 'semua_pengajuan':
			pengajuan_ = qs.filter(~Q(status=11) and ~Q(status=8))
		elif func_view.__name__ == 'survey':
			pengajuan_ = qs.filter(status=8)
		elif func_view.__name__ == 'verifikasi_operator':
			pengajuan_ = qs.filter(status=6)
		elif func_view.__name__ == 'verifikasi_kabid':
			pengajuan_ = qs.filter(status=4)
		elif func_view.__name__ == 'verifikasi_pembuat_surat':
			pengajuan_ = qs.filter(skizin__isnull=True, status=2)
		elif func_view.__name__ == 'kasir':
			pengajuan_ = qs.filter(status=5)
		elif func_view.__name__ == 'verifikasi_skizin_kabid':
			id_pengajuan_list = []
			if request.user.groups.filter(name='Kabid'):
				id_list = SKIzin.objects.filter(status=6).values_list('pengajuan_izin_id', flat=True)
				id_pengajuan_list += id_list
			pengajuan_ = qs.filter(id__in=id_pengajuan_list)
		elif func_view.__name__ == 'verifikasi_skizin_kadin':
			id_pengajuan_list = []
			if request.user.groups.filter(name='Kadin'):
				id_list = SKIzin.objects.filter(status=4).values_list('pengajuan_izin_id', flat=True)
				id_pengajuan_list += id_list
			pengajuan_ = qs.filter(id__in=id_pengajuan_list)
		elif func_view.__name__ == 'verifikasi_skizin_bupati':
			id_pengajuan_list = []
			if request.user.groups.filter(name='Bupati'):	
				id_list = SKIzin.objects.filter(status=12).values_list('pengajuan_izin_id', flat=True)
				id_pengajuan_list += id_list
			pengajuan_ = qs.filter(id__in=id_pengajuan_list)
		elif func_view.__name__ == 'verifikasi_skizin_cetak':
			id_pengajuan_list = []
			if request.user.groups.filter(name='Cetak'):
				id_list = SKIzin.objects.filter(status=10).values_list('pengajuan_izin_id', flat=True)
				id_pengajuan_list += id_list
			pengajuan_ = qs.filter(id__in=id_pengajuan_list)
		elif func_view.__name__ == 'penomoran_skizin':
			id_pengajuan_list = []
			if request.user.groups.filter(name='Penomoran'):
				id_list = SKIzin.objects.filter(status=9).values_list('pengajuan_izin_id', flat=True)
				id_pengajuan_list += id_list
			pengajuan_ = qs.filter(id__in=id_pengajuan_list)
		elif func_view.__name__ == 'stemple_izin':
			id_pengajuan_list = []
			if request.user.groups.filter(name='Selesai'):
				id_list = SKIzin.objects.filter(status=2).values_list('pengajuan_izin_id', flat=True)
				id_pengajuan_list += id_list
			pengajuan_ = qs.filter(id__in=id_pengajuan_list)
		else:
			pengajuan_ = qs
		return pengajuan_.order_by('-updated_at')

	def get_perusahaan(self, obj):
		return obj.perusahaan
	get_perusahaan.short_description = "Perusahaan"

	def get_status_proses(self, obj):
		return "%s\n%s" % (obj.created_at.strftime("%d/%m/%y"), "Pengajuan Dibuat")
	get_status_proses.short_description = "Tgl & Status Proses"

	def get_kelompok_jenis_izin(self, obj):
		return obj.kelompok_jenis_izin
	get_kelompok_jenis_izin.short_description = "Izin Pengajuan"

	def get_tanggal_pengajuan(self, obj):
		return obj.created_at.strftime("%d-%m-%y")
	get_tanggal_pengajuan.short_description = "Tgl. Pengajuan"

	def get_no_pengajuan(self, obj):
		# no_pengajuan = mark_safe("""
		# 	<a href="%s" target="_blank"> %s </a>
		# 	""" % ("#", obj.no_pengajuan ))
		split_ = obj.no_pengajuan
		# print split_
		no_pengajuan = mark_safe("""
				<span>%s</span>
				""" % ( obj.no_pengajuan ))
		# if split_[0] == 'SIUP':
			# if request.user.is_superuser:
			# 	no_pengajuan = mark_safe("""
			# 	<a href="%s" target="_blank"> %s </a>
			# 	""" % (reverse('admin:izin_detilsiup_change', args=(obj.id,)), obj.no_pengajuan ))
			# else:
			# no_pengajuan
		# elif split_[0] == 'Reklame':
			# if request.user.is_superuser:
			# 	no_pengajuan = mark_safe("""
			# 	<a href="%s" target="_blank"> %s </a>
			# 	""" % (reverse('admin:izin_detilreklame_change', args=(obj.id,)), obj.no_pengajuan ))
			# else:
			# no_pengajuan
		# elif split_[0] == 'TDP':
			# if request.user.is_superuser:
			# 	no_pengajuan = mark_safe("""
			# 	<a href="%s" target="_blank"> %s </a>
			# 	""" % (reverse('admin:izin_detiltdp_change', args=(obj.id,)), obj.no_pengajuan ))
			# else:
			# no_pengajuan
		return no_pengajuan
	get_no_pengajuan.short_description = "No. Pengajuan"

	def linkdetilizin(self, obj):
		link_ = '#'
		jenis_izin_ = obj.kelompok_jenis_izin.kode
		print jenis_izin_
		if jenis_izin_ == "503.08":
			link_ = reverse('admin:detil_siup_view', kwargs={'id_pengajuan_izin_': obj.id})
		elif jenis_izin_ == "503.03.01/" or jenis_izin_ == "503.03.02/":
			link_ = reverse('admin:view_pengajuan_reklame', kwargs={'id_pengajuan_izin_': obj.id})
		elif jenis_izin_ == "IUJK":
			link_ = reverse('admin:view_pengajuan_iujk', kwargs={'id_pengajuan_izin_': obj.id})
		elif jenis_izin_ == "503.01.06/":
			link_ = reverse('admin:view_pengajuan_imb_reklame', kwargs={'id_pengajuan_izin_': obj.id})
		elif jenis_izin_ == "503.01.05/":
			link_ = reverse('admin:view_pengajuan_imb_umum', kwargs={'id_pengajuan_izin_': obj.id})
		elif jenis_izin_ == "503.01.04/":
			link_ = reverse('admin:view_pengajuan_imb_perumahan', kwargs={'id_pengajuan_izin_': obj.id})
		elif jenis_izin_ == "503.06.01/":
			link_ = reverse('admin:view_pemakaian_kekayaan_daerah', kwargs={'id_pengajuan_izin_': obj.id})	
		elif jenis_izin_ == "503.02/":
			link_ = reverse('admin:view_pengajuan_izin_gangguan', kwargs={'id_pengajuan_izin_': obj.id})
		elif obj.kelompok_jenis_izin.kode == "HULLER":
			link_ = reverse('admin:view_pengajuan_huller', kwargs={'id_pengajuan_izin_': obj.id})
		elif jenis_izin_ == "503.07/" or obj.kelompok_jenis_izin.kode == "IPPT-Rumah":
			link_ = reverse('admin:view_pengajuan_izin_lokasi', kwargs={'id_pengajuan_izin_': obj.id})
		elif obj.kelompok_jenis_izin.kode == "IPPT-Usaha":
			link_ = reverse('admin:view_pengajuan_ippt_usaha', kwargs={'id_pengajuan_izin_': obj.id})	
		btn = mark_safe("""
				<a href="%s" target="_blank" class="btn btn-primary btn-rounded btn-ef btn-ef-5 btn-ef-5a mb-10"><i class="icon-eyeglasses"></i> <span>Detil</span> </a>
				""" % link_ )
		return btn
	linkdetilizin.short_description = "Aksi"

	def button_cetak_pendaftaran(self, obj):
		link_ = '#'
		jenis_izin_ = obj.kelompok_jenis_izin.kode
		if jenis_izin_ == "503.08":
			link_ = reverse('admin:view_pengajuan_siup', kwargs={'id_pengajuan_izin_': obj.id})
		elif jenis_izin_ == "503.03.01/" or jenis_izin_ == "503.03.02/":
			link_ = reverse('admin:view_pengajuan_reklame', kwargs={'id_pengajuan_izin_': obj.id})
		elif jenis_izin_ == "IUJK":
			link_ = reverse('admin:view_pengajuan_iujk', kwargs={'id_pengajuan_izin_': obj.id})
		elif jenis_izin_ == "503.01.06/":
			link_ = reverse('admin:view_pengajuan_imb_reklame', kwargs={'id_pengajuan_izin_': obj.id})
		elif jenis_izin_ == "503.01.04/":
			link_ = reverse('admin:view_pengajuan_imb_perumahan', kwargs={'id_pengajuan_izin_': obj.id})
		elif jenis_izin_ == "503.01.05/":
			link_ = reverse('admin:view_pengajuan_imb_umum', kwargs={'id_pengajuan_izin_': obj.id})
		elif jenis_izin_ == "503.06.01/":
			link_ = reverse('admin:view_pemakaian_kekayaan_daerah', kwargs={'id_pengajuan_izin_': obj.id})	
		elif jenis_izin_ == "503.02/":
			link_ = reverse('admin:view_pengajuan_izin_gangguan', kwargs={'id_pengajuan_izin_': obj.id})
		elif jenis_izin_ == "503.07/" or obj.kelompok_jenis_izin.kode == "IPPT-Rumah":
			link_ = reverse('admin:view_pengajuan_izin_lokasi', kwargs={'id_pengajuan_izin_': obj.id})
		elif obj.kelompok_jenis_izin.kode == "HULLER":
			link_ = reverse('admin:view_pengajuan_huller', kwargs={'id_pengajuan_izin_': obj.id})
		elif obj.kelompok_jenis_izin.kode == "IPPT-Usaha":
			link_ = reverse('admin:view_pengajuan_ippt_usaha', kwargs={'id_pengajuan_izin_': obj.id})		
		elif obj.kelompok_jenis_izin.kode == "TDP-PT":
			link_ = reverse('admin:view_pengajuan_tdp_pt', kwargs={'id_pengajuan_izin_': obj.id})
		elif obj.kelompok_jenis_izin.kode == "TDP-CV":
			link_ = reverse('admin:view_pengajuan_tdp_cv', kwargs={'id_pengajuan_izin_': obj.id})
		elif obj.kelompok_jenis_izin.kode == "TDP-FIRMA":
			link_ = reverse('admin:view_pengajuan_tdp_firma', kwargs={'id_pengajuan_izin_': obj.id})
		elif obj.kelompok_jenis_izin.kode == "TDP-PERORANGAN":
			link_ = reverse('admin:view_pengajuan_tdp_perorangan', kwargs={'id_pengajuan_izin_': obj.id})
		elif obj.kelompok_jenis_izin.kode == "TDP-BUL":
			link_ = reverse('admin:view_pengajuan_tdp_bul', kwargs={'id_pengajuan_izin_': obj.id})
		elif obj.kelompok_jenis_izin.kode == "TDP-KOPERASI":
			link_ = reverse('admin:view_pengajuan_tdp_koperasi', kwargs={'id_pengajuan_izin_': obj.id})
		elif obj.kelompok_jenis_izin.kode == "TDUP":
			link_ = reverse('admin:view_pengajuan_izin_tdup', kwargs={'id_pengajuan_izin_': obj.id})
		btn = mark_safe("""
				<a href="%s" class="btn btn-success btn-rounded btn-ef btn-ef-5 btn-ef-5a mb-10"><i class="fa fa-cog fa-spin"></i> <span>Proses</span> </a>
				""" % link_ )
		return btn
	button_cetak_pendaftaran.short_description = "Aksi"

	def pendaftaran_selesai(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Pengajuan Selesai'})
			pengajuan_ = PengajuanIzin.objects.get(id=id_pengajuan_izin_)
			extra_context.update({'pemohon': pengajuan_.pemohon})
			extra_context.update({'id_pengajuan': pengajuan_.id})
			extra_context.update({'jenis_pemohon': pengajuan_.pemohon.jenis_pemohon})
			extra_context.update({'alamat_pemohon': str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)})
			extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})
		template = loader.get_template("admin/izin/izin/pengajuan_baru_selesai.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_siup_asli(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			pengajuan_ = DetilSIUP.objects.get(id=id_pengajuan_izin_)
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", Ds. "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+",f"+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Ds. "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_perusahaan': alamat_perusahaan_})
				extra_context.update({'perusahaan': pengajuan_.perusahaan })
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'pengajuan': pengajuan_ })
			extra_context.update({'foto': pengajuan_.pemohon.berkas_foto.all().last()})
			# kelembagaan = pengajuan_.kelembagaan.kelembagaan.upper()
			# extra_context.update({'kelembagaan': kelembagaan })
			if pengajuan_.kekayaan_bersih:
				kekayaan_ = pengajuan_.kekayaan_bersih.replace('.', '')
				terbilang_ = terbilang(int(kekayaan_))
				extra_context.update({'terbilang': str(terbilang_) })
				extra_context.update({ 'kekayaan_bersih': "Rp "+str(pengajuan_.kekayaan_bersih) })
			skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
			if skizin_:
				extra_context.update({'skizin': skizin_ })
				extra_context.update({'skizin_status': skizin_.status })
			kepala_ =  Pegawai.objects.filter(jabatan__nama_jabatan="Kepala Dinas").last()
			if kepala_:
				extra_context.update({'kepala_dinas': kepala_ })
				extra_context.update({'nip_kepala_dinas': kepala_.nomoridentitaspengguna_set.last() })
			template = Template.objects.filter(kelompok_jenis_izin=pengajuan_.kelompok_jenis_izin).last()
			extra_context.update({'template': template })
		template = loader.get_template("front-end/include/formulir_siup/cetak_siup_asli.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def total_izin(self, request):
		id_elemet = []
		jumlah_izin = []
		pesan = []
		url = []
		total = 0
		if request.user.groups.filter(name='Operator'):
			pengajuan_ = PengajuanIzin.objects.filter(status=6).count()
			id_elemet.append('operator')
			jumlah_izin.append(pengajuan_)
			url = "/admin/izin/pengajuanizin/verifikasi-operator/"
			total = pengajuan_
		if request.user.groups.filter(name='Kasir'):
			pengajuan_ = PengajuanIzin.objects.filter(status=5).count()
			id_elemet.append('kasir')
			jumlah_izin.append(pengajuan_)
			url = "/admin/izin/pengajuanizin/kasir/"
			total = pengajuan_
		if request.user.groups.filter(name='Kabid'):
			# verifikasi pengajuan
			pengajuan_ = PengajuanIzin.objects.filter(status=4).count()
			id_elemet.append('kabid_pengajuan')
			jumlah_izin.append(pengajuan_)
			url = "/admin/izin/pengajuanizin/verifikasi-operator/"
			total = pengajuan_ + total
			# kabid draft sk
			skizin = SKIzin.objects.filter(status=6).count()
			id_elemet.append('kabid_skizin')
			jumlah_izin.append(skizin)
			url = "/admin/izin/pengajuanizin/verifikasi-skizin-kabid/"
			total = skizin + total
		if request.user.groups.filter(name='Pembuat Surat'):
			pengajuan_ = PengajuanIzin.objects.filter(skizin__isnull=True, status=2).count()
			id_elemet.append('pembuat_surat')
			jumlah_izin.append(pengajuan_)
			url = "/admin/izin/pengajuanizin/verifikasi-pembuat-surat/"
			total = pengajuan_ + total
		if request.user.groups.filter(name='Penomoran'):
			pengajuan_ = len(SKIzin.objects.filter(status=9).values('pengajuan_izin_id'))
			id_elemet.append('penomoran')
			jumlah_izin.append(pengajuan_)
			url = "/admin/izin/pengajuanizin/penomoran-skizin/"
			total = pengajuan_ + total
		if request.user.groups.filter(name='Kadin'):
			skizin = len(SKIzin.objects.filter(status=4).values('pengajuan_izin_id'))
			id_elemet.append('kadin_skizin')
			jumlah_izin.append(skizin)
			url = "/admin/izin/pengajuanizin/verifikasi-skizin-kadin/"
			total = skizin + total
		if request.user.groups.filter(name='Bupati'):
			skizin = len(SKIzin.objects.filter(status=12).values('pengajuan_izin_id'))
			id_elemet.append('bupati_skizin')
			jumlah_izin.append(skizin)
			url = "/admin/izin/pengajuanizin/verifikasi-skizin-bupati/"
			total = skizin + total
		if request.user.groups.filter(name='Cetak'):
			skizin = len(SKIzin.objects.filter(status=10).values('pengajuan_izin_id'))
			id_elemet.append('cetak')
			jumlah_izin.append(skizin)
			url = "/admin/izin/pengajuanizin/verifikasi-skizin-cetak"
			total = skizin + total
		if request.user.groups.filter(name='Selesai'):
			skizin = len(SKIzin.objects.filter(status=2).values('pengajuan_izin_id'))
			id_elemet.append('selesai')
			jumlah_izin.append(skizin)
			url = "/admin/izin/pengajuanizin/stemple-skizin/"
			total = skizin + total

		if request.user.groups.filter(name='Cek Lokasi'):
			skizin = 0
			id_elemet.append('cek_lokasi')
			jumlah_izin.append(skizin)
			url = "/admin/izin/survey/"
			total = skizin + total

		pesan = "Ada "+str(total)+" Izin yang harus dikerjakan."
		total = total

		data = {'success': True, 'pesan': 'Perusahaan Sudah Ada.', 'id_elemet':id_elemet, 'jumlah_izin':jumlah_izin , 'pesan': pesan, 'url': url, 'total': total}
		return HttpResponse(json.dumps(data))

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

	def option_kelompokjenisizin(self, request):
		kode_jenis_izin = request.POST.get('param', None)
		if kode_jenis_izin:
			kelompokjenisizin_list = KelompokJenisIzin.objects.filter(jenis_izin__kode=kode_jenis_izin)
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
		
	def create_skizin(self, request):
		id_detil_siup = request.POST.get('id_detil_siup', None)
		# if request.user.has_perm('izin.change_detilsiup') or request.user.is_superuser or request.user.groups.filter(name='Admin Sistem'):
		# print id_detil_siup
		if request.user.has_perm('izin.add_skizin') or request.user.is_superuser or request.user.groups.filter(name='Admin Sistem'):
			pengajuan_ = PengajuanIzin.objects.filter(id=id_detil_siup).last()
			template_ = Template.objects.filter(kelompok_jenis_izin=pengajuan_.kelompok_jenis_izin).last()
			body_html = ""
			if template_:
				body_html = template_.body_html
			skizin = SKIzin(
				pengajuan_izin_id = id_detil_siup,
				created_by_id = request.user.id,
				body_html = body_html,
				status = 6)
			skizin.save()
			# print "id_skizin"+str(skizin.id)
			riwayat_ = Riwayat(
				sk_izin_id = skizin.id ,
				pengajuan_izin_id = id_detil_siup,
				created_by_id = request.user.id,
				keterangan = "Draf (Izin)" 
				)
			riwayat_.save()
			response = {
						"success": True,
						"pesan": "Draft SKIzin berhasil tersimpan.",
						"redirect": '',
					}
		else:
			response = {
				"success": False,
				"pesan": "Anda tidak memiliki hak akses untuk memverifikasi izin.",
			}
		return HttpResponse(json.dumps(response))
	
	def aksi_detil_siup(self, request):
		id_pengajuan_izin = request.POST.get('id_detil_siup')
		try:
			obj = PengajuanIzin.objects.get(id=id_pengajuan_izin)
			# and request.user.has_perm('izin.change_detilsiup') or request.user.is_superuser or request.user.groups.filter(name='Admin Sistem')
			# print request.POST.get('aksi')
			if request.POST.get('aksi'):
				# print 'masuk'
				if request.POST.get('aksi') == '_submit_operator':
					# print "operator"
					obj.status = 4
					obj.verified_by_id = request.user.id
					obj.verified_at = datetime.datetime.now()
					obj.save()
					riwayat_ = Riwayat(
						pengajuan_izin_id = id_pengajuan_izin,
						created_by_id = request.user.id,
						keterangan = "Submitted (Pengajuan)"
					)
					riwayat_.save()
					response = {
						"success": True,
						"pesan": "Izin berhasil di verifikasi.",
						"redirect": '',
					}
				elif request.POST.get('aksi') == '_submit_kabid':
					obj.status = 2
					obj.verified_by_id = request.user.id
					obj.verified_at = datetime.datetime.now()
					obj.save()
					riwayat_ = Riwayat(
						pengajuan_izin_id = id_pengajuan_izin,
						created_by_id = request.user.id,
						keterangan = "Kabid Verified (Pengajuan)"
					)
					# print Survey.objects.filter(pengajuan=obj)
					s = Survey.objects.filter(pengajuan=obj)
					# print s
					if s.exists():
						for i in s:
							i.status = 1
							i.save()

					riwayat_.save()
					response = {
						"success": True,
						"pesan": "Izin berhasil di verifikasi.",
						"redirect": '',
					}
				elif request.POST.get('aksi') == '_submit_edit_skizin':
					try:
						if request.POST.get('tdp_pt') == 'TDP PT':
							p = DetilTDP.objects.get(id=id_pengajuan_izin)
						else:
							p = DetilSIUP.objects.get(id=id_pengajuan_izin)
						# print request.POST.get('produk_utama')
						p.produk_utama = request.POST.get('produk_utama')
						p.save()
						response = {
							"success": True,
							"pesan": "Barang / Jasa Perdagangan Utama berhasil di edit.",
							"redirect": '',
						}
					except:
						response = {
							"success": False,
							"pesan": "Anda tidak memiliki hak akses untuk memverifikasi izin.",
							"redirect": '',
						}
				elif request.POST.get('aksi') == '_submit_edit_status_pusat':
					status_pusat = request.POST.get('status_pusat')
					if status_pusat:
						try:
							p = DetilTDP.objects.get(id=id_pengajuan_izin)
							print status_pusat
							p.status_waralaba = status_pusat
							p.save()
							response = {
								"success": True,
								"pesan": "Status Pusat berhasil diedit.",
								"redirect": '',
							}
						except ObjectDoesNotExist:
							response = {
								"success": False,
								"pesan": "Status Pusat gagal diedit.",
								"redirect": '',
							}
					else:
						response = {
							"success": False,
							"pesan": "Inputan Status Pusat kosong.",
							"redirect": '',
						}	
				
				elif request.POST.get('aksi') == '_submit_buat_skizin':
					skizin = SKIzin(
						pengajuan_izin_id = obj.id,
						created_by_id = request.user.id,
						status = 11)
					skizin.save()
					# riwayat_ = Riwayat(
					# 	sk_izin_id = skizin.id ,
					# 	pengajuan_izin_id = obj.id,
					# 	created_by_id = request.user.id,
					# 	keterangan = "Draf (Izin)" 
					# 	)
					# riwayat_.save()
					response = {
						"success": True,
						"pesan": "Draft SKIzin berhasil dibuat.",
						"redirect": '',
					}
				else:
					response = {
						"success": False,
						"pesan": "Anda tidak memiliki hak akses untuk memverifikasi izin.s",
						"redirect": '',
					}
				try:
					obj_skizin = SKIzin.objects.get(pengajuan_izin_id=id_pengajuan_izin)
					# print obj_skizin
					if request.POST.get('aksi') == '_submit_generate_skizin':

						obj_skizin.status = 6
						obj_skizin.save()
						obj.verified_by_id = request.user.id
						obj.verified_at = datetime.datetime.now()
						obj.save()
						riwayat_ = Riwayat(
							sk_izin_id = obj_skizin.id ,
							pengajuan_izin_id = id_pengajuan_izin,
							created_by_id = request.user.id,
							keterangan = "Draft (SKIzin)"
						)
						riwayat_.save()
						response = {
							"success": True,
							"pesan": "SKIzin berhasil dibuat.",
							"redirect": '',
						}
					elif request.POST.get('aksi') == '_submit_skizin_kabid':
						obj_skizin.status = 4
						obj_skizin.save()
						obj.verified_by_id = request.user.id
						obj.verified_at = datetime.datetime.now()
						obj.save()
						riwayat_ = Riwayat(
							sk_izin_id = obj_skizin.id ,
							pengajuan_izin_id = id_pengajuan_izin,
							created_by_id = request.user.id,
							keterangan = "Kabid Verified (Izin)"
						)
						riwayat_.save()
						response = {
							"success": True,
							"pesan": "SKIzin berhasil di verifikasi.",
							"redirect": '',
						}
					elif request.POST.get('aksi') == '_submit_skizin_kabid_to_kasir':
						obj.status = 5
						obj.verified_by_id = request.user.id
						obj.verified_at = datetime.datetime.now()
						obj.save()
						obj_skizin.status = 5
						obj_skizin.save()
						riwayat_ = Riwayat(
							sk_izin_id = obj_skizin.id ,
							pengajuan_izin_id = id_pengajuan_izin,
							created_by_id = request.user.id,
							keterangan = "Kabid Verified (Izin)"
						)
						riwayat_.save()
						response = {
							"success": True,
							"pesan": "SKIzin berhasil di verifikasi.",
							"redirect": '',
						}

					elif request.POST.get('aksi') == '_submit_skizin_kadin':
						pejabat = Pegawai.objects.filter(id=request.user.id).last()
						# print request.user.id
						# print pejabat.nama_lengkap
						obj_skizin.status = 9
						gelar_depan = ""
						gelar_belakang = ""
						if pejabat.gelar_depan:
							gelar_depan = pejabat.gelar_depan
						if pejabat.gelar_belakang:
							gelar_belakang = pejabat.gelar_belakang
						nama_pejabat = str(gelar_depan)+" "+str(pejabat.nama_lengkap)+" "+str(gelar_belakang)
						obj_skizin.nama_pejabat = nama_pejabat
						obj_skizin.nip_pejabat = str(pejabat.username)
						if pejabat.jabatan:
							obj_skizin.jabatan_pejabat = str(pejabat.jabatan.nama_jabatan.upper())+" DPMPTSP"
						else:
							obj_skizin.jabatan_pejabat = "Kepala Dinas DPMPTSP"
						obj_skizin.keterangan = "Pembina Tk.l"
						obj_skizin.save()
						obj.verified_by_id = request.user.id
						obj.verified_at = datetime.datetime.now()
						obj.save()
						riwayat_ = Riwayat(
							sk_izin_id = obj_skizin.id ,
							pengajuan_izin_id = id_pengajuan_izin,
							created_by_id = request.user.id,
							keterangan = "Kadin Verified (Izin)"
						)
						riwayat_.save()
						response = {
							"success": True,
							"pesan": "SKIzin berhasil di verifikasi.",
							"redirect": '',
						}
					
					#Digunakan untuk verifikasi Bupati
					elif request.POST.get('aksi') == '_submit_skizin_kadin_to_bupati':
						pejabat = Pegawai.objects.filter(id=request.user.id).last()
						# print request.user.id
						# print pejabat.nama_lengkap
						obj_skizin.status = 12
						gelar_depan = ""
						gelar_belakang = ""
						if pejabat.gelar_depan:
							gelar_depan = pejabat.gelar_depan
						if pejabat.gelar_belakang:
							gelar_belakang = pejabat.gelar_belakang
						nama_pejabat = str(gelar_depan)+" "+str(pejabat.nama_lengkap)+" "+str(gelar_belakang)
						obj_skizin.nama_pejabat = nama_pejabat
						obj_skizin.nip_pejabat = str(pejabat.username)
						if pejabat.jabatan:
							obj_skizin.jabatan_pejabat = str(pejabat.jabatan.nama_jabatan.upper())+" DPMPTSP"
						else:
							obj_skizin.jabatan_pejabat = "Kepala Dinas DPMPTSP"

						obj_skizin.keterangan = "Pembina Tk.l"
						obj_skizin.save()
						obj.status = 12
						obj.verified_by_id = request.user.id
						obj.verified_at = datetime.datetime.now()
						obj.save()
						riwayat_ = Riwayat(
							sk_izin_id = obj_skizin.id ,
							pengajuan_izin_id = id_pengajuan_izin,
							created_by_id = request.user.id,
							keterangan = "Kadin Verified (Izin)"
						)
						riwayat_.save()
						response = {
							"success": True,
							"pesan": "SKIzin berhasil di verifikasi.",
							"redirect": '',
						}

					elif request.POST.get('aksi') == '_submit_skizin_bupati':
						pejabat = Pegawai.objects.filter(id=request.user.id).last()
						# print request.user.id
						# print pejabat.nama_lengkap
						obj_skizin.status = 9

						#Keterangan Yang Digunakan Untuk Sk Izin	
						obj_skizin.keterangan = "Pembina Tk.l"

						obj_skizin.save()
						obj.verified_by_id = request.user.id
						obj.verified_at = datetime.datetime.now()
						obj.save()
						riwayat_ = Riwayat(
							sk_izin_id = obj_skizin.id ,
							pengajuan_izin_id = id_pengajuan_izin,
							created_by_id = request.user.id,
							keterangan = "Bupati Verified (Izin)"
						)
						riwayat_.save()
						response = {
							"success": True,
							"pesan": "SKIzin berhasil di verifikasi.",
							"redirect": '',
						}

					# elif request.POST.get('aksi') == '_submit_sk_kasir_kadin':
					# 	pejabat = Pegawai.objects.filter(id=request.user.id).last()
					# 	obj.status = 5
					# 	obj.save()
					# 	obj_skizin.status = 9
					# 	gelar_depan = ""
					# 	gelar_belakang = ""
					# 	if pejabat.gelar_depan:
					# 		gelar_depan = pejabat.gelar_depan
					# 	if pejabat.gelar_belakang:
					# 		gelar_belakang = pejabat.gelar_belakang
					# 	nama_pejabat = str(gelar_depan)+" "+str(pejabat.nama_lengkap)+" "+str(gelar_belakang)
					# 	obj_skizin.nama_pejabat = nama_pejabat
					# 	obj_skizin.nip_pejabat = str(pejabat.username)
					# 	if pejabat.jabatan:
					# 		obj_skizin.jabatan_pejabat = str(pejabat.jabatan.nama_jabatan.upper())+" DPMPTSP"
					# 	else:
					# 		obj_skizin.jabatan_pejabat = "Kepala Dinas DPMPTSP"
					# 	obj_skizin.keterangan = "Pembina Tk.l"
					# 	obj_skizin.save()
					# 	riwayat_ = Riwayat(
					# 		sk_izin_id = obj_skizin.id ,
					# 		pengajuan_izin_id = id_pengajuan_izin,
					# 		created_by_id = request.user.id,
					# 		keterangan = "Kadin Verified (Izin)"
					# 	)
					# 	riwayat_.save()
					# 	response = {
					# 		"success": True,
					# 		"pesan": "SKIzin berhasil di verifikasi.",
					# 		"redirect": '',
					# 	}
					elif request.POST.get('aksi') == '_submit_penomoran':
						obj_skizin.status = 10
						obj_skizin.save()
						obj.verified_by_id = request.user.id
						obj.verified_at = datetime.datetime.now()
						obj.save()
						try:
							kode_izin_ =  request.POST.get('kode_jenis_izin')
							nomor_urut_ = request.POST.get('kode_izin')
							tahun_ = request.POST.get('tahun')
							nomor_sk = request.POST.get('nomor_izin_sk')
							obj.no_izin = kode_izin_+"/"+nomor_urut_+"/"+nomor_sk+"/"+tahun_
							obj.save()
							riwayat_ = Riwayat(
								sk_izin_id = obj_skizin.id ,
								pengajuan_izin_id = id_pengajuan_izin,
								created_by_id = request.user.id,
								keterangan = "Registered (Izin)"
							)
							riwayat_.save()
							response = {
								"success": True,
								"pesan": "SKIzin berhasil di register.",
								"redirect": '',
							}
						except IntegrityError:
							response = {
								"success": False,
								"pesan": "Nomor SKIzin telah ada coba cek kembali.",
								"redirect": '',
							}
					
					elif request.POST.get('aksi') == '_submit_penomoran_tdp':
						obj_skizin.status = 10
						obj_skizin.created_at = datetime.datetime.now()
						obj_skizin.save()
						obj.verified_by_id = request.user.id
						obj.verified_at = datetime.datetime.now()
						obj.save()

						# Untuk Penomoran 
						# obj.verified_at = datetime.datetime.now()
						# obj.save()
						#
						try:
							nomor = request.POST.get('nomor')
							if nomor:
								obj.no_izin = nomor
								obj.save()

								if obj.kelompok_jenis_izin.kode == "IUJK":
									from dateutil.relativedelta import relativedelta
									obj_skizin.masa_berlaku_izin = datetime.datetime.now()+relativedelta(years=3)
									obj_skizin.save()

								riwayat_ = Riwayat(
									sk_izin_id = obj_skizin.id ,
									pengajuan_izin_id = id_pengajuan_izin,
									created_by_id = request.user.id,
									keterangan = "Registered (Izin)"
								)
								riwayat_.save()
								response = {
									"success": True,
									"pesan": "SKIzin berhasil di register.",
									"redirect": '',
								}
							
							else:
								response = {
									"success": False,
									"pesan": "Nomor Kosong.",
									"redirect": '',
								}
						except IntegrityError:
							if obj.kelompok_jenis_izin.kode == "IUJK":
								obj.no_izin = nomor+"/perubahan"
								obj.save()

								if obj.kelompok_jenis_izin.kode == "IUJK":
									from dateutil.relativedelta import relativedelta
									obj_skizin.masa_berlaku_izin = datetime.datetime.now()+relativedelta(years=3)
									obj_skizin.save()
								riwayat_ = Riwayat(
									sk_izin_id = obj_skizin.id ,
									pengajuan_izin_id = id_pengajuan_izin,
									created_by_id = request.user.id,
									keterangan = "Registered (Izin)"
								)
								riwayat_.save()
								response = {
									"success": True,
									"pesan": "SKIzin Perubahan berhasil di register.",
									"redirect": '',
								}
							else:	
								response = {
									"success": False,
									"pesan": "Nomor SKIzin telah ada coba cek kembali.",
									"redirect": '',
								}
					elif request.POST.get('aksi') == '_submit_cetak_izin':
						obj_skizin.status = 2
						obj_skizin.save()
						obj.verified_by_id = request.user.id
						obj.verified_at = datetime.datetime.now()
						obj.save()
						riwayat_ = Riwayat(
							sk_izin_id = obj_skizin.id ,
							pengajuan_izin_id = id_pengajuan_izin,
							created_by_id = request.user.id,
							keterangan = "Printed (Izin)"
						)
						riwayat_.save()
						response = {
							"success": True,
							"pesan": "SKIzin berhasil di cetak.",
							"redirect": '',
						}
					elif request.POST.get('aksi') == '_submit_izin_selsai':
						obj_skizin.status = 1
						obj_skizin.save()
						obj.status = 1
						obj.verified_by_id = request.user.id
						obj.verified_at = datetime.datetime.now()
						if obj.pemohon:
							obj.pemohon.status = 1
						if obj.kelompok_jenis_izin:
							if obj.kelompok_jenis_izin.kode:
								obj_detil_ = get_model_detil(obj.kelompok_jenis_izin.kode)
								if obj_detil_:
									obj_detil_ = obj_detil_.objects.filter(id=obj.id).last()
									if obj_detil_:
										if obj_detil_.perusahaan:
											obj_detil_.perusahaan.status = 1
											obj_detil_.save()
						# if obj.perusahaan:
						# 	obj.perusahaan.status = 1
						obj.save()
						riwayat_ = Riwayat(
							sk_izin_id = obj_skizin.id ,
							pengajuan_izin_id = id_pengajuan_izin,
							created_by_id = request.user.id,
							keterangan = "Finished (Izin)"
						)
						riwayat_.save()
						response = {
							"success": True,
							"pesan": "Izin telah selsai diproses.",
							"redirect": '',
						}
					elif request.POST.get('aksi') == '_submit_kasir':
						obj.status = 5
						obj.verified_by_id = request.user.id
						obj.verified_at = datetime.datetime.now()
						obj.save()
						obj_skizin.status = 5
						obj_skizin.save()
						riwayat_ = Riwayat(
							pengajuan_izin_id = id_pengajuan_izin,
							created_by_id = request.user.id,
							keterangan = "Kadin Verified To Kasir (Pengajuan)"
						)
						riwayat_.save()
						response = {
							"success": True,
							"pesan": "Izin berhasil di verifikasi.",
							"redirect": '',
						}
				except ObjectDoesNotExist:
					pass
			else:
				response = {
					"success": False,
					"pesan": "Anda tidak memiliki hak akses untuk memverifikasi izin.b",
					"redirect": '',
				}
		except ObjectDoesNotExist:
			response = {
					"success": False,
					"pesan": "Terjadi kesalahan, pengajuan izin tidak ada dalam daftar.",
					"redirect": '',
				}
		return HttpResponse(json.dumps(response))


	def penolakanizin(self, request):
		from master.models import Berkas
		id_detil_siup = request.POST.get('id_pengajuan')
		try:
			obj = PengajuanIzin.objects.get(id=id_detil_siup)
			if request.user.is_superuser or request.user.groups.filter(name='Admin Sistem') or request.user.groups.filter(name='Operator') or request.user.groups.filter(name='Kabid') or request.user.groups.filter(name='Kadin'):
				berkas =  request.FILES.get('berkas', None)
				if request.method == "POST":
					riwayat_ = Riwayat(
									alasan = request.POST.get('alasan', None),
									pengajuan_izin_id = id_detil_siup,
									created_by_id = request.user.id,
									keterangan = "Tolak (Izin)."
								)
					# cek bila berkas kosong jika kosong lewati
					if berkas and berkas is not None:
						berkas_obj = Berkas(
							nama_berkas = 'Berkas Penolakan Izin '+str(obj.pemohon.nama_lengkap),
							berkas = berkas,
							created_by_id = request.user.id,
							)
						berkas_obj.save()
						riwayat_.berkas_id = berkas_obj.id
					riwayat_.save()
					try:
						obj_skizin = SKIzin.objects.get(pengajuan_izin_id=id_detil_siup)
						obj_skizin.status = 7
						obj_skizin.created_by_id = request.user.id
						obj_skizin.save()
						riwayat_.sk_izin = obj_skizin
						riwayat_.save()
					except ObjectDoesNotExist:
						pass

					response = {
								"success": True,
								"pesan": "Izin telah ditolak.",
								"redirect": '',
							}
				else:
					response = {
						"success": False,
						"pesan": "Terjadi kesalahan server",
						"redirect": '',
					}
			else:
				response = {
					"success": False,
					"pesan": "Anda tidak memiliki hak akses untuk memverifikasi izin.",
					"redirect": '',
				}
		except ObjectDoesNotExist:
			response = {
					"success": False,
					"pesan": "Terjadi kesalahan, detil siup tidak ada dalam daftar.",
					"redirect": '',
				}
		return HttpResponse(json.dumps(response))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(IzinAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^wizard/add/$', self.admin_site.admin_view(add_wizard_siup), name='add_wizard_izin'),
			url(r'^option/izin/$', self.admin_site.admin_view(self.option_namaizin), name='option_namaizin'),
			url(r'^option/kelompokizin/$', self.admin_site.admin_view(self.option_kelompokjenisizin), name='option_kelompokjenisizin'),
			url(r'^wizard/add/proses/siup/$', self.admin_site.admin_view(formulir_siup), name='izin_proses_siup'),
			url(r'^wizard/add/proses/reklame/$', self.admin_site.admin_view(formulir_reklame), name='izin_proses_reklame'),
			url(r'^wizard/add/proses/imb-reklame/$', self.admin_site.admin_view(formulir_imb_reklame), name='izin_proses_imb_reklame'),
			url(r'^wizard/add/proses/imb-umum/$', self.admin_site.admin_view(formulir_imb_umum), name='izin_proses_imb_umum'),
			url(r'^wizard/add/proses/imb-perumahan/$', self.admin_site.admin_view(formulir_imb_perumahan), name='izin_proses_imb_perumahan'),
			url(r'^wizard/add/proses/tdp-pt/$', self.admin_site.admin_view(formulir_tdp_pt), name='izin_proses_tdp_pt'),
			url(r'^wizard/add/proses/tdp-cv/$', self.admin_site.admin_view(formulir_tdp_cv), name='izin_proses_tdp_cv'),
			url(r'^wizard/add/proses/tdp-firma/$', self.admin_site.admin_view(formulir_tdp_firma), name='izin_proses_tdp_firma'),
			url(r'^wizard/add/proses/tdp-perorangan/$', self.admin_site.admin_view(formulir_tdp_perorangan), name='izin_proses_tdp_perorangan'),
			url(r'^wizard/add/proses/tdp-koperasi/$', self.admin_site.admin_view(formulir_tdp_koperasi), name='izin_proses_tdp_koperasi'),
			url(r'^wizard/add/proses/tdp-bul/$', self.admin_site.admin_view(formulir_tdp_bul), name='izin_proses_tdp_bul'),
			url(r'^wizard/add/proses/pemakaian-kekayaan-daerah/$', self.admin_site.admin_view(formulir_informasi_kekayaan_daerah), name='izin_proses_pemakaian_kekayaan_daerah'),
			url(r'^wizard/add/proses/izin-gangguan/$', self.admin_site.admin_view(formulir_izin_gangguan), name='izin_proses_gangguan'),
			url(r'^wizard/add/proses/izin-lokasi/$', self.admin_site.admin_view(formulir_izin_lokasi), name='izin_proses_lokasi'),
			url(r'^wizard/add/proses/ippt-rumah/$', self.admin_site.admin_view(formulir_ippt_rumah), name='izin_proses_ippt_rumah'),
			url(r'^wizard/add/proses/ippt-usaha/$', self.admin_site.admin_view(formulir_ippt_usaha), name='izin_proses_ippt_usaha'),
			url(r'^wizard/add/proses/penggilingan-padi-&-huller/$', self.admin_site.admin_view(formulir_detilhuller), name='izin_proses_huller'),
			url(r'^wizard/add/proses/tdup/$', self.admin_site.admin_view(formulir_tdup), name='izin_proses_tdup'),

			url(r'^pendaftaran/(?P<id_pengajuan_izin_>[0-9]+)/$', self.admin_site.admin_view(cetak), name='pendaftaran_selesai'),
			# url(r'^pendaftaran/(?P<id_pengajuan_izin_>[0-9]+)/cetak$', self.admin_site.admin_view(self.print_out_pendaftaran), name='print_out_pendaftaran'),
			url(r'^aksi/$', self.admin_site.admin_view(self.aksi_detil_siup), name='aksi_detil_siup'),
			url(r'^aksi-tolak/$', self.admin_site.admin_view(self.penolakanizin), name='penolakanizin'),
			url(r'^create-skizin/$', self.admin_site.admin_view(self.create_skizin), name='create_skizin'),
			url(r'^cetak-siup-asli/(?P<id_pengajuan_izin_>[0-9 A-Za-z_\-=]+)$', self.admin_site.admin_view(self.cetak_siup_asli), name='cetak_siup_asli'),
			# url(r'^verifikasi/$', self.admin_site.admin_view(self.verifikasi), name='verifikasi'),
			url(r'^verifikasi-operator/$', self.admin_site.admin_view(self.verifikasi_operator), name='verifikasi_operator'),
			url(r'^verifikasi-kabid/$', self.admin_site.admin_view(self.verifikasi_kabid), name='verifikasi_kabid'),
			url(r'^verifikasi-pembuat-surat/$', self.admin_site.admin_view(self.verifikasi_pembuat_surat), name='verifikasi_pembuat_surat'),
			url(r'^survey/$', self.admin_site.admin_view(self.survey), name='survey'),
			url(r'^semua-pengajuan/$', self.admin_site.admin_view(self.semua_pengajuan), name='semua_pengajuan'),
			url(r'^penomoran-skizin/$', self.admin_site.admin_view(self.penomoran_skizin), name='penomoran_skizin'),
			url(r'^stemple-skizin/$', self.admin_site.admin_view(self.stemple_izin), name='stemple_izin'),
			url(r'^kasir/$', self.admin_site.admin_view(self.kasir), name='kasir'),
			# url(r'^verifikasi-skizin/$', self.admin_site.admin_view(self.verifikasi_skizin), name='verifikasi_skizin'),
			url(r'^verifikasi-skizin-kabid/$', self.admin_site.admin_view(self.verifikasi_skizin_kabid), name='verifikasi_skizin_kabid'),
			url(r'^verifikasi-skizin-kadin/$', self.admin_site.admin_view(self.verifikasi_skizin_kadin), name='verifikasi_skizin_kadin'),
			url(r'^verifikasi-skizin-bupati/$', self.admin_site.admin_view(self.verifikasi_skizin_bupati), name='verifikasi_skizin_bupati'),
			url(r'^verifikasi-skizin-cetak/$', self.admin_site.admin_view(self.verifikasi_skizin_cetak), name='verifikasi_skizin_cetak'),
			url(r'^izin-terdaftar/$', self.admin_site.admin_view(self.izinterdaftar), name='izinterdaftar'),
			url(r'^total-pengajuan/$', self.admin_site.admin_view(self.total_izin), name='total_izin'),
			url(r'^wizard/iujk/$', self.admin_site.admin_view(IUJKWizard), name='izin_iujk'),

			)
		return my_urls + urls

	def suit_cell_attributes(self, obj, column):
		if column in ['button_cetak_pendaftaran', 'linkdetilizin', 'get_status_pengajuan']:
			return {'class': 'text-center'}
		else:
			return None

	def save_model(self, request, obj, form, change):
		# clean the nomor_identitas
		obj.create_by = request.user
		obj.save()

admin.site.register(PengajuanIzin, IzinAdmin)


