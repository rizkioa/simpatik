from django.contrib import admin, messages
from models import Laboratorium
from django.shortcuts import get_object_or_404, render
from kepegawaian.models import UnitKerja
from django.contrib.auth.models import Group
from izin.models import Survey
from django.core.urlresolvers import reverse
from utils import get_title_verifikasi
from simpdu.api_settings import API_URL_PENGAJUAN_DINKES
from master.models import Settings
from requests.exceptions import ConnectionError

import requests

class LaboratoriumAdmin(admin.ModelAdmin):

	def view_pengajuan_izin_laboratorium(self, request, id_pengajuan):
		extra_context = {}
		pengajuan_obj = get_object_or_404(Laboratorium, id=id_pengajuan)
		riwayat_list = pengajuan_obj.riwayat_set.all().order_by('created_at')
		skizin_obj = pengajuan_obj.skizin_set.last()
		perusahaan_obj = pengajuan_obj.nama_laboratorium
		jenis_izin = pengajuan_obj.kelompok_jenis_izin.kode

		api_url_obj = Settings.objects.filter(parameter='API URL PENGAJUAN DINKES').last()
		if api_url_obj:
			api_url_dinkes = api_url_obj.url
			api_berkas_dinkes = api_url_obj_.url[:-1]

		h = Group.objects.filter(name="Cek Lokasi")
		if h.exists():
			h = h.last()
		h = h.user_set.all()

		try:
			try:
				s = Survey.objects.get(pengajuan=pengajuan_obj)
			except Survey.MultipleObjectsReturned:
				s = Survey.objects.filter(pengajuan=pengajuan_obj).last()
			extra_context.update({'detilbap': s.survey_reklame_ho.all().last() })
		except Survey.DoesNotExist:
			s = ""

		no_pengajuan_encode = pengajuan_obj.no_pengajuan.encode('base64')
		no_pengajuan_encode = no_pengajuan_encode[:-1]

		api_url_obj = Settings.objects.filter(parameter='URL GET SURVEY DINKES').last()
		if api_url_obj:
			url_get_dinkes = api_url_obj.url
			key_get = api_url_obj.value
			get_pengajuan_dinkes = requests.get(url_get_dinkes+'admin/izin/pengajuanizin/'+no_pengajuan_encode+'/get-pengajuanizin-json/?key='+key_get, headers={'content-type': 'application/json'})

		extra_context.update({
			'has_permission': True,
			'title': 'Proses Verifikasi Pengajuan Izin Laboratorium',
			'pengajuan': pengajuan_obj,
			'jenis_izin': jenis_izin,
			'riwayat': riwayat_list,
			'skizin': skizin_obj,
			'skpd_list' : UnitKerja.objects.all(),
			'pegawai_list' : h,
			'survey': s,
			'banyak': len(Laboratorium.objects.filter(no_izin__isnull=False))+1,
			'title_verifikasi': get_title_verifikasi(request, pengajuan_obj, skizin_obj),
			'url_cetak': reverse("admin:laboratorium__cetak_skizin", kwargs={'id_pengajuan': pengajuan_obj.id}),
			'url_form': reverse("admin:izin_proses_izin_laboratorium"),
			'API_URL_PENGAJUAN_DINKES': api_url_dinkes,
			'API_BERKAS_DINKES': api_berkas_dinkes,
			'perusahaan': perusahaan_obj
			})
		return render(request, "admin/izin_dinkes/laboratorium/view_verifikasi.html", extra_context)

	def cetak_skizin(self, request, id_pengajuan):
		extra_context = {}
		pengajuan_obj = get_object_or_404(Laboratorium, id=id_pengajuan)
		skizin_obj = pengajuan_obj.skizin_set.last()
		extra_context.update({
			'pengajuan' : pengajuan_obj,
			'skizin' : skizin_obj,
			'title' : "Cetak SK Izin Laboratorium "+pengajuan_obj.get_no_skizin()
			})
		return render(request, "front-end/include/formulir_izin_toko_obat/cetak_skizin.html", extra_context)

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(LaboratoriumAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^view-verfikasi/(?P<id_pengajuan>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_izin_laboratorium), name='izinlaboratorium__view_verifikasi'),
			url(r'^cetak/(?P<id_pengajuan>[0-9]+)$', self.admin_site.admin_view(self.cetak_skizin), name='laboratorium__cetak_skizin'),
			)
		return my_urls + urls