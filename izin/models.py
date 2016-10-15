from django.conf import settings
from django.db import models
from accounts.models import Account
from master.models import JenisPemohon, AtributTambahan, Berkas, JenisReklame, Desa
from perusahaan.models import KBLI, Kelembagaan, ProdukUtama, JenisPenanamanModal, BentukKegiatanUsaha, Legalitas
from decimal import Decimal

from izin.utils import JENIS_IZIN, get_tahun_choices, JENIS_IUJK, JENIS_ANGGOTA_BADAN_USAHA

# from mptt.models import MPTTModel
# from mptt.fields import TreeForeignKey
# from django.utils.deconstruct import deconstructible
# from django.db.models.signals import pre_delete
# from django.dispatch.dispatcher import receiver

from datetime import datetime

# Create your models here.

class Pemohon(Account):
	jenis_pemohon = models.ForeignKey(JenisPemohon, verbose_name='Jenis Pemohon')
	jabatan_pemohon = models.CharField(max_length=255, blank=True, null=True, verbose_name='Jabatan Pemohon')
	berkas_foto = models.ManyToManyField(Berkas, verbose_name="Berkas Foto", related_name='berkas_foto_pemohon', blank=True)
	berkas_npwp = models.ForeignKey(Berkas, verbose_name="Berkas NPWP", related_name='berkas_npwp_pemohon', blank=True, null=True)

	def as_json(self):
		tanggal_lahir = ''
		if self.tanggal_lahir:
			tanggal_lahir = self.tanggal_lahir.strftime("%d-%m-%Y")
		return dict(id=self.id,username=self.username, nama_lengkap=self.nama_lengkap, jabatan_pemohon=self.jabatan_pemohon, alamat=self.alamat, tempat_lahir=self.tempat_lahir,
					tanggal_lahir=tanggal_lahir,telephone=self.telephone, kewarganegaraan=self.kewarganegaraan)

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.nama_lengkap)+"</option>"

	def set_username(self):
		nomor_list = self.nomoridentitaspengguna_set.all()
		jumlah_ =  nomor_list.count()
		if jumlah_ == 1:
			nomor_ = nomor_list.first()
			nomor_.set_as_username()
		elif jumlah_ > 1:
			username = None
			nip_list = []
			jenis_identitas = None
			for n in nomor_list:
				ji = n.jenis_identitas
				nip_list.append(ji)
				if jenis_identitas and ji:
					if jenis_identitas.id > ji.id:
						jenis_identitas = ji
						username = n.nomor
				elif not jenis_identitas and ji:
					jenis_identitas = ji
					username = n.nomor
			if username:
				self.username = re.sub('[^0-9a-zA-Z]+', '', username)

	def __unicode__(self):
		return "%s" % (self.nama_lengkap)

	class Meta:
		ordering = ['-status', 'id']
		verbose_name = 'Pemohon'
		verbose_name_plural = 'Pemohon'

class JenisPeraturan(models.Model):
	jenis_peraturan = models.CharField(max_length=100, verbose_name='Jenis Peraturan')
	keterangan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Keterangan')

	def get_title(self):
		if self.keterangan:
			return self.keterangan
		else:
			return self.jenis_peraturan

	def __unicode__(self):
		return "%s" % (self.jenis_peraturan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Peraturan'
		verbose_name_plural = 'Jenis Peraturan'

class DasarHukum(models.Model):
	jenis_peraturan = models.ForeignKey(JenisPeraturan, verbose_name='Jenis Peraturan')
	instansi = models.CharField(max_length=100, verbose_name='Instansi')
	nomor = models.CharField(max_length=100, verbose_name='Nomor')
	tahun = models.PositiveSmallIntegerField(choices=get_tahun_choices(1945))
	tentang = models.CharField(max_length=255, verbose_name='Tentang')
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')
	berkas = models.ForeignKey(Berkas, verbose_name="Berkas", blank=True, null=True)

	def as_tr(self):
		file_url = self.get_file_url()
		if file_url == "#":
			file_url = "-"
		else:
			file_url = '<a href="'+file_url+'"><i class="fa fa-download"></i> Unduh</a>'
		return """
			<tr>
		        <td>%s %s No. %s Tahun %s</td>
		        <td>%s</td>
		        <td>%s</td>
	      	</tr>
		""" % (str(self.jenis_peraturan), str(self.instansi), str(self.nomor), str(self.tahun), self.tentang, file_url)

	def get_file_url(self):
		if self.berkas:
			return self.berkas.get_file_url()
		return "#"

	def __unicode__(self):
		return "%s" % (self.nomor)

	class Meta:
		ordering = ['id']
		verbose_name = 'Dasar Hukum'
		verbose_name_plural = 'Dasar Hukum'

class JenisIzin(models.Model):
	dasar_hukum = models.ManyToManyField(DasarHukum, verbose_name='Dasar Hukum')
	kode = models.CharField(max_length=15, verbose_name="Kode", blank=True, null=True)
	nama_izin = models.CharField(max_length=100, verbose_name='Nama Izin')
	jenis_izin = models.CharField(max_length=20, verbose_name='Jenis Izin', choices=JENIS_IZIN, default=1)
	keterangan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Keterangan')
	
	def as_option(self):
		return "<option value='"+str(self.kode)+"'>"+str(self.nama_izin)+"</option>"

	def __unicode__(self):
		return "%s" % (self.nama_izin)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Izin'
		verbose_name_plural = 'Jenis Izin'

class KelompokJenisIzin(models.Model):
	jenis_izin = models.ForeignKey(JenisIzin, verbose_name='Jenis Izin')
	kode = models.CharField(max_length=15, verbose_name="Kode", blank=True, null=True)
	kelompok_jenis_izin = models.CharField(max_length=100, verbose_name='Kelompok Jenis Izin')
	biaya = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Biaya')
	standart_waktu = models.PositiveSmallIntegerField(verbose_name='Standar Waktu (Berapa Hari?)', null=True, blank=True,)
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return "%s" % (self.kelompok_jenis_izin)

	def get_biaya(self):
		return 'Rp. %.2f' % self.biaya

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.kelompok_jenis_izin)+"</option>"

	class Meta:
		ordering = ['id']
		verbose_name = 'Kelompok Jenis Izin'
		verbose_name_plural = 'Kelompok Jenis Izin'

class Syarat(models.Model):
	jenis_izin = models.ForeignKey(KelompokJenisIzin, verbose_name='Kelompok Jenis Izin')
	syarat = models.CharField(max_length=255, verbose_name='Syarat')
	keterangan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Keterangan')

	def as_li(self):
		return """
			<li>%s</li>
		""" % (str(self.syarat))

	def __unicode__(self):
		return "%s" % (self.syarat)

	class Meta:
		ordering = ['id']
		verbose_name = 'Syarat'
		verbose_name_plural = 'Syarat'

class Prosedur(models.Model):
	jenis_izin = models.ForeignKey(KelompokJenisIzin, verbose_name='Kelompok Jenis Izin')
	nomor_urut = models.IntegerField(verbose_name="Nomor Urut", null=True, blank=True)
	prosedur = models.CharField(max_length=255, verbose_name='Prosedur')
	lama = models.PositiveSmallIntegerField(verbose_name='Lama (Berapa Hari?)', null=True, blank=True,)
	keterangan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Keterangan')

	def as_li(self):
		return """
			<li>%s</li>
		""" % (str(self.prosedur))

	def __unicode__(self):
		return "%s" % (self.prosedur)

	class Meta:
		ordering = ['id']
		verbose_name = 'Prosedur'
		verbose_name_plural = 'Prosedur'

class JenisPermohonanIzin(models.Model):
	jenis_permohonan_izin = models.CharField(max_length=255, verbose_name='Jenis Permohonan Izin')
	keterangan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Keterangan')
	jenis_izin = models.ManyToManyField(KelompokJenisIzin, verbose_name='Kelompok Jenis Izin')

	def __unicode__(self):
		return "%s" % (self.jenis_permohonan_izin)

	class Meta:
		ordering = ['id']
		verbose_name ='Jenis Permohonan Izin'
		verbose_name_plural = 'Jenis Permohonan Izin'

class PengajuanIzin(AtributTambahan):
	# berkaitan dengan pengejuan izin sebelumnya jika ada
	izin_induk = models.ForeignKey('PengajuanIzin', blank=True, null=True)
	pemohon = models.ForeignKey(Pemohon, related_name='pemohon_izin', null=True, blank=True,)
	kelompok_jenis_izin = models.ForeignKey(KelompokJenisIzin, verbose_name='Kelompok Jenis Izin')
	jenis_permohonan = models.ForeignKey(JenisPermohonanIzin, verbose_name='Jenis Permohonan Izin')

	no_pengajuan = models.CharField(max_length=255, verbose_name='No. Pengajuan', blank=True, null=True, unique=True)
	no_izin = models.CharField(max_length=255, verbose_name='No. Izin', blank=True, null=True, unique=True)
	nama_kuasa = models.CharField(max_length=255, verbose_name='Nama Kuasa', blank=True, null=True)
	no_identitas_kuasa = models.CharField(max_length=255, verbose_name='No. Identitas Kuasa', blank=True, null=True)
	telephone_kuasa = models.CharField(max_length=255, verbose_name='Telp. Kuasa', blank=True, null=True)

	berkas_tambahan = models.ManyToManyField(Berkas, related_name='berkas_tambahan_izin', verbose_name="Berkas Tambahan", blank=True)

	keterangan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return u'%s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Pengajuan Izin'
		verbose_name_plural = 'Pengajuan Izin'

class DetilSIUP(PengajuanIzin):
	# salah satu dari data pemohon
	perusahaan= models.ForeignKey('perusahaan.Perusahaan', related_name='siup_perusahaan', blank=True, null=True)
	berkas_foto = models.ForeignKey(Berkas, verbose_name="Berkas Foto", related_name='berkas_foto_siup', blank=True, null=True)
	# salah satu dari data pemohon
	berkas_npwp_pemohon = models.ForeignKey(Berkas, verbose_name="Berkas NPWP Pemohon", related_name='berkas_npwp_pemohon_siup', blank=True, null=True)
	berkas_npwp_perusahaan = models.ForeignKey(Berkas, verbose_name="Berkas NPWP Perusahaan", related_name='berkas_npwp_perusahaan_siup', blank=True, null=True)
	legalitas = models.ManyToManyField(Legalitas, related_name='legalitas_siup', verbose_name='Legalitas', blank=True)
	kbli = models.ManyToManyField(KBLI, related_name='kbli_siup', verbose_name='KBLI', blank=True)
	# Contoh isian: perdagangan mikro/ kecil/ menengah/ besar
	kelembagaan = models.ForeignKey(Kelembagaan, related_name='kelembagaan_siup', blank=True, null=True, verbose_name='Kelembagaan')
	produk_utama = models.ManyToManyField(ProdukUtama, related_name='barang_jasa_siup', verbose_name='Barang / Jasa Dagangan Utama')
	bentuk_kegiatan_usaha = models.ForeignKey(BentukKegiatanUsaha, related_name='bentuk_kegiatan_usaha_siup', blank=True, null=True, verbose_name='Kegiatan Usaha')
	jenis_penanaman_modal = models.ForeignKey(JenisPenanamanModal, related_name='jenis_penanaman_modal_siup', blank=True, null=True, verbose_name='Jenis Penanaman Modal')	
	kekayaan_bersih = models.DecimalField(verbose_name='Kekayaan Bersih Perusahaan', null=True, blank=True, max_digits=10, decimal_places=2, help_text='Tidak termasuk tanah dan bangunan tempat usaha')
	total_nilai_saham = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Total Nilai Saham')
	presentase_saham_nasional = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True, verbose_name='Presentase Saham Nasional')
	presentase_saham_asing = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True, verbose_name='Presentase Saham Asing')
	jenis_pengajuan = models.IntegerField(verbose_name="Jenis Pengajuan", null=True, blank=True)

	def __unicode__(self):
		return u'Detil %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Detil SIUP'
		verbose_name_plural = 'Detil SIUP'

class DetilReklame(PengajuanIzin):
	perusahaan= models.ForeignKey('perusahaan.Perusahaan', related_name='reklame_perusahaan', blank=True, null=True)
	jenis_reklame = models.ForeignKey(JenisReklame, verbose_name='Jenis Reklame')
	judul_reklame = models.CharField(max_length=255, verbose_name='Judul Reklame')
	panjang = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Panjang', null=True, blank=True)
	lebar = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Lebar', null=True, blank=True)
	sisi = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Sisi', null=True, blank=True)
	letak_pemasangan = models.CharField(max_length=255, verbose_name='Letak Pemasangan', null=True, blank=True)
	desa = models.ForeignKey(Desa, verbose_name='Desa')
	lt = models.CharField(max_length=100, null=True, blank=True, verbose_name='Latitute')
	lg = models.CharField(max_length=100, null=True, blank=True, verbose_name='Longitute')

	def __unicode__(self):
		return u'Detil %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Detil Reklame'
		verbose_name_plural = 'Detil Reklame'

class SKIzin(AtributTambahan):
	pengajuan_izin = models.ForeignKey(PengajuanIzin, verbose_name='Pengajuan Izin')
	isi = models.TextField(verbose_name="Isi", blank=True, null=True)
	berkas = models.ForeignKey(Berkas, verbose_name="Berkas", related_name='berkas_sk', blank=True, null=True)
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')
	
class Riwayat(AtributTambahan):
	alasan = models.CharField(max_length=255, verbose_name='Keterangan', null=True, blank=True)
	sk_izin = models.ForeignKey(SKIzin, verbose_name='SK Izin', null=True, blank=True)
	pengajuan_izin = models.ForeignKey(PengajuanIzin, verbose_name='Pengajuan Izin', null=True, blank=True)
	berkas = models.ForeignKey(Berkas, verbose_name="Berkas", related_name='berkas_penolakan', blank=True, null=True)
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return u'%s - %s' % (str(self.pengajuan_izin), str(self.sk_izin))

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Riwayat'
		verbose_name_plural = 'Riwayat'

class DetilIUJK(PengajuanIzin):
	perusahaan= models.ForeignKey('perusahaan.Perusahaan', related_name='iujk_perusahaan', blank=True, null=True)
	jenis_iujk = models.CharField(max_length=255, verbose_name='Jenis IUJK', choices=JENIS_IZIN)

	def __unicode__(self):
		return u'Detil %s - %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan), str(self.jenis_iujk))

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Detil IUJK'
		verbose_name_plural = 'Detil IUJK'

class PaketPekerjaan(models.Model):
	detil_iujk = models.ForeignKey(DetilIUJK, related_name='paket_pekerjaan_iujk', verbose_name='Detil IUJK')
	nama_paket_pekerjaan = models.CharField(max_length=255, verbose_name='Nama Paket Pekerjaan') 
	klasifikasi_usaha = models.CharField(max_length=255, null=True, blank=True, verbose_name='Klasifikasi / Sub Klasifikasi Usaha pada SBU') 
	tahun = models.PositiveSmallIntegerField(choices=get_tahun_choices(1945))
	nilai_paket_pekerjaan = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Nilai Paket Pekerjaan')

	def __unicode__(self):
		return u'%s - %s' % (str(self.nama_paket_pekerjaan), str(self.detil_iujk))

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Paket Pekerjaan'
		verbose_name_plural = 'Paket Pekerjaan'

class AnggotaBadanUsaha(models.Model):
	detil_iujk = models.ForeignKey(DetilIUJK, related_name='anggota_badan_iujk', verbose_name='Detil IUJK')
	jenis_anggota_badan = models.CharField(max_length=255, verbose_name='Jenis Anggota Badan Usaha', choices=JENIS_ANGGOTA_BADAN_USAHA)
	nama = models.CharField(max_length=255, verbose_name='Nama')
	berkas_tambahan = models.ManyToManyField(Berkas, related_name='berkas_anggota_badan_usaha', verbose_name="Berkas Tambahan", blank=True)

	def __unicode__(self):
		return u'%s - %s' % (str(self.nama), str(self.detil_iujk))

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Anggota Badan Usaha'
		verbose_name_plural = 'Anggota Badan Usaha'

# class jenisLokasiUsaha(models.Model):
# 	jenis_lokasi_usaha = models.CharField(max_length=255,null=True, blank=True, verbose_name='Jenis Lokasi Usaha')

# 	def __unicode__(self):
# 		return "%s" % (self.jenis_lokasi_usaha)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Jenis Lokasi Usaha'
# 		verbose_name_plural = 'Jenis Lokasi Usaha'

# class JenisBangunan(models.Model):
# 	jenis_bangunan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Jenis Bangunan')

# 	def __unicode__(self):
# 		return "%s" % (self.jenis_bangunan)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Jenis Bangunan'
# 		verbose_name_plural = 'Jenis Bangunan'

# class ParameterBangunan(models.Model):
# 	parameter = models.CharField(max_length=255,null=True, blank=True, verbose_name='Parameter')
# 	detil_parameter = models.CharField(max_length=255, blank=True, null=True, verbose_name='Detil Parameter')
# 	nilai = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Nilai', null=True, blank=True)

# 	def __unicode__(self):
# 		return "%s" % (self.parameter)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Parameter Bangunan'
# 		verbose_name_plural = 'Parameter Bangunan'

# class JenisKegiatanPembangunan(models.Model):
# 	jenis_kegiatan_pembangunan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Jenis Kegiatan Pembangunan')
# 	detil_jenis_kegiatan = models.CharField(max_length=255, blank=True, null=True, verbose_name='Detil Jenis Kegiatan')
# 	nilai = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Nilai', null=True, blank=True)

# 	def __unicode__(self):
# 		return "%s" % (self.jenis_kegiatan_pembangunan)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Jenis Kegiatan Pembangunan'
# 		verbose_name_plural = 'Jenis Kegiatan pembangunan'

# class DetilIMBPapanReklame(models.Model):
# 	jenis_papan_reklame = models.CharField(max_length=255, verbose_name='Jenis Papan Reklame')
# 	lebar = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Lebar')
# 	tinggi = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Tinggi')
# 	lokasi_pasang = models.CharField(max_length=255, blank=True, null=True, verbose_name='Lokasi Pasang')
# 	batas_utara = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Utara')
# 	batas_timur = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Timur')
# 	batas_selatan = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Selatan')
# 	batas_barat = models.CharField(max_length=255, blank=True, null=True, verbose_name='Bats Barat')

# 	def __unicode__(self):
# 		return "%s" % (self.jenis_papan_reklame)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Detil IMB Papan Reklame'
# 		verbose_name_plural = 'Detil IMB Papan Reklame'

# class JenisGangguan(models.Model):
# 	jenis_gangguan = models.CharField(max_length=255,null=True, blank=True,verbose_name='Jenis Gangguan')

# 	def __unicode__(self):
# 		return "%s" % (self.jenis_gangguan)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Jenis Gangguan'
# 		verbose_name_plural = 'Jenis Gangguan'

# class DetilHo(models.Model):
# 	jenis_lokasi = models.ForeignKey(jenisLokasiUsaha, verbose_name='Jenis Lokasi Usaha')
# 	jenis_bangunan = models.ForeignKey(JenisBangunan, verbose_name='Jenis Bangunan')
# 	izin = models.ForeignKey(Izin, verbose_name='Izin')
# 	perkiraan_modal = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True, verbose_name='Perkiraan Modal')
# 	keperluan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Keperluan')
# 	alamat = models.CharField(max_length=255,null=True, blank=True, verbose_name='Alamat')
# 	bahan_baku_dan_penolong = models.CharField(max_length=255,null=True, blank=True, verbose_name='Bahan Baku Dan Penolong')
# 	proses_produksi = models.CharField(max_length=255,null=True, blank=True, verbose_name='Proses Produksi')

# 	def __unicode__(self):
# 		return "%s" % str(self.perkiraan_modal)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Detil HO'
# 		verbose_name_plural = 'Detil HO'

# class VerivikasiIzin(models.Model):
# 	nama_verifikasi = models.CharField(max_length=255,null=True, blank=True, verbose_name='Nama Verifikasi')

# 	def __unicode__(self):
# 		return "%s" % (self.nama_verifikasi)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Verifikasi Izin'
# 		verbose_name_plural = 'Verifikasi Izin'

# class StatusVerifikasi(models.Model):
# 	izin = models.ForeignKey(Izin, verbose_name='Izin')
# 	account = models.ForeignKey(Account, verbose_name='User')
# 	nama_verifikasi = models.ForeignKey(VerivikasiIzin, verbose_name='Verifikasi Izin')
# 	cek_status = models.BooleanField()
# 	tanggal_verifikasi = models.DateField()
# 	keterangan = models.CharField(max_length=255,blank=True, null=True, verbose_name='Keterangan')

# 	def __unicode__(self):
# 		return "%s" % (self.cek_status)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Status Verifikasi'
# 		verbose_name_plural = 'Status Verifikasi'


# class StatusHakTanah(models.Model):
# 	hak_tanah = models.CharField(max_length=255,null=True, blank=True, verbose_name='Hak Tanah')

# 	def __unicode__(self):
# 		return "%s" % (self.hak_tanah)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Status Hak Tanah'
# 		verbose_name_plural = 'Status Hak Tanah'

# class KepemilikkanTanah(models.Model):
# 	kepemilikan_tanah = models.CharField(max_length=255, null=True, blank=True, verbose_name='Kepemilikan Tanah')

# 	def __unicode__(self):
# 		return "%s" % (self.kepemilikan_tanah)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Kepemilikan Tanah'
# 		verbose_name_plural = 'Kepemilikan Tanah'

# class JenisTanah(models.Model):
# 	jenis_tanah = models.CharField(max_length=255, null=True, blank=True, verbose_name='Jenis Tanah')

# 	def __unicode__(self):
# 		return "%s" % (self.jenis_tanah)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Jenis Tanah'
# 		verbose_name_plural = 'Jenis Tanah'

# class DetilIMBGedung(models.Model):
# 	izin = models.ForeignKey(Izin, verbose_name='Izin')
# 	status_tanah = models.ForeignKey(StatusHakTanah, verbose_name='Status Hak Tanah')
# 	kepemilikan_tanah = models.ForeignKey(KepemilikkanTanah, verbose_name='Kepemilikan Tanah')
# 	jenis_tanah = models.ForeignKey(JenisTanah, verbose_name='JenisTanah')
# 	luas_bangunan = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Luas Bangunan')
# 	unit = models.IntegerField(verbose_name='Unit')
# 	luas_tanah = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Luas Tanah')
# 	no_surat_tanah = models.CharField(max_length=255, verbose_name='No Surat Tanah')
# 	tanggal_surat_tanah = models.DateField()

# 	def __unicode__(self):
# 		return "%s" % (self.luas_bangunan)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Detil IMB Gedung'
# 		verbose_name_plural = 'Detil IMB Gedung'

# class CeklisSyaratIzin(models.Model):
# 	izin = models.ForeignKey(Izin, verbose_name='Izin')
# 	syarat = models.ForeignKey(Syarat, verbose_name='Syarat')
# 	cek = models.BooleanField(default=False)

# 	def __unicode__(self):
# 		return "%s" % (self.cek)

# 	class Meta:
# 		ordering = ['id']
# 		verbose_name = 'Ceklis Syarat Izin'
# 		verbose_name_plural = 'Ceklis Syarat Izin'