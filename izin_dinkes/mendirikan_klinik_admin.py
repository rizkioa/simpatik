from django.contrib import admin
from models import MendirikanKlinik
from django.shortcuts import get_object_or_404, render
from kepegawaian.models import UnitKerja
from django.contrib.auth.models import Group
from izin.models import Survey
from django.core.urlresolvers import reverse
from utils import get_title_verifikasi
from simpdu.api_settings import API_URL_PENGAJUAN_DINKES

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
			'url_cetak': reverse("admin:mendirikan_klinik__cetak_skizin", kwargs={'id_pengajuan': pengajuan_obj.id}),
			'url_form': reverse("admin:izin_proses_imk"),
			'API_URL_PENGAJUAN_DINKES': API_URL_PENGAJUAN_DINKES,
			'perusahaan': perusahaan_obj
			})
		return render(request, "admin/izin_dinkes/mendirikan_klinik/view_verifikasi.html", extra_context)

	def cetak_skizin(self, request, id_pengajuan):
		extra_context = {}
		pengajuan_obj = get_object_or_404(MendirikanKlinik, id=id_pengajuan)
		skizin_obj = pengajuan_obj.skizin_set.last()
		extra_context.update({
			'pengajuan' : pengajuan_obj,
			'skizin' : skizin_obj,
			'title' : "Cetak SK Izin Mendirikan Klinik "+pengajuan_obj.get_no_skizin()
			})
		return render(request, "front-end/include/formulir_izin_toko_obat/cetak_skizin.html", extra_context)

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(MendirikanKlinikAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^view-verfikasi/(?P<id_pengajuan>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_izin_mendirikan_klinik), name='mendirikan_klinik__view_verifikasi'),
			url(r'^cetak/(?P<id_pengajuan>[0-9]+)$', self.admin_site.admin_view(self.cetak_skizin), name='mendirikan_klinik__cetak_skizin'),
			)
		return my_urls + urls