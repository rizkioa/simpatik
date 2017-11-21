import os
import json
import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from izin_dinkes.forms import ApotekForm, TokoObatForm
from izin_dinkes.models import Apotek, TokoObat
from izin.izin_forms import BerkasForm

def save_izin_apotek(request):
	data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
	data = json.dumps(data)
	response = HttpResponse(data)
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				pengajuan_obj = Apotek.objects.filter(id=request.COOKIES['id_pengajuan']).last()
				form_apotek = ApotekForm(request.POST, instance=pengajuan_obj)
				if form_apotek.is_valid():
					p = form_apotek.save(commit=False)
					p.save()
					data = {'success': True, 'pesan': 'Data Izin Apotek berhasil tersimpan.'}
					response = HttpResponse(json.dumps(data))
				else:
					data = form_apotek.errors.as_json()
					data = {'success': False, 'pesan': 'Data Izin Apotek gagal.', 'data': data}
					response = HttpResponse(json.dumps(data))
	return response

def save_izin_toko_obat(request):
	data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES.get('id_pengajuan') != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				pengajuan_obj = TokoObat.objects.filter(id=request.COOKIES.get('id_pengajuan')).last()
				if pengajuan_obj:
					form_ = TokoObatForm(request.POST, instance=pengajuan_obj)
					if form_.is_valid():
						p = form_.save(commit=False)
						p.save()
						data = {'success': True, 'pesan': 'Data Izin Apotek berhasil tersimpan.'}
					else:
						data_error = form_apotek.errors.as_json()
						data = {'success': False, 'pesan': 'Data Izin Apotek gagal.', 'data': data_error}
	return HttpResponse(json.dumps(data))

def upload_berkas(request):
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
									p = Apotek.objects.get(id=request.COOKIES['id_pengajuan'])
									berkas = form.save(commit=False)
									kode = request.POST.get('kode')
									if kode == 'Ijazah Apoteker':
										berkas.nama_berkas = "Ijazah Apoteker "+p.nama_apotek
										berkas.keterangan = "Ijazah Apoteker "+p.npwp
									elif kode == 'STRA Apoteker':
										berkas.nama_berkas = "STRA Apoteker "+p.nama_apotek
										berkas.keterangan = "STRA Apoteker "+p.npwp
									elif kode == 'Surat Rekomendasi IAI':
										berkas.nama_berkas = "Surat Rekomendasi IAI "+p.nama_apotek
										berkas.keterangan = "Surat Rekomendasi IAI "+p.npwp
									elif kode == 'Izin Gangguan':
										berkas.nama_berkas = "Izin Gangguan "+p.nama_apotek
										berkas.keterangan = "Izin Gangguan "+p.npwp
									elif kode == 'KTP':
										berkas.nama_berkas = "NO KTP "+p.nama_apotek
										berkas.keterangan = "NO KTP "+p.npwp
									elif kode == 'Denah Lokasi':
										berkas.nama_berkas = "Denah Lokasi "+p.nama_apotek
										berkas.keterangan = "Denah Lokasi "+p.npwp
									elif kode == 'Denah Bangunan':
										berkas.nama_berkas = "Denah Bangunan "+p.nama_apotek
										berkas.keterangan = "Denah Bangunan "+p.npwp
									elif kode == 'Status Bangunan':
										berkas.nama_berkas = "Status Bangunan "+p.nama_apotek
										berkas.keterangan = "Status Bangunan "+p.npwp
									elif kode == 'IMB dan Izin Gangguan':
										berkas.nama_berkas = "IMB dan Izin Gangguan "+p.nama_apotek
										berkas.keterangan = "IMB dan Izin Gangguan "+p.npwp
									elif kode == 'Ijazah STRTTK':
										berkas.nama_berkas = "Ijazah STRTTK "+p.nama_apotek
										berkas.keterangan = "Ijazah STRTTK "+p.npwp
									elif kode == 'Daftar Tenaga Teknis':
										berkas.nama_berkas = "Daftar Tenaga Teknis "+p.nama_apotek
										berkas.keterangan = "Daftar Tenaga Teknis "+p.npwp
									elif kode == 'Daftar Perlengkapan Apotek':
										berkas.nama_berkas = "Daftar Perlengkapan Apotek "+p.nama_apotek
										berkas.keterangan = "Daftar Perlengkapan Apotek "+p.npwp
									elif kode == 'Surat Izin Atasan':
										berkas.nama_berkas = "Surat Izin Atasan "+p.nama_apotek
										berkas.keterangan = "Surat Izin Atasan "+p.npwp
									elif kode == 'Akta Perjanjian Kerjasama Apoteker':
										berkas.nama_berkas = "Akta Perjanjian Kerjasama Apoteker "+p.nama_apotek
										berkas.keterangan = "Akta Perjanjian Kerjasama Apoteker "+p.npwp
									elif kode == 'Surat Pernyataan Apoteker (Peraturan)':
										berkas.nama_berkas = "Surat Pernyataan Apoteker (Peraturan) "+p.nama_apotek
										berkas.keterangan = "Surat Pernyataan Apoteker (Peraturan) "+p.npwp
									elif kode == 'Surat Pernyataan Pemilik (Peraturan)':
										berkas.nama_berkas = "Surat Pernyataan Pemilik (Peraturan) "+p.nama_apotek
										berkas.keterangan = "Surat Pernyataan Pemilik (Peraturan) "+p.npwp
									elif kode == 'SIA':
										berkas.nama_berkas = "SIA "+p.nama_apotek
										berkas.keterangan = "SIA "+p.npwp
									elif kode == 'SIPA':
										berkas.nama_berkas = "SIPA "+p.nama_apotek
										berkas.keterangan = "SIPA "+p.npwp
									elif kode == 'SIPTTK(AA)':
										berkas.nama_berkas = "SIPTTK(AA) "+p.nama_apotek
										berkas.keterangan = "SIPTTK(AA) "+p.npwp
									elif kode == 'Surat Pernyataan Pemilik':
										berkas.nama_berkas = "Surat Pernyataan Pemilik "+p.nama_apotek
										berkas.keterangan = "Surat Pernyataan Pemilik "+p.npwp
									elif kode == 'Surat Pernyataan Apoteker':
										berkas.nama_berkas = "Surat Pernyataan Apoteker "+p.nama_apotek
										berkas.keterangan = "Surat Pernyataan Apoteker "+p.npwp
									if request.user.is_authenticated():
										berkas.created_by_id = request.user.id
									else:
										berkas.created_by_id = request.COOKIES['id_pemohon']
									berkas.save()
									p.berkas_terkait_izin.add(berkas)

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

def apotek_upload_dokumen_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': [] }
	return HttpResponse(json.dumps(data))

def ajax_load_berkas_apotek(request, id_pengajuan):
	url_berkas = []
	id_elemen = []
	nm_berkas =[]
	id_berkas =[]
	if id_pengajuan:
		try:
			apotek = Apotek.objects.get(id=id_pengajuan)
			npwp = apotek.npwp
			berkas_ = apotek.berkas_terkait_izin.all()
			pemohon_ = apotek.pemohon

			if berkas_:
				ijazah_apoteker = berkas_.filter(keterangan='Ijazah Apoteker '+npwp).last()
				if ijazah_apoteker:
					url_berkas.append(ijazah_apoteker.berkas.url)
					id_elemen.append('ijazah_apoteker')
					nm_berkas.append(ijazah_apoteker.nama_berkas)
					id_berkas.append(ijazah_apoteker.id)
					apotek.berkas_terkait_izin.add(ijazah_apoteker)

				stra_apoteker = berkas_.filter(keterangan='STRA Apoteker '+npwp).last()
				if stra_apoteker:
					url_berkas.append(stra_apoteker.berkas.url)
					id_elemen.append('ijazah_apoteker')
					nm_berkas.append(stra_apoteker.nama_berkas)
					id_berkas.append(stra_apoteker.id)
					apotek.berkas_terkait_izin.add(stra_apoteker)

				rekom_iai = berkas_.filter(keterangan='Surat Rekomendasi IAI '+npwp).last()
				if rekom_iai:
					url_berkas.append(rekom_iai.berkas.url)
					id_elemen.append('rekom_iai')
					nm_berkas.append(rekom_iai.nama_berkas)
					id_berkas.append(rekom_iai.id)
					apotek.berkas_terkait_izin.add(rekom_iai)

				ktp = berkas_.filter(keterangan='KTP '+npwp).last()
				if ktp:
					url_berkas.append(ktp.berkas.url)
					id_elemen.append('ktp')
					nm_berkas.append(ktp.nama_berkas)
					id_berkas.append(ktp.id)
					apotek.berkas_terkait_izin.add(ktp)

				denah_lokasi = berkas_.filter(keterangan='Denah Lokasi '+npwp).last()
				if denah_lokasi:
					url_berkas.append(denah_lokasi.berkas.url)
					id_elemen.append('denah_lokasi')
					nm_berkas.append(denah_lokasi.nama_berkas)
					id_berkas.append(denah_lokasi.id)
					apotek.berkas_terkait_izin.add(denah_lokasi)

				denah_bangunan = berkas_.filter(keterangan='Denah Bangunan '+npwp).last()
				if denah_bangunan:
					url_berkas.append(denah_bangunan.berkas.url)
					id_elemen.append('denah_bangunan')
					nm_berkas.append(denah_bangunan.nama_berkas)
					id_berkas.append(denah_bangunan.id)
					apotek.berkas_terkait_izin.add(denah_bangunan)

				status_bangunan = berkas_.filter(keterangan='Status Bangunan '+npwp).last()
				if status_bangunan:
					url_berkas.append(status_bangunan.berkas.url)
					id_elemen.append('status_bangunan')
					nm_berkas.append(status_bangunan.nama_berkas)
					id_berkas.append(status_bangunan.id)
					apotek.berkas_terkait_izin.add(status_bangunan)

				izin_gangguan = berkas_.filter(keterangan='IMB dan Izin Gangguan '+npwp).last()
				if izin_gangguan:
					url_berkas.append(izin_gangguan.berkas.url)
					id_elemen.append('izin_gangguan')
					nm_berkas.append(izin_gangguan.nama_berkas)
					id_berkas.append(izin_gangguan.id)
					apotek.berkas_terkait_izin.add(izin_gangguan)

				ijazah_strttk = berkas_.filter(keterangan='Ijazah STRTTK '+npwp).last()
				if ijazah_strttk:
					url_berkas.append(ijazah_strttk.berkas.url)
					id_elemen.append('ijazah_strttk')
					nm_berkas.append(ijazah_strttk.nama_berkas)
					id_berkas.append(ijazah_strttk.id)
					apotek.berkas_terkait_izin.add(ijazah_strttk)

				daftar_tenaga_teknis = berkas_.filter(keterangan='Ijazah STRTTK '+npwp).last()
				if daftar_tenaga_teknis:
					url_berkas.append(daftar_tenaga_teknis.berkas.url)
					id_elemen.append('daftar_tenaga_teknis')
					nm_berkas.append(daftar_tenaga_teknis.nama_berkas)
					id_berkas.append(daftar_tenaga_teknis.id)
					apotek.berkas_terkait_izin.add(daftar_tenaga_teknis)

				daftar_tenaga_teknis = berkas_.filter(keterangan='Daftar Tenaga Teknis '+npwp).last()
				if daftar_tenaga_teknis:
					url_berkas.append(daftar_tenaga_teknis.berkas.url)
					id_elemen.append('daftar_tenaga_teknis')
					nm_berkas.append(daftar_tenaga_teknis.nama_berkas)
					id_berkas.append(daftar_tenaga_teknis.id)
					apotek.berkas_terkait_izin.add(daftar_tenaga_teknis)

				alat_perlengkapan_apotek = berkas_.filter(keterangan='Daftar Perlengkapan Apotek '+npwp).last()
				if alat_perlengkapan_apotek:
					url_berkas.append(alat_perlengkapan_apotek.berkas.url)
					id_elemen.append('alat_perlengkapan_apotek')
					nm_berkas.append(alat_perlengkapan_apotek.nama_berkas)
					id_berkas.append(alat_perlengkapan_apotek.id)
					apotek.berkas_terkait_izin.add(alat_perlengkapan_apotek)

				izin_atasan = berkas_.filter(keterangan='Surat Izin Atasan '+npwp).last()
				if izin_atasan:
					url_berkas.append(izin_atasan.berkas.url)
					id_elemen.append('izin_atasan')
					nm_berkas.append(izin_atasan.nama_berkas)
					id_berkas.append(izin_atasan.id)
					apotek.berkas_terkait_izin.add(izin_atasan)

				perjanjian_apoteker = berkas_.filter(keterangan='Akta Perjanjian Kerjasama Apoteker '+npwp).last()
				if perjanjian_apoteker:
					url_berkas.append(perjanjian_apoteker.berkas.url)
					id_elemen.append('perjanjian_apoteker')
					nm_berkas.append(perjanjian_apoteker.nama_berkas)
					id_berkas.append(perjanjian_apoteker.id)
					apotek.berkas_terkait_izin.add(perjanjian_apoteker)

				pernyataan_peraturan_apoteker = berkas_.filter(keterangan='Surat Pernyataan Apoteker (Peraturan) '+npwp).last()
				if pernyataan_peraturan_apoteker:
					url_berkas.append(pernyataan_peraturan_apoteker.berkas.url)
					id_elemen.append('pernyataan_peraturan_apoteker')
					nm_berkas.append(pernyataan_peraturan_apoteker.nama_berkas)
					id_berkas.append(pernyataan_peraturan_apoteker.id)
					apotek.berkas_terkait_izin.add(pernyataan_peraturan_apoteker)

				sia = berkas_.filter(keterangan='SIA '+npwp).last()
				if sia:
					url_berkas.append(sia.berkas.url)
					id_elemen.append('sia')
					nm_berkas.append(sia.nama_berkas)
					id_berkas.append(sia.id)
					apotek.berkas_terkait_izin.add(sia)

				sipa = berkas_.filter(keterangan='SIPA '+npwp).last()
				if sipa:
					url_berkas.append(sipa.berkas.url)
					id_elemen.append('sipa')
					nm_berkas.append(sipa.nama_berkas)
					id_berkas.append(sipa.id)
					apotek.berkas_terkait_izin.add(sipa)

				sipttk = berkas_.filter(keterangan='SIPTTK(AA) '+npwp).last()
				if sipttk:
					url_berkas.append(sipttk.berkas.url)
					id_elemen.append('sipttk')
					nm_berkas.append(sipttk.nama_berkas)
					id_berkas.append(sipttk.id)
					apotek.berkas_terkait_izin.add(sipttk)

				pernyataan_pemilik = berkas_.filter(keterangan='Surat Pernyataan Pemilik '+npwp).last()
				if pernyataan_pemilik:
					url_berkas.append(pernyataan_pemilik.berkas.url)
					id_elemen.append('pernyataan_pemilik')
					nm_berkas.append(pernyataan_pemilik.nama_berkas)
					id_berkas.append(pernyataan_pemilik.id)
					apotek.berkas_terkait_izin.add(pernyataan_pemilik)
				
				pernyataan_apoteker = berkas_.filter(keterangan='Surat Pernyataan Apoteker '+npwp).last()
				if pernyataan_apoteker:
					url_berkas.append(pernyataan_apoteker.berkas.url)
					id_elemen.append('pernyataan_apoteker')
					nm_berkas.append(pernyataan_apoteker.nama_berkas)
					id_berkas.append(pernyataan_apoteker.id)
					apotek.berkas_terkait_izin.add(pernyataan_apoteker)

			data = {'success': True, 'pesan': 'Sukses.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': '' }
	response = HttpResponse(json.dumps(data))
	return response
