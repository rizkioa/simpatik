from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, resolve
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader
from django.contrib import admin, messages
from django.http import HttpResponse
from izin.models import DetilIUA, Kendaraan, Riwayat, SKIzin
from simpdu import settings
import drest
from izin.utils import holder
from kepegawaian.models import UnitKerja

class DetilIUAAdmin(admin.ModelAdmin):
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
		if split_[0] == 'IUA':
			no_pengajuan = mark_safe("""
				<a href="%s" target="_blank"> %s </a>
				""" % (reverse('admin:izin_detiltdp_change', args=(obj.id,)), obj.no_pengajuan ))
		return no_pengajuan
	get_no_pengajuan.short_description = "No. Pengajuan"

	def view_pengajuan_iua(self, request, id_pengajuan):
		extra_context = {}
		extra_context.update({'has_permission': True })
		extra_context.update({'title': 'Proses Pengajuan Izin Usaha Angkutan (IUA)'})
		pengajuan_ = get_object_or_404(DetilIUA, id=id_pengajuan)
		if pengajuan_:
			kendaraan_list = pengajuan_.kendaraan_set.all()
			kendaraan_count = kendaraan_list.count()
			riwayat_ = pengajuan_.riwayat_set.all().order_by('created_at')
			if riwayat_:
				extra_context.update({'riwayat': riwayat_ })
			skizin_ = pengajuan_.skizin_set.last()
			extra_context.update({'pengajuan':pengajuan_, 'pemohon': pengajuan_.pemohon, 'perusahaan':pengajuan_.perusahaan, 'status': pengajuan_.status, 'kendaraan_list': kendaraan_list, 'kendaraan_count':kendaraan_count, 'skizin':skizin_})
		template = loader.get_template("admin/izin/pengajuanizin/dishub/view_izin_angkutan.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_sk_izin(self, request, id_pengajuan):
		extra_context = {}
		response = holder()
		if id_pengajuan:
			try:
				try:
					# api = drest.api.TastyPieAPI('http://simpatik.kedirikab.go.id/api/v1/')
					api = drest.api.TastyPieAPI('http://192.168.100.210:8000/api/v1/')
					api.auth('dishub', 'jgHwLBYweHsfKSZiJHfmIQ2L5KZDNh4J')
					api.request.add_header('X-CSRFToken', '{{csrf_token}}')
					api.request.add_header('Content-Type', 'application/json')
					# GET resource API angkutan
					detail = api.izin.get(id_pengajuan)
					if detail.status in (200, 201, 202):
						# response.pesan = detail
						# response.success = True
						from collections import OrderedDict
						a = eval(detail.data['surat']['data'])
						# print type(a)
						unit_kerja_obj = UnitKerja.objects.filter(nama_unit_kerja="DISHUB").last()

						extra_context.update({
							'pengajuan':detail.data,
							'surat': a,
							'unit_kerja':unit_kerja_obj
							})
						data_surat = detail.data['surat']['data']
						# print data_surat.
						# response.pesan = detail
                        # response.success = True
						# data = {'iua_id__contains':obj_id}
						# kendaraan = api.kendaraan.get(params=data)
						# if kendaraan.status in (200, 201, 202):
							# extra_context.update({'kendaraan': kendaraan})
					else:
						messages.add_message(request, messages.ERROR, 'Gagal Mengambil data')
				except drest.exc.dRestAPIError as e:
					messages.add_message(request, messages.ERROR, '[E002] '+str(e.msg))
			except drest.exc.dRestRequestError as e:
				messages.add_message(request, messages.ERROR, '[E001] '+str(e.msg))
		else:
			messages.add_message(request, messages.ERROR, 'Data tidak ditemukan')
		template = loader.get_template("admin/izin/izin/dishub/cetak_skizin_iua.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilIUAAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^view-pengajuan-iua/(?P<id_pengajuan>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_iua), name='view_pangajuan_iua'),
			url(r'^cetak-skizin-iua/(?P<id_pengajuan>[0-9]+)$', self.admin_site.admin_view(self.cetak_sk_izin), name='cetak_sk_izin_iua'),
			)
		return my_urls + urls

admin.site.register(DetilIUA, DetilIUAAdmin)