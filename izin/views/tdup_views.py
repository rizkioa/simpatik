import os, json, datetime
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from izin.models import DetilTDUP, RincianSubJenis
from izin.izin_forms import RincianSubJenisForm, KeteranganUsahaTDUPForm
from izin.tdp_forms import BerkasForm

def tdup_data_usaha_pariwisata_save(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				# print "masuk save"
				try:
					pengajuan = DetilTDUP.objects.get(id=request.COOKIES['id_pengajuan'])
					bidang_usaha_list = request.POST.getlist('bidang_usaha_pariwisata')
					sub_jenis_bidang_usaha_list = request.POST.getlist('sub_jenis_bidang_usaha')
					# save many to many bidang usaha pariwisata
					# for bidang_usaha in bidang_usaha_list:
					# 	bidang_usaha_obj = BidangUsahaPariwisata.objects.get(id=bidang_usaha)
					# 	pengajuan.bidang_usaha_pariwisata.add(bidang_usaha_obj)
					# for sub_jenis_bidang_usaha in sub_jenis_bidang_usaha_list:
					# 	sub_jenis_bidang_usaha_obj = SubJenisBidangUsaha.objects.get(id=sub_jenis_bidang_usaha)
					# 	pengajuan.sub_jenis_bidang_usaha.add(sub_jenis_bidang_usaha_obj)
					# if pengajuan.rincian_sub_jenis:
					rincian = 0
					if pengajuan.rincian_sub_jenis:
						rincian = pengajuan.rincian_sub_jenis.id
					try:
						rincian_sub_jenis_list = RincianSubJenis.objects.get(id=rincian)
						rincian_sub_jenis_form = RincianSubJenisForm(request.POST, instance=rincian_sub_jenis_list)
					except ObjectDoesNotExist:
						rincian_sub_jenis_form = RincianSubJenisForm(request.POST)
					if rincian_sub_jenis_form.is_valid():
						# print "masukss"
						r = rincian_sub_jenis_form.save(commit=False)
						r.save()
						# print r
						pengajuan.rincian_sub_jenis = r
					pengajuan.save()

					data = {'success': True, 'pesan': 'Data Usaha Pariwisata berhasil tersimpan.', 'data': []}
					data = json.dumps(data)
					response = HttpResponse(data)
				except ObjectDoesNotExist:
					data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = {'Terjadi Kesalahan': [{'message': 'Data Kelompok Jenis Izin tidak ditemukan/data kosong'}]}
				data = json.dumps(data)
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response


def ajax_data_usaha_pariwista(request, id_pengajuan):
	if id_pengajuan:
		try:
			pengajuan = DetilTDUP.objects.get(id=id_pengajuan)
			# bidang_usaha_list = pengajuan.bidang_usaha_pariwisata.all()
			bidang_usaha_json = []
			# if bidang_usaha_list:
				# bidang_usaha_json = [k.as_json() for k in BidangUsahaPariwisata.objects.filter(id__in=bidang_usaha_list)]
			# sub_jenis_list = pengajuan.sub_jenis_bidang_usaha.all()
			sub_jenis_json = []
			# if sub_jenis_list:
				# sub_jenis_json = [k.as_json() for k in SubJenisBidangUsaha.objects.filter(id__in=sub_jenis_list)]

			jumlah_unit_angkutan_jalan_wisata = ""
			kapasitas_angkutan_jalan_wisata = ""
			jumlah_unit_angkutan_kereta_api_wisata = ""
			kapasitas_angkutan_kereta_api_wisata = ""
			jumlah_unit_angkutan_sungai_dan_danau_wisata = ""
			kapasitas_angkutan_sungai_dan_danau_wisata = ""
			jumlah_unit_angkutan_laut_domestik_wisata = ""
			kapasitas_angkutan_laut_domestik_wisata = ""
			jumlah_unit_angkutan_laut_internasional_wisata = ""
			kapasitas_angkutan_laut_internasional_wisata = ""
			# makanan dan minuman
			jumlah_kursi_restoran = ""
			jumlah_kursi_rumah_makan = ""
			jumlah_kursi_bar_atau_rumah_minum = ""
			jumlah_kursi_kafe = ""
			jumlah_stand_pusat_makanan = ""
			kapasitas_produksi_jasa_boga = ""
			r = pengajuan.rincian_sub_jenis
			if r:
				# transportasi wisata
				jumlah_unit_angkutan_jalan_wisata = r.jumlah_unit_angkutan_jalan_wisata
				# print jumlah_unit_angkutan_jalan_wisata
				kapasitas_angkutan_jalan_wisata = r.kapasitas_angkutan_jalan_wisata
				jumlah_unit_angkutan_kereta_api_wisata = r.jumlah_unit_angkutan_kereta_api_wisata
				kapasitas_angkutan_kereta_api_wisata = r.kapasitas_angkutan_kereta_api_wisata
				jumlah_unit_angkutan_sungai_dan_danau_wisata = r.jumlah_unit_angkutan_sungai_dan_danau_wisata
				kapasitas_angkutan_sungai_dan_danau_wisata = r.kapasitas_angkutan_sungai_dan_danau_wisata
				jumlah_unit_angkutan_laut_domestik_wisata = r.jumlah_unit_angkutan_laut_domestik_wisata
				kapasitas_angkutan_laut_domestik_wisata = r.kapasitas_angkutan_laut_domestik_wisata
				jumlah_unit_angkutan_laut_internasional_wisata = r.jumlah_unit_angkutan_laut_internasional_wisata
				kapasitas_angkutan_laut_internasional_wisata = r.kapasitas_angkutan_laut_internasional_wisata
				# makanan dan minuman
				jumlah_kursi_restoran = r.jumlah_kursi_restoran
				jumlah_kursi_rumah_makan = r.jumlah_kursi_rumah_makan
				jumlah_kursi_bar_atau_rumah_minum = r.jumlah_kursi_bar_atau_rumah_minum
				jumlah_kursi_kafe = r.jumlah_kursi_kafe
				jumlah_stand_pusat_makanan = r.jumlah_stand_pusat_makanan
				kapasitas_produksi_jasa_boga = r.kapasitas_produksi_jasa_boga

			data = {'success': True, 'pesan': 'Load data kegiatan perusahaan', 'data':{ 'bidang_usaha_json':bidang_usaha_json, 'sub_jenis_json': sub_jenis_json, 'jumlah_unit_angkutan_jalan_wisata': jumlah_unit_angkutan_jalan_wisata, 'kapasitas_angkutan_jalan_wisata': kapasitas_angkutan_jalan_wisata, 'jumlah_unit_angkutan_kereta_api_wisata':jumlah_unit_angkutan_kereta_api_wisata, 'kapasitas_angkutan_kereta_api_wisata':kapasitas_angkutan_kereta_api_wisata, 'jumlah_unit_angkutan_sungai_dan_danau_wisata':jumlah_unit_angkutan_sungai_dan_danau_wisata, 'kapasitas_angkutan_sungai_dan_danau_wisata':kapasitas_angkutan_sungai_dan_danau_wisata, 'jumlah_unit_angkutan_laut_domestik_wisata':jumlah_unit_angkutan_laut_domestik_wisata, 'kapasitas_angkutan_laut_domestik_wisata':kapasitas_angkutan_laut_domestik_wisata, 'jumlah_unit_angkutan_laut_internasional_wisata':jumlah_unit_angkutan_laut_internasional_wisata, 'kapasitas_angkutan_laut_internasional_wisata':kapasitas_angkutan_laut_internasional_wisata, 'jumlah_kursi_restoran':jumlah_kursi_restoran, 'jumlah_kursi_rumah_makan':jumlah_kursi_rumah_makan, 'jumlah_kursi_bar_atau_rumah_minum':jumlah_kursi_bar_atau_rumah_minum, 'jumlah_kursi_kafe':jumlah_kursi_kafe, 'jumlah_stand_pusat_makanan':jumlah_stand_pusat_makanan, 'kapasitas_produksi_jasa_boga':kapasitas_produksi_jasa_boga}}
			data = json.dumps(data)
			response = HttpResponse(data)

		except ObjectDoesNotExist:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def tdup_keterangan_usaha_save(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				# print "masuk save"
				try:
					pengajuan = DetilTDUP.objects.get(id=request.COOKIES['id_pengajuan'])
					keteranganform = KeteranganUsahaTDUPForm(request.POST, instance=pengajuan)
					if keteranganform.is_valid():
						r = keteranganform.save(commit=False)
						r.save()
						data = {'success': True, 'pesan': 'Data Usaha Pariwisata berhasil tersimpan.', 'data': []}
						data = json.dumps(data)
						response = HttpResponse(data)
					else:
						data = keteranganform.errors.as_json()
						response = HttpResponse(data)
				except ObjectDoesNotExist:
					data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = {'Terjadi Kesalahan': [{'message': 'Data Kelompok Jenis Izin tidak ditemukan/data kosong'}]}
				data = json.dumps(data)
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def tdup_keterangan_usaha_ajax(request, id_pengajuan):
	if id_pengajuan:
		try:
			pengajuan = DetilTDUP.objects.get(id=id_pengajuan)
			nama_usaha = ''
			lokasi_usaha_pariwisata = ''
			provinsi = ''
			kabupaten = ''
			kecamatan = ''
			desa = ''
			telephone = ''
			nomor_izin_gangguan = ''
			tanggal_izin_gangguan = ''
			nomor_dokumen_pengelolaan = ''
			tanggal_dokumen_pengelolaan = ''
			if pengajuan:
				nama_usaha = pengajuan.nama_usaha
				lokasi_usaha_pariwisata = pengajuan.lokasi_usaha_pariwisata
				provinsi = pengajuan.desa_lokasi.kecamatan.kabupaten.provinsi.id
				kabupaten = pengajuan.desa_lokasi.kecamatan.kabupaten.id
				kecamatan = pengajuan.desa_lokasi.kecamatan.id
				desa = pengajuan.desa_lokasi.id
				telephone = pengajuan.telephone
				nomor_izin_gangguan = pengajuan.nomor_izin_gangguan
				tanggal_izin_gangguan = pengajuan.tanggal_izin_gangguan.strftime('%d-%m-%Y')
				nomor_dokumen_pengelolaan = pengajuan.nomor_dokumen_pengelolaan
				tanggal_dokumen_pengelolaan = pengajuan.tanggal_dokumen_pengelolaan.strftime('%d-%m-%Y')
				data = {'success': True, 'pesan': 'Load data keterangan usaha', 'data':{ 'nama_usaha':nama_usaha, 'lokasi_usaha_pariwisata': lokasi_usaha_pariwisata, 'provinsi':provinsi, 'kabupaten':kabupaten, 'kecamatan':kecamatan, 'desa':desa, 'telephone':telephone, 'nomor_izin_gangguan':nomor_izin_gangguan, 'tanggal_izin_gangguan':tanggal_izin_gangguan, 'nomor_dokumen_pengelolaan':nomor_dokumen_pengelolaan, 'tanggal_dokumen_pengelolaan':tanggal_dokumen_pengelolaan}}
				data = json.dumps(data)
				response = HttpResponse(data)
		except ObjectDoesNotExist:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def tdp_upload_surat_keputusan(request):
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
									p = DetilTDUP.objects.get(id=request.COOKIES['id_pengajuan'])
									try:
										# perusahaan_ = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
										berkas = form.save(commit=False)
										kode = request.POST.get('kode')
										if kode == 'Surat Permohonan':
											berkas.nama_berkas = "Surat Permohonan "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "Surat Permohonan "+p.perusahaan.npwp
										elif kode == 'Permohonan Perubahan':
											berkas.nama_berkas = "Izin Tempat Usaha Pariwisata yang masih berlaku berlaku "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "Izin Tempat Usaha Pariwisata yang masih berlaku berlaku "+p.perusahaan.npwp
										elif kode == 'Sertifikat Lahan':
											berkas.nama_berkas = "Sertifikat Lahan "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "Sertifikat Lahan "+p.perusahaan.npwp
										elif kode == 'Izin Gangguan':
											berkas.nama_berkas = "Izin Gangguan "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "Izin Gangguan "+p.perusahaan.npwp
										elif kode == 'IMB':
											berkas.nama_berkas = "IMB "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "IMB "+p.perusahaan.npwp
										elif kode == 'Nomor Pokok Wajib Pajak':
											berkas.nama_berkas = "Nomor Pokok Wajib Pajak "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "Nomor Pokok Wajib Pajak "+p.perusahaan.npwp
										elif kode == 'SIUP':
											berkas.nama_berkas = "SIUP "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "SIUP "+p.perusahaan.npwp
										elif kode == 'Surat Pernyataan':
											berkas.nama_berkas = "Surat pernyataan tertulis dari pengusaha yang menjamin bahwa data dan dokumen yang diserahakan benar dan sah "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "Surat pernyataan tertulis dari pengusaha yang menjamin bahwa data dan dokumen yang diserahakan benar dan sah "+p.perusahaan.npwp
										elif kode == 'Dokumen Lingkungan':
											berkas.nama_berkas = "Dokumen lingkungan "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "Dokumen lingkungan "+p.perusahaan.npwp
										elif kode == 'Izin Usaha Angkutan':
											berkas.nama_berkas = "Izin Usaha Angkutan "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "Izin Usaha Angkutan "+p.perusahaan.npwp
										elif kode == 'Berkas Tambahan':
											berkas.nama_berkas = "Berkas Tambahan "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "Berkas Tambahan "+p.perusahaan.npwp
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

def tdup_done(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilTDUP.objects.get(id=request.COOKIES['id_pengajuan'])
			pengajuan_.status = 6
			pengajuan_.save()
					
			data = {'success': True, 'pesan': 'Proses Selesai.' }
			response = HttpResponse(json.dumps(data))
			response.delete_cookie(key='id_jenis_pengajuan') # set cookie	
			response.delete_cookie(key='id_kelompok_izin') # set cookie	
			response.delete_cookie(key='id_pengajuan') # set cookie	
			response.delete_cookie(key='id_perusahaan') # set cookie
			response.delete_cookie(key='nomor_ktp') # set cookie	
			response.delete_cookie(key='nomor_paspor') # set cookie	
			response.delete_cookie(key='id_pemohon') # set cookie	
			response.delete_cookie(key='id_kelompok_izin') # set cookie
			response.delete_cookie(key='id_legalitas') # set cookie
			response.delete_cookie(key='id_legalitas_perubahan') # set cookie
			response.delete_cookie(key='npwp_perusahaan') # set cookie
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response