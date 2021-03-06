from django.db import models
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from datetime import datetime

from accounts.utils import STATUS, get_status_color
# from izin.models import DetilIMB

class Template(models.Model):
	kelompok_jenis_izin = models.ForeignKey('izin.KelompokJenisIzin', verbose_name='Kelompok Jenis Izin', related_name="survey_iujk", blank=True, null=True)
	body_html = RichTextField()

	def __unicode__(self):
		return '%s' % mark_safe(self.kelompok_jenis_izin)

	class Meta:
		ordering = ['id']
		verbose_name = 'Template'
		verbose_name_plural = 'Template'

class JenisKualifikasi(models.Model):
	nama_kualifikasi = models.CharField(max_length=255, verbose_name='Nama Kualifikasi')
	
	def __unicode__(self):
		return "%s" % (self.nama_kualifikasi)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Kualifikasi IUJK'
		verbose_name_plural = 'Jenis Kualifikasi IUJK'

class JenisReklame(models.Model):
	jenis_reklame = models.CharField(max_length=255, verbose_name='Jenis Reklame')
	keterangan = models.CharField(max_length=255, blank=True, null=True)
	
	def __unicode__(self):
		return "%s" % (self.jenis_reklame)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Reklame'
		verbose_name_plural = 'Jenis Reklame'

class JenisTipeReklame(models.Model):
	jenis_tipe_reklame = models.CharField(max_length=255, verbose_name='Jenis Tipe Reklame')
	keterangan = models.CharField(max_length=255, blank=True, null=True)
	
	def __unicode__(self):
		return "%s" % (self.jenis_tipe_reklame)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Tipe Reklame'
		verbose_name_plural = 'Jenis Tipe Reklame'


class MetaAtribut(models.Model):
	status = models.PositiveSmallIntegerField(verbose_name='Status Data', choices=STATUS, default=6)
	# created_by = models.ForeignKey("accounts.Account", related_name="create_by_user", verbose_name="Dibuat Oleh", blank=True, null=True)
	created_by = models.ForeignKey("accounts.Account", related_name="%(app_label)s_%(class)s_create_by_user", verbose_name="Dibuat Oleh", blank=True, null=True)
	created_at = models.DateTimeField(editable=False)
	# verified_by = models.ForeignKey("accounts.Account", related_name="verify_by_user", verbose_name="Diverifikasi Oleh", blank=True, null=True)
	verified_by = models.ForeignKey("accounts.Account", related_name="%(app_label)s_%(class)s_verify_by_user", verbose_name="Diverifikasi Oleh", blank=True, null=True)
	verified_at = models.DateTimeField(editable=False, blank=True, null=True)
	# rejected_by = models.ForeignKey("accounts.Account", related_name="rejected_by_user", verbose_name="Dibatalkan Oleh", blank=True, null=True)
	rejected_by = models.ForeignKey("accounts.Account", related_name="%(app_label)s_%(class)s_rejected_by_user", verbose_name="Dibatalkan Oleh", blank=True, null=True)
	rejected_at = models.DateTimeField(editable=False, blank=True, null=True)

	updated_at = models.DateTimeField(auto_now=True)

	def get_color_status(self):
		return get_status_color(self)
		
	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.created_at = datetime.now()
		self.updated_at = datetime.now()
		return super(MetaAtribut, self).save(*args, **kwargs)

	def __unicode__(self):
		return u'%s' % (str(self.status))

	class Meta:
		abstract = True


class AtributTambahan(models.Model):
	status = models.PositiveSmallIntegerField(verbose_name='Status Data', choices=STATUS, default=6)

	created_by = models.ForeignKey("accounts.Account", related_name="create_by_user", verbose_name="Dibuat Oleh", blank=True, null=True)
	created_at = models.DateTimeField(editable=False)
	verified_by = models.ForeignKey("accounts.Account", related_name="verify_by_user", verbose_name="Diverifikasi Oleh", blank=True, null=True)
	verified_at = models.DateTimeField(editable=False, blank=True, null=True)
	rejected_by = models.ForeignKey("accounts.Account", related_name="rejected_by_user", verbose_name="Dibatalkan Oleh", blank=True, null=True)
	rejected_at = models.DateTimeField(editable=False, blank=True, null=True)

	updated_at = models.DateTimeField(auto_now=True)

	def get_color_status(self):
		return get_status_color(self)
		
	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.created_at = datetime.now()
		self.updated_at = datetime.now()
		return super(AtributTambahan, self).save(*args, **kwargs)

	def __unicode__(self):
		return u'%s' % (str(self.status))

class JenisPemohon(models.Model):
	jenis_pemohon = models.CharField(max_length=255, verbose_name='Jenis Pemohon')
	keterangan = models.CharField(max_length=255, blank=True, null=True)
	
	def __unicode__(self):
		return "%s" % (self.jenis_pemohon)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Pemohon'
		verbose_name_plural = 'Jenis Pemohon'

class JenisNomorIdentitas(models.Model):
	"""docstring for skpd"""
	jenis_nomor_identitas = models.CharField(max_length=30, verbose_name='Jenis Nomor Identitas')
	keterangan = models.CharField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		return u'%s. %s' % (self.id, self.jenis_nomor_identitas)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Nomor Identitas'
		verbose_name_plural = 'Jenis Nomor Identitas'


class Settings(models.Model):
	parameter = models.CharField("Nama Parameter", max_length=100)
	value = models.CharField("Nilai", max_length=100)
	url = models.URLField(max_length=200, verbose_name='url', null=True, blank=True)

	class Meta:
		verbose_name='Setting'
		verbose_name_plural='Setting'


# ALAMAT LOKASI #
class Negara(models.Model):
	nama_negara = models.CharField(max_length=40, verbose_name="Negara")
	keterangan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Keterangan")
	kode = models.CharField(max_length=10, blank=True, null=True, verbose_name="Kode Negara")
	lt = models.CharField(max_length=100, null=True, blank=True, verbose_name='Latitute')
	lg = models.CharField(max_length=100, null=True, blank=True, verbose_name='Longitute')


	def as_json(self):
		return dict(id=self.id, nama_negara=self.nama_negara, keterangan=self.keterangan)

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.nama_negara)+"</option>"

	def __unicode__(self):
		return "%s" % (self.nama_negara,)

	class Meta:
		ordering = ['nama_negara']
		verbose_name = "Negara"
		verbose_name_plural = "Negara"

class Provinsi(models.Model):
	negara = models.ForeignKey(Negara, verbose_name="Negara")
	nama_provinsi = models.CharField(max_length=40, verbose_name="Provinsi")
	keterangan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Keterangan")
	lt = models.CharField(max_length=100, null=True, blank=True, verbose_name='Latitute')
	lg = models.CharField(max_length=100, null=True, blank=True, verbose_name='Longitute')
	kode = models.CharField(max_length=10, null=True, blank=True, verbose_name='Kode')

	def as_json(self):
		return dict(id=self.id, nama_provinsi=self.nama_provinsi, negara=self.negara.nama_negara, keterangan=self.keterangan)

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.nama_provinsi)+"</option>"

	def __unicode__(self):
		return "%s" % (self.nama_provinsi,)

	class Meta:
		ordering = ['nama_provinsi']
		verbose_name = "Provinsi"
		verbose_name_plural = "Provinsi"

class Kabupaten(models.Model):
	"""docstring for Kabupaten"""
	provinsi = models.ForeignKey(Provinsi, verbose_name="Provinsi")
	nama_kabupaten = models.CharField(max_length=40, verbose_name="Kabupaten / Kota")
	keterangan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Keterangan")
	lt = models.CharField(max_length=100, null=True, blank=True, verbose_name='Latitute')
	lg = models.CharField(max_length=100, null=True, blank=True, verbose_name='Longitute')
	kode = models.CharField(max_length=10, null=True, blank=True, verbose_name='Kode')

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.nama_kabupaten)+"</option>"

	def as_option_complete(self):
		return "<option value='"+str(self.id)+"'>"+str(self.nama_kabupaten)+", "+str(self.provinsi.nama_provinsi)+" - "+str(self.provinsi.negara.nama_negara)+"</option>"
		
	def __unicode__ (self):
		return "%s" % (self.nama_kabupaten,)

	class Meta:
		ordering = ['nama_kabupaten']
		verbose_name = "Kabupaten / Kota"
		verbose_name_plural = "Kabupaten / Kota"

class Kecamatan(models.Model):
	"""docstring for Kecamatan"""
	kabupaten = models.ForeignKey(Kabupaten, verbose_name="Kabupaten / Kota")
	nama_kecamatan = models.CharField(max_length=40, verbose_name="Kecamatan")
	keterangan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Keterangan")
	lt = models.CharField(max_length=100, null=True, blank=True, verbose_name='Latitute')
	lg = models.CharField(max_length=100, null=True, blank=True, verbose_name='Longitute')
	kode = models.CharField(max_length=10, null=True, blank=True, verbose_name='Kode')


	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.nama_kecamatan)+"</option>"

	def __unicode__(self):
		return "%s" % (self.nama_kecamatan,)

	class Meta:
		ordering = ['nama_kecamatan']
		verbose_name = "Kecamatan"
		verbose_name_plural = "Kecamatan"

class Desa(models.Model):
	"""docstring for Desa"""
	kecamatan = models.ForeignKey(Kecamatan, verbose_name="Kecamatan")
	nama_desa = models.CharField(max_length=40, null=True, verbose_name="Nama Desa / Kelurahan")
	keterangan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Keterangan")
	lt = models.CharField(max_length=100, null=True, blank=True, verbose_name='Latitute')
	lg = models.CharField(max_length=100, null=True, blank=True, verbose_name='Longitute')
	kode = models.CharField(max_length=10, null=True, blank=True, verbose_name='Kode')

	def __unicode__(self):
		return "%s" % (self.nama_desa,)

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.nama_desa)+"</option>"

	def lokasi_lengkap(self):
		data = ''
		if self.kecamatan:
			if self.kecamatan.kabupaten:
				if self.kecamatan.kabupaten.provinsi:
					data = 'Ds. '+str(self.nama_desa)+', Kec. '+str(self.kecamatan.nama_kecamatan)+', '+str(self.kecamatan.kabupaten.nama_kabupaten)+', Prov. '+str(self.kecamatan.kabupaten.provinsi.nama_provinsi)
		return data

	def as_json(self):
		id_desa = ''
		id_kecamatan = ''
		id_kabupaten = ''
		id_provinsi = ''
		nama_desa = ''
		nama_kecamatan = ''
		nama_kabupaten = ''
		nama_provinsi = ''
		if self.nama_desa:
			id_desa = str(self.id)
			nama_desa = str(self.nama_desa)
		if self.kecamatan:
			id_kecamatan = str(self.kecamatan.id)
			nama_kecamatan = str(self.kecamatan.nama_kecamatan)
			if self.kecamatan.kabupaten:
				id_kabupaten = str(self.kecamatan.kabupaten.id)
				nama_kabupaten = str(self.kecamatan.kabupaten.nama_kabupaten)
				if self.kecamatan.kabupaten.provinsi:
					id_provinsi = str(self.kecamatan.kabupaten.provinsi.id)
					nama_provinsi = str(self.kecamatan.kabupaten.provinsi.nama_provinsi)
		return dict(id_desa=id_desa, nama_desa=nama_desa, id_kecamatan=id_kecamatan, nama_kecamatan=nama_kecamatan, id_kabupaten=id_kabupaten, nama_kabupaten=nama_kabupaten, id_provinsi=id_provinsi, nama_provinsi=nama_provinsi)

	class Meta:
		ordering = ['nama_desa']
		verbose_name = "Desa / Kelurahan"
		verbose_name_plural = "Desa / Kelurahan"

# END OF ALAMAT LOKASI #

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

class JenisKontruksi(MetaAtribut):
	kode = models.CharField(verbose_name="Kode Jenis Kontruksi", max_length=10)
	nama_jenis_kontruksi = models.CharField(verbose_name="Nama Jenis Kontruksi", max_length=50)

	def __unicode__(self):
		return u'Jenis Kontruksi %s - %s' % (str(self.kode), str(self.nama_jenis_kontruksi))

	class Meta:
		ordering = ['-status']
		verbose_name = 'Jenis Kontruksi'
		verbose_name_plural = 'Jenis Kontruksi'

class BangunanJenisKontruksi(MetaAtribut):
	jenis_kontruksi = models.ForeignKey(JenisKontruksi,verbose_name="Jenis Kontruksi")
	kode = models.CharField(verbose_name="Kode Bangunan Jenis Kontruksi", max_length=10)
	nama_bangunan = models.CharField(verbose_name="Nama Bangunan", max_length=50)
	biaya_bangunan = models.IntegerField(verbose_name="Ret./Satuan", null=True, blank=True)

	def as_option(self):
		return "<option value='"+str(self.kode)+"'>"+str(self.nama_bangunan)+"</option>"
		
	def __unicode__(self):
		return u'Bangunan %s - %s' % (str(self.kode), str(self.nama_bangunan))

	class Meta:
		ordering = ['-status']
		verbose_name = 'Bangunan'
		verbose_name_plural = 'Bangunan'

from uuid import uuid4
from django.utils.deconstruct import deconstructible
import os, re
from django.conf import settings

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

class Berkas(MetaAtribut):
	# nama_berkas = models.CharField("Nama Berkas", max_length=254)
	nama_berkas = models.TextField("Nama Berkas")
	berkas = FileField(upload_to=path_and_rename, max_length=255)
	no_berkas = models.CharField("Nomor Berkas", max_length=30, blank=True, null=True, help_text="Masukkan Nomor Surat / Berkas jika ada.")

	keterangan = models.CharField("Keterangan", blank=True, null=True, max_length=255)

	def get_file_url(self):
		if self.berkas:
			return settings.MEDIA_URL+str(self.berkas)
		return "#"

	def as_dict(self):
		return {
			'nama_berkas': self.nama_berkas,
			'berkas': self.get_file_url(),
		}

	def as_json(self):
		return dict(nama_berkas= self.nama_berkas, file=self.get_file_url())

	def __unicode__(self):
		return self.nama_berkas

	class Meta:
		verbose_name='Berkas'
		verbose_name_plural='Berkas'

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

@receiver(pre_delete, sender=Berkas)
def mymodel_delete(sender, instance, **kwargs):
	# Pass false so FileField doesn't save the model.
	if instance:
		instance.berkas.delete(False)

class KategoriPengaduan(models.Model):
	nama_kategori = models.CharField(max_length=255, verbose_name="Nama Kategori")
	keterangan = models.CharField(max_length=255, verbose_name="Keterangan", null=True, blank=True)

	class Meta:
		verbose_name = "Kategori Pengaduan"
		verbose_name_plural = "Kategori Pengaduan"

class ChatUserPemohon(models.Model):
	# email = models.EmailField(unique=True, blank=True, null=True)
	no_ktp = models.CharField(max_length=255, verbose_name="Nomor KTP")
	nama_pemohon = models.CharField(max_length=255, verbose_name="Nama Lengkap")

	def __unicode__(self):
		return self.no_ktp

	class Meta:
		verbose_name = "Chat User Pemohon"
		verbose_name_plural = "Chat User Pemohon"

class ChatRoom(MetaAtribut):
	operator = models.ForeignKey("accounts.Account", related_name="%(app_label)s_%(class)s_operator", verbose_name="Operator", blank=True, null=True)
	userpemohon = models.ForeignKey(ChatUserPemohon, verbose_name="Chat User Pemohon", null=True, blank=True)
	kelompok_jenis_izin = models.ForeignKey('izin.KelompokJenisIzin', verbose_name='Kelompok Jenis Izin', related_name="kelompok_jenis_izin_chat", blank=True, null=True)

	class Meta:
		verbose_name = "Chat Room"
		verbose_name_plural = "Chat Room"

class Chat(MetaAtribut):
	chat_room = models.ForeignKey(ChatRoom, verbose_name="Chat Room")
	isi_pesan = models.TextField(verbose_name="Isi Pesan", null=True, blank=True)
	berkas = models.ManyToManyField(Berkas, related_name='berkas_chat', verbose_name="Berkas Chat", blank=True)

	class Meta:
		verbose_name = "Chat"
		verbose_name_plural = "Chat"
	# created_at = models.DateTimeField(editable=False)
	# status = models.IntegerField(verbose_name="Status", null=True, blank=True) # 1 (dari Operator) 2 (dari pemohon)

	# def save(self, *args, **kwargs):
	# 	''' On save, update timestamps '''
	# 	if not self.id:
	# 		self.created_at = datetime.now()
	# 	return super(Chat, self).save(*args, **kwargs)

class PengaduanIzin(MetaAtribut):
	no_ktp = models.CharField(max_length=255, verbose_name="Nomor KTP", null=True, blank=True)
	nama_lengkap = models.CharField(max_length=255, verbose_name="Nama Lengkap", null=True, blank=True)
	no_telp = models.CharField(max_length=50, verbose_name="Nomor Telphone", null=True, blank=True)
	email = models.EmailField(blank=True, null=True)
	kelompok_jenis_izin = models.ForeignKey('izin.KelompokJenisIzin', verbose_name='Kelompok Jenis Izin', related_name="kelompok_jenis_izin_pengaduan", blank=True, null=True)
	isi_pengaduan = models.TextField(max_length=255, verbose_name= "Isi Pengaduan", null=True, blank=True)
	balas = models.TextField(max_length=255, verbose_name= "Balas", blank=True, null=True)

	def as_json(self):
		kelompok_jenis_izin = ''
		if self.kelompok_jenis_izin:
			kelompok_jenis_izin = self.kelompok_jenis_izin.kelompok_jenis_izin
		return dict(id=self.id, no_ktp=self.no_ktp, nama_lengkap=self.nama_lengkap, no_telp=self.no_telp, email=self.email, kelompok_jenis_izin=kelompok_jenis_izin, isi_pengaduan=self.isi_pengaduan, balas=self.balas, status=self.status)

	class Meta:
		verbose_name = "Pengaduan Izin"
		verbose_name_plural = "Pengaduan Izin"

class PesanPengaduan(MetaAtribut):
	pengaduan_izin = models.ForeignKey(PengaduanIzin, verbose_name="Base Pengaduan Izin")
	pesan = models.TextField(verbose_name="Pesan", null=True, blank=True)
	status_pemohon = models.BooleanField(verbose_name="Apakah pesan ini dari pemohon", default=True) # Jika True dari Pemohon, False dari Operator
	berkas = models.ManyToManyField(Berkas, related_name='berkas_pesan_pengaduan', verbose_name="Berkas Pesan Pengaduan", blank=True)

	def pretty_tanggal(self):
		from izin.utils import pretty_date
		import pendulum
		t2 = pendulum.timezone('Asia/Jakarta')
		t2 = t2.convert(self.created_at)
		t2 = t2.replace(tzinfo=None)
		pretty = pretty_date(t2)
		return pretty

	class Meta:
		verbose_name = "Pesan Pengaduan"
		verbose_name_plural = "Pesan Pengaduan"


class NotificationSMS(MetaAtribut):
	"""
		status :
			6 = masuk antrian sms
			1 = sms sudah dikirim
			2 = sms error atau terjadi kesalahan saat mengirim
	"""

	pesan = models.CharField(verbose_name="Pesan", null=True, blank=True, max_length=255)
	nomor_tujuan = models.CharField(verbose_name="Nomor Tujuan", max_length=255)
	keterangan = models.CharField(verbose_name="Keterangan", null=True, blank=True, max_length=255)

	def __unicode__(self):
		return u'%s - %s' % (self.nomor_tujuan, self.pesan)

	class Meta:
		verbose_name = "Notification SMS"
		verbose_name_plural = "Notification SMS"