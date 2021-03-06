from django.db import models
from izin.models import PengajuanIzin
from master.models import Desa
from perusahaan.models import Perusahaan

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
	no_stra = models.CharField(verbose_name='No STRA', max_length=100, null=True, blank=True)
	no_sipa = models.CharField(verbose_name='No SIPA', max_length=100, null=True, blank=True)
	sarana = models.ForeignKey(Sarana, verbose_name="Sarana", null=True, blank=True)
	nama_pemilik_sarana = models.CharField(verbose_name='Nama Pemilik Sarana', max_length=100, null=True, blank=True)
	alamat_sarana = models.CharField(verbose_name='Alamat Sarana', max_length=100, null=True, blank=True)
	npwp = models.CharField(verbose_name='NPWP', max_length=100, null=True, blank=True)

	def as_json(self):
		alamat_lengkap = ''
		if self.desa and self.alamat_apotek:
			alamat_lengkap = str(self.alamat_apotek)+self.desa.lokasi_lengkap()
		desa = ''
		if self.desa:
			desa = self.desa.as_json()
		sarana = ''
		if self.sarana:
			sarana = self.sarana.nama_sarana

		return dict(nama_apotek=self.nama_apotek, no_stra=self.no_stra, no_sipa=self.no_sipa, alamat_apotek=alamat_lengkap, desa=desa, no_telepon=self.no_telepon, sarana=sarana, nama_pemilik_sarana=self.nama_pemilik_sarana, alamat_sarana=self.alamat_sarana, npwp=self.npwp)

	def __unicode__(self):
		return u'%s' % str(self.nama_apotek)

	class Meta:
		verbose_name = 'Apotek'
		verbose_name_plural = 'Apotek'
# Pengajuan Apotik

class TokoObat(PengajuanIzin):
	nama_toko_obat = models.CharField(verbose_name='Nama Toko Obat', max_length=100, null=True, blank=True)
	no_sipttk = models.CharField(verbose_name='Nomor Izin TTK', max_length=100, null=True, blank=True)
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
	nama_laboratorium = models.CharField(verbose_name='Nama Laboratorium', max_length=256, null=True, blank=True)
	alamat_laboratorium = models.CharField(verbose_name='Alamat Laboratorium', max_length=256, null=True, blank=True)
	desa = models.ForeignKey(Desa, verbose_name='Desa', null=True, blank=True)
	penanggung_jawab_teknis = models.CharField(verbose_name='Penanggung Jawab Teknis', max_length=256, null=True, blank=True)

	def as_json(self):
		alamat_lengkap = ''
		if self.desa and self.alamat_laboratorium:
			alamat_lengkap = str(self.alamat_laboratorium)+self.desa.lokasi_lengkap()
		desa = ''
		if self.desa:
			desa = self.desa.as_json()

		return dict(klasifikasi_laboratorium=self.klasifikasi_laboratorium, nama_laboratorium=self.nama_laboratorium, alamat_laboratorium=alamat_lengkap, desa=desa, penanggung_jawab_teknis=self.penanggung_jawab_teknis)

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

	def as_json(self):
		laboratorium = ''
		if self.laboratorium:
			laboratorium = self.laboratorium.nama_laboratorium
		return dict(id=self.id, laboratorium=laboratorium, jenis_peralatan=self.jenis_peralatan, jumlah=self.jumlah, keterangan=self.keterangan)

	def __unicode__(self):
		return u'%s' % str(self.jenis_peralatan)

	class Meta:
		verbose_name = 'Laboratorium'
		verbose_name_plural = 'Laboratorium'

class JenisKelengkapanBangunan(models.Model):
	nama_jenis_kelengkapan_bangunan = models.CharField(verbose_name='Nama Jenis Kelengkapan Bangunan', max_length=256)
	keterangan = models.CharField(verbose_name='Keterangan', max_length=100, null=True, blank=True)

	def __unicode__(self):
		return u'%s' % str(self.nama_jenis_kelengkapan_bangunan)

	class Meta:
		verbose_name = 'Nama Kelengkapan Bangunan'
		verbose_name_plural = 'Nama Kelengkapan Bangunan'

class BangunanLaboratorium(models.Model):
	laboratorium = models.ForeignKey(Laboratorium, verbose_name='Laboratorium')
	jenis_kelengkapan_bangunan = models.ForeignKey(JenisKelengkapanBangunan, verbose_name='Jenis Kelegkapan Bangunan', null=True, blank=True)
	nama_kelengkapan_bangunan = models.CharField(verbose_name='Nama Kelengkapan Bangunan', max_length=256, null=True, blank=True)
	keterangan = models.CharField(verbose_name='Keterangan', max_length=100, null=True, blank=True)

	def as_json(self):
		laboratorium = ''
		if self.laboratorium:
			laboratorium = self.laboratorium.nama_laboratorium
		if self.jenis_kelengkapan_bangunan:
			jenis_kelengkapan_bangunan_id = self.jenis_kelengkapan_bangunan.id
		if self.jenis_kelengkapan_bangunan:
			jenis_kelengkapan_bangunan = self.jenis_kelengkapan_bangunan.nama_jenis_kelengkapan_bangunan

		return dict(id=self.id, laboratorium=laboratorium, jenis_kelengkapan_bangunan_id=jenis_kelengkapan_bangunan_id, jenis_kelengkapan_bangunan=jenis_kelengkapan_bangunan, nama_kelengkapan_bangunan=self.nama_kelengkapan_bangunan, keterangan=self.keterangan)

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

	def as_json__penutupan_apotek(self):
		return dict(nama_apotek=self.nama_apotek, alamat_apotek=self.alamat_apotek, no_telepon=self.no_telepon, no_sia=self.no_sia, nama_pemilik_sarana=self.nama_pemilik_sarana, alamat_sarana=self.alamat_sarana)

	def __unicode__(self):
		return u'%s' % str(self.nama_apotek)

	class Meta:
		verbose_name = 'Penutupan Apotik'
		verbose_name_plural = 'Penutupan Apotik'

class PengunduranApoteker(models.Model):
	nama_apotek = models.ForeignKey(PenutupanApotek, verbose_name='Nama Apotek')
	nama_apoteker = models.CharField(verbose_name='Nama Apoteker', max_length=256)
	tempat_lahir = models.CharField(verbose_name='Tempat Lahir', max_length=256)
	tanggal_lahir = models.DateField(verbose_name='Tanggal Lahir', max_length=256, null=True, blank=True)
	alamat_apoteker = models.CharField(verbose_name='Alamat Apoteker', max_length=256)
	telepon_apoteker = models.CharField(verbose_name='Telepon Apoteker', max_length=256)
	keterangan = models.CharField(verbose_name='Keterangan', max_length=100, null=True, blank=True)

	def as_json__pengunduran_apoteker(self):
		if self.tanggal_lahir:
			tanggal_lahir = self.tanggal_lahir.strftime('%d-%m-%Y')
		return dict(id=self.id, nama_apotek=self.nama_apotek.nama_apotek, nama_apoteker=self.nama_apoteker, tempat_lahir=self.tempat_lahir, tanggal_lahir=tanggal_lahir, alamat_apoteker=self.alamat_apoteker, telepon_apoteker=self.telepon_apoteker, keterangan=self.keterangan)

	def __unicode__(self):
		return u'%s' % str(self.nama_apoteker)

	class Meta:
		verbose_name = 'Pengunduran Apoteker'
		verbose_name_plural = 'Pengunduran Apoteker'

class Optikal(PengajuanIzin):
	nama_optikal = models.CharField(verbose_name='Nama Optikal', max_length=256, null=True, blank=True)
	nama_pemilik_perusahaan = models.CharField(verbose_name='Nama Pemilik / Perusahaan', max_length=256, null=True, blank=True)
	jenis_badan_usaha = models.CharField(verbose_name='Jenis Badan Usaha', max_length=256, null=True, blank=True)
	alamat_usaha = models.CharField(verbose_name='Alamat Perusahaan / Usaha', max_length=256, null=True, blank=True)
	no_telepon = models.CharField(verbose_name='No Telepon', max_length=256, null=True, blank=True)
	jenis_kegiatan_usaha = models.CharField(verbose_name='Jenis Kegiatan Usaha', max_length=256, null=True, blank=True)
	lokasi_kegiatan_usaha = models.CharField(verbose_name='Lokasi Kegiatan Usaha', max_length=256, null=True, blank=True)
	luas_tanah_bangunan = models.CharField(verbose_name='Luas Tanah / Bangunan', max_length=256, null=True, blank=True)

	def as_json(self):

		return dict(id=self.id, nama_optikal=self.nama_optikal, nama_pemilik_perusahaan=self.nama_pemilik_perusahaan, jenis_badan_usaha=self.jenis_badan_usaha, alamat_usaha=self.alamat_usaha, no_telepon=self.no_telepon, jenis_kegiatan_usaha=self.jenis_kegiatan_usaha, lokasi_kegiatan_usaha=self.lokasi_kegiatan_usaha, luas_tanah_bangunan=self.luas_tanah_bangunan)


	def __unicode__(self):
		return u'%s' % str(self.nama_optikal)

	class Meta:
		verbose_name = 'Optikal'
		verbose_name_plural = 'Optikal'

class JenisKlinik(models.Model):
	kode_jenis_klinik = models.CharField(verbose_name='Kode Jenis Klinik', max_length=256)
	jenis_klinik = models.CharField(verbose_name='Jenis Klinik', max_length=256, null=True, blank=True)
	keterangan = models.CharField(verbose_name='Keterangan', max_length=100, null=True, blank=True)

	def as_json__jenis_klinik(self):
		return dict(id=self.id, jenis_klinik=self.jenis_klinik, keterangan=self.keterangan)

	def __unicode__(self):
		return u'%s' % str(self.jenis_klinik)

	class Meta:
		verbose_name = 'Jenis Klinik'
		verbose_name_plural = 'Jenis Klinik'

class MendirikanKlinik(PengajuanIzin):
	perusahaan = models.ForeignKey(Perusahaan, verbose_name='Perusahaan', null=True, blank=True)
	jenis_klinik = models.ForeignKey(JenisKlinik, verbose_name='Jenis Klinik', null=True, blank=True)
	nama_klinik = models.CharField(verbose_name='Nama Klinik', max_length=256, null=True, blank=True)
	alamat_klinik = models.CharField(verbose_name='Alamat Klinik', max_length=256, null=True, blank=True)
	desa = models.ForeignKey(Desa, verbose_name='Desa', null=True, blank=True)
	no_telepon = models.CharField(verbose_name='No Telepon', max_length=256, null=True, blank=True)

	def as_json__mendirikan_klinik(self):
		alamat_lengkap = ''
		if self.desa and self.alamat_klinik:
			alamat_lengkap = str(self.alamat_klinik)+self.desa.lokasi_lengkap()
		desa = ''
		if self.desa:
			desa = self.desa.as_json()
		jenis_klinik = ''
		if self.jenis_klinik:
			jenis_klinik = self.jenis_klinik.as_json__jenis_klinik()
		return dict(id=self.id, jenis_klinik=jenis_klinik, nama_klinik=self.nama_klinik, alamat_klinik=self.alamat_klinik, alamat_lengkap=alamat_lengkap, desa=desa, no_telepon=self.no_telepon)


	def __unicode__(self):
		return u'%s' % str(self.nama_klinik)

	class Meta:
		verbose_name = 'Mendirikan Klinik'
		verbose_name_plural = 'Mendirikan Klinik'

class OperasionalKlinik(PengajuanIzin):
	perusahaan = models.ForeignKey(Perusahaan, verbose_name='Perusahaan', null=True, blank=True)
	jenis_klinik = models.ForeignKey(JenisKlinik, verbose_name='Jenis Klinik', null=True, blank=True)
	nama_klinik = models.CharField(verbose_name='Nama Klinik', max_length=256, null=True, blank=True)
	alamat_klinik = models.CharField(verbose_name='Alamat Klinik', max_length=256, null=True, blank=True)
	desa = models.ForeignKey(Desa, verbose_name='Desa', null=True, blank=True)
	no_telepon = models.CharField(verbose_name='No Telepon', max_length=256, null=True, blank=True)

	def as_json__operasional_klinik(self):
		alamat_lengkap = ''
		if self.desa and self.alamat_klinik:
			alamat_lengkap = str(self.alamat_klinik)+self.desa.lokasi_lengkap()
		desa = ''
		if self.desa:
			desa = self.desa.as_json()
		jenis_klinik = ''
		if self.jenis_klinik:
			jenis_klinik = self.jenis_klinik.as_json__jenis_klinik()
		return dict(id=self.id, jenis_klinik=jenis_klinik, nama_klinik=self.nama_klinik, alamat_klinik=self.alamat_klinik, alamat_lengkap=alamat_lengkap, desa=desa, no_telepon=self.no_telepon)

	def __unicode__(self):
		return u'%s' % str(self.nama_klinik)

	class Meta:
		verbose_name = 'Operasional Klinik'
		verbose_name_plural = 'Operasional Klinik'