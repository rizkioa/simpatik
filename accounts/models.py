
from accounts.utils import STATUS
from datetime import datetime
from django.conf import settings

from django.db import models

from django.utils.deconstruct import deconstructible

from master.models import JenisNomorIdentitas, Desa, AtributTambahan

from uuid import uuid4

import os, re

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
path_and_rename = PathAndRename("profiles/")

class ImageField(models.ImageField):
	def save_form_data(self, instance, data):
		if data is not None: 
			file = getattr(instance, self.attname)
			if file != data:
				file.delete(save=False)
		super(ImageField, self).save_form_data(instance, data)


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class AccountManager(BaseUserManager):
	def create_user(self, username, nama_lengkap, password=None):
		"""
		Creates and saves a User with the given username, nama_lengkap and password.
		"""
		if not username:
			raise ValueError('Users must have an username')
		user = self.model(
			username=username,
			nama_lengkap=nama_lengkap,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, nama_lengkap, password):
		"""
		Creates and saves a superuser with the given identity number, nama_lengkap and password.
		"""
		user = self.create_user(username,
			password=password,
			nama_lengkap=nama_lengkap
		)
		user.is_admin = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class IdentitasPribadi(AtributTambahan):
	nama_lengkap = models.CharField("Nama Lengkap", max_length=100)

	tempat_lahir = models.CharField(max_length=30, verbose_name='Tempat Lahir', null=True, blank=True)
	tanggal_lahir = models.DateField(verbose_name='Tanggal Lahir', null=True, blank=True)
	telephone = models.CharField(verbose_name='Telepon', max_length=50, null=True, blank=True)
	hp = models.CharField(verbose_name='No. HP', max_length=50, null=True, blank=True)
	email = models.EmailField(unique=True, blank=True, null=True)

	desa = models.ForeignKey(Desa, null=True, blank=True, verbose_name='Desa')
	alamat = models.CharField(max_length=255, null=True, blank=True)
	lintang = models.CharField(max_length=255, verbose_name='Lintang', blank=True, null=True)
	bujur = models.CharField(max_length=255, verbose_name='Bujur', blank=True, null=True)

	kewarganegaraan = models.CharField(max_length=100, null=True, blank=True)

	pekerjaan = models.CharField(max_length=255, blank=True, null=True)
	
	keterangan = models.CharField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (self.nama_lengkap)

	class Meta:
		ordering = ['id']
		verbose_name = 'Identitas Pribadi'
		verbose_name_plural = 'Identitas Pribadi'


# Create your models here.

class Account(AbstractBaseUser, PermissionsMixin, IdentitasPribadi):

	username = models.CharField(max_length=40, unique=True)
	foto = ImageField(upload_to=path_and_rename, max_length=255, null=True, blank=True)
	is_active = models.BooleanField(default=True, verbose_name="Apakah Active?")
	is_admin = models.BooleanField(default=False, verbose_name="Apakah Admin?")

	# status = models.PositiveSmallIntegerField(verbose_name='Status Data', choices=STATUS, default=1)
	# created_at = models.DateTimeField(editable=False)
	# updated_at = models.DateTimeField(auto_now=True)

	objects = AccountManager()
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['nama_lengkap']

	@property
	def is_staff(self):
		"Allow All Member to Login"
		# Simplest possible answer: All admins are staff
		return self.is_active

	def get_short_name(self):
		# The user is identified by their nama
		return self.username

	def get_full_name(self):
		# The user is identified by their nama
		return self.username

	def get_foto(self):
		if self.foto:
			return settings.MEDIA_URL+str(self.foto)
		return settings.STATIC_URL+"images/no-avatar.jpg"

	def save(self, *args, **kwargs):
		self.nama_lengkap = self.nama_lengkap.upper()
		if not self.id:
			self.created_at = datetime.now()
		self.updated_at = datetime.now()
		super(Account, self).save(*args, **kwargs)

	def __unicode__(self):
		return u'%s - %s' % (self.nama_lengkap, self.username)

	class Meta:
		ordering = ['id']
		verbose_name = 'Akun'
		verbose_name_plural = 'Akun'

class NomorIdentitasPengguna(models.Model):
	nomor = models.CharField(max_length=100, unique=True)
	user = models.ForeignKey(IdentitasPribadi, verbose_name='User')
	jenis_identitas = models.ForeignKey(JenisNomorIdentitas, verbose_name='Jenis Nomor Identitas')

	def set_as_username(self):
		self.user.username = re.sub('[^0-9a-zA-Z]+', '', self.nomor)
		self.user.save()

	def __unicode__(self):
		return u'%s' % (self.nomor)

	class Meta:
		verbose_name = 'Nomor Identitas Pengguna'
		verbose_name_plural = 'Nomor Identitas Pengguna'

