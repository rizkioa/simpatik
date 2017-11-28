from django.contrib import admin
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
import json

from izin.models import PaketPekerjaan

class PaketPekerjaanAdmin(admin.ModelAdmin):
	"""docstring for PaketPekerjaanAdmin"""
	list_display = ('detil_iujk', 'nama_paket_pekerjaan','klasifikasi_usaha','tahun','nilai_paket_pekerjaan')

	def ajax_paketpekerjaan(self, request, id_pengajuan_):
		if id_pengajuan_:
			obj = PaketPekerjaan.objects.filter(detil_iujk_id = id_pengajuan_).last()
			if obj:
				response = {'success': True, 'pesan':'', 
							}
			else:
				response = {'success': False, 'pesan':'Pengajuan tidak ditemukan'}	
		else:
			response = {'success': False, 'pesan':'Pengajuan kosong/Tidak ada'}

		return HttpResponse(json.dumps(response))

	
	def delete_paketpekerjaan(self, request):
		# print request.user.has_perm('izin.delete_paketpekerjaan')
		# if request.user.has_perm('izin.delete_paketpekerjaan'):
			
		# else:
		# 	response = {'success': False, 'pesan':'Anda Tidak Punya Akses'}
		# APAKAH PERLU UNTUK CEK HAK AKSES?? JIKA YA BAGAIMANA UNTUK HANDLING FORM UNTUK UMUM??
		id_paket_ = request.POST.get('id_paket_pekerjaan')
		if id_paket_:
			try:
				obj = PaketPekerjaan.objects.get(id = id_paket_)
				pesan_ = "Paket Pekejraan "+str(obj.nama_paket_pekerjaan)+" Berhasil Dihapus"
				obj.delete()
				response = {'success': True, 'pesan': pesan_}
			except ObjectDoesNotExist:
				response = {'success': False, 'pesan':'Paket Pekerjaan Tidak ada'}
		else:
			response = {'success': False, 'pesan':'Paket Pekerjaan Kosong'}

		return HttpResponse(json.dumps(response))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(PaketPekerjaanAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^delete/$', self.admin_site.admin_view(self.delete_paketpekerjaan), name='delete_paketpekerjaan'),
			)
		return my_urls + urls
		

admin.site.register(PaketPekerjaan, PaketPekerjaanAdmin)