from django.db import models
from accounts.utils import STATUS
from perusahaan.models import Perusahaan
from accounts.models import Account
from izin.utils import JENIS

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.utils.deconstruct import deconstructible
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.

@deconstructible
class PathAndRename(object):

	def __init__(self, sub_path):
		self.path = sub_path

	def __call__(self, instance, filename):
		ext = filename.split('.')[-1]
		# set filename as random string
		filename = '{}.{}'.format(uuid4().hex, ext)
		# return the whole path to the file
		return os.path.join(self.path, filename)

path_and_rename = PathAndRename("berkas/")

class FileField(models.FileField):
	def save_form_data(self, instance, data):
		if data is not None: 
			file = getattr(instance, self.attname)
			if file != data:
				file.delete(save=False)
		super(FileField, self).save_form_data(instance, data)

class JenisPemohon(models.Model):
	jenis_pemohon = models.CharField(max_length=255, null=True, blank=True, verbose_name='Jenis Pemohon')

	def __unicode__(self):
		return "%s" % (self.jenis_pemohon)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Pemohon'
		verbose_name_plural = 'Jenis Pemohon'

class Pemohon(Account):
	jenis_pemohon = models.ForeignKey(JenisPemohon, verbose_name='Jenis Pemohon')
	jabatan_pemohon = models.CharField(max_length=255, blank=True, null=True, verbose_name='Jabatan Pemohon')

	def as_json(self):
		return dict(id=self.id, nama_lengkap=self.nama_lengkap, jabatan_pemohon=self.jabatan_pemohon)

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.nama_lengkap)+"</option>"

	def __unicode__(self):
		return "%s" % (self.nama_lengkap)

	class Meta:
		ordering = ['id']
		verbose_name = 'Pemohon'
		verbose_name_plural = 'Pemohon'

class JenisPeraturan(models.Model):
	jenis_peraturan = models.CharField(max_length=100,null=True, blank=True, verbose_name='Jenis Peraturan')
	keterangan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.jenis_peraturan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Peraturan'
		verbose_name_plural = 'Jenis Peraturan'

class DasarHukum(models.Model):
	jenis_peraturan = models.ForeignKey(JenisPeraturan, verbose_name='Jenis Peraturan')
	instansi = models.CharField(max_length=100,null=True, blank=True, verbose_name='Instansi')
	nomor = models.CharField(max_length=100,null=True, blank=True, verbose_name='Nomor')
	tentang = models.CharField(max_length=255,null=True, blank=True, verbose_name='Tentang')
	keterangan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.instansi)

	class Meta:
		ordering = ['id']
		verbose_name = 'Dasar Hukum'
		verbose_name_plural = 'Dasar Hukum'

class Syarat(models.Model):
	syarat = models.CharField(max_length=255,null=True, blank=True, verbose_name='Syarat')
	keterangan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.syarat)

	class Meta:
		ordering = ['id']
		verbose_name = 'Syarat'
		verbose_name_plural = 'Syarat'

class Prosedur(models.Model):
	prosedur = models.CharField(max_length=255,null=True, blank=True, verbose_name='Prosedur')
	lama = models.DateTimeField()
	keterangan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.prosedur)

	class Meta:
		ordering = ['id']
		verbose_name = 'Prosedur'
		verbose_name_plural = 'Prosedur'

class JenisIzin(models.Model):
	dasar_hukum = models.ManyToManyField(DasarHukum, verbose_name='Dasar Hukum')
	nama_izin = models.CharField(max_length=100,null=True, blank=True, verbose_name='Nama Izin')
	jenis_izin = models.CharField(max_length=20, verbose_name='Jenis Izin', choices=JENIS, default=1)
	keterangan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.nama_izin)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Izin'
		verbose_name_plural = 'Jenis Izin'

class KelompokJenisIzin(models.Model):
	jenis_izin = models.ForeignKey(JenisIzin, verbose_name='Jenis Izin')
	kelompok_jenis_izin = models.CharField(max_length=100,null=True, blank=True, verbose_name='Kelompok Jenis Izin')
	biaya = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True,verbose_name='Biaya')
	standart_waktu = models.DateTimeField()
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.kelompok_jenis_izin)

	def get_biaya(self):
		return 'Rp. %.2f' % self.biaya

	class Meta:
		ordering = ['id']
		verbose_name = 'Kelompok Jenis Izin'
		verbose_name_plural = 'Kelompok Jenis Izin'

class JenisBerkas(models.Model):
	jenis_berkas = models.CharField(max_length=50, null=True, blank=True, verbose_name='Jenis Berkas')
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.nama_berkas)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Berkas'
		verbose_name_plural = 'Jenis Berkas'

class Berkas(models.Model):
	pemohon = models.ForeignKey(Pemohon,null=True, related_name='pemohon_izin_berkas')
	perusahaan = models.ForeignKey(Perusahaan,null=True, verbose_name='Perusahaan')
	jenis_berkas = models.ForeignKey(JenisBerkas,null=True, blank=True, verbose_name='Jenis Berkas')
	nama_berkas = models.CharField("Nama Berkas", max_length=100)
	berkas = FileField(upload_to=path_and_rename, max_length=255)

	def get_file_url(self):
		if self.berkas:
			return settings.MEDIA_URL+str(self.berkas)
		return "#"

	def __unicode__(self):
		return self.nama_berkas

	class Meta:
		verbose_name='Berkas'
		verbose_name_plural='Berkas'

@receiver(pre_delete, sender=Berkas)
def mymodel_delete(sender, instance, **kwargs):
	# Pass false so FileField doesn't save the model.
	if instance:
		instance.berkas.delete(False)


class DataPerubahan(models.Model):
	tabel_asal = models.CharField(max_length=255, blank=True, null=True, verbose_name='Tabel Asal')
	nama_field = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nama Field')
	isi_field_lama = models.CharField(max_length=255, blank=True, null=True, verbose_name='Isi Field Lama')
	created_at = models.DateTimeField(editable=False)

	def __unicode__(self):
		return "%s" % (self.tabel_asal)

	class Meta:
		ordering = ['id']
		verbose_name = 'Data Perubahan'
		verbose_name_plural = 'Data Perubahan'

class jenisLokasiUsaha(models.Model):
	jenis_lokasi_usaha = models.CharField(max_length=255,null=True, blank=True, verbose_name='Jenis Lokasi Usaha')

	def __unicode__(self):
		return "%s" % (self.jenis_lokasi_usaha)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Lokasi Usaha'
		verbose_name_plural = 'Jenis Lokasi Usaha'

class JenisBangunan(models.Model):
	jenis_bangunan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Jenis Bangunan')

	def __unicode__(self):
		return "%s" % (self.jenis_bangunan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Bangunan'
		verbose_name_plural = 'Jenis Bangunan'

class ParameterBangunan(models.Model):
	parameter = models.CharField(max_length=255,null=True, blank=True, verbose_name='Parameter')
	detil_parameter = models.CharField(max_length=255, blank=True, null=True, verbose_name='Detil Parameter')
	nilai = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Nilai', null=True, blank=True)

	def __unicode__(self):
		return "%s" % (self.parameter)

	class Meta:
		ordering = ['id']
		verbose_name = 'Parameter Bangunan'
		verbose_name_plural = 'Parameter Bangunan'

class JenisKegiatanPembangunan(models.Model):
	jenis_kegiatan_pembangunan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Jenis Kegiatan Pembangunan')
	detil_jenis_kegiatan = models.CharField(max_length=255, blank=True, null=True, verbose_name='Detil Jenis Kegiatan')
	nilai = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Nilai', null=True, blank=True)

	def __unicode__(self):
		return "%s" % (self.jenis_kegiatan_pembangunan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Kegiatan Pembangunan'
		verbose_name_plural = 'Jenis Kegiatan pembangunan'

class JenisPermohonanIzin(models.Model):
	jenis_permohonan_izin = models.CharField(max_length=255, null=True, blank=True, verbose_name='Jenis Permohonan Izin')

	def __unicode__(self):
		return "%s" % (self.jenis_permohonan_izin)

	class Meta:
		ordering = ['id']
		verbose_name ='Jenis Permohonan Izin'
		verbose_name_plural = 'Jenis Permohonan Izin'

class DetilIMBPapanReklame(models.Model):
	jenis_papan_reklame = models.CharField(max_length=255, verbose_name='Jenis Papan Reklame')
	lebar = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Lebar')
	tinggi = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Tinggi')
	lokasi_pasang = models.CharField(max_length=255, blank=True, null=True, verbose_name='Lokasi Pasang')
	batas_utara = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Utara')
	batas_timur = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Timur')
	batas_selatan = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Selatan')
	batas_barat = models.CharField(max_length=255, blank=True, null=True, verbose_name='Bats Barat')

	def __unicode__(self):
		return "%s" % (self.jenis_papan_reklame)

	class Meta:
		ordering = ['id']
		verbose_name = 'Detil IMB Papan Reklame'
		verbose_name_plural = 'Detil IMB Papan Reklame'

class JenisGangguan(models.Model):
	jenis_gangguan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Jenis Gangguan')

	def __unicode__(self):
		return "%s" % (self.jenis_gangguan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Gangguan'
		verbose_name_plural = 'Jenis Gangguan'

class Izin(models.Model):
	izin_induk = models.ForeignKey('Izin', blank=True, null=True)

	perusahaan = models.ForeignKey(Perusahaan, null=True, blank=True, verbose_name='Perusahaan')
	pemohon = models.ForeignKey(Pemohon, related_name='pemohon_izin')
	kelompok_jenis_izin = models.ForeignKey(KelompokJenisIzin, verbose_name='Kelompok Jenis Izin')
	jenis_permohonan = models.ForeignKey(JenisPermohonanIzin, verbose_name='Jenis Permohonan Izin')
	detil_papan_reklame = models.ForeignKey(DetilIMBPapanReklame, verbose_name='Detil IMB Papan Reklame')

	jenis_gangguan = models.ManyToManyField(JenisGangguan, verbose_name='Jenis Gangguan')
	jenis_kegiatan_pembangunan = models.ManyToManyField(JenisKegiatanPembangunan, verbose_name='Jenis Kegiatan Pembangunan')
	parameter_bgunan = models.ManyToManyField(ParameterBangunan, verbose_name='Parameter')
	
	pendaftaran = models.SmallIntegerField(verbose_name='Pendaftaran')
	pembaharuan = models.IntegerField(verbose_name='Pembaharuan')
	
	create_by = models.ForeignKey(Account, related_name='izin_create_by' ,verbose_name='Dibuat Oleh' )
	status = models.PositiveSmallIntegerField(verbose_name='Status Data', choices=STATUS, default=1)
	created_at = models.DateTimeField(editable=False)
	updated_at = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.created_at = datetime.now()
		self.updated_at = datetime.now()
		return super(Izin, self).save(*args, **kwargs)

	def __unicode__(self):
		return "%s" % str(self.pendaftaran)

	class Meta:
		ordering = ['id']
		verbose_name = 'Izin'
		verbose_name_plural = 'Izin'

class KekayaanDanSaham(models.Model):
	"""docstring for Kekayaan Dan Saham"""
	izin = models.ForeignKey(Izin, verbose_name='Izin')
	kekayaan_bersih = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='Kekayaan Bersih')
	total_nilai_saham = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Total Nilai Saham')
	presentase_saham_nasional = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True, verbose_name='Presentase Saham Nasional')
	presentase_saham_asing = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True, verbose_name='Presentase Saham Asing')

	def __unicode__(self):
		return "%s" % str(self.kekayaan_bersih)

	class Meta:
		ordering = ['id']
		verbose_name = 'Kekayaan Dan Saham'
		verbose_name_plural = 'Kekayaan Dan Saham'

class DetilHo(models.Model):
	jenis_lokasi = models.ForeignKey(jenisLokasiUsaha, verbose_name='Jenis Lokasi Usaha')
	jenis_bangunan = models.ForeignKey(JenisBangunan, verbose_name='Jenis Bangunan')
	izin = models.ForeignKey(Izin, verbose_name='Izin')
	perkiraan_modal = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True, verbose_name='Perkiraan Modal')
	keperluan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Keperluan')
	alamat = models.CharField(max_length=255,null=True, blank=True, verbose_name='Alamat')
	bahan_baku_dan_penolong = models.CharField(max_length=255,null=True, blank=True, verbose_name='Bahan Baku Dan Penolong')
	proses_produksi = models.CharField(max_length=255,null=True, blank=True, verbose_name='Proses Produksi')

	def __unicode__(self):
		return "%s" % str(self.perkiraan_modal)

	class Meta:
		ordering = ['id']
		verbose_name = 'Detil HO'
		verbose_name_plural = 'Detil HO'

class JenisReklame(models.Model):
	jenis_reklame = models.CharField(max_length=255, verbose_name='Jenis Reklame')

	def __unicode__(self):
		return "%s" % (self.jenis_reklame)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Reklame'
		verbose_name_plural = 'Jenis Reklame'

class DataReklame(models.Model):
	izin = models.ForeignKey(Izin, verbose_name='Izin')
	jenis_reklame = models.ForeignKey(JenisReklame, verbose_name='Jenis Reklame')
	judul_reklame = models.CharField(max_length=255,null=True, blank=True, verbose_name='Judul Reklame')
	panjang = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Panjang')
	lebar = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Lebar')
	sisi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Sisi')
	lama_pemasangan = models.IntegerField(blank=True, null=True, verbose_name='Lama Pemasangan')

	def __unicode__(self):
		return "%s" % (self.judul_reklame)

	class Meta:
		ordering = ['id']
		verbose_name = 'Data Reklame'
		verbose_name_plural = 'Data Reklame'

class VerivikasiIzin(models.Model):
	nama_verifikasi = models.CharField(max_length=255,null=True, blank=True, verbose_name='Nama Verifikasi')

	def __unicode__(self):
		return "%s" % (self.nama_verifikasi)

	class Meta:
		ordering = ['id']
		verbose_name = 'Verifikasi Izin'
		verbose_name_plural = 'Verifikasi Izin'

class StatusVerifikasi(models.Model):
	izin = models.ForeignKey(Izin, verbose_name='Izin')
	account = models.ForeignKey(Account, verbose_name='User')
	nama_verifikasi = models.ForeignKey(VerivikasiIzin, verbose_name='Verifikasi Izin')
	cek_status = models.BooleanField()
	tanggal_verifikasi = models.DateField()
	keterangan = models.CharField(max_length=255,blank=True, null=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.cek_status)

	class Meta:
		ordering = ['id']
		verbose_name = 'Status Verifikasi'
		verbose_name_plural = 'Status Verifikasi'


class StatusHakTanah(models.Model):
	hak_tanah = models.CharField(max_length=255,null=True, blank=True, verbose_name='Hak Tanah')

	def __unicode__(self):
		return "%s" % (self.hak_tanah)

	class Meta:
		ordering = ['id']
		verbose_name = 'Status Hak Tanah'
		verbose_name_plural = 'Status Hak Tanah'

class KepemilikkanTanah(models.Model):
	kepemilikan_tanah = models.CharField(max_length=255, null=True, blank=True, verbose_name='Kepemilikan Tanah')

	def __unicode__(self):
		return "%s" % (self.kepemilikan_tanah)

	class Meta:
		ordering = ['id']
		verbose_name = 'Kepemilikan Tanah'
		verbose_name_plural = 'Kepemilikan Tanah'

class JenisTanah(models.Model):
	jenis_tanah = models.CharField(max_length=255, null=True, blank=True, verbose_name='Jenis Tanah')

	def __unicode__(self):
		return "%s" % (self.jenis_tanah)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Tanah'
		verbose_name_plural = 'Jenis Tanah'

class DetilIMBGedung(models.Model):
	izin = models.ForeignKey(Izin, verbose_name='Izin')
	status_tanah = models.ForeignKey(StatusHakTanah, verbose_name='Status Hak Tanah')
	kepemilikan_tanah = models.ForeignKey(KepemilikkanTanah, verbose_name='Kepemilikan Tanah')
	jenis_tanah = models.ForeignKey(JenisTanah, verbose_name='JenisTanah')
	luas_bangunan = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Luas Bangunan')
	unit = models.IntegerField(verbose_name='Unit')
	luas_tanah = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Luas Tanah')
	no_surat_tanah = models.CharField(max_length=255, verbose_name='No Surat Tanah')
	tanggal_surat_tanah = models.DateField()

	def __unicode__(self):
		return "%s" % (self.luas_bangunan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Detil IMB Gedung'
		verbose_name_plural = 'Detil IMB Gedung'

class CeklisSyaratIzin(models.Model):
	izin = models.ForeignKey(Izin, verbose_name='Izin')
	syarat = models.ForeignKey(Syarat, verbose_name='Syarat')
	cek = models.BooleanField(default=False)

	def __unicode__(self):
		return "%s" % (self.cek)

	class Meta:
		ordering = ['id']
		verbose_name = 'Ceklis Syarat Izin'
		verbose_name_plural = 'Ceklis Syarat Izin'

# END OF Models Izin #