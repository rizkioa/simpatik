from django.contrib import admin
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist
from izin.models import PengajuanIzin, JenisIzin, KelompokJenisIzin, Syarat, DetilSIUP, SKIzin, Riwayat
from kepegawaian.models import Pegawai
from izin.controllers.siup import add_wizard_siup, formulir_siup, cetak
from izin.controllers.reklame import formulir_reklame
from izin.controllers.tdp import formulir_tdp_pt
from izin.controllers.iujk import IUJKWizard
from izin_forms import UploadBerkasPenolakanIzinForm, PemohonForm, PerusahaanForm
import json
import base64
from izin.utils import terbilang_, terbilang, formatrupiah
from django.db.models import Q

class IzinAdmin(admin.ModelAdmin):
	# list_display = ('get_no_pengajuan', 'get_tanggal_pengajuan', 'get_kelompok_jenis_izin', 'pemohon','jenis_permohonan', 'get_status_proses','status', 'button_cetak_pendaftaran')
	list_filter = ('kelompok_jenis_izin',)
	search_fields = ('no_izin', 'pemohon__nama_lengkap')

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

	def verifikasi(self, request, extra_context={}):
		self.request = request
		izin = KelompokJenisIzin.objects.all()
		extra_context.update({'izin': izin})
		return super(IzinAdmin, self).changelist_view(request, extra_context=extra_context)

	def verifikasi_skizin(self, request, extra_context={}):
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

	def get_list_display(self, request):
		func_view, func_view_args, func_view_kwargs = resolve(request.path)
		list_display = ('get_no_pengajuan', 'get_tanggal_pengajuan', 'get_kelompok_jenis_izin', 'pemohon','jenis_permohonan', 'get_status_proses','status', 'button_cetak_pendaftaran')
		if func_view.__name__ == 'izinterdaftar':
			list_display = ('get_no_pengajuan', 'no_izin', 'get_kelompok_jenis_izin', 'pemohon', 'jenis_permohonan', 'get_status_proses')
		# else:
			# list_display = ('get_no_pengajuan', 'get_tanggal_pengajuan', 'get_kelompok_jenis_izin', 'pemohon','jenis_permohonan', 'get_status_proses')
		return list_display

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
			pengajuan_ = qs.filter(~Q(status=11))
		elif func_view.__name__ == 'verifikasi':
			if request.user.groups.filter(name='Operator'):
				pengajuan_ = qs.filter(status=6)
			elif request.user.groups.filter(name='Kabid'):
				pengajuan_ = qs.filter(status=4)
			elif request.user.groups.filter(name='Pembuat Surat'):
				pengajuan_ = qs.filter(skizin__isnull=True, status=2)

		elif func_view.__name__ == 'verifikasi_skizin':
			id_pengajuan_list = []
			if request.user.groups.filter(name='Kabid'):
				id_list = SKIzin.objects.filter(status=6).values_list('pengajuan_izin_id', flat=True)
				id_pengajuan_list += id_list
				
			elif request.user.groups.filter(name='Kadin'):
				id_list = SKIzin.objects.filter(status=4).values_list('pengajuan_izin_id', flat=True)
				id_pengajuan_list += id_list
			
			if request.user.groups.filter(name='Cetak'):
				id_list = SKIzin.objects.filter(status=10).values_list('pengajuan_izin_id', flat=True)
				id_pengajuan_list += id_list
			
			# print id_pengajuan_list
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
		return pengajuan_

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
		return obj.created_at
	get_tanggal_pengajuan.short_description = "Tgl. Pengajuan"

	def get_no_pengajuan(self, obj):
		no_pengajuan = mark_safe("""
			<a href="%s" target="_blank"> %s </a>
			""" % ("#", obj.no_pengajuan ))
		split_ = obj.no_pengajuan.split('/')
		# print split_
		no_pengajuan = mark_safe("""
				<span>%s</span>
				""" % ( obj.no_pengajuan ))
		if split_[0] == 'SIUP':
			# if request.user.is_superuser:
			# 	no_pengajuan = mark_safe("""
			# 	<a href="%s" target="_blank"> %s </a>
			# 	""" % (reverse('admin:izin_detilsiup_change', args=(obj.id,)), obj.no_pengajuan ))
			# else:
			no_pengajuan
		elif split_[0] == 'Reklame':
			# if request.user.is_superuser:
			# 	no_pengajuan = mark_safe("""
			# 	<a href="%s" target="_blank"> %s </a>
			# 	""" % (reverse('admin:izin_detilreklame_change', args=(obj.id,)), obj.no_pengajuan ))
			# else:
			no_pengajuan
		elif split_[0] == 'TDP':
			# if request.user.is_superuser:
			# 	no_pengajuan = mark_safe("""
			# 	<a href="%s" target="_blank"> %s </a>
			# 	""" % (reverse('admin:izin_detiltdp_change', args=(obj.id,)), obj.no_pengajuan ))
			# else:
			no_pengajuan
		return no_pengajuan
	get_no_pengajuan.short_description = "No. Pengajuan"

	def button_cetak_pendaftaran(self, obj):
		link_ = '#'
		jenis_izin_ = obj.kelompok_jenis_izin.kode
		# print jenis_izin_
		if jenis_izin_ == "503.08/":
			link_ = reverse('admin:view_pengajuan_siup', kwargs={'id_pengajuan_izin_': obj.id})
		elif jenis_izin_ == "503.03.01/" or jenis_izin_ == "503.03.02/":
			link_ = reverse('admin:view_pengajuan_reklame', kwargs={'id_pengajuan_izin_': obj.id})
		elif jenis_izin_ == "IUJK":
			link_ = reverse('admin:view_pengajuan_iujk', kwargs={'id_pengajuan_izin_': obj.id})
		btn = mark_safe("""
				<a href="%s" target="_blank" class="btn btn-darkgray btn-rounded-20 btn-ef btn-ef-5 btn-ef-5a mb-10"><i class="fa fa-cog"></i> <span>Proses</span> </a>
				""" % link_ )
		if self.request.user.groups.filter(name='Operator'):
			if obj.status == 4:
				btn = mark_safe("""<span class="label bg-primary">Verifikasi Kabid</span>""")
			elif obj.status == 2 and not obj.skizin_set.all().exists():
				btn = mark_safe("""<span class="label bg-slategray">Pembuatan SKIzin</span>""")
			elif obj.skizin_set.filter(status=6):
				btn = mark_safe("""<span class="label bg-info">Verifikasi SK Kabid</span>""")
			elif obj.skizin_set.filter(status=4):
				btn = mark_safe("""<span class="label bg-warning">Verifikasi SK Kadin</span>""")
			elif obj.skizin_set.filter(status=9):
				btn = mark_safe("""<span class="label bg-cyan">Penomoran</span>""")
			elif obj.skizin_set.filter(status=10):
				btn = mark_safe("""<span class="label bg-green">Pencetakan</span>""")
			elif obj.skizin_set.filter(status=2):
				btn = mark_safe("""<span class="label bg-drank">Penstempelan</span>""")
			elif obj.status == 1:
				btn = mark_safe("""<span class="label bg-success">SELESAI</span>""")
			elif obj.status == 7:
				btn = mark_safe("""<span class="label bg-danger">DITOLAK</span>""")
			else:
				btn = btn
		elif self.request.user.groups.filter(name='Kabid'):
			if obj.status == 6:
				btn = mark_safe("""<span class="label bg-dutch">Menunggu Operator</span>""")
			elif obj.status == 2 and not obj.skizin_set.all().exists():
				btn = mark_safe("""<span class="label bg-slategray">Pembuatan SKIzin</span>""")
			# elif obj.skizin_set.filter(status=6):
			# 	btn = mark_safe("""<span class="label bg-info">Verifikasi SK Kabid</span>""")
			elif obj.skizin_set.filter(status=4):
				btn = mark_safe("""<span class="label bg-warning">Verifikasi SK Kadin</span>""")
			elif obj.skizin_set.filter(status=9):
				btn = mark_safe("""<span class="label bg-cyan">Penomoran</span>""")
			elif obj.skizin_set.filter(status=10):
				btn = mark_safe("""<span class="label bg-green">Pencetakan</span>""")
			elif obj.skizin_set.filter(status=2):
				btn = mark_safe("""<span class="label bg-drank">Penstempelan</span>""")
			elif obj.status == 1:
				btn = mark_safe("""<span class="label bg-success">SELESAI</span>""")
			elif obj.status == 7:
				btn = mark_safe("""<span class="label bg-danger">DITOLAK</span>""")
			else:
				btn = btn
		elif self.request.user.groups.filter(name='Kadin'): 
			if obj.status == 6:
				btn = mark_safe("""<span class="label bg-dutch">Menunggu Operator</span>""")
			elif obj.status == 4:
				btn = mark_safe("""<span class="label bg-primary">Menunggu Kabid</span>""")
			elif obj.status == 2 and not obj.skizin_set.all().exists():
				btn = mark_safe("""<span class="label bg-slategray">Pembuatan SKIzin</span>""")
			elif obj.skizin_set.filter(status=6):
				btn = mark_safe("""<span class="label bg-info">Menunggu SK Kabid</span>""")
			elif obj.skizin_set.filter(status=9):
				btn = mark_safe("""<span class="label bg-cyan">Penomoran</span>""")
			elif obj.skizin_set.filter(status=10):
				btn = mark_safe("""<span class="label bg-green">Pencetakan</span>""")
			elif obj.skizin_set.filter(status=2):
				btn = mark_safe("""<span class="label bg-drank">Penstempelan</span>""")
			elif obj.status == 1:
				btn = mark_safe("""<span class="label bg-success">SELESAI</span>""")
			elif obj.status == 7:
				btn = mark_safe("""<span class="label bg-danger">DITOLAK</span>""")
			else:
				btn = btn
		elif self.request.user.groups.filter(name='Pembuat Surat'):
			if obj.status == 6:
				btn = mark_safe("""<span class="label bg-dutch">Menunggu Operator</span>""")
			elif obj.status == 4:
				btn = mark_safe("""<span class="label bg-primary">Menunggu Kabid</span>""")
			elif obj.skizin_set.filter(status=6):
				btn = mark_safe("""<span class="label bg-info">Verifikasi SK Kabid</span>""")
			elif obj.skizin_set.filter(status=4):
				btn = mark_safe("""<span class="label bg-warning">Verifikasi SK Kadin</span>""")
			elif obj.skizin_set.filter(status=9):
				btn = mark_safe("""<span class="label bg-cyan">Penomoran</span>""")
			# elif obj.skizin_set.filter(status=10):
				# btn = mark_safe("""<span class="label bg-green">Pencetakan</span>""")
			elif obj.skizin_set.filter(status=2):
				btn = mark_safe("""<span class="label bg-drank">Penstempelan</span>""")
			elif obj.status == 1:
				btn = mark_safe("""<span class="label bg-success">SELESAI</span>""")
			elif obj.status == 7:
				btn = mark_safe("""<span class="label bg-danger">DITOLAK</span>""")
			else:
				btn = btn
		elif self.request.user.groups.filter(name='Penomoran'):
			if obj.status == 6:
				btn = mark_safe("""<span class="label bg-dutch">Menunggu Operator</span>""")
			elif obj.status == 4:
				btn = mark_safe("""<span class="label bg-primary">Menunggu Kabid</span>""")
			elif obj.status == 2 and not obj.skizin_set.all().exists():
				btn = mark_safe("""<span class="label bg-slategray">Pembuatan SKIzin</span>""")
			elif obj.skizin_set.filter(status=6):
				btn = mark_safe("""<span class="label bg-info">Menunggu SK Kabid</span>""")
			elif obj.skizin_set.filter(status=4):
				btn = mark_safe("""<span class="label bg-warning">Menunggu SK Kadin</span>""")
			elif obj.skizin_set.filter(status=10):
				btn = mark_safe("""<span class="label bg-green">Pencetakan</span>""")
			# elif obj.skizin_set.filter(status=2):
				# btn = mark_safe("""<span class="label bg-drank">Penstempelan</span>""")
			elif obj.status == 1:
				btn = mark_safe("""<span class="label bg-success">SELESAI</span>""")
			elif obj.status == 7:
				btn = mark_safe("""<span class="label bg-danger">DITOLAK</span>""")
			else:
				btn = btn
		elif self.request.user.groups.filter(name='Cetak'):
			if obj.status == 6:
				btn = mark_safe("""<span class="label bg-dutch">Menunggu Operator</span>""")
			elif obj.status == 4:
				btn = mark_safe("""<span class="label bg-primary">Menunggu Kabid</span>""")
			# elif obj.status == 2 and not obj.skizin_set.all().exists():
			# 	btn = mark_safe("""<span class="label bg-slategray">Pembuatan SKIzin</span>""")
			elif obj.skizin_set.filter(status=6):
				btn = mark_safe("""<span class="label bg-info">Menunggu SK Kabid</span>""")
			elif obj.skizin_set.filter(status=4):
				btn = mark_safe("""<span class="label bg-warning">Menunggu SK Kadin</span>""")
			elif obj.skizin_set.filter(status=9):
				btn = mark_safe("""<span class="label bg-cyan">Menunggu Penomoran</span>""")
			elif obj.skizin_set.filter(status=2):
				btn = mark_safe("""<span class="label bg-drank">Penstempelan</span>""")
			elif obj.status == 1:
				btn = mark_safe("""<span class="label bg-success">SELESAI</span>""")
			elif obj.status == 7:
				btn = mark_safe("""<span class="label bg-danger">DITOLAK</span>""")
			else:
				btn = btn
		elif self.request.user.groups.filter(name='Selesai'):
			if obj.status == 6:
				btn = mark_safe("""<span class="label bg-dutch">Menunggu Operator</span>""")
			elif obj.status == 4:
				btn = mark_safe("""<span class="label bg-primary">Menunggu Kabid</span>""")
			elif obj.status == 2 and not obj.skizin_set.all().exists():
				btn = mark_safe("""<span class="label bg-slategray">Pembuatan SKIzin</span>""")
			elif obj.skizin_set.filter(status=6):
				btn = mark_safe("""<span class="label bg-info">Menunggu SK Kabid</span>""")
			elif obj.skizin_set.filter(status=4):
				btn = mark_safe("""<span class="label bg-warning">Menunggu SK Kadin</span>""")
			# elif obj.skizin_set.filter(status=9):
				# btn = mark_safe("""<span class="label bg-cyan">Menunggu Penomoran</span>""")
			elif obj.skizin_set.filter(status=10):
				btn = mark_safe("""<span class="label bg-green">Menunggu Pencetakan</span>""")
			elif obj.status == 1:
				btn = mark_safe("""<span class="label bg-success">SELESAI</span>""")
			elif obj.status == 7:
				btn = mark_safe("""<span class="label bg-danger">DITOLAK</span>""")
			else:
				btn = btn
		# elif obj.status == 1:
		# 	btn = mark_safe("""<span class="label label-default">SELESAI</span>""")
		# elif obj.status == 7:
		# 	btn = mark_safe("""<span class="label label-danger">DITOLAK</span>""")
		else:
			btn = btn
				# reverse('admin:print_out_pendaftaran', kwargs={'id_pengajuan_izin_': obj.id})
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

	def print_out_pendaftaran(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Pengajuan Selesai'})
			pengajuan_ = PengajuanIzin.objects.get(id=id_pengajuan_izin_)
			extra_context.update({'pemohon': pengajuan_.pemohon})
			nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
			extra_context.update({'nomor_identitas': nomor_identitas_ })
			extra_context.update({'jenis_pemohon': pengajuan_.pemohon.jenis_pemohon})
			alamat_ = ""
			if pengajuan_.pemohon.desa:
				alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
			extra_context.update({'alamat_pemohon': alamat_})
			extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})

			syarat_ = Syarat.objects.filter(jenis_izin__id=pengajuan_.id)
			extra_context.update({'syarat': syarat_})

		# template = loader.get_template("admin/izin/izin/add_wizard.html")
		template = loader.get_template("admin/izin/izin/cetak_bukti_pendaftaran.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_siup_asli(self, request, id_pengajuan_izin_):
		extra_context = {}
		# id_pengajuan_izin_ = base64.b64decode(id_pengajuan_izin_)
		if id_pengajuan_izin_:
			pengajuan_ = DetilSIUP.objects.get(id=id_pengajuan_izin_)
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+",f"+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_perusahaan': alamat_perusahaan_})
				extra_context.update({'perusahaan': pengajuan_.perusahaan })
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'pengajuan': pengajuan_ })
			extra_context.update({'foto': pengajuan_.pemohon.berkas_foto.all().last()})
			kelembagaan = pengajuan_.kelembagaan.kelembagaan.upper()
			extra_context.update({'kelembagaan': kelembagaan })
			if pengajuan_.kekayaan_bersih:
				terbilang_ = terbilang(pengajuan_.kekayaan_bersih)
				extra_context.update({'terbilang': str(terbilang_) })
				extra_context.update({ 'kekayaan_bersih': formatrupiah(pengajuan_.kekayaan_bersih) })
			# try:
			skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
			if skizin_:
				extra_context.update({'skizin': skizin_ })
				extra_context.update({'skizin_status': skizin_.status })
			# except ObjectDoesNotExist:
			# 	pass
			# try:
			kepala_ =  Pegawai.objects.filter(jabatan__nama_jabatan="Kepala Dinas").last()
			if kepala_:
				extra_context.update({'kepala_dinas': kepala_ })
				extra_context.update({'nip_kepala_dinas': kepala_.nomoridentitaspengguna_set.last() })

			# except ObjectDoesNotExist:
			# 	pass
			# print pengajuan_.kbli.nama_kbli.all()
			# print pengajuan_.produk_utama
		template = loader.get_template("front-end/include/formulir_siup/cetak_siup_asli.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def total_izin(self, request):
		# pengajuan_ = PengajuanIzin.objects.filter(status=6).count()
		pengajuan_ = ""
		if request.user.groups.filter(name='Operator'):
			pengajuan_ = PengajuanIzin.objects.filter(status=6).count()
		elif request.user.groups.filter(name='Kabid'):
			pengajuan_ = PengajuanIzin.objects.filter(status=4).count()
		elif request.user.groups.filter(name='Pembuat Surat'):
			pengajuan_ = PengajuanIzin.objects.filter(skizin__isnull=True, status=2).count()
		elif request.user.groups.filter(name='Penomoran'):
			pengajuan_ = len(SKIzin.objects.filter(status=9).values('pengajuan_izin_id'))
		return HttpResponse(json.dumps(pengajuan_))

	def total_skizin(self, request):
		pengajuan_ = ""
		if request.user.groups.filter(name='Kabid'):
			pengajuan_ = len(SKIzin.objects.filter(status=6).values('pengajuan_izin_id'))
		elif request.user.groups.filter(name='Kadin'):
			pengajuan_ = len(SKIzin.objects.filter(status=4).values('pengajuan_izin_id'))
		elif request.user.groups.filter(name='Cetak'):
			pengajuan_ = len(SKIzin.objects.filter(status=10).values('pengajuan_izin_id'))
		elif request.user.groups.filter(name='Selesai'):
			pengajuan_ = len(SKIzin.objects.filter(status=2).values('pengajuan_izin_id'))
		return HttpResponse(json.dumps(pengajuan_))

	def notification(self, request):
		data = ""
		if request.user.groups.filter(name='Operator'):
			pengajuan_ = len(PengajuanIzin.objects.filter(status=6))
			pesan = "Ada "+str(pengajuan_)+" pengajuan baru."
			url = "/admin/izin/pengajuanizin/verifikasi/"
			data = {'success': True, 'pesan': pesan, 'total': pengajuan_, 'url': url }
		elif request.user.groups.filter(name='Kabid'):
			pengajuan_ = len(PengajuanIzin.objects.filter(status=4))
			pesan =  "Ada "+str(pengajuan_)+" pengajuan baru."
			url = "/admin/izin/pengajuanizin/verifikasi/"
			data = {'success': True, 'pesan': pesan, 'total': pengajuan_, 'url': url }
		elif request.user.groups.filter(name='Pembuat Surat'):
			pengajuan_ = len(PengajuanIzin.objects.filter(skizin__isnull=True, status=2))
			pesan =  "Ada "+str(pengajuan_)+" SK Izin yang harus diverifikasi."
			url = "/admin/izin/pengajuanizin/verifikasi/"
			data = {'success': True, 'pesan': pesan, 'total': pengajuan_, 'url': url }
		elif request.user.groups.filter(name='Kabid'):
			pengajuan_ = len(SKIzin.objects.filter(status=6).values('pengajuan_izin_id'))
			pesan = "Ada "+str(pengajuan_)+" SK Izin yang harus diverifikasi."
			url = "/admin/izin/pengajuanizin/verifikasi-skizin/"
			data = {'success': True, 'pesan': pesan, 'total': pengajuan_, 'url': url }
		elif request.user.groups.filter(name='Kadin'):
			pengajuan_ = len(SKIzin.objects.filter(status=4).values('pengajuan_izin_id'))
			pesan =  "Ada "+str(pengajuan_)+" SK Izin yang harus diverifikasi."
			url = "/admin/izin/pengajuanizin/verifikasi-skizin/"
			data = {'success': True, 'pesan': pesan, 'total': pengajuan_, 'url': url }
		elif request.user.groups.filter(name='Penomoran'):
			pengajuan_ = len(SKIzin.objects.filter(status=9).values('pengajuan_izin_id'))
			pesan =  "Ada "+str(pengajuan_)+" SK Izin yang harus diverifikasi."
			url = "/admin/izin/pengajuanizin/verifikasi-skizin/"
			data = {'success': True, 'pesan': pesan, 'total': pengajuan_, 'url': url }
		elif request.user.groups.filter(name='Cetak'):
			pengajuan_ = len(SKIzin.objects.filter(status=10).values('pengajuan_izin_id'))
			pesan =  "Ada "+str(pengajuan_)+" SK Izin yang harus diverifikasi."
			url = "/admin/izin/pengajuanizin/verifikasi-skizin/"
			data = {'success': True, 'pesan': pesan, 'total': pengajuan_, 'url': url }
		elif request.user.groups.filter(name='Selesai'):
			pengajuan_ = len(SKIzin.objects.filter(status=2).values('pengajuan_izin_id'))
			pesan =  "Ada "+str(pengajuan_)+" SK Izin yang harus diverifikasi."
			url = "/admin/izin/pengajuanizin/verifikasi-skizin/"
			data = {'success': True, 'pesan': pesan, 'total': pengajuan_, 'url': url }
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
			skizin = SKIzin(
				pengajuan_izin_id = id_detil_siup,
				created_by_id = request.user.id,
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
		# print request.POST.get('aksi')
		# print id_pengajuan_izin
		try:
			obj = PengajuanIzin.objects.get(id=id_pengajuan_izin)
			# and request.user.has_perm('izin.change_detilsiup') or request.user.is_superuser or request.user.groups.filter(name='Admin Sistem')
			if request.POST.get('aksi', None):
				if request.POST.get('aksi') == '_submit_operator':
					# print "operator"
					obj.status = 4
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
					obj.save()
					riwayat_ = Riwayat(
						pengajuan_izin_id = id_pengajuan_izin,
						created_by_id = request.user.id,
						keterangan = "Kabid Verified (Pengajuan)"
					)
					riwayat_.save()
					response = {
						"success": True,
						"pesan": "Izin berhasil di verifikasi.",
						"redirect": '',
					}
				elif request.POST.get('aksi') == '_submit_edit_skizin':
					try:
						detilsiup = DetilSIUP.objects.get(id=id_pengajuan_izin)
						print request.POST.get('produk_utama')
						detilsiup.produk_utama = request.POST.get('produk_utama')
						detilsiup.save()
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
				else:
					response = {
						"success": False,
						"pesan": "Anda tidak memiliki hak akses untuk memverifikasi izin.",
						"redirect": '',
					}

				try:
					obj_skizin = SKIzin.objects.get(pengajuan_izin_id=id_pengajuan_izin)
					if request.POST.get('aksi') == '_submit_skizin_kabid':
						obj_skizin.status = 4
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
						obj_skizin.status = 9
						obj_skizin.save()
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
					elif request.POST.get('aksi') == '_submit_penomoran':
						obj_skizin.status = 10
						obj_skizin.save()
						kode_izin_ =  obj.kelompok_jenis_izin.kode
						nomor_urut_ = request.POST.get('kode_izin')
						tahun_ = request.POST.get('tahun')
						obj.no_izin = kode_izin_+nomor_urut_+"/418.71/"+tahun_
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
					elif request.POST.get('aksi') == '_submit_cetak_izin':
						obj_skizin.status = 2
						obj_skizin.save()
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
					else:
						response = {
							"success": False,
							"pesan": "Anda tidak memiliki hak akses untuk memverifikasi izin.",
							"redirect": '',
						}
				except ObjectDoesNotExist:
					pass
			else:
				response = {
					"success": False,
					"pesan": "Anda tidak memiliki hak akses untuk memverifikasi izin.",
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
		id_detil_siup = request.POST.get('id_pengajuan')
		try:
			obj = DetilSIUP.objects.get(id=id_detil_siup)
			if request.user.has_perm('izin.change_detilsiup') or request.user.is_superuser or request.user.groups.filter(name='Admin Sistem'):
				form = UploadBerkasPenolakanIzinForm(request.POST, request.FILES)
				if request.method == "POST":
					if request.FILES.get('berkas'):
						if form.is_valid():
							berkas = form.save(commit=False)
							berkas.nama_berkas = "Berkas Penolakan Izin"
							berkas.created_by_id = request.user.id
							berkas.save()
							obj.status = 7
							obj.rejected_by_id = request.user.id
							obj.save()
							riwayat_ = Riwayat(
										alasan = request.POST.get('alasan', None),
										pengajuan_izin_id = id_detil_siup,
										created_by_id = request.user.id,
										keterangan = "Tolak (Izin)."
									)
							riwayat_.berkas_id = berkas.id
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
							data = form.errors.as_json()
							response = HttpResponse(data)
					else:
						response = {
							"success": False,
							"pesan": "Berkas Kosong",
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
			url(r'^wizard/add/proses/tdp-pt/$', self.admin_site.admin_view(formulir_tdp_pt), name='izin_proses_tdp_pt'),
			url(r'^pendaftaran/(?P<id_pengajuan_izin_>[0-9]+)/$', self.admin_site.admin_view(cetak), name='pendaftaran_selesai'),
			url(r'^pendaftaran/(?P<id_pengajuan_izin_>[0-9]+)/cetak$', self.admin_site.admin_view(self.print_out_pendaftaran), name='print_out_pendaftaran'),
			url(r'^aksi/$', self.admin_site.admin_view(self.aksi_detil_siup), name='aksi_detil_siup'),
			url(r'^aksi-tolak/$', self.admin_site.admin_view(self.penolakanizin), name='penolakanizin'),
			url(r'^create-skizin/$', self.admin_site.admin_view(self.create_skizin), name='create_skizin'),
			url(r'^cetak-siup-asli/(?P<id_pengajuan_izin_>[0-9 A-Za-z_\-=]+)$', self.admin_site.admin_view(self.cetak_siup_asli), name='cetak_siup_asli'),
			url(r'^verifikasi/$', self.admin_site.admin_view(self.verifikasi), name='verifikasi'),
			url(r'^semua-pengajuan/$', self.admin_site.admin_view(self.semua_pengajuan), name='semua_pengajuan'),
			url(r'^penomoran-skizin/$', self.admin_site.admin_view(self.penomoran_skizin), name='penomoran_skizin'),
			url(r'^stemple-skizin/$', self.admin_site.admin_view(self.stemple_izin), name='stemple_izin'),
			url(r'^verifikasi-skizin/$', self.admin_site.admin_view(self.verifikasi_skizin), name='verifikasi_skizin'),
			url(r'^izin-terdaftar/$', self.admin_site.admin_view(self.izinterdaftar), name='izinterdaftar'),
			url(r'^total-pengajuan/$', self.admin_site.admin_view(self.total_izin), name='total_izin'),
			url(r'^total-skizin/$', self.admin_site.admin_view(self.total_skizin), name='total_skizin'),
			url(r'^notification/$', self.admin_site.admin_view(self.notification), name='notification'),
			url(r'^wizard/iujk/$', self.admin_site.admin_view(IUJKWizard), name='izin_iujk'),

			)
		return my_urls + urls

	def suit_cell_attributes(self, obj, column):
		if column in ['button_cetak_pendaftaran']:
			return {'class': 'text-center'}
		else:
			return None

	def save_model(self, request, obj, form, change):
		# clean the nomor_identitas
		obj.create_by = request.user
		obj.save()


admin.site.register(PengajuanIzin, IzinAdmin)
