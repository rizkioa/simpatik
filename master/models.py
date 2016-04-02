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
class Provinsi(models.Model):
	nama_prov = models.CharField(max_length=40, verbose_name="Provinsi")
	keterangan = models.CharField(max_length=255, null=True, verbose_name="Keterangan")
	lt = models.CharField(max_length=100, null=True, verbose_name='Latitute')
	lg = models.CharField(max_length=100, null=True, verbose_name='Longitute')

	def __unicode__(self):
		return "%s" % (self.nama_prov,)

	class Meta:
		verbose_name = "Provinsi"
		verbose_name_plural = "Provinsi"

class Kabupaten(models.Model):
	"""docstring for Kabupaten"""
	nama_prov = models.ForeignKey(Provinsi, verbose_name="Provinsi")
	nama_kab = models.CharField(max_length=40, verbose_name="Kabupaten")
	keterangan = models.CharField(max_length=255, null=True, verbose_name="Keterangan")
	lt = models.CharField(max_length=100, null=True, verbose_name='Latitute')
	lg = models.CharField(max_length=100, null=True, verbose_name='Longitute')

	def __unicode__ (self):
		return "%s" % (self.nama_kab,)

	class Meta:
		verbose_name = "Kabupaten"
		verbose_name_plural = "Kabupaten"

class Kecamatan(models.Model):
	"""docstring for Kecamatan"""
	nama_kab = models.ForeignKey(Kabupaten, verbose_name="Kabupaten")
	nama_kec = models.CharField(max_length=40, verbose_name="Kecamatan")
	keterangan = models.CharField(max_length=255, null=True, verbose_name="Keterangan")
	lt = models.CharField(max_length=100, null=True, verbose_name='Latitute')
	lg = models.CharField(max_length=100, null=True, verbose_name='Longitute')

	def __unicode__(self):
		return "%s" % (self.nama_kec,)

	class Meta:
		verbose_name = "Kecamatan"
		verbose_name_plural = "Kecamatan"

class Desa(models.Model):
	"""docstring for Desa"""
	nama_kec = models.ForeignKey(Kecamatan, verbose_name="Kecamatan")
	nama_desa = models.CharField(max_length=40, null=True, verbose_name="Nama Desa")
	keterangan = models.CharField(max_length=255, null=True, verbose_name="Keterangan")
	lt = models.CharField(max_length=100, null=True, verbose_name='Latitute')
	lg = models.CharField(max_length=100, null=True, verbose_name='Longitute')

	def __unicode__(self):
		return "Kec. %s - %s" % (self.nama_kec,self.nama_desa,)

	class Meta:
		verbose_name = "Desa"
		verbose_name_plural = "Desa"

# END OF ALAMAT LOKASI #