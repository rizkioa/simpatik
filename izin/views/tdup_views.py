import os, json, datetime
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from izin.models import DetilTDUP, RincianSubJenis, IzinLainTDUP
from izin.izin_forms import RincianSubJenisForm, KeteranganUsahaTDUPForm
from izin.tdp_forms import BerkasForm
from master.models import Berkas
from accounts.models import NomorIdentitasPengguna

def tdup_data_usaha_pariwisata_save(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				# print "masuk save"
				try:
					pengajuan = DetilTDUP.objects.get(id=request.COOKIES['id_pengajuan'])
					bidang_usaha_pariwisata = request.POST.get('bidang_usaha_pariwisata', None)
					jenis_usaha_pariwisata = request.POST.get('jenis_usaha_pariwisata', None)
					sub_jenis_usaha_pariwisata = request.POST.get('sub_jenis_usaha_pariwisata', None)
					print '++++++++++'
					print bidang_usaha_pariwisata
					print '++++++++++'
					pengajuan.bidang_usaha_pariwisata_id = bidang_usaha_pariwisata
					pengajuan.jenis_usaha_pariwisata_id = jenis_usaha_pariwisata
					pengajuan.sub_jenis_usaha_pariwisata_id = sub_jenis_usaha_pariwisata
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

			bidang_usaha_pariwisata = ""
			if pengajuan.bidang_usaha_pariwisata:
				bidang_usaha_pariwisata = pengajuan.bidang_usaha_pariwisata.id
			jenis_usaha_pariwisata = ""
			if pengajuan.jenis_usaha_pariwisata:
				jenis_usaha_pariwisata = pengajuan.jenis_usaha_pariwisata.id
			sub_jenis_usaha_pariwisata = ""
			if pengajuan.sub_jenis_usaha_pariwisata:
				sub_jenis_usaha_pariwisata = pengajuan.sub_jenis_usaha_pariwisata.id
			jumlah_unit_angkutan_jalan_wisata = ""
			kapasitas_angkutan_jalan_wisata = ""
			jumlah_unit_angkutan_kereta_api_wisata = ""
			kapasitas_angkutan_kereta_api_wisata = ""
			jumlah_unit_angkutan_sungai_dan_danau_wisata = ""
			kapasitas_angkutan_sungai_dan_danau_wisata = ""
			# jumlah_unit_angkutan_laut_domestik_wisata = ""
			# kapasitas_angkutan_laut_domestik_wisata = ""
			# jumlah_unit_angkutan_laut_internasional_wisata = ""
			# kapasitas_angkutan_laut_internasional_wisata = ""
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
				# jumlah_unit_angkutan_laut_domestik_wisata = r.jumlah_unit_angkutan_laut_domestik_wisata
				# kapasitas_angkutan_laut_domestik_wisata = r.kapasitas_angkutan_laut_domestik_wisata
				# jumlah_unit_angkutan_laut_internasional_wisata = r.jumlah_unit_angkutan_laut_internasional_wisata
				# kapasitas_angkutan_laut_internasional_wisata = r.kapasitas_angkutan_laut_internasional_wisata
				# makanan dan minuman
				jumlah_kursi_restoran = r.jumlah_kursi_restoran
				jumlah_kursi_rumah_makan = r.jumlah_kursi_rumah_makan
				jumlah_kursi_bar_atau_rumah_minum = r.jumlah_kursi_bar_atau_rumah_minum
				jumlah_kursi_kafe = r.jumlah_kursi_kafe
				jumlah_stand_pusat_makanan = r.jumlah_stand_pusat_makanan
				kapasitas_produksi_jasa_boga = r.kapasitas_produksi_jasa_boga

			data = {'success': True, 'pesan': 'Load data kegiatan perusahaan', 'data':{ 'bidang_usaha_pariwisata':bidang_usaha_pariwisata, 'jenis_usaha_pariwisata': jenis_usaha_pariwisata, 'sub_jenis_usaha_pariwisata': sub_jenis_usaha_pariwisata, 'jumlah_unit_angkutan_jalan_wisata': jumlah_unit_angkutan_jalan_wisata, 'kapasitas_angkutan_jalan_wisata': kapasitas_angkutan_jalan_wisata, 'jumlah_unit_angkutan_kereta_api_wisata':jumlah_unit_angkutan_kereta_api_wisata, 'kapasitas_angkutan_kereta_api_wisata':kapasitas_angkutan_kereta_api_wisata, 'jumlah_unit_angkutan_sungai_dan_danau_wisata':jumlah_unit_angkutan_sungai_dan_danau_wisata, 'kapasitas_angkutan_sungai_dan_danau_wisata':kapasitas_angkutan_sungai_dan_danau_wisata,'jumlah_kursi_restoran':jumlah_kursi_restoran, 'jumlah_kursi_rumah_makan':jumlah_kursi_rumah_makan, 'jumlah_kursi_bar_atau_rumah_minum':jumlah_kursi_bar_atau_rumah_minum, 'jumlah_kursi_kafe':jumlah_kursi_kafe, 'jumlah_stand_pusat_makanan':jumlah_stand_pusat_makanan, 'kapasitas_produksi_jasa_boga':kapasitas_produksi_jasa_boga}}
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
			# nomor_izin_gangguan = ''
			# tanggal_izin_gangguan = ''
			nomor_dokumen_pengelolaan = ''
			tanggal_dokumen_pengelolaan = ''
			lokasi_lengkap = ''
			if pengajuan:
				nama_usaha = pengajuan.nama_usaha
				lokasi_usaha_pariwisata = pengajuan.lokasi_usaha_pariwisata
				telephone = pengajuan.telephone
				# if pengajuan.nomor_izin_gangguan:
				# 	nomor_izin_gangguan = pengajuan.nomor_izin_gangguan
				# tanggal_izin_gangguan = pengajuan.tanggal_izin_gangguan.strftime('%d-%m-%Y')
				if pengajuan.nomor_dokumen_pengelolaan:
					nomor_dokumen_pengelolaan = pengajuan.nomor_dokumen_pengelolaan
				if pengajuan.tanggal_dokumen_pengelolaan:
					tanggal_dokumen_pengelolaan = pengajuan.tanggal_dokumen_pengelolaan.strftime('%d-%m-%Y')
				# nomor_dokumen_pengelolaan = pengajuan.nomor_dokumen_pengelolaan
				# tanggal_dokumen_pengelolaan = pengajuan.tanggal_dokumen_pengelolaan.strftime('%d-%m-%Y')
				if pengajuan.desa_lokasi:
					lokasi_lengkap = pengajuan.desa_lokasi.as_json()
				data = {'success': True, 'pesan': 'Load data keterangan usaha', 'data':{ 'nama_usaha':nama_usaha, 'lokasi_usaha_pariwisata': lokasi_usaha_pariwisata, 'telephone':telephone, 'nomor_dokumen_pengelolaan':nomor_dokumen_pengelolaan, 'tanggal_dokumen_pengelolaan':tanggal_dokumen_pengelolaan, 'lokasi_lengkap': lokasi_lengkap}}
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': 'Data Pengajuan tidak ditemukan/data kosong' }
	else:
		data = {'success': False, 'pesan': 'Data Pengajuan tidak ditemukan/data kosong' }
	data = json.dumps(data)
	response = HttpResponse(data)
	return response

def tdup_upload_berkas(request):
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
									berkas = form.save(commit=False)
									kode = request.POST.get('kode')
									print '++++++++'
									print kode
									print '++++++++'
									if kode == 'Surat Permohonan':
										berkas.nama_berkas = "Surat Permohonan "+p.perusahaan.nama_perusahaan
										berkas.keterangan = "Surat Permohonan "+p.perusahaan.npwp
									elif kode == 'Izin Tempat Usaha':
										berkas.nama_berkas = "Izin Tempat Usaha Pariwisata yang masih berlaku berlaku "+p.perusahaan.nama_perusahaan
										berkas.keterangan = "Izin Tempat Usaha Pariwisata yang masih berlaku berlaku "+p.perusahaan.npwp
									elif kode == 'Sertifikat Lahan':
										berkas.nama_berkas = "Sertifikat Lahan / Surat Sewa "+p.perusahaan.nama_perusahaan
										berkas.keterangan = "Sertifikat Lahan / Surat Sewa "+p.perusahaan.npwp
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
										berkas.nama_berkas = "Izin Usaha Angkutan Khusus untuk bidang jasa transportasi wisata "+p.perusahaan.nama_perusahaan
										berkas.keterangan = "Izin Usaha Angkutan Khusus untuk bidang jasa transportasi wisata "+p.perusahaan.npwp
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

def ajax_load_berkas_tdup(request, id_pengajuan):
	url_berkas = []
	id_elemen = []
	nm_berkas =[]
	id_berkas =[]
	if id_pengajuan:
		try:
			tdup = DetilTDUP.objects.get(id=id_pengajuan)
			perusahaan_ = tdup.perusahaan
			berkas_ = tdup.berkas_tambahan.all()
			pemohon_ = tdup.pemohon
			legalitas_1 = perusahaan_.legalitas_set.filter(jenis_legalitas_id=1).last()
			legalitas_2 = perusahaan_.legalitas_set.filter(jenis_legalitas_id=2).last()

			if perusahaan_:
				npwp_perusahaan = perusahaan_.berkas_npwp
				if npwp_perusahaan:
					url_berkas.append(npwp_perusahaan.berkas.url)
					id_elemen.append('npwp_perusahaan')
					nm_berkas.append(npwp_perusahaan.nama_berkas)
					id_berkas.append(npwp_perusahaan.id)

			if berkas_:
				surat_keputusan = berkas_.filter(keterangan='Surat Permohonan '+perusahaan_.npwp).last()
				if surat_keputusan:
					url_berkas.append(surat_keputusan.berkas.url)
					id_elemen.append('surat_keputusan')
					nm_berkas.append(surat_keputusan.nama_berkas)
					id_berkas.append(surat_keputusan.id)

				izin_tempat_usaha = berkas_.filter(keterangan='Izin Tempat Usaha Pariwisata yang masih berlaku berlaku '+perusahaan_.npwp).last()
				if izin_tempat_usaha:
					url_berkas.append(izin_tempat_usaha.berkas.url)
					id_elemen.append('izin_tempat_usaha')
					nm_berkas.append(izin_tempat_usaha.nama_berkas)
					id_berkas.append(izin_tempat_usaha.id)

				sertifikat_lahan = berkas_.filter(keterangan='Sertifikat Lahan / Surat Sewa '+perusahaan_.npwp).last()
				if sertifikat_lahan:
					url_berkas.append(sertifikat_lahan.berkas.url)
					id_elemen.append('sertifikat_lahan')
					nm_berkas.append(sertifikat_lahan.nama_berkas)
					id_berkas.append(sertifikat_lahan.id)

				izin_gangguan = berkas_.filter(keterangan='Izin Gangguan '+perusahaan_.npwp).last()
				if izin_gangguan:
					url_berkas.append(izin_gangguan.berkas.url)
					id_elemen.append('izin_gangguan')
					nm_berkas.append(izin_gangguan.nama_berkas)
					id_berkas.append(izin_gangguan.id)

				imb = berkas_.filter(keterangan='IMB '+perusahaan_.npwp).last()
				if imb:
					url_berkas.append(imb.berkas.url)
					id_elemen.append('imb')
					nm_berkas.append(imb.nama_berkas)
					id_berkas.append(imb.id)

				siup = berkas_.filter(keterangan='SIUP '+perusahaan_.npwp).last()
				if siup:
					url_berkas.append(siup.berkas.url)
					id_elemen.append('siup')
					nm_berkas.append(siup.nama_berkas)
					id_berkas.append(siup.id)

				surat_pernyataan = berkas_.filter(keterangan='Surat pernyataan tertulis dari pengusaha yang menjamin bahwa data dan dokumen yang diserahakan benar dan sah '+perusahaan_.npwp).last()
				if surat_pernyataan:
					url_berkas.append(surat_pernyataan.berkas.url)
					id_elemen.append('surat_pernyataan')
					nm_berkas.append(surat_pernyataan.nama_berkas)
					id_berkas.append(surat_pernyataan.id)

				dokumen_lingkungan = berkas_.filter(keterangan='Dokumen lingkungan '+perusahaan_.npwp).last()
				if dokumen_lingkungan:
					url_berkas.append(dokumen_lingkungan.berkas.url)
					id_elemen.append('dokumen_lingkungan')
					nm_berkas.append(dokumen_lingkungan.nama_berkas)
					id_berkas.append(dokumen_lingkungan.id)

				izin_usaha_angkutan = berkas_.filter(keterangan='Izin Usaha Angkutan Khusus untuk bidang jasa transportasi wisata '+perusahaan_.npwp).last()
				if izin_usaha_angkutan:
					url_berkas.append(izin_usaha_angkutan.berkas.url)
					id_elemen.append('izin_usaha_angkutan')
					nm_berkas.append(izin_usaha_angkutan.nama_berkas)
					id_berkas.append(izin_usaha_angkutan.id)

				berkas_tambahan = berkas_.filter(keterangan='Berkas Tambahan '+perusahaan_.npwp).last()
				if berkas_tambahan:
					url_berkas.append(berkas_tambahan.berkas.url)
					id_elemen.append('berkas_tambahan')
					nm_berkas.append(berkas_tambahan.nama_berkas)
					id_berkas.append(berkas_tambahan.id)

			if pemohon_:
				npwp_pribadi = pemohon_.berkas_npwp
				if npwp_pribadi:
					url_berkas.append(npwp_pribadi.berkas.url)
					id_elemen.append('npwp_pribadi')
					nm_berkas.append(npwp_pribadi.nama_berkas)
					id_berkas.append(npwp_pribadi.id)

			if legalitas_1:
				legalitas_1 = legalitas_1.berkas
				if legalitas_1:
					url_berkas.append(legalitas_1.berkas.url)
					id_elemen.append('akta_pendirian')
					nm_berkas.append(legalitas_1.nama_berkas)
					id_berkas.append(legalitas_1.id)

			if legalitas_2:
				legalitas_2 = legalitas_2.berkas
				if legalitas_2:
					url_berkas.append(legalitas_2.berkas.url)
					id_elemen.append('akta_perubahan')
					nm_berkas.append(legalitas_2.nama_berkas)
					id_berkas.append(legalitas_2.id)

			nomor_ktp = request.COOKIES['nomor_ktp']
			if nomor_ktp:
				ktp_ = Berkas.objects.filter(nama_berkas="Berkas KTP Pemohon "+str(nomor_ktp)).last()
				if ktp_:
					url_berkas.append(ktp_.berkas.url)
					id_elemen.append('ktp')
					nm_berkas.append(ktp_.nama_berkas)
					id_berkas.append(ktp_.id)

			data = {'success': True, 'pesan': 'Perusahaan Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': '' }
	response = HttpResponse(json.dumps(data))
	return response

def tdup_done(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilTDUP.objects.get(id=request.COOKIES['id_pengajuan'])
			pengajuan_.status = 6
			pengajuan_.save()
					
			data = {'success': True, 'pesan': 'Proses Selesai.' , 'data':{'pengajuan_id':pengajuan_.id}}
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
			data = {'success': False, 'pesan': 'Data pengajuan tidak terdaftar.'}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'success': False, 'pesan': 'Data pengajuan tidak terdaftar.'}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def ajax_konfirmasi_tdup(request, pengajuan_id):
	if pengajuan_id:
		pengajuan_ = DetilTDUP.objects.get(id=pengajuan_id)
		jenis_pengajuan = ""
		ktp_ = ""
		paspor_ = ""
		if pengajuan_:
			pemohon_ = pengajuan_.pemohon
			perusahaan_ = pengajuan_.perusahaan
			
			jenis_pengajuan = pengajuan_.jenis_permohonan.jenis_permohonan_izin
			nama_kuasa = ""
			no_identitas_kuasa = ""
			telephone_kuasa = ""
			if pengajuan_.nama_kuasa:
				nama_kuasa = pengajuan_.nama_kuasa
				no_identitas_kuasa = pengajuan_.no_identitas_kuasa
				telephone_kuasa = pengajuan_.telephone_kuasa
			data_kuasa = {'kuasa': {'nama_kuasa':nama_kuasa, 'no_identitas_kuasa':no_identitas_kuasa, 'telephone_kuasa':telephone_kuasa}}
			if pemohon_:
				ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pemohon_.id, jenis_identitas_id=1).last()
				paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pemohon_.id, jenis_identitas_id=2).last()
				jenis_pemohon = pemohon_.jenis_pemohon.jenis_pemohon
				nama_lengkap_pemohon = pemohon_.nama_lengkap
				alamat_lengkap_pemohon = str(pemohon_.alamat)+", Ds. "+str(pemohon_.desa.nama_desa)+", Kec."+str(pemohon_.desa.kecamatan.nama_kecamatan)+", "+str(pemohon_.desa.kecamatan.kabupaten.nama_kabupaten)
				telephone_pemohon = pemohon_.telephone
				hp_pemohon = pemohon_.hp
				email_pemohon = ""
				if pemohon_.email is not None:
					email_pemohon = str(pemohon_.email)
				kewarganegaraan_pemohon = pemohon_.kewarganegaraan
				pekerjaan_pemohon = pemohon_.pekerjaan
				nomor_ktp = ""
				nomor_paspor = ""
				if 'nomor_ktp' in request.COOKIES.keys():
					nomor_ktp = request.COOKIES['nomor_ktp']
				elif ktp_.nomor:
					nomor_ktp = ktp_.nomor
				if 'nomor_paspor' in request.COOKIES.keys():
					nomor_paspor = request.COOKIES['nomor_paspor']
				elif paspor_.nomor:
					nomor_paspor = paspor_.nomor
			data_pemohon = {'pemohon': 
					{
						'jenis_pengajuan': jenis_pengajuan, 
						'ktp_paspor': nomor_ktp+" / "+nomor_paspor, 
						'jenis_pemohon': jenis_pemohon, 
						'nama_lengkap_pemohon': nama_lengkap_pemohon, 
						'alamat_lengkap_pemohon': alamat_lengkap_pemohon, 
						'telephone_pemohon': telephone_pemohon, 
						'hp_pemohon': hp_pemohon, 
						'email_pemohon': email_pemohon, 
						'kewarganegaraan_pemohon': kewarganegaraan_pemohon, 
						'pekerjaan_pemohon': pekerjaan_pemohon
					}
				}

			if perusahaan_:
				npwp_perusahaan = perusahaan_.npwp
				nama_perusahaan = perusahaan_.nama_perusahaan
				alamat_lengkap_perusahaan = str(perusahaan_.alamat_perusahaan)+", Ds. "+str(perusahaan_.desa.nama_desa)+", Kec."+str(perusahaan_.desa.kecamatan.nama_kecamatan)+", "+str(perusahaan_.desa.kecamatan.kabupaten.nama_kabupaten)
				kode_pos_perusahaan = perusahaan_.kode_pos
				telephone_perusahaan = perusahaan_.telepon
				fax_perusahaan = perusahaan_.fax
				email_perusahaan = perusahaan_.email
			data_perusahaan = {'perusahaan': 
				{
					'npwp_perusahaan':npwp_perusahaan,
					'nama_perusahaan':nama_perusahaan, 
					'alamat_lengkap_perusahaan':alamat_lengkap_perusahaan, 
					'kode_pos_perusahaan':kode_pos_perusahaan, 
					'telephone_perusahaan':telephone_perusahaan, 
					'fax_perusahaan':fax_perusahaan, 
					'email_perusahaan':email_perusahaan
				}
			}
			
			# ############# step 3 ############
			bidang_usaha_pariwisata = ''
			jenis_usaha_pariwisata = ''
			sub_jenis_usaha_pariwisata = ''
			if pengajuan_.bidang_usaha_pariwisata:
				bidang_usaha_pariwisata = pengajuan_.bidang_usaha_pariwisata.nama_bidang_usaha_pariwisata
			if pengajuan_.jenis_usaha_pariwisata:
				jenis_usaha_pariwisata = pengajuan_.jenis_usaha_pariwisata.nama_jenis_usaha_pariwisata
			if pengajuan_.sub_jenis_usaha_pariwisata:
				sub_jenis_usaha_pariwisata = pengajuan_.sub_jenis_usaha_pariwisata.nama_sub_jenis
			# //////// rincian sub jenis /////
			jumlah_unit_angkutan_jalan_wisata = ''
			kapasitas_angkutan_jalan_wisata = ''
			jumlah_unit_angkutan_kereta_api_wisata = ''
			kapasitas_angkutan_kereta_api_wisata = ''
			jumlah_unit_angkutan_sungai_dan_danau_wisata = ''
			kapasitas_angkutan_sungai_dan_danau_wisata = ''
			jumlah_kursi_restoran = ''
			jumlah_kursi_rumah_makan = ''
			jumlah_kursi_bar_atau_rumah_minum = ''
			jumlah_kursi_kafe = ''
			jumlah_stand_pusat_makanan = ''
			kapasitas_produksi_jasa_boga = ''
			if pengajuan_.rincian_sub_jenis:
				rincian = pengajuan_.rincian_sub_jenis
				if rincian.jumlah_unit_angkutan_jalan_wisata:
					jumlah_unit_angkutan_jalan_wisata = rincian.jumlah_unit_angkutan_jalan_wisata
				if rincian.kapasitas_angkutan_jalan_wisata:
					kapasitas_angkutan_jalan_wisata = rincian.kapasitas_angkutan_jalan_wisata
				if rincian.jumlah_unit_angkutan_kereta_api_wisata:
					jumlah_unit_angkutan_kereta_api_wisata = rincian.jumlah_unit_angkutan_kereta_api_wisata
				if rincian.kapasitas_angkutan_kereta_api_wisata:
					kapasitas_angkutan_kereta_api_wisata = rincian.kapasitas_angkutan_kereta_api_wisata
				if rincian.jumlah_unit_angkutan_sungai_dan_danau_wisata:
					jumlah_unit_angkutan_sungai_dan_danau_wisata = rincian.jumlah_unit_angkutan_sungai_dan_danau_wisata
				if rincian.kapasitas_angkutan_sungai_dan_danau_wisata:
					kapasitas_angkutan_sungai_dan_danau_wisata = rincian.kapasitas_angkutan_sungai_dan_danau_wisata
				if rincian.jumlah_kursi_restoran:
					jumlah_kursi_restoran = rincian.jumlah_kursi_restoran
				if rincian.jumlah_kursi_rumah_makan:
					jumlah_kursi_rumah_makan = rincian.jumlah_kursi_rumah_makan
				if rincian.jumlah_kursi_bar_atau_rumah_minum:
					jumlah_kursi_bar_atau_rumah_minum = rincian.jumlah_kursi_bar_atau_rumah_minum
				if rincian.jumlah_kursi_kafe:
					jumlah_kursi_kafe = rincian.jumlah_kursi_kafe
				if rincian.jumlah_stand_pusat_makanan:
					jumlah_stand_pusat_makanan = rincian.jumlah_stand_pusat_makanan
				if rincian.kapasitas_produksi_jasa_boga:
					kapasitas_produksi_jasa_boga = rincian.kapasitas_produksi_jasa_boga
			data_usaha = {'data_usaha':
				{
					'bidang_usaha_pariwisata': bidang_usaha_pariwisata,
					'jenis_usaha_pariwisata': jenis_usaha_pariwisata,
					'sub_jenis_usaha_pariwisata': sub_jenis_usaha_pariwisata,
					'jumlah_unit_angkutan_jalan_wisata': jumlah_unit_angkutan_jalan_wisata,
					'kapasitas_angkutan_jalan_wisata': kapasitas_angkutan_jalan_wisata,
					'jumlah_unit_angkutan_kereta_api_wisata': jumlah_unit_angkutan_kereta_api_wisata,
					'kapasitas_angkutan_kereta_api_wisata': kapasitas_angkutan_kereta_api_wisata,
					'jumlah_unit_angkutan_sungai_dan_danau_wisata': jumlah_unit_angkutan_sungai_dan_danau_wisata,
					'kapasitas_angkutan_sungai_dan_danau_wisata': kapasitas_angkutan_sungai_dan_danau_wisata,
					'jumlah_kursi_restoran': jumlah_kursi_restoran,
					'jumlah_kursi_rumah_makan': jumlah_kursi_rumah_makan,
					'jumlah_kursi_bar_atau_rumah_minum': jumlah_kursi_bar_atau_rumah_minum,
					'jumlah_kursi_kafe': jumlah_kursi_kafe,
					'jumlah_stand_pusat_makanan': jumlah_stand_pusat_makanan,
					'kapasitas_produksi_jasa_boga': kapasitas_produksi_jasa_boga,
				}
			}
			###################################
			# ######### step 4 ################
			nama_usaha = ''
			lokasi_usaha_pariwisata = ''
			telephone = ''
			nomor_izin_gangguan = ''
			tanggal_izin_gangguan = ''
			nomor_dokumen_pengelolaan = ''
			tanggal_dokumen_pengelolaan = ''
			if pengajuan_.nama_usaha:
				nama_usaha = pengajuan_.nama_usaha
			if pengajuan_.lokasi_usaha_pariwisata:
				lokasi_usaha_pariwisata = str(pengajuan_.lokasi_usaha_pariwisata) + ', Ds. ' +str(pengajuan_.desa_lokasi)+', Kec. '+str(pengajuan_.desa_lokasi.kecamatan)+', '+str(pengajuan_.desa_lokasi.kecamatan.kabupaten)+', Prov. '+str(pengajuan_.desa_lokasi.kecamatan.kabupaten.provinsi)
			if pengajuan_.telephone:
				telephone = pengajuan_.telephone
			# if pengajuan_.nomor_izin_gangguan:
			# 	nomor_izin_gangguan = pengajuan_.nomor_izin_gangguan
			# if pengajuan_.tanggal_izin_gangguan:
			# 	tanggal_izin_gangguan = pengajuan_.tanggal_izin_gangguan.strftime('%d-%m-%Y')
			izin_lain_json = []
			izin_lain_list = IzinLainTDUP.objects.filter(detil_tdup_id=pengajuan_.id)
			if izin_lain_list:
				izin_lain_json = [x.as_json() for x in izin_lain_list]
			if pengajuan_.nomor_dokumen_pengelolaan:
				nomor_dokumen_pengelolaan = pengajuan_.nomor_dokumen_pengelolaan
			if pengajuan_.tanggal_dokumen_pengelolaan:
				tanggal_dokumen_pengelolaan = pengajuan_.tanggal_dokumen_pengelolaan.strftime('%d-%m-%Y')
			keterangan_usaha = {'keterangan_usaha':
				{
					'nama_usaha': nama_usaha,
					'lokasi_usaha_pariwisata': lokasi_usaha_pariwisata,
					'telephone': telephone,
					'nomor_izin_gangguan': nomor_izin_gangguan,
					'tanggal_izin_gangguan': tanggal_izin_gangguan,
					'nomor_dokumen_pengelolaan': nomor_dokumen_pengelolaan,
					'tanggal_dokumen_pengelolaan': tanggal_dokumen_pengelolaan,
					'izin_lain_json': izin_lain_json
				}
			}
			###################################


			data = {'success': True, 'pesan': 'load konfirmasi berhasil', },data_pemohon, data_perusahaan, keterangan_usaha, data_kuasa, data_usaha
			response = HttpResponse(json.dumps(data))
			return response

def save_data_izin_lain(request):
	# izin_lain_obj, created = IzinLainTDUP.objects.get_or_create(id=id_izin_lain)
	pengajuan_id = request.POST.get('pengajuan_id')
	if pengajuan_id:
		no_izin = request.POST.get('nomor_izin', None)
		tanggal_izin = request.POST.get('tanggal_izin', None)
		print tanggal_izin
		if tanggal_izin:
			tanggal_izin = datetime.datetime.strptime(tanggal_izin, '%d-%m-%Y').strftime('%Y-%m-%d')
		izin_lain_obj = IzinLainTDUP(detil_tdup_id=pengajuan_id, no_izin=no_izin, tanggal_izin=tanggal_izin)
		izin_lain_obj.save()
		data = {'success': True, 'pesan': 'Simpan berhasil'}
	else:
		data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
	response = HttpResponse(json.dumps(data))
	return response

def delete_data_izin_lain(request, id_izin_lain):
	if id_izin_lain:
		try:
			i = IzinLainTDUP.objects.get(id=id_izin_lain)
			i.delete()
			data = {'success': True, 'pesan': 'Data berhasil dihapus.'}
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
	else:
		data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
	data = json.dumps(data)
	return HttpResponse(data)

def load_data_izin_lain(request, id_pengajuan):
	izin_lain_json = []
	if id_pengajuan:
		izin_lain_list = IzinLainTDUP.objects.filter(detil_tdup_id=id_pengajuan)
		if izin_lain_list:
			izin_lain_json = [x.as_json() for x in izin_lain_list]
	data = {'success': True, 'pesan': 'load konfirmasi berhasil', 'izin_lain_json': izin_lain_json}
	response = HttpResponse(json.dumps(data))
	return response
