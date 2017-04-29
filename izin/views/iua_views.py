import json
import datetime
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from izin.models import DetilIUA

def save_data_kendaraan(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				try:
					pengajuan_ = DetilIUA.objects.get(id=request.COOKIES['id_pengajuan'])
					pengajuan_.nilai_investasi = request.POST.get('nilai_investasi')
					pengajuan_.kategori_kendaraan = request.POST.get('kategori_kendaraan')
					pengajuan_.save()
					data = {'success': True, 'pesan': 'Data Umum Perusahaan berhasil tersimpan.', 'data': []}
				except ObjectDoesNotExist:
					data = {'success':False, 'pesan': 'sjhajsd', 'data': []}
			else:
				data = {'success':False, 'pesan': 'sjhajsd', 'data': []}
		else:
			data = {'success':False, 'pesan': 'sjhajsd', 'data': []}
	else:
		data = {'success':False, 'pesan': 'sjhajsd', 'data': []}
	data = json.dumps(data)
	response = HttpResponse(data)
	return response

