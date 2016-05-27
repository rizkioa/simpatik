from django.contrib import admin
# from django.core.urlresolvers import reverse
# from django.http import HttpResponse
# from django.utils.safestring import mark_safe

from izin.pemohon_admin import PemohonAdmin
from izin.models import Pemohon
from master.models import JenisPemohon

# import json

# from izin.izin_admin import IzinAdmin
# from perusahaan.models import Perusahaan

# from django.shortcuts import get_object_or_404
# from django.core import serializers

# Register your models here.

admin.site.register(JenisPemohon)

admin.site.register(Pemohon, PemohonAdmin)

# class JenisPeraturanAdmin(admin.ModelAdmin):
# 	list_display = ('jenis_peraturan','keterangan')
# 	list_filter = ('jenis_peraturan','keterangan')

# admin.site.register(JenisPeraturan,JenisPeraturanAdmin)

# class DasarHukumAdmin(admin.ModelAdmin):
# 	list_display = ('instansi','nomor','tentang')
# 	list_filter = ('instansi','nomor','tentang')
# 	search_fields = ('jenis_peraturan','instansi','nomor','tentang')

# admin.site.register(DasarHukum,DasarHukumAdmin)

# class SyaratAdmin(admin.ModelAdmin):
# 	list_display = ('syarat', 'keterangan')
# 	search_fields = ('syarat',)

# admin.site.register(Syarat, SyaratAdmin)

# class ProsedurAdmin(admin.ModelAdmin):
# 	list_display = ('prosedur','lama','keterangan')
# 	list_filter = ('prosedur','lama')

# admin.site.register(Prosedur, ProsedurAdmin)

# class KelompokJenisIzinAdmin(admin.ModelAdmin):
# 	list_display = ('kelompok_jenis_izin','hargabeli','standart_waktu','keterangan')
# 	list_filter = ('kelompok_jenis_izin','biaya','standart_waktu')
# 	search_fields = ('kelompok_jenis_izin','biaya')

# 	def hargabeli(self, obj):
# 		return obj.get_biaya()
# 	hargabeli.short_description = 'Biaya'
# 	hargabeli.admin_order_field = 'biaya'

# admin.site.register(KelompokJenisIzin, KelompokJenisIzinAdmin)

# class JenisIzinAdmin(admin.ModelAdmin):
# 	list_display = ('nama_izin','jenis_izin','keterangan')
# 	list_filter = ('nama_izin','jenis_izin')
# 	search_fields = ('nama_izin','jenis_izin')
# 	filter_horizontal = ('dasar_hukum',)

# admin.site.register(JenisIzin,JenisIzinAdmin)

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

# admin.site.register(JenisPermohonanIzin)

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
