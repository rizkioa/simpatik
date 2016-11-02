from django.http import HttpResponse
import json

from izin.models import PaketPekerjaan, DetilIUJK
from izin.iujk_forms import PaketPekerjaanForm, DetilIUJKForm, DataAnggotaForm
from izin.izin_forms import LegalitasPerusahaanForm, LegalitasPerusahaanPerubahanForm



def iujk_paketpekerjaan_save(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			PaketPekerjaan_ = PaketPekerjaanForm(request.POST)
			if PaketPekerjaan_.is_valid():
				p = PaketPekerjaan_.save(commit=False)
				p.detil_iujk_id = request.COOKIES['id_pengajuan']
				p.save()

				data = {'success': True, 
				'pesan': 'Paket Pekerjaan Berhasil Disimpan.',
				'data': [
							{'id': p.id},
							{'klasifikasi_usaha': p.klasifikasi_usaha},
							{'nama_paket_pekerjaan': p.nama_paket_pekerjaan},
							{'tahun': p.tahun},
							{'nilai_paket_pekerjaan': 'Rp. '+'{:,.2f}'.format(float(p.nilai_paket_pekerjaan))},
							{'nilai_str': str(p.nilai_paket_pekerjaan)},
							{'delete':False},
						]
				}
				data = json.dumps(data)
				response = HttpResponse(data)
			else:
				data = PaketPekerjaan_.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	# response.set_cookie(key='id_detail_siup', value=pengajuan_.id)
	return response

def iujk_paketpekerjaan_edit(request, id_paket_):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			paket_ = PaketPekerjaan.objects.get(id=id_paket_)
			PaketPekerjaan_ = PaketPekerjaanForm(request.POST, instance=paket_)
			if PaketPekerjaan_.is_valid():
				p = PaketPekerjaan_.save(commit=False)
				p.detil_iujk_id = request.COOKIES['id_pengajuan']
				p.save()

				data = {'success': True, 
				'pesan': 'Perubahan Paket Pekerjaan Berhasil Disimpan.',
				'data': [
							{'id': p.id},
							{'klasifikasi_usaha': p.klasifikasi_usaha},
							{'nama_paket_pekerjaan': p.nama_paket_pekerjaan},
							{'tahun': p.tahun},
							{'nilai_paket_pekerjaan': 'Rp. '+'{:,.2f}'.format(float(p.nilai_paket_pekerjaan))},
							{'nilai_str': str(p.nilai_paket_pekerjaan)},
							{'delete':True},
						]
				}
				data = json.dumps(data)
				response = HttpResponse(data)
			else:
				data = PaketPekerjaan_.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	# response.set_cookie(key='id_detail_siup', value=pengajuan_.id)
	return response


# IUJK DETIL TIDAK ADA LEGALITAS
def iujk_detiliujk_save(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilIUJK.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			DetilIUJKForm_ = DetilIUJKForm(request.POST, instance=pengajuan_)
			if DetilIUJKForm_.is_valid():
				iujk = DetilIUJKForm_.save(commit=False)
				iujk.perusahaan_id = request.COOKIES['id_perusahaan']
				iujk.save()
				data = {'success': True, 
					'pesan': 'Data IUJK Berhasil Disimpan.',
					'data': []
				}
				data = json.dumps(data)
				response = HttpResponse(data)
			else:
				data = DetilIUJKForm_.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)

	return response

def iujk_legalitas_perusahaan_save(request):
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			if 'id_pengajuan' in request.COOKIES.keys():
				if request.COOKIES['id_pengajuan'] != '':
					pengajuan_ = DetilIUJK.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
					if request.POST.get('onoffswitch_pendirian') == 'on':
						form = LegalitasPerusahaanForm(request.POST)
						if form.is_valid():
							f = form.save(commit=False)
							f.perusahaan_id = request.COOKIES['id_perusahaan']
							if request.user.is_authenticated():
								f.created_by_id = request.user.id
							else:
								f.created_by_id = request.COOKIES['id_pemohon']
							f.save()
							pengajuan_.legalitas.add(f)
							data = {'success': True, 'pesan': 'Legalitas Perusahaan berhasil disimpan. Proses Selanjutnya.', 'data': [
								{'jenis_legalitas': f.jenis_legalitas.jenis_legalitas},
								{'nama_notaris': f.nama_notaris},
								{'alamat_notaris': f.alamat},
								{'telephone_notaris': f.telephone},
								{'nomor_pengesahaan': f.nomor_pengesahan},
								{'tanggal_pengesahan': str(f.tanggal_pengesahan)}
								]}
							data = json.dumps(data)
							response = HttpResponse(data)
							response.set_cookie(key='id_legalitas', value=f.id)

							if request.POST.get('onoffswitch') == 'on':
								formperubahan = LegalitasPerusahaanPerubahanForm(request.POST)
								
								if formperubahan.is_valid():
									if request.user.is_authenticated():
										created = request.user.id
									else:
										created = request.COOKIES['id_pemohon']
									legalitas = Legalitas(
										created_by_id = created,	
										jenis_legalitas_id = 2,
										perusahaan_id = request.COOKIES['id_perusahaan'],
										nama_notaris=request.POST.get('nama_notaris_perubahan'), 
										alamat=request.POST.get('alamat_notaris_perubahan'), 
										telephone=request.POST.get('telephone_notaris_perubahan'), 
										nomor_pengesahan=request.POST.get('nomor_pengesahan_perubahan'), 
										tanggal_pengesahan=formperubahan.cleaned_data['tanggal_pengesahan_perubahan'])
									legalitas.save()
									pengajuan_.legalitas.add(legalitas)
									data = {'success': True, 'pesan': 'Legalitas Perusahaan berhasil disimpan. Proses Selanjutnya.', 'data': [
										# # legalitas perubahaan
										{'jenis_legalitas_perubahan': legalitas.jenis_legalitas.jenis_legalitas},
										{'nama_notaris_perubahan': legalitas.nama_notaris},
										{'alamat_notaris_perubahan': legalitas.alamat},
										{'telephone_notaris_perubahan': legalitas.telephone},
										{'nomor_pengesahaan_perubahan': legalitas.nomor_pengesahan},
										{'tanggal_pengesahan_perubahan': str(legalitas.tanggal_pengesahan)}
										]}
									data = json.dumps(data)
									response = HttpResponse(data)
									response.set_cookie(key='id_legalitas_perubahan', value=legalitas.id)
								else:
									data = formperubahan.errors.as_json()
									response = HttpResponse(data)
						# else:
						# 	data = {'Terjadi Kesalahan': [{'message': 'Data Perusahaan tidak ditemukan/data kosong'}]}
						# 	data = json.dumps(data)
						# 	response = HttpResponse(data)

						else:
							data = form.errors.as_json()
							response = HttpResponse(data)
					else:
						pengajuan_.jenis_pengajuan = 1
						pengajuan_.save()
						data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': []}
						data = json.dumps(data)
						response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
				data = json.dumps(data)
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response


def penanggung_jawab_save_bu():
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pass
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)

	return response