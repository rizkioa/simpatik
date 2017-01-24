from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django import forms
import json
from django.utils.safestring import mark_safe
from django.http import HttpResponse


from .models import AnggotaTim, Rekomendasi, DetilBAP, BAPReklameHO
from kepegawaian.models import Pegawai

# Register your models here.


class AnggotaTimForm(forms.ModelForm):
	class Meta:
		model = AnggotaTim
		# fields = '__all__'
		exclude = ['koordinator']



class AnggotaTimAdmin(admin.ModelAdmin):
	"""docstring for AnggotaTimAdmin"""
	list_display = ('survey_iujk', 'pegawai', 'koordinator')
	list_filter = ('survey_iujk',)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "pegawai":
			pegawai = Pegawai.objects.all()
			if request.user.groups.filter(name='Admin Pembangunan').exists():
				get_pegawai_skpd = Pegawai.objects.get(pk=request.user.id)
				pegawai = pegawai.filter(unit_kerja=get_pegawai_skpd.unit_kerja)
			kwargs["queryset"] = pegawai
		return super(AnggotaTimAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def simpan_ajax(self, request):
		anggota = AnggotaTimForm(request.POST)
		# id_survey = request.POST.get('survey_iujk')
		if anggota.is_valid():
			a = anggota.save(commit=False)
			a.save()

			data = {'success': True, 'pesan': 'Anggota Tim '+str(a.pegawai)+' berhasil ditambahkan.' }
			data = json.dumps(data)
			response = HttpResponse(data)
		else:
			data = anggota.errors.as_json()
			response = HttpResponse(data)

		return response
	def delete_anggotatim(self, request, id_pengajuan_izin_, id_survey, id_anggota):
		try:
			get_anggota = AnggotaTim.objects.get(pk=id_anggota)
			data = {'success': True, 'pesan': 'Anggota '+str(get_anggota.pegawai)+' berhasil Hapus.' }
			get_anggota.delete()
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': 'Anggota Tidak Ada Dalam Daftar' }

		return HttpResponseRedirect(reverse('admin:cek_kelengkapan', args=[id_pengajuan_izin_, id_survey]))

	def delete_ajax(self, request, id_anggota):
		try:
			get_anggota = AnggotaTim.objects.get(pk=id_anggota)
			data = {'success': True, 'pesan': 'Anggota '+str(get_anggota.pegawai)+' berhasil Hapus.' }
			get_anggota.delete()
			data = json.dumps(data)
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': 'Anggota Tidak Ada Dalam Daftar' }
			data = json.dumps(data)

		response = HttpResponse(data)
		return response


	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(AnggotaTimAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^simpan-anggotatim/$', self.admin_site.admin_view(self.simpan_ajax), name='simpan_ajax'),
			url(r'^hapus-anggotatim/(?P<id_pengajuan_izin_>[0-9]+)/(?P<id_survey>[0-9]+)/(?P<id_anggota>[0-9]+)$', self.admin_site.admin_view(self.delete_anggotatim), name='hapus_ajax'),
			url(r'^hapus-anggotatim-ajax/(?P<id_anggota>[0-9]+)$', self.admin_site.admin_view(self.delete_ajax), name='hapus_anggotatim_ajax'),
			)
		return my_urls + urls


		
admin.site.register(AnggotaTim, AnggotaTimAdmin)

class RekomendasiAdmin(admin.ModelAdmin):
	list_display = ('get_rekomendasi',)

	def get_rekomendasi(self, obj):
		return mark_safe(obj.rekomendasi)
	get_rekomendasi.short_description = "Rekomendasi"

	def get_fieldsets(self, request, obj=None):
		field_user = ()
		field_admin = ('unit_kerja', 'survey_iujk','rekomendasi','keterangan','berkas','created_by','status')

		if obj:
			if request.user.is_superuser:
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': field_admin
						}),
				)
			else:
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': field_user
						}),
				)
		else:
			pass

		return add_fieldsets

	def get_queryset(self, request):
		qs = super(RekomendasiAdmin, self).get_queryset(request)
		if not request.user.is_superuser:
			if request.user.groups.filter(name='Tim Teknis').exists():
				print "ASEM"
			qs = qs.filter(created_by=request.user)
		return qs



admin.site.register(Rekomendasi,RekomendasiAdmin)
admin.site.register(DetilBAP)
admin.site.register(BAPReklameHO)
