import os
import json
import datetime
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import NomorIdentitasPengguna
from izin.models import DetilTDP, RincianPerusahaan, IzinLain, PengajuanIzin, KelompokJenisIzin
from izin.tdp_forms import DataUmumPerusahaanPTForm, DataKegiatanPTForm, RincianPerusahaanForm, LegalitasForm, IzinLainForm, PemegangSahamForm, DataPimpinanForm, PerusahaanCabangForm, BerkasForm
from perusahaan.models import Legalitas, Perusahaan, PemegangSaham, DataPimpinan, KBLI
from master.models import Berkas

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
				# jbu = request.POST.get('jenis_badan_usaha')
				k = KelompokJenisIzin.objects.filter(id=request.COOKIES['id_kelompok_izin']).last()
				if k.id == 25:
					p.nomor_tdp_kantor_pusat = 1
				elif k.id == 26:
					p.nomor_tdp_kantor_pusat = 2
				# if onoffkantorcabang == 'on':
				# 	p.nomor_tdp_kantor_pusat = no_tdp
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
						per.nomor_tdp = no_tdp
						per.save()
					except ObjectDoesNotExist:
						per = Perusahaan(npwp=npwp, nama_perusahaan=nama, alamat_perusahaan=alamat, desa_id=desa, nomor_tdp=no_tdp)
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
				kegiatan_usaha = request.POST.getlist('kegiatan_usaha_pokok')
				nama_kbli = []
				for kbli in kegiatan_usaha:
					kbli_obj = KBLI.objects.get(id=kbli)
					p.kegiatan_usaha_pokok.add(kbli_obj)
					nama_kbli.append(kbli_obj.nama_kbli)			
				if len(nama_kbli) > 1:
					p.produk_utama = ",".join(nama_kbli)
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
					# nomor_pengesahan_pendirian = request.POST.get('nomor_pengesahan_pendirian')
					# tanggal_pengesahan_pendirian = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_pendirian'), '%d-%m-%Y').strftime('%Y-%m-%d')
					perusahaan_id = pengajuan_.perusahaan.id
					# save legalitas pendirian
					try:
						legalitas_pendirian = Legalitas.objects.get(perusahaan_id=perusahaan_id, jenis_legalitas_id=1)
						# if legalitas_pendirian.jenis_legalitas_id == 1:
						legalitas_pendirian.jenis_legalitas_id=1
						legalitas_pendirian.perusahaan_id = perusahaan_id
						legalitas_pendirian.nama_notaris = nama_notaris_pendirian
						legalitas_pendirian.alamat = alamat_pendirian
						legalitas_pendirian.telephone = telephone_pendirian
						legalitas_pendirian.nomor_akta = nomor_akta_pendirian
						legalitas_pendirian.tanggal_akta = tanggal_akta_pendirian
						# legalitas_pendirian.nomor_pengesahan = nomor_pengesahan_pendirian
						# legalitas_pendirian.tanggal_pengesahan = tanggal_pengesahan_pendirian
						legalitas_pendirian.save()
						# else:
						# 	pass
					except ObjectDoesNotExist:
						legalitas_pendirian = Legalitas(perusahaan_id=perusahaan_id, jenis_legalitas_id=1,  nama_notaris=nama_notaris_pendirian, alamat=alamat_pendirian, telephone=telephone_pendirian, nomor_akta=nomor_akta_pendirian, tanggal_akta=tanggal_akta_pendirian)
						legalitas_pendirian.save(force_insert=True)
					# +++++++ save akta perubahan ++++
					onoffaktaperubahan = request.POST.get('onoffaktaperubahan')
					if onoffaktaperubahan == 'on':
						nama_notaris_perubahan = request.POST.get('nama_notaris_akta_perubahan')
						alamat_perubahan = request.POST.get('alamat_akta_perubahan')
						telephone_perubahan = request.POST.get('telephone_akta_perubahan')
						nomor_akta_perubahan = request.POST.get('nomor_akta_perubahan')
						tanggal_akta_perubahan = datetime.datetime.strptime(request.POST.get('tanggal_akta_perubahan'), '%d-%m-%Y').strftime('%Y-%m-%d')
						# nomor_pengesahan_perubahan = request.POST.get('nomor_pengesahan_akta_perubahan')
						# tanggal_pengesahan_perubahan = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_akta_perubahan'), '%d-%m-%Y').strftime('%Y-%m-%d')
						try:
							legalitas_perubahan = Legalitas.objects.get(perusahaan_id=perusahaan_id, jenis_legalitas_id=2)
							legalitas_perubahan.jenis_legalitas_id = 2
							legalitas_perubahan.perusahaan_id = perusahaan
							legalitas_perubahan.nama_notaris = nama_notaris_perubahan
							legalitas_perubahan.alamat = alamat_perubahan
							legalitas_perubahan.telephone = telephone_perubahan
							legalitas_perubahan.nomor_akta = nomor_akta_perubahan
							legalitas_perubahan.tanggal_akta = tanggal_akta_perubahan
							# legalitas_perubahan.nomor_pengesahan = nomor_pengesahan_perubahan
							# legalitas_perubahan.tanggal_pengesahan = tanggal_pengesahan_perubahan
							legalitas_perubahan.save()
						except ObjectDoesNotExist:
							legalitas_perubahan = Legalitas(perusahaan_id=perusahaan_id, jenis_legalitas_id=2,  nama_notaris=nama_notaris_perubahan, alamat=alamat_perubahan, telephone=telephone_perubahan, nomor_akta=nomor_akta_perubahan, tanggal_akta=tanggal_akta_perubahan)
							legalitas_perubahan.save(force_insert=True)
					# +++++++ end save akta perubahan ++++
					# +++++++ save pengesahan menteri +++++
					onoffpengesahanmenteri = request.POST.get('onoffpengesahanmenteri')
					if onoffpengesahanmenteri == 'on':
						noppm1 = request.POST.get('nomor_pengesahan_pengesahan_menteri')
						tglppm1 = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_pengesahan_menteri'), '%d-%m-%Y').strftime('%Y-%m-%d')
						try:
							legalitas_pengesahan_menteri = Legalitas.objects.get(perusahaan_id=perusahaan_id, jenis_legalitas_id=3)
							legalitas_pengesahan_menteri.jenis_legalitas_id = 3
							legalitas_pengesahan_menteri.perusahaan_id = perusahaan_id
							legalitas_pengesahan_menteri.nomor_pengesahan = noppm1
							legalitas_pengesahan_menteri.tanggal_pengesahan = tglppm1
							legalitas_pengesahan_menteri.save()
						except ObjectDoesNotExist:
							legalitas_pengesahan_menteri = Legalitas(nomor_pengesahan=noppm1, tanggal_pengesahan=tglppm1, jenis_legalitas_id=3, perusahaan_id=perusahaan_id)
							legalitas_pengesahan_menteri.save(force_insert=True)
					# +++++++ end save pengesahan menteri +++++
					# +++++++ save persetujuan menteri +++++
					onoffpersetujuanmenteri = request.POST.get('onoffpersetujuanmenteri')
					if onoffpersetujuanmenteri == 'on':
						noppm2 = request.POST.get('nomor_pengesahan_persetujuan_menteri')
						tglppm2 = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_persetujuan_menteri'), '%d-%m-%Y').strftime('%Y-%m-%d')
						try:
							legalitas_persetujuan_menteri = Legalitas.objects.get(perusahaan_id=perusahaan_id, jenis_legalitas_id=4)
							legalitas_persetujuan_menteri.jenis_legalitas_id = 4
							legalitas_persetujuan_menteri.perusahaan_id = perusahaan_id
							legalitas_persetujuan_menteri.nomor_pengesahan = noppm2
							legalitas_persetujuan_menteri.tanggal_pengesahan = tglppm2
							legalitas_persetujuan_menteri.save()
						except ObjectDoesNotExist:
							legalitas_persetujuan_menteri = Legalitas(nomor_pengesahan=noppm2, tanggal_pengesahan=tglppm2, jenis_legalitas_id=4, perusahaan_id=perusahaan_id)
							legalitas_persetujuan_menteri.save(force_insert=True)
					# +++++++ end save persetujuan menteri +++++
					# +++++++ save penerima laporan +++++
					onoffpenerimalaporan = request.POST.get('onoffpenerimalaporan')
					if onoffpenerimalaporan == 'on':
						noppm3 = request.POST.get('nomor_pengesahan_penerima_laporan')
						tglppm3 = datetime.datetime.strptime(request.POST.get('tanggal_pengesahaan_penerima_laporan'), '%d-%m-%Y').strftime('%Y-%m-%d')
						try:
							legalitas_penerima_laporan = Legalitas.objects.get(perusahaan_id=perusahaan_id, jenis_legalitas_id=6)
							legalitas_penerima_laporan.jenis_legalitas_id = 6
							legalitas_penerima_laporan.perusahaan_id = perusahaan_id
							legalitas_penerima_laporan.nomor_pengesahan = noppm3
							legalitas_penerima_laporan.tanggal_pengesahan = tglppm3
							legalitas_penerima_laporan.save()
						except ObjectDoesNotExist:
							legalitas_penerima_laporan = Legalitas(nomor_pengesahan=noppm3, tanggal_pengesahan=tglppm3, jenis_legalitas_id=6, perusahaan_id=perusahaan_id)
							legalitas_penerima_laporan.save(force_insert=True)
					# +++++++ end save penerima laporan +++++
					onoffpenerimaanpemberitahuan = request.POST.get('onoffpenerimaanpemberitahuan')
					if onoffpenerimaanpemberitahuan == 'on':
						noppm4 = request.POST.get('nomor_pengesahan_penerimaan_pemberitahuan')
						tglppm4 = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_penerimaan_pemberitahuan'), '%d-%m-%Y').strftime('%Y-%m-%d')
						try:
							legalitas_penerimaan_pemberitahuan = Legalitas.objects.get(perusahaan_id=perusahaan_id, jenis_legalitas_id=7)
							legalitas_penerimaan_pemberitahuan.jenis_legalitas_id = 7
							legalitas_penerimaan_pemberitahuan.perusahaan_id = perusahaan_id
							legalitas_penerimaan_pemberitahuan.nomor_pengesahan = noppm4
							legalitas_penerimaan_pemberitahuan.tanggal_pengesahan = tglppm4
							legalitas_penerimaan_pemberitahuan.save()
						except ObjectDoesNotExist:
							legalitas_penerimaan_pemberitahuan = Legalitas(nomor_pengesahan=noppm4, tanggal_pengesahan=tglppm4, jenis_legalitas_id=7, perusahaan_id=perusahaan_id)
							legalitas_penerimaan_pemberitahuan.save(force_insert=True)
					# +++++++ save penerimaan pemberitahuan +++++

					# +++++++ end save penerimaan pemberitahuan +++++

					data = {'success': True, 'pesan': 'Data Kegiatan Perusahaan, berhasil tersimpan.', 'data': []}
					data = json.dumps(data)
					response = HttpResponse(data)
					response.set_cookie(key='id_legalitas', value=legalitas_pendirian.id)
					if onoffaktaperubahan == 'on':
						response.set_cookie(key='id_legalitas_perubahan', value=legalitas_perubahan.id)

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
			# nomor_tdp_kantor_pusat = ""
			# if pengajuan_.nomor_tdp_kantor_pusat:
			# 	nomor_tdp_kantor_pusat = pengajuan_.nomor_tdp_kantor_pusat
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

			data = {'success': True, 'pesan': 'Load data umum perusahaan', 'data':{
			'status_perusahaan': status_perusahaan, 'jenis_badan_usaha': jenis_badan_usaha, 'bentuk_kerjasama': bentuk_kerjasama, 'jumlah_bank': jumlah_bank, 'nasabah_utama_bank_1': nasabah_utama_bank_1, 'nasabah_utama_bank_2': nasabah_utama_bank_2, 'jenis_penanaman_modal': jenis_penanaman_modal, 'tanggal_pendirian': tanggal_pendirian, 'tanggal_mulai_kegiatan': tanggal_mulai_kegiatan, 'jangka_waktu_berdiri': jangka_waktu_berdiri, 'alamat_unit_produksi': alamat_unit_produksi, 'desa': desa, 'kecamatan': kecamatan, 'kabupaten': kabupaten, 'provinsi': provinsi, 'merek_dagang': merek_dagang,'no_merek_dagang': no_merek_dagang, 'pemegang_hak_cipta': pemegang_hak_cipta, 'no_hak_cipta': no_hak_cipta, 'pemegang_hak_paten': pemegang_hak_paten, 'no_hak_paten': no_hak_paten
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
			# kegiatan_usaha_pokok = ""
			# if pengajuan_.kegiatan_usaha_pokok:
			# 	kegiatan_usaha_pokok = pengajuan_.kegiatan_usaha_pokok
			# kegiatan_usaha_lain_1 = ""
			# if pengajuan_.kegiatan_usaha_lain_1:
			# 	kegiatan_usaha_lain_1 = pengajuan_.kegiatan_usaha_lain_1
			# kegiatan_usaha_lain_2 = ""
			# if pengajuan_.kegiatan_usaha_lain_2:
			# 	kegiatan_usaha_lain_2 = pengajuan_.kegiatan_usaha_lain_2
			kbli_list = pengajuan_.kegiatan_usaha_pokok.all()
			kbli_json = [k.as_json() for k in KBLI.objects.filter(id__in=kbli_list)]
			# print kbli_list
			# print kbli_json
			# komoditi_produk_pokok = ""
			# if pengajuan_.komoditi_produk_pokok:
			# 	komoditi_produk_pokok = pengajuan_.komoditi_produk_pokok
			# komoditi_produk_lain_1 = ""
			# if pengajuan_.komoditi_produk_lain_1:
			# 	komoditi_produk_lain_1 = pengajuan_.komoditi_produk_lain_1
			# komoditi_produk_lain_2 = ""
			# if pengajuan_.komoditi_produk_lain_2:
			# 	komoditi_produk_lain_2 = pengajuan_.komoditi_produk_lain_2
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

			data = {'success': True, 'pesan': 'Load data kegiatan perusahaan', 'data':{ 'kbli_json':kbli_json, 'omset_per_tahun': omset_per_tahun, 'total_aset': total_aset, 'jumlah_karyawan_wni': jumlah_karyawan_wni, 'jumlah_karyawan_wna': jumlah_karyawan_wna, 'kapasitas_mesin_terpasang': kapasitas_mesin_terpasang, 'satuan_kapasitas_mesin_terpasang': satuan_kapasitas_mesin_terpasang, 'kapasitas_produksi_per_tahun': kapasitas_produksi_per_tahun, 'satuan_kapasitas_produksi_per_tahun': satuan_kapasitas_produksi_per_tahun, 'presentase_kandungan_produk_lokal': presentase_kandungan_produk_lokal, 'presentase_kandungan_produk_import': presentase_kandungan_produk_import, 'jenis_pengecer': jenis_pengecer, 'kedudukan_kegiatan_usaha': kedudukan_kegiatan_usaha, 'jenis_perusahaan': jenis_perusahaan, 'modal_dasar': modal_dasar, 'modal_ditempatkan': modal_ditempatkan, 'modal_disetor': modal_disetor, 'banyaknya_saham': banyaknya_saham, 'nilai_nominal_per_saham': nilai_nominal_per_saham}}
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
				# print request.POST.get('id')
				i = IzinLain.objects.filter(id=request.POST.get('id')).last()
				izin_lain_form = IzinLainForm(request.POST, instance=i)
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
	data = []
	if pengajuan_id:
		i = IzinLain.objects.filter(pengajuan_izin_id=pengajuan_id)
		# if len(i) > 0:
			# data1 = {'success': True, 'pesan':'Berhasil'}
		data = [ob.as_json() for ob in i]
		response = HttpResponse(json.dumps(data), content_type="application/json")
	# 	else:
	# 		
	# 		data = {}
	# 		data = json.dumps(data)
	# 		response = HttpResponse(data)
	# else:
	# 	data = {}
	# 	data = json.dumps(data)
	# 	response = HttpResponse(data)
	return response

def edit_tdp_izin_lain(request, izin_lain_id):
	if izin_lain_id:
		try:
			i = IzinLain.objects.get(id=izin_lain_id)

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

def delete_tdp_izin_lain(request, izin_lain_id):
	if izin_lain_id:
		try:
			i = IzinLain.objects.get(id=izin_lain_id)
			i.delete()
			data = {'success': True, 'pesan': 'Data berhasil dihapus.'}
			data = json.dumps(data)
			response = HttpResponse(data)
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def pemegang_saham_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			try:
				pengajuan_ = PengajuanIzin.objects.get(id=request.COOKIES['id_pengajuan'])
				p = PemegangSaham.objects.filter(id=request.POST.get('id')).last()
				pemegang_saham_form = PemegangSahamForm(request.POST, instance=p)
				if pemegang_saham_form.is_valid():
					i = pemegang_saham_form.save(commit=False)
					i.pengajuan_izin_id = request.COOKIES['id_pengajuan']
					i.save()
					data = {'success': True, 'pesan': 'Data Pemegang Saham berhasil disimpan.'}
					data = json.dumps(data)
					response = HttpResponse(data)
				else:
					data = pemegang_saham_form.errors.as_json()
					response = HttpResponse(data)
			except ObjectDoesNotExist:
				data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
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

def load_pemegang_saham(request, pengajuan_id):
	data = []
	if pengajuan_id:
		i = PemegangSaham.objects.filter(pengajuan_izin_id=pengajuan_id)
		# if len(i) > 0:
			# data1 = {'success': True, 'pesan': 'Berhasil.'}
			# data1 = dict(success=True, pesan="berhasil.")
		data = [ob.as_json() for ob in i]
		response = HttpResponse(json.dumps(data), content_type="application/json")
	# 	else:
	# 		data = {'success': False, 'pesan':'Data tidak ditemukan.'}
	# 		data = json.dumps(data)
	# 		response = HttpResponse(data)
	# else:
	# 	data = {'success': False, 'pesan':'Data tidak ditemukan'}
	# 	data = json.dumps(data)
	# 	response = HttpResponse(data)
	return response


def edit_pemegang_saham(request, pemegang_saham_id):
	if pemegang_saham_id:
		try:
			i = PemegangSaham.objects.get(id=pemegang_saham_id)
			data = {'data':{'id':i.id, 'nama_lengkap':i.nama_lengkap, 'alamat':i.alamat, 'telephone':i.telephone, 'kewarganegaraan':i.kewarganegaraan, 'npwp':i.npwp, 'dimiliki':i.jumlah_saham_dimiliki, 'disetor':i.jumlah_saham_disetor}}
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

def delete_pemegang_saham(request, pemegang_saham_id):
	if pemegang_saham_id:
		try:
			i = PemegangSaham.objects.get(id=pemegang_saham_id)
			i.delete()
			data = {'success': True, 'pesan': 'Data berhasil dihapus.'}
			data = json.dumps(data)
			response = HttpResponse(data)
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def data_pimpinan_save(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			try:
				pengajuan_ = PengajuanIzin.objects.get(id=request.COOKIES['id_pengajuan'])
				p = DataPimpinan.objects.filter(id=request.POST.get('id')).last()
				data_pimpinan_form = DataPimpinanForm(request.POST, instance=p)
				if data_pimpinan_form.is_valid():
					i = data_pimpinan_form.save(commit=False)
					i.detil_tdp_id = request.COOKIES['id_pengajuan']
					i.save()
					data = {'success': True, 'pesan': 'Data Pemegang Saham berhasil disimpan.'}
					data = json.dumps(data)
					response = HttpResponse(data)
				else:
					data = data_pimpinan_form.errors.as_json()
					response = HttpResponse(data)
			except ObjectDoesNotExist:
				data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
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

def load_data_pimpinan(request, pengajuan_id):
	data = []
	if pengajuan_id:
		i = DataPimpinan.objects.filter(detil_tdp_id=pengajuan_id)
		# if len(i) > 0:
		data = [ob.as_json() for ob in i]
		response = HttpResponse(json.dumps(data), content_type="application/json")
	# 	else:
	# 		data = {'error': False, 'pesan':'Data tidak ditemukan'}
	# 		data = json.dumps(data)
	# 		response = HttpResponse(data)
	# else:
	# 	data = {'error': False, 'pesan':'Data tidak ditemukan'}
	# 	data = json.dumps(data)
	# 	response = HttpResponse(data)
	return response

def edit_data_pimpinan(request, data_pimpinan_id):
	if data_pimpinan_id:
		try:
			i = DataPimpinan.objects.get(id=data_pimpinan_id)
			tanggal_menduduki_jabatan_perusahaan_lain = ''
			if i.tanggal_menduduki_jabatan_perusahaan_lain:
				tanggal_menduduki_jabatan_perusahaan_lain = i.tanggal_menduduki_jabatan_perusahaan_lain.strftime('%d-%m-%Y')
			data = {'data':{'id':i.id, 'kedudukan': i.kedudukan.id, 'nama_lengkap':i.nama_lengkap, 'tempat_lahir': i.tempat_lahir, 'tanggal_lahir': i.tanggal_lahir.strftime('%d-%m-%Y'), 'alamat':i.alamat, 'telephone':i.telephone, 'hp':i.hp, 'email': i.email ,'kewarganegaraan':i.kewarganegaraan, 'tanggal_menduduki_jabatan': i.tanggal_menduduki_jabatan.strftime('%d-%m-%Y'),  'dimiliki':i.jumlah_saham_dimiliki, 'disetor':i.jumlah_saham_disetor, 'kedudukan_diperusahaan_lain': i.kedudukan_diperusahaan_lain, 'nama_perusahaan_lain': i.nama_perusahaan_lain, 'alamat_perusahaan_lain': i.alamat_perusahaan_lain, 'kode_pos_perusahaan_lain': i.kode_pos_perusahaan_lain, 'telepon_perusahaan_lain': i.telepon_perusahaan_lain, 'tanggal_menduduki_jabatan_perusahaan_lain': tanggal_menduduki_jabatan_perusahaan_lain}}
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

def delete_data_pimpinan(request, data_pimpinan_id):
	if data_pimpinan_id:
		try:
			i = DataPimpinan.objects.get(id=data_pimpinan_id)
			i.delete()
			data = {'success': True, 'pesan': 'Data berhasil dihapus.'}
			data = json.dumps(data)
			response = HttpResponse(data)
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def data_perusahaan_cabang_save(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_perusahaan' in request.COOKIES.keys():
				if request.COOKIES['id_perusahaan'] != '':
					try:
						perusahaan_ = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
						p = Perusahaan.objects.filter(id=request.POST.get('id')).last()
						perusahaan_cabang_form = PerusahaanCabangForm(request.POST, instance=p)
						if perusahaan_cabang_form.is_valid():
							i = perusahaan_cabang_form.save(commit=False)
							i.perusahaan_induk_id = perusahaan_.id
							i.npwp = None
							i.save()
							data = {'success': True, 'pesan': 'Data Perusahaan Cabang berhasil disimpan.'}
							data = json.dumps(data)
							response = HttpResponse(data)
						else:
							data = perusahaan_cabang_form.errors.as_json()
							response = HttpResponse(data)
					except ObjectDoesNotExist:
						data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
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
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def load_perusahaan_cabang(request, pengajuan_id):
	data = []
	if pengajuan_id:
		try:
			pengajuan_ = DetilTDP.objects.get(id=pengajuan_id)
			i = Perusahaan.objects.filter(perusahaan_induk_id=pengajuan_.perusahaan.id)
			# if len(i) > 0:
			data = [ob.as_json() for ob in i]
			
		except ObjectDoesNotExist:
			pass
		response = HttpResponse(json.dumps(data), content_type="application/json")
	return response

def edit_perusahaan_cabang(request, perusahaan_id):
	if perusahaan_id:
		try:
			perusahaan_ = Perusahaan.objects.get(id=perusahaan_id)
			data = {'success': True, 'data':{'id': perusahaan_.id, 'nama_perusahaan':perusahaan_.nama_perusahaan, 'alamat_perusahaan': perusahaan_.alamat_perusahaan, 'desa':perusahaan_.desa.id, 'kecamatan':perusahaan_.desa.kecamatan.id, 'kabupaten':perusahaan_.desa.kecamatan.kabupaten.id, 'provinsi': perusahaan_.desa.kecamatan.kabupaten.provinsi.id, 'kode_pos': perusahaan_.kode_pos, 'telepon':perusahaan_.telepon, 'fax':perusahaan_.fax, 'status_perusahaan':perusahaan_.status_perusahaan, 'kegiatan_usaha':perusahaan_.kegiatan_usaha, 'nomor_tdp':perusahaan_.nomor_tdp}}
			data = json.dumps(data)
			response = HttpResponse(data)
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan':'Data perusahaan tidak ada...!!!'}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'success': False, 'pesan':'Data perusahaan tidak ada...!!!'}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def delete_perusahaan_cabang(request, perusahaan_id):
	if perusahaan_id:
		try:
			i = Perusahaan.objects.get(id=perusahaan_id)
			i.delete()
			data = {'success': True, 'pesan': 'Data berhasil dihapus.'}
			data = json.dumps(data)
			response = HttpResponse(data)
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
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
							valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.jpeg', '.png']
							if not ext in valid_extensions:
								data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
								data = json.dumps(data)
								response = HttpResponse(data)
							else:
								try:
									p = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
									try:
										perusahaan_ = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
										berkas = form.save(commit=False)
										kode = request.POST.get('kode')
										if kode == 'Surat Keputusan':
											berkas.nama_berkas = "Surat Keputusan Pengesahan Badan Hukum "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "File Surat Keputusan Pengesahan Badan Hukum Dari Departemen Hukum Dari Menteri Kehakiman Dan Hak Asasi Manusia "+perusahaan_.npwp
										elif kode == 'Ijin Usaha':
											berkas.nama_berkas = "Ijin Usaha/Ijin Teknis "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "File Ijin Usaha/Ijin Teknis atau SK yang dipersamakan "+perusahaan_.npwp
										elif kode == 'Sertifikat Asli TDP':
											berkas.nama_berkas = "Sertifikat Asli TDP "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "Sertifikat Asli TDP "+perusahaan_.npwp
										elif kode == 'Neraca Perusahaan':
											berkas.nama_berkas = "Neraca Perusahaan "+p.perusahaan.nama_perusahaan
											berkas.keterangan = "Neraca Perusahaan "+perusahaan_.npwp
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

def tdp_upload_akta_legalitas(request):
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
							valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.jpeg', '.png']
							if not ext in valid_extensions:
								data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
								data = json.dumps(data)
								response = HttpResponse(data)
							else:
								try:
									jenis_legalitas = request.POST.get('jenis_legalitas')
									print jenis_legalitas
									p = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
									berkas = form.save(commit=False)
									if jenis_legalitas == '3':
										legalitas = p.perusahaan.legalitas_set.filter(jenis_legalitas_id=3).last()
										berkas.nama_berkas = "Akta Pengesahan Menteri dan HAM "+p.perusahaan.nama_perusahaan
										berkas.keterangan = "Akta Pengesahan Menteri dan HAM "+p.perusahaan.npwp
									elif jenis_legalitas == '4':
										legalitas = p.perusahaan.legalitas_set.filter(jenis_legalitas_id=4).last()
										berkas.nama_berkas = "Akta Persetujuan Menteri Hukum dan HAM Atas Perubahan Anggaran Dasar "+p.perusahaan.nama_perusahaan
										berkas.keterangan = "Akta Persetujuan Menteri Hukum dan HAM Atas Perubahan Anggaran Dasar "+p.perusahaan.npwp
									elif jenis_legalitas == '6':
										legalitas = p.perusahaan.legalitas_set.filter(jenis_legalitas_id=6).last()
										berkas.nama_berkas = "Akta Penerimaan Laporan Perubahan Anggaran Dasar "+p.perusahaan.nama_perusahaan
										berkas.keterangan = "Akta Penerimaan Laporan Perubahan Anggaran Dasar "+p.perusahaan.npwp
									elif jenis_legalitas == '7':
										legalitas = p.perusahaan.legalitas_set.filter(jenis_legalitas_id=7).last()
										berkas.nama_berkas = "Akta Penerimaan Pemberitahuan Direksi/Komisaris "+p.perusahaan.nama_perusahaan
										berkas.keterangan = "Akta Penerimaan Pemberitahuan Direksi/Komisaris "+p.perusahaan.npwp									
									
									if request.user.is_authenticated():
										berkas.created_by_id = request.user.id
									else:
										berkas.created_by_id = request.COOKIES['id_pemohon']
									berkas.save()

									legalitas.berkas = berkas
									legalitas.save()

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

def ajax_load_berkas_tdp(request, id_pengajuan):
	url_berkas = []
	id_elemen = []
	nm_berkas =[]
	id_berkas =[]
	if id_pengajuan:
		try:
			tdp = DetilTDP.objects.get(id=id_pengajuan)
			perusahaan_ = tdp.perusahaan
			berkas_ = tdp.berkas_tambahan.all()
			pemohon_ = tdp.pemohon
			legalitas_1 = perusahaan_.legalitas_set.filter(jenis_legalitas__id=1).last()
			legalitas_2 = perusahaan_.legalitas_set.filter(jenis_legalitas__id=2).last()
			legalitas_3 = perusahaan_.legalitas_set.filter(jenis_legalitas__id=3).last()
			legalitas_4 = perusahaan_.legalitas_set.filter(jenis_legalitas__id=4).last()
			legalitas_6 = perusahaan_.legalitas_set.filter(jenis_legalitas__id=6).last()
			legalitas_7 = perusahaan_.legalitas_set.filter(jenis_legalitas__id=7).last()

			if berkas_:
				neraca_perusahaan = berkas_.filter(keterangan='Neraca Perusahaan '+perusahaan_.npwp).last()
				if neraca_perusahaan:
					url_berkas.append(neraca_perusahaan.berkas.url)
					id_elemen.append('neraca_perusahaan')
					nm_berkas.append(neraca_perusahaan.nama_berkas)
					id_berkas.append(neraca_perusahaan.id)

				surat_keputusan = berkas_.filter(keterangan='File Surat Keputusan Pengesahan Badan Hukum Dari Departemen Hukum Dari Menteri Kehakiman Dan Hak Asasi Manusia '+perusahaan_.npwp).last()
				if surat_keputusan:
					url_berkas.append(surat_keputusan.berkas.url)
					id_elemen.append('surat_keputusan')
					nm_berkas.append(surat_keputusan.nama_berkas)
					id_berkas.append(surat_keputusan.id)

				ijin_usaha = berkas_.filter(keterangan='File Ijin Usaha/Ijin Teknis atau SK yang dipersamakan '+perusahaan_.npwp).last()
				if ijin_usaha:
					url_berkas.append(ijin_usaha.berkas.url)
					id_elemen.append('ijin_usaha')
					nm_berkas.append(ijin_usaha.nama_berkas)
					id_berkas.append(ijin_usaha.id)

				sertifikat_asli_tdp = berkas_.filter(keterangan='Sertifikat Asli TDP '+perusahaan_.npwp).last()
				if sertifikat_asli_tdp:
					url_berkas.append(sertifikat_asli_tdp.berkas.url)
					id_elemen.append('sertifikat_asli_tdp')
					nm_berkas.append(sertifikat_asli_tdp.nama_berkas)
					id_berkas.append(sertifikat_asli_tdp.id)

				pendukung = berkas_.filter(keterangan='pendukung '+perusahaan_.npwp).last()
				if pendukung:
					url_berkas.append(pendukung.berkas.url)
					id_elemen.append('berkas_tambahan')
					nm_berkas.append(pendukung.nama_berkas)
					id_berkas.append(pendukung.id)

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

			if legalitas_3:
				legalitas_3 = legalitas_3.berkas
				if legalitas_3:
					url_berkas.append(legalitas_3.berkas.url)
					id_elemen.append('akta_pengesahaan_menteri')
					nm_berkas.append(legalitas_3.nama_berkas)
					id_berkas.append(legalitas_3.id)

			if legalitas_4:
				legalitas_4 = legalitas_4.berkas
				if legalitas_4:
					url_berkas.append(legalitas_4.berkas.url)
					id_elemen.append('akta_persetujuan_menteri')
					nm_berkas.append(legalitas_4.nama_berkas)
					id_berkas.append(legalitas_4.id)

			if legalitas_6:
				legalitas_6 = legalitas_6.berkas
				if legalitas_6:
					url_berkas.append(legalitas_6.berkas.url)
					id_elemen.append('akta_penerimaan_laporan')
					nm_berkas.append(legalitas_6.nama_berkas)
					id_berkas.append(legalitas_6.id)

			if legalitas_7:
				legalitas_7 = legalitas_7.berkas
				if legalitas_7:
					url_berkas.append(legalitas_7.berkas.url)
					id_elemen.append('akta_penerimaan_pemberitahuan')
					nm_berkas.append(legalitas_7.nama_berkas)
					id_berkas.append(legalitas_7.id)

			nomor_ktp = request.COOKIES['nomor_ktp']
			if nomor_ktp:
				ktp_ = Berkas.objects.filter(nama_berkas="Berkas KTP Pemohon "+str(nomor_ktp)).last()
				if ktp_:
					url_berkas.append(ktp_.berkas.url)
					id_elemen.append('ktp')
					nm_berkas.append(ktp_.nama_berkas)
					id_berkas.append(ktp_.id)

			if perusahaan_:
				npwp_perusahaan = perusahaan_.berkas_npwp
				if npwp_perusahaan:
					url_berkas.append(npwp_perusahaan.berkas.url)
					id_elemen.append('npwp_perusahaan')
					nm_berkas.append(npwp_perusahaan.nama_berkas)
					id_berkas.append(npwp_perusahaan.id)

			data = {'success': True, 'pesan': 'Perusahaan Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': '' }
	response = HttpResponse(json.dumps(data))
	return response

def ajax_delete_berkas_tdp(request, id_berkas, kode):
	if id_berkas:
		if kode == 'npwp_perusahaan':
			p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
			p.berkas_npwp = None
			p.save()
		elif kode == 'ktp':
			n = NomorIdentitasPengguna.objects.filter(nomor = request.COOKIES['nomor_ktp'], jenis_identitas_id=1).last()
			n.berkas = None
			n.save()
		elif kode == 'akta_pendirian':
			p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
			legalitas_pendirian = p.legalitas_set.filter(~Q(jenis_legalitas__id=2)).last()
			legalitas_pendirian.berkas = None
			legalitas_pendirian.save()
		elif kode == 'akta_perubahan':
			p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
			legalitas_perubahan= p.legalitas_set.filter(jenis_legalitas__id=2).last()
			legalitas_perubahan.berkas = None
			legalitas_perubahan.save()
		elif kode == 'akta_pengesahaan_menteri':
			p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
			legalitas_perubahan= p.legalitas_set.filter(jenis_legalitas__id=3).last()
			legalitas_perubahan.berkas = None
			legalitas_perubahan.save()
		elif kode == 'akta_persetujuan_menteri':
			p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
			legalitas_perubahan= p.legalitas_set.filter(jenis_legalitas__id=4).last()
			legalitas_perubahan.berkas = None
			legalitas_perubahan.save()
		elif kode == 'akta_penerimaan_laporan':
			p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
			legalitas_perubahan= p.legalitas_set.filter(jenis_legalitas__id=6).last()
			legalitas_perubahan.berkas = None
			legalitas_perubahan.save()
		elif kode == 'akta_penerimaan_pemberitahuan':
			p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
			legalitas_perubahan= p.legalitas_set.filter(jenis_legalitas__id=7).last()
			legalitas_perubahan.berkas = None
			legalitas_perubahan.save()
		else:
			pass
		try:
			b = Berkas.objects.get(id=id_berkas)
			data = {'success': True, 'pesan': str(b)+" berhasil dihapus" }
			b.delete()
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': 'Berkas Tidak Ada' }
			
		response = HttpResponse(json.dumps(data))
		return response

def ajax_konfirmasi_tdp(request, pengajuan_id):
	if pengajuan_id:
		pengajuan_ = DetilTDP.objects.get(id=pengajuan_id)
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
				# print email_pemohon
					# email_pemohon = ""
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
			data_pemohon = {'pemohon': {'jenis_pengajuan': jenis_pengajuan, 'ktp_paspor': nomor_ktp+" / "+nomor_paspor, 'jenis_pemohon': jenis_pemohon, 'nama_lengkap_pemohon': nama_lengkap_pemohon, 'alamat_lengkap_pemohon': alamat_lengkap_pemohon, 'telephone_pemohon': telephone_pemohon, 'hp_pemohon': hp_pemohon, 'email_pemohon': email_pemohon, 'kewarganegaraan_pemohon': kewarganegaraan_pemohon, 'pekerjaan_pemohon': pekerjaan_pemohon}}
			if perusahaan_:
				npwp_perusahaan = perusahaan_.npwp
				nama_perusahaan = perusahaan_.nama_perusahaan
				alamat_lengkap_perusahaan = str(perusahaan_.alamat_perusahaan)+", Ds. "+str(perusahaan_.desa.nama_desa)+", Kec."+str(perusahaan_.desa.kecamatan.nama_kecamatan)+", "+str(perusahaan_.desa.kecamatan.kabupaten.nama_kabupaten)
				kode_pos_perusahaan = perusahaan_.kode_pos
				telephone_perusahaan = perusahaan_.telepon
				fax_perusahaan = perusahaan_.fax
				email_perusahaan = perusahaan_.email
			data_perusahaan = {'perusahaan': {'npwp_perusahaan':npwp_perusahaan, 'nama_perusahaan':nama_perusahaan, 'alamat_lengkap_perusahaan':alamat_lengkap_perusahaan, 'kode_pos_perusahaan':kode_pos_perusahaan, 'telephone_perusahaan':telephone_perusahaan, 'fax_perusahaan':fax_perusahaan, 'email_perusahaan':email_perusahaan}}
			# #### data umum perusahaan ####
			jenis_badan_usaha = pengajuan_.jenis_badan_usaha.jenis_badan_usaha
			status_perusahaan = pengajuan_.status_perusahaan.status_perusahaan
			jumlah_bank = pengajuan_.jumlah_bank
			nasabah_utama_bank_1 = pengajuan_.nasabah_utama_bank_1
			nasabah_utama_bank_2 = pengajuan_.nasabah_utama_bank_2
			jenis_penanaman_modal = pengajuan_.jenis_penanaman_modal.jenis_penanaman_modal
			tanggal_pendirian = pengajuan_.tanggal_pendirian.strftime('%d-%m-%Y')
			tanggal_mulai_kegiatan = ""
			if pengajuan_.tanggal_mulai_kegiatan:
				tanggal_mulai_kegiatan = pengajuan_.tanggal_mulai_kegiatan.strftime('%d-%m-%Y')
			jangka_waktu_berdiri = pengajuan_.jangka_waktu_berdiri
			bentuk_kerjasama = ""
			if pengajuan_.bentuk_kerjasama:
				bentuk_kerjasama = pengajuan_.bentuk_kerjasama.bentuk_kerjasama
			# bagi memiliki unit produksi
			alamat_lengkap_unit_produksi = ""
			if pengajuan_.alamat_unit_produksi:
				if pengajuan_.desa_unit_produksi:
					alamat_lengkap_unit_produksi = str(pengajuan_.alamat_unit_produksi)+", Ds. "+str(pengajuan_.desa_unit_produksi.nama_desa)+", Kec."+str(pengajuan_.desa_unit_produksi.kecamatan.nama_kecamatan)+", "+str(pengajuan_.desa_unit_produksi.kecamatan.kabupaten.nama_kabupaten)
			# ++++++++++++++
			merek_dagang = pengajuan_.merek_dagang
			no_merek_dagang = pengajuan_.no_merek_dagang
			pemegang_hak_cipta = pengajuan_.pemegang_hak_cipta
			no_hak_cipta = pengajuan_.no_hak_cipta
			pemegang_hak_paten = pengajuan_.pemegang_hak_paten
			no_hak_paten = pengajuan_.no_hak_paten

			data_umum_perusahaan = {'dup': {'jenis_badan_usaha':jenis_badan_usaha, 'status_perusahaan':status_perusahaan, 'jumlah_bank':jumlah_bank, 'nasabah_utama_bank_1':nasabah_utama_bank_1, 'nasabah_utama_bank_2':nasabah_utama_bank_2, 'jenis_penanaman_modal':jenis_penanaman_modal, 'tanggal_pendirian':tanggal_pendirian, 'tanggal_mulai_kegiatan':tanggal_mulai_kegiatan, 'jangka_waktu_berdiri':jangka_waktu_berdiri, 'bentuk_kerjasama':bentuk_kerjasama, 'alamat_lengkap_unit_produksi':alamat_lengkap_unit_produksi, 'merek_dagang':merek_dagang, 'no_merek_dagang':no_merek_dagang,'pemegang_hak_cipta':pemegang_hak_cipta, 'no_hak_cipta':no_hak_cipta, 'pemegang_hak_paten':pemegang_hak_paten, 'no_hak_paten':no_hak_paten}}
			# data_umum_perusahaan = {'dup': {'jenis_badan_usaha':jenis_badan_usaha, 'status_perusahaan':status_perusahaan}}
			# #### end data umum perusahaan ####

			# ###### data kegiatan perusahaan ######
			# kegiatan_usaha_pokok = pengajuan_.kegiatan_usaha_pokok
			# kegiatan_usaha_lain_1 = pengajuan_.kegiatan_usaha_lain_1
			# kegiatan_usaha_lain_2 = pengajuan_.kegiatan_usaha_lain_2
			kbli_list = []
			if pengajuan_.kegiatan_usaha_pokok:
				kbli_list = pengajuan_.kegiatan_usaha_pokok.all()
				kbli_json = [k.as_json() for k in KBLI.objects.filter(id__in=kbli_list)]

			# komoditi_produk_pokok = pengajuan_.komoditi_produk_pokok
			# komoditi_produk_lain_1 = pengajuan_.komoditi_produk_lain_1
			# komoditi_produk_lain_2 = pengajuan_.komoditi_produk_lain_2
			omset_per_tahun = pengajuan_.omset_per_tahun
			total_aset = pengajuan_.total_aset
			jumlah_karyawan_wni = pengajuan_.jumlah_karyawan_wni
			jumlah_karyawan_wna = pengajuan_.jumlah_karyawan_wna
			total_karyawan = jumlah_karyawan_wni+jumlah_karyawan_wna
			kapasitas_mesin_terpasang_ = ""
			if pengajuan_.kapasitas_mesin_terpasang:
				kapasitas_mesin_terpasang_ = str(int(pengajuan_.kapasitas_mesin_terpasang))
			satuan_kapasitas_mesin_terpasang_ = ""
			if pengajuan_.satuan_kapasitas_mesin_terpasang:
				satuan_kapasitas_mesin_terpasang_ = str(pengajuan_.satuan_kapasitas_mesin_terpasang)
			kapasitas_mesin_terpasang = kapasitas_mesin_terpasang_+", satuan: "+satuan_kapasitas_mesin_terpasang_
			kapasitas_produksi_per_tahun_ = ""
			if pengajuan_.kapasitas_produksi_per_tahun:
				kapasitas_produksi_per_tahun_ = str(int(pengajuan_.kapasitas_produksi_per_tahun))
			satuan_kapasitas_produksi_per_tahun_ = ""
			if pengajuan_.satuan_kapasitas_produksi_per_tahun:
				satuan_kapasitas_produksi_per_tahun_ = str(pengajuan_.satuan_kapasitas_produksi_per_tahun)
			kapasitas_produksi_per_tahun = kapasitas_produksi_per_tahun_+", satuan: "+satuan_kapasitas_produksi_per_tahun_
			presentase_kandungan_produk_lokal = ""
			if pengajuan_.presentase_kandungan_produk_lokal:
				presentase_kandungan_produk_lokal = int(pengajuan_.presentase_kandungan_produk_lokal)
			presentase_kandungan_produk_import = ""
			if pengajuan_.presentase_kandungan_produk_import:
				presentase_kandungan_produk_import = int(pengajuan_.presentase_kandungan_produk_import)
			jenis_pengecer = ""
			if pengajuan_.jenis_pengecer:
				jenis_pengecer = pengajuan_.jenis_pengecer.jenis_pengecer
			jenis_perusahaan = ""
			if pengajuan_.jenis_perusahaan:
				jenis_perusahaan = pengajuan_.jenis_perusahaan.jenis_perusahaan
			kedudukan_kegiatan_usaha = ""
			if pengajuan_.kedudukan_kegiatan_usaha:
				kedudukan_kegiatan_usaha = pengajuan_.kedudukan_kegiatan_usaha.kedudukan_kegiatan_usaha

			data_kegiatan_perusahaan = {'dkp': { 'omset_per_tahun':omset_per_tahun, 'total_aset':total_aset, 'jumlah_karyawan_wni':jumlah_karyawan_wni, 'jumlah_karyawan_wna':jumlah_karyawan_wna, 'total_karyawan':total_karyawan, 'kapasitas_mesin_terpasang':kapasitas_mesin_terpasang, 'kapasitas_produksi_per_tahun': kapasitas_produksi_per_tahun, 'presentase_kandungan_produk_lokal':presentase_kandungan_produk_lokal, 'presentase_kandungan_produk_import': presentase_kandungan_produk_import, 'jenis_pengecer':jenis_pengecer, 'jenis_perusahaan':jenis_perusahaan, 'kedudukan_kegiatan_usaha':kedudukan_kegiatan_usaha, 'kbli_json':kbli_json}}

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
			data_rincian_perusahaan = {'rincian':{'modal_dasar':modal_dasar, 'modal_ditempatkan':modal_ditempatkan, 'modal_disetor':modal_disetor, 'banyaknya_saham':banyaknya_saham, 'nilai_nominal_per_saham':nilai_nominal_per_saham}}
			# ###### end data kegiatan perusahaan ######
			data = {'success': True, 'pesan': 'load konfirmasi berhasil', },data_pemohon,data_perusahaan,data_umum_perusahaan,data_kegiatan_perusahaan,data_rincian_perusahaan,data_kuasa
			response = HttpResponse(json.dumps(data))
			return response

def load_legalitas_perusahaan_tdp(request, perusahaan_id):
	data = []
	if perusahaan_id:

		i = Legalitas.objects.filter(perusahaan_id=perusahaan_id)
		# if len(i) > 0:
			# data1 = {'success': True, 'pesan': 'Berhasil.'}
			# data1 = dict(success=True, pesan="berhasil.")
		data = [ob.as_json() for ob in i]
		response = HttpResponse(json.dumps(data), content_type="application/json")
	# 	else:
	# 		data = {'success': False, 'pesan':'Data tidak ditemukan.'}
	# 		data = json.dumps(data)
	# 		response = HttpResponse(data)
	# else:
	# 	data = {'success': False, 'pesan':'Data tidak ditemukan'}
	# 	data = json.dumps(data)
	# 	response = HttpResponse(data)
	return response

def tdp_pt_done(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
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
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response