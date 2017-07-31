import json, os, datetime
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from izin.models import DetilIUA, Kendaraan, DetilHO, Syarat, DetilTrayek, PengajuanIzin
from izin.iua_forms import DataKendaraanForm
from master.models import Berkas
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from izin.tdp_forms import BerkasForm

def save_detil_iua(request):
	data = {'success':False, 'pesan': 'Terjadi Kesalahan, data tidak ditemukan', 'data': []}
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'kode_kelompok_jenis_izin' in request.COOKIES.keys() != '' and request.COOKIES['kode_kelompok_jenis_izin'] != '':
				try:
					if request.COOKIES['kode_kelompok_jenis_izin'] == 'TRAYEK':
						pengajuan_ = DetilTrayek.objects.get(id=request.COOKIES['id_pengajuan'])
					else:	
						pengajuan_ = DetilIUA.objects.get(id=request.COOKIES['id_pengajuan'])
					pengajuan_.nilai_investasi = request.POST.get('nilai_investasi')
					pengajuan_.kategori_kendaraan_id = request.POST.get('kategori_kendaraan')
					pengajuan_.save()
					data = {'success': True, 'pesan': 'Data Umum Perusahaan berhasil tersimpan.', 'data': []}
				except ObjectDoesNotExist:
					pass
	data = json.dumps(data)
	response = HttpResponse(data)
	return response

def save_data_kendaraan(request):
	data = {'success': False, 'pesan': 'Data Kendaraan gagal disimpan.'}
	data = json.dumps(data)
	response = HttpResponse(data)
	# print request.POST.get('id_kendaraan')
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			try:
				pengajuan_obj = DetilIUA.objects.get(id=request.COOKIES['id_pengajuan'])
				if pengajuan_obj:
					# kendaraan_obj = Kendaraan.objects.none()
					data_kendaraan_form = DataKendaraanForm(request.POST)
					if request.POST.get('id_kendaraan'):
						try:
							kendaraan_obj = Kendaraan.objects.get(id=request.POST.get('id_kendaraan'))
							data_kendaraan_form = DataKendaraanForm(request.POST, instance=kendaraan_obj)
						except ObjectDoesNotExist:
							pass
					
					if data_kendaraan_form.is_valid():
						i = data_kendaraan_form.save(commit=False)
						i.pengajuan_izin_id = pengajuan_obj.id
						i.save()
						data = {'success': True, 'pesan': 'Data Kendaraan berhasil disimpan.'}
						data = json.dumps(data)
						response = HttpResponse(data)
					else:
						data = data_kendaraan_form.errors.as_json()
						response = HttpResponse(data)
			except ObjectDoesNotExist:
				pass
	return response

def load_data_kendaraan(request, pengajuan_id):
	data = []
	if pengajuan_id:
		i = Kendaraan.objects.filter(pengajuan_izin_id=pengajuan_id)
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
	if 'kode_kelompok_jenis_izin' in request.COOKIES.keys() != '' and request.COOKIES['kode_kelompok_jenis_izin'] != '':
		if pengajuan_id:
			try:
				if request.COOKIES['kode_kelompok_jenis_izin'] == 'TRAYEK':
					i = DetilTrayek.objects.get(id=pengajuan_id)
				else:
					i = DetilIUA.objects.get(id=pengajuan_id)
				if i:
					data = i.as_json()
				print data
			except ObjectDoesNotExist:
				pass
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
			response = HttpResponse(data)
	else:
		data = {'success': False, 'pesan': 'Data tidak ditemukan'}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def load_izin_ho(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			data = {'success': False, 'pesan': 'Data tidak ditemukan'}
			nomor_izin_ho = request.POST.get('nomor_izin_ho')
			if nomor_izin_ho and nomor_izin_ho is not None:
				detil_ho = DetilHO.objects.filter(no_izin=nomor_izin_ho).last()
				if detil_ho and detil_ho is not None:
					if 'id_pengajuan' in request.COOKIES.keys():
						if request.COOKIES['id_pengajuan'] != '':
							pengajuan_obj = DetilIUA.objects.filter(id=request.COOKIES['id_pengajuan']).last()
							if pengajuan_obj and pengajuan_obj is not None:
								pengajuan_obj.detil_izin_ho_id = detil_ho.id
								pengajuan_obj.save()
								if pengajuan_obj.detil_izin_ho:
									if pengajuan_obj.detil_izin_ho.no_izin:
										nomor_izin = pengajuan_obj.detil_izin_ho.no_izin		
										data = {'success': True, 'pesan': 'Data berhasil disimpan.', 'data': nomor_izin}
			data = json.dumps(data)
			response = HttpResponse(data)
			return response
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Nomor Izin Gangguan tidak ditemukan'}]}
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
											berkas.nama_berkas = "Scan Akte Pendirian Perusahaan / Koperasi / Tanda Jati Diri Perorangan "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "File Scan Akte Pendirian Perusahaan / Koperasi / Tanda Jati Diri Perorangan "+p.perusahaan.npwp
										elif kode == 'Domisili':
											berkas.nama_berkas = "Scan Surat Keterangan Domisili "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "File Scan Surat Keterangan Domisili "+p.perusahaan.npwp
										elif kode == 'Pernyataan Kesanggupan Memilkik':
											berkas.nama_berkas = "Scan Surat Pernyataan Kesanggupan Untuk Memiliki / Menguasai Kendaraan Berat "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "File Scan Surat Pernyataan Kesanggupan Untuk Memiliki / Menguasai Kendaraan Berat "+p.perusahaan.npwp
										elif kode == 'Pernyataan Kesanggupan Menyediakan':
											berkas.nama_berkas = "Scan Surat Pernyataan Kesanggupan Menyediakan Kendaraan "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "File Scan Surat Pernyataan Kesanggupan Menyediakan Kendaraan "+p.perusahaan.npwp
										elif kode == 'Buku Uji Berkala':
											berkas.nama_berkas = "Buku Uji Berkala Kendaraan Bermotor "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "File Buku Uji Berkala Kendaraan Bermotor "+p.perusahaan.npwp
										if request.user.is_authenticated():
											berkas.created_by_id = request.user.id
										else:
											berkas.created_by_id = request.COOKIES['id_pemohon']
										berkas.save()
										p.berkas_tambahan.add(berkas)
										p.berkas_terkait_izin.add(berkas)

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
			# print iua.perusahaan.berkas_npwp
			if perusahaan_:
				npwp_perusahaan = perusahaan_.berkas_npwp
				if npwp_perusahaan:
					url_berkas.append(npwp_perusahaan.berkas.url)
					id_elemen.append('npwp_perusahaan')
					nm_berkas.append(npwp_perusahaan.nama_berkas)
					id_berkas.append(npwp_perusahaan.id)
					iua.berkas_terkait_izin.add(npwp_perusahaan)
					
			if berkas_:
				akte_pendirian = berkas_.filter(keterangan='File Scan Akte Pendirian Perusahaan / Koperasi / Tanda Jati Diri Perorangan '+perusahaan_.npwp).last()
				if akte_pendirian:
					url_berkas.append(akte_pendirian.berkas.url)
					id_elemen.append('akte_pendirian')
					nm_berkas.append(akte_pendirian.nama_berkas)
					id_berkas.append(akte_pendirian.id)
					iua.berkas_terkait_izin.add(akte_pendirian)

				domisili = berkas_.filter(keterangan='File Scan Surat Keterangan Domisili '+perusahaan_.npwp).last()
				if domisili:
					url_berkas.append(domisili.berkas.url)
					id_elemen.append('domisili')
					nm_berkas.append(domisili.nama_berkas)
					id_berkas.append(domisili.id)
					iua.berkas_terkait_izin.add(domisili)

				pernyataan_kesanggupan_memiliki = berkas_.filter(keterangan='File Scan Surat Pernyataan Kesanggupan Untuk Memiliki / Menguasai Kendaraan Berat '+perusahaan_.npwp).last()
				if pernyataan_kesanggupan_memiliki:
					url_berkas.append(pernyataan_kesanggupan_memiliki.berkas.url)
					id_elemen.append('pernyataan_kesanggupan_memiliki')
					nm_berkas.append(pernyataan_kesanggupan_memiliki.nama_berkas)
					id_berkas.append(pernyataan_kesanggupan_memiliki.id)
					iua.berkas_terkait_izin.add(pernyataan_kesanggupan_memiliki)

				pernyataan_kesanggupan_menyediakan = berkas_.filter(keterangan='File Scan Surat Pernyataan Kesanggupan Menyediakan Kendaraan '+perusahaan_.npwp).last()
				if pernyataan_kesanggupan_menyediakan:
					url_berkas.append(pernyataan_kesanggupan_menyediakan.berkas.url)
					id_elemen.append('pernyataan_kesanggupan_menyediakan')
					nm_berkas.append(pernyataan_kesanggupan_menyediakan.nama_berkas)
					id_berkas.append(pernyataan_kesanggupan_menyediakan.id)
					iua.berkas_terkait_izin.add(pernyataan_kesanggupan_menyediakan)

				buku_uji_berkala = berkas_.filter(keterangan='File Buku Uji Berkala Kendaraan Bermotor '+perusahaan_.npwp).last()
				if buku_uji_berkala:
					url_berkas.append(buku_uji_berkala.berkas.url)
					id_elemen.append('buku_uji_berkala')
					nm_berkas.append(buku_uji_berkala.nama_berkas)
					id_berkas.append(buku_uji_berkala.id)
					iua.berkas_terkait_izin.add(buku_uji_berkala)

			data = {'success': True, 'pesan': 'Perusahaan Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas}
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': ''}
	response = HttpResponse(json.dumps(data))
	return response

def ajax_delete_berkas_iua(request, id_berkas, kode):
	data = {'success': False, 'pesan': 'Berkas Tidak Ada' }
	if id_berkas:
		try:
			pengajuan_obj = DetilIUA.objects.get(id=request.COOKIES.get('id_pengajuan'))
			if kode == "npwp_perusahaan":
				if pengajuan_obj.perusahaan:
					perusahaan = pengajuan_obj.perusahaan
					perusahaan.berkas_npwp = None
					perusahaan.save()
					# print "Delete"
				pengajuan_obj.berkas_npwp_perusahaan = None
				pengajuan_obj.save()
			try:
				b = Berkas.objects.get(id=id_berkas)
				data = {'success': True, 'pesan': str(b)+"berhasil dihapus"}
				b.delete()
				# berkas_terkait = pengajuan_obj.berkas_terkait_izin.filter(id=b.id)
				# if berkas_terkait.exists():
				# 	berkas_terkait = berkas_terkait.last()
				# 	berkas_terkait
				
			except ObjectDoesNotExist:
				pass
		except ObjectDoesNotExist:
			pass
	return HttpResponse(json.dumps(data))

def load_data_konfirmasi(request, pengajuan_id):
	pemohon_json = {}
	data = {'success': False, 'pesan': 'Data tidak ditemukan'}
	if pengajuan_id and pengajuan_id is not None:
		if 'kode_kelompok_jenis_izin' in request.COOKIES.keys():
			if request.COOKIES['kode_kelompok_jenis_izin'] != '':
				try:
					if request.COOKIES['kode_kelompok_jenis_izin'] == "TRAYEK":
						pengajuan_obj = DetilTrayek.objects.get(id=pengajuan_id)
					else:
						pengajuan_obj = DetilIUA.objects.get(id=pengajuan_id)
					jenis_pengajuan = pengajuan_obj.jenis_permohonan.jenis_permohonan_izin
					nilai_investasi = pengajuan_obj.nilai_investasi
					detil_ho = ""
					if pengajuan_obj.detil_ho:
						detil_ho = pengajuan_obj.detil_izin_ho.no_izin
					kategori_kendaraan = pengajuan_obj.kategori_kendaraan.nama_kategori
					pemohon_obj = pengajuan_obj.pemohon
					perusahaan_obj = pengajuan_obj.perusahaan
					kendaraan_obj = Kendaraan.objects.filter(pengajuan_izin_id=pengajuan_obj.id)
					# print kendaraan_obj
					jumlah_kendaraan_obj = kendaraan_obj.count()

					if pengajuan_obj:
						# pengajuan_json = pengajuan_.as_json()
						pemohon_json = pemohon_obj.as_json()
						perusahaan_json = perusahaan_obj.as_json()
						kendaraan_json = [k.as_json() for k in kendaraan_obj]
					data = {'success': True, 'pesan': 'Data Berhasil','jenis_pengajuan': jenis_pengajuan, 'nilai_investasi': nilai_investasi,'detil_izin_ho': detil_ho, 'kategori_kendaraan': kategori_kendaraan, 'pemohon_json': pemohon_json, 'perusahaan_json': perusahaan_json,'kendaraan': kendaraan_json, 'jumlah_kendaraan': jumlah_kendaraan_obj}
				except ObjectDoesNotExist:
					pass

	response = HttpResponse(json.dumps(data))
	return response

def cetak_iua(request, id_pengajuan):
	extra_context = {}
	if id_pengajuan:
		pengajuan_obj = get_object_or_404(DetilIUA, id=id_pengajuan)
		if pengajuan_obj:
			extra_context.update({'pengajuan':pengajuan_obj})
	return render(request, "front-end/include/formulir_iua/cetak.html", extra_context)

def cetak_bukti_pendaftaran_iua(request, id_pengajuan):
	extra_context = {}
	extra_context.update({'formulir_judul': 'FORMULIR PENDAFTARAN IZIN USAHA ANGKUTAN'})
	if id_pengajuan:
		pengajuan_ = get_object_or_404(DetilIUA, id=id_pengajuan)
		if pengajuan_:
			nilai_investasi = pengajuan_.nilai_investasi
			kategori_kendaraan = pengajuan_.kategori_kendaraan.nama_kategori
			kendaraan_ = pengajuan_.kendaraan_set.all()
			kendaraan_jumlah = kendaraan_.count()
			# rincian_perusahaan_ = RincianPerusahaan.objects.filter(detil_tdp_id=pengajuan_.id).last()
			# id_kelompok_list = KelompokJenisIzin.objects.filter(jenis_izin__kode=25)
			syarat_ = Syarat.objects.filter(jenis_izin__kode="IUA")
			extra_context.update({ 'nilai_investasi': nilai_investasi, 'kategori_kendaraan': kategori_kendaraan, 'kendaraan_jumlah': kendaraan_jumlah, 'kendaraan': kendaraan_,  'pengajuan_':pengajuan_, 'syarat': syarat_})
	return render(request, "front-end/include/formulir_iua/cetak_bukti_pendaftaran.html", extra_context)

def iua_done(request):
	data = {'success': False, 'pesan': 'Terjadi Kesalahan. Data pengajuan tidak terdaftar.'}
	response = HttpResponse(json.dumps(data))
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			try:
				pengajuan_ = DetilIUA.objects.get(id=request.COOKIES['id_pengajuan'])
				if pengajuan_:
					pengajuan_.status = 6
					pengajuan_.save()
							
					data = {'success': True, 'pesan': 'Proses Selesai.' }
					response = HttpResponse(json.dumps(data))
					response.delete_cookie(key='id_jenis_pengajuan') # set cookie	
					response.delete_cookie(key='id_kelompok_izin') # set cookie	
					response.delete_cookie(key='id_pengajuan') # set cookie	
					response.delete_cookie(key='id_perusahaan') # set cookie	
					response.delete_cookie(key='id_perusahaan_induk') # set cookie	
					response.delete_cookie(key='nomor_ktp') # set cookie	
					response.delete_cookie(key='nomor_paspor') # set cookie	
					response.delete_cookie(key='id_pemohon') # set cookie	
					response.delete_cookie(key='id_kelompok_izin') # set cookie
					response.delete_cookie(key='id_legalitas') # set cookie
					response.delete_cookie(key='id_legalitas_perubahan') # set cookie
					response.delete_cookie(key='npwp_perusahaan') # set cookie
					response.delete_cookie(key='npwp_perusahaan_induk') # set cookie
					response.delete_cookie(key='kode_kelompok_jenis_izin') # set cookie
			except ObjectDoesNotExist:
				pass
	return response