from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader
from accounts.models import NomorIdentitasPengguna
from kepegawaian.models import Pegawai, UnitKerja
from izin.models import DetilIzinParkirIsidentil , Syarat, SKIzin, Riwayat, Survey, DetilSk

class DetilIzinParkirIsidentilAdmin(admin.ModelAdmin):
	def view_pengajuan_parkir(self, request, id_pengajuan):
		extra_context = {}
		extra_context.update({'has_permission': True })
		extra_context.update({'title': 'Proses Pengajuan Izin Parkir'})
		pengajuan_ = get_object_or_404(DetilIzinParkirIsidentil, id=id_pengajuan)
		# skizin_obj = pengajuan_.skizin_set.last()
		if pengajuan_:
			kendaraan_list = pengajuan_.kendaraan_set.all()
			kendaraan_count = kendaraan_list.count()
			riwayat_ = pengajuan_.riwayat_set.all().order_by('created_at')
			if riwayat_:
				extra_context.update({'riwayat': riwayat_ })
			skizin_ = pengajuan_.skizin_set.last()
			extra_context.update({'pengajuan':pengajuan_, 'pemohon': pengajuan_.pemohon, 'perusahaan':pengajuan_.perusahaan, 'status': pengajuan_.status, 'kendaraan_list': kendaraan_list, 'kendaraan_count':kendaraan_count, 'skizin':skizin_, 'url_cetak': reverse("admin:parkir__cetak_skizin", kwargs={'id_pengajuan': pengajuan_.id}),})
		template = loader.get_template("admin/izin/pengajuanizin/dishub/view_izin_parkir.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_skizin(self, request, id_pengajuan):
		extra_context = {}
		pengajuan_obj = get_object_or_404(DetilIzinParkirIsidentil, id=id_pengajuan)
		skizin_obj = pengajuan_obj.skizin_set.last()
		extra_context.update({
			'pengajuan' : pengajuan_obj,
			'skizin' : skizin_obj,
			'title' : "Cetak SK Izin Parkir "+pengajuan_obj.get_no_skizin()
			})
		return render(request, "front-end/include/formulir_iua/cetak_skizin_parkir.html", extra_context)

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilIzinParkirIsidentil, self).get_urls()
		my_urls = patterns('',
			url(r'^view-pengajuan-iua/(?P<id_pengajuan>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_iua), name='view_pangajuan_parkir'),
			url(r'^cetak/(?P<id_pengajuan>[0-9]+)$', self.admin_site.admin_view(self.cetak_skizin), name='parkir__cetak_skizin'),
			)
			
		return my_urls + urls

admin.site.register(DetilIzinParkirIsidentil, DetilIzinParkirIsidentilAdmin)