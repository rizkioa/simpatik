from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django import forms
import json
from django.http import HttpResponse


from .models import AnggotaTim, Rekomendasi, DetilBAP
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
	def delete_ajax(self, request, id_pengajuan_izin_, id_survey, id_anggota):
		try:
			get_anggota = AnggotaTim.objects.get(pk=id_anggota)
			data = {'success': True, 'pesan': 'Anggota '+str(get_anggota.pegawai)+' berhasil Hapus.' }
			get_anggota.delete()
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': 'Anggota Tidak Ada Dalam Daftar' }

		return HttpResponseRedirect(reverse('admin:cek_kelengkapan', args=[id_pengajuan_izin_, id_survey]))


	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(AnggotaTimAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^simpan-anggotatim/$', self.admin_site.admin_view(self.simpan_ajax), name='simpan_ajax'),
			url(r'^hapus-anggotatim/(?P<id_pengajuan_izin_>[0-9]+)/(?P<id_survey>[0-9]+)/(?P<id_anggota>[0-9]+)$', self.admin_site.admin_view(self.delete_ajax), name='hapus_ajax'),
			)
		return my_urls + urls
		
admin.site.register(AnggotaTim, AnggotaTimAdmin)





admin.site.register(Rekomendasi)
admin.site.register(DetilBAP)
