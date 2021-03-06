from django.db import models
from ckeditor.fields import RichTextField
from django.utils.safestring import mark_safe

from .utils import KONDISI_LAHAN, JENIS_BANGUNAN, KLASIFIKASI_JALAN

from izin.models import Survey
from kepegawaian.models import Pegawai, UnitKerja
from master.models import MetaAtribut, Berkas

# Create your models here.


class AnggotaTim(models.Model):
	"""docstring for AnggotaTim"""
	survey_iujk = models.ForeignKey(Survey, verbose_name='Data Survey', related_name="survey_iujk")
	pegawai = models.ForeignKey(Pegawai, verbose_name='Pegawai')
	koordinator = models.BooleanField(default=False, verbose_name="Apakah Koordinator?")

	def __unicode__(self):
		return u'%s' % (str(self.pegawai))

class Rekomendasi(MetaAtribut):
	"""docstring for Rekomendasi"""
	unit_kerja = models.ForeignKey(UnitKerja, verbose_name='Unit Kerja', related_name="skpd_rekomendiasi")
	survey_iujk = models.ForeignKey(Survey, verbose_name='Data Survey', related_name="survey_rekomendiasi")
	rekomendasi = RichTextField()
	keterangan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Keterangan")
	berkas = models.ForeignKey(Berkas, verbose_name='Lampiran', related_name="lampiran_rekomendiasi", blank=True, null=True)

	def __unicode__(self):
		return '%s' % mark_safe(self.rekomendasi)

	class Meta:
		ordering = ['id']
		verbose_name = 'Rekomendasi/Pertimbangan'
		verbose_name_plural = 'Rekomendasi/Pertimbangan'


class DetilBAP(MetaAtribut):
	"""docstring for DetilBAP"""
	survey_iujk = models.ForeignKey(Survey, verbose_name='Data Survey', related_name="survey_detilbap", null=True)
	bangunan_kantor = models.BooleanField(default=False, verbose_name="Apakan Permanen")
	ruang_direktur = models.BooleanField(default=False, verbose_name="Ruang Direktur")
	ruang_staf = models.BooleanField(default=False, verbose_name="Ruang Staff")
	ruang_meja_kursi_derektur = models.BooleanField(default=False, verbose_name="Meja + Kursi Direktur")
	ruang_meja_kursi_staff_administrasi = models.BooleanField(default=False, verbose_name="Meja + Kursi Staf Administrasi")
	ruang_meja_kursi_staff_teknis = models.BooleanField(default=False, verbose_name="Meja + Kursi Staf")
	komputer = models.BooleanField(default=False, verbose_name="Komputer")
	lemari = models.BooleanField(default=False, verbose_name="Almari/Filling")
	papan_nama_klasifikasi_k1_k2 = models.BooleanField(default=False, verbose_name="Klasifikasi (K1+k2) Uk. 0,50m x 0,90m")
	papan_nama_klasifikasi_mb = models.BooleanField(default=False, verbose_name="Klasifikasi (M+B) Uk. 0,60m x 1,20m")
	papan_nama_ada_nama_perusahaan = models.BooleanField(default=False, verbose_name="Nama Perusahaan")
	papan_nama_ada_telp = models.BooleanField(default=False, verbose_name="No.Telp")
	papan_nama_ada_alamat = models.BooleanField(default=False, verbose_name="Alamat")
	papan_nama_ada_npwp = models.BooleanField(default=False, verbose_name="NPWP")
	papan_nama_ada_nama_anggota_asosiasi = models.BooleanField(default=False, verbose_name="Nomor Anggota Asosiasi")
	keterangan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Keterangan")


	def __unicode__(self):
		return '%s' % self.survey_iujk

	class Meta:
		ordering = ['id']
		verbose_name = 'Detil BAP'
		verbose_name_plural = 'Detil BAP'


class BAPReklameHO(MetaAtribut):
	"""docstring for BAPReklameHO"""
	survey = models.ForeignKey(Survey, verbose_name="Data Survey", related_name="survey_reklame_ho")
	kondisi_lahan_usaha = models.IntegerField(verbose_name='Kondisi Lahan Usaha', choices=KONDISI_LAHAN, blank=True, null=True)
	luas_tempat_usaha = models.IntegerField(verbose_name='Luas Tempat Usaha', blank=True, null=True)
	jumlah_mesin = models.IntegerField(verbose_name='Jumlah Mesin', blank=True, null=True)
	daya_kekuatan_mesin = models.IntegerField(verbose_name='Daya Kekuatan Mesin', blank=True, null=True)
	jenis_bangunan = models.IntegerField(verbose_name='Kondisi Lahan Usaha', choices=JENIS_BANGUNAN, blank=True, null=True)
	sebelah_utara = models.CharField(max_length=254, verbose_name="Sebelah Utara", blank=True, null=True)
	sebelah_timur = models.CharField(max_length=254, verbose_name="Sebelah Timur", blank=True, null=True)
	sebelah_selatan = models.CharField(max_length=254, verbose_name="Sebelah Selatan", blank=True, null=True)
	sebelah_barat = models.CharField(max_length=254, verbose_name="Sebelah Barat", blank=True, null=True)
	klasifikasi_jalan = models.IntegerField(verbose_name='Kondisi Lahan Usaha', choices=KLASIFIKASI_JALAN, blank=True, null=True)
		
	def __unicode__(self):
		return '%s' % self.survey

	class Meta:
		ordering = ['id']
		verbose_name = 'Detil BAP Reklame/HO'
		verbose_name_plural = 'Detil BAP Reklame/HO'