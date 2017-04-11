from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import json

from izin.detiltdp_admin import DetilTDPAdmin
from izin.detilsiup_admin import DetilSIUPAdmin
from izin.detiliujk_admin import DetilIUJKAdmin
from izin.detilreklame_admin import DetilReklameAdmin
from izin.imbreklame_admin import DetilIMBPapanReklameAdmin
from izin.imb_admin import DetilIMBAdmin
from izin.informasikekayaan_admin import InformasiKekayaanDaerahAdmin
from izin.detilho_admin import DetilHOAdmin
from izin.izin_admin import IzinAdmin 
from izin.informasitanah_admin import InformasiTanahAdmin 
from izin.paketpekerjaan_admin import PaketPekerjaanAdmin
from izin.huller_admin import DetilHullerAdmin
from izin.survey_admin import SurveyAdmin
from izin.detiltdup_admin import DetilTDUPAdmin
from izin.mesin_perusahaan_admin import MesinPerusahaanAdmin
from izin.models import Pemohon, JenisPeraturan, DasarHukum, JenisIzin, Syarat, Prosedur, KelompokJenisIzin, JenisPermohonanIzin, SKIzin, Riwayat, AnggotaBadanUsaha, PaketPekerjaan, DetilIUJK, PaketPekerjaan, Survey,JenisMesin, MesinHuller, MesinPerusahaan, PenggunaanTanahIPPTUsaha,PerumahanYangDimilikiIPPTUsaha, BentukKoperasi, JenisKoperasi, SertifikatTanah, DetilSk, DetilPembayaran, BidangUsahaPariwisata, JenisUsahaPariwisata, SubJenisUsahaPariwisata,DetilReklameIzin
from izin.pemohon_admin import PemohonAdmin
from master.models import JenisPemohon
from izin.izin_forms import SurveyForm
from izin.utils import get_nomor_pengajuan
from pembangunan.views import get_rekomendasi_pembangunan

# from perusahaan.models import Perusahaan

# from django.shortcuts import get_object_or_404
# from django.core import serializers

# Register your models here.
admin.site.register(BidangUsahaPariwisata)
admin.site.register(JenisUsahaPariwisata)
admin.site.register(SubJenisUsahaPariwisata)
admin.site.register(JenisKoperasi)
admin.site.register(BentukKoperasi)
admin.site.register(JenisPemohon)
admin.site.register(SKIzin)
admin.site.register(Riwayat)
admin.site.register(JenisMesin)
admin.site.register(MesinHuller)
admin.site.register(DetilPembayaran)
admin.site.register(SertifikatTanah)
admin.site.register(AnggotaBadanUsaha)
admin.site.register(DetilSk)
admin.site.register(DetilReklameIzin)
admin.site.register(Pemohon, PemohonAdmin)

class JenisPeraturanAdmin(admin.ModelAdmin):
	list_display = ('jenis_peraturan','keterangan')

admin.site.register(JenisPeraturan, JenisPeraturanAdmin)

class DasarHukumAdmin(admin.ModelAdmin):
	list_display = ('nomor', 'tahun', 'instansi', 'jenis_peraturan', 'tentang', 'keterangan', 'aksi')
	list_filter = ('jenis_peraturan__jenis_peraturan', 'tahun', )
	search_fields = ('instansi','nomor','tentang', 'keterangan')

	def aksi(self, obj):
		aksi_str = '<a title="Hapus Dasar Hukum" href="'+reverse('admin:izin_dasarhukum_delete', args=(obj.id,))+'"><span class="glyphicon glyphicon-remove-circle"></span></a>'
		link_berkas = ""
		if obj.berkas:
			link_berkas = "<a href='"+str(obj.get_file_url())+"'><span class='fa fa-download'></span></a>"
			aksi_str = link_berkas+" "+aksi_str
		return mark_safe(aksi_str)
	aksi.short_description = 'Aksi'
admin.site.register(DasarHukum, DasarHukumAdmin)

class JenisIzinAdmin(admin.ModelAdmin):
	list_display = ('kode','nama_izin','jenis_izin','keterangan')
	list_filter = ('dasar_hukum','jenis_izin')
	search_fields = ('kode','nama_izin','jenis_izin', 'dasar_hukum', 'keterangan')

	def tr_dasar_hukum(self, request, id_jenis_izin):
		jenis_izin_list = JenisIzin.objects.filter(id=id_jenis_izin)
		dasar_hukum_list = DasarHukum.objects.none()

		if jenis_izin_list.exists():
			dasar_hukum_list = jenis_izin_list.first().dasar_hukum.all()
		return HttpResponse(mark_safe("".join(x.as_tr() for x in dasar_hukum_list)))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(JenisIzinAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^tr/(?P<id_jenis_izin>\w+)/$', self.tr_dasar_hukum, name="tr_dasar_hukum_jenis_izin" )
			)
		return my_urls + urls

admin.site.register(JenisIzin, JenisIzinAdmin)

class SyaratAdmin(admin.ModelAdmin):
	list_display = ('syarat', 'keterangan')
	list_filter = ('jenis_izin', )
	search_fields = ('syarat', 'keterangan')

	def li(self, request, id_kelompok_jenis_izin):
		syarat_list = Syarat.objects.filter(jenis_izin__id=id_kelompok_jenis_izin)
		return HttpResponse(mark_safe("".join(x.as_li() for x in syarat_list)))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(SyaratAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^li/(?P<id_kelompok_jenis_izin>\w+)/$', self.li, name="li_syarat_kelompok_jenis_izin" )
			)
		return my_urls + urls

admin.site.register(Syarat, SyaratAdmin)

class ProsedurAdmin(admin.ModelAdmin):
	list_display = ('prosedur','lama','keterangan')
	search_fields = ('prosedur','lama','keterangan')

	def li(self, request, id_kelompok_jenis_izin):
		prosedur_list = Prosedur.objects.filter(jenis_izin__id=id_kelompok_jenis_izin).order_by('nomor_urut')
		return HttpResponse(mark_safe("".join(x.as_li() for x in prosedur_list)))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(ProsedurAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^li/(?P<id_kelompok_jenis_izin>\w+)/$', self.li, name="li_prosedur_kelompok_jenis_izin" )
			)
		return my_urls + urls

admin.site.register(Prosedur, ProsedurAdmin)

class KelompokJenisIzinAdmin(admin.ModelAdmin):
	list_display = ('kelompok_jenis_izin','jenis_izin', 'hargabeli', 'standart_waktu', 'keterangan')
	list_filter = ('biaya','standart_waktu', 'jenis_izin')
	search_fields = ('kelompok_jenis_izin','biaya', 'jenis_izin', 'biaya', 'standart_waktu', 'keterangan')

	def hargabeli(self, obj):
		return obj.get_biaya()
	hargabeli.short_description = 'Biaya'
	hargabeli.admin_order_field = 'biaya'

	

admin.site.register(KelompokJenisIzin, KelompokJenisIzinAdmin)

admin.site.register(JenisPermohonanIzin)
admin.site.register(PenggunaanTanahIPPTUsaha)
admin.site.register(PerumahanYangDimilikiIPPTUsaha)

# class DataPerubahanAdmin(admin.ModelAdmin):
# 	list_display = ('tabel_asal','nama_field','isi_field_lama','created_at')
# 	list_filter = ('tabel_asal','nama_field','created_at')
# 	search_fields = ('tabel_asal','nama_field','isi_field_lama')

# admin.site.register(DataPerubahan,DataPerubahanAdmin)

# admin.site.register(jenisLokasiUsaha)
# admin.site.register(JenisBangunan)

# class ParameterBangunanAdmin(admin.ModelAdmin):
# 	list_display = ('parameter','detil_parameter','nilai')
# 	list_filter = ('parameter','detil_parameter','nilai')
# 	search_fields = ('parameter','detil_parameter','nilai')

# admin.site.register(ParameterBangunan,ParameterBangunanAdmin)

# class JenisKegiatanPembangunanAdmin(admin.ModelAdmin):
# 	list_display = ('jenis_kegiatan_pembangunan','detil_jenis_kegiatan','nilai')
# 	list_filter = ('jenis_kegiatan_pembangunan','detil_jenis_kegiatan','nilai')
# 	search_fields = ('jenis_kegiatan_pembangunan','detil_jenis_kegiatan','nilai')

# admin.site.register(JenisKegiatanPembangunan, JenisKegiatanPembangunanAdmin)



# class DetilIMBPapanReklameAdmin(admin.ModelAdmin):
# 	list_display = ('jenis_papan_reklame','lebar','tinggi','lokasi_pasang')
# 	list_filter = ('jenis_papan_reklame','lokasi_pasang')
# 	search_fields = ('jenis_papan_reklame','lokasi_pasang')
# 	fieldsets = (
# 		(' Detil Papan Reklame', {
# 			'fields': ('jenis_papan_reklame', 'lebar', 'tinggi','lokasi_pasang',('batas_utara','batas_selatan'),('batas_timur','batas_barat'))
# 			}),
# 		)

# admin.site.register(DetilIMBPapanReklame, DetilIMBPapanReklameAdmin)

# admin.site.register(JenisGangguan)

# admin.site.register(Izin, IzinAdmin)

# class KekayaanDanSahamAdmin(admin.ModelAdmin):
# 	list_display = ('kekayaan_bersih','total_nilai_saham','presentase_saham_nasional','presentase_saham_asing')
# 	list_filter = ('kekayaan_bersih','total_nilai_saham')

# 	def ajax_kekayaan(self, request, perusahaan_id=None):
# 		kekayaan_get = KekayaanDanSaham.objects.filter(izin__perusahaan_id=perusahaan_id)
# 		results = [ob.as_json() for ob in kekayaan_get]
# 		return HttpResponse(json.dumps(results))

# 	def get_urls(self):
# 		from django.conf.urls import patterns, url
# 		urls = super(KekayaanDanSahamAdmin, self).get_urls()
# 		my_urls = patterns('',
# 			url(r'^ajax/kekayaan/(?P<perusahaan_id>\w+)/$', self.admin_site.admin_view(self.ajax_kekayaan), name='ajax_kekayaan'),
# 			)
# 		return my_urls + urls

# admin.site.register(KekayaanDanSaham, KekayaanDanSahamAdmin)

# class DetilHoAdmin(admin.ModelAdmin):
# 	list_display = ('perkiraan_modal','keperluan','alamat','bahan_baku_dan_penolong','proses_produksi')
# 	list_filter = ('perkiraan_modal','keperluan','bahan_baku_dan_penolong','proses_produksi')
# 	search_fields = ('perkiraan_modal','keperluan','alamat','bahan_baku_dan_penolong','proses_produksi')

# admin.site.register(DetilHo, DetilHoAdmin)

# admin.site.register(JenisReklame)

# class DataReklameAdmin(admin.ModelAdmin):
# 	list_display = ('judul_reklame','panjang','lebar','sisi')
# 	list_filter = ('judul_reklame','lama_pemasangan')
# 	search_fields = ('judul_reklame',)

# admin.site.register(DataReklame, DataReklameAdmin)

# admin.site.register(VerivikasiIzin)

# class StatusVerifikasiAdmin(admin.ModelAdmin):
# 	list_display = ('nama_verifikasi','cek_status','tanggal_verifikasi','keterangan')
# 	list_filter = ('nama_verifikasi','cek_status','tanggal_verifikasi')
# 	search_fields = ('nama_verifikasi')

# admin.site.register(StatusVerifikasi)
# admin.site.register(StatusHakTanah)
# admin.site.register(KepemilikkanTanah)
# admin.site.register(JenisTanah)

# class DetilIMBGedungAdmin(admin.ModelAdmin):
# 	list_display = ('luas_bangunan','unit','luas_tanah','no_surat_tanah')
# 	list_filter = ('luas_bangunan','unit','luas_tanah')
# 	search_fields = ('no_surat_tanah','luas_bangunan')

# admin.site.register(DetilIMBGedung, DetilIMBGedungAdmin)

# class CeklisSyaratIzinAdmin(admin.ModelAdmin):
# 	list_filter = ('cek',)

# admin.site.register(CeklisSyaratIzin, CeklisSyaratIzinAdmin)

# class JenisBerkasAdmin(admin.ModelAdmin):
# 	list_display = ('jenis_berkas','keterangan')
# 	list_filter = ('jenis_berkas',)
# 	search_fields = ('jenis_berkas',)

# admin.site.register(JenisBerkas, JenisBerkasAdmin)

# class BerkasAdmin(admin.ModelAdmin):
# 	list_display = ('jenis_berkas','nama_berkas','berkas')
# 	list_filter = ('jenis_berkas','nama_berkas')
# 	search_fields = ('jenis_berkas','nama_berkas','berkas')

# admin.site.register(Berkas, BerkasAdmin)
