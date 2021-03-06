from django.contrib import admin, messages
from models import MendirikanKlinik
from django.shortcuts import get_object_or_404, render
from kepegawaian.models import UnitKerja
from django.contrib.auth.models import Group
from izin.models import Survey
from django.core.urlresolvers import reverse
from utils import get_title_verifikasi
# from simpdu.api_settings import API_URL_PENGAJUAN_DINKES
from master.models import Settings
from requests.exceptions import ConnectionError
import requests

class MendirikanKlinikAdmin(admin.ModelAdmin):

	def view_pengajuan_izin_mendirikan_klinik(self, request, id_pengajuan):
		extra_context = {}
		pengajuan_obj = get_object_or_404(MendirikanKlinik, id=id_pengajuan)
		riwayat_list = pengajuan_obj.riwayat_set.all().order_by('created_at')
		skizin_obj = pengajuan_obj.skizin_set.last()
		jenis_izin = pengajuan_obj.kelompok_jenis_izin.kode

		if pengajuan_obj.perusahaan:
			perusahaan_obj = pengajuan_obj.perusahaan
		else:
			perusahaan_obj = pengajuan_obj.nama_klinik

		api_url_obj_ = Settings.objects.filter(parameter='API URL PENGAJUAN DINKES').last()
		if api_url_obj_:
			api_url_dinkes = api_url_obj_.url
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
		print no_pengajuan_encode.decode('base64')
		no_pengajuan_encode = no_pengajuan_encode[:-1]

		api_url_obj = Settings.objects.filter(parameter='URL GET SURVEY DINKES').last()
		if api_url_obj:
			url_get_dinkes = api_url_obj.url
			key_get = api_url_obj.value
			try:
				get_pengajuan_dinkes = requests.get(url_get_dinkes+'admin/izin/pengajuanizin/'+no_pengajuan_encode+'/get-pengajuanizin-json/?key='+key_get, headers={'content-type': 'application/json'})
				extra_context.update({
					'data_get_pengajuan_dinkes': get_pengajuan_dinkes.text,
					})
			except ConnectionError as e:
				messages.add_message(request, messages.ERROR, "Koneksi pada URL Request gagal, Tidak Bisa Mengambil data dinkes, Cek kembali Url Request server ("+url_get_dinkes+")")
		extra_context.update({
			'has_permission': True,
			'title': 'Proses Verifikasi Pengajuan Izin Mendirikan Klinik',
			'pengajuan': pengajuan_obj,
			'jenis_izin': jenis_izin,
			'riwayat': riwayat_list,
			'skizin': skizin_obj,
			'skpd_list' : UnitKerja.objects.all(),
			'pegawai_list' : h,
			'survey': s,
			'banyak': len(MendirikanKlinik.objects.filter(no_izin__isnull=False))+1,
			'title_verifikasi': get_title_verifikasi(request, pengajuan_obj, skizin_obj),
			'url_cetak': reverse("admin:mendirikan_klinik__cetak_skizin", kwargs={'id_pengajuan': pengajuan_obj.id, 'no_pengajuan': no_pengajuan_encode	}),
			'url_form': reverse("admin:izin_proses_imk"),
			'url_view_survey': reverse("admin:mendirikan_klinik__view_survey", kwargs={'no_pengajuan': no_pengajuan_encode}),
			'API_URL_PENGAJUAN_DINKES': api_url_dinkes,
			'API_BERKAS_DINKES': api_berkas_dinkes,
			'perusahaan': perusahaan_obj,
			})
		return render(request, "admin/izin_dinkes/mendirikan_klinik/view_verifikasi.html", extra_context)

	def cetak_skizin(self, request, id_pengajuan, no_pengajuan):
		extra_context = {}
		pengajuan_obj = get_object_or_404(MendirikanKlinik, id=id_pengajuan)
		skizin_obj = pengajuan_obj.skizin_set.last()

		no_pengajuan_ = (no_pengajuan).decode('base64')

		api_url_obj = Settings.objects.filter(parameter='URL GET SURVEY DINKES').last()
		if api_url_obj:
			url_get_dinkes = api_url_obj.url
			key_get = api_url_obj.value
			try:
				get_pengajuan_dinkes = requests.get(url_get_dinkes+'admin/izin/pengajuanizin/'+no_pengajuan_+'/get-pengajuanizin-json/?key='+key_get, headers={'content-type': 'application/json'})
				extra_context.update({
					'data_get_pengajuan_dinkes': get_pengajuan_dinkes.text,
					})
			except ConnectionError as e:
				extra_context.update({
					'pengajuan' : pengajuan_obj,
					'skizin' : skizin_obj,
					'title' : "Cetak SK Izin Mendirikan Klinik "+pengajuan_obj.get_no_skizin()
					})
		return render(request, "front-end/include/formulir_izin_mendirikan_klinik/cetak_skizin_klinik.html", extra_context)

	def view_survey(self, request, no_pengajuan):

		api_url_obj = Settings.objects.filter(parameter='URL GET SURVEY DINKES').last()
		if api_url_obj:
			url_get_dinkes = api_url_obj.url
			key_get = api_url_obj.value
			try:
			 	perincian_json = requests.get(url_get_dinkes+'admin/izin/perincian/IMK/get-perincian-json/?key='+key_get, headers={'content-type': 'application/json'})
				extra_context = {
					'is_popup': 'popup',
					'no_pengajuan_': no_pengajuan,
					'title': 'View Hasil Survey Mendirikan Klinik',
					'url_server_dinkes': url_get_dinkes,
					'key': key_get,
					'data': perincian_json.text,
					}
			except ConnectionError as e:
				messages.add_message(request, messages.ERROR, "Koneksi pada URL Request gagal, Tidak Bisa Mengambil data dinkes, Cek kembali Url Request server ("+url_get_dinkes+")")

		return render(request, "admin/izin_dinkes/view_survey.html", extra_context)

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(MendirikanKlinikAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^view-verfikasi/(?P<id_pengajuan>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_izin_mendirikan_klinik), name='mendirikan_klinik__view_verifikasi'),
			url(r'^cetak/(?P<id_pengajuan>[0-9]+)/(?P<no_pengajuan>[0-9A-Za-z_\-/]+)$', self.admin_site.admin_view(self.cetak_skizin), name='mendirikan_klinik__cetak_skizin'),
			url(r'^view-rekomendasi/(?P<no_pengajuan>[0-9A-Za-z_\-/]+)$', self.admin_site.admin_view(self.view_survey), name='mendirikan_klinik__view_survey'),
			)
		return my_urls + urls