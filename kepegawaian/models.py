from django.db import models
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from accounts.models import Account

class JenisUnitKerja(MPTTModel):
	jenis_unit_kerja = models.CharField(max_length=30, verbose_name='Jenis Unit Kerja')
	jenis_unit_kerja_induk = TreeForeignKey("self", verbose_name='Jenis Unit Kerja Induk', null=True, blank=True)
	keterangan = models.CharField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (self.jenis_unit_kerja)

	def save(self, *args, **kwargs):
		super(JenisUnitKerja, self).save(*args, **kwargs)
		JenisUnitKerja.objects.rebuild()

	class MPTTMeta:
		verbose_name='Jenis Unit Kerja'
		verbose_name_plural = 'Jenis Unit Kerja'
		parent_attr = 'jenis_unit_kerja_induk'

	class Meta:
		ordering = ['id']
		verbose_name = 'Jenis Unit Kerja'
		verbose_name_plural = 'Jenis Unit Kerja'

class UnitKerja(MPTTModel):
	nama_unit_kerja = models.CharField(max_length=100, verbose_name='Unit Kerja')
	jenis_unit_kerja = models.ForeignKey(JenisUnitKerja, related_name='unit_kerja_jenis', verbose_name='Jenis Unit Kerja', null=True, blank=True)
	unit_kerja_induk = TreeForeignKey("self", verbose_name='Unit Kerja Induk', null=True, blank=True)
	keterangan = models.CharField(max_length=255, blank=True, null=True)

	kode_rekening = models.CharField(verbose_name='Kode Rekening', max_length=15, blank=True, null=True, default='xx')

	kepala = models.ForeignKey("Pegawai", related_name='kepala', verbose_name='Kepala Unit Kerja', null=True, blank=True)
	plt = models.BooleanField(default=False, verbose_name="Apakah PLT?")
	
	telephone = models.CharField(max_length=50, null=True, blank=True)
	email = models.EmailField(max_length=50, null=True, blank=True)
	alamat = models.CharField(max_length=255, null=True, blank=True)
	kode_pos = models.CharField(max_length=50, null=True, blank=True)
	url_simpatik = models.URLField(null=True, blank=True, verbose_name="URL simpatik", help_text="contoh : http://simpatik.kedirikab.go.id")

	def save(self, *args, **kwargs):
		super(UnitKerja, self).save(*args, **kwargs)
		UnitKerja.objects.rebuild()

	def __unicode__(self):
		return "%s" % (self.nama_unit_kerja)

	class MPTTMeta:
		verbose_name='Unit Kerja'
		verbose_name_plural = 'Unit Kerja'
		parent_attr = 'unit_kerja_induk'

	class Meta:
		ordering = ['id']
		verbose_name = 'Unit Kerja'
		verbose_name_plural = 'Unit Kerja'


class BidangStruktural(MPTTModel):
	nama_bidang = models.CharField(max_length=200, verbose_name='Bagian / Bidang / Seksi (Struktural)')
	unit_kerja = TreeForeignKey(UnitKerja, verbose_name='Unit Kerja')
	bidang_induk = TreeForeignKey("self", verbose_name='Bidang Induk', null=True, blank=True)
	keterangan = models.CharField(max_length=255, blank=True, null=True)

	def get_name_tree(self):
		strip = '---'
		return '%s %s' % (self.level*strip, self.__unicode__())

	def as_option(self, tree_):
		if tree_:
			return "<option value='"+str(self.id)+"'>"+self.level*'--- '+str(self.nama_bidang)+"</option>"
		return "<option value='"+str(self.id)+"'>"+str(self.nama_bidang)+"</option>"

	def save(self, *args, **kwargs):
		super(BidangStruktural, self).save(*args, **kwargs)
		BidangStruktural.objects.rebuild()

	def __unicode__(self):
		if self.unit_kerja:
			return u'%s (%s)' % (self.nama_bidang, self.unit_kerja)
		return u'%s' % (self.nama_bidang)

	class MPTTMeta:
		verbose_name='Bagian / Bidang / Seksi (Struktural)'
		verbose_name_plural = 'Bagian / Bidang / Seksi (Struktural)'
		parent_attr = 'bidang_induk'

	class Meta:
		ordering = ['id']
		verbose_name = 'Bagian / Bidang / Seksi (Struktural)'
		verbose_name_plural = 'Bagian / Bidang / Seksi (Struktural)'

# Create your models here.
class Jabatan(models.Model):
	nama_jabatan = models.CharField(max_length=50, verbose_name='Nama Jabatan')
	keterangan = models.CharField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (self.nama_jabatan)

	class Meta:
		ordering = ['id']
		verbose_name = 'Jabatan'
		verbose_name_plural = 'Jabatan'

class Pegawai(Account):
	unit_kerja = TreeForeignKey(UnitKerja, verbose_name='Unit Kerja')
	bidang_struktural = TreeForeignKey(BidangStruktural, verbose_name='Bagian / Bidang / Seksi (Struktural)', blank=True, null=True)
	jabatan = models.ForeignKey(Jabatan, verbose_name='Jabatan', blank=True, null=True)

	def as_option(self):
		return "<option value='"+str(self.id)+"'>"+str(self.nama_lengkap)+" - "+str(self.username)+"</option>"
		
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
		return u'%s' % (self.nama_lengkap)

	class Meta:
		verbose_name = 'Pegawai'
		verbose_name_plural = 'Pegawai'	
