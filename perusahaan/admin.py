from django.contrib import admin
from perusahaan.models import JenisPerusahaan, KBLI, JenisPenanamanModal, StatusPerusahaan, JenisKerjasama, JenisBadanUsaha, Perusahaan, JenisKedudukan, DataPimpinan, JenisKegiatanUsaha, JenisPengecer, KegiatanUsaha, DataRincianPerusahaan, PemegangSahamLain, Kelembagaan, ProdukUtama, JenisMesin, MesinHuller, MesinPerusahaan, AktaNotaris, JenisModalKoprasi, ModalKoprasi, NilaiModal, LokasiUnitProduksi
from perusahaan.perusahaan_admin import PerusahaanAdmin

# Register your models here.

admin.site.register(JenisPenanamanModal)

class JenisPerusahaanAdmin(admin.ModelAdmin):
	list_display = ('jenis_perusahaan',)
	search_fields = ('jenis_perusahaan',)

admin.site.register(JenisPerusahaan, JenisPerusahaanAdmin)

class KBLIAdmin(admin.ModelAdmin):
	list_display = ('kode_kbli','nama_kbli')
	search_fields = ('nama_kbli',)

admin.site.register(KBLI, KBLIAdmin)

admin.site.register(Perusahaan, PerusahaanAdmin)

admin.site.register(JenisKedudukan)

class DataPimpinanAdmin(admin.ModelAdmin):
	list_display = ('nama_lengkap','perusahaan','kedudukan','tanggal_menduduki_jabatan','kedudukan_diperusahaan_lain','nama_perusahaan_lain')
	list_filter = ('kedudukan','nama_lengkap')
	search_fields = ('nama_lengkap','kedudukan')

admin.site.register(DataPimpinan, DataPimpinanAdmin)

class JenisKegiatanUsahaAdmin(admin.ModelAdmin):
	list_display = ('jenis_kegiatan_usaha',)
	list_filter = ('jenis_kegiatan_usaha',)

admin.site.register(JenisKegiatanUsaha, JenisKegiatanUsahaAdmin)

class DataRincianPerusahaanAdmin(admin.ModelAdmin):
	list_display = ('perusahaan', 'omset_per_tahun', 'total_aset', 'kapasitas_mesin_terpasang','jenis_kegiatan',)
	search_fields = ('perusahaan', 'jenis_kegiatan', 'omset_per_tahun','total_aset', 'kapasitas_mesin_terpasang')
	list_filter = ('perusahaan','jenis_kegiatan','omset_per_tahun')
	ordering = ('id',)

admin.site.register(DataRincianPerusahaan, DataRincianPerusahaanAdmin)

class KelembagaanAdmin(admin.ModelAdmin):
	list_display = ('nama_kelembagaan',)
	search_fields = ('nama_kelembagaan',)

admin.site.register(Kelembagaan, KelembagaanAdmin)

class PemegangSahamaLainAdmin(admin.ModelAdmin):
	list_display = ('perusahaan','npwp','jumlah_saham_dimiliki','jumlah_modal_disetor')
	list_filter = ('perusahaan','jumlah_saham_dimiliki')
	search_fields = ('npwp','perusahaan')

admin.site.register(PemegangSahamLain, PemegangSahamaLainAdmin)

class MesinPerusahaanAdmin(admin.ModelAdmin):
	list_display = ('mesin','tipe','PK','merk')
	list_filter = ('tipe','merk')
	search_fields = ('mesin','tipe', 'PK', 'merk')

admin.site.register(MesinPerusahaan, MesinPerusahaanAdmin)

class AktaNotarisAdmin(admin.ModelAdmin):
	list_display = ('no_akta','tanggal_akta','jenis_akta')
	list_filter = ('no_akta','tanggal_akta')
	search_fields = ('no_akta','tanggal_akta','jenis_akta')

admin.site.register(AktaNotaris, AktaNotarisAdmin)

class ProdukUtamaAdmin(admin.ModelAdmin):
	list_display = ('perusahaan','kelembagaan','barang_jasa_utama')
	list_filter = ('barang_jasa_utama',)

admin.site.register(ProdukUtama, ProdukUtamaAdmin)

class MesinHullerAdmin(admin.ModelAdmin):
	list_display = ('jenis','mesin_huller')

admin.site.register(MesinHuller, MesinHullerAdmin)

class ModalKoprasiAdmin(admin.ModelAdmin):
	list_display = ('jenis_modal','modal_koprasi')

admin.site.register(ModalKoprasi, ModalKoprasiAdmin)

class NilaiModalAdmin(admin.ModelAdmin):
	list_display = ('perusahaan','modal', 'nilai')

admin.site.register(NilaiModal, NilaiModalAdmin)

class NilaiModalAdmin(admin.ModelAdmin):
	list_display = ('perusahaan','desa', 'alamat')

admin.site.register(LokasiUnitProduksi)

admin.site.register(JenisPengecer)
admin.site.register(KegiatanUsaha)
admin.site.register(StatusPerusahaan)
admin.site.register(JenisKerjasama)
admin.site.register(JenisBadanUsaha)
admin.site.register(JenisMesin)
admin.site.register(JenisModalKoprasi)
