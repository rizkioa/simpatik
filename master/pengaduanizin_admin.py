from django.contrib import admin
from models import PengaduanIzin, PesanPengaduan
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist
import json, datetime
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.contrib import messages


class PengaduanIzinAdmin(admin.ModelAdmin):
	list_display = ('no_ktp', 'nama_lengkap', 'kelompok_jenis_izin', 'dibalas_oleh', 'status_data', 'detil')

	def dibalas_oleh(self, obj):
		dibalas = "-"
		if obj.verified_by:
			dibalas = obj.verified_by.nama_lengkap
		return dibalas
	dibalas_oleh.short_description = 'Dibalas Oleh'

	def status_data(self, obj):
		status = ""
		if obj.status == 6:
			status = '<button class="btn btn-xs btn-success" type="button">Draft</button>'
		elif obj.status == 1:
			status = '<button class="btn btn-xs btn-warning" type="button">Sudah dibalas</button>'
		elif obj.status == 2:
			status = '<button class="btn btn-xs btn-danger" type="button">Sudah ditutup</button>'

		return mark_safe(status)
	status_data.short_description = 'Status'

	def detil(self, obj):
		return mark_safe('''<button type="button" class="btn btn-info" onclick="detilpengaduan('''+str(obj.id)+''')" tittle="Lihat Detil">Lihat Detil</button> | <a href="%s" class="btn btn-success">Balas</a> | <a href="%s" class="btn btn-danger">Tutup Pengaduan</a>''' % (reverse('admin:list_pesan_pengaduan', kwargs={'id_pengaduan': obj.id}), reverse('admin:tutup_pengaduan', kwargs={'id_pengaduan': obj.id})))
	detil.short_description = 'Aksi'

	def json_pengaduanizin(self, request, id_pengaduan):
		# print id_pengaduan
		data = {'success': False, 'pesan': 'Data tidak ditemukan.', 'data': ''}
		if id_pengaduan:
			try:
				pengaduan_obj = PengaduanIzin.objects.get(id=id_pengaduan)
				# print pengaduan_obj
				# print pengaduan_obj.as_json()
				data = {'success': True, 'pesan': 'Data berhasil diload', 'data': pengaduan_obj.as_json()}
			except ObjectDoesNotExist:
				pass
		return HttpResponse(json.dumps(data))

	def balas_pengaduanizin(self, request):
		data = {'success': False, 'pesan': 'Data tidak ditemukan'}
		id_pengaduan = request.POST.get('id_pengaduan')
		balas = request.POST.get('balas')
		# print id_pengaduan
		# print isi_pengaduan
		if id_pengaduan:
			try:
				pengaduan_obj = PengaduanIzin.objects.get(id=request.POST.get('id_pengaduan'))
				if pengaduan_obj.status == 6:
					pengaduan_obj.status = 1
					pengaduan_obj.balas = balas
					pengaduan_obj.verified_by = request.user
					pengaduan_obj.verified_at = datetime.datetime.now()
					pengaduan_obj.save()
					data = {'success': True, 'pesan': 'Pengaduan berhasil dibalas.'}
				elif pengaduan_obj.status == 1:
					data = {'success': False, 'pesan': 'Pengaduan sudah dibalas.'}
				else:
					data = {'success': False, 'pesan': 'Pengaduan izin telah ditutup.'}
			except ObjectDoesNotExist:
				pass
		return HttpResponse(json.dumps(data))

	def list_pesan_pengaduan(self, request, id_pengaduan):
		extra_context = {}
		pengaduan_obj = get_object_or_404(PengaduanIzin, id=id_pengaduan)
		if pengaduan_obj:
			pesan_pengaduan_list = pengaduan_obj.pesanpengaduan_set.all()
			extra_context.update({
				'pengaduan_obj': pengaduan_obj,
				'pesan_pengaduan_list': pesan_pengaduan_list,
				'title': "Pesan Pengaduan "+pengaduan_obj.nama_lengkap
				})
			if request.POST:
				if request.POST.get('pesan') is not None:
					pesan_pengaduan_obj = PesanPengaduan(
						pengaduan_izin_id = pengaduan_obj.id,
						pesan = request.POST.get('pesan'),
						status_pemohon = False,
						created_by = request.user
						)
					pesan_pengaduan_obj.save()
					pengaduan_obj.status = 1
					pengaduan_obj.balas = request.POST.get('pesan')
					pengaduan_obj.save()
		return render(request, "admin/master/pengaduanizin/list_pesan_pengaduan.html", extra_context)

	def tutup_pengaduan(self, request, id_pengaduan):
		from django.shortcuts import redirect
		if id_pengaduan:
			try:
				pengaduanizin_obj = PengaduanIzin.objects.get(id=id_pengaduan)
				pengaduanizin_obj.status = 2
				pengaduanizin_obj.save()
				messages.success(request, 'Data Pengaduan Izin berhasil ditutup.')
			except ObjectDoesNotExist:
				messages.warning(request, 'Data Pengaduan Izin tidak ditemukan.')
		return redirect('/admin/master/pengaduanizin')

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(PengaduanIzinAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^json/(?P<id_pengaduan>[0-9]+)$', self.admin_site.admin_view(self.json_pengaduanizin), name='json_pengaduanizin'),
			url(r'^pesan/(?P<id_pengaduan>[0-9]+)$', self.admin_site.admin_view(self.list_pesan_pengaduan), name='list_pesan_pengaduan'),
			url(r'^tutup-pengaduan/(?P<id_pengaduan>[0-9]+)$', self.admin_site.admin_view(self.tutup_pengaduan), name='tutup_pengaduan'),
			url(r'^balas/$', self.admin_site.admin_view(self.balas_pengaduanizin), name='balas_pengaduanizin'),
			)
		return my_urls + urls

	def suit_cell_attributes(self, obj, column):
		if column in ['status_data', 'detil']:
			return {'class': 'text-center'}
		else:
			return None
admin.site.register(PengaduanIzin, PengaduanIzinAdmin)