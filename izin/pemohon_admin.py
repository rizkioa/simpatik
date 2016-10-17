from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from accounts.models import NomorIdentitasPengguna
from izin.models import Pemohon, PengajuanIzin, Riwayat
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
	list_display = ('get_nomor_ktp', 'nama_lengkap','telephone','jenis_pemohon','jabatan_pemohon', 'get_alamat')
	list_filter = ('nama_lengkap','telephone','jenis_pemohon','jabatan_pemohon')
	search_fields = ('jenis_pemohon','jabatan_pemohon')
	
	def get_list_display_links(self, request, list_display):
		if request.user.groups.filter(name='Kabid') or request.user.groups.filter(name='Kadin') or request.user.groups.filter(name='Pembuat Surat') or request.user.groups.filter(name='Penomoran') or request.user.groups.filter(name='Cetak') or request.user.groups.filter(name='Selesai'):
			list_display_links = None
		else:
			list_display_links = ('nama_lengkap',)
		return list_display_links

	def get_riwayat(self, obj):
		# pengajuan_ = PengajuanIzin.objects.filter(pemohon=obj.id).last()
		riwayat_ = Riwayat.objects.filter(pengajuan_izin__pemohon=obj).last()
		aktivitas_ = riwayat_.created_at
		# aktivitas_ = ""
		return aktivitas_
	get_riwayat.short_description = "Tgl Aktivitas Terakhir"

	def get_nomor_ktp(self, obj):
		ktp_ = str(obj.nomoridentitaspengguna_set.last())
		return ktp_
	get_nomor_ktp.short_description = "No KTP/Paspor"

	def get_pengajuan_terakhir(self, obj):
		pengajuan_ = PengajuanIzin.objects.filter(pemohon=obj).last()
		jenis_izin_ = pengajuan_.kelompok_jenis_izin.kelompok_jenis_izin
		return jenis_izin_
	get_pengajuan_terakhir.short_description = "Pengajuan Izin Terakhir"

	def get_alamat(self, obj):
		alamat_ = obj.alamat
		if obj.desa:
			alamat_ = str(obj.alamat)+", "+str(obj.desa)+", Kec. "+str(obj.desa.kecamatan)+", "+str(obj.desa.kecamatan.kabupaten)
		return alamat_
	get_alamat.short_description = "Alamat"

	def ajax_autocomplete(self, request):
		pilihan = "<option></option>"
		pemohon_list = Pemohon.objects.all()
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in pemohon_list)));

	def ajax_pemohon(self, request, pemohon_id=None):
		pemohon_get = Pemohon.objects.filter(id=pemohon_id)
		results = [ob.as_json() for ob in pemohon_get]
		return HttpResponse(json.dumps(results))

	def ajax_cek_email(self, request):
		email_ = request.POST.get('value', None)
		results = False
		if email_:
			pemohon = Pemohon.objects.filter(email=email_)
			print pemohon.count()
			if pemohon.count() > 0:
				results = False
			else:
				results = True
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
			url(r'^ajax/cek-email/$', self.admin_site.admin_view(self.ajax_cek_email), name='ajax_cek_email'),
			# url(r'^pemohon/(?P<pemohon_id>[0-9]+)/$', self.admin_site.admin_view(self.admin_pemohon_edit), name="admin_pemohon_edit"),
			# url(r'^(?P<pemohon_id>[0-9]+)/$', self.admin_site.admin_view(self.pemohon_edit), name="pemohon_edit"),
			)
		return my_urls + urls

	def get_fieldsets(self, request, obj = None):
		field = ('nama_lengkap', ('tempat_lahir', 'tanggal_lahir'), 'telephone', 'email', 'jenis_pemohon','jabatan_pemohon','kewarganegaraan', 'pekerjaan')
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

	def suit_cell_attributes(self, obj, column):
		if column in ['alamat']:
			return {'class': 'text-center'}
		else:
			return None

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

	

