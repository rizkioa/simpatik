from izin.izin_forms import PengajuanReklameForm
import json
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from master.models import Berkas
from izin.models import DetilReklame


def reklame_detilreklame_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilReklame.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			detilReklame = PengajuanReklameForm(request.POST, instances=pengajuan_)
			if detilReklame.is_valid():
				pengajuan_.perusahaan = request.COOKIES['id_perusahaan']
				pengajuan_.save()
				letak_ = pengajuan_.letak_pemasangan + "Desa "+str(pengajuan_.desa) + "Kec. "+str(pengajuan_.desa.kecamatan) + str(pengajuan_.desa.kecamatan.kabupaten)
				data = {'success': True,
						'pesan': 'Data Reklame berhasil disimpan. Proses Selanjutnya.',
						'data': [
						{'jenis_reklame': pengajuan_.jenis_reklame},
						{'judul_reklame': pengajuan_.judul_reklame},
						{'panjang': pengajuan_.panjang},
						{'lebar': pengajuan_.lebar},
						{'sisi': pengajuan_.sisi},
						{'letak_pemasangan': letak_}]}
				data = json.dumps(data)
				response = HttpResponse(json.dumps(data))
			else:
				data = detilSIUP.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response