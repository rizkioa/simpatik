from django.contrib import admin
from models import TokoObat
from django.shortcuts import get_object_or_404, render
from kepegawaian.models import UnitKerja
from django.contrib.auth.models import Group
from izin.models import Survey
from django.core.urlresolvers import reverse
from utils import get_title_verifikasi
from simpdu.api_settings import API_URL_PENGAJUAN_DINKES
from master.models import Settings

class TokoObatAdmin(admin.ModelAdmin):

	def view_pengajuan_izin_tokoobat(self, request, id_pengajuan):
		extra_context = {}
		pengajuan_obj = get_object_or_404(TokoObat, id=id_pengajuan)
		riwayat_list = pengajuan_obj.riwayat_set.all().order_by('created_at')
		skizin_obj = pengajuan_obj.skizin_set.last()
		jenis_izin = pengajuan_obj.kelompok_jenis_izin.kode
		perusahaan_obj = pengajuan_obj.nama_toko_obat
		# if pengajuan_obj.perusahaan:
		# 	perusahaan_obj = pengajuan_obj.perusahaan
		# else:
		# 	perusahaan_obj = pengajuan_obj.nama_toko_obat
		api_url_obj = Settings.objects.filter(parameter='API URL PENGAJUAN DINKES').last()
		if api_url_obj:
			api_url_dinkes = api_url_obj.url

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
		# print API_URL_DINKES
		extra_context.update({
			'has_permission': True,
			'title': 'Proses Verifikasi Pengajuan Izin Toko Obat',
			'pengajuan': pengajuan_obj,
			'riwayat': riwayat_list,
			'skizin': skizin_obj,
			'jenis_izin': jenis_izin,
			'skpd_list' : UnitKerja.objects.all(),
			'pegawai_list' : h,
			'survey': s,
			'banyak': len(TokoObat.objects.filter(no_izin__isnull=False))+1,
			'title_verifikasi': get_title_verifikasi(request, pengajuan_obj, skizin_obj),
			'url_cetak': reverse("admin:tokoobat__cetak_skizin", kwargs={'id_pengajuan': pengajuan_obj.id}),
			'url_form': reverse("admin:izin_proses_izin_toko_obat"),
			'API_URL_PENGAJUAN_DINKES': api_url_dinkes,
			'perusahaan': perusahaan_obj,
			'url_view_survey': reverse("admin:tokoobat__view_survey", kwargs={'id_pengajuan': pengajuan_obj.id}),
			'data_get_pengajuan_dinkes': get_pengajuan_dinkes.text,
			})
		return render(request, "admin/izin_dinkes/tokoobat/view_verifikasi.html", extra_context)

	def cetak_skizin(self, request, id_pengajuan):
		extra_context = {}
		pengajuan_obj = get_object_or_404(TokoObat, id=id_pengajuan)
		skizin_obj = pengajuan_obj.skizin_set.last()

		api_url_obj = Settings.objects.filter(parameter='URL GET SURVEY DINKES').last()
		if api_url_obj:
			url_get_dinkes = api_url_obj.url
			key_get = api_url_obj.value
			get_pengajuan_dinkes = requests.get(url_get_dinkes+'admin/izin/pengajuanizin/'+id_pengajuan+'/get-pengajuanizin-json/?key='+key_get, headers={'content-type': 'application/json'})

		extra_context.update({
			'pengajuan' : pengajuan_obj,
			'skizin' : skizin_obj,
			'data_get_pengajuan_dinkes': get_pengajuan_dinkes.text,
			'title' : "Cetak SK Izin Toko Obat "+pengajuan_obj.get_no_skizin()
			})
		return render(request, "front-end/include/formulir_izin_toko_obat/cetak_skizin.html", extra_context)

	def view_survey(self, request, id_pengajuan):

		api_url_obj = Settings.objects.filter(parameter='URL GET SURVEY DINKES').last()
		if api_url_obj:
			url_get_dinkes = api_url_obj.url
			key_get = api_url_obj.value
		 	perincian_json = requests.get(url_get_dinkes+'admin/izin/perincian/ITO/get-perincian-json/?key='+key_get, headers={'content-type': 'application/json'})
			extra_context = {
				'is_popup': 'popup',
				'id_pengajuan': id_pengajuan,
				'title': 'View Hasil Survey Optikal',
				'url_server_dinkes': url_get_dinkes,
				'key': key_get,
				'data': perincian_json.text,
				}

		return render(request, "admin/izin_dinkes/view_survey.html", extra_context)

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(TokoObatAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^view-verfikasi/(?P<id_pengajuan>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_izin_tokoobat), name='tokoobat__view_verifikasi'),
			url(r'^cetak/(?P<id_pengajuan>[0-9]+)$', self.admin_site.admin_view(self.cetak_skizin), name='tokoobat__cetak_skizin'),
			url(r'^view-rekomendasi/(?P<id_pengajuan>[0-9]+)$', self.admin_site.admin_view(self.view_survey), name='	'),
			)
		return my_urls + urls