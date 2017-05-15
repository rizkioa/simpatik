import json, os, datetime
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from izin.models import DetilIUA, Kendaraan
from izin.iua_forms import DataKendaraanForm
from izin.tdp_forms import BerkasForm

def save_detil_iua(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				try:
					pengajuan_ = DetilIUA.objects.get(id=request.COOKIES['id_pengajuan'])
					pengajuan_.nilai_investasi = request.POST.get('nilai_investasi')
					pengajuan_.kategori_kendaraan_id = request.POST.get('kategori_kendaraan')
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

def save_data_kendaraan(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			try:
				pengajuan_ = DetilIUA.objects.get(id=request.COOKIES['id_pengajuan'])
				data_kendaraan_form = DataKendaraanForm(request.POST)
				if data_kendaraan_form.is_valid():
					i = data_kendaraan_form.save(commit=False)
					i.iua_id = pengajuan_.id
					i.save()
					data = {'success': True, 'pesan': 'Data Kendaraan berhasil disimpan.'}
					data = json.dumps(data)
					response = HttpResponse(data)
				else:
					data = data_kendaraan_form.errors.as_json()
					response = HttpResponse(data)
			except ObjectDoesNotExist:
				data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada.'}]}
				data = json.dumps(data)
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def load_data_kendaraan(request, pengajuan_id):
	data = []
	if pengajuan_id:
		i = Kendaraan.objects.filter(iua_id=pengajuan_id)
		data = [ob.as_json() for ob in i]
		response = HttpResponse(json.dumps(data), content_type="application/json")
		return response

def jumlah_data_kendaraan(request, pengajuan_id):
	if pengajuan_id:
		kendaraan = len(Kendaraan.objects.filter(iua_id=pengajuan_id))
		data = {'data':{'kendaraan':kendaraan}}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def load_detil_iua(request, pengajuan_id):
	data = []
	if pengajuan_id:
		i = DetilIUA.objects.filter(id=pengajuan_id).last()
		if i:
			data = i.as_json()
			response = HttpResponse(json.dumps(data), content_type="application/json")
			return response

def delete_data_kendaraan(request, kendaraan_id):
	if kendaraan_id:
		try:
			i = Kendaraan.objects.get(id=kendaraan_id)
			i.delete()
			data = {'success': True, 'pesan': 'Data berhasil dihapus.'}
			data = json.dumps(data)
			response = HttpResponse(data)
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
			data = json.dumps(data)
			response = HttpResponse
	else:
		data = {'success': False, 'pesan': 'Data tidak ditemukan'}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def iua_upload_dokument(request):
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
									p = DetilIUA.objects.get(id=request.COOKIES['id_pengajuan'])
									try:
										# perusahaan_ = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
										berkas = form.save(commit=False)
										kode = request.POST.get('kode')
										if kode == 'Akte Pendirian':
											berkas.nama_berkas = "Scan Akte Pendirian Perusahaan / Koperasi / Tanda Jati Diri Perorangan"+p.perusahaan.nama_perusahaan
											berkas.keterangan = "File Scan Akte Pendirian Perusahaan / Koperasi / Tanda Jati Diri Perorangan"+p.perusahaan.npwp
										elif kode == 'Domisili':
											berkas.nama_berkas = "Scan Surat Keterangan Domisili"+p.perusahaan.nama_perusahaan
											berkas.keterangan = "File Scan Surat Keterangan Domisili"+p.perusahaan.npwp
										elif kode == 'Pernyataan Kesanggupan Memilkik':
											berkas.nama_berkas = "Scan Surat Pernyataan Kesanggupan Untuk Memiliki / Menguasai Kendaraan Berat"+p.perusahaan.nama_perusahaan
											berkas.keterangan = "File Scan Surat Pernyataan Kesanggupan Untuk Memiliki / Menguasai Kendaraan Berat"+p.perusahaan.npwp
										elif kode == 'Pernyataan Kesanggupan Menyediakan':
											berkas.nama_berkas = "Scan Surat Pernyataan Kesanggupan Menyediakan Kendaraan"+p.perusahaan.nama_perusahaan
											berkas.keterangan = "File Scan Surat Pernyataan Kesanggupan Menyediakan Kendaraan"+p.perusahaan.npwp
										elif kode == 'Buku Uji Berkala':
											berkas.nama_berkas = "Buku Uji Berkala Kendaraan Bermotor"+p.perusahaan.nama_perusahaan
											berkas.keterangan = "File Buku Uji Berkala Kendaraan Bermotor"+p.perusahaan.npwp
										if request.user.is_authenticated():
											berkas.created_by_id = request.user.id
										else:
											berkas.created_by_id = request.COOKIES['id_pemohon']
										berkas.save()
										p.berkas_tambahan.add(berkas)

										data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
												{'status_upload': 'ok'},
											]}
										data = json.dumps(data)
										response = HttpResponse(data)
									except ObjectDoesNotExist:
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

def ajax_load_berkas_iua(request, id_pengajuan):
	url_berkas = []
	id_elemen = []
	nm_berkas = []
	id_berkas = []
	if id_pengajuan:
		try:
			iua = DetilIUA.objects.get(id=id_pengajuan)
			perusahaan_ = iua.perusahaan
			berkas_ = iua.berkas_tambahan.all()
			pemohon_ = iua.pemohon

			if pemohon_:
				npwp = pemohon_.berkas_npwp
				if npwp:
					url_berkas.apped(npwp.berkas.url)
					id_elemen.apped('npwp')
					nm_berkas.apped(npwp.nama_berkas)
					id_berkas.apped(npwp.id)
			if berkas_:
				akte_pendirian = berkas_.filter(keterangan='Akte Pendirian '+perusahaan_.npwp).last()
				if akte_pendirian:
					url_berkas.append(akte_pendirian.berkas.url)
					id_elemen.append('akte_pendirian')
					nm_berkas.append(akte_pendirian.nama_berkas)
					id_berkas.append(akte_pendirian.id)

				domisili = berkas_.filter(keterangan='Domisili '+perusahaan_.npwp).last()
				if domisili:
					url_berkas.append(domisili.berkas.url)
					id_elemen.append('domisili')
					nm_berkas.append(domisili.nama_berkas)
					id_berkas.append(domisili.id)

				pernyataan_kesanggupan_memiliki = berkas_.filter(keterangan='Pernyataan Kesanggupan Memilkik '+perusahaan_.npwp).last()
				if pernyataan_kesanggupan_memiliki:
					url_berkas.append(pernyataan_kesanggupan_memiliki.berkas.url)
					id_elemen.append('pernyataan_kesanggupan_memiliki')
					nm_berkas.append(pernyataan_kesanggupan_memiliki.nama_berkas)
					id_berkas.append(pernyataan_kesanggupan_memiliki.id)

				pernyataan_kesanggupan_menyediakan = berkas_.filter(keterangan='Pernyataan Kesanggupan Menyediakan '+perusahaan_.npwp).last()
				if pernyataan_kesanggupan_menyediakan:
					url_berkas.append(pernyataan_kesanggupan_menyediakan.berkas.url)
					id_elemen.append('pernyataan_kesanggupan_menyediakan')
					nm_berkas.append(pernyataan_kesanggupan_menyediakan.nama_berkas)
					id_berkas.append(pernyataan_kesanggupan_menyediakan.id)

				buku_uji_berkala = berkas_.filter(keterangan='Buku Uji Berkala '+perusahaan_.npwp).last()
				if buku_uji_berkala:
					url_berkas.append(buku_uji_berkala.berkas.url)
					id_elemen.append('buku_uji_berkala')
					nm_berkas.append(buku_uji_berkala.nama_berkas)
					id_berkas.append(buku_uji_berkala.id)

			data = {'success': True, 'pesan': 'Perusahaan Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas}
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': ''}
	response = HttpResponse(json.dumps(data))
	return response