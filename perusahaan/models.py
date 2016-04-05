from accounts.utils import STATUS
from perusahaan.utils import AKTA, KEDUDUKAN

from master.models import Desa
from accounts.models import IdentitasPribadi

from datetime import datetime
from django.db import models


# Create your models here.

class JenisPenanamanModal(models.Model):
	jenis_penanaman_modal = models.CharField(max_length=255, blank=True, null=True, verbose_name='Jenis Penanaman Modal')

	def __unicode__(self):
		return "%s" % (self.jenis_penanaman_modal)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Penanaman Modal'
		verbose_name_plural = 'Jenis Penanaman Modal'

class JenisPerusahaan(models.Model):
	jenis_perusahaan = models.CharField(max_length=255, blank=True, null=True, verbose_name='Jenis Perusahaan')

	def __unicode__(self):
		return "%s" % (self.jenis_perusahaan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Perusahaan'
		verbose_name_plural = 'Jenis Perusahaan'

class KBLI(models.Model):
	kode_kbli = models.IntegerField(blank=True, null=True, verbose_name='Kode KBLI')
	nama_kbli = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nama KBLI')

	def __unicode__(self):
		return "%s" % str(self.kode_kbli)

	class Meta:
		ordering = ['id']
		verbose_name = 'KBLI'
		verbose_name_plural = 'KBLI'

class StatusPerusahaan(models.Model):
	status_perusahaan = models.CharField(max_length=255, blank=True, null=True, verbose_name='Status Perusahaan')

	def __unicode__(self):
		return "%s" % (self.status_perusahaan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Status Perusahaan'
		verbose_name_plural = 'Status Perusahaan'


class JenisKerjasama(models.Model):
	jenis_kerjasama = models.CharField(max_length=255,blank=True, null=True, verbose_name='Jenis Kerjasama')

	def __unicode__(self):
		return "%s" % (self.jenis_kerjasama)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Kerjasama'
		verbose_name_plural = 'Jenis Kerjasama'

class JenisBadanUsaha(models.Model):
	jenis_badan_usaha = models.CharField(max_length=255,blank=True, null=True, verbose_name='Jenis Badan Usaha')

	def __unicode__(self):
		return "%s" % (self.jenis_badan_usaha)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Badan Usaha'
		verbose_name_plural = 'Jenis Badan Usaha'

class Perusahaan(models.Model):
	"""docstring for Perusahaan"""
	perusahaan_induk = models.ForeignKey('Perusahaan', blank=True, null=True)
	nama_perusahaan = models.CharField(max_length=100, verbose_name='Nama Perusahaan')
	alamat_perusahaan = models.CharField(max_length=255,  blank=True, null=True, verbose_name='Alamat Perusahaan')
	lt = models.CharField(max_length=100, null=True, verbose_name='Latitute')
	lg = models.CharField(max_length=100, null=True, verbose_name='Longitute')
	kode_pos = models.IntegerField(verbose_name='Kode Pos')
	telepon = models.CharField(max_length=50, blank=True, null=True, verbose_name='Telepon')
	fax = models.CharField(max_length=20, verbose_name='Fax')
	email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='E-mail')

	jenis_perusahaan = models.ForeignKey(JenisPerusahaan, blank=True, null=True, verbose_name='Jenis Perusahaan')
	kbli = models.ForeignKey(KBLI, blank=True, null=True, verbose_name='KBLI')
	nama_kelompok_perusahaan = models.CharField(max_length=100, verbose_name='Nama Kelompok Perusahaan')
	nasabah_utama_bank1 = models.CharField(max_length=255, verbose_name='Nasabah Utama Bank 1')
	nasabah_utama_bank2 = models.CharField(max_length=255, verbose_name='Nasabah Utama Bank 2')
	jumlah_bank = models.IntegerField(verbose_name='Jumlah Bank')
	npwp = models.IntegerField(blank=True, null=True, verbose_name='NPWP')
	
	tanggal_pendirian = models.DateField(verbose_name='Tanggal Pendirian')
	tanggal_mulai_kegiatan = models.DateField(verbose_name='Tanggal Mulai Kegiatan')
	merk_dagang = models.CharField(max_length=255, verbose_name='Merk Dagang')
	pemegang_hak_paten = models.CharField(max_length=255, verbose_name='Pemegang Hak Paten')
	pemegang_hak_cipta = models.CharField(max_length=255, verbose_name='Pemegang Hak Cipta')

	penanaman_modal = models.ForeignKey(JenisPenanamanModal, blank=True, null=True, verbose_name='Jenis Penanaman Modal')
	status_perusahaan = models.ForeignKey(StatusPerusahaan, blank=True, null=True, verbose_name='Status Perusahaan')
	kerjasama = models.ForeignKey(JenisKerjasama, blank=True, null=True, verbose_name='Jenis Kerjasama')
	badan_usaha = models.ForeignKey(JenisBadanUsaha, blank=True, null=True, verbose_name='Jenis Badan Usaha')

	status = models.PositiveSmallIntegerField(verbose_name='Status Data', choices=STATUS, default=1)
	created_at = models.DateTimeField(editable=False)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__ (self):
		return "%s" % (self.nama_perusahaan)

	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.created_at = datetime.now()
		self.updated_at = datetime.now()
		return super(Perusahaan, self).save(*args, **kwargs)

	class Meta:
		ordering = ['id']
		verbose_name = 'Perusahaan'
		verbose_name_plural = 'Perusahaan'

class JenisKedudukan(models.Model):
	kedudukan = models.CharField(max_length=50, choices=KEDUDUKAN, default=1 ,blank=True, null=True, verbose_name='Kedudukan')

	def __unicode__(self):
		return "%s" % (self.kedudukan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Kedudukan'
		verbose_name_plural = 'Jenis Kedudukan'

class DataPimpinan(IdentitasPribadi):
	"""docstring for Data Pimpinan"""
	perusahaan = models.ForeignKey(Perusahaan, verbose_name='Perusahaan')
	kedudukan = models.ForeignKey(JenisKedudukan, verbose_name='Jenis Kedudukan')
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


class JenisKegiatanUsaha(models.Model):
	jenis_kegiatan_usaha = models.CharField(max_length=255, blank=True, null=True, verbose_name='Jenis Kegiatan Usaha')

	def __unicode__(self):
		return "%s" % (self.jenis_kegiatan_usaha)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Kegiatan Usaha'
		verbose_name_plural = 'Jenis Kegiatan Usaha'

class JenisPengecer(models.Model):
	jenis_pengecer = models.CharField(max_length=255, blank=True, null=True, verbose_name='Jenis Pengecer')

	def __unicode__(self):
		return "%s" % (self.jenis_pengecer)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Pengecer'
		verbose_name_plural = 'Jenis Pengecer'

class KegiatanUsaha(models.Model):
	kegiatan_usaha = models.CharField(max_length=255, blank=True, null=True, verbose_name='Kegiatan Usaha')

	def __unicode__(self):
		return "%s" % (self.kegiatan_usaha)

	class Meta:
		ordering = ['id']
		verbose_name = 'Kegiatan Usaha'
		verbose_name_plural = 'Kegiatan Usaha'


class DataRincianPerusahaan(models.Model):
	"""docstring for Data Rincian Perusahaan"""
	perusahaan = models.ForeignKey(Perusahaan, verbose_name='Perusahaan')
	omset_per_tahun = models.IntegerField(blank=True, null=True, verbose_name='Omset Per Tahun')
	total_aset = models.IntegerField(verbose_name='Total Aset')
	jumlah_karyawan_wni = models.IntegerField(verbose_name='Jumlah Karyawan WNI')
	jumlah_karyawan_wna = models.IntegerField(verbose_name='Jumlah Karyawan WNA')

	kapasitas_mesin_terpasang = models.IntegerField(verbose_name='Kapasitas Mesin Terpasang')
	stuan_kapasitas_msin_terpasang = models.CharField(max_length=10, verbose_name='Satuan Kapasitas Mesin Terpasang')
	kapasitas_produksi_pertahun = models.IntegerField(verbose_name='Kapasitas Produksi Per Tahun')
	stuan_kapasitas_produksi = models.CharField(max_length=255, verbose_name='Satuan Kapasitas Produksi')

	jenis_kegiatan = models.ForeignKey(JenisKegiatanUsaha, blank=True, null=True, verbose_name='Jenis Kegiatan Usaha')
	kegiatan_usaha = models.ForeignKey(KegiatanUsaha, blank=True, null=True, verbose_name='Kegiatan Usaha')
	pengecer = models.ForeignKey(JenisPengecer, blank=True, null=True, verbose_name='Jenis Pengecer')
	presentase_kandungan_komponen_produk_lokal = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Presentase Kandungan Komponen Produk Lokal')
	presentase_kandungan_komponen_produk_import = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Presentase Kandungan Komponen Produk Import')
	
	modal_dasar = models.IntegerField(verbose_name='Modal Dasar')
	modal_disetor = models.IntegerField(verbose_name='Modal Disetor')
	modal_ditempatkan = models.IntegerField(verbose_name='Modal Ditempatkan')
	jumlah_saham = models.IntegerField(verbose_name='Jumlah Saham')
	nilai_saham_per_lembar = models.IntegerField(verbose_name='Nilai Saham Per Lembar')

	def __unicode__(self):
		return "%s" % str(self.omset_per_tahun)

	class Meta:
		ordering = ['id']
		verbose_name = 'Data Rincian Perusahaan'
		verbose_name_plural = 'Data Rincian Perusahaan'

class PemegangSahamLain(IdentitasPribadi):
	perusahaan = models.ForeignKey(Perusahaan, verbose_name='Perusahaan')
	npwp = models.IntegerField(blank=True, null=True, verbose_name='NPWP')
	jumlah_saham_dimiliki = models.IntegerField(verbose_name='Jumlah Saham Dimiliki')
	jumlah_modal_disetor = models.IntegerField(verbose_name='Jumlah Modal Disetor')

	def __unicode__(self):
		return "%s" % str(self.npwp)

	class Meta:
		ordering = ['id']
		verbose_name = 'Pemegang Saham Lain'
		verbose_name_plural = 'Pemegang Saham Lain'

class Kelembagaan(models.Model):
	nama_kelembagaan = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nama Kelembagaan')

	def __unicode__(self):
		return "%s" % (self.nama_kelembagaan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Kelembagaan'
		verbose_name_plural = 'Kelembagaan'

class ProdukUtama(models.Model):
	perusahaan = models.ForeignKey(Perusahaan, verbose_name='Perusahaan')
	kelembagaan = models.ForeignKey(Kelembagaan, verbose_name='Kelembagaan')
	barang_jasa_utama = models.CharField(max_length=255, verbose_name='Barang Jasa Utama')

	def __unicode__(self):
		return "%s" % (self.barang_jasa_utama)

	class Meta:
		ordering = ['id']
		verbose_name = 'Produk Utama'
		verbose_name_plural = 'Produk Utama'

class JenisMesin(models.Model):
	jenis_mesin = models.CharField(max_length=255, blank=True, null=True, verbose_name='Jenis Mesin')

	def __unicode__(self):
		return "%s" % (self.jenis_mesin)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Mesin'
		verbose_name_plural = 'Jenis Mesin'

class MesinHuller(models.Model):
	jenis = models.ForeignKey(JenisMesin, verbose_name='Jenis Mesin')
	mesin_huller = models.CharField(max_length=255, blank=True, null=True, verbose_name='Mesin Huller')

	def __unicode__(self):
		return "%s" % (self.mesin_huller)

	class Meta:
		ordering = ['id']
		verbose_name = 'Mesin Huller'
		verbose_name_plural = 'Mesin Huller'

class MesinPerusahaan(models.Model):
	perusahaan = models.ForeignKey(Perusahaan, verbose_name='Perusahaan')
	mesin = models.ForeignKey(MesinHuller, verbose_name='Mesin Huller')
	tipe = models.CharField(max_length=255, verbose_name='Type')
	PK = models.CharField(max_length=255, verbose_name='PK')
	kapasitas = models.IntegerField(verbose_name='Kapasitas')
	merk = models.CharField(max_length=255, verbose_name='Merk')
	jumlah_unit = models.CharField(max_length=255, verbose_name='Jumlah Unit')

	def __unicode__(self):
		return "%s" % (self.tipe)

	class Meta:
		ordering = ['id']
		verbose_name = ' Mesin Perusahaan'
		verbose_name_plural = 'Mesin Perusahaan'


class AktaNotaris(models.Model):
	perusahaan = models.ForeignKey(Perusahaan, verbose_name='Perusahaan')
	no_akta = models.CharField(max_length=255, blank=True, null=True, verbose_name='No Akta')
	tanggal_akta = models.DateField( blank=True, null=True, verbose_name='Tanggal Akta')
	no_pengesahan = models.CharField(max_length=255, blank=True, null=True, verbose_name='No Pengesahan')
	tanggal_pengesahan = models.DateField(verbose_name='Tanggal Pengesahan')
	jenis_akta = models.CharField(max_length=20, verbose_name='Jenis Akta', choices=AKTA, default=1)

	def __unicode__(self):
		return "%s" % (self.no_akta)

	class Meta:
		ordering = ['id']
		verbose_name = 'Akta Notaris'
		verbose_name_plural = 'Akta Notaris'

class JenisModalKoprasi(models.Model):
	jenis_modal_koprasi = models.CharField(max_length=255, blank=True, null=True, verbose_name='Jenis Modal Koprasi')

	def __unicode__(self):
		return "%s" % (self.jenis_modal_koprasi)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Modal Koprasi'
		verbose_name_plural = 'Jenis Modal Koprasi'

class ModalKoprasi(models.Model):
	jenis_modal = models.ForeignKey(JenisModalKoprasi, verbose_name='Jenis Modal Koprasi')
	modal_koprasi = models.CharField(max_length=255, blank=True, null=True, verbose_name='Modal Koprasi')

	def __unicode__(self):
		return "%s" % (self.modal_koprasi)

	class Meta:
		ordering = ['id']
		verbose_name = 'Modal Koprasi'
		verbose_name_plural = 'Modal Koprasi'

class NilaiModal(models.Model):
	perusahaan = models.ForeignKey(Perusahaan, verbose_name='Perusahaan')
	modal = models.ForeignKey(ModalKoprasi, verbose_name='Modal Koprasi')
	nilai = models.IntegerField(verbose_name='Modal Koprasi')

	def __unicode__(self):
		return "%s" % str(self.nilai)

	class Meta:
		ordering = ['id']
		verbose_name = 'Nilai Modal'
		verbose_name_plural = 'Nilai Modal'

class LokasiUnitProduksi(models.Model):
	perusahaan = models.ForeignKey(Perusahaan, verbose_name='Perusahaan')
	desa = models.ForeignKey(Desa, verbose_name='Desa')
	alamat = models.CharField(max_length=255, verbose_name='Alamat')

	def __unicode__(self):
		return "%s" % (self.alamat)

	class Meta:
		ordering = ['id']
		verbose_name = 'Lokasi Unit Perusahaan'
		verbose_name_plural = 'Lokasi Unit Perusahaan'


# END OF Models Perusahaan #


