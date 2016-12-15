from django.conf import settings
from django.db import models
from accounts.models import Account
from master.models import JenisPemohon, AtributTambahan, Berkas, JenisReklame, Desa, MetaAtribut,ParameterBangunan
from perusahaan.models import KBLI, Kelembagaan, JenisPenanamanModal, BentukKegiatanUsaha, Legalitas, JenisBadanUsaha, StatusPerusahaan, BentukKerjasama, JenisPengecer, KedudukanKegiatanUsaha, JenisPerusahaan
from decimal import Decimal

from izin.utils import JENIS_IZIN, get_tahun_choices, JENIS_IUJK, JENIS_ANGGOTA_BADAN_USAHA, JENIS_PERMOHONAN,STATUS_HAK_TANAH,KEPEMILIKAN_TANAH

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
	masa_berlaku = models.PositiveSmallIntegerField(verbose_name='Masa Berlaku (Berapa Tahun?)', null=True, blank=True)
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
	legalitas = models.ManyToManyField(Legalitas, related_name='legalitas_pengajuan', verbose_name='Legalitas', blank=True)

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
	kbli = models.ManyToManyField(KBLI, related_name='kbli_siup', verbose_name='KBLI', blank=True)
	# Contoh isian: perdagangan mikro/ kecil/ menengah/ besar
	kelembagaan = models.ForeignKey(Kelembagaan, related_name='kelembagaan_siup', blank=True, null=True, verbose_name='Kelembagaan')
	# produk_utama = models.ManyToManyField(ProdukUtama, related_name='barang_jasa_siup', verbose_name='Barang / Jasa Dagangan Utama')
	produk_utama = models.TextField(null=True, blank=True, verbose_name='Barang / Jasa Dagang Utama')
	bentuk_kegiatan_usaha = models.ForeignKey(BentukKegiatanUsaha, related_name='bentuk_kegiatan_usaha_siup', blank=True, null=True, verbose_name='Kegiatan Usaha')
	jenis_penanaman_modal = models.ForeignKey(JenisPenanamanModal, related_name='jenis_penanaman_modal_siup', blank=True, null=True, verbose_name='Jenis Penanaman Modal')	
	kekayaan_bersih = models.CharField(verbose_name='Kekayaan Bersih Perusahaan', null=True, blank=True, max_length=255, help_text='Tidak termasuk tanah dan bangunan tempat usaha')
	total_nilai_saham = models.CharField(max_length=255, null=True, blank=True, verbose_name='Total Nilai Saham')
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
	jenis_reklame = models.ForeignKey(JenisReklame, verbose_name='Jenis Reklame', blank=True, null=True)
	judul_reklame = models.CharField(max_length=255, verbose_name='Judul Reklame')
	panjang = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Panjang',default=0, null=True, blank=True)
	lebar = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Lebar',default=0 ,null=True, blank=True)
	sisi = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Sisi',default=0, null=True, blank=True)
	letak_pemasangan = models.CharField(max_length=255, verbose_name='Letak Pemasangan', null=True, blank=True)
	jumlah = models.IntegerField(verbose_name="Jumlah", null=True, blank=True)
	desa = models.ForeignKey(Desa, verbose_name='Desa', null=True, blank=True)
	tanggal_mulai = models.DateField(verbose_name='Tanggal Mulai Dipasang', null=True, blank=True)
	tanggal_akhir = models.DateField(verbose_name='Tanggal Akhir Dipasang', null=True, blank=True)
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
	nama_pejabat = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nama Pejabat')
	jabatan_pejabat = models.CharField(max_length=255, null=True, blank=True, verbose_name='Jabatan Pejabat')
	nip_pejabat = models.CharField(max_length=255, null=True, blank=True, verbose_name='NIP Pejabat')
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
	jenis_iujk = models.CharField(max_length=255, verbose_name='Jenis IUJK', choices=JENIS_IUJK)

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
	nilai_paket_pekerjaan = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Nilai Paket Pekerjaan')

	def __unicode__(self):
		return u'%s - %s' % (str(self.nama_paket_pekerjaan), str(self.detil_iujk))

	def get_nilai_rupiah(self):
		if self.nilai_paket_pekerjaan:
			return 'Rp. '+'{:,.2f}'.format(float(self.nilai_paket_pekerjaan))
		return 'Rp. 0.00'

	def as_dict(self):
		return {
			'nama_paket_pekerjaan': self.nama_paket_pekerjaan,
			'klasifikasi_usaha': self.klasifikasi_usaha,
			'tahun': self.tahun,
			'nilai_paket_pekerjaan': str(self.get_nilai_rupiah()),
		}

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

	def as_dict(self):
		return {
			'jenis_anggota_badan': self.jenis_anggota_badan,
			'nama': self.nama,
			'id': self.id,
			# 'berkas_tambahan': self.berkas_tambahan.all(),
		}

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Anggota Badan Usaha'
		verbose_name_plural = 'Anggota Badan Usaha'

class DetilTDP(PengajuanIzin):
	perusahaan= models.ForeignKey('perusahaan.Perusahaan', related_name='tdp_perusahaan', blank=True, null=True)
	# Data Umum Perusahaan PT
	status_perusahaan = models.ForeignKey(StatusPerusahaan, related_name='status_perusahaan_tdp', verbose_name='Status Perusahaan', blank=True, null=True)
	jenis_badan_usaha = models.ForeignKey(JenisBadanUsaha, related_name='jenis_badan_usaha_tdp', verbose_name='Jenis Badan Usaha', blank=True, null=True)
	bentuk_kerjasama = models.ForeignKey(BentukKerjasama, related_name='bentuk_kerjasama_tdp', verbose_name='Bentuk Kerjasama', blank=True, null=True)

	jumlah_bank = models.IntegerField(verbose_name='Jumlah Bank', default=0)
	nasabah_utama_bank_1 = models.CharField(max_length=100, verbose_name='Nasabah Utama Bank 1')
	nasabah_utama_bank_2 = models.CharField(max_length=100, verbose_name='Nasabah Utama Bank 2 (Jika Ada)', blank=True, null=True)
	jenis_penanaman_modal = models.ForeignKey(JenisPenanamanModal, related_name='jenis_penanaman_modal_tdp', blank=True, null=True, verbose_name='Jenis Penanaman Modal')
	tanggal_pendirian = models.DateField(verbose_name='Tanggal Pendirian', null=True, blank=True)
	tanggal_mulai_kegiatan = models.DateField(verbose_name='Tanggal Mulai Kegiatan', null=True, blank=True)
	jangka_waktu_berdiri = models.PositiveSmallIntegerField(verbose_name='Jangka Waktu Berdiri (Berapa Tahun?)', null=True, blank=True)

	# Jika bukan kantor pusat
	nomor_tdp_kantor_pusat = models.CharField(max_length=150, verbose_name='No. TDP Kantor Pusat', null=True, blank=True)
	# Jika memiliki unit produksi
	alamat_unit_produksi = models.CharField(max_length=255,  verbose_name='Alamat Unit Produksi', null=True, blank=True)
	desa_unit_produksi = models.ForeignKey(Desa, verbose_name='Desa', null=True, blank=True)

	merek_dagang = models.CharField(max_length=100, verbose_name='Merek Dagang (Jika Ada)', blank=True, null=True)
	no_merek_dagang = models.CharField(max_length=100, verbose_name='Nomor Merek Dagang (Jika Ada)', blank=True, null=True)
	pemegang_hak_cipta = models.CharField(max_length=100, verbose_name='Pemegang Hak Cipta (Jika Ada)', blank=True, null=True)
	no_hak_cipta = models.CharField(max_length=100, verbose_name='Nomor Hak Cipta (Jika Ada)', blank=True, null=True)
	pemegang_hak_paten = models.CharField(max_length=100, verbose_name='Pemegang Hak Paten (Jika Ada)', blank=True, null=True)
	no_hak_paten = models.CharField(max_length=100, verbose_name='Nomor Hak Paten (Jika Ada)', blank=True, null=True)

	# Data Kegiatan PT 
	kegiatan_usaha_pokok = models.CharField(max_length=255, verbose_name='Kegiatan Usaha Pokok', blank=True, null=True)
	kegiatan_usaha_lain_1 = models.CharField(max_length=255, verbose_name='Kegiatan Usaha Lain (1)', blank=True, null=True)
	kegiatan_usaha_lain_2 = models.CharField(max_length=255, verbose_name='Kegiatan Usaha Lain (2)', blank=True, null=True)
	komoditi_produk_pokok = models.CharField(max_length=255, verbose_name='Komoditi / Produk Pokok', blank=True, null=True)
	komoditi_produk_lain_1 = models.CharField(max_length=255, verbose_name='Komoditi / Produk Lain (1)', blank=True, null=True)
	komoditi_produk_lain_2 = models.CharField(max_length=255, verbose_name='Komoditi / Produk Lain (2)', blank=True, null=True)
	omset_per_tahun = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Omset Perusahaan Per Tahun', null=True, blank=True)
	total_aset = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total Aset (setelah perusahaan beroperasi)', null=True, blank=True)
	jumlah_karyawan_wni = models.IntegerField(verbose_name='Jumlah Karyawan WNI', default=0)
	jumlah_karyawan_wna = models.IntegerField(verbose_name='Jumlah Karyawan WNA', default=0)
	kapasitas_mesin_terpasang = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Kapasitas Mesin Terpasang', null=True, blank=True)
	satuan_kapasitas_mesin_terpasang = models.CharField(max_length=100, verbose_name='Satuan', blank=True, null=True)
	kapasitas_produksi_per_tahun = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Kapasitas Produksi Per Tahun', null=True, blank=True)
	satuan_kapasitas_produksi_per_tahun = models.CharField(max_length=100, verbose_name='Satuan', blank=True, null=True)
	prosentase_kandungan_produk_lokal = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Prosentase Kandungan Produk Lokal', null=True, blank=True)
	prosentase_kandungan_produk_import = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Prosentase Kandungan Produk Import', null=True, blank=True)
	jenis_pengecer = models.ForeignKey(JenisPengecer, verbose_name='Jenis Pengecer', null=True, blank=True)
	kedudukan_kegiatan_usaha = models.ForeignKey(KedudukanKegiatanUsaha, verbose_name='Kedudukan dalam mata rantai kegiatan usaha', null=True, blank=True)
	jenis_perusahaan = models.ForeignKey(JenisPerusahaan, verbose_name='Jenis Perusahaan', null=True, blank=True)

	# masih sampe tab4 TDP PT

	def __unicode__(self):
		return u'Detil %s - %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan), str(self.perusahaan))

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Detil TDP'
		verbose_name_plural = 'Detil TDP'

class IzinLain(AtributTambahan):
	pengajuan_izin = models.ForeignKey(PengajuanIzin, related_name='izin_lain_pengajuan_izin', verbose_name='Izin Lain')
	kelompok_jenis_izin = models.ForeignKey(KelompokJenisIzin, verbose_name='Kelompok Jenis Izin')
	no_izin = models.CharField(max_length=255, verbose_name='nomor izin', blank=True, null=True)
	dikeluarkan_oleh = models.CharField(max_length=255, verbose_name='dikeluarkan oleh', blank=True, null=True)
	tanggal_dikeluarkan = models.DateField(verbose_name='Tanggal Dikeluarkan', blank=True, null=True)
	masa_berlaku = models.PositiveSmallIntegerField(verbose_name='Masa Berlaku (Berapa Tahun?)', null=True, blank=True)

class RincianPerusahaan(models.Model):
	detil_tdp = models.OneToOneField(DetilTDP, related_name='rincian_perusahaan_detil_tdp', verbose_name='Detil TDP')
	model_dasar = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Modal Dasar Rp.')
	model_ditempatkan = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Modal Ditempatkan Rp.', null=True, blank=True)
	model_disetor = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Modal Disetor Rp.', null=True, blank=True)
	banyaknya_saham = models.IntegerField(verbose_name='Banyaknya Saham', default=0)
	nilai_nominal_per_saham = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Nilai Nominal Per Saham', null=True, blank=True)

class Survey(MetaAtribut):
	no_survey = models.CharField(verbose_name='Nomor Survey', max_length=255, unique=True)
	pengajuan = models.ForeignKey(DetilIUJK, related_name='survey_pengajuan', verbose_name='Pengajuan')
	skpd = models.ForeignKey("kepegawaian.UnitKerja", related_name="survey_skpd", verbose_name='SKPD')
	kelompok_jenis_izin = models.ForeignKey(KelompokJenisIzin, verbose_name="Kelompk Jenis Izin")
	permohonan = models.CharField(verbose_name='Permohonan', choices=JENIS_PERMOHONAN, max_length=100,)
	tanggal_survey = models.DateField(verbose_name='Tanggal Survey')
	deadline_survey = models.DateField(verbose_name='Deadline Survey')
	keterangan_tambahan = models.CharField(verbose_name='Keterangan Tambahan',  max_length=255, blank=True, null=True)
	no_berita_acara = models.CharField(verbose_name='Nomor Berita Acara', max_length=255, blank=True, null=True)
	tanggal_berita_acara_dibuat = models.DateField(verbose_name='Tanggal Berita Acara Dibuat', blank=True, null=True)
	tanggal_berita_acara_diverifkasi = models.DateField(verbose_name='Tanggal Berita Acara Diverifikasi', blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (str(self.no_survey))

	class Meta:
		verbose_name = 'Survey'
		verbose_name_plural = 'Survey'


class DetilIMBPapanReklame(PengajuanIzin):
	perusahaan= models.ForeignKey('perusahaan.Perusahaan', related_name='imbreklame_perusahaan', blank=True, null=True)
	jenis_papan_reklame = models.CharField(max_length=255, verbose_name='Jenis Papan Reklame')
	lebar = models.DecimalField(max_digits=5, decimal_places=2,default=0 ,verbose_name='Lebar')
	tinggi = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Tinggi')
	lokasi_pasang = models.CharField(max_length=255, blank=True, null=True, verbose_name='Lokasi Pasang')
	jumlah = models.IntegerField(verbose_name="Jumlah", null=True, blank=True)
	desa = models.ForeignKey(Desa, verbose_name='Desa', null=True, blank=True)
	klasifikasi_jalan = models.CharField(max_length=255, blank=True, null=True, verbose_name='Klasifikasi Jalan')
	batas_utara = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Utara')
	batas_timur = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Timur')
	batas_selatan = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Selatan')
	batas_barat = models.CharField(max_length=255, blank=True, null=True, verbose_name='Bats Barat')

	def __unicode__(self):
		return u'Detil %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		ordering = ['-status']
		verbose_name = 'Detil IMB Papan Reklame'
		verbose_name_plural = 'Detil IMB Papan Reklame'

class DetilIMB(PengajuanIzin):
	bangunan = models.CharField(verbose_name="Bangunan", max_length=150)
	luas_bangunan = models.DecimalField(max_digits=5, decimal_places=2, default=0,verbose_name='Luas Bangunan')
	jumlah_bangunan = models.IntegerField(verbose_name="Jumlah Bangunan", null=True, blank=True)
	luas_tanah = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Luas Tanah')
	no_surat_tanah = models.CharField(max_length=255, verbose_name='No Surat Tanah')
	tanggal_surat_tanah = models.DateField(verbose_name='Tanggal Surat Tanah', null=True, blank=True)
	lokasi = models.CharField(verbose_name="Lokasi", max_length=150, null=True, blank=True)
	desa = models.ForeignKey(Desa, verbose_name='Desa', null=True, blank=True)
	status_hak_tanah = models.CharField(verbose_name='Status Hak Tanah', choices=STATUS_HAK_TANAH, max_length=20, null=True, blank=True)
	kepemilikan_tanah = models.CharField(verbose_name='Kepemilikan Tanah', choices=KEPEMILIKAN_TANAH, max_length=20, null=True, blank=True)
	parameter_bangunan = models.ManyToManyField(ParameterBangunan,verbose_name="Parameter Bangunan",blank=True)
	luas_bangunan_lama = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,verbose_name='Luas Bangunan Yang Sudah Ada')
	no_imb_lama = models.CharField(max_length=255, verbose_name='No. IMB Bangunan Yang Sudah Ada', null=True, blank=True)
	tanggal_imb_lama =models.DateField(verbose_name='Tanggal IMB Bangunan Yang Sudah Ada', null=True, blank=True)
	def __unicode__(self):
		return "%s" % (self.bangunan)

	class Meta:
		ordering = ['-status']
		verbose_name = 'Detil IMB'
		verbose_name_plural = 'Detil IMB'

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