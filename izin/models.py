from django.conf import settings
from django.db import models
from accounts.models import Account, IdentitasPribadi
from master.models import JenisPemohon, Berkas, JenisReklame, JenisTipeReklame, Desa, MetaAtribut, ParameterBangunan, JenisKualifikasi, BangunanJenisKontruksi
from perusahaan.models import KBLI, Kelembagaan, JenisPenanamanModal, BentukKegiatanUsaha, Legalitas, JenisBadanUsaha, StatusPerusahaan, BentukKerjasama, JenisPengecer, KedudukanKegiatanUsaha, JenisPerusahaan
from decimal import Decimal

from izin.utils import JENIS_IZIN, get_tahun_choices, JENIS_IUJK, JENIS_ANGGOTA_BADAN_USAHA, JENIS_PERMOHONAN, STATUS_HAK_TANAH, KEPEMILIKAN_TANAH, KLASIFIKASI_JALAN, RUMIJA, RUWASJA, JENIS_LOKASI_USAHA, JENIS_BANGUNAN, JENIS_GANGGUAN, JENIS_MESIN_PERALATAN, JENIS_PENGGUNAAN,SATUAN
# from mptt.models import MPTTModel
# from mptt.fields import TreeForeignKey
# from django.utils.deconstruct import deconstructible
# from django.db.models.signals import pre_delete
# from django.dispatch.dispatcher import receiver

import datetime
from ckeditor.fields import RichTextField

# from accounts.utils import KETERANGAN_PEKERJAAN

class Pemohon(Account):
	jenis_pemohon = models.ForeignKey(JenisPemohon, verbose_name='Jenis Pemohon')
	jabatan_pemohon = models.CharField(max_length=255, blank=True, null=True, verbose_name='Jabatan Pemohon')
	keterangan_pekerjaan = models.CharField(max_length=50, verbose_name='Keterangan Pekerjaan', blank=True, null=True)
	berkas_foto = models.ManyToManyField(Berkas, verbose_name="Berkas Foto", related_name='berkas_foto_pemohon', blank=True)
	berkas_npwp = models.ForeignKey(Berkas, verbose_name="Berkas NPWP", related_name='berkas_npwp_pemohon', blank=True, null=True)

	def get_obj_ktp(self):
		ktp = None
		ktp_obj = self.nomoridentitaspengguna_set.filter(jenis_identitas=1).last()
		if ktp_obj:
			ktp = ktp_obj
		return ktp

	def get_berkas_ktp(self):
		berkas = None
		ktp_obj = self.nomoridentitaspengguna_set.filter(jenis_identitas=1).last()
		if ktp_obj:
			berkas = ktp_obj.berkas
		return berkas

	def get_berkas_paspor(self):
		berkas = None
		paspor_obj = self.nomoridentitaspengguna_set.filter(jenis_identitas=2).last()
		if paspor_obj:
			berkas = paspor_obj.berkas
		return berkas

	def get_ktp(self):
		nomor_ktp = ""
		ktp_obj = self.nomoridentitaspengguna_set.filter(jenis_identitas=1).last()
		if ktp_obj:
			nomor_ktp = ktp_obj.nomor
		return nomor_ktp

	def get_paspor(self):
		nomor_paspor = ""
		paspor_obj = self.nomoridentitaspengguna_set.filter(jenis_identitas=2).last()
		if paspor_obj:
			nomor_paspor = paspor_obj.nomor
		return nomor_paspor

	def as_json(self):
		tanggal_lahir = '-'
		if self.tanggal_lahir:
			tanggal_lahir = self.tanggal_lahir.strftime("%d-%m-%Y")
		jenis_pemohon =  '-'
		if self.jenis_pemohon:
			jenis_pemohon = self.jenis_pemohon.jenis_pemohon
		jabatan_pemohon = '-'
		if self.jabatan_pemohon:
			jabatan_pemohon = self.jabatan_pemohon
		alamat_lengkap = '-'
		if self.alamat and self.desa:
			alamat_lengkap = str(self.alamat)+', Ds. '+str(self.desa.nama_desa)+', Kec. '+str(self.desa.kecamatan.nama_kecamatan)+', '+str(self.desa.kecamatan.kabupaten.nama_kabupaten)+', Prov. '+str(self.desa.kecamatan.kabupaten.provinsi.nama_provinsi)
		email = '-'
		if self.email:
			email = self.email
		pekerjaan = '-'
		if self.pekerjaan:
			pekerjaan = self.pekerjaan
		kewarganegaraan = '-'
		if self.kewarganegaraan:
			kewarganegaraan = self.kewarganegaraan
		hp = '-'
		if self.hp:
			hp = self.hp
		return dict(id=self.id,username=self.username, nama_lengkap=self.nama_lengkap, jabatan_pemohon=jabatan_pemohon, alamat=self.alamat, tempat_lahir=self.tempat_lahir,
					tanggal_lahir=tanggal_lahir,telephone=self.telephone, hp=hp, jenis_pemohon=jenis_pemohon, alamat_lengkap=alamat_lengkap, email=email, pekerjaan=pekerjaan, kewarganegaraan=kewarganegaraan)

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.nama_lengkap)+"</option>"

	def get_berkas(self):
		berkas_npwp = ''
		berkas_foto = ''
		if self.berkas_npwp:
			berkas_npwp = self.berkas_npwp.as_json()
		if self.berkas_foto:
			berkas_foto_list = self.berkas_foto.all()
			if berkas_foto_list:
				berkas_foto = [x.as_json() for x in berkas_foto_list]
		return dict(berkas_npwp=berkas_npwp, berkas_foto=berkas_foto)

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
		return "No. %s Tahun %s" % (self.nomor, self.tahun)

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
	aktif = models.BooleanField(verbose_name="Apakah izin ini aktif ?", default=True)
	
	def as_option(self):
		return "<option value='"+str(self.kode)+"'>"+str(self.nama_izin)+"</option>"

	def __unicode__(self):
		return "%s - %s" % (str(self.kode) , str(self.nama_izin))

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
	aktif = models.BooleanField(verbose_name="Apakah izin ini aktif ?", default=True)

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

# Meta
class PengajuanIzin(MetaAtribut):
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
	berkas_terkait_izin = models.ManyToManyField(Berkas, related_name='berkas_terkait_izin', verbose_name="Berkas Tambahan", blank=True)

	def __unicode__(self):
		return u'%s - %s' % (str(self.no_pengajuan), str(self.pemohon))

	def get_no_skizin(self):
		no_izin = "-"
		if self.no_izin:
			if self.jenis_permohonan_id == 2 or self.jenis_permohonan_id == 3:
				no_izin = self.no_izin.replace("/PERUBAHAN", "")
			else:
				no_izin = self.no_izin
		return no_izin

	def as_json(self):
		jenis_permohonan = ''
		if self.jenis_permohonan:
			jenis_permohonan = self.jenis_permohonan.jenis_permohonan_izin
		pemohon = ''
		if self.pemohon:
			pemohon = self.pemohon.nama_lengkap
		kelompok_jenis_izin = ''
		if self.kelompok_jenis_izin:
			kelompok_jenis_izin = self.kelompok_jenis_izin.kelompok_jenis_izin
		no_pengajuan = ''
		if self.no_pengajuan:
			no_pengajuan = self.no_pengajuan
		no_izin = ''
		if self.no_izin:
			no_izin = self.no_izin
		nama_kuasa = ''
		if self.nama_kuasa:
			nama_kuasa = self.nama_kuasa
		no_identitas_kuasa = ''
		if self.no_identitas_kuasa:
			no_identitas_kuasa = self.no_identitas_kuasa
		telephone_kuasa = ''
		if self.telephone_kuasa:
			telephone_kuasa = self.telephone_kuasa
		berkas_tambahan_list = []
		berkas_tambahan_json = {}
		if self.berkas_tambahan:
			berkas_tambahan_list = self.berkas_tambahan.all()
			berkas_tambahan_json = [obj.as_json() for obj in berkas_tambahan_list]
		verified_at = ''
		if self.verified_at:
			verified_at = self.verified_at.strftime('%d-%m-%Y')
		return dict(jenis_permohonan=jenis_permohonan, pemohon=pemohon, kelompok_jenis_izin=kelompok_jenis_izin, no_pengajuan=no_pengajuan, no_izin=no_izin, nama_kuasa=nama_kuasa, telephone_kuasa=telephone_kuasa, berkas_tambahan=berkas_tambahan_json, verified_at=verified_at)

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
	kelembagaan = models.ManyToManyField(Kelembagaan, related_name='kelembagaan_siup', blank=True, verbose_name='Kelembagaan')
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
		return u'Detil SIUP %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	def get_terbilang(self):
		from izin.utils import konversi
		terbilang = ""
		if self.kekayaan_bersih:
			kekayaan = self.kekayaan_bersih.replace(".", "")
			if kekayaan:
				terbilang = konversi(kekayaan)
		return terbilang

	def as_json(self):
		from utils import terbilang
		bentuk_kegiatan_usaha = ''
		if self.bentuk_kegiatan_usaha:
			bentuk_kegiatan_usaha = self.bentuk_kegiatan_usaha.kegiatan_usaha
		kekayaan_bersih = ''
		if self.kekayaan_bersih:
			kekayaan_bersih = 'Rp. '+str(self.kekayaan_bersih)
		total_nilai_saham = ''
		if self.total_nilai_saham:
			total_nilai_saham = 'Rp. '+str(self.total_nilai_saham)
		presentase_saham_nasional = '0 %'
		if self.presentase_saham_nasional:
			presentase_saham_nasional = str(self.presentase_saham_nasional)+' %'
		presentase_saham_asing = '0 %'
		if self.presentase_saham_asing:
			presentase_saham_asing = str(self.presentase_saham_asing)+' %'
		kelembagaan = []
		if self.kelembagaan:
			kelembagaan_list = self.kelembagaan.all()
			kelembagaan = [x.as_json() for x in kelembagaan_list]
		kbli = []
		if self.kbli:
			kbli_list = self.kbli.all()
			kbli = [x.as_json() for x in kbli_list]
		terbilang_ = ''
		if self.kekayaan_bersih:
			kekayaan = str(self.kekayaan_bersih)
			kekayaan = kekayaan.replace('.', '')
			terbilang_ = terbilang(kekayaan)
		return dict(bentuk_kegiatan_usaha=bentuk_kegiatan_usaha, kekayaan_bersih=kekayaan_bersih, total_nilai_saham=total_nilai_saham, presentase_saham_nasional=presentase_saham_nasional, presentase_saham_asing=presentase_saham_asing, kelembagaan=kelembagaan, kbli=kbli, terbilang=terbilang_)

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Detil SIUP'
		verbose_name_plural = 'Detil SIUP'

class DetilReklame(PengajuanIzin):
	perusahaan= models.ForeignKey('perusahaan.Perusahaan', related_name='reklame_perusahaan', blank=True, null=True)
	jenis_reklame = models.ForeignKey(JenisReklame, verbose_name='Jenis Izin Reklame', blank=True, null=True)
	tipe_reklame = models.ForeignKey(JenisTipeReklame,verbose_name='Tipe Reklame',blank=True,null=True)
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
		return u'Detil Reklame %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Detil Reklame'
		verbose_name_plural = 'Detil Reklame'

# meta
class DetilReklameIzin(MetaAtribut):
	detil_reklame = models.ForeignKey(DetilReklame, verbose_name='Detil Reklame', blank=True,null=True)
	tipe_reklame = models.ForeignKey(JenisTipeReklame,verbose_name='Tipe Reklame',blank=True,null=True)
	judul_reklame = models.CharField(max_length=255, verbose_name='Judul Reklame',blank=True,null=True)
	panjang = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Panjang',default=0, null=True, blank=True)
	lebar = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Lebar',default=0 ,null=True, blank=True)
	sisi = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Sisi',default=0, null=True, blank=True)
	letak_pemasangan = models.CharField(max_length=255, verbose_name='Letak Pemasangan', null=True, blank=True)
	jumlah = models.IntegerField(verbose_name="Jumlah", null=True, blank=True)
	desa = models.ForeignKey(Desa, verbose_name='Desa', null=True, blank=True)
	tanggal_mulai = models.DateField(verbose_name='Tanggal Mulai Dipasang', null=True, blank=True)
	tanggal_akhir = models.DateField(verbose_name='Tanggal Akhir Dipasang', null=True, blank=True)

	def as_dict(self):
		return {
			# "id": self.id,
			"tipe_reklame": str(self.tipe_reklame),
			"judul_reklame": self.judul_reklame,
			"letak_pemasangan": self.letak_pemasangan,
			"jumlah": str(self.jumlah),

		}

	def as_json(self):
		return dict(kecamatan=self.desa.kecamatan.nama_kecamatan, desa=self.desa.nama_desa)


	def __unicode__(self):
		return u'Detil Reklame Izin %s ' % (str(self.detil_reklame))

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Detil Reklame Izin'
		verbose_name_plural = 'Detil Reklame Izin'

# meta
class SKIzin(MetaAtribut):
	pengajuan_izin = models.ForeignKey(PengajuanIzin, verbose_name='Pengajuan Izin')
	isi = models.TextField(verbose_name="Isi", blank=True, null=True)
	berkas = models.ForeignKey(Berkas, verbose_name="Berkas", related_name='berkas_sk', blank=True, null=True)
	nama_pejabat = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nama Pejabat')
	jabatan_pejabat = models.CharField(max_length=255, null=True, blank=True, verbose_name='Jabatan Pejabat')
	nip_pejabat = models.CharField(max_length=255, null=True, blank=True, verbose_name='NIP Pejabat')
	# untuk tanggal skizin masa berlaku izin
	masa_berlaku_izin = models.DateField(verbose_name='Tanggal Masa Berlaku SKIzin', null=True, blank=True)
	# untuk status pendaftaran baru ,perubahan
	status_pendaftaran = models.CharField(max_length=50, verbose_name='Status Pendaftaran', null=True, blank=True)
	# untuk status pembaharuan ke 1 - 8
	status_pembaharuan_ke = models.IntegerField(verbose_name='Status Pembaharuan Ke', null=True, blank=True)
	# untuk tdp status waralaba
	status_perusahaan = models.CharField(max_length=255, verbose_name="Status Perusahaan", null=True, blank=True)
	body_html = RichTextField(null=True, blank=True)
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')
	tanggal_diterbitkan = models.DateField(verbose_name='Tanggal SK Izin Diterbitkan', null=True, blank=True)


	def get_masa_berlaku_izin(self):
		masa_berlaku_izin = ''
		if self.masa_berlaku_izin:
			masa_berlaku_izin = self.masa_berlaku_izin.strftime('%d-%m-%Y')
		return str(masa_berlaku_izin)

	def as_json(self):
		nama_pejabat = '-'
		if self.nama_pejabat:
			nama_pejabat = self.nama_pejabat
		jabatan_pejabat = '-'
		if self.jabatan_pejabat:
			jabatan_pejabat = self.jabatan_pejabat
		nip_pejabat = '-'
		if self.nip_pejabat:
			nip_pejabat = self.nip_pejabat
		masa_berlaku_izin = '-'
		if self.masa_berlaku_izin:
			masa_berlaku_izin = self.masa_berlaku_izin.strftime('%d-%m-%Y')
		status_pendaftaran = '-'
		if self.status_pendaftaran:
			status_pendaftaran = self.status_pendaftaran
		status_pembaharuan_ke = '-'
		if self.status_pembaharuan_ke:
			status_pembaharuan_ke = self.status_pembaharuan_ke
		status_perusahaan = '-'
		if self.status_perusahaan:
			status_perusahaan = self.status_perusahaan
		keterangan = ''
		if self.keterangan:
			keterangan = self.keterangan
		created_at = ''
		if self.created_at:
			created_at = self.created_at.strftime('%d-%m-%Y')
		return dict(nama_pejabat=nama_pejabat, jabatan_pejabat=jabatan_pejabat, nip_pejabat=nip_pejabat, masa_berlaku_izin=masa_berlaku_izin, status_pendaftaran=status_pendaftaran, status_pembaharuan_ke=status_pembaharuan_ke, status_perusahaan=status_perusahaan, keterangan=keterangan, created_at=created_at, status=self.status)

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'SKIzin'
		verbose_name_plural = 'SKIzin'
	
# meta
class Riwayat(MetaAtribut):
	alasan = models.CharField(max_length=255, verbose_name='Keterangan', null=True, blank=True)
	sk_izin = models.ForeignKey(SKIzin, verbose_name='SK Izin', null=True, blank=True)
	pengajuan_izin = models.ForeignKey(PengajuanIzin, verbose_name='Pengajuan Izin', null=True, blank=True)
	berkas = models.ForeignKey(Berkas, verbose_name="Berkas", related_name='berkas_penolakan', blank=True, null=True)
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return u'%s - %s' % (str(self.pengajuan_izin), str(self.sk_izin))

	def as_json(self):
		# pemohon = ''
		# if self.pengajuan_izin.pemohon:
		# 	pemohon = self.pengajuan_izin.pemohon.nama_lengkap
		created_at = self.created_at.strftime('%d-%m-%Y %I:%M:%S %p')
		return dict(created_at=str(created_at), keterangan=self.keterangan, created_by=self.created_by.nama_lengkap)

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Riwayat'
		verbose_name_plural = 'Riwayat'

class DetilIUJK(PengajuanIzin):
	kualifikasi = models.ForeignKey(JenisKualifikasi, verbose_name="Kualifikasi", related_name="kualifikasi_iujk", blank=True, null=True)
	perusahaan= models.ForeignKey('perusahaan.Perusahaan', related_name='iujk_perusahaan', blank=True, null=True)
	jenis_iujk = models.CharField(max_length=255, verbose_name='Jenis IUJK', choices=JENIS_IUJK)

	def __unicode__(self):
		return u'Detil IUJK %s - %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan), str(self.jenis_iujk))

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Detil IUJK'
		verbose_name_plural = 'Detil IUJK'

class Klasifikasi(models.Model):
	"""docstring for Klasifikasi"""
	jenis_iujk = models.CharField(max_length=255, verbose_name='Jenis IUJK', choices=JENIS_IUJK, null=True, blank=True)
	klasifikasi = models.CharField(max_length=255, verbose_name="Klasifikasi")
	keterangan = models.CharField(max_length=255, verbose_name="Keterangan", blank=True)

	def __unicode__(self):
		return u'%s' % (self.klasifikasi, )

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.klasifikasi)+"</option>"

	class Meta:
		verbose_name = "Kalsifikasi IUJK"
		verbose_name_plural = "Klasifikasi IUJK"

class Subklasifikasi(models.Model):
	"""docstring for SubKlasifikasi"""
	klasifikasi = models.ForeignKey(Klasifikasi, verbose_name="Klasifikasi")
	kode = models.CharField(max_length=8, verbose_name="Kode")
	subklasifikasi = models.CharField(max_length=255, verbose_name="Subklasifikasi")
	keterangan = models.TextField(verbose_name="Keterangan", blank=True)
		
	def __unicode__(self):
		return u'%s' % (self.subklasifikasi)

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.subklasifikasi)+"</option>"

	def subklasifikasi_as_li(self):
		return "<li>"+str(self.subklasifikasi)+"</li>"

	def klasifikasi_as_li(self):
		return "<li>"+str(self.klasifikasi)+"</li>"

	class Meta:
		verbose_name = "SubKalsifikasi IUJK"
		verbose_name_plural = "SubKalsifikasi IUJK"
		

class PaketPekerjaan(models.Model):
	detil_iujk = models.ForeignKey(DetilIUJK, related_name='paket_pekerjaan_iujk', verbose_name='Detil IUJK')
	nama_paket_pekerjaan = models.CharField(max_length=255, verbose_name='Nama Paket Pekerjaan', null=True, blank=True) 
	klasifikasi_usaha = models.CharField(max_length=255, null=True, blank=True, verbose_name='Klasifikasi / Sub Klasifikasi Usaha pada SBU')
	subklasifikasi = models.ForeignKey(Subklasifikasi, related_name="subklasifikasi_paketpekerjaan", null=True, blank=True, verbose_name='SubKlasifikasi Usaha pada SBU')
	tahun = models.PositiveSmallIntegerField(choices=get_tahun_choices(1945), null=True, blank=True)
	nilai_paket_pekerjaan = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Nilai Paket Pekerjaan', null=True, blank=True)
	keterangan = models.TextField(verbose_name="Keterangan", null=True, blank=True)

	def __unicode__(self):
		return u'%s - %s' % (str(self.nama_paket_pekerjaan), str(self.detil_iujk))

	def get_nilai_rupiah(self):
		if self.nilai_paket_pekerjaan:
			return 'Rp. '+'{:,.2f}'.format(float(self.nilai_paket_pekerjaan))
		return 'Rp. 0.00'

	def as_dict(self):
		tahun = ''
		if self.tahun:
			tahun = self.tahun

		return {
			'klasifikasi': self.subklasifikasi.klasifikasi.klasifikasi,
			'subklasifikasi': self.subklasifikasi.subklasifikasi,
			'nama_paket_pekerjaan': self.nama_paket_pekerjaan,
			'keterangan': self.keterangan,
			'tahun': tahun,
			'nilai_paket_pekerjaan': str(self.get_nilai_rupiah()),
		}

	def klasifikasi_as_li(self):
		return "<li>"+str(self.subklasifikasi.klasifikasi)+"</li>"

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Paket Pekerjaan'
		verbose_name_plural = 'Paket Pekerjaan'

class AnggotaBadanUsaha(models.Model):
	detil_iujk = models.ForeignKey(DetilIUJK, related_name='anggota_badan_iujk', verbose_name='Detil IUJK')
	jenis_anggota_badan = models.CharField(max_length=255, verbose_name='Jenis Anggota Badan Usaha', choices=JENIS_ANGGOTA_BADAN_USAHA)
	nama = models.CharField(max_length=255, verbose_name='Nama')
	npwp = models.CharField(max_length=255, verbose_name='NPWP', blank=True)
	no_pjt_bu = models.CharField(max_length=255, verbose_name='No PJT-BU', blank=True)
	berkas_tambahan = models.ManyToManyField(Berkas, related_name='berkas_anggota_badan_usaha', verbose_name="Berkas Tambahan", blank=True)

	def __unicode__(self):
		return u'%s - %s' % (str(self.nama), str(self.detil_iujk))

	def as_dict(self):
		return {
			'jenis_anggota_badan': self.jenis_anggota_badan,
			'nama': self.nama,
			'id': self.id,
			'no_pjt_bu': self.no_pjt_bu,
			# 'berkas_tambahan': self.berkas_tambahan.all(),
		}

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Anggota Badan Usaha'
		verbose_name_plural = 'Anggota Badan Usaha'

class JenisKoperasi(models.Model):
	jenis_koperasi = models.CharField(max_length=255, verbose_name='Jenis Koperasi')
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return u'%s' % (str(self.jenis_koperasi))

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Jenis Koperasi'
		verbose_name_plural = 'Jenis Koperasi'

class BentukKoperasi(models.Model):
	bentuk_koperasi = models.CharField(max_length=255, verbose_name='Bentuk Koperasi')
	keterangan = models.CharField(max_length=255, null=True, blank=True, verbose_name='Keterangan')

	def __unicode__(self):
		return u'%s' % (str(self.bentuk_koperasi))
	
	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Bentuk Koperasi'
		verbose_name_plural = 'Bentuk Koperasi'

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
	# nomor_tdp_kantor_pusat = models.CharField(max_length=150, verbose_name='No. TDP Kantor Pusat', null=True, blank=True)
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
	# kegiatan_usaha_pokok = models.CharField(max_length=255, verbose_name='Kegiatan Usaha Pokok', blank=True, null=True)
	kegiatan_usaha_pokok = models.ManyToManyField(KBLI, related_name='kegiatan_usaha_pokok', verbose_name='Kegiatan Usaha Pokok', blank=True)
	produk_utama = models.TextField(null=True, blank=True, verbose_name='Barang / Jasa Dagang Utama')

	# kegiatan_usaha_lain_1 = models.CharField(max_length=255, verbose_name='Kegiatan Usaha Lain (1)', blank=True, null=True)
	# kegiatan_usaha_lain_2 = models.CharField(max_length=255, verbose_name='Kegiatan Usaha Lain (2)', blank=True, null=True)
	# komoditi_produk_pokok = models.CharField(max_length=255, verbose_name='Komoditi / Produk Pokok', blank=True, null=True)
	# komoditi_produk_lain_1 = models.CharField(max_length=255, verbose_name='Komoditi / Produk Lain (1)', blank=True, null=True)
	# komoditi_produk_lain_2 = models.CharField(max_length=255, verbose_name='Komoditi / Produk Lain (2)', blank=True, null=True)
	omset_per_tahun = models.CharField(max_length=100, verbose_name='Omset Perusahaan Per Tahun', null=True, blank=True)
	total_aset = models.CharField(max_length=100, verbose_name='Total Aset (setelah perusahaan beroperasi)', null=True, blank=True)
	jumlah_karyawan_wni = models.IntegerField(verbose_name='Jumlah Karyawan WNI', default=0)
	jumlah_karyawan_wna = models.IntegerField(verbose_name='Jumlah Karyawan WNA', default=0)
	kapasitas_mesin_terpasang = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Kapasitas Mesin Terpasang', null=True, blank=True)
	satuan_kapasitas_mesin_terpasang = models.CharField(max_length=100, verbose_name='Satuan', blank=True, null=True)
	kapasitas_produksi_per_tahun = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Kapasitas Produksi Per Tahun', null=True, blank=True)
	satuan_kapasitas_produksi_per_tahun = models.CharField(max_length=100, verbose_name='Satuan', blank=True, null=True)
	presentase_kandungan_produk_lokal = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Prosentase Kandungan Produk Lokal', null=True, blank=True)
	presentase_kandungan_produk_import = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Prosentase Kandungan Produk Import', null=True, blank=True)
	jenis_pengecer = models.ForeignKey(JenisPengecer, verbose_name='Jenis Pengecer', null=True, blank=True)
	kedudukan_kegiatan_usaha = models.ForeignKey(KedudukanKegiatanUsaha, verbose_name='Kedudukan dalam mata rantai kegiatan usaha', null=True, blank=True)
	jenis_perusahaan = models.ForeignKey(JenisPerusahaan, verbose_name='Jenis Perusahaan', null=True, blank=True)
	status_waralaba = models.CharField(max_length=255, verbose_name='Status Waralaba', null=True, blank=True, default='BUKAN WARALABA')

	# rincian perusahaan
	modal_dasar = models.CharField(max_length=100, verbose_name='Modal Dasar Rp.', null=True, blank=True)
	modal_ditempatkan = models.CharField(max_length=100, verbose_name='Modal Ditempatkan Rp.', null=True, blank=True)
	modal_disetor = models.CharField(max_length=100, verbose_name='Modal Disetor Rp.', null=True, blank=True)
	banyaknya_saham = models.IntegerField(verbose_name='Banyaknya Saham', default=0, null=True, blank=True)
	nilai_nominal_per_saham = models.CharField(max_length=100, verbose_name='Nilai Nominal Per Saham', null=True, blank=True)

	# rincian koperasi
	jenis_koperasi = models.ForeignKey(JenisKoperasi, verbose_name='Jenis Koperasi', null=True, blank=True)
	bentuk_koperasi = models.ForeignKey(BentukKoperasi, verbose_name='Bentuk Koperasi', null=True, blank=True)
	modal_sendiri_simpanan_pokok = models.CharField(max_length=255, verbose_name='Modal Sendiri Simpan Pokok', null=True, blank=True)
	modal_sendiri_simpanan_wajib = models.CharField(max_length=255, verbose_name='Modal Sendiri Simpan Wajib', null=True, blank=True)
	modal_sendiri_dana_cadangan = models.CharField(max_length=255, verbose_name='Modal Sendiri Dana Cadangan', null=True, blank=True)
	modal_sendiri_hibah = models.CharField(max_length=255, verbose_name='Modal Sendiri Hibah', null=True, blank=True)
	modal_pinjaman_anggota = models.CharField(max_length=255, verbose_name='Modal Pinjaman Anggota', null=True, blank=True)
	modal_pinjaman_koperasi_lain = models.CharField(max_length=255, verbose_name='Modal Pinjaman Koperasi Lain', null=True, blank=True)
	modal_pinjaman_bank = models.CharField(max_length=255, verbose_name='Modal Pinjaman Bank', null=True, blank=True)
	modal_pinjaman_lainnya = models.CharField(max_length=255, verbose_name='Modal Pinjaman Lainnya', null=True, blank=True)
	jumlah_anggota = models.CharField(max_length=255, verbose_name='Jumlah Anggota', null=True, blank=True)
	# berkas_npwp_perusahaan = models.ForeignKey(Berkas, verbose_name="Berkas NPWP Perusahaan", related_name='berkas_npwp_perusahaan_tdp', blank=True, null=True)

	def __unicode__(self):
		return u'Detil TDP %s - %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan), str(self.perusahaan))

	def as_json(self):
		status_perusahaan = ''
		if self.status_perusahaan:
			if self.status_perusahaan.status_perusahaan:
				status_perusahaan = self.status_perusahaan.status_perusahaan
		jenis_badan_usaha = ''
		if self.jenis_badan_usaha:
			if self.jenis_badan_usaha.jenis_badan_usaha:
				jenis_badan_usaha = self.jenis_badan_usaha.jenis_badan_usaha
		bentuk_kerjasama = ''
		if self.bentuk_kerjasama:
			if self.bentuk_kerjasama.bentuk_kerjasama:
				bentuk_kerjasama = self.bentuk_kerjasama.bentuk_kerjasama
		jumlah_bank = ''
		if self.jumlah_bank:
			jumlah_bank = self.jumlah_bank
		nasabah_utama_bank_1 = ''
		if self.nasabah_utama_bank_1:
			nasabah_utama_bank_1 = self.nasabah_utama_bank_1
		nasabah_utama_bank_2 = ''
		if self.nasabah_utama_bank_2:
			nasabah_utama_bank_2 = self.nasabah_utama_bank_2
		jenis_penanaman_modal = ''
		if self.jenis_penanaman_modal:
			if self.jenis_penanaman_modal.jenis_penanaman_modal:
				jenis_penanaman_modal = self.jenis_penanaman_modal.jenis_penanaman_modal
		tanggal_pendirian = ''
		if self.tanggal_pendirian:
			tanggal_pendirian = self.tanggal_pendirian.strftime('%d-%m-%Y')
		tanggal_mulai_kegiatan = ''
		if self.tanggal_mulai_kegiatan:
			tanggal_mulai_kegiatan = self.tanggal_mulai_kegiatan.strftime('%d-%m-%Y')
		desa_unit_produksi = ''
		if self.desa_unit_produksi:
			desa_unit_produksi = self.desa_unit_produksi.lokasi_lengkap()

		return dict(status_perusahaan=status_perusahaan, jenis_badan_usaha=jenis_badan_usaha, bentuk_kerjasama=bentuk_kerjasama, jumlah_bank=jumlah_bank, nasabah_utama_bank_1=nasabah_utama_bank_1, nasabah_utama_bank_2=nasabah_utama_bank_2, jenis_penanaman_modal=jenis_penanaman_modal, tanggal_pendirian=tanggal_pendirian, tanggal_mulai_kegiatan=tanggal_mulai_kegiatan, jangka_waktu_berdiri=self.jangka_waktu_berdiri, alamat_unit_produksi=self.alamat_unit_produksi, desa_unit_produksi=desa_unit_produksi, merek_dagang=self.merek_dagang, no_merek_dagang=self.no_merek_dagang, pemegang_hak_cipta=self.pemegang_hak_cipta)

	def get_skizin(self):
		skizin = None
		skizin_obj = self.skizin_set.last()
		if skizin_obj:
			skizin = skizin_obj
		return skizin

	def get_masa_berlaku(self):
		masa_berlaku = ''
		if self.get_skizin():
			masa_berlaku = self.get_skizin().get_masa_berlaku_izin()
		return masa_berlaku

	def get_skizin_as_json():
		json = {}
		if self.get_skizin():
			json = self.get_skizin().as_json()
		return json

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Detil TDP'
		verbose_name_plural = 'Detil TDP'

# meta
class IzinLain(MetaAtribut):
	pengajuan_izin = models.ForeignKey(PengajuanIzin, related_name='izin_lain_pengajuan_izin', verbose_name='Izin Lain')
	kelompok_jenis_izin = models.ForeignKey(KelompokJenisIzin, verbose_name='Kelompok Jenis Izin')
	no_izin = models.CharField(max_length=255, verbose_name='nomor izin', blank=True, null=True)
	dikeluarkan_oleh = models.CharField(max_length=255, verbose_name='dikeluarkan oleh', blank=True, null=True)
	tanggal_dikeluarkan = models.DateField(verbose_name='Tanggal Dikeluarkan', blank=True, null=True)
	masa_berlaku = models.PositiveSmallIntegerField(verbose_name='Masa Berlaku (Berapa Tahun?)', null=True, blank=True)

	def as_json(self):
		return dict(
			id=self.id, id_jenis_izin=self.kelompok_jenis_izin.id ,nama_jenis_izin=self.kelompok_jenis_izin.kelompok_jenis_izin, no_izin=self.no_izin, dikeluarkan_oleh=self.dikeluarkan_oleh, tanggal_dikeluarkan=self.tanggal_dikeluarkan.strftime('%d-%m-%Y'), masa_berlaku=self.masa_berlaku )

	class Meta:
		# ordering = ['-status', '-updated_at',]
		verbose_name = 'Izin Lain'
		verbose_name_plural = 'Izin Lain'

# meta
class Survey(MetaAtribut):
	no_survey = models.CharField(verbose_name='Nomor Survey', max_length=255, unique=True)
	pengajuan = models.ForeignKey(PengajuanIzin, related_name='survey_pengajuan', verbose_name='Pengajuan')
	skpd = models.ForeignKey("kepegawaian.UnitKerja", related_name="survey_skpd", verbose_name='SKPD', blank=True, null=True)
	kelompok_jenis_izin = models.ForeignKey(KelompokJenisIzin, verbose_name="Kelompk Jenis Izin", blank=True, null=True)
	permohonan = models.CharField(verbose_name='Permohonan', choices=JENIS_PERMOHONAN, max_length=100,blank=True, null=True)
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
	milik = models.CharField(max_length=150, blank=True, null=True, verbose_name='Milik')
	jumlah = models.IntegerField(verbose_name="Jumlah", null=True, blank=True)
	desa = models.ForeignKey(Desa, verbose_name='Desa', null=True, blank=True)
	klasifikasi_jalan = models.CharField(verbose_name='Klasifikasi Jalan', choices=JENIS_LOKASI_USAHA, max_length=19, null=True, blank=True)
	batas_utara = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Utara')
	batas_timur = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Timur')
	batas_selatan = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Selatan')
	batas_barat = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Barat')

	def __unicode__(self):
		return u'Detil IMB Papan Reklame %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Detil IMB Papan Reklame'
		verbose_name_plural = 'Detil IMB Papan Reklame'

class DetilIMB(PengajuanIzin):
	perusahaan = models.ForeignKey('perusahaan.Perusahaan', related_name='detilimb_perusahaan', blank=True, null=True)
	bangunan = models.CharField(verbose_name="Bangunan", max_length=150)
	luas_bangunan = models.DecimalField(max_digits=8, decimal_places=2, default=0,verbose_name='Luas Bangunan')
	jumlah_bangunan = models.IntegerField(verbose_name="Jumlah Bangunan", null=True, blank=True)
	luas_tanah = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Luas Tanah')
	no_surat_tanah = models.CharField(max_length=255, verbose_name='No Surat Tanah', null=True, blank=True)
	tanggal_surat_tanah = models.DateField(verbose_name='Tanggal Surat Tanah', null=True, blank=True)
	lokasi = models.CharField(verbose_name="Lokasi", max_length=150, null=True, blank=True)
	desa = models.ForeignKey(Desa, verbose_name='Desa', null=True, blank=True)
	status_hak_tanah = models.CharField(verbose_name='Status Hak Tanah', choices=STATUS_HAK_TANAH, max_length=20, null=True, blank=True)
	kepemilikan_tanah = models.CharField(verbose_name='Kepemilikan Tanah', choices=KEPEMILIKAN_TANAH, max_length=20, null=True, blank=True)
	klasifikasi_jalan = models.CharField(verbose_name='Klasifikasi Jalan', choices=JENIS_LOKASI_USAHA, max_length=19, null=True, blank=True)
	ruang_milik_jalan = models.PositiveSmallIntegerField(verbose_name='Ruang Milik Jalan', choices=RUMIJA, null=True, blank=True)
	ruang_pengawasan_jalan = models.PositiveSmallIntegerField(verbose_name='Ruang Pengawasan Jalan', choices=RUWASJA, null=True, blank=True)
	total_biaya = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Total Biaya')
	luas_bangunan_lama = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,verbose_name='Luas Bangunan Yang Sudah Ada')
	no_imb_lama = models.CharField(max_length=255, verbose_name='No. IMB Bangunan Yang Sudah Ada', null=True, blank=True)
	tanggal_imb_lama =models.DateField(verbose_name='Tanggal IMB Bangunan Yang Sudah Ada', null=True, blank=True)
	# jenis_bangunan = models.ManyToManyField('BangunanJenisKontruksi',verbose_name="Jenis Bangunan",blank=True,null=True)
	panjang = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='Panjang')

	batas_utara = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Utara')
	batas_timur = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Timur')
	batas_selatan = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Selatan')
	batas_barat = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Barat')

	

	def __unicode__(self):
		return u'Detil IMB %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Detil IMB'
		verbose_name_plural = 'Detil IMB'

# meta
class DetilSk(MetaAtribut):
	pengajuan_izin = models.ForeignKey(PengajuanIzin, verbose_name="Detil Pengajuan Izin",blank=True, null=True)
	sk_menimbang_a = models.CharField(max_length=255, verbose_name='SK Menimbang A.', null=True, blank=True)
	sk_menimbang_b = models.CharField(max_length=255, verbose_name='SK Menimbang B.', null=True, blank=True)
	sk_menimbang_c = models.CharField(max_length=255, verbose_name='SK Menimbang C.', null=True, blank=True)
	sk_menimbang_d = models.CharField(max_length=255, verbose_name='SK Menimbang D.', null=True, blank=True)

	sk_menetapkan_a = models.CharField(max_length=255, verbose_name='SK Menetapkan A', null=True, blank=True)
	sk_menetapkan_b = models.CharField(max_length=255, verbose_name='SK Menetapkan B', null=True, blank=True)
	sk_menetapkan_c = models.CharField(max_length=255, verbose_name='SK Menetapkan C', null=True, blank=True)
	sk_menetapkan_d = models.CharField(max_length=255, verbose_name='SK Menetapkan D', null=True, blank=True)

	sk_diktum2_g = models.CharField(max_length=255, verbose_name='SK Diktum Ke 2 G', null=True, blank=True)
	sk_diktum2_h = models.CharField(max_length=255, verbose_name='SK Diktum Ke 2 H', null=True, blank=True)
	sk_diktum2_i = models.CharField(max_length=255, verbose_name='SK Diktum Ke 2 I', null=True, blank=True)
	sk_diktum2_j = models.CharField(max_length=255, verbose_name='SK Diktum Ke 2 J', null=True, blank=True)

	sk_diktum3_i = models.CharField(max_length=255, verbose_name='SK Diktum Ke 3 I', null=True, blank=True)
	sk_diktum3_j = models.CharField(max_length=255, verbose_name='SK Diktum Ke 3 J', null=True, blank=True)
	sk_diktum3_k = models.CharField(max_length=255, verbose_name='SK Diktum Ke 3 K', null=True, blank=True)
	sk_diktum3_l = models.CharField(max_length=255, verbose_name='SK Diktum Ke 3 L', null=True, blank=True)

	def __unicode__(self):
		return u'Detil SK %s - %s' % (str(self.pengajuan_izin.kelompok_jenis_izin), str(self.pengajuan_izin.pemohon))

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Detil SK'
		verbose_name_plural = 'Detil SK'

class InformasiKekayaanDaerah(PengajuanIzin):
	perusahaan= models.ForeignKey('perusahaan.Perusahaan', related_name='informasikekayaandaerah_perusahaan', blank=True, null=True)
	lokasi = models.CharField(verbose_name="Lokasi", max_length=150, null=True, blank=True)
	desa = models.ForeignKey(Desa, verbose_name='Desa', null=True, blank=True)
	# lebar = models.DecimalField(max_digits=5, decimal_places=2,default=0 ,verbose_name='Lebar')
	# panjang = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Panjang')
	jenis_penggunaan = models.CharField(verbose_name='Jenis Penggunaan', choices=JENIS_PENGGUNAAN, max_length=10, null=True, blank=True)
	luas = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Luas')
	penggunaan = models.CharField(verbose_name="Penggunaan", max_length=150, null=True, blank=True)
	no_rekomendasi = models.CharField(verbose_name="NO. Rekomendasi", max_length=150, null=True, blank=True)

	def __unicode__(self):
		return u'Detil Informasi Kekayaan Daerah %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Informasi Kekayaan Daerah'
		verbose_name_plural = 'Informasi Kekayaan Daerah'

class DetilHO(PengajuanIzin):
	perusahaan= models.ForeignKey('perusahaan.Perusahaan', related_name='detilho_perusahaan', blank=True, null=True)
	perkiraan_modal = models.CharField(max_length=200, null=True, blank=True, verbose_name='Perkiraan Modal')
	tujuan_gangguan = models.CharField(max_length=255,null=True, blank=True, verbose_name='Tujuan')
	alamat = models.CharField(max_length=255,null=True, blank=True, verbose_name='Alamat')
	no_surat_tanah = models.CharField(max_length=255, verbose_name='No Surat Tanah' ,null=True, blank=True)
	tanggal_surat_tanah = models.DateField(verbose_name='Tanggal Surat Tanah', null=True, blank=True)
	desa = models.ForeignKey(Desa, verbose_name='Desa', null=True, blank=True)
	bahan_baku_dan_penolong = models.CharField(max_length=200,null=True, blank=True, verbose_name='Bahan Baku dan Penolong')
	proses_produksi = models.CharField(max_length=200,null=True, blank=True, verbose_name='Proses Produksi')
	jenis_produksi = models.CharField(max_length=200,null=True, blank=True, verbose_name='Jenis Produksi')
	kapasitas_produksi = models.CharField(max_length=200,null=True, blank=True, verbose_name='Kapasitas Produksi')
	jumlah_tenaga_kerja = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Jumlah Tenaga Kerja')
	jumlah_mesin = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Jumlah Mesin')
	merk_mesin = models.CharField(max_length=150,null=True, blank=True, verbose_name='Merk Mesin')
	daya = models.CharField(max_length=100,null=True, blank=True, verbose_name='Daya')
	kekuatan = models.CharField(max_length=100,null=True, blank=True, verbose_name='Kekuatan')
	luas_ruang_tempat_usaha = models.DecimalField(max_digits=10, decimal_places=2,default=0, verbose_name='Luas Ruang Tempat Usaha/Bangunan')
	luas_lahan_usaha = models.DecimalField(max_digits=10, decimal_places=2,default=0, verbose_name='Luas Lahan Usaha')
	jenis_lokasi_usaha = models.CharField(verbose_name='Jenis Lokasi Usaha', choices=JENIS_LOKASI_USAHA, max_length=20,null=True, blank=True)
	jenis_bangunan = models.CharField(verbose_name='Jenis Bangunan', choices=JENIS_BANGUNAN, max_length=20,null=True, blank=True)
	jenis_gangguan = models.CharField(verbose_name='Jenis Gangguan', choices=JENIS_GANGGUAN, max_length=20,null=True, blank=True)

	batas_utara = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Utara')
	batas_timur = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Timur')
	batas_selatan = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Selatan')
	batas_barat = models.CharField(max_length=255, blank=True, null=True, verbose_name='Batas Barat')
	
	def __unicode__(self):
		return u'Detil HO %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Detil HO'
		verbose_name_plural = 'Detil HO'


class InformasiTanah(PengajuanIzin):
	perusahaan= models.ForeignKey('perusahaan.Perusahaan', related_name='informasitanah_perusahaan', blank=True, null=True)
	alamat = models.CharField(max_length=100,null=True, blank=True, verbose_name='Alamat')
	desa = models.ForeignKey(Desa, verbose_name='Desa', null=True, blank=True)
	luas = models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name='Luas Tanah')
	status_tanah = models.CharField(verbose_name='Status Tanah', max_length=20,)
	no_surat_pemberitahuan =  models.CharField(max_length=30, verbose_name='No. Surat Pemberitahuan', null=True, blank=True)
	tanggal_surat_pemberitahuan = models.DateField(verbose_name='Tanggal Surat Pemberitahuan', null=True, blank=True)
	no_sertifikat_petak =  models.CharField(max_length=30, verbose_name='No. Sertifikat/Petak D', null=True, blank=True)
	luas_sertifikat_petak = models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name='Luas Sertifikat/Petak D')
	atas_nama_sertifikat_petak =  models.CharField(max_length=255, verbose_name='Atas Nama Sertifikat/Petak D', null=True, blank=True)
	tahun_sertifikat = models.DateField(verbose_name='Tanggal Sertifikat Tanah', null=True, blank=True)
	no_persil =  models.CharField(max_length=30, verbose_name='No. Persil', null=True, blank=True)
	klas_persil= models.CharField(max_length=30, verbose_name='Klas Persil', null=True, blank=True)
	atas_nama_persil=  models.CharField(max_length=255, verbose_name='Atas Nama Persil', null=True, blank=True)
	no_jual_beli = models.CharField(max_length=255, verbose_name='No Jual Beli', null=True, blank=True)
	tanggal_jual_beli = models.DateField(verbose_name='Tanggal Jual Beli', null=True, blank=True)
	atas_nama_jual_beli = models.CharField(max_length=255, verbose_name='Atas Nama Jual Beli', null=True, blank=True)
	penggunaan_sekarang = models.CharField(max_length=150,null=True, blank=True, verbose_name='Penggunaan Sekarang')
	rencana_penggunaan = models.CharField(max_length=150,null=True, blank=True, verbose_name='Rencana Penggunaan')
	penggunaan_tanah_sebelumnya = models.CharField(max_length=150,null=True, blank=True, verbose_name='Penggunaan Tanah Sebelumnya')
	arahan_fungsi_kawasan = models.CharField(max_length=150,null=True, blank=True, verbose_name='Arahan Fungsi Kawasan')
	#Tambahan Informasi Tanah IPPT USAHA
	batas_utara = models.CharField(max_length=150, blank=True, null=True, verbose_name='Batas Utara')
	batas_timur = models.CharField(max_length=150, blank=True, null=True, verbose_name='Batas Timur')
	batas_selatan = models.CharField(max_length=150, blank=True, null=True, verbose_name='Batas Selatan')
	batas_barat = models.CharField(max_length=150, blank=True, null=True, verbose_name='Batas Barat')
	tanah_negara_belum_dikuasai = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Tanah Negara Belum Dikuasai')
	tanah_kas_desa_belum_dikuasai = models.DecimalField(max_digits=5, decimal_places=2, default=0,verbose_name='Tanah Kas Desa Belum Dikuasai')
	tanah_hak_pakai_belum_dikuasai = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Tanah Hak Pakai Belum Dikuasai')
	tanah_hak_guna_bangunan_belum_dikuasai = models.DecimalField(max_digits=5, decimal_places=2, default=0,verbose_name='Tanah Hak Guna Bangunan Belum Dikuasai')
	tanah_hak_milik_sertifikat_belum_dikuasai = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Tanah Hak MIlik Sertifikat Belum Dikuasai')
	tanah_adat_belum_dikuasai = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Tanah Adat Belum Dikuasai')
	pemegang_hak_semula_dari_tanah_belum_dikuasai = models.CharField(max_length=50,null=True, blank=True, verbose_name='Pemegang Hak Tanah Sebelum Dkuasai')
	tanah_belum_dikuasai_melalui = models.CharField(max_length=100,null=True, blank=True, verbose_name='Tanah Belum Dikuasai Melalui')
	jumlah_tanah_belum_dikuasai = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='Jumlah Tanah Negara Sudah Dikuasai')
	tanah_negara_sudah_dikuasai = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Tanah Negara Sudah Dikuasai')
	tanah_kas_desa_sudah_dikuasai = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Tanah Kas Desa Sudah Dikuasai')
	tanah_hak_pakai_sudah_dikuasai = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Tanah Hak Pakai Sudah Dikuasai')
	tanah_hak_guna_bangunan_sudah_dikuasai = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Tanah Hak Guna Bangunan Sudah Dikuasai')
	tanah_hak_milik_sertifikat_sudah_dikuasai = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Tanah Hak MIlik Sertifikat Sudah Dikuasai')
	tanah_adat_sudah_dikuasai = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Tanah Adat Sudah Dikuasai')
	pemegang_hak_semula_dari_tanah_sudah_dikuasai = models.CharField(max_length=50,null=True, blank=True, verbose_name='Pemegang Hak Tanah Sesudah Dkuasai')
	tanah_sudah_dikuasai_melalui = models.CharField(max_length=100,null=True, blank=True, verbose_name='Tanah Sudah Dikuasai Melalui')
	jumlah_tanah_sudah_dikuasai = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='Jumlah Tanah Negara Sudah Dikuasai')
	#Rencana Pembangunan
	tipe1 = models.CharField(max_length=20,null=True, blank=True, verbose_name='Tipe 1')
	tipe2 = models.CharField(max_length=20,null=True, blank=True, verbose_name='Tipe 2')
	tipe3 = models.CharField(max_length=20,null=True, blank=True, verbose_name='Tipe 3')
	gudang1 = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Gudang 1')
	gudang2 = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Gudang 2')
	gudang3 = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Gudang 3')
	luas_tipe1 = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Luas Tipe 1')
	luas_tipe2 = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Luas Tipe 2')
	luas_tipe3 = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Luas Tipe 3')
	luas_lapangan = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Luas Lapangan')
	luas_kantor = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Luas Kantor')
	luas_saluran = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Luas Saluran')
	luas_taman = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Luas Taman')
	jumlah_perincian_penggunaan_tanah = models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name='Jumlah Perincian Penggunaan Tanah')
	pematangan_tanah_tahap1 = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Pematangan Tanah Tahap 1')
	pematangan_tanah_tahap2 = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Pematangan Tanah Tahap 2')
	pematangan_tanah_tahap3 = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Pematangan Tanah Tahap 3')
	pembangunan_gedung_tahap1 = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Pembangunan Gedung Tahap 1')
	pembangunan_gedung_tahap2 = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Pembangunan Gedung Tahap 2')
	pembangunan_gedung_tahap3 = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Pembangunan Gedung Tahap 3')
	jangka_waktu_selesai = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Jangka Waktu Selesai')
	#Presentase Perincian Penggunaan Tanah
	presentase_luas_tipe1 = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Presentase Luas Tipe 1')
	presentase_luas_tipe2 = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Presentase Luas Tipe 2')
	presentase_luas_tipe3 = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Presentase Luas Tipe 3')
	presentase_luas_lapangan = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Presentase Luas Lapangan')
	presentase_luas_kantor = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Presentase Luas Kantor')
	presentase_luas_saluran = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Presentase Luas Saluran')
	presentase_luas_taman = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Presentase Luas Taman')
	presentase_jumlah_perincian_penggunaan_tanah = models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name='Presentase Jumlah Perincian Penggunaan Tanah')

	#Rencana Pembiayaan & Pemodalan
	modal_tetap_tanah = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Tetap Tanah')
	modal_tetap_bangunan = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Tetap Bangunan')
	modal_tetap_mesin = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Tetap Mesin - Mesin dan Peralatan')
	modal_tetap_angkutan = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Tetap Alat-alat Angkutan')
	modal_tetap_inventaris = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Tetap Alat-alat Kantor dan Inventaris')
	modal_tetap_lainnya = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Tetap Lainnya')
	jumlah_modal_tetap = models.CharField(max_length=20, null=True, blank=True, verbose_name='Jumlah Modal Tetap')

	modal_kerja_bahan = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Kerja Bahan Baku')
	modal_kerja_gaji = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Kerja Gaji/Upah')
	modal_kerja_alat_angkut = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Kerja Alat-alat Angkutan')
	modal_kerja_lainnya = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Kerja Lainnya')
	jumlah_modal_kerja = models.CharField(max_length=20, null=True, blank=True, verbose_name='Julah Modal Kerja')

	modal_dasar = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Dasar')
	modal_ditetapkan = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Ditetapkan')
	modal_disetor = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Disetor')
	modal_bank_pemerintah = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Bank Pemerintah')
	modal_bank_swasta = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Bank Swasta')
	modal_lembaga_non_bank = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Lembaga Non Bank')
	modal_pihak_ketiga = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Pihak Ketiga')
	modal_pinjaman_luar_negeri = models.CharField(max_length=15, null=True, blank=True, verbose_name='Modal Pinjaman Luar Negeri')
	jumlah_investasi = models.CharField(max_length=20, null=True, blank=True, verbose_name='Jumlah Investasi')

	saham_indonesia = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Saham Indonesia')
	saham_asing = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Saham Asing')

	#Kebutuhan Lainnya
	tenaga_ahli = models.IntegerField(verbose_name="Tenaga Ahli", null=True, blank=True)
	pegawai_tetap = models.IntegerField(verbose_name="Pegawai Tetap", null=True, blank=True)
	pegawai_harian_tetap = models.IntegerField(verbose_name="Pegawai Harian Tetap", null=True, blank=True)
	pegawai_harian_tidak_tetap = models.IntegerField(verbose_name="Pegawai Harian Tidak Tetap", null=True, blank=True)
	kebutuhan_listrik = models.IntegerField(verbose_name="Kebutuhan Listrik", null=True, blank=True)
	kebutuhan_listrik_sehari_hari = models.IntegerField(verbose_name="Kebutuhuan Listrik Sehari-Hari", null=True, blank=True)
	jumlah_daya_genset = models.IntegerField(verbose_name="Jumlah Daya Genset", null=True, blank=True)
	jumlah_listrik_kebutuhan_dari_pln = models.IntegerField(verbose_name="Jumlah Kebutuhan Listrik Dari PLN", null=True, blank=True)
	air_untuk_rumah_tangga = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Air Untuk Rumah Tangga')
	air_untuk_produksi = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Air Untuk Produksi')
	air_lainnya = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Untuk Lain-Lain')
	air_dari_pdam = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Air Dari PDAM')
	air_dari_sumber = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Air Dari Sumber')
	air_dari_sungai = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Air Dari Sungai')
	tenaga_kerja_wni = models.IntegerField(verbose_name="Tenaga Kerja WNI", null=True, blank=True)
	tenaga_kerja_wna = models.IntegerField(verbose_name="Tenaga Kerja WNA", null=True, blank=True)
	tenaga_kerja_tetap = models.IntegerField(verbose_name="Tenaga Kerja Tetap", null=True, blank=True)
	tenaga_kerja_tidak_tetap = models.IntegerField(verbose_name="Tenaga Kerja Tidak Tetap", null=True, blank=True)

	#Luas Tanah Yag Disetujui
	luas_tanah_yang_disetujui = models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name='Tanah Yang Disetujui')
	def __unicode__(self):
		return u'Detil Informasi Tanah %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Informasi Tanah'
		verbose_name_plural = 'Informasi Tanah'

# meta
class SertifikatTanah(MetaAtribut):
	informasi_tanah = models.ForeignKey(InformasiTanah, verbose_name="Informasi Tanah", null=True, blank=True)
	pengajuan_izin = models.ForeignKey(PengajuanIzin, verbose_name="Detil Pengajuan Izin",blank=True, null=True, related_name="sertifikat_tanah_pengajuan_izin")
	no_sertifikat_petak =  models.CharField(max_length=60, verbose_name='No. Sertifikat/Petak D', null=True, blank=True)
	luas_sertifikat_petak = models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name='Luas Sertifikat/Petak D')
	atas_nama_sertifikat_petak =  models.CharField(max_length=255, verbose_name='Atas Nama Sertifikat/Petak D', null=True, blank=True)
	tahun_sertifikat = models.DateField(verbose_name='Tanggal Sertifikat Tanah', null=True, blank=True)
	berkas_sertifikat = models.ForeignKey(Berkas, verbose_name="Berkas Sertifikat Tanah", related_name='berkas_sertifikat_tanah', blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (str(self.no_sertifikat_petak))

	def get_file_url(self):
		if self.berkas_sertifikat:
			return self.berkas_sertifikat.get_file_url()
		return "#"

	def as_dict(self):
		return {
			# "id": self.id,
			"no_sertifikat_petak": self.no_sertifikat_petak,
			"luas_sertifikat_petak": str(self.luas_sertifikat_petak),
			"atas_nama_sertifikat_petak": self.atas_nama_sertifikat_petak,
			"tahun_sertifikat": self.tahun_sertifikat.strftime("%d-%m-%Y"),

		}

	def as_json(self):
		return dict(no_sertifikat_petak=self.no_sertifikat_petak, luas_sertifikat_petak=str(self.luas_sertifikat_petak),atas_nama_sertifikat_petak=self.atas_nama_sertifikat_petak, tahun_sertifikat=self.tahun_sertifikat.strftime("%d-%m-%Y"))

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Sertifikat Tanah'
		verbose_name_plural = 'Sertifikat Tanah'

# meta
class AktaJualBeliTanah(MetaAtribut):
	informasi_tanah = models.ForeignKey(InformasiTanah, verbose_name="Informasi Tanah")
	no_jual_beli = models.CharField(max_length=255, verbose_name='No Jual Beli', null=True, blank=True)
	tanggal_jual_beli = models.DateField(verbose_name='Tanggal Jual Beli', null=True, blank=True)
	atas_nama_jual_beli = models.CharField(max_length=255, verbose_name='Atas Nama Jual Beli', null=True, blank=True)

	def __unicode__(self):
		return u'%s' % (str(self.no_jual_beli))
	
	def as_dict(self):
		return {
			# "id": self.id,
			"no_jual_beli": self.no_jual_beli,
			"tanggal_jual_beli": str(self.tanggal_jual_beli.strftime("%d-%m-%Y")),
			"atas_nama_jual_beli": self.atas_nama_jual_beli,
		}

	def as_json(self):
		return dict(no_jual_beli=self.no_jual_beli, tanggal_jual_beli=self.tanggal_jual_beli.strftime("%d-%m-%Y"),atas_nama_jual_beli=self.atas_nama_jual_beli)

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Akta Jual Beli Tanah'
		verbose_name_plural = 'Akta Jual Beli tanah'

# meta
class NoPTP(MetaAtribut):
	informasi_tanah = models.ForeignKey(InformasiTanah, verbose_name="Informasi Tanah")
	no_ptp = models.CharField(max_length=255, verbose_name='No PTP', null=True, blank=True)
	tanggal_ptp = models.DateField(verbose_name='Tanggal PTP', null=True, blank=True)

	def __unicode__(self):
		return u'%s' % (str(self.no_ptp))
	
	def as_dict(self):
		return {
			# "id": self.id,
			"no_ptp": self.no_ptp,
			"tanggal_ptp": str(self.tanggal_ptp.strftime("%d-%m-%Y")),
		}

	def as_json(self):
		return dict(no_ptp=self.no_ptp,tanggal_ptp=self.tanggal_ptp.strftime("%d-%m-%Y"))

	class Meta:
		# ordering = ['-status']
		verbose_name = 'No PTP'
		verbose_name_plural = 'No PTP'

# meta
class PenggunaanTanahIPPTUsaha(MetaAtribut):
	informasi_tanah = models.ForeignKey(InformasiTanah, verbose_name="Informasi Tanah")
	nama_penggunaan = models.CharField(max_length=20, verbose_name='Penggunaan Tanah', blank=True, null=True)
	ukuran_penggunaan = models.IntegerField(verbose_name="Ukuran Penggunaan", null=True, blank=True)

	def __unicode__(self):
		return u'%s' % (str(self.nama_penggunaan))
	
	def as_dict(self):
		return {
			# "id": self.id,
			"nama_penggunaan": self.nama_penggunaan,
			"ukuran_penggunaan": self.ukuran_penggunaan,

		}

	def as_json(self):
		return dict(nama_penggunaan=self.nama_penggunaan, ukuran_penggunaan=self.ukuran_penggunaan)

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Penggunaan Tanah IPPT Usaha'
		verbose_name_plural = 'Penggunaan Tanah IPPT Usaha'

# meta
class PerumahanYangDimilikiIPPTUsaha(MetaAtribut):
	informasi_tanah = models.ForeignKey(InformasiTanah, verbose_name="Informasi Tanah")
	nama_perumahan = models.CharField(max_length=20, verbose_name='Nama Perumahan', blank=True, null=True)
	luas_tanah = models.DecimalField(max_digits=5, decimal_places=2,default=0,verbose_name="Luas Tanah")
	status_tanah = models.CharField(verbose_name='Status Tanah', max_length=20, null=True, blank=True)
	desa = models.ForeignKey(Desa, verbose_name='Desa',null=True, blank=True)

	def __unicode__(self):
		return u'%s' % (str(self.nama_perumahan))

	def as_dict(self):
		return {
			# "id": self.id,
			"nama_perumahan": self.nama_perumahan,
			"luas_tanah": str(self.luas_tanah),
			"status_tanah": self.status_tanah,
			"desa": str(self.desa),
			"kecamatan": str(self.desa.kecamatan),

		}

	def as_json(self):
		desa = str(self.desa)
		kecamatan = str(self.desa.kecamatan)
		luas_tanah = str(self.luas_tanah)
		return dict(nama_perumahan=self.nama_perumahan, luas_tanah=luas_tanah,status_tanah= self.status_tanah,desa= desa,kecamatan= kecamatan)

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Perumahan Yang Sudah Dimiliki IPPT Usaha'
		verbose_name_plural = 'Perumahan Yang Sudah Dimiliki IPPT Usaha'


class DetilHuller(PengajuanIzin):
	perusahaan = models.ForeignKey('perusahaan.Perusahaan', related_name='detilhuller_perusahaan', blank=True, null=True)
	
	pemilik_badan_usaha = models.BooleanField(default=False) #Pemilik perorangan atau badan usaha, jika badan usaha wajib upload akta
	
	pemilik_nama_perorangan = models.CharField(max_length=50, verbose_name='Nama Lengkap Perorangan', null=True, blank=True)
	pemilik_alamat = models.CharField(max_length=255, verbose_name='Alamat Perorangan', null=True, blank=True)
	pemilik_desa = models.ForeignKey(Desa, verbose_name='Desa Perorangan', related_name='pemilik_desa',null=True, blank=True)
	pemilik_kewarganegaraan = models.CharField(max_length=100, null=True, blank=True)
	pemilik_nama_badan_usaha = models.CharField(max_length=50, verbose_name='Nama Badan Usaha Perorangan', null=True, blank=True)

	pengusaha_badan_usaha = models.BooleanField(default=False) #Pengusaha perorangan atau badan usaha, jika badan usaha wajib upload akta
	pengusaha_nama_perorangan = models.CharField(max_length=50, verbose_name='Nama Lengkap Pengusaha', null=True, blank=True)
	pengusaha_alamat = models.CharField(max_length=255, verbose_name='Alamat Pengusaha', null=True, blank=True)
	pengusaha_desa = models.ForeignKey(Desa, verbose_name='Desa Pengusaha', related_name='pengusaha_desa',null=True, blank=True)
	pengusaha_kewarganegaraan = models.CharField(max_length=100, null=True, blank=True)
	pengusaha_nama_badan_usaha = models.CharField(max_length=50, verbose_name='Nama Badan Usaha Pengusaha', null=True, blank=True)

	hubungan_pemilik_pengusaha = models.CharField(max_length=50, verbose_name='Hubungan kerjasama antara Pengusaha dengan Pemilik Perusahaan', null=True, blank=True)
	kapasitas_potensial_giling_beras_per_jam = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Kapasitas Potensial Giling Keseluruhan Mesin memproduksi Beras per Jam')
	kapasitas_potensial_giling_beras_per_tahun = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name='Kapasitas Potensial Giling Keseluruhan Mesin memproduksi Beras per Tahun')

	def __unicode__(self):
		return u'Detil Huller %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Huller'
		verbose_name_plural = 'Huller'

# meta
class JenisMesin(MetaAtribut):
	jenis_mesin = models.CharField(max_length=200, verbose_name='Jenis Mesin')
	keterangan = models.CharField(max_length=255,blank=True, null=True, verbose_name='Keterangan')

	def __unicode__(self):
		return u'%s' % (str(self.jenis_mesin),)

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Jenis Mesin'
		verbose_name_plural = 'Jenis Mesin'

# Parameter / Property untuk Mesin Huller Value ada di mesin perusahaan
# meta
class MesinHuller(MetaAtribut):
	jenis_mesin = models.ForeignKey(JenisMesin, verbose_name="Jenis Mesin")
	mesin_huller = models.CharField(max_length=200, verbose_name='Mesin Huller')
	keterangan = models.CharField(max_length=255, blank=True, null=True, verbose_name='Keterangan')

	def __unicode__(self):
		return u'%s - %s' % (str(self.jenis_mesin), str(self.mesin_huller))

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Mesin Huller'
		verbose_name_plural = 'Mesin Huller'

# meta
class MesinPerusahaan(MetaAtribut):
	detil_huller = models.ForeignKey(DetilHuller, verbose_name="Detil Huller")
	mesin_huller = models.ForeignKey(MesinHuller, verbose_name="Mesin Huller")

	type_model = models.CharField(max_length=255, verbose_name='Type / Model', blank=True, null=True)
	pk_mesin = models.CharField(max_length=255, verbose_name='PK', blank=True, null=True)
	buatan = models.CharField(max_length=255, verbose_name='Buatan / Merk', blank=True, null=True)
	jumlah_unit = models.IntegerField(verbose_name="Jumlah Unit", null=True, blank=True)
	# selain penggerak tambah kapasitas
	kapasitas = models.IntegerField(verbose_name="Kapasitas", null=True, blank=True)

	def __unicode__(self):
		return u'%s - %s' % (str(self.mesin_huller), str(self.detil_huller))

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Mesin Perusahaan'
		verbose_name_plural = 'Mesin Perusahaan'	

# ++++++++++++ TDUP ++++++++++++
class BidangUsahaPariwisata(models.Model):
	kode = models.CharField(max_length=10, verbose_name="Kode", null=True, blank=True)
	nama_bidang_usaha_pariwisata = models.CharField(max_length=255, verbose_name="Nama Bidang Usaha Pariwisata")
	keterangan = models.CharField(max_length=255, verbose_name="Keterangan", null=True, blank=True)

	def __unicode__(self):
		return u'%s' % (str(self.nama_bidang_usaha_pariwisata),)

	def as_json(self):
		return dict(id=self.id, nama_bidang_usaha_pariwisata=self.nama_bidang_usaha_pariwisata, keterangan=self.keterangan)

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.nama_bidang_usaha_pariwisata)+"</option>"

	class Meta:
		verbose_name = 'Bidang Usaha Pariwisata'
		verbose_name_plural = 'Bidang Usaha Pariwisata'

class JenisUsahaPariwisata(models.Model):
	kode = models.CharField(max_length=10, verbose_name="Kode", null=True, blank=True)
	bidang_usaha_pariwisata = models.ForeignKey(BidangUsahaPariwisata, verbose_name="Bidang Usaha Pariwisata")
	nama_jenis_usaha_pariwisata = models.CharField(max_length=255, verbose_name="Nama Jenis Usaha Pariwisata")
	keterangan = models.CharField(max_length=255, verbose_name="Keterangan", null=True, blank=True)

	def __unicode__(self):
		return u'%s' % (str(self.nama_jenis_usaha_pariwisata),)

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.nama_jenis_usaha_pariwisata)+"</option>"

	class Meta:
		verbose_name = 'Jenis Usaha Pariwisata'
		verbose_name_plural = 'Jenis Usaha Pariwisata'

class SubJenisUsahaPariwisata(models.Model):
	kode = models.CharField(max_length=10, verbose_name="Kode", null=True, blank=True)
	jenis_usaha_pariwisata = models.ForeignKey(JenisUsahaPariwisata, verbose_name="Jenis Usaha Pariwisata")
	nama_sub_jenis = models.CharField(max_length=255, verbose_name="Nama SubJenis")
	keterangan = models.CharField(max_length=255, verbose_name="Keterangan", null=True, blank=True)

	def __unicode__(self):
		return u'%s' % (str(self.nama_sub_jenis),)

	def as_json(self):
		return dict(id=self.id, kode=self.kode, nama_sub_jenis=self.nama_sub_jenis, keterangan=self.keterangan)

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.nama_sub_jenis)+"</option>"

	class Meta:
		ordering = ['id']
		verbose_name = 'Sub Jenis Usaha Pariwisata'
		verbose_name_plural = 'Sub Jenis Usaha Pariwisata'

class RincianSubJenis(models.Model):
	# transportasi wisata
	jumlah_unit_angkutan_jalan_wisata = models.IntegerField(verbose_name="Jumlah Unit Angkutan Jalan Wisata", null=True, blank=True)
	kapasitas_angkutan_jalan_wisata = models.IntegerField(verbose_name="Kapasitas Angkutan Jalan Wisata", null=True, blank=True)
	jumlah_unit_angkutan_kereta_api_wisata = models.IntegerField(verbose_name="Jumlah Unit Angkutan Kereta Api Wisata", null=True, blank=True)
	kapasitas_angkutan_kereta_api_wisata = models.IntegerField(verbose_name="Kapasitas Angkutan Kereta Api Wisata", null=True, blank=True)
	jumlah_unit_angkutan_sungai_dan_danau_wisata = models.IntegerField(verbose_name="Jumlah Unit Angkutan Sungai dan Danau Wisata", null=True, blank=True)
	kapasitas_angkutan_sungai_dan_danau_wisata = models.IntegerField(verbose_name="Kapasitas Angkutan Sungai dan Danau Wisata", null=True, blank=True)
	# jumlah_unit_angkutan_laut_domestik_wisata = models.IntegerField(verbose_name="Jumlah Unit Angkutan Laut Domestik Wisata", null=True, blank=True)
	# kapasitas_angkutan_laut_domestik_wisata = models.IntegerField(verbose_name="Kapasitas Angkutan Laut Domestik Wisata", null=True, blank=True)
	# jumlah_unit_angkutan_laut_internasional_wisata = models.IntegerField(verbose_name="Jumlah Unit Angkutan Laut Internasional Wisata", null=True, blank=True)
	# kapasitas_angkutan_laut_internasional_wisata = models.IntegerField(verbose_name="Kapasitas Angkutan Laut Internasional Wisata", null=True, blank=True)
	# makanan minuman
	jumlah_kursi_restoran = models.IntegerField(verbose_name="Jumlah Kursi Restoran", null=True, blank=True)
	jumlah_kursi_rumah_makan = models.IntegerField(verbose_name="Jumlah Kursi Rumah Makan", null=True, blank=True)
	jumlah_kursi_bar_atau_rumah_minum = models.IntegerField(verbose_name="Jumlah Kursi Bar / Rumah Minum", null=True, blank=True)
	jumlah_kursi_kafe = models.IntegerField(verbose_name="Jumlah Kursi Kafe", null=True, blank=True)
	jumlah_stand_pusat_makanan = models.IntegerField(verbose_name="Jumlah Stand Pusat Makanan", null=True, blank=True)
	kapasitas_produksi_jasa_boga = models.IntegerField(verbose_name="Jumlah Kursi Jasa Boga", null=True, blank=True)

	class Meta:
		verbose_name = 'Rincian Sub Jenis'
		verbose_name_plural = 'Rincian Sub Jenis'

class DetilTDUP(PengajuanIzin):
	perusahaan= models.ForeignKey('perusahaan.Perusahaan', related_name='tdup_perusahaan', blank=True, null=True)
	bidang_usaha_pariwisata = models.ForeignKey(BidangUsahaPariwisata, verbose_name="Bidang Usaha Pariwisata", null=True, blank=True)
	jenis_usaha_pariwisata = models.ForeignKey(JenisUsahaPariwisata, verbose_name="Jenis Usaha Pariwisata", null=True, blank=True)
	sub_jenis_usaha_pariwisata = models.ForeignKey(SubJenisUsahaPariwisata, verbose_name="Sub Jenis Usaha Pariwisata", null=True, blank=True)
	rincian_sub_jenis = models.OneToOneField(RincianSubJenis, verbose_name="Rincian Sub Jenis", null=True, blank=True)
	nama_usaha = models.CharField(max_length=255, verbose_name="Nama Usaha", null=True, blank=True)
	lokasi_usaha_pariwisata = models.CharField(max_length=255, verbose_name="Lokasi Usaha Pariwisata", null=True, blank=True)
	desa_lokasi = models.ForeignKey(Desa, verbose_name="Desa", null=True, blank=True)
	telephone = models.CharField(max_length=255, verbose_name="Telephone", null=True, blank=True)
	# Izin gangguan
	# nomor_izin_gangguan = models.CharField(max_length=255, verbose_name="Nomor Izin Gangguan", null=True, blank=True)
	# tanggal_izin_gangguan = models.DateField(verbose_name="Tanggal Izin Gangguan", null=True, blank=True)
	# izin_lain = models.ForeignKey(IzinLainTDUP, verbose_name='Izin Lain', null=True, blank=True)
	# Dokumen Pengelolaan Lingkungan
	nomor_dokumen_pengelolaan = models.CharField(max_length=255, verbose_name="Nomor Dokumen Pengelolaan Lingkungan", null=True, blank=True)
	tanggal_dokumen_pengelolaan = models.DateField(verbose_name="Tanggal Dokumen Pengelolaan Lingkungan", null=True, blank=True)
	berkas_npwp_perusahaan = models.ForeignKey(Berkas, verbose_name="Berkas NPWP Perusahaan", related_name='berkas_npwp_perusahaan_tdup', blank=True, null=True)
	kapasitas = models.CharField(max_length=255, verbose_name="Kapasitas", null=True, blank=True)

	def __unicode__(self):
		return u'Detil TDUP %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	def alamat_lengkap(self):
		data = ''
		if self.desa_lokasi and self.lokasi_usaha_pariwisata:
			data = str(self.lokasi_usaha_pariwisata)+self.desa_lokasi.lokasi_lengkap()
		return data

	class Meta:
		# ordering = ['-status']
		verbose_name = 'TDUP'
		verbose_name_plural = 'TDUP'

class PengurusBadanUsaha(models.Model):
	detil_tdup = models.ForeignKey(DetilTDUP, max_length=255, verbose_name='Detil TDUP', null=True, blank=True)
	nama_lengkap = models.CharField("Nama Lengkap", max_length=100, null=True, blank=True)
	alamat = models.CharField(max_length=255, null=True, blank=True)
	telephone = models.CharField(verbose_name='Telepon', max_length=50, null=True, blank=True)
	nomor_ktp = models.CharField(max_length=50, blank=True, null=True, verbose_name='Nomor KTP')
	keterangan = models.CharField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % str(self.nama_lengkap)

	def as_json(self):
		return dict(id=self.id, nomor_ktp=self.nomor_ktp, nama_lengkap=self.nama_lengkap, alamat=self.alamat, telephone=self.telephone, keterangan=self.keterangan)

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Pengurus Badan Usaha'
		verbose_name_plural = 'Pengurus Badan Usaha'

class IzinLainTDUP(models.Model):
	detil_tdup = models.ForeignKey(DetilTDUP, related_name='detil_tdup_izin_lain')
	no_izin = models.CharField(max_length=255, verbose_name='Nomor Izin')
	tanggal_izin = models.DateField(verbose_name="Tanggal Izin", null=True, blank=True)

	def as_json(self):
		tanggal_izin = ''
		if self.tanggal_izin:
			tanggal_izin = self.tanggal_izin.strftime("%d-%m-%Y")
		return dict(id=self.id, no_izin=self.no_izin, tanggal_izin=tanggal_izin)

	class Meta:
		verbose_name = 'Izin Lain TDUP'
		verbose_name_plural = 'Izin Lain TDUP'

class VasilitasTDUP(models.Model):
	detil_tdup = models.ForeignKey(DetilTDUP, related_name='detil_tdup_vasilitas_perusahaan')
	nama_vasilitas = models.CharField(max_length=255, verbose_name="Nama Vasilitas", null=True, blank=True)
	jumlah = models.IntegerField(verbose_name="Jumlah Vasilitas", default=0, null=True, blank=True)

	def as_json(self):
		return dict(id=self.id, nama_vasilitas=self.nama_vasilitas, jumlah=self.jumlah)

	class Meta:
		verbose_name = 'Vasilitas TDUP'
		verbose_name_plural = 'Vasilitas TDUP'


# ++++++++++++ end TDUP ++++++++++++
class BankPembayaran(models.Model):
	nama_bank = models.CharField(max_length=255, verbose_name="Nama Bank")
	nomor_rekening = models.CharField(max_length=255, verbose_name="Nomor Rekening", null=True, blank=True)
	aktif = models.BooleanField(default=True, verbose_name="Apakah dipakai untuk pembayaran ?")
	keterangan = models.CharField(max_length=255, verbose_name="Keterangan", null=True, blank=True)

	def __unicode__(self):
		return u'%s' % str(self.nama_bank)

	class Meta:
		verbose_name = 'Bank Pembayaran'
		verbose_name_plural = 'Bank Pembayaran'

# Detil Pembayaran Izin
# meta
class DetilPembayaran(MetaAtribut):
	kode = models.CharField(max_length=16, verbose_name="Kode", null=True, blank=True)
	pengajuan_izin = models.ForeignKey(PengajuanIzin, verbose_name="Detil Pengajuan Izin",blank=True, null=True)
	tanggal_bayar = models.DateField(verbose_name="Tanggal Bayar", null=True, blank=True)
	tanggal_deadline = models.DateField(verbose_name="Tanggal Deadline", null=True, blank=True)
	tanggal_dibuat = models.DateField(verbose_name="Tanggal Dibuat", null=True, blank=True)
	nomor_kwitansi = models.CharField(max_length=255, verbose_name='Nomor Kwitansi', null=True, blank=True)
	jumlah_pembayaran = models.CharField(max_length=255, verbose_name='Jumlah Pembayaran', null=True, blank=True)
	peruntukan = models.CharField(max_length=255, verbose_name="Peruntukan", null=True, blank=True)
	bank_pembayaran = models.ForeignKey(BankPembayaran, null=True, blank=True, verbose_name="Bank Pembayaran")
	terbayar = models.BooleanField(default=False, verbose_name="Apakah pembayaran sudah terbayar ?")
	# pembayaran piutang
	nama_pemohon = models.CharField(max_length=255, verbose_name="Nama Pemohon", null=True, blank=True, help_text="Jika retribusi piutang isi nama pemohon.")
	nama_perusahaan = models.CharField(max_length=255, verbose_name="Nama Perusahaan", null=True, blank=True, help_text="Jika retribusi piutang isi nama perusahaan.")
	alamat_usaha = models.CharField(max_length=255, verbose_name="Alamat Usaha", null=True, blank=True)
	piutang = models.BooleanField(verbose_name="Apakah pembayaran piutang ?", default=False)

	def __unicode__(self):
		return u'Detil Pembayaran %s' % (str(self.pengajuan_izin))

	def bank(self):
		bank = None
		if self.bank_pembayaran:
			bank = self.bank_pembayaran.nama_bank
		return bank

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Detil Pembayaran'
		verbose_name_plural = 'Detil Pembayaran'

	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		# if not self.id:
		""" tanggal dateline otomatis 3 bulan dari pembuatan kwitansi """
		import datetime
		from utils import generate_kode_bank_jatim
		self.tanggal_deadline = datetime.date.today() + datetime.timedelta(3*365/12)
		# jumlah_data = DetilPembayaran.objects.filter(created_at__gte=datetime.date.today()).count()+1
		# self.kode = generate_kode_bank_jatim(jumlah_data)
		return super(DetilPembayaran, self).save(*args, **kwargs)

# +++++++++++++ LPK Sw ++++++++++++
class SumberBiayaPelatihan(models.Model):
	sumber_dana = models.CharField(max_length=255, verbose_name='Sumber Dana Pelatihan') # siswa, sponsor, subsidi, lembaga sendiri
	keterangan = models.CharField(max_length=255, verbose_name='Keterangan', null=True, blank=True)

	def __unicode__(self):
		return u'%s' % (str(self.sumber_dana))

	class Meta:
		ordering = ['-id']
		verbose_name = 'Sumber Biaya Pelatihan'
		verbose_name_plural = 'Sumber Biaya Pelatihan'

class DetilLPKSW(PengajuanIzin):
	# metode pelatihan
	ceramah = models.BooleanField(default=False, verbose_name='Metode Pelatihan Ceramah')
	diskusi = models.BooleanField(default=False, verbose_name='Metode Pelatihan Diskusi')
	praktek = models.BooleanField(default=False, verbose_name='Metode Pelatihan Praktek')
	lain_lain = models.BooleanField(default=False, verbose_name='Metode Pelatihan Lain-lain')
	# metode pelatihan
	ruang_kantor = models.CharField(max_length=30, verbose_name='Ruang Kantor', null=True, blank=True)
	ruang_praktek = models.CharField(max_length=30, verbose_name='Ruang Praktek', null=True, blank=True)
	ruang_teori = models.CharField(max_length=30, verbose_name='Ruang Teori', null=True, blank=True)
	ruang_lain = models.CharField(max_length=30, verbose_name='Ruang Lain-lain', null=True, blank=True)

	# lain lain
	pencari_kerja = models.BooleanField(default=False, verbose_name='Sumber Siswa Pencari Kerja')
	karyawan = models.BooleanField(default=False, verbose_name='Sumber Siswa Karyawan')
	# ++ umur siswa
	umur_dari = models.CharField(max_length=10, verbose_name='Umur Dari', null=True, blank=True)
	umur_sampai = models.CharField(max_length=10, verbose_name='Umur Sampai', null=True, blank=True)
	# ++ umur siswa
	sumber_dana_pelatihan = models.ManyToManyField(SumberBiayaPelatihan, verbose_name='Sumber Dana')

	# lain lain

	def __unicode__(self):
		return u'Detil LPKSW %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Detil LPKSW'
		verbose_name_plural = 'Detil LPKSW'

class JenisProgramPelatihan(models.Model):
	detil_lpksw = models.ForeignKey(DetilLPKSW, verbose_name='Detil LPK Sw')
	jenis_program = models.CharField(max_length=255, verbose_name='Jenis Program', null=True, blank=True)
	lama_pelatihan = models.CharField(max_length=255, verbose_name='Lama Pelatihan (Jam)', null=True, blank=True)
	jumlah_peserta_per_grup = models.IntegerField(verbose_name='Jumlah Peserta per Grup', null=True, blank=True)
	jumlah_peserta_per_tahun = models.IntegerField(verbose_name='Jumlah Peserta per Tahun', null=True, blank=True)
	biaya_pelatihan_per_orang = models.CharField(max_length=255, verbose_name='Biaya Pelatihan per Orang (Rp)', null=True, blank=True)
	keterangan = models.CharField(max_length=255, verbose_name='Keterangan', null=True, blank=True)

	def __unicode__(self):
		return u'%s' % (str(self.jenis_program))

	class Meta:
		ordering = ['-id']
		verbose_name = 'Jenis Program Pelatihan'
		verbose_name_plural = 'Jenis Program Pelatihan'

class MesinPeralatan(models.Model):
	detil_lpksw = models.ForeignKey(DetilLPKSW, verbose_name='Detil LPK Sw')
	mesin_peralatan = models.CharField(max_length=255, verbose_name='Mesin atau Peralatan', choices=JENIS_MESIN_PERALATAN)
	jenis_mesin = models.CharField(max_length=255, verbose_name='Jenis Mesin', null=True, blank=True)
	jumlah_mesin_baik = models.CharField(max_length=255, verbose_name='Jumlah Mesin Baik', null=True, blank=True)
	jumlah_mesin_rusak_ringan = models.CharField(max_length=255, verbose_name='Jumlah Mesin Rusak Ringan', null=True, blank=True)
	jumlah_mesin_rusak_berat = models.CharField(max_length=255, verbose_name='Jumlah Mesin Rusak Berat', null=True, blank=True)
	jumlah_total = models.CharField(max_length=255, verbose_name='Jumlah Total', null=True, blank=True)

	def __unicode__(self):
		return u'%s' % (str(self.mesin_peralatan))

	class Meta:
		ordering = ['-id']
		verbose_name = 'Mesin Peralatan'
		verbose_name_plural = 'Mesin Peralatan'

class Instruktur(models.Model):
	detil_lpksw = models.ForeignKey(DetilLPKSW, verbose_name='Detil LPK Sw')
	jenis_pelatihan = models.CharField(max_length=255, verbose_name='Jenis Pelatihan')
	jumlah_instruktur = models.IntegerField(verbose_name='Jumlah Intruktur', null=True, blank=True)
	jumlah_kualifikasi_baik = models.IntegerField(verbose_name='Jumlah Kualifikasi Baik', null=True, blank=True)
	jumlah_kualifikasi_cukup = models.IntegerField(verbose_name='Jumlah Kualifikasi Cukup', null=True, blank=True)
	jumlah_status_tetap = models.IntegerField(verbose_name='Jumlah Status Tetap', null=True, blank=True)
	jumlah_status_tidak_tetap = models.IntegerField(verbose_name='Jumlah Status Tidak Tetap', null=True, blank=True)
	jumlah_pria = models.IntegerField(verbose_name='Jumlah Pria', null=True, blank=True)
	jumlah_wanita = models.IntegerField(verbose_name='Jumlah Wanita', null=True, blank=True)
	keterangan = models.CharField(max_length=255, verbose_name='Keterangan', null=True, blank=True)

	def __unicode__(self):
		return u'%s' % (str(self.jenis_pelatihan))

	class Meta:
		ordering = ['-id']
		verbose_name = 'Instruktur'
		verbose_name_plural = 'Instruktur'

class IdentitasInstruktur(models.Model):
	detil_lpksw = models.ForeignKey(DetilLPKSW, verbose_name='Detil LPK Sw')
	nama = models.CharField(max_length=255, verbose_name='Nama Instruktur', null=True, blank=True)
	umur = models.IntegerField(verbose_name='Umur', null=True, blank=True)
	pendidikan = models.CharField(max_length=255, verbose_name='Pendidikan', null=True, blank=True)
	pelatihan_teknis_dibidangnya = models.CharField(max_length=255, verbose_name='Pelatihan Teknis Dibidangnya', null=True, blank=True)
	pengalaman_teknis_dibidangnya = models.CharField(max_length=255, verbose_name='Pengalaman Teknis Dibidangnya', null=True, blank=True)
	keterangan = models.CharField(max_length=255, verbose_name='Keterangan', null=True, blank=True)

	def __unicode__(self):
		return u'%s' % (str(self.jenis_pelatihan))

	class Meta:
		ordering = ['-id']
		verbose_name = 'Identitas Instruktur'
		verbose_name_plural = 'Identitas Instruktur'
# +++++++++++++ end LPK Sw ++++++++

# ++++++++++++ IPCTKI +++++++++
class DetilIPCTKI(PengajuanIzin):

	def __unicode__(self):
		return u'Detil IPCTKI %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Detil IPCTKI'
		verbose_name_plural = 'Detil IPCTKI'
# ++++++++++++ end IPCTKI +++++++++

# ++++++++++++ UP3CTKI +++++++++++++++
class DetilUP3CTKI(PengajuanIzin):

	def __unicode__(self):
		return u'Detil UP3CTKI %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Detil UP3CTKI'
		verbose_name_plural = 'Detil UP3CTKI'
# ++++++++++++ end UP3CTKI +++++++++++

# ++++++++++++ TDG +++++++++++++++++
# models Detil TDG belum selsai mockup ruwet :D
class DetilTDG(PengajuanIzin):
	lokasi_gudang = models.CharField(max_length=255, verbose_name='Lokasi Gudang', null=True, blank=True)
	desa_lokasi = models.ForeignKey(Desa, verbose_name='Lokasi Desa', null=True, blank=True)
	luas_gudang = models.CharField(max_length=255, verbose_name='Luas Gudang m2', null=True, blank=True)
	kapasitas = models.CharField(max_length=255, verbose_name='Kapasitas', null=True, blank=True)
	nilai_gudang = models.CharField(max_length=255, verbose_name='Nilai Gudang (Rp)', null=True, blank=True)
	# kapasitas kepemilikan
	nasional = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True, verbose_name='Presentase Kepemilikan Nasional')
	asing = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True, verbose_name='Presentase Kepemilikan Asing')
	# kota/kab label salah dimockup
	# berpendingin, tidak berpendingin, keduanya
	# kota = models.CharField()

	jenis_isi_gudang = models.TextField(verbose_name='Macam dan Jenis Isi Gudang', null=True, blank=True)
# ++++++++++++ end TDG +++++++++++++

# +++++++++++ IUTM +++++++++++++
class DetilIUTM(PengajuanIzin):
	modal = models.CharField(max_length=255, verbose_name='Modal', null=True, blank=True)
	total_nilai_saham = models.CharField(max_length=255, null=True, blank=True, verbose_name='Total Nilai Saham')
	presentase_saham_nasional = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True, verbose_name='Presentase Saham Nasional')
	presentase_saham_asing = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True, verbose_name='Presentase Saham Asing')
	# status_penanaman_modal = models

	# identitas perbelanjaan
	nama_perbelanjaan = models.CharField(max_length=255, verbose_name='Nama Perbelanjaan', null=True, blank=True)
	luas_tanah = models.CharField(max_length=255, verbose_name='Luas Tanah (m2)', null=True, blank=True)
	luas_bangunan = models.CharField(max_length=255, verbose_name='Luas Bangunan (m2)', null=True, blank=True)
	luas_lantai_penjualan = models.CharField(max_length=255, verbose_name='Luas Lantai Penjualan (m2)', null=True, blank=True)
	luas_lantai_parkir = models.CharField(max_length=255, verbose_name='Luas Lantai Parkir (m2)', null=True, blank=True)
	kapasitas_parkir = models.CharField(max_length=255, verbose_name='Kapasitas Parkir (Roda Empat)', null=True, blank=True)
	alamat_lokasi = models.CharField(max_length=255, verbose_name='Alamat Lokasi', null=True, blank=True)
	desa_lokasi = models.ForeignKey(Desa, verbose_name='Lokasi Desa', null=True, blank=True)

	def __unicode__(self):
		return u'Detil IUTM %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		# ordering = ['-status']
		verbose_name = 'Detil IUTM'
		verbose_name_plural = 'Detil IUTM'
# +++++++++++ end IUTM +++++++++++++

#### Izin Dinas Perhubungan ####

class KategoriKendaraan(models.Model):
	# Mobil barang, angkutan orang
	nama_kategori = models.CharField(max_length=255, verbose_name='Nama Kategori')
	keterangan = models.CharField(max_length=255, verbose_name='keterangan', null=True, blank=True)

	def __unicode__(self):
		return u'%s' % str(self.nama_kategori)

	class Meta:
		verbose_name = 'Kategori Kendaraan'
		verbose_name_plural = 'Kategori Kendaraan'

class MerkTypeKendaraan(models.Model):
	nama_type = models.CharField(max_length=255, verbose_name='Nama Type')
	keterangan = models.CharField(max_length=255, verbose_name='Keterangan', null=True, blank=True)

	def __unicode__(self):
		return u'%s' % str(self.nama_type)

	class Meta:
		verbose_name = 'Merk Type'
		verbose_name_plural = 'Merk Type'

class DetilIUA(PengajuanIzin):
	perusahaan= models.ForeignKey('perusahaan.Perusahaan', related_name='iua_perusahaan', blank=True, null=True)
	nilai_investasi = models.CharField(max_length=255, verbose_name='Nilai Investasi', null=True, blank=True)
	kategori_kendaraan = models.ForeignKey(KategoriKendaraan, max_length=255, verbose_name='Nama Kategori', null=True, blank=True)
	detil_ho = models.ForeignKey(DetilHO, max_length=255, verbose_name='Nomor Izin HO', null=True, blank=True)
	# berkas_npwp_perusahaan = models.ForeignKey(Berkas, verbose_name="Berkas NPWP Perusahaan", related_name='berkas_npwp_perusahaan_iua', blank=True, null=True)

	def as_json(self):
		nilai_investasi = ''
		if self.nilai_investasi:
			nilai_investasi = self.nilai_investasi
		kategori_kendaraan = ''
		if self.kategori_kendaraan:
			kategori_kendaraan = self.kategori_kendaraan.nama_kategori
		detil_ho = ''
		if self.detil_ho:
			detil_ho = self.detil_ho.no_izin
		return dict(nilai_investasi=nilai_investasi, kategori_kendaraan=kategori_kendaraan, kategori_kendaraan_id=self.kategori_kendaraan_id, id=self.id)

	def __unicode__(self):
		return u'Detil IUA %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		verbose_name = 'Detil IUA'
		verbose_name_plural = 'Detil IUA'

class Trayek(models.Model):
	trayek = models.CharField(max_length=100, verbose_name='Trayek')
	jurusan = models.CharField(max_length=255, verbose_name='Jurusan')
	rute_dilewati = models.TextField(verbose_name='Rute dilewati')
	jumlah_mpu =models.CharField(max_length=255, verbose_name="Jumlah MPU", null=True, blank=True)

	def __unicode__(self):
		return u'%s' % str(self.trayek)

	class Meta:
		verbose_name = 'Trayek'
		verbose_name_plural = 'Trayek'

class Kendaraan(models.Model):
	pengajuan_izin = models.ForeignKey(PengajuanIzin, max_length=255, verbose_name='Pengajuan Izin', null=True, blank=True)
	nomor_kendaraan = models.CharField(max_length=255, verbose_name='Nomor Kendaraan', null=True, blank=True)
	nomor_uji_berkala = models.CharField(max_length=255, verbose_name='Nomor Uji Berkala', null=True, blank=True)
	merk_kendaraan = models.ForeignKey(MerkTypeKendaraan, max_length=255, verbose_name='Merk Kendaraan', null=True, blank=True)
	berat_diperbolehkan = models.CharField(max_length=255, verbose_name='Berat diperbolehkan', null=True, blank=True)
	nomor_rangka = models.CharField(max_length=255, verbose_name='Nomor Rangka', null=True, blank=True)
	nomor_mesin = models.CharField(max_length=255, verbose_name='Nomor Mesin', null=True, blank=True)
	trayek = models.ForeignKey(Trayek, verbose_name='Trayek', null=True, blank=True)
	tahun_pembuatan = models.CharField(max_length=255, verbose_name='Tahun Pembuatan', null=True, blank=True)
	keterangan = models.CharField(max_length=255, verbose_name='keterangan', null=True, blank=True)
	berkas_stnk = models.ForeignKey(Berkas, verbose_name="Berkas STNK", related_name='berkas_scan_stnk', blank=True, null=True)
	berkas_kartu_pengawasan = models.ForeignKey(Berkas, verbose_name="Berkas Kartu Pengawasan", related_name='berkas_kartu_pengawasan', blank=True, null=True)

	def as_json(self):
		merk_kendaraan_nama = ''
		if self.merk_kendaraan:
			if self.merk_kendaraan.nama_type:
				merk_kendaraan_nama = self.merk_kendaraan.nama_type
		nomor_rangka = ''
		if self.nomor_rangka:
			nomor_rangka = self.nomor_rangka
		tahun_pembuatan = ''
		if self.tahun_pembuatan:
			tahun_pembuatan = self.tahun_pembuatan
		berkas_stnk_nama = ''
		berkas_stnk = None
		if self.berkas_stnk:
			berkas_stnk_nama = self.berkas_stnk.nama_berkas
			berkas_stnk = self.berkas_stnk.get_file_url()
		berkas_kartu_pengawasan = None
		berkas_kartu_pengawasan_nama = ''
		if self.berkas_kartu_pengawasan:
			berkas_kartu_pengawasan_nama = self.berkas_kartu_pengawasan.nama_berkas
			berkas_kartu_pengawasan = self.berkas_kartu_pengawasan.get_file_url()
		trayek = ""
		if self.trayek:
			trayek = self.trayek.trayek+" - "+self.trayek.jurusan
		return dict(id=self.id, nomor_kendaraan=self.nomor_kendaraan, nomor_uji_berkala=self.nomor_uji_berkala, merk_kendaraan_nama=merk_kendaraan_nama, berat_diperbolehkan=self.berat_diperbolehkan, nomor_rangka=nomor_rangka, nomor_mesin=self.nomor_mesin, tahun_pembuatan=tahun_pembuatan, keterangan=self.keterangan, berkas_stnk=berkas_stnk, berkas_kartu_pengawasan=berkas_kartu_pengawasan, berkas_stnk_nama=berkas_stnk_nama, berkas_kartu_pengawasan_nama=berkas_kartu_pengawasan_nama, trayek=trayek)

	def __unicode__(self):
		return u'%s' % str(self.nomor_kendaraan)

	class Meta:
		verbose_name = 'Kendaraan'
		verbose_name_plural = 'Kendaraan'

class DetilTrayek(PengajuanIzin):
	detil_iua = models.ForeignKey(DetilIUA, verbose_name='Nomor Izin Angkutan', null=True, blank=True)
	perusahaan= models.ForeignKey('perusahaan.Perusahaan', related_name='trayek_perusahaan', blank=True, null=True)
	nilai_investasi = models.CharField(max_length=255, verbose_name='Nilai Investasi', null=True, blank=True)
	kategori_kendaraan = models.ForeignKey(KategoriKendaraan, max_length=255, verbose_name='Nama Kategori', null=True, blank=True)
	detil_ho = models.ForeignKey(DetilHO, max_length=255, verbose_name='Nomor Izin HO', null=True, blank=True)
	berkas_npwp_perusahaan = models.ForeignKey(Berkas, verbose_name="Berkas NPWP Perusahaan", related_name='berkas_npwp_perusahaan_trayek', blank=True, null=True)

	def as_json(self):
		nilai_investasi = ''
		if self.nilai_investasi:
			nilai_investasi = self.nilai_investasi
		kategori_kendaraan = ''
		if self.kategori_kendaraan:
			kategori_kendaraan = self.kategori_kendaraan.nama_kategori
		detil_ho = ''
		if self.detil_ho:
			detil_ho = self.detil_ho.no_izin
		return dict(nilai_investasi=nilai_investasi, kategori_kendaraan=kategori_kendaraan, kategori_kendaraan_id=self.kategori_kendaraan_id, id=self.id)

	def __unicode__(self):
		return u'Detil Izin Trayek %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	class Meta:
		verbose_name = 'Trayek'
		verbose_name_plural = 'Trayek'


class DetilIzinParkirIsidentil(PengajuanIzin):
	jenis_penitipan = models.CharField(max_length=100, verbose_name='Jenis Penitipan', null=True, blank=True)
	lebar_penitipan = models.CharField(max_length=20, verbose_name='Luas Penitipan M', null=True, blank=True)
	panjang_penitipan = models.CharField(max_length=20, verbose_name='Panjang Penitipan M', null=True, blank=True)
	desa = models.ForeignKey(Desa, verbose_name='Desa', null=True, blank=True)
	alamat = models.CharField(max_length=150, verbose_name='Alamat', null=True, blank=True)
	tanggal_pelaksanaan_parkir = models.DateField(verbose_name="Tanggal Pelaksanaan Parkir", null=True, blank=True)
	waktu_mulai = models.TimeField(verbose_name='Waktu Mulai', auto_now=False, auto_now_add=False, null=True, blank=True)
	waktu_berakhir = models.TimeField(verbose_name='Waktu Berakhir', auto_now=False, auto_now_add=False, null=True, blank=True)
	jumlah_anggota_parkir = models.CharField(max_length=20, verbose_name='Jumlah Anggota Parkir', null=True, blank=True)
	batas_utara = models.CharField(max_length=150, blank=True, null=True, verbose_name='Batas Utara')
	batas_timur = models.CharField(max_length=150, blank=True, null=True, verbose_name='Batas Timur')
	batas_selatan = models.CharField(max_length=150, blank=True, null=True, verbose_name='Batas Selatan')
	batas_barat = models.CharField(max_length=150, blank=True, null=True, verbose_name='Batas Barat')

	def __unicode__(self):
		return u'Detil Izin Parkir Isidentil %s - %s' % (str(self.kelompok_jenis_izin), str(self.jenis_permohonan))

	def get_lama_penitipan(self):
		lama_pelatihan = ""
		if self.tanggal_pelaksanaan_parkir and self.waktu_mulai and self.waktu_berakhir:
			lama_pelatihan = "Tanggal "+self.tanggal_pelaksanaan_parkir.strftime("%d-%m-%Y")+" , "+self.waktu_mulai.strftime("%H:%M")+" sampai dengan "+self.waktu_berakhir.strftime("%H:%M")
		return lama_pelatihan

	def as_json(self):
		alamat_lengkap = ''
		if self.desa and self.alamat:
			alamat_lengkap = str(self.alamat)+self.desa.lokasi_lengkap()
		desa = ''
		if self.desa:
			desa = self.desa.as_json()
		tanggal_pelaksanaan_parkir = ''
		if self.tanggal_pelaksanaan_parkir:
			tanggal_pelaksanaan_parkir = self.tanggal_pelaksanaan_parkir.strftime("%d-%m-%Y")
		waktu_mulai = ''
		if self.waktu_mulai:
			waktu_mulai = self.waktu_mulai.strftime("%H:%M")
		waktu_berakhir = ''
		if self.waktu_berakhir:
			waktu_berakhir = self.waktu_berakhir.strftime("%H:%M")

		return dict(jenis_penitipan=self.jenis_penitipan, lebar_penitipan=self.lebar_penitipan, panjang_penitipan=self.panjang_penitipan, desa=desa, alamat=self.alamat, tanggal_pelaksanaan_parkir=tanggal_pelaksanaan_parkir, waktu_mulai=waktu_mulai, waktu_berakhir=waktu_berakhir, jumlah_anggota_parkir=self.jumlah_anggota_parkir, batas_utara=self.batas_utara, batas_timur=self.batas_timur, batas_selatan=self.batas_selatan, batas_barat=self.batas_barat, alamat_lengkap=alamat_lengkap)

	class Meta:
		verbose_name = 'Detil Izin Parkir Isidentil'
		verbose_name_plural = 'Detil Izin Parkir Isidentil'

class DataAnggotaParkir(IdentitasPribadi):
	izin_parkir_isidentil = models.ForeignKey(DetilIzinParkirIsidentil, max_length=255, verbose_name='Izin Usaha Parkir', null=True, blank=True)
	nomor_ktp = models.CharField(max_length=50, blank=True, null=True, verbose_name='Nomor KTP')
	# nama_anggota = models.CharField(max_length=150, blank=True, null=True, verbose_name='Nama Anggota')
	# tanggal_lahir = models.DateField(verbose_name="Tanggal Lahir",null=True, blank=True)
	# alamat = models.CharField(max_length=150, blank=True, null=True, verbose_name='Alamat')
	# no_hp_telepon = models.CharField(max_length=150, blank=True, null=True, verbose_name='No HP/Telpon')
	# keterangan = models.CharField(max_length=150, blank=True, null=True, verbose_name='Keterangan')
	
	def __unicode__(self):
		return u'%s' % str(self.nama_lengkap)

	def as_json(self):
		nomor_ktp = '-'
		if self.nomor_ktp:
			nomor_ktp = self.nomor_ktp
		tanggal_lahir = '-'
		if self.tanggal_lahir:
			tanggal_lahir = self.tanggal_lahir.strftime("%d-%m-%Y")
		alamat = '-'
		if self.alamat:
			alamat = self.alamat
		telephone = '-'
		if self.telephone:
			telephone = self.telephone
		keterangan = '-'
		if self.keterangan:
			keterangan = self.keterangan
		return dict(id=self.id, nama_lengkap=self.nama_lengkap, nomor_ktp=nomor_ktp, tanggal_lahir=tanggal_lahir, alamat=alamat, telephone=telephone, keterangan=keterangan)

	class Meta:
		verbose_name = 'Data Anggota Izin Parkir Isidentil'
		verbose_name_plural = 'Data Anggota Parkir Isidentil'


class DetilBangunanIMB(MetaAtribut):
	detil_izin_imb = models.ForeignKey(DetilIMB,verbose_name="Detil Izin IMB",blank=True, null=True,)
	detil_bangunan_imb = models.ForeignKey(BangunanJenisKontruksi,verbose_name="Detil Bangunan IMB",blank=True, null=True,)
	parameter_bangunan = models.ManyToManyField(ParameterBangunan,verbose_name="Parameter Bangunan",blank=True)
	total_luas = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Total Luas')
	satuan_luas = models.CharField(verbose_name='Satuan Luas', choices=SATUAN, max_length=10, null=True, blank=True)
	total_biaya_detil = models.CharField(max_length=20, null=True, blank=True, verbose_name='Total Biaya')

	def as_json(self):
		jenis_kontruksi = '-'
		if self.detil_bangunan_imb:
			jenis_kontruksi = self.detil_bangunan_imb.jenis_kontruksi.nama_jenis_kontruksi
		bangunan_imb = '-'
		if self.detil_bangunan_imb:
			bangunan_imb = self.detil_bangunan_imb.nama_bangunan
		total_biaya_detil = '-'
		if self.total_biaya_detil:
			total_biaya_detil = str(self.total_biaya_detil)

		return dict(id=self.id, jenis_kontruksi=jenis_kontruksi, bangunan_imb=bangunan_imb, total_biaya_detil=total_biaya_detil,)

	class Meta:
		verbose_name = 'Detil Bangunan IMB'
		verbose_name_plural = 'Detil Bangunan IMB'


# class Retribusi(MetaAtribut):
# 	pengajuan_izin = models.ForeignKey(PengajuanIzin, verbose_name="Pengajuan Izin")
# 	kode = models.CharField(max_length=255, verbose_name="Kode Retribusi", unique=True)
# 	peruntukan = models.CharField(max_length=255, verbose_name="Peruntukan", null=True, blank=True)
# 	total_bayar = models.CharField(max_length=100, verbose_name="Total Bayar")
# 	tanggal_bayar = models.DateField(verbose_name="Tanggal Bayar", null=True, blank=True)
# 	tanggal_deadline = models.DateField(verbose_name="Tanggal Deadline", null=True, blank=True)
# 	bank = models.CharField(max_length=255, verbose_name="BANK", null=True, blank=True)

# 	def as_json(self):
# 		tanggal_bayar = ""
# 		if self.tanggal_bayar:
# 			tanggal_bayar = self.tanggal_akhir.strftime("%d-%m-%Y")
# 		tanggal_deadline = ""
# 		if self.tanggal_deadline:
# 			tanggal_deadline = self.tanggal_deadline.strftime("%d-%m-%Y")
# 		return dict(kode=self.kode, peruntukan=self.peruntukan, total_bayar=self.total_bayar, tanggal_bayar=tanggal_bayar, tanggal_deadline=tanggal_deadline)

# 	class Meta:
# 		verbose_name = "Retribusi"
# 		verbose_name_plural = "Retribusi"

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
