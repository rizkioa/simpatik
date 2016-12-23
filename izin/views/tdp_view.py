import json
import datetime
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from izin.models import DetilTDP, RincianPerusahaan, IzinLain
from izin.tdp_forms import DataUmumPerusahaanPTForm, DataKegiatanPTForm, RincianPerusahaanForm, LegalitasForm, IzinLainForm
from perusahaan.models import Legalitas, Perusahaan

def tdp_data_umum_perusahaan_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
			data_umum_form = DataUmumPerusahaanPTForm(request.POST, instance=pengajuan_)
			onoffkantorcabang = request.POST.get('onoffkantorcabang')
			onoffunitproduksi = request.POST.get('onoffunitproduksi')
			no_tdp = request.POST.get('no_tdp')
			if data_umum_form.is_valid():
				p = data_umum_form.save(commit=False)
				p.jenis_badan_usaha_id = 1
				if onoffkantorcabang == 'on':
					p.nomor_tdp_kantor_pusat = no_tdp
				p.save()
				if onoffkantorcabang == 'on':
					npwp = request.POST.get('npwp_perusahaan_induk')
					nama = request.POST.get('nama_perusahaan_induk')
					alamat = request.POST.get('alamat_perusahaan_induk')
					desa = request.POST.get('desa_perusahaan_induk')
					perusahaan_cabang = request.COOKIES.get('id_perusahaan')
					try:
						per = Perusahaan.objects.get(npwp=npwp)
						per.perusahaan_induk_id = request.COOKIES['id_perusahaan_induk']
						per.nama_perusahaan = nama
						per.alamat_perusahaan = alamat
						per.desa_id = desa
						per.save()
					except ObjectDoesNotExist:
						per = Perusahaan(npwp=npwp, nama_perusahaan=nama, alamat_perusahaan=alamat, desa_id=desa)
						per.save(force_insert=True)
					try:
						per_cabang = Perusahaan.objects.get(id=perusahaan_cabang)
						per_cabang.perusahaan_induk_id = per.id
						per_cabang.save()
					except ObjectDoesNotExist:
						pass
				if onoffunitproduksi == 'on':
					alamat = request.POST.get('alamat_unit_produksi')
					desa = request.POST.get('desa_unit_prosuksi')
					try:
						unit = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
						unit.alamat_unit_produksi = alamat
						unit.desa_unit_produksi_id = desa
						unit.save()
					except ObjectDoesNotExist:
						pass
				data = {'success': True, 'pesan': 'Data Umum Perusahaan berhasil tersimpan.', 'data': []}
				data = json.dumps(data)
				response = HttpResponse(data)
				if onoffkantorcabang == 'on':
					response.set_cookie(key='id_perusahaan_induk', value=per.id)
					response.set_cookie(key='npwp_perusahaan_induk', value=per.npwp)
			else:
				data = data_umum_form.errors.as_json()
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

def tdp_data_kegiatan_pt_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
			data_kegiatan_form = DataKegiatanPTForm(request.POST, instance=pengajuan_)
			if data_kegiatan_form.is_valid():
				p = data_kegiatan_form.save(commit=False)
				p.save()
				try:
					rincian_ = RincianPerusahaan.objects.get(detil_tdp_id=p.id)
					rincianperusahaan_form = RincianPerusahaanForm(request.POST, instance=rincian_)
				except ObjectDoesNotExist:
					rincianperusahaan_form = RincianPerusahaanForm(request.POST)
				
				if rincianperusahaan_form.is_valid():
					rp = rincianperusahaan_form.save(commit=False)
					rp.detil_tdp_id = p.id
					rp.save()
					data = {'success': True, 'pesan': 'Data Kegiatan Perusahaan, berhasil tersimpan.', 'data': []}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = data_kegiatan_form.errors.as_json()
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

def tdp_legalitas_pt_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
			if 'id_perusahaan' in request.COOKIES.keys():
				if request.COOKIES['id_perusahaan'] != '':
					perusahaan = request.COOKIES['id_perusahaan']
					nama_notaris_pendirian = request.POST.get('nama_notaris_pendirian')
					alamat_pendirian = request.POST.get('alamat_pendirian')
					telephone_pendirian = request.POST.get('telephone_pendirian')
					nomor_akta_pendirian = request.POST.get('nomor_akta_pendirian')
					tanggal_akta_pendirian = datetime.datetime.strptime(request.POST.get('tanggal_akta_pendirian'), '%d-%m-%Y').strftime('%Y-%m-%d')
					nomor_pengesahan_pendirian = request.POST.get('nomor_pengesahan_pendirian')
					tanggal_pengesahan_pendirian = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_pendirian'), '%d-%m-%Y').strftime('%Y-%m-%d')
					# save legalitas pendirian
					try:
						legalitas_pendirian = Legalitas.objects.get(perusahaan_id=perusahaan, jenis_legalitas_id=1)
						if legalitas_pendirian.jenis_legalitas_id == 1:
							legalitas_pendirian.jenis_legalitas_id=1
							legalitas_pendirian.perusahaan_id = perusahaan
							legalitas_pendirian.nama_notaris = nama_notaris_pendirian
							legalitas_pendirian.alamat = alamat_pendirian
							legalitas_pendirian.telephone = telephone_pendirian
							legalitas_pendirian.nomor_akta = nomor_akta_pendirian
							legalitas_pendirian.tanggal_akta = tanggal_akta_pendirian
							legalitas_pendirian.nomor_pengesahan = nomor_pengesahan_pendirian
							legalitas_pendirian.tanggal_pengesahan = tanggal_pengesahan_pendirian
							legalitas_pendirian.save()
						else:
							pass
					except ObjectDoesNotExist:
						legalitas_pendirian = Legalitas(perusahaan_id=perusahaan, jenis_legalitas_id=1,  nama_notaris=nama_notaris_pendirian, alamat=alamat_pendirian, telephone=telephone_pendirian, nomor_akta=nomor_akta_pendirian, tanggal_akta=tanggal_akta_pendirian, nomor_pengesahan=nomor_pengesahan_pendirian, tanggal_pengesahan=tanggal_pengesahan_pendirian)
						legalitas_pendirian.save(force_insert=True)
					# +++++++ save akta perubahan ++++
					onoffaktaperubahan = request.POST.get('onoffaktaperubahan')
					if onoffaktaperubahan == 'on':
						nama_notaris_perubahan = request.POST.get('nama_notaris_akta_perubahan')
						alamat_perubahan = request.POST.get('alamat_akta_perubahan')
						telephone_perubahan = request.POST.get('telephone_akta_perubahan')
						nomor_akta_perubahan = request.POST.get('nomor_akta_perubahan')
						tanggal_akta_perubahan = datetime.datetime.strptime(request.POST.get('tanggal_akta_perubahan'), '%d-%m-%Y').strftime('%Y-%m-%d')
						nomor_pengesahan_perubahan = request.POST.get('nomor_pengesahan_akta_perubahan')
						tanggal_pengesahan_perubahan = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_akta_perubahan'), '%d-%m-%Y').strftime('%Y-%m-%d')
						try:
							legalitas_perubahan = Legalitas.objects.get(perusahaan_id=perusahaan, jenis_legalitas_id=2)
							legalitas_perubahan.jenis_legalitas_id = 2
							legalitas_perubahan.perusahaan_id = perusahaan
							legalitas_perubahan.nama_notaris = nama_notaris_perubahan
							legalitas_perubahan.alamat = alamat_perubahan
							legalitas_perubahan.telephone = telephone_perubahan
							legalitas_perubahan.nomor_akta = nomor_akta_perubahan
							legalitas_perubahan.tanggal_akta = tanggal_akta_perubahan
							legalitas_perubahan.nomor_pengesahan = nomor_pengesahan_perubahan
							legalitas_perubahan.tanggal_pengesahan = tanggal_pengesahan_perubahan
							legalitas_perubahan.save()
						except ObjectDoesNotExist:
							legalitas_perubahan = Legalitas(perusahaan_id=perusahaan, jenis_legalitas_id=2,  nama_notaris=nama_notaris_perubahan, alamat=alamat_perubahan, telephone=telephone_perubahan, nomor_akta=nomor_akta_perubahan, tanggal_akta=tanggal_akta_perubahan, nomor_pengesahan=nomor_pengesahan_perubahan, tanggal_pengesahan=tanggal_pengesahan_perubahan)
							legalitas_perubahan.save(force_insert=True)
					# +++++++ end save akta perubahan ++++
					# +++++++ save pengesahan menteri +++++
					onoffpengesahanmenteri = request.POST.get('onoffpengesahanmenteri')
					if onoffpengesahanmenteri == 'on':
						noppm1 = request.POST.get('nomor_pengesahan_pengesahan_menteri')
						tglppm1 = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_pengesahan_menteri'), '%d-%m-%Y').strftime('%Y-%m-%d')
						try:
							legalitas_pengesahan_menteri = Legalitas.objects.get(perusahaan_id=perusahaan, jenis_legalitas_id=3)
							legalitas_pengesahan_menteri.jenis_legalitas_id = 3
							legalitas_pengesahan_menteri.perusahaan_id = perusahaan
							legalitas_pengesahan_menteri.nomor_pengesahan = noppm1
							legalitas_pengesahan_menteri.tanggal_pengesahan = tglppm1
							legalitas_pengesahan_menteri.save()
						except ObjectDoesNotExist:
							legalitas_pengesahan_menteri = Legalitas(nomor_pengesahan=noppm1, tanggal_pengesahan=tglppm1, jenis_legalitas_id=3, perusahaan_id=perusahaan)
							legalitas_pengesahan_menteri.save(force_insert=True)
					# +++++++ end save pengesahan menteri +++++
					# +++++++ save persetujuan menteri +++++
					onoffpersetujuanmenteri = request.POST.get('onoffpersetujuanmenteri')
					if onoffpersetujuanmenteri == 'on':
						noppm2 = request.POST.get('nomor_pengesahan_persetujuan_menteri')
						tglppm2 = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_persetujuan_menteri'), '%d-%m-%Y').strftime('%Y-%m-%d')
						try:
							legalitas_persetujuan_menteri = Legalitas.objects.get(perusahaan_id=perusahaan, jenis_legalitas_id=4)
							legalitas_persetujuan_menteri.jenis_legalitas_id = 4
							legalitas_persetujuan_menteri.perusahaan_id = perusahaan
							legalitas_persetujuan_menteri.nomor_pengesahan = noppm2
							legalitas_persetujuan_menteri.tanggal_pengesahan = tglppm2
							legalitas_persetujuan_menteri.save()
						except ObjectDoesNotExist:
							legalitas_persetujuan_menteri = Legalitas(nomor_pengesahan=noppm2, tanggal_pengesahan=tglppm2, jenis_legalitas_id=4, perusahaan_id=perusahaan)
							legalitas_persetujuan_menteri.save(force_insert=True)
					# +++++++ end save persetujuan menteri +++++
					# +++++++ save penerima laporan +++++
					onoffpenerimalaporan = request.POST.get('onoffpenerimalaporan')
					if onoffpenerimalaporan == 'on':
						noppm3 = request.POST.get('nomor_pengesahan_penerima_laporan')
						tglppm3 = datetime.datetime.strptime(request.POST.get('tanggal_pengesahaan_penerima_laporan'), '%d-%m-%Y').strftime('%Y-%m-%d')
						try:
							legalitas_penerima_laporan = Legalitas.objects.get(perusahaan_id=perusahaan, jenis_legalitas_id=6)
							legalitas_penerima_laporan.jenis_legalitas_id = 6
							legalitas_penerima_laporan.perusahaan_id = perusahaan
							legalitas_penerima_laporan.nomor_pengesahan = noppm3
							legalitas_penerima_laporan.tanggal_pengesahan = tglppm3
							legalitas_penerima_laporan.save()
						except ObjectDoesNotExist:
							legalitas_penerima_laporan = Legalitas(nomor_pengesahan=noppm3, tanggal_pengesahan=tglppm3, jenis_legalitas_id=6, perusahaan_id=perusahaan)
							legalitas_penerima_laporan.save(force_insert=True)
					# +++++++ end save penerima laporan +++++
					onoffpenerimaanpemberitahuan = request.POST.get('onoffpenerimaanpemberitahuan')
					if onoffpenerimaanpemberitahuan == 'on':
						noppm4 = request.POST.get('nomor_pengesahan_penerimaan_pemberitahuan')
						tglppm4 = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_penerimaan_pemberitahuan'), '%d-%m-%Y').strftime('%Y-%m-%d')
						try:
							legalitas_penerimaan_pemberitahuan = Legalitas.objects.get(perusahaan_id=perusahaan, jenis_legalitas_id=7)
							legalitas_penerimaan_pemberitahuan.jenis_legalitas_id = 7
							legalitas_penerimaan_pemberitahuan.perusahaan_id = perusahaan
							legalitas_penerimaan_pemberitahuan.nomor_pengesahan = noppm4
							legalitas_penerimaan_pemberitahuan.tanggal_pengesahan = tglppm4
							legalitas_penerimaan_pemberitahuan.save()
						except ObjectDoesNotExist:
							legalitas_penerimaan_pemberitahuan = Legalitas(nomor_pengesahan=noppm4, tanggal_pengesahan=tglppm4, jenis_legalitas_id=7, perusahaan_id=perusahaan)
							legalitas_penerimaan_pemberitahuan.save(force_insert=True)
					# +++++++ save penerimaan pemberitahuan +++++

					# +++++++ end save penerimaan pemberitahuan +++++

					data = {'success': True, 'pesan': 'Data Kegiatan Perusahaan, berhasil tersimpan.', 'data': []}
					data = json.dumps(data)
					response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Data Perusahaan tidak ditemukan/data kosong'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = {'Terjadi Kesalahan': [{'message': 'Data Perusahaan tidak ditemukan/data kosong'}]}
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


def load_data_umum_perusahaan(request, pengajuan_id):
	if pengajuan_id:
		pengajuan_ = DetilTDP.objects.filter(id=pengajuan_id).last()
		if pengajuan_:
			status_perusahaan = "0"
			if pengajuan_.status_perusahaan:
				status_perusahaan = pengajuan_.status_perusahaan.id
			jenis_badan_usaha = "0"
			if pengajuan_.jenis_badan_usaha:
				jenis_badan_usaha = pengajuan_.jenis_badan_usaha.id
			bentuk_kerjasama = "0"
			if pengajuan_.bentuk_kerjasama:
				bentuk_kerjasama = pengajuan_.bentuk_kerjasama.id
			jumlah_bank = ""
			if pengajuan_.jumlah_bank:
				jumlah_bank = pengajuan_.jumlah_bank
			nasabah_utama_bank_1 = ""
			if pengajuan_.nasabah_utama_bank_1:
				nasabah_utama_bank_1 = pengajuan_.nasabah_utama_bank_1
			nasabah_utama_bank_2 = ""
			if pengajuan_.nasabah_utama_bank_2:
				nasabah_utama_bank_2 = pengajuan_.nasabah_utama_bank_2
			jenis_penanaman_modal = "0"
			if pengajuan_.jenis_penanaman_modal:
				jenis_penanaman_modal = pengajuan_.jenis_penanaman_modal.id
			tanggal_pendirian = ""
			if pengajuan_.tanggal_pendirian:
				tanggal_pendirian = pengajuan_.tanggal_pendirian.strftime('%d-%m-%Y')
			tanggal_mulai_kegiatan = ""
			if pengajuan_.tanggal_mulai_kegiatan:
				tanggal_mulai_kegiatan = pengajuan_.tanggal_mulai_kegiatan.strftime('%d-%m-%Y')
			jangka_waktu_berdiri = ""
			if pengajuan_.jangka_waktu_berdiri:
				jangka_waktu_berdiri = pengajuan_.jangka_waktu_berdiri
			nomor_tdp_kantor_pusat = ""
			if pengajuan_.nomor_tdp_kantor_pusat:
				nomor_tdp_kantor_pusat = pengajuan_.nomor_tdp_kantor_pusat
			alamat_unit_produksi = ""
			if pengajuan_.alamat_unit_produksi:
				alamat_unit_produksi = pengajuan_.alamat_unit_produksi
			desa = "0"
			kecamatan = "0"
			kabupaten = "0"
			provinsi = "0"
			if pengajuan_.desa_unit_produksi:
				desa = pengajuan_.desa_unit_produksi.id
				print desa
				if pengajuan_.desa_unit_produksi.kecamatan:
					kecamatan = pengajuan_.desa_unit_produksi.kecamatan.id
					print kecamatan
					if pengajuan_.desa_unit_produksi.kecamatan.kabupaten:
						kabupaten = pengajuan_.desa_unit_produksi.kecamatan.kabupaten.id
						print kabupaten
						if pengajuan_.desa_unit_produksi.kecamatan.kabupaten.provinsi:
							provinsi = pengajuan_.desa_unit_produksi.kecamatan.kabupaten.provinsi.id
							print provinsi
			merek_dagang = ""
			if pengajuan_.merek_dagang:
				merek_dagang = pengajuan_.merek_dagang
			no_merek_dagang = ""
			if pengajuan_.no_merek_dagang:
				no_merek_dagang = pengajuan_.no_merek_dagang
			pemegang_hak_cipta = ""
			if pengajuan_.pemegang_hak_cipta:
				pemegang_hak_cipta = pengajuan_.pemegang_hak_cipta
			no_hak_cipta = ""
			if pengajuan_.pemegang_hak_cipta:
				no_hak_cipta = pengajuan_.pemegang_hak_cipta
			pemegang_hak_paten = ""
			if pengajuan_.pemegang_hak_paten:
				pemegang_hak_paten = pengajuan_.pemegang_hak_paten
			no_hak_paten = ""
			if pengajuan_.no_hak_paten:
				no_hak_paten = pengajuan_.no_hak_paten

			data = {'success': True, 'pesan': 'Load data umum perusahan', 'data':{
			'status_perusahaan': status_perusahaan, 'jenis_badan_usaha': jenis_badan_usaha, 'bentuk_kerjasama': bentuk_kerjasama, 'jumlah_bank': jumlah_bank, 'nasabah_utama_bank_1': nasabah_utama_bank_1, 'nasabah_utama_bank_2': nasabah_utama_bank_2, 'jenis_penanaman_modal': jenis_penanaman_modal, 'tanggal_pendirian': tanggal_pendirian, 'tanggal_mulai_kegiatan': tanggal_mulai_kegiatan, 'jangka_waktu_berdiri': jangka_waktu_berdiri, 'nomor_tdp_kantor_pusat': nomor_tdp_kantor_pusat, 'alamat_unit_produksi': alamat_unit_produksi, 'desa': desa, 'kecamatan': kecamatan, 'kabupaten': kabupaten, 'provinsi': provinsi, 'merek_dagang': merek_dagang,'no_merek_dagang': no_merek_dagang, 'pemegang_hak_cipta': pemegang_hak_cipta, 'no_hak_cipta': no_hak_cipta, 'pemegang_hak_paten': pemegang_hak_paten, 'no_hak_paten': no_hak_paten
			}}
		else:
			data = {'success': False, 'pesan': "Riwayat tidak ditemukan" }
	else:
		data = {'success': False, 'pesan': "Riwayat tidak ditemukan" }
	return HttpResponse(json.dumps(data))

def load_data_kegiatan_perusahaan(request, pengajuan_id):
	if pengajuan_id:
		pengajuan_ = DetilTDP.objects.filter(id=pengajuan_id).last()
		if pengajuan_:
			kegiatan_usaha_pokok = ""
			if pengajuan_.kegiatan_usaha_pokok:
				kegiatan_usaha_pokok = pengajuan_.kegiatan_usaha_pokok
			kegiatan_usaha_lain_1 = ""
			if pengajuan_.kegiatan_usaha_lain_1:
				kegiatan_usaha_lain_1 = pengajuan_.kegiatan_usaha_lain_1
			kegiatan_usaha_lain_2 = ""
			if pengajuan_.kegiatan_usaha_lain_2:
				kegiatan_usaha_lain_2 = pengajuan_.kegiatan_usaha_lain_2
			komoditi_produk_pokok = ""
			if pengajuan_.komoditi_produk_pokok:
				komoditi_produk_pokok = pengajuan_.komoditi_produk_pokok
			komoditi_produk_lain_1 = ""
			if pengajuan_.komoditi_produk_lain_1:
				komoditi_produk_lain_1 = pengajuan_.komoditi_produk_lain_1
			komoditi_produk_lain_2 = ""
			if pengajuan_.komoditi_produk_lain_2:
				komoditi_produk_lain_2 = pengajuan_.komoditi_produk_lain_2
			omset_per_tahun = ""
			if pengajuan_.omset_per_tahun:
				omset_per_tahun = pengajuan_.omset_per_tahun
			total_aset = ""
			if pengajuan_.total_aset:
				total_aset = pengajuan_.total_aset
			jumlah_karyawan_wni = ""
			if pengajuan_.jumlah_karyawan_wni:
				jumlah_karyawan_wni = pengajuan_.jumlah_karyawan_wni
			jumlah_karyawan_wna = ""
			if pengajuan_.jumlah_karyawan_wna:
				jumlah_karyawan_wna = pengajuan_.jumlah_karyawan_wna
			kapasitas_mesin_terpasang = ""
			if pengajuan_.kapasitas_mesin_terpasang:
				kapasitas_mesin_terpasang = int(pengajuan_.kapasitas_mesin_terpasang)
			satuan_kapasitas_mesin_terpasang = ""
			if pengajuan_.satuan_kapasitas_mesin_terpasang:
				satuan_kapasitas_mesin_terpasang = pengajuan_.satuan_kapasitas_mesin_terpasang
			kapasitas_produksi_per_tahun = ""
			if pengajuan_.kapasitas_produksi_per_tahun:
				kapasitas_produksi_per_tahun = int(pengajuan_.kapasitas_produksi_per_tahun)
			satuan_kapasitas_produksi_per_tahun = ""
			if pengajuan_.satuan_kapasitas_produksi_per_tahun:
				satuan_kapasitas_produksi_per_tahun = pengajuan_.satuan_kapasitas_produksi_per_tahun
			presentase_kandungan_produk_lokal = ""
			if pengajuan_.presentase_kandungan_produk_lokal:
				presentase_kandungan_produk_lokal = str(pengajuan_.presentase_kandungan_produk_lokal)
			presentase_kandungan_produk_import = ""
			if pengajuan_.presentase_kandungan_produk_import:
				presentase_kandungan_produk_import = str(pengajuan_.presentase_kandungan_produk_import)
			jenis_pengecer = "0"
			if pengajuan_.jenis_pengecer:
				jenis_pengecer = pengajuan_.jenis_pengecer.id
			kedudukan_kegiatan_usaha = "0"
			if pengajuan_.kedudukan_kegiatan_usaha:
				kedudukan_kegiatan_usaha = pengajuan_.kedudukan_kegiatan_usaha.id
			jenis_perusahaan = "0"
			if pengajuan_.jenis_perusahaan:
				jenis_perusahaan = pengajuan_.jenis_perusahaan.id

			# +++++ Rincian Perusahaan ++++++++++++
			rincian_ = RincianPerusahaan.objects.filter(detil_tdp_id=pengajuan_id).last()
			modal_dasar = ""
			modal_ditempatkan = ""
			modal_disetor = ""
			banyaknya_saham = ""
			nilai_nominal_per_saham = ""
			if rincian_:
				if rincian_.modal_dasar:
					modal_dasar = rincian_.modal_dasar
				if rincian_.modal_ditempatkan:
					modal_ditempatkan = rincian_.modal_ditempatkan
				if rincian_.modal_disetor:
					modal_disetor = rincian_.modal_disetor
				if rincian_.banyaknya_saham:
					banyaknya_saham = rincian_.banyaknya_saham
				if rincian_.nilai_nominal_per_saham:
					nilai_nominal_per_saham = rincian_.nilai_nominal_per_saham

			data = {'success': True, 'pesan': 'Load data kegiatan perusahan', 'data':{'kegiatan_usaha_pokok': kegiatan_usaha_pokok, 'kegiatan_usaha_lain_1': kegiatan_usaha_lain_1, 'kegiatan_usaha_lain_2': kegiatan_usaha_lain_2, 'komoditi_produk_pokok': komoditi_produk_pokok, 'komoditi_produk_lain_1': komoditi_produk_lain_1, 'komoditi_produk_lain_2': komoditi_produk_lain_2, 'omset_per_tahun': omset_per_tahun, 'total_aset': total_aset, 'jumlah_karyawan_wni': jumlah_karyawan_wni, 'jumlah_karyawan_wna': jumlah_karyawan_wna, 'kapasitas_mesin_terpasang': kapasitas_mesin_terpasang, 'satuan_kapasitas_mesin_terpasang': satuan_kapasitas_mesin_terpasang, 'kapasitas_produksi_per_tahun': kapasitas_produksi_per_tahun, 'satuan_kapasitas_produksi_per_tahun': satuan_kapasitas_produksi_per_tahun, 'presentase_kandungan_produk_lokal': presentase_kandungan_produk_lokal, 'presentase_kandungan_produk_import': presentase_kandungan_produk_import, 'jenis_pengecer': jenis_pengecer, 'kedudukan_kegiatan_usaha': kedudukan_kegiatan_usaha, 'jenis_perusahaan': jenis_perusahaan, 'modal_dasar': modal_dasar, 'modal_ditempatkan': modal_ditempatkan, 'modal_disetor': modal_disetor, 'banyaknya_saham': banyaknya_saham, 'nilai_nominal_per_saham': nilai_nominal_per_saham}}
		else:
			data = {'success': False, 'pesan': "Riwayat tidak ditemukan" }
	else:
		data = {'success': False, 'pesan': "Riwayat tidak ditemukan" }
	return HttpResponse(json.dumps(data))

def tdp_izin_lain_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			try:
				pengajuan_ = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
				izin_lain_form = IzinLainForm(request.POST)
				if izin_lain_form.is_valid():
					i = izin_lain_form.save(commit=False)
					i.pengajuan_izin_id = pengajuan_.id
					i.save()
					data = {'success': True, 'pesan': 'IzinLain disimpan. Proses Selanjutnya.', 'data': [{'id':i.id}, {'jenis_izin':i.kelompok_jenis_izin.kelompok_jenis_izin}, {'no_izin':i.no_izin}, {'dikeluarkan_oleh':i.dikeluarkan_oleh}, {'tanggal_dikeluarkan':i.tanggal_dikeluarkan.strftime('%d-%m-%Y')}, {'masa_berlaku':i.masa_berlaku}]}
					data = json.dumps(data)
					response = HttpResponse(data)
				else:
					data = izin_lain_form.errors.as_json()
					response = HttpResponse(data)
			except ObjectDoesNotExist:
				data = {'Terjadi Kesalahan': [{'message': 'Data tidak ditemukan.'}]}
				data = json.dumps(data)
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data tidak ditemukan.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data tidak ditemukan.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def load_tdp_izin_lain(request, pengajuan_id):
	if pengajuan_id:
		i = IzinLain.objects.filter(pengajuan_izin_id=pengajuan_id)
		if len(i) > 0:
			data = [ob.as_json() for ob in i]
			response = HttpResponse(json.dumps(data), content_type="application/json")
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data tidak ditemukan.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def edit_tdp_izin_lain(request, pengajuan_id):
	if pengajuan_id:
		try:
			i = IzinLain.objects.get(id=pengajuan_id)

			kelompok_jenis_izin = i.kelompok_jenis_izin.id
			no_izin = i.no_izin
			dikeluarkan_oleh = i.dikeluarkan_oleh
			tanggal_dikeluarkan = i.tanggal_dikeluarkan.strftime('%d-%m-%Y')
			masa_berlaku = i.masa_berlaku
			data = {'data':{'jenis_izin':kelompok_jenis_izin, 'no_izin':no_izin, 'dikeluarkan_oleh': dikeluarkan_oleh, 'tanggal_dikeluarkan': tanggal_dikeluarkan, 'masa_berlaku': masa_berlaku}}
			data = json.dumps(data)
			response = HttpResponse(data)
		except ObjectDoesNotExist:
			data = {'Terjadi Kesalahan': [{'message': 'Data tidak ditemukan.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data tidak ditemukan.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response
