from django.contrib import admin
from django.core.urlresolvers import reverse, resolve
from izin.models import PengajuanIzin, DetilSIUP, DetilReklame, Pemohon, Syarat, SKIzin, Riwayat, JenisIzin
from perusahaan.models import Perusahaan, KBLI, ProdukUtama
from django.utils.safestring import mark_safe
from django.http import HttpResponse
import json
from django.db.models import Q
from datetime import date
import base64
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
from accounts.models import NomorIdentitasPengguna
from izin.utils import formatrupiah

class DetilSIUPAdmin(admin.ModelAdmin):
	list_display = ('get_no_pengajuan', 'pemohon', 'get_kelompok_jenis_izin','jenis_permohonan', 'status')
	search_fields = ('no_izin', 'pemohon__nama_lengkap')
	# fieldsets = [
	# 	('Detil SIUP',	{'fields':['pemohon', 'get_no_pengajuan']}),
	# ]
	# 
	# def get_fieldsets(self, request, obj = None):
	# 	if request.user.is_superuser:
	# 		add_fieldsets = (
	# 			(None, {
	# 				'classes': ('wide',),
	# 				'fields': ('get_no_pengajuan', 'get_kelompok_jenis_izin')
	# 				})
	# 			)

	def get_kelompok_jenis_izin(self, obj):
		return obj.kelompok_jenis_izin
	get_kelompok_jenis_izin.short_description = "Izin Pengajuan"

	def get_no_pengajuan(self, obj):
		no_pengajuan = mark_safe("""
			<a href="%s" > %s </a>
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
		fields_edit = ('pemohon', 'kelompok_jenis_izin', 'jenis_permohonan', 'nama_kuasa', 'no_identitas_kuasa', 'telephone_kuasa', 'berkas_tambahan', 'perusahaan', 'berkas_foto', 'berkas_npwp_pemohon', 'berkas_npwp_perusahaan', 'legalitas', 'kbli', 'kelembagaan', 'produk_utama', 'bentuk_kegiatan_usaha', 'jenis_penanaman_modal', 'kekayaan_bersih', 'total_nilai_saham', 'presentase_saham_nasional', 'presentase_saham_asing')
		if obj:
			if request.user.is_superuser:
				add_fieldsets = (
					# ('Pemohon', {
					# 	'classes': ('wide',),
					# 	'fields': ('pemohon',),
					# 	}),
					('Detil SIUP', {
						'classes': ('wide',),
						'fields': fields+fields_admin
						}),
				)
			elif request.user.groups.filter(name='Operator') or request.user.groups.filter(name='Kabid') or request.user.groups.filter(name='Kadin') or request.user.groups.filter(name='Pembuat Surat') or request.user.groups.filter(name='Penomoran'):
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': fields_edit
						}),
				)
			else:
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': fields_edit+('no_pengajuan',)
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
		pengajuan_proses = len(PengajuanIzin.objects.filter(~Q(status=1) and ~Q(status=6)))
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

	def view_pengajuan_siup(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			pengajuan_ = DetilSIUP.objects.get(id=id_pengajuan_izin_)
			
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
				nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
				ktp_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(jenis_identitas_id=1).last()
				paspor_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(jenis_identitas_id=2).last()
				extra_context.update({'ktp': ktp_ })
				extra_context.update({'paspor': paspor_ })
				extra_context.update({'nomor_identitas': nomor_identitas_ })
				try:
					ktp_ = NomorIdentitasPengguna.objects.get(user_id=pengajuan_.pemohon.id, jenis_identitas__id=1)
					extra_context.update({'cookie_file_ktp': ktp_.berkas })
				except ObjectDoesNotExist:
					pass
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_perusahaan': alamat_perusahaan_ })
				extra_context.update({'perusahaan': pengajuan_.perusahaan})
				legalitas_pendirian = pengajuan_.legalitas.filter(~Q(jenis_legalitas_id=2)).last()
				legalitas_perubahan = pengajuan_.legalitas.filter(jenis_legalitas_id=2).last()
				extra_context.update({ 'legalitas_pendirian': legalitas_pendirian })
				extra_context.update({ 'legalitas_perubahan': legalitas_perubahan })

			# extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})
			
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})
			extra_context.update({'status': pengajuan_.status})
			extra_context.update({'pengajuan': pengajuan_})
			# encode_pengajuan_id = base64.b64encode(str(pengajuan_.id))
			# extra_context.update({'pengajuan_id': encode_pengajuan_id})
			#+++++++++++++ page logout ++++++++++
			extra_context.update({'has_permission': True })
			#+++++++++++++ end page logout ++++++++++
			banyak = len(DetilSIUP.objects.all())
			extra_context.update({'banyak': banyak})
			syarat_ = Syarat.objects.filter(jenis_izin__jenis_izin__kode="SIUP")
			extra_context.update({'syarat': syarat_})
			kekayaan_bersih = int(pengajuan_.kekayaan_bersih)
			extra_context.update({'kekayaan_bersih': formatrupiah(kekayaan_bersih)})
			total_nilai_saham = int(pengajuan_.total_nilai_saham)
			extra_context.update({'total_nilai_saham': formatrupiah(total_nilai_saham)})

			try:
				skizin_ = SKIzin.objects.get(pengajuan_izin_id = id_pengajuan_izin_ )
				if skizin_:
					extra_context.update({'skizin': skizin_ })
					extra_context.update({'skizin_status': skizin_.status })
			except ObjectDoesNotExist:
				pass
			try:
				riwayat_ = Riwayat.objects.filter(pengajuan_izin_id = id_pengajuan_izin_).order_by('created_at')
				if riwayat_:
					extra_context.update({'riwayat': riwayat_ })
			except ObjectDoesNotExist:
				pass
		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_siup.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilSIUPAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^ajax-dashboard/$', self.admin_site.admin_view(self.ajax_dashboard), name='ajax_dashboard'),
			url(r'^ajax-load-pengajuan-siup/(?P<id_pengajuan_>[0-9]+)/$', self.admin_site.admin_view(self.ajax_load_pengajuan_siup), name='ajax_load_pengajuan_siup'),
			url(r'^view-pengajuan-siup/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_siup), name='view_pengajuan_siup'),
			)
		return my_urls + urls

admin.site.register(DetilSIUP, DetilSIUPAdmin)