from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from izin.models import Pemohon

import json

class PemohonAdmin(admin.ModelAdmin):
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
		if request.user.groups.filter(name='Front Desk').exists():
			fieldsets = (
			(' Identitas Pribadi', {
				'fields': ('nama_lengkap', 'tempat_lahir', 'tanggal_lahir','jenis_pemohon','jabatan_pemohon','telephone','email','desa','alamat',('lintang','bujur'),'kewarganegaraan')
				}),

			('Account', {
				'fields': ('username','password','foto','is_active','status')
				}),
		)
		elif request.user.is_superuser:
			fieldsets = (
			(' Identitas Pribadi', {
				'fields': ('nama_lengkap', 'tempat_lahir', 'tanggal_lahir','jenis_pemohon','jabatan_pemohon','telephone','email','desa','alamat',('lintang','bujur'),'kewarganegaraan')
				}),

			('Account', {
				'fields': ('username','password','foto','is_active','is_admin','status')
				}),
		)
		else:

			fieldsets = (
			(' Identitas Pribadi', {
				'fields': ('nama_lengkap', 'tempat_lahir', 'tanggal_lahir','jenis_pemohon','jabatan_pemohon','telephone','email','desa','alamat',('lintang','bujur'),'kewarganegaraan')
				}),

			('Account', {
				'fields': ('username','password','foto','is_active','is_admin','status')
				}),
		)
		return fieldsets