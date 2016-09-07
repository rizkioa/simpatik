from django.db import models
from accounts.utils import STATUS, get_status_color
# from accounts.models import Account
from datetime import datetime

# Create your models here.

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
	jenis_pemohon = models.CharField(max_length=255, null=True, blank=True, verbose_name='Jenis Pemohon')
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

	class Meta:
		verbose_name='Setting'
		verbose_name_plural='Setting'


# ALAMAT LOKASI #
class Negara(models.Model):
	nama_negara = models.CharField(max_length=40, verbose_name="Negara")
	keterangan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Keterangan")
	code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Kode Negara")
	lt = models.CharField(max_length=100, null=True, blank=True, verbose_name='Latitute')
	lg = models.CharField(max_length=100, null=True, blank=True, verbose_name='Longitute')

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

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.nama_desa)+"</option>"

	def __unicode__(self):
		return "%s" % (self.nama_desa,)

	class Meta:
		ordering = ['nama_desa']
		verbose_name = "Desa / Kelurahan"
		verbose_name_plural = "Desa / Kelurahan"

# END OF ALAMAT LOKASI #
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

class Berkas(AtributTambahan):
	nama_berkas = models.CharField("Nama Berkas", max_length=100)
	berkas = FileField(upload_to=path_and_rename, max_length=255)
	no_berkas = models.CharField("Nomor Berkas", max_length=30, blank=True, null=True, help_text="Masukkan Nomor Surat / Berkas jika ada.")

	keterangan = models.CharField("Keterangan", blank=True, null=True, max_length=255)

	def get_file_url(self):
		if self.berkas:
			return settings.MEDIA_URL+str(self.berkas)
		return "#"

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