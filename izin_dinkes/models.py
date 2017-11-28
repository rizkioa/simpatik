from django.db import models
from izin.models import PengajuanIzin
from master.models import Desa

# Pengajuan Apotik
class Sarana(models.Model):
	nama_sarana = models.CharField(verbose_name='Nama Sarana', max_length=100)
	keterangan = models.CharField(verbose_name='Keterangan', max_length=100, null=True, blank=True)

	def __unicode__(self):
		return u'%s' % str(self.nama_sarana)

	class Meta:
		verbose_name = 'Sarana'
		verbose_name_plural = 'Sarana'

class Apotek(PengajuanIzin):
	nama_apotek = models.CharField(verbose_name='Nama Apotek', max_length=100, null=True, blank=True)
	alamat_apotek = models.CharField(verbose_name='Alamat Apotek', max_length=256, null=True, blank=True)
	desa = models.ForeignKey(Desa, verbose_name='Desa', null=True, blank=True)
	no_telepon = models.CharField(verbose_name='No Telepon', max_length=100, null=True, blank=True)
	sarana = models.ForeignKey(Sarana, verbose_name="Sarana", null=True, blank=True)
	nama_pemilik_sarana = models.CharField(verbose_name='Nama Pemilik Sarana', max_length=100, null=True, blank=True)
	alamat_sarana = models.CharField(verbose_name='Alamat Sarana', max_length=100, null=True, blank=True)
	npwp = models.CharField(verbose_name='NPWP', max_length=100, null=True, blank=True)

	def __unicode__(self):
		return u'%s' % str(self.nama_apotek)

	class Meta:
		verbose_name = 'Apotek'
		verbose_name_plural = 'Apotek'
# Pengajuan Apotik

class TokoObat(PengajuanIzin):
	nama_toko_obat = models.CharField(verbose_name='Nama Toko Obat', max_length=100, null=True, blank=True)
	nama_ttk_penanggung_jawab = models.CharField(verbose_name='Nama TTK Penanggung Jawab', max_length=100, null=True, blank=True)
	alamat_ttk = models.CharField(verbose_name='Alamat TTK', max_length=100, null=True, blank=True)
	alamat_tempat_usaha = models.CharField(verbose_name='Alamat Tempat Usaha', max_length=100, null=True, blank=True)

	def __unicode__(self):
		return u'%s' % str(self.nama_toko_obat)

	def as_json__toko_obat(self):
		return dict(nama_toko_obat=self.nama_toko_obat, nama_ttk_penanggung_jawab=self.nama_ttk_penanggung_jawab, alamat_ttk=self.alamat_ttk, alamat_tempat_usaha=self.alamat_tempat_usaha)

	class Meta:
		verbose_name = 'Toko Obat'
		verbose_name_plural = 'Toko Obat'

class Laboratorium(PengajuanIzin):
	klasifikasi_laboratorium = models.CharField(verbose_name='Klasifikasi Laboratorium', max_length=256)
	nama_laboratorium = models.CharField(verbose_name='Nama Laboratorium', max_length=256)
	alamat_laboratorium = models.CharField(verbose_name='Alamat Laboratorium', max_length=256)
	penanggung_jawab_teknis = models.CharField(verbose_name='Penanggung Jawab Teknis', max_length=256)

	def __unicode__(self):
		return u'%s' % str(self.nama_laboratorium)

	class Meta:
		verbose_name = 'Laboratorium'
		verbose_name_plural = 'Laboratorium'

class PeralatanLaboratorium(models.Model):
	laboratorium = models.ForeignKey(Laboratorium, verbose_name='Laboratorium')
	jenis_peralatan = models.CharField(verbose_name='Jenis Peralatan', max_length=256)
	jumlah = models.CharField(verbose_name='Jumlah', max_length=256)
	keterangan = models.CharField(verbose_name='Keterangan', max_length=100, null=True, blank=True)

	def __unicode__(self):
		return u'%s' % str(self.jenis_peralatan)

	class Meta:
		verbose_name = 'Laboratorium'
		verbose_name_plural = 'Laboratorium'

class JenisKelengkapanBangunan(models.Model):
	nama_jenis_kelengkapan_bangunan = models.CharField(verbose_name='Nama Jenis Kelengkapan Bangunan', max_length=256)
	keterangan = models.CharField(verbose_name='Keterangan', max_length=100, null=True, blank=True)

	def __unicode__(self):
		return u'%s' % str(self.nama_kelengkapan_bangunan)

	class Meta:
		verbose_name = 'Nama Kelengkapan Bangunan'
		verbose_name_plural = 'Nama Kelengkapan Bangunan'

class BangunanLaboratorium(models.Model):
	laboratorium = models.ForeignKey(Laboratorium, verbose_name='Laboratorium')
	jenis_kelengkapan_bangunan = models.ForeignKey(JenisKelengkapanBangunan, verbose_name='Jenis Kelegkapan Bangunan')
	nama_kelengkapan_bangunan = models.CharField(verbose_name='Nama Kelengkapan Bangunan', max_length=256)
	keterangan = models.CharField(verbose_name='Keterangan', max_length=100, null=True, blank=True)


	def __unicode__(self):
		return u'%s' % str(self.nama_kelengkapan_bangunan)

	class Meta:
		verbose_name = 'Bangunan Laboratorium'
		verbose_name_plural = 'Bangunan Laboratorium'


class PenutupanApotek(PengajuanIzin):
	nama_apotek = models.CharField(verbose_name='Nama Apotek', max_length=256)
	alamat_apotek = models.CharField(verbose_name='Alamat Apotek', max_length=256)
	no_telepon = models.CharField(verbose_name='No Telepon', max_length=256)
	no_sia = models.CharField(verbose_name='No SIA', max_length=256)
	nama_pemilik_sarana = models.CharField(verbose_name='Nama Pemilik Sarana', max_length=256)
	alamat_sarana = models.CharField(verbose_name='Alamat Sarana', max_length=256)

	def __unicode__(self):
		return u'%s' % str(self.nama_apotik)

	class Meta:
		verbose_name = 'Penutupan Apotik'
		verbose_name_plural = 'Penutupan Apotik'

class PengunduranApoteker(models.Model):
	nama_apotek = models.ForeignKey(PenutupanApotek, verbose_name='Nama Apotek')
	nama_apoteker = models.CharField(verbose_name='Nama Apoteker', max_length=256)
	tempat_lahir = models.CharField(verbose_name='Tempat Lahir', max_length=256)
	tanggal_lahir = models.DateField(verbose_name='Tanggal Lahir', max_length=256)
	alamat_apoteker = models.CharField(verbose_name='Alamat Apoteker', max_length=256)
	telepon_apoteker = models.CharField(verbose_name='Telepon Apoteker', max_length=256)
	keterangan = models.CharField(verbose_name='Keterangan', max_length=100, null=True, blank=True)

	def __unicode__(self):
		return u'%s' % str(self.nama_apoteker)

	class Meta:
		verbose_name = 'Pengunduran Apoteker'
		verbose_name_plural = 'Pengunduran Apoteker'

class Optikal(PengajuanIzin):
	nama_optikal = models.CharField(verbose_name='Nama Optikal', max_length=256)
	nama_pemilik_perusahaan = models.CharField(verbose_name='Nama Pemilik / Perusahaan', max_length=256)
	jenis_badan_usaha = models.CharField(verbose_name='Jenis Badan Usaha', max_length=256)
	alamat_usaha = models.CharField(verbose_name='Alamat Perusahaan / Usaha', max_length=256)
	no_telepon = models.CharField(verbose_name='No Telepon', max_length=256)
	jenis_kegiatan_usaha = models.CharField(verbose_name='Jenis Kegiatan Usaha', max_length=256)
	lokasi_kegiatan_usaha = models.CharField(verbose_name='Lokasi Kegiatan Usaha', max_length=256)
	luas_tanah_bangunan = models.CharField(verbose_name='Luas Tanah / Bangunan', max_length=256)

	def __unicode__(self):
		return u'%s' % str(self.nama_optikal)

	class Meta:
		verbose_name = 'Optikal'
		verbose_name_plural = 'Optikal'

