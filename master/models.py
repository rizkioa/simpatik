from django.db import models

# Create your models here.

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