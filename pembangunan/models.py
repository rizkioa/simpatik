from django.db import models

from izin.models import Survey
from kepegawaian.models import Pegawai

# Create your models here.


class AnggotaTim(models.Model):
	"""docstring for AnggotaTim"""
	survey_iujk = models.ForeignKey(Survey, verbose_name='Data Survey')
	pegawai = models.ForeignKey(Pegawai, verbose_name='Pegawai')
	koordinator = models.BooleanField(default=False, verbose_name="Apakah Koordinator?")

	def __unicode__(self):
		return u'%s' % (str(self.pegawai))






