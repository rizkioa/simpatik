import base64, datetime
from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, resolve
from django.shortcuts import get_object_or_404, render
from django.http import Http404

from izin.models import InformasiTanah, Syarat, SKIzin, Riwayat, SertifikatTanah, DetilSk, Survey
from kepegawaian.models import Pegawai, UnitKerja
from accounts.models import NomorIdentitasPengguna

class InformasiTanahAdmin(admin.ModelAdmin):
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
		# 	add_fieldsets = (
		# 		(None, {
		# 			'classes': ('wide',),
		# 			'fields': ('pemohon','perusahaan',)
		# 			}
		# 		),
		# 		('Detail Izin', {'fields': ('kelompok_jenis_izin', 'jenis_permohonan','no_pengajuan', 'no_izin','legalitas')}),
		# 		('Detail Kuasa', {'fields': ('nama_kuasa','no_identitas_kuasa','telephone_kuasa',) }),
		# 		('Detail Informasi Tanah', {'fields': ('no_surat_kuasa','tanggal_surat_kuasa','alamat','desa','luas','status_tanah','no_sertifikat_petak','luas_sertifikat_petak','atas_nama_sertifikat_petak','no_persil','klas_persil','atas_nama_persil','penggunaan_sekarang','rencana_penggunaan') }),
		# 		('Berkas & Keterangan', {'fields': ('berkas_tambahan', 'keterangan',)}),

		# 		('Lain-lain', {'fields': ('status', 'created_by', 'created_at', 'verified_by', 'verified_at', 'updated_at')}),
		# 	)
		# if obj.kelompok_jenis_izin.kode == "IPPT-Usaha" and request.user.is_superuser:
			add_fieldsets = (
				(None, {
					'classes': ('wide',),
					'fields': ('pemohon','perusahaan',)
					}
				),
				('Detail Izin', {'fields': ('kelompok_jenis_izin', 'jenis_permohonan','no_pengajuan', 'no_izin','legalitas')}),
				('Detail Kuasa', {'fields': ('nama_kuasa','no_identitas_kuasa','telephone_kuasa',) }),
				('Detail Informasi Tanah', {'fields': ('alamat','desa','luas','status_tanah','no_sertifikat_petak','luas_sertifikat_petak','atas_nama_sertifikat_petak','tahun_sertifikat','no_persil','klas_persil','atas_nama_persil','no_jual_beli','tanggal_jual_beli','atas_nama_jual_beli','no_surat_pemberitahuan','tanggal_surat_pemberitahuan','rencana_penggunaan','luas_tanah_yang_disetujui','batas_utara','batas_timur','batas_selatan','batas_barat','tanah_negara_belum_dikuasai','tanah_kas_desa_belum_dikuasai','tanah_hak_pakai_belum_dikuasai','tanah_hak_guna_bangunan_belum_dikuasai','tanah_hak_milik_sertifikat_belum_dikuasai','tanah_adat_belum_dikuasai','pemegang_hak_semula_dari_tanah_belum_dikuasai','tanah_belum_dikuasai_melalui','tanah_negara_sudah_dikuasai','tanah_kas_desa_sudah_dikuasai','tanah_hak_pakai_sudah_dikuasai','tanah_hak_guna_bangunan_sudah_dikuasai','tanah_hak_milik_sertifikat_sudah_dikuasai','tanah_adat_sudah_dikuasai','pemegang_hak_semula_dari_tanah_sudah_dikuasai','tanah_sudah_dikuasai_melalui','jumlah_tanah_belum_dikuasai','jumlah_tanah_sudah_dikuasai') }),
				('Rencana Pembangunan',{'fields': ('tipe1','tipe2','tipe3','gudang1','gudang2','gudang3','luas_tipe1','luas_tipe2','luas_tipe3','luas_lapangan','luas_kantor','luas_saluran','luas_taman','presentase_luas_tipe1','presentase_luas_tipe2','presentase_luas_tipe3','presentase_luas_lapangan','presentase_luas_kantor','presentase_luas_saluran','presentase_luas_taman','presentase_jumlah_perincian_penggunaan_tanah','jumlah_perincian_penggunaan_tanah','pematangan_tanah_tahap1','pematangan_tanah_tahap2','pematangan_tanah_tahap3','pembangunan_gedung_tahap1','pembangunan_gedung_tahap2','pembangunan_gedung_tahap3','jangka_waktu_selesai')}),
				('Rencana Pembiayaan & Pemodalan',{'fields': ('modal_tetap_tanah','modal_tetap_bangunan','modal_tetap_mesin','modal_tetap_angkutan','modal_tetap_inventaris','modal_tetap_lainnya','jumlah_modal_tetap','modal_kerja_bahan','modal_kerja_gaji','modal_kerja_alat_angkut','modal_kerja_lainnya','jumlah_modal_kerja','modal_dasar','modal_ditetapkan','modal_disetor','modal_bank_pemerintah','modal_bank_swasta','modal_lembaga_non_bank','modal_pihak_ketiga','modal_pinjaman_luar_negeri','jumlah_investasi','saham_indonesia','saham_asing')}),
				('Kebutuhan Lainnya',{'fields': ('tenaga_ahli','pegawai_tetap','pegawai_harian_tetap','pegawai_harian_tidak_tetap','kebutuhan_listrik','kebutuhan_listrik_sehari_hari','jumlah_daya_genset','jumlah_listrik_kebutuhan_dari_pln','air_untuk_rumah_tangga','air_untuk_produksi','air_lainnya','air_dari_pdam','air_dari_sumber','air_dari_sungai','tenaga_kerja_wni','tenaga_kerja_wna','tenaga_kerja_tetap','tenaga_kerja_tidak_tetap')}),
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
				('Detail Informasi Tanah', {'fields': ('alamat','desa','luas','status_tanah','no_sertifikat_petak','luas_sertifikat_petak','atas_nama_sertifikat_petak','tahun_sertifikat','no_persil','klas_persil','atas_nama_persil','no_jual_beli','tanggal_jual_beli','atas_nama_jual_beli','no_surat_pemberitahuan','tanggal_surat_pemberitahuan','rencana_penggunaan','batas_utara','batas_timur','batas_selatan','batas_barat','tanah_negara_belum_dikuasai','tanah_kas_desa_belum_dikuasai','tanah_hak_pakai_belum_dikuasai','tanah_hak_guna_bangunan_belum_dikuasai','tanah_hak_milik_sertifikat_belum_dikuasai','tanah_adat_belum_dikuasai','pemegang_hak_semula_dari_tanah_belum_dikuasai','tanah_belum_dikuasai_melalui','tanah_negara_sudah_dikuasai','tanah_kas_desa_sudah_dikuasai','tanah_hak_pakai_sudah_dikuasai','tanah_hak_guna_bangunan_sudah_dikuasai','tanah_hak_milik_sertifikat_sudah_dikuasai','tanah_adat_sudah_dikuasai','pemegang_hak_semula_dari_tanah_sudah_dikuasai','tanah_sudah_dikuasai_melalui','jumlah_tanah_belum_dikuasai','jumlah_tanah_sudah_dikuasai') }),
				('Rencana Pembangunan',{'fields': ('tipe1','tipe2','tipe3','gudang1','gudang2','gudang3','luas_tipe1','luas_tipe2','luas_tipe3','luas_lapangan','luas_kantor','luas_saluran','luas_taman','presentase_luas_tipe1','presentase_luas_tipe2','presentase_luas_tipe3','presentase_luas_lapangan','presentase_luas_kantor','presentase_luas_saluran','presentase_luas_taman','presentase_jumlah_perincian_penggunaan_tanah','jumlah_perincian_penggunaan_tanah','pematangan_tanah_tahap1','pematangan_tanah_tahap2','pematangan_tanah_tahap3','pembangunan_gedung_tahap1','pembangunan_gedung_tahap2','pembangunan_gedung_tahap3','jangka_waktu_selesai')}),
				('Rencana Pembiayaan & Pemodalan',{'fields': ('modal_tetap_tanah','modal_tetap_bangunan','modal_tetap_mesin','modal_tetap_angkutan','modal_tetap_inventaris','modal_tetap_lainnya','jumlah_modal_tetap','modal_kerja_bahan','modal_kerja_gaji','modal_kerja_alat_angkut','modal_kerja_lainnya','jumlah_modal_kerja','modal_dasar','modal_ditetapkan','modal_disetor','modal_bank_pemerintah','modal_bank_swasta','modal_lembaga_non_bank','modal_pihak_ketiga','modal_pinjaman_luar_negeri','jumlah_investasi','saham_indonesia','saham_asing')}),
				('Kebutuhan Lainnya',{'fields': ('tenaga_ahli','pegawai_tetap','pegawai_harian_tetap','pegawai_harian_tidak_tetap','kebutuhan_listrik','kebutuhan_listrik_sehari_hari','jumlah_daya_genset','jumlah_listrik_kebutuhan_dari_pln','air_untuk_rumah_tangga','air_untuk_produksi','air_lainnya','air_dari_pdam','air_dari_sumber','air_dari_sungai','tenaga_kerja_wni','tenaga_kerja_wna','tenaga_kerja_tetap','tenaga_kerja_tidak_tetap')}),
				('Berkas & Keterangan', {'fields': ('berkas_tambahan', 'keterangan',)}),
			)
		return add_fieldsets

	def view_pengajuan_izin_lokasi(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			# pengajuan_ = InformasiTanah.objects.get(id=id_pengajuan_izin_)
			pengajuan_ = get_object_or_404(InformasiTanah, id=id_pengajuan_izin_)
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
				ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id)
				if ktp_.exists():
					ktp_ = ktp_.last()
					extra_context.update({'cookie_file_ktp': ktp_.berkas })
				
				sertifikat_tanah_list = SertifikatTanah.objects.filter(informasi_tanah__id=id_pengajuan_izin_)
				extra_context.update({'sertifikat_tanah_list': sertifikat_tanah_list})
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({'alamat_perusahaan': alamat_perusahaan_ })
				extra_context.update({'perusahaan': pengajuan_.perusahaan})

				legalitas_pendirian = pengajuan_.perusahaan.legalitas_set.filter(berkas__keterangan="akta pendirian").last()
				legalitas_perubahan = pengajuan_.perusahaan.legalitas_set.filter(berkas__keterangan="akta perubahan").last()
				extra_context.update({ 'legalitas_pendirian': legalitas_pendirian })
				extra_context.update({ 'legalitas_perubahan': legalitas_perubahan })
			if pengajuan_.desa:
				letak_ = pengajuan_.alamat +", Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())
			else:
				letak_ = pengajuan_.alamat
			# extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})
			pengajuan_id = pengajuan_.id
			extra_context.update({'letak': letak_})
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})
			extra_context.update({'status': pengajuan_.status})
			extra_context.update({'pengajuan': pengajuan_})
			# encode_pengajuan_id = (str(pengajuan_.id))
			extra_context.update({'pengajuan_id': pengajuan_id })
			#+++++++++++++ page logout ++++++++++
			extra_context.update({'has_permission': True })

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
			except ObjectDoesNotExist:
				s = ''

			extra_context.update({'survey': s })
			extra_context.update({'skpd_list' : UnitKerja.objects.all() })
			#+++++++++++++ end page logout ++++++++++

			# lama_pemasangan = pengajuan_.tanggal_akhir-pengajuan_.tanggal_mulai
			# print lama_pemasangan
			banyak = len(InformasiTanah.objects.all())
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
		template = loader.get_template("admin/izin/pengajuanizin/view_izin_lokasi.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def view_pengajuan_ippt_usaha(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			# pengajuan_ = InformasiTanah.objects.get(id=id_pengajuan_izin_)
			pengajuan_ = get_object_or_404(InformasiTanah, id=id_pengajuan_izin_)
			extra_context.update({'survey_pengajuan' : pengajuan_.survey_pengajuan.all().last() })
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
					ktp_ = NomorIdentitasPengguna.objects.get(user_id=pengajuan_.pemohon.id)
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
			if pengajuan_.desa:
				letak_ = pengajuan_.alamat +", Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())
			else:
				letak_ = pengajuan_.alamat
			legalitas_list = pengajuan_.perusahaan.legalitas_set.all()
			penggunaan_tanah_list = pengajuan_.penggunaantanahipptusaha_set.all()
			perumahan_yang_dimiliki_list = pengajuan_.perumahanyangdimilikiipptusaha_set.all()

			if pengajuan_.jumlah_modal_tetap or pengajuan_.jumlah_modal_kerja != '':
				jumlah_rencana_biaya = int(pengajuan_.jumlah_modal_tetap.replace(".",""))+int(pengajuan_.jumlah_modal_kerja.replace(".",""))
			else:
				jumlah_rencana_biaya = ""

			if pengajuan_.modal_bank_pemerintah or pengajuan_.modal_bank_swasta or pengajuan_.modal_lembaga_non_bank or pengajuan_.modal_pihak_ketiga != '':
				jumlah_pinjaman_dalam = int(pengajuan_.modal_bank_pemerintah.replace(".",""))+int(pengajuan_.modal_bank_swasta.replace(".",""))+int(pengajuan_.modal_lembaga_non_bank.replace(".",""))+int(pengajuan_.modal_pihak_ketiga.replace(".",""))
			else:
				jumlah_pinjaman_dalam = ""

			jumlah_saham = str(pengajuan_.saham_indonesia + pengajuan_.saham_asing)
			jumlah_kebutuhan_air = str(pengajuan_.air_untuk_rumah_tangga + pengajuan_.air_untuk_produksi + pengajuan_.air_lainnya)
			jumlah_minimal_kebutuhan_air = str(pengajuan_.air_dari_pdam + pengajuan_.air_dari_sumber + pengajuan_.air_dari_sungai)

			if pengajuan_.tenaga_kerja_wni or pengajuan_.tenaga_kerja_wna or pengajuan_.tenaga_kerja_tetap or pengajuan_.tenaga_kerja_tidak_tetap != None:
				jumlah_tenaga_kerja = pengajuan_.tenaga_kerja_wni + pengajuan_.tenaga_kerja_wna + pengajuan_.tenaga_kerja_tetap + pengajuan_.tenaga_kerja_tidak_tetap
			else:
				jumlah_tenaga_kerja = ""
			pengajuan_id = pengajuan_.id
			extra_context.update({ 'legalitas_list': legalitas_list })
			extra_context.update({ 'penggunaan_tanah_list': penggunaan_tanah_list })
			extra_context.update({ 'perumahan_yang_dimiliki_list': perumahan_yang_dimiliki_list })
			extra_context.update({ 'jumlah_rencana_biaya': jumlah_rencana_biaya })
			extra_context.update({ 'jumlah_pinjaman_dalam': jumlah_pinjaman_dalam })
			extra_context.update({ 'jumlah_saham': jumlah_saham })
			extra_context.update({ 'jumlah_kebutuhan_air': jumlah_kebutuhan_air })
			extra_context.update({ 'jumlah_minimal_kebutuhan_air': jumlah_minimal_kebutuhan_air })
			extra_context.update({ 'jumlah_tenaga_kerja': jumlah_tenaga_kerja })
			extra_context.update({'letak': letak_})
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})
			extra_context.update({'status': pengajuan_.status})
			extra_context.update({'pengajuan': pengajuan_})
			# encode_pengajuan_id = (str(pengajuan_.id))
			extra_context.update({'pengajuan_id': pengajuan_id })
			#+++++++++++++ page logout ++++++++++
			extra_context.update({'has_permission': True })
			#+++++++++++++ end page logout ++++++++++

			# lama_pemasangan = pengajuan_.tanggal_akhir-pengajuan_.tanggal_mulai
			# print lama_pemasangan
			banyak = len(InformasiTanah.objects.all())
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
		template = loader.get_template("admin/izin/pengajuanizin/view_izin_ippt_usaha.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_sk_izin_lokasi(self, request, id_pengajuan_izin_, salinan_=None):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'salinan': salinan_})
			# pengajuan_ = InformasiTanah.objects.get(id=id_pengajuan_izin_)
			pengajuan_ = get_object_or_404(InformasiTanah, id=id_pengajuan_izin_)
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
			letak_ = pengajuan_.alamat +", Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())

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
				sk_ = DetilSk.objects.get(pengajuan_izin__id = id_pengajuan_izin_ )
				if sk_:
					extra_context.update({'sk_': sk_ })
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

		template = loader.get_template("front-end/include/formulir_izin_lokasi/cetak_sk_izin_lokasi.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_skizin_ippt_rumah_super(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			# extra_context.update({'salinan': salinan_})
			# pengajuan_ = InformasiTanah.objects.get(id=id_pengajuan_izin_)
			pengajuan_ = get_object_or_404(InformasiTanah, id=id_pengajuan_izin_)
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
			letak_ = pengajuan_.alamat +", Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())

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
				sk_ = DetilSk.objects.get(pengajuan_izin__id = id_pengajuan_izin_ )
				if sk_:
					extra_context.update({'sk_': sk_ })
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
		return extra_context

	def cetak_sk_izin_ippt_rumah(self, request, id_pengajuan_izin_, salinan_=None):
		extra_context = {}
		extra_context = self.cetak_skizin_ippt_rumah_super(request, id_pengajuan_izin_)
		extra_context.update({'salinan': salinan_})
		extra_context.update({'print': "oke"})
		template = loader.get_template("front-end/include/formulir_ippt_rumah/cetak_sk_izin_ippt_rumah.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_skizin_ippt_usaha_super(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			# extra_context.update({'salinan': salinan_})
			# pengajuan_ = InformasiTanah.objects.get(id=id_pengajuan_izin_)
			pengajuan_ = get_object_or_404(InformasiTanah, id=id_pengajuan_izin_)
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
			letak_ = pengajuan_.alamat +", Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())

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
		return extra_context

	def cetak_sk_izin_ippt_usaha(self, request, id_pengajuan_izin_, salinan_=None):
		extra_context = {}
		extra_context = self.cetak_skizin_ippt_usaha_super(request, id_pengajuan_izin_)
		extra_context.update({'salinan': salinan_})
		extra_context.update({'print': "oke"})
		template = loader.get_template("front-end/include/formulir_ippt_usaha/cetak_sk_izin_ippt_usaha.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_skizin_ippt_rumah_pdf(self, request, id_pengajuan_izin_, salinan_=None):
		extra_context = {}
		extra_context = self.cetak_skizin_ippt_rumah_super(request, id_pengajuan_izin_)
		extra_context.update({'salinan': salinan_})
		template = loader.get_template("front-end/include/formulir_ippt_rumah/cetak_sk_izin_ippt_rumah.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_skizin_ippt_usaha_pdf(self, request, id_pengajuan_izin_, salinan_=None):
		extra_context = {}
		extra_context = self.cetak_skizin_ippt_usaha_super(request, id_pengajuan_izin_)
		extra_context.update({'salinan': salinan_})
		template = loader.get_template("front-end/include/formulir_ippt_usaha/cetak_sk_izin_ippt_usaha.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_sk_izin_lokasi_pdf(self, request, id_pengajuan):
		from izin.utils import render_to_pdf, cek_apikey
		extra_context = {}
		username = request.GET.get('username')
		apikey = request.GET.get('api_key')
		cek = cek_apikey(apikey, username)
		if cek == True:
			if id_pengajuan:
				pengajuan_ = get_object_or_404(InformasiTanah, id=id_pengajuan)
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
				letak_ = ""
				if pengajuan_.alamat:
					letak_ = pengajuan_.lokasi+", "
				if pengajuan_.desa:
					letak_ = pengajuan_.desa.lokasi_lengkap()

				extra_context.update({'letak': letak_})
				nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
				extra_context.update({'nomor_identitas': nomor_identitas_ })
				extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
				extra_context.update({'pengajuan': pengajuan_ })
				extra_context.update({'foto': pengajuan_.pemohon.berkas_foto.all().last()})
				try:
					skizin_ = SKIzin.objects.get(pengajuan_izin_id = id_pengajuan )
					if skizin_:
						extra_context.update({'skizin': skizin_ })
						extra_context.update({'skizin_status': skizin_.status })
				except ObjectDoesNotExist:
					pass
				try:
					sk_ = DetilSk.objects.get(pengajuan_izin__id = id_pengajuan)
					if sk_:
						extra_context.update({'sk_': sk_ })
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
			else:
				raise Http404
		else:
			raise Http404
		return render(request, "front-end/include/formulir_izin_lokasi/cetak_skizin_izin_lokasi_pdf.html", extra_context)

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(InformasiTanahAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^cetak-sk-izin-lokasi/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.cetak_sk_izin_lokasi), name='cetak_sk_izin_lokasi'),
			url(r'^cetak-sk-izin-lokasi/(?P<id_pengajuan_izin_>[0-9]+)/(?P<salinan_>\w+)/$', self.admin_site.admin_view(self.cetak_sk_izin_lokasi), name='cetak_sk_izin_lokasi'),
			url(r'^cetak-sk-izin-ippt-rumah/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.cetak_sk_izin_ippt_rumah), name='cetak_sk_izin_ippt_rumah'),
			url(r'^cetak-sk-izin-ippt-rumah-pdf/(?P<id_pengajuan_izin_>[0-9]+)$', self.cetak_skizin_ippt_rumah_pdf, name='cetak_skizin_ippt_rumah_pdf'),
			url(r'^cetak-sk-izin-ippt-rumah/(?P<id_pengajuan_izin_>[0-9]+)/(?P<salinan_>\w+)/$', self.admin_site.admin_view(self.cetak_sk_izin_ippt_rumah), name='cetak_sk_izin_ippt_rumah'),
			url(r'^cetak-sk-izin-ippt-usaha/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.cetak_sk_izin_ippt_usaha), name='cetak_sk_izin_ippt_usaha'),
			url(r'^cetak-sk-izin-ippt-usaha-pdf/(?P<id_pengajuan_izin_>[0-9]+)$', self.cetak_skizin_ippt_usaha_pdf, name='cetak_skizin_ippt_usaha_pdf'),
			url(r'^cetak-sk-izin-ippt-usaha/(?P<id_pengajuan_izin_>[0-9]+)/(?P<salinan_>\w+)/$', self.admin_site.admin_view(self.cetak_sk_izin_ippt_usaha), name='cetak_sk_izin_ippt_usaha'),
			url(r'^view-pengajuan-izin/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_izin_lokasi), name='view_pengajuan_izin_lokasi'),
			url(r'^cetak-sk-izin-lokasi-pdf/(?P<id_pengajuan>[0-9]+)/$', self.cetak_sk_izin_lokasi_pdf, name='cetak_sk_izin_lokasi_pdf'),
			url(r'^ippt-usaha/view-pengajuan-izin/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_ippt_usaha), name='view_pengajuan_ippt_usaha'),
			)
		return my_urls + urls

admin.site.register(InformasiTanah, InformasiTanahAdmin)