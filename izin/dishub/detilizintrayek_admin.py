from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, resolve
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader
from django.contrib import admin
from django.http import HttpResponse
from izin.models import DetilIUA, Kendaraan, DetilTrayek

class DetilTrayekAdmin(admin.ModelAdmin):
	list_display = ('get_no_pengajuan', 'pemohon', 'get_kelompok_jenis_izin')

	def get_kelompok_jenis_izin(self, obj):
		return obj.kelompok_jenis_izin
	get_kelompok_jenis_izin.short_description = "Izin Pengajuan"

	def get_no_pengajuan(self, obj):
		no_pengajuan = mark_safe("""
			<a href="%s" target="_blank"> %s </a>
			""" % ("#", obj.no_pengajuan ))
		split_ = obj.no_pengajuan.split('/')
		# print split_
		if split_[0] == 'Trayek':
			no_pengajuan = mark_safe("""
				<a href="%s" target="_blank"> %s </a>
				""" % (reverse('admin:izin_detiltdp_change', args=(obj.id,)), obj.no_pengajuan ))
		return no_pengajuan
	get_no_pengajuan.short_description = "No. Pengajuan"

	def view_pengajuan_trayek(self, request, id_pengajuan):
		extra_context = {}
		extra_context.update({'has_permission': True })
		extra_context.update({'title': 'Proses Pengajuan Izin Usaha Trayek Angkutan'})
		pengajuan_ = get_object_or_404(DetilTrayek, id=id_pengajuan)
		if pengajuan_:
			kendaraan_list = pengajuan_.kendaraan_set.all()
			kendaraan_count = kendaraan_list.count()
			riwayat_ = pengajuan_.riwayat_set.all().order_by('created_at')
			if riwayat_:
				extra_context.update({'riwayat': riwayat_ })
			skizin_ = pengajuan_.skizin_set.last()
			extra_context.update({'pengajuan':pengajuan_, 'pemohon': pengajuan_.pemohon, 'perusahaan':pengajuan_.perusahaan, 'status': pengajuan_.status, 'kendaraan': kendaraan_list, 'kendaraan_count':kendaraan_count, 'skizin':skizin_})
		template = loader.get_template("admin/izin/pengajuanizin/dishub/view_izin_trayek.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilTrayekAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^view-pengajuan-trayek/(?P<id_pengajuan>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_trayek), name='view_pangajuan_trayek'),
			)
		return my_urls + urls

admin.site.register(DetilTrayek, DetilTrayekAdmin)