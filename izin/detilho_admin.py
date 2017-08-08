import base64, datetime
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, resolve
from django.shortcuts import get_object_or_404

from izin.models import DetilHO, Syarat, SKIzin, Riwayat, Survey, DetilSk, DetilPembayaran
from kepegawaian.models import Pegawai, UnitKerja
from accounts.models import NomorIdentitasPengguna
from izin.utils import*

class DetilHOAdmin(admin.ModelAdmin):
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
		if split_[0] == 'HO':
			no_pengajuan = mark_safe("""
				<a href="%s" target="_blank"> %s </a>
				""" % (reverse('admin:izin_detilho_change', args=(obj.id,)), obj.no_pengajuan ))
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
					'fields': ('pemohon','perusahaan')
					}
				),
				('Detail Izin', {'fields': ('kelompok_jenis_izin', 'jenis_permohonan','no_pengajuan', 'no_izin','legalitas')}),
				('Detail Kuasa', {'fields': ('nama_kuasa','no_identitas_kuasa','telephone_kuasa',) }),
				('Detail HO', {'fields': ('perkiraan_modal','tujuan_gangguan','alamat','no_surat_tanah','tanggal_surat_tanah','desa','bahan_baku_dan_penolong','proses_produksi','jenis_produksi','kapasitas_produksi','jumlah_tenaga_kerja','jumlah_mesin','merk_mesin','daya','kekuatan','luas_ruang_tempat_usaha','luas_lahan_usaha','jenis_lokasi_usaha','jenis_bangunan','jenis_gangguan') }),
				('Berkas & Keterangan', {'fields': ('berkas_tambahan', 'keterangan',)}),

				('Lain-lain', {'fields': ('status', 'created_by', 'created_at', 'verified_by', 'verified_at', 'updated_at')}),
			)
		else:
			add_fieldsets = (
				(None, {
					'classes': ('wide',),
					'fields': ('pemohon','perusahaan')
					}
				),
				('Detail Izin', {'fields': ('kelompok_jenis_izin', 'jenis_permohonan','no_pengajuan', 'no_izin','legalitas')}),
				('Detail Kuasa', {'fields': ('nama_kuasa','no_identitas_kuasa','telephone_kuasa',) }),
				('Detail HO', {'fields': ('perkiraan_modal','tujuan_gangguan','alamat','no_surat_tanah','tanggal_surat_tanah','desa','bahan_baku_dan_penolong','proses_produksi','jenis_produksi','kapasitas_produksi','jumlah_tenaga_kerja','jumlah_mesin','merk_mesin','daya','kekuatan','luas_ruang_tempat_usaha','luas_lahan_usaha','jenis_lokasi_usaha','jenis_bangunan','jenis_gangguan') }),
				('Berkas & Keterangan', {'fields': ('berkas_tambahan', 'keterangan',)}),
			)
		return add_fieldsets

	def view_pengajuan_izin_gangguan(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			pengajuan_ = DetilHO.objects.get(id=id_pengajuan_izin_)
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.pemohon.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
				nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all().last()
				extra_context.update({'nomor_identitas': nomor_identitas_ })
				try:
					try:
						ktp_ = NomorIdentitasPengguna.objects.get(user_id=pengajuan_.pemohon.id)
					except MultipleObjectsReturned:
						ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id).order_by('id').first()
					extra_context.update({'cookie_file_ktp': ktp_.berkas })
				except ObjectDoesNotExist:
					pass
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({'alamat_perusahaan': alamat_perusahaan_ })
				extra_context.update({'perusahaan': pengajuan_.perusahaan})

				legalitas_pendirian = pengajuan_.perusahaan.legalitas_set.filter(berkas__keterangan="akta pendirian").last()
				legalitas_perubahan = pengajuan_.perusahaan.legalitas_set.filter(berkas__keterangan="akta perubahan").last()
				extra_context.update({ 'legalitas_pendirian': legalitas_pendirian })
				extra_context.update({ 'legalitas_perubahan': legalitas_perubahan })
			letak_ = ""
			if pengajuan_.alamat:
				letak_ = pengajuan_.alamat
			if pengajuan_.desa and pengajuan_.desa:
				letak_ = pengajuan_.alamat + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)

			# extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})
			pengajuan_id = pengajuan_.id
			extra_context.update({'letak': letak_})
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})
			extra_context.update({'status': pengajuan_.status})
			extra_context.update({'pengajuan': pengajuan_})
			# encode_pengajuan_id = (str(pengajuan_.id))


			# UNTUK SURVEY
			from django.contrib.auth.models import Group

			extra_context.update({'skpd_list' : UnitKerja.objects.all() })

			h = Group.objects.filter(name="Cek Lokasi")
			if h.exists():
				h = h.last()
			h = h.user_set.all()
			extra_context.update({'pegawai_list' : h })

			try:
				try:
					s = Survey.objects.get(pengajuan=pengajuan_)
				except Survey.MultipleObjectsReturned:
					s = Survey.objects.filter(pengajuan=pengajuan_).last()
					# print s.survey_iujk.all()
				# print s.survey_reklame_ho.all()
				extra_context.update({'detilbap': s.survey_reklame_ho.all().last() })
			except ObjectDoesNotExist:
				s = ''

			extra_context.update({'survey': s })
			# END UNTUK SURVEY

			extra_context.update({'pengajuan_id': pengajuan_id })
			#+++++++++++++ page logout ++++++++++
			extra_context.update({'has_permission': True })
			#+++++++++++++ end page logout ++++++++++

			# lama_pemasangan = pengajuan_.tanggal_akhir-pengajuan_.tanggal_mulai
			# print lama_pemasangan
			banyak = len(DetilHO.objects.all())
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

			try:
				sk_imb_ = DetilSk.objects.get(pengajuan_izin_id = id_pengajuan_izin_ )
				if sk_imb_:
					extra_context.update({'sk_imb': sk_imb_ })
			except ObjectDoesNotExist:
				print "WASEM"

		template = loader.get_template("admin/izin/pengajuanizin/view_izin_gangguan.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_sk_izin_gangguan(self, request, id_pengajuan_izin_, salinan_=None):
		extra_context = {}
		# id_pengajuan_izin_ = base64.b64decode(id_pengajuan_izin_)
		# print id_pengajuan_izin_
		if id_pengajuan_izin_:
			extra_context.update({'salinan': salinan_})
			pengajuan_ = DetilHO.objects.get(id=id_pengajuan_izin_)
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.pemohon.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({'alamat_perusahaan': alamat_perusahaan_})
				extra_context.update({'perusahaan': pengajuan_.perusahaan })
			letak_ = pengajuan_.alamat + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
			if pengajuan_.luas_ruang_tempat_usaha:
				luas_ruang_tempat_usaha_ = '{0:f}'.format(pengajuan_.luas_ruang_tempat_usaha)
				luas_ruang_tempat_ = luas_ruang_tempat_usaha_.split(".")[1]
				if luas_ruang_tempat_ == "00":
					luas_ruang_tempat_usaha_ = ("%.0f" % pengajuan_.luas_ruang_tempat_usaha)
				else:
					luas_ruang_tempat_usaha_ = pengajuan_.luas_ruang_tempat_usaha
				extra_context.update({'luas_ruang_tempat_usaha_': luas_ruang_tempat_usaha_})
			if pengajuan_.luas_lahan_usaha:
				luas_lahan_usaha_ = '{0:f}'.format(pengajuan_.luas_lahan_usaha)
				luas_lahan_ = luas_lahan_usaha_.split(".")[1]
				if luas_lahan_ == "00":
					luas_lahan_usaha_ = ("%.0f" % pengajuan_.luas_lahan_usaha)
				else:
					luas_lahan_usaha_ = pengajuan_.luas_lahan_usaha
				extra_context.update({'luas_lahan_usaha_': luas_lahan_usaha_})			
			# ukuran_ = "Lebar = "+str(int(pengajuan_.lebar))+" M, Tinggi = "+str(int(pengajuan_.tinggi))+" M"  
			# jumlah_ = str(int(pengajuan_.jumlah))
			# klasifikasi_ = pengajuan_.klasifikasi_jalan

			# extra_context.update({'jumlah': jumlah_ })
			# extra_context.update({'klasifikasi_jalan': klasifikasi_ })
			# extra_context.update({'ukuran': ukuran_})
			extra_context.update({'letak': letak_})
			nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
			extra_context.update({'nomor_identitas': nomor_identitas_ })
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'pengajuan': pengajuan_ })
			extra_context.update({'foto': pengajuan_.pemohon.berkas_foto.all().last()})
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
					extra_context.update({'gelar_depan': kepala_.gelar_depan })
					extra_context.update({'nama_kepala_dinas': kepala_.nama_lengkap })
					extra_context.update({'nip_kepala_dinas': kepala_.nomoridentitaspengguna_set.last() })

			except ObjectDoesNotExist:
				pass
			try:
				sk_imb_ = DetilSk.objects.get(pengajuan_izin__id = id_pengajuan_izin_ )
				if sk_imb_:
					extra_context.update({'sk_imb': sk_imb_ })
			except ObjectDoesNotExist:
				pass

			try:
				retribusi_ = DetilPembayaran.objects.get(pengajuan_izin__id = id_pengajuan_izin_)
				if retribusi_:
					n = int(retribusi_.jumlah_pembayaran.replace(".", ""))
					terbilang_ = terbilang(n)
					extra_context.update({'retribusi': retribusi_ })
					extra_context.update({'terbilang': terbilang_ })
			except ObjectDoesNotExist:
				pass
		template = loader.get_template("front-end/include/formulir_ho/cetak_sk_izin_gangguan.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))


	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilHOAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^cetak-sk-izin-gangguan/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.cetak_sk_izin_gangguan), name='cetak_sk_izin_gangguan'),
			url(r'^cetak-sk-izin-gangguan/(?P<id_pengajuan_izin_>[0-9]+)/(?P<salinan_>\w+)$', self.admin_site.admin_view(self.cetak_sk_izin_gangguan), name='cetak_sk_izin_gangguan'),
			url(r'^view-pengajuan-izin-gangguan/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_izin_gangguan), name='view_pengajuan_izin_gangguan'),

			)
		return my_urls + urls

admin.site.register(DetilHO, DetilHOAdmin)