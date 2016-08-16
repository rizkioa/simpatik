from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from accounts.models import NomorIdentitasPengguna
from izin.models import Pemohon
from master.models import JenisNomorIdentitas
from pemohon_forms import PemohonForm

import json
import re

class ItemInlineFormSet(BaseInlineFormSet):
	def clean(self):
		c_ = super(ItemInlineFormSet, self).clean()
		jumlah_ = len(self.forms)
		jumlah_nomor_identitas = JenisNomorIdentitas.objects.all().count()
		if jumlah_nomor_identitas < 1:
			raise forms.ValidationError("Jenis Nomor Identitas Masih Kosong.")
		elif jumlah_ > jumlah_nomor_identitas:
			raise forms.ValidationError("Nomor Identitas melebihi jumlah jenis nomor identitas yang ada.")
		elif jumlah_ > 1:
			nip_list = []
			username = None
			jenis_identitas = None
			f = None
			for form in self.forms:
				nomor_ = form.cleaned_data.get('nomor', None)
				ji = form.cleaned_data.get('jenis_identitas', None)
				if nomor_ and ji:
					if ji in nip_list:
						form.add_error('nomor', "Nomor untuk jenis identitas "+str(ji)+" sudah dimasukkan.")
					else:                        
						nip_list.append(ji)
					if jenis_identitas and ji:
						if jenis_identitas.id > ji.id:
							jenis_identitas = ji
							username = nomor_
					elif not jenis_identitas and ji:
						jenis_identitas = ji
						username = nomor_
					f = form
			if username and f and hasattr(form.instance, "user"):
				form.instance.user.username = re.sub('[^0-9a-zA-Z]+', '', username)
				form.instance.user.save()
		elif jumlah_ == 1:
			form = self.forms[0]
			nomor_ = form.cleaned_data.get('nomor', None)
			if nomor_ and hasattr(form.instance, "user"):
				form.instance.user.username = re.sub('[^0-9a-zA-Z]+', '', nomor_)
				form.instance.user.save()
		elif jumlah_ < 1:
			raise forms.ValidationError("Masukkan minimal 1 Nomor Identitas.")
		return c_

class NomorIdentitasInline(admin.StackedInline):
	verbose_name = 'Nomor Identitas'
	verbose_name_plural = 'Nomor Identitas'
	model = NomorIdentitasPengguna
	formset = ItemInlineFormSet
	min_num = 1
	extra = 0

class PemohonAdmin(admin.ModelAdmin):
	form = PemohonForm
	inlines = [NomorIdentitasInline,]
	list_display = ('nama_lengkap','telephone','jenis_pemohon','jabatan_pemohon')
	list_filter = ('nama_lengkap','telephone','jenis_pemohon','jabatan_pemohon')
	search_fields = ('jenis_pemohon','jabatan_pemohon')
	
	def ajax_autocomplete(self, request):
		pilihan = "<option></option>"
		pemohon_list = Pemohon.objects.all()
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in pemohon_list)));

	def ajax_pemohon(self, request, pemohon_id=None):
		pemohon_get = Pemohon.objects.filter(id=pemohon_id)
		results = [ob.as_json() for ob in pemohon_get]
		return HttpResponse(json.dumps(results))

	# def pemohon_add(request, pemohon_id=None):
	# 	pemohon_add = Pemohon.objects.filter(id=pemohon_id)
	# 	return HttpResponse(pemohon_add)

	# def admin_pemohon_edit(self, request, pemohon_id=None, extra_context={}):
	# 	if pemohon_id:
	# 		pemohon = Pemohon.objects.get(pk=pemohon_id)
	# 		pemohon_edit()
	# 	return HttpResponseRedirect(reverse("admin:izin_pemohon_change"))

	def get_form(self, request, obj=None, **kwargs):
		form = super(PemohonAdmin, self).get_form(request, obj, **kwargs)
		form.request = request
		return form

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(PemohonAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^ajax/autocomplete/$', self.admin_site.admin_view(self.ajax_autocomplete), name='pemohon_ajax_autocomplete'),
			url(r'^ajax/pemohon/(?P<pemohon_id>\w+)/$', self.admin_site.admin_view(self.ajax_pemohon), name='ajax_pemohon'),
			# url(r'^pemohon/(?P<pemohon_id>[0-9]+)/$', self.admin_site.admin_view(self.admin_pemohon_edit), name="admin_pemohon_edit"),
			# url(r'^(?P<pemohon_id>[0-9]+)/$', self.admin_site.admin_view(self.pemohon_edit), name="pemohon_edit"),
			)
		return my_urls + urls

	def get_fieldsets(self, request, obj = None):
		field = ('nama_lengkap', ('tempat_lahir', 'tanggal_lahir'), 'telephone', 'email', 'jenis_pemohon','jabatan_pemohon','kewarganegaraan')
		fieldsets = (
			(None, {
				'classes': ('wide',),
				'fields': field
				}
			),
			('Alamat', {'fields': ('alamat', 'negara', 'provinsi', 'kabupaten', 'kecamatan', 'desa')}),
			('Lain-lain', {'fields': ('foto', 'keterangan', 'status', )}),
		)

		# if request.user.groups.filter(name='Front Desk').exists():
		# 	fieldsets = (
		# 	(' Identitas Pribadi', {
		# 		'fields': ('nama_lengkap', 'tempat_lahir', 'tanggal_lahir','jenis_pemohon','jabatan_pemohon','telephone','email','desa','alamat',('lintang','bujur'),'kewarganegaraan')
		# 		}),

		# 	('Account', {
		# 		'fields': ('username','password','foto','is_active','status')
		# 		}),
		# )
		# elif request.user.is_superuser:
		# 	fieldsets = (
		# 	(' Identitas Pribadi', {
		# 		'fields': ('nama_lengkap', ('tempat_lahir', 'tanggal_lahir'),'jenis_pemohon','jabatan_pemohon','telephone','email','desa','alamat',('lintang','bujur'),'kewarganegaraan')
		# 		}),

		# 	('Account', {
		# 		'fields': ('username','password','foto','is_active','is_admin','status')
		# 		}),
		# )
		# else:

		# 	fieldsets = (
		# 	(' Identitas Pribadi', {
		# 		'fields': ('nama_lengkap', 'tempat_lahir', 'tanggal_lahir','jenis_pemohon','jabatan_pemohon','telephone','email','desa','alamat',('lintang','bujur'),'kewarganegaraan')
		# 		}),

		# 	('Account', {
		# 		'fields': ('username','password','foto','is_active','is_admin','status')
		# 		}),
		# )
		return fieldsets

	def save_formset(self, request, form, formset, change):
		instances = formset.save(commit=False)
		for obj in formset.deleted_objects:
			obj.delete()
		i = None
		for instance in instances:
			instance.save()
			i = instance
		if i:
			i.user.pemohon.set_username()

	

