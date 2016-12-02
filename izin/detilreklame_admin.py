from django.contrib import admin
from izin.models import DetilReklame, Syarat, SKIzin, Riwayat
from kepegawaian.models import Pegawai
from accounts.models import NomorIdentitasPengguna
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
from django.http import HttpResponse
import base64
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, resolve
import datetime

class DetilReklameAdmin(admin.ModelAdmin):
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
		if split_[0] == 'Reklame':
			no_pengajuan = mark_safe("""
				<a href="%s" target="_blank"> %s </a>
				""" % (reverse('admin:izin_detilreklame_change', args=(obj.id,)), obj.no_pengajuan ))
		return no_pengajuan
	get_no_pengajuan.short_description = "No. Pengajuan"

	def view_pengajuan_reklame(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			pengajuan_ = DetilReklame.objects.get(id=id_pengajuan_izin_)
			
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
				nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all().last()
				extra_context.update({'nomor_identitas': nomor_identitas_ })
				try:
					ktp_ = NomorIdentitasPengguna.objects.get(user_id=pengajuan_.pemohon.id)
					extra_context.update({'cookie_file_ktp': ktp_.berkas })
				except ObjectDoesNotExist:
					pass
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_perusahaan': alamat_perusahaan_ })
				extra_context.update({'perusahaan': pengajuan_.perusahaan})

				legalitas_pendirian = pengajuan_.perusahaan.legalitas_set.filter(berkas__keterangan="akta pendirian").last()
				legalitas_perubahan = pengajuan_.perusahaan.legalitas_set.filter(berkas__keterangan="akta perubahan").last()
				extra_context.update({ 'legalitas_pendirian': legalitas_pendirian })
				extra_context.update({ 'legalitas_perubahan': legalitas_perubahan })

			# extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})
			
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})
			extra_context.update({'status': pengajuan_.status})
			extra_context.update({'pengajuan': pengajuan_})
			encode_pengajuan_id = base64.b64encode(str(pengajuan_.id))
			extra_context.update({'pengajuan_id': encode_pengajuan_id})
			#+++++++++++++ page logout ++++++++++
			extra_context.update({'has_permission': True })
			#+++++++++++++ end page logout ++++++++++
			if pengajuan_.tanggal_mulai and pengajuan_.tanggal_akhir:
				tanggal_mulai = pengajuan_.tanggal_mulai
				tanggal_akhir = pengajuan_.tanggal_akhir

				jumlah_lama =  tanggal_akhir-tanggal_mulai
				extra_context.update({'jumlah_lama': jumlah_lama})

			# lama_pemasangan = pengajuan_.tanggal_akhir-pengajuan_.tanggal_mulai
			# print lama_pemasangan
			banyak = len(DetilReklame.objects.all())
			extra_context.update({'banyak': banyak})
			syarat_ = Syarat.objects.filter(jenis_izin__jenis_izin__kode="reklame")
			extra_context.update({'syarat': syarat_})
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
		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_reklame.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_reklame_asli(self, request, id_pengajuan_izin_):
		extra_context = {}
		id_pengajuan_izin_ = base64.b64decode(id_pengajuan_izin_)
		print id_pengajuan_izin_
		if id_pengajuan_izin_:
			pengajuan_ = DetilReklame.objects.get(id=id_pengajuan_izin_)
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_perusahaan': alamat_perusahaan_})
				extra_context.update({'perusahaan': pengajuan_.perusahaan })
			nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
			extra_context.update({'nomor_identitas': nomor_identitas_ })
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'pengajuan': pengajuan_ })
			extra_context.update({'foto': pengajuan_.pemohon.berkas_foto.all().last()})
			if pengajuan_.tanggal_mulai and pengajuan_.tanggal_akhir:
				tanggal_mulai = pengajuan_.tanggal_mulai
				tanggal_akhir = pengajuan_.tanggal_akhir

				jumlah_lama =  tanggal_akhir-tanggal_mulai
				extra_context.update({'jumlah_lama': jumlah_lama})
			try:
				skizin_ = SKIzin.objects.get(pengajuan_izin_id = id_pengajuan_izin_ )
				if skizin_:
					extra_context.update({'skizin': skizin_ })
					extra_context.update({'skizin_status': skizin_.status })
			except ObjectDoesNotExist:
				pass
			try:
				kepala_ =  Pegawai.objects.get(jabatan__nama_jabatan="Kepala Dinas")
				if kepala_:
					extra_context.update({'nama_kepala_dinas': kepala_.nama_lengkap })
					extra_context.update({'nip_kepala_dinas': kepala_.nomoridentitaspengguna_set.last() })

			except ObjectDoesNotExist:
				pass
			# print pengajuan_.kbli.nama_kbli.all()
			# print pengajuan_.produk_utama
		template = loader.get_template("front-end/include/formulir_reklame/cetak_reklame_asli.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_bukti_admin_reklame(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			pengajuan_ = DetilReklame.objects.get(id=id_pengajuan_izin_)
			extra_context.update({'pengajuan': pengajuan_ })
		template = loader.get_template("front-end/include/formulir_reklame/cetak_bukti_pendaftaran_admin.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilReklameAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^cetak-reklame-asli/(?P<id_pengajuan_izin_>[0-9 A-Za-z_\-=]+)$', self.admin_site.admin_view(self.cetak_reklame_asli), name='cetak_reklame_asli'),
			url(r'^view-pengajuan-reklame/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_reklame), name='view_pengajuan_reklame'),
			url(r'^cetak-bukti-pendaftaran-admin/(?P<id_pengajuan_izin_>[0-9]+)/$', self.admin_site.admin_view(self.cetak_bukti_admin_reklame), name='cetak_bukti_admin_reklame'),
			)
		return my_urls + urls

admin.site.register(DetilReklame, DetilReklameAdmin)