from django.db import models
from master.models import Desa, AtributTambahan, Berkas, MetaAtribut
from accounts.utils import STATUS
# from perusahaan.utils import AKTA, KEDUDUKAN
# from accounts.models import IdentitasPribadi
from datetime import datetime
# from izin.models import DetilTDP
from accounts.models import IdentitasPribadi
# import json


# Create your models here.

class KBLI(MetaAtribut):
	kode_kbli = models.CharField(max_length=15, verbose_name='Kode KBLI')
	nama_kbli = models.CharField(max_length=255, verbose_name='Nama KBLI')
	versi = models.CharField(max_length=255, null=True, blank=True, verbose_name='Versi')
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % str(self.kode_kbli)

	def as_json(self):
		return dict(id=self.id, nama_kbli=self.nama_kbli, kode_kbli=self.kode_kbli)

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.kode_kbli)+str(self.nama_kbli)+"</option>"

	def as_dict(self):
		return {
			# "id": self.id,
			"kode_kbli": self.kode_kbli,
			"nama_kbli": self.nama_kbli,
		}

	class Meta:
		ordering = ['id']
		verbose_name = 'KBLI'
		verbose_name_plural = 'KBLI'

class JenisPerusahaan(models.Model):
	jenis_perusahaan = models.CharField(max_length=255, verbose_name='Jenis Perusahaan')
	keterangan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.jenis_perusahaan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Perusahaan'
		verbose_name_plural = 'Jenis Perusahaan'

class Kelembagaan(models.Model):
	kelembagaan = models.CharField(max_length=255, verbose_name='Nama Kelembagaan')
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.kelembagaan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Kelembagaan'
		verbose_name_plural = 'Kelembagaan'

# class ProdukUtama(models.Model):
# 	barang_jasa_utama = models.CharField(max_length=255, verbose_name='Barang / Jasa Utama')
# 	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

# 	def __unicode__(self):
# 		return "%s" % (self.barang_jasa_utama)

# 	def as_dict(self):
# 		return {
# 			# "id": self.id,
# 			"barang_jasa_utama": self.barang_jasa_utama,
# 		}

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Produk Utama'
# 		verbose_name_plural = 'Produk Utama'

class JenisPenanamanModal(models.Model):
	jenis_penanaman_modal = models.CharField(max_length=255, verbose_name='Jenis Penanaman Modal')
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.jenis_penanaman_modal)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Penanaman Modal'
		verbose_name_plural = 'Jenis Penanaman Modal'

# PERSEROAN TERBATAS (PT), PERSEKUTUAN KOMANDITER (CV), FIRMA, PERUSAHAAN PERORANGAN (PO), KOPERASI, BENTUK USAHA LAINNYA
class JenisBadanUsaha(models.Model):
	jenis_badan_usaha = models.CharField(max_length=255, verbose_name='Jenis Badan Usaha')
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.jenis_badan_usaha)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Badan Usaha'
		verbose_name_plural = 'Jenis Badan Usaha'

# mikro, kecil, menengah, besar untuk SIUP
class BentukKegiatanUsaha(models.Model):
	kegiatan_usaha = models.CharField(max_length=255, blank=True, null=True, verbose_name='Kegiatan Usaha')
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.kegiatan_usaha)

	class Meta:
		ordering = ['id']
		verbose_name = 'Kegiatan Usaha'
		verbose_name_plural = 'Kegiatan Usaha'

class Perusahaan(AtributTambahan):
	perusahaan_induk = models.ForeignKey('Perusahaan', related_name='izin_perusahaan_induk', blank=True, null=True) # contoh: Jika cabang, pusat nya dimasukkan juga
	perusahaan_lama = models.ForeignKey('Perusahaan', related_name='izin_perusahaan_lama', blank=True, null=True) # contoh: pengembangan CV ke PT

	nama_perusahaan = models.CharField(max_length=100, verbose_name='Nama Perusahaan')
	nama_grup = models.CharField(max_length=100, verbose_name='Nama Grup Perusahaan', blank=True, null=True)
	alamat_perusahaan = models.CharField(max_length=255,  verbose_name='Alamat Perusahaan')
	desa = models.ForeignKey(Desa, verbose_name='Desa')
	lt = models.CharField(max_length=100, blank=True, null=True, verbose_name='Latitute')
	lg = models.CharField(max_length=100, blank=True, null=True, verbose_name='Longitute')
	kode_pos = models.CharField(max_length=50, null=True, blank=True, verbose_name='Kode Pos')
	telepon = models.CharField(max_length=50, verbose_name='Telepon')
	fax = models.CharField(max_length=20, blank=True, null=True, verbose_name='Fax')
	email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='E-mail')
	npwp = models.CharField(max_length=100, verbose_name='NPWP', unique=True)
	berkas_npwp = models.ForeignKey(Berkas, verbose_name="Berkas NPWP", related_name='berkas_npwp_perusahaan', blank=True, null=True)
	penanggung_jawab = models.ForeignKey('izin.Pemohon', related_name='penanggung_jawab_perusahaan', blank=True, null=True)
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.nama_perusahaan)+"</option>"

	def __unicode__ (self):
		return "%s" % (self.nama_perusahaan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Perusahaan'
		verbose_name_plural = 'Perusahaan'

class JenisLegalitas(models.Model):
	jenis_legalitas = models.CharField(max_length=100, verbose_name='Jenis Legalitas')
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__ (self):
		return "%s" % (self.jenis_legalitas)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Legalitas'
		verbose_name_plural = 'Jenis Legalitas'

class Legalitas(AtributTambahan):
	perusahaan = models.ForeignKey(Perusahaan, verbose_name='Perusahaan')
	nama_notaris = models.CharField(max_length=100, verbose_name='Nama Notaris')
	jenis_legalitas = models.ForeignKey(JenisLegalitas, related_name='jenis_legalitas_perusahaan', blank=True, null=True)
	alamat = models.CharField(max_length=255, null=True, blank=True)
	telephone = models.CharField(verbose_name='Telepon', max_length=50, null=True, blank=True)
	nomor_akta = models.CharField("Nomor Akta", max_length=255, blank=True, null=True)
	tanggal_akta = models.DateField("Tanggal Akta", blank=True, null=True)
	nomor_pengesahan = models.CharField("Nomor Pengesahan", max_length=255, blank=True, null=True)
	tanggal_pengesahan = models.DateField("Tanggal Pengesahan", blank=True, null=True)
	berkas = models.ForeignKey(Berkas, verbose_name="Berkas", blank=True, null=True)
	keterangan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Keterangan")

	def __unicode__ (self):
		return "%s" % (str(self.jenis_legalitas))

	def as_dict(self):
		return {
			# "id": self.id,
			"jenis_legalitas": self.jenis_legalitas.jenis_legalitas,
			"nama_notaris": self.nama_notaris,
			"alamat": self.alamat,
			"telephone": self.telephone,
			"nomor_akta": self.nomor_akta,
			"tanggal_akta": self.tanggal_akta.strftime('%d-%m-%Y'),
			"nomor_pengesahan": self.nomor_pengesahan,
			"tanggal_pengesahan": self.tanggal_pengesahan.strftime('%d-%m-%Y'),			
		}

	class Meta:
		ordering = ['id']
		verbose_name = 'Legalitas'
		verbose_name_plural = 'Legalitas'

# TDP PT
class JenisPengecer(models.Model):
	jenis_pengecer = models.CharField(max_length=255, verbose_name='Jenis Pengecer')
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.jenis_pengecer)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Pengecer'
		verbose_name_plural = 'Jenis Pengecer'

class KedudukanKegiatanUsaha(models.Model):
	kedudukan_kegiatan_usaha = models.CharField(max_length=255, verbose_name='Kedudukan Kegiatan Usaha')
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.kedudukan_kegiatan_usaha)

	class Meta:
		ordering = ['id']
		verbose_name = 'Kedudukan Kegiatan Usaha'
		verbose_name_plural = 'Kedudukan Kegiatan Usaha'

class StatusPerusahaan(models.Model):
	status_perusahaan = models.CharField(max_length=255, verbose_name='Status Perusahaan')
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.status_perusahaan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Status Perusahaan'
		verbose_name_plural = 'Status Perusahaan'

class BentukKerjasama(models.Model):
	bentuk_kerjasama = models.CharField(max_length=255, verbose_name='Bentuk Kerjasama')
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.bentuk_kerjasama)

	class Meta:
		ordering = ['id']
		verbose_name = 'Bentuk Kerjasama'
		verbose_name_plural = 'Bentuk Kerjasama'

class JenisKedudukan(models.Model):
	kedudukan_pimpinan = models.CharField(max_length=255, verbose_name='Kedudukan')
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.kedudukan_pimpinan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Kedudukan'
		verbose_name_plural = 'Jenis Kedudukan'

class DataPimpinan(IdentitasPribadi):
	"""docstring for Data Pimpinan"""
	perusahaan = models.ForeignKey(Perusahaan, verbose_name='Perusahaan')
	kedudukan = models.ForeignKey(JenisKedudukan, verbose_name='Jenis Kedudukan')
	detil_tdp = models.ForeignKey('izin.DetilTDP', verbose_name='Detil TDP')
	tanggal_menduduki_jabatan = models.DateField(verbose_name='Tanggal Menduduki Jabatan')
	jumlah_saham_dimiliki = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Jumlah Saham Dimiliki')
	jumlah_saham_disetor = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Jumlah Saham Disetor')

	kedudukan_diperusahaan_lain = models.CharField(max_length=255, verbose_name='Kedudukan Di Perusahaan Lain')
	nama_perusahaan_lain = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nama Perusahaan Lain')
	alamat_perusahaan_lain = models.CharField(max_length=255, blank=True, null=True, verbose_name='Alamat Perusahaan Lain')
	kode_pos_perusahaan_lain = models.IntegerField(blank=True, null=True, verbose_name='Kode Pos Perusahaan Lain')
	telepon_perusahaan_lain = models.CharField(max_length=50, blank=True, null=True, verbose_name='Telepon Perusahaan Lain')
	tanggal_menduduki_jabatan_perusahaan_lain = models.DateField(blank=True, null=True, verbose_name=' Tanggal Menduduki Jabatan Di Perusahaan Lain')

	def __unicode__(self):
		return "%s" % (self.kedudukan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Data Pimpinan'
		verbose_name_plural = 'Data Pimpinan'

class PemegangSaham(IdentitasPribadi):
	"""docstring for Pemegang Saham"""
	npwp = models.CharField(max_length=100, verbose_name='NPWP', unique=True)
	jumlah_saham_dimiliki = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Jumlah Saham Dimiliki')
	jumlah_saham_disetor = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Jumlah Saham Disetor')

	def __unicode__(self):
		return "%s" % (self.npwp)

	class Meta:
		ordering = ['id']
		verbose_name = 'Pemegang Saham'
		verbose_name_plural = 'Pemegang Saham'

# class DataRincianPerusahaan(models.Model):
# 	"""docstring for Data Rincian Perusahaan"""
# 	perusahaan = models.ForeignKey(Perusahaan, verbose_name='Perusahaan')
# 	omset_per_tahun = models.IntegerField(blank=True, null=True, verbose_name='Omset Per Tahun')
# 	total_aset = models.IntegerField(blank=True, null=True, verbose_name='Total Aset')
# 	jumlah_karyawan_wni = models.IntegerField(blank=True, null=True, verbose_name='Jumlah Karyawan WNI')
# 	jumlah_karyawan_wna = models.IntegerField(blank=True, null=True, verbose_name='Jumlah Karyawan WNA')

# 	kapasitas_mesin_terpasang = models.IntegerField(blank=True, null=True, verbose_name='Kapasitas Mesin Terpasang')
# 	stuan_kapasitas_msin_terpasang = models.CharField(max_length=10,blank=True, null=True, verbose_name='Satuan Kapasitas Mesin Terpasang')
# 	kapasitas_produksi_pertahun = models.IntegerField(blank=True, null=True, verbose_name='Kapasitas Produksi Per Tahun')
# 	stuan_kapasitas_produksi = models.CharField(blank=True, null=True, max_length=255, verbose_name='Satuan Kapasitas Produksi')

# 	jenis_kegiatan = models.ForeignKey(JenisKegiatanUsaha, blank=True, null=True, verbose_name='Jenis Kegiatan Usaha')
# 	kegiatan_usaha = models.ForeignKey(KegiatanUsaha, blank=True, null=True, verbose_name='Kegiatan Usaha')
# 	pengecer = models.ForeignKey(JenisPengecer, blank=True, null=True, verbose_name='Jenis Pengecer')
# 	presentase_kandungan_komponen_produk_lokal = models.DecimalField(max_digits=5, decimal_places=2,blank=True, null=True, verbose_name='Presentase Kandungan Komponen Produk Lokal')
# 	presentase_kandungan_komponen_produk_import = models.DecimalField(max_digits=5, decimal_places=2,blank=True, null=True, verbose_name='Presentase Kandungan Komponen Produk Import')
	
# 	modal_dasar = models.IntegerField(blank=True, null=True, verbose_name='Modal Dasar')
# 	modal_disetor = models.IntegerField(blank=True, null=True, verbose_name='Modal Disetor')
# 	modal_ditempatkan = models.IntegerField(blank=True, null=True, verbose_name='Modal Ditempatkan')
# 	jumlah_saham = models.IntegerField(blank=True, null=True, verbose_name='Jumlah Saham')
# 	nilai_saham_per_lembar = models.IntegerField(blank=True, null=True,verbose_name='Nilai Saham Per Lembar')

# 	def as_json(self):
# 		perusahaan = ''
# 		kegiatan_usaha = ''
# 		if self.perusahaan:
# 			perusahaan = self.perusahaan.nama_perusahaan
# 			if self.kegiatan_usaha:
# 				kegiatan_usaha = self.kegiatan_usaha.kegiatan_usaha

# 		return dict(id=self.id, perusahaan=self.perusahaan.nama_perusahaan,kegiatan_usaha=kegiatan_usaha)

# 	def __unicode__(self):
# 		return "%s" % str(self.omset_per_tahun)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Data Rincian Perusahaan'
# 		verbose_name_plural = 'Data Rincian Perusahaan'

# class PemegangSahamLain(IdentitasPribadi):
# 	perusahaan = models.ForeignKey(Perusahaan,blank=True, null=True, verbose_name='Perusahaan')
# 	npwp = models.IntegerField(blank=True, null=True, verbose_name='NPWP')
# 	jumlah_saham_dimiliki = models.IntegerField(blank=True, null=True, verbose_name='Jumlah Saham Dimiliki')
# 	jumlah_modal_disetor = models.IntegerField( blank=True, null=True, verbose_name='Jumlah Modal Disetor')

# 	def __unicode__(self):
# 		return "%s" % str(self.npwp)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Pemegang Saham Lain'
# 		verbose_name_plural = 'Pemegang Saham Lain'

# class JenisMesin(models.Model):
# 	jenis_mesin = models.CharField(max_length=255, blank=True, null=True, verbose_name='Jenis Mesin')

# 	def __unicode__(self):
# 		return "%s" % (self.jenis_mesin)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Jenis Mesin'
# 		verbose_name_plural = 'Jenis Mesin'

# class MesinHuller(models.Model):
# 	jenis = models.ForeignKey(JenisMesin,blank=True, null=True, verbose_name='Jenis Mesin')
# 	mesin_huller = models.CharField(max_length=255, blank=True, null=True, verbose_name='Mesin Huller')

# 	def __unicode__(self):
# 		return "%s" % (self.mesin_huller)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Mesin Huller'
# 		verbose_name_plural = 'Mesin Huller'

# class MesinPerusahaan(models.Model):
# 	perusahaan = models.ForeignKey(Perusahaan, blank=True, null=True, verbose_name='Perusahaan')
# 	mesin = models.ForeignKey(MesinHuller, blank=True, null=True, verbose_name='Mesin Huller')
# 	tipe = models.CharField(blank=True, null=True, max_length=255, verbose_name='Type')
# 	PK = models.CharField(blank=True, null=True, max_length=255, verbose_name='PK')
# 	kapasitas = models.IntegerField(blank=True, null=True, verbose_name='Kapasitas')
# 	merk = models.CharField(blank=True, null=True, max_length=255, verbose_name='Merk')
# 	jumlah_unit = models.CharField(blank=True, null=True, max_length=255, verbose_name='Jumlah Unit')

# 	def __unicode__(self):
# 		return "%s" % (self.tipe)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = ' Mesin Perusahaan'
# 		verbose_name_plural = 'Mesin Perusahaan'


# class AktaNotaris(models.Model):
# 	perusahaan = models.ForeignKey(Perusahaan,blank=True, null=True, verbose_name='Perusahaan')
# 	no_akta = models.CharField(max_length=255, blank=True, null=True, verbose_name='No Akta')
# 	tanggal_akta = models.DateField( blank=True, null=True, verbose_name='Tanggal Akta')
# 	no_pengesahan = models.CharField(max_length=255, blank=True, null=True, verbose_name='No Pengesahan')
# 	tanggal_pengesahan = models.DateField(blank=True, null=True, verbose_name='Tanggal Pengesahan')
# 	jenis_akta = models.CharField(blank=True, null=True, max_length=20, verbose_name='Jenis Akta', choices=AKTA, default=1)

# 	def as_json(self):
# 		perusahaan = ''
# 		tanggal_pengesahan = ''
# 		tanggal_akta = ''
# 		if self.perusahaan:
# 			perusahaan = self.perusahaan.nama_perusahaan
# 			if self.tanggal_pengesahan:
# 				tanggal_pengesahan = self.tanggal_pengesahan.strftime("%d-%m-%Y")
# 				if self.tanggal_akta:
# 					tanggal_akta = self.tanggal_akta.strftime("%d-%m-%Y")

# 		return dict(id=self.id, perusahaan=self.perusahaan.nama_perusahaan, no_akta=self.no_akta, 
# 			tanggal_akta=tanggal_akta, no_pengesahan=self.no_pengesahan,tanggal_pengesahan=tanggal_pengesahan)

# 	def as_option(self):
# 		return "<option value='"+str(self.id)+"'>"+str(self.no_akta)+"</option>"

# 	def __unicode__(self):
# 		return "%s" % (self.no_akta + " (" + str(self.perusahaan) + ")")

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Akta Notaris'
# 		verbose_name_plural = 'Akta Notaris'

# class JenisModalKoprasi(models.Model):
# 	jenis_modal_koprasi = models.CharField(max_length=255, blank=True, null=True, verbose_name='Jenis Modal Koprasi')

# 	def __unicode__(self):
# 		return "%s" % (self.jenis_modal_koprasi)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Jenis Modal Koprasi'
# 		verbose_name_plural = 'Jenis Modal Koprasi'

# class ModalKoprasi(models.Model):
# 	jenis_modal = models.ForeignKey(JenisModalKoprasi, blank=True, null=True, verbose_name='Jenis Modal Koprasi')
# 	modal_koprasi = models.CharField(max_length=255, blank=True, null=True, verbose_name='Modal Koprasi')

# 	def __unicode__(self):
# 		return "%s" % (self.modal_koprasi)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Modal Koprasi'
# 		verbose_name_plural = 'Modal Koprasi'

# class NilaiModal(models.Model):
# 	perusahaan = models.ForeignKey(Perusahaan,blank=True, null=True, verbose_name='Perusahaan')
# 	modal = models.ForeignKey(ModalKoprasi, blank=True, null=True, verbose_name='Modal Koprasi')
# 	nilai = models.IntegerField(blank=True, null=True, verbose_name='Modal Koprasi')

# 	def __unicode__(self):
# 		return "%s" % str(self.nilai)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Nilai Modal'
# 		verbose_name_plural = 'Nilai Modal'

# class LokasiUnitProduksi(models.Model):
# 	perusahaan = models.ForeignKey(Perusahaan,blank=True, null=True, verbose_name='Perusahaan')
# 	desa = models.ForeignKey(Desa,blank=True, null=True,  verbose_name='Desa')
# 	alamat = models.CharField(blank=True, null=True, max_length=255, verbose_name='Alamat')

# 	def __unicode__(self):
# 		return "%s" % (self.alamat)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Lokasi Unit Perusahaan'
# 		verbose_name_plural = 'Lokasi Unit Perusahaan'


# # END OF Models Perusahaan #


