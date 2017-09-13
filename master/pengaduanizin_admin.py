from django.contrib import admin
from models import PengaduanIzin
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist
import json, datetime
from django.http import HttpResponse
from django.core.urlresolvers import reverse


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
		return mark_safe('<button type="button" class="btn btn-info" onclick="detilpengaduan('+str(obj.id)+')" tittle="Lihat Detil">Lihat Detil</button>')
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

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(PengaduanIzinAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^json/(?P<id_pengaduan>[0-9]+)$', self.admin_site.admin_view(self.json_pengaduanizin), name='json_pengaduanizin'),
			url(r'^balas/$', self.admin_site.admin_view(self.balas_pengaduanizin), name='balas_pengaduanizin'),
			)
		return my_urls + urls

	def suit_cell_attributes(self, obj, column):
		if column in ['status_data', 'detil']:
			return {'class': 'text-center'}
		else:
			return None
admin.site.register(PengaduanIzin, PengaduanIzinAdmin)