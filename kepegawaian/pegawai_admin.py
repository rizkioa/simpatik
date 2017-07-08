from django.contrib import admin
from kepegawaian.forms import PegawaiForm, AddPegawaiForm
from accounts.models import NomorIdentitasPengguna, Account
from master.models import JenisNomorIdentitas
from kepegawaian.models import Pegawai, UnitKerja
from django.forms.models import BaseInlineFormSet
from django import forms
from django.db.models import Q
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import re
import xlrd

from django.shortcuts import render
from django.core.urlresolvers import resolve, reverse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist



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

class PegawaiAdmin(admin.ModelAdmin):
	# form = PegawaiForm
	list_display = ('nomor_identitas', 'get_full_name', 'unit_kerja', 'jabatan', 'bidang_struktural', 'keterangan', 'jenis_pegawai', 'login_as')
	list_filter = ('groups__name', 'jabatan', )
	inlines = [NomorIdentitasInline,]
	search_fields = ('username', 'nama_lengkap')

	def changelist_view(self, request, extra_context={}):
		self.request = request
		unit_kerja = UnitKerja.objects.all()
		extra_context.update({'unit_kerja':unit_kerja})
		return super(PegawaiAdmin, self).changelist_view(request, extra_context=extra_context)

	def login_as(self, obj):
		str_aksi = ""
		return mark_safe(str_aksi+'<a class="btn btn-xs btn-success" title="Login sebagai %s" href="%s"><i style="margin: 0px;" class="icon-login"></i></a>' % (obj.nama_lengkap,reverse('loginas-user-login', kwargs={'user_id': obj.id })))
	login_as.short_description = 'Aksi'

	def nomor_identitas(self, obj):
		return obj.username
	nomor_identitas.short_description = 'Nomor Identitas'
	nomor_identitas.admin_order_field = 'username'

	def jenis_pegawai(self, obj):
		groups = obj.groups.all()
		return ", ".join(str(g.hakakses.keterangan) if hasattr(g, 'hakakses') else str(g.name) for g in groups)
	jenis_pegawai.short_description = 'Jenis Pegawai'

	def option_pegawai(self, request):		
		pegawai_list = Pegawai.objects.all()
		q = request.POST.get('q', None)
		if q:
			pegawai_list = pegawai_list.filter(Q(nama_lengkap__icontains=q)|Q(username__icontains=q))
		else:
			pegawai_list = Pegawai.objects.none()
		pilihan = "<option></option>"
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in pegawai_list)));

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(PegawaiAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^option/$', self.admin_site.admin_view(self.option_pegawai), name='option_pegawai'),
		)
		return my_urls + urls

	def get_form(self, request, obj=None, **kwargs):
		func_view, func_view_args, func_view_kwargs = resolve(request.path)
		if func_view.__name__ == self.change_view.__name__:
			kwargs['form'] = PegawaiForm
		else:
			kwargs['form'] = AddPegawaiForm
		form = super(PegawaiAdmin, self).get_form(request, obj, **kwargs)
		form.request = request
		return form
		
	def get_fieldsets(self, request, obj = None):
		func_view, func_view_args, func_view_kwargs = resolve(request.path)
		if func_view.__name__ == self.change_view.__name__:
			field = (('gelar_depan', 'nama_lengkap', 'gelar_belakang'), ('tempat_lahir', 'tanggal_lahir'), 'telephone', 'email')
			add_fieldsets = (
				(None, {
					'classes': ('wide',),
					'fields': field
					}
				),
				('Kepegawaian', {'fields': ('unit_kerja', 'bidang_struktural', 'jabatan', )}),
				('Alamat', {'fields': ('alamat', 'negara', 'provinsi', 'kabupaten', 'kecamatan', 'desa')}),
				('Notifikasi', {'fields': ('notifikasi_telegram', 'notifikasi_email')}),
				('Lain-lain', {'fields': ('foto', 'keterangan', 'groups')}),
			)
		else:
			field = ('nama_lengkap', ('tempat_lahir', 'tanggal_lahir'), 'telephone', 'email')

			add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': field
						}
					),
					('Kepegawaian', {'fields': ('unit_kerja', 'bidang_struktural', 'jabatan', )}),
				)
		return add_fieldsets

	def get_queryset(self, request):
		qs = super(PegawaiAdmin, self).get_queryset(request)
		return qs.order_by('-jabatan_id')

	def save_formset(self, request, form, formset, change):
		instances = formset.save(commit=False)
		for obj in formset.deleted_objects:
			obj.delete()
		i = None
		for instance in instances:
			instance.save()
			i = instance
		if i:
			i.user.pegawai.set_username()
			i.user.pegawai.set_password(i.user.username)
			i.save()

	def save_model(self, request, obj, form, change):
		obj.save()
	


