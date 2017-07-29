import os
import json
import datetime
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from izin.models import DetilIzinParkirIsidentil, DataAnggotaParkir, PengajuanIzin
from izin.forms.izin_parkir_forms import DetilIzinParkirIsidentilForm, DataAnggotaParkirForm
from izin.tdp_forms import BerkasForm
from master.models import Berkas

def save_detil_izin_parkir(request):
	data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
	data = json.dumps(data)
	response = HttpResponse(data)
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				pengajuan_obj = DetilIzinParkirIsidentil.objects.filter(id=request.COOKIES['id_pengajuan']).last()
				form_detilizinparkir = DetilIzinParkirIsidentilForm(request.POST, instance=pengajuan_obj)
				if form_detilizinparkir.is_valid():
					p = form_detilizinparkir.save(commit=False)
					p.save()
					data = {'success': True, 'pesan': 'Data Izin Parkir berhasil tersimpan.', 'data': data}
					response = HttpResponse(json.dumps(data))
				else:
					data = form_detilizinparkir.errors.as_json()
					data = {'success': False, 'pesan': 'Data Izin Parkir gagal.', 'data': data}
					response = HttpResponse(json.dumps(data))
	return response

def load_detil_izin_parkir(request, id_pengajuan):
	data = {}
	response = {'success': False, 'pesan': 'Data Umum Perusahaan berhasil tersimpan.', 'data': data}
	if id_pengajuan:
		pengajuan_obj = DetilIzinParkirIsidentil.objects.filter(id=id_pengajuan).last()
		if pengajuan_obj:
			data = pengajuan_obj.as_json()
			response = {'success': True, 'pesan': 'Data Umum Perusahaan berhasil tersimpan.', 'data': data}
	return HttpResponse(json.dumps(response))

def save_data_anggota(request):
	data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
	data = json.dumps(data)
	response = HttpResponse(data)
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				pengajuan_obj = DetilIzinParkirIsidentil.objects.filter(id=request.COOKIES['id_pengajuan']).last()
				form_data_anggota = DataAnggotaParkirForm(request.POST)
				if form_data_anggota.is_valid():
					p = form_data_anggota.save(commit=False)
					p.izin_parkir_isidentil_id = request.COOKIES['id_pengajuan']
					p.save()
					data = {'success': True, 'pesan': 'Data Anggota berhasil tersimpan.'}
					response = HttpResponse(json.dumps(data))
				else:
					data = form_data_anggota.errors.as_json()
					data = {'success': False, 'pesan': 'Data Anggota gagal.', 'data': data}
					response = HttpResponse(json.dumps(data))
	return response

def load_data_anggota(request, id_pengajuan):
	data = []
	response = {'success': False, 'pesan': 'Data gagal diload.', 'data': data} 
	if id_pengajuan:
		pengajuan_list = DataAnggotaParkir.objects.filter(izin_parkir_isidentil_id=id_pengajuan)
		if pengajuan_list:
			data = [x.as_json() for x in pengajuan_list]
			response = {'success': True, 'pesan': 'Data berhasil diload.', 'data': data}
	return HttpResponse(json.dumps(response))

def delete_data_anggota(response, id_data_anggota):
	data = {'success': False, 'pesan': 'Data gagal dihapus.'}
	if id_data_anggota:
		data_anggota_obj = DataAnggotaParkir.objects.filter(id=id_data_anggota)
		if data_anggota_obj:
			data_anggota_obj.delete()
			data = {'success': True, 'pesan': 'Data berhasil dihapus.'}
	return HttpResponse(json.dumps(data))

def upload_berkas_save(request):
	data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/tidak ada'}]}
	data = json.dumps(data)
	response = HttpResponse(data)
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			form = BerkasForm(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if berkas_._size > 4*1024*1024:
				data = {'Terjadi Kesalahan': [{'message': 'Ukuran file tidak boleh melebihi dari 4mb.'}]}
				data = json.dumps(data)
				response = HttpResponse(data)
			else:
				if request.method == "POST":
					if berkas_:
						if form.is_valid():
							ext = os.path.splitext(berkas_.name)[1]
							valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.jpeg', '.png', '.PDF', '.DOC', '.DOCX', '.JPG', '.JPEG', '.PNG']
							if not ext in valid_extensions:
								data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
								data = json.dumps(data)
								response = HttpResponse(data)
							else:
								try:
									pengajuan_obj = DetilIzinParkirIsidentil.objects.get(id=request.COOKIES['id_pengajuan'])
									kode = request.POST.get('kode')
									berkas = form.save(commit=False)
									if pengajuan_obj:
										if pengajuan_obj.pemohon:
											nomor_ktp = pengajuan_obj.pemohon.nomoridentitaspengguna_set.filter(jenis_identitas=1).last()
											if kode == 'KTP':
												berkas.nama_berkas = "KTP "+pengajuan_obj.pemohon.nama_lengkap
												berkas.keterangan = "KTP "+nomor_ktp.nomor
											elif kode == 'Sketsa Lokasi Tempat Parkir':
												berkas.nama_berkas = "Sketsa Lokasi Tempat Parkir/Gambar Lokasi Tempar Parkir "+pengajuan_obj.pemohon.nama_lengkap
												berkas.keterangan = "Sketsa Lokasi Tempat Parkir/Gambar Lokasi Tempar Parkir "+nomor_ktp.nomor
											elif kode == 'Surat Pernyataan':
												berkas.nama_berkas = "Surat Pernyataan"+pengajuan_obj.pemohon.nama_lengkap
												berkas.keterangan = "Surat Pernyataan "+nomor_ktp.nomor

											if request.user.is_authenticated():
												berkas.created_by_id = request.user.id
											else:
												berkas.created_by_id = request.COOKIES['id_pemohon']
											berkas.save()
											pengajuan_obj.berkas_tambahan.add(berkas)
											pengajuan_obj.berkas_terkait_izin.add(berkas)

											data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
													{'status_upload': 'ok'},
												]}
											data = json.dumps(data)
											response = HttpResponse(data)
									else:
										data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar'}]}
										data = json.dumps(data)
										response = HttpResponse(data)
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
	return response

def load_berkas_izin_parkir(request, id_pengajuan):
	url_berkas = []
	id_elemen = []
	nm_berkas =[]
	id_berkas =[]
	data = {'success': False, 'pesan': 'Data tidak ditemukan/kosong.' }
	if id_pengajuan:
		try:
			pengajuan_obj = DetilIzinParkirIsidentil.objects.get(id=id_pengajuan)
			if pengajuan_obj:
				if pengajuan_obj.pemohon:
					pemohon_obj = pengajuan_obj.pemohon
					nomor_ktp = pemohon_obj.nomoridentitaspengguna_set.filter(jenis_identitas=1).last()
				# 	if nomor_ktp:
				# 		ktp_ = Berkas.objects.filter(nama_berkas="Berkas KTP Pemohon "+str(nomor_ktp.nomor)).last()
				# 		if ktp_:
				# 			url_berkas.append(ktp_.berkas.url)
				# 			id_elemen.append('ktp')
				# 			nm_berkas.append(ktp_.nama_berkas)
				# 			id_berkas.append(ktp_.id)
					if nomor_ktp:
						if pengajuan_obj.berkas_tambahan:
							berkas_tambahan = pengajuan_obj.berkas_tambahan
							ktp = berkas_tambahan.filter(keterangan='KTP '+nomor_ktp.nomor).last()
							if ktp:
								url_berkas.append(ktp.berkas.url)
								id_elemen.append('ktp')
								nm_berkas.append(ktp.nama_berkas)
								id_berkas.append(ktp.id)

							sketsa_lokasi = berkas_tambahan.filter(keterangan='Sketsa Lokasi Tempat Parkir/Gambar Lokasi Tempar Parkir '+nomor_ktp.nomor).last()
							if sketsa_lokasi:
								url_berkas.append(sketsa_lokasi.berkas.url)
								id_elemen.append('sketsa_lokasi')
								nm_berkas.append(sketsa_lokasi.nama_berkas)
								id_berkas.append(sketsa_lokasi.id)

							surat_pernyataan = berkas_tambahan.filter(keterangan='Surat Pernyataan '+nomor_ktp.nomor).last()
							if surat_pernyataan:
								url_berkas.append(surat_pernyataan.berkas.url)
								id_elemen.append('surat_pernyataan')
								nm_berkas.append(surat_pernyataan.nama_berkas)
								id_berkas.append(surat_pernyataan.id)
			data = {'success': True, 'pesan': 'Perusahaan Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': 'Data tidak ditemukan/kosong.' }
	response = HttpResponse(json.dumps(data))
	return response

def delete_berkas_izin_parkir(request, id_berkas, kode):
	data = {'success': False, 'pesan': 'Berkas Tidak Ada' }
	if id_berkas:
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan'] != '':
				try:
					pengajuan_obj = DetilIzinParkirIsidentil.objects.get(id=request.COOKIES['id_pengajuan'])
					if pengajuan_obj:
						if kode == 'ktp':
							if pengajuan_obj.pemohon:
								nomor_ktp = pengajuan_obj.pemohon.nomoridentitaspengguna_set.filter(jenis_identitas=1)
								if nomor_ktp:
									nomor_ktp.berkas = None
									nomor_ktp.save()
					try:
						b = Berkas.objects.get(id=id_berkas)
						data = {'success': True, 'pesan': str(b)+" berhasil dihapus" }
						b.delete()
					except ObjectDoesNotExist:
						pass
				except ObjectDoesNotExist:
					pass
	return HttpResponse(json.dumps(data))

def load_konfirmasi(request, id_pengajuan):
	data = {'success': False, 'pesan': 'Data tidak ditemukan.' }
	if id_pengajuan:
		try:
			pengajuan_obj = PengajuanIzin.objects.get(id=id_pengajuan)
			detil_obj = DetilIzinParkirIsidentil.objects.filter(id=id_pengajuan).last()
			pengajuan_json = {}
			pemohon_json = {}
			detil_json = {}
			data_anggota_json = []
			if pengajuan_obj:
				pengajuan_json = pengajuan_obj.as_json()
				if pengajuan_obj.pemohon:
					pemohon_json = pengajuan_obj.pemohon.as_json()

				if detil_obj:
					detil_json = detil_obj.as_json()
					data_anggota_list = DataAnggotaParkir.objects.filter(izin_parkir_isidentil_id=detil_obj.id)
					if data_anggota_list:
						data_anggota_json = [x.as_json() for x in data_anggota_list]
			data = {'success': True, 'pesan': 'Data tidak ditemukan.', 'data': { 'pengajuan_json':pengajuan_json, 'pemohon_json': pemohon_json, 'detil_json': detil_json, 'data_anggota_json': data_anggota_json}}
		except ObjectDoesNotExist:
			pass
	return HttpResponse(json.dumps(data))

def izin_parkir_done(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilIzinParkirIsidentil.objects.get(id=request.COOKIES['id_pengajuan'])
			pengajuan_.status = 6
			pengajuan_.save()
					
			data = {'success': True, 'pesan': 'Proses Selesai.' }
			response = HttpResponse(json.dumps(data))
			response.delete_cookie(key='id_jenis_pengajuan')
			response.delete_cookie(key='id_kelompok_izin')
			response.delete_cookie(key='kode_kelompok_jenis_izin')
			response.delete_cookie(key='id_pengajuan')
			response.delete_cookie(key='id_perusahaan')
			response.delete_cookie(key='nomor_ktp')
			response.delete_cookie(key='nomor_paspor')
			response.delete_cookie(key='id_pemohon')
			response.delete_cookie(key='id_jenis_pengajuan')
			response.delete_cookie(key='npwp_perusahaan')
			response.delete_cookie(key='npwp_perusahaan_induk') # set cookie
		else:
			data = {'success': False, 'pesan': 'Terjadi Kesalahan, Data tidak ditemukan.' }
			response = HttpResponse(json.dumps(data))
	else:
		data = {'success': False, 'pesan': 'Terjadi Kesalahan, Data tidak ditemukan.' }
		response = HttpResponse(json.dumps(data))
	return response