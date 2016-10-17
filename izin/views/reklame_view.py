from izin.izin_forms import PengajuanReklameForm
import json
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from master.models import Berkas
from izin.models import DetilReklame, PengajuanIzin
from izin.izin_forms import UploadBerkasPendukungForm


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

def reklame_upload_berkas_pendukung(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			form = UploadBerkasPendukungForm(request.POST, request.FILES)
			# print request.FILES
			if request.method == "POST":
				if request.FILES.get('berkas'):
					if form.is_valid():
						try:
							p = PengajuanIzin.objects.get(id=request.COOKIES['id_pengajuan'])
							berkas = form.save(commit=False)
							berkas.nama_berkas = "Berkas Pendukung "+p.pemohon.nama_lengkap
							if request.user.is_authenticated():
								berkas.created_by_id = request.user.id
							else:
								berkas.created_by_id = request.COOKIES['id_pemohon']
							berkas.save()
							p.berkas_tambahan.add(berkas)

							data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
									{'status_upload': 'ok'},
								]}
						except ObjectDoesNotExist:
							data = {'Terjadi Kesalahan': [{'message': 'Pengajuan tidak ada dalam daftar'}]}
						data = json.dumps(data)
						response = HttpResponse(data)
					else:
						data = form.errors.as_json()
						response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = form.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response
