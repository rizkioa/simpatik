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
				try:
					pengajuan_obj = TokoObat.objects.get(id=request.COOKIES.get('id_pengajuan'))
					pengajuan_obj.nama_toko_obat = request.POST.get("nama_toko_obat")
					pengajuan_obj.nama_ttk_penanggung_jawab = request.POST.get("nama_ttk_penanggung_jawab")
					pengajuan_obj.alamat_ttk = request.POST.get("alamat_ttk")
					pengajuan_obj.alamat_tempat_usaha = request.POST.get("alamat_tempat_usaha")
					pengajuan_obj.save()
					data = {'success':True, 'pesan': 'Data izin toko obat berhasil disimpan.'}
				except TokoObat.ObjectDoesNotExist:
					data = {'success': False, 'pesan': 'Proses simpaan data izin toko obat terjadi kesalahan.', 'data': ""}
				# if pengajuan_obj:
				# 	form_ = TokoObatForm(request.POST, instance=pengajuan_obj)
				# 	if form_.is_valid():
				# 		p = form_.save(commit=False)
				# 		p.save()
				# 		data = {'success': True, 'pesan': 'Data Izin Apotek berhasil tersimpan.'}
				# 	else:
				# 		data_error = form_apotek.errors.as_json()
				# 		data = {'success': False, 'pesan': 'Data Izin Apotek gagal.', 'data': data_error}
	return HttpResponse(json.dumps(data))


def upload_berkas_toko_obat(request):
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
									p = TokoObat.objects.get(id=request.COOKIES.get('id_pengajuan'))
									berkas = form.save(commit=False)
									kode = request.POST.get('kode')
									if kode == 'Ijazah STRTTK':
										berkas.nama_berkas = "Ijazah STRTTK "+p.nama_toko_obat
										berkas.keterangan = "Ijazah STRTTK "+p.nama_toko_obat
									elif kode == 'Denah Lokasi':
										berkas.nama_berkas = "Denah Lokasi "+p.nama_toko_obat
										berkas.keterangan = "Denah Lokasi "+p.nama_toko_obat
									elif kode == 'Denah Bangunan':
										berkas.nama_berkas = "Denah Bangunan "+p.nama_toko_obat
										berkas.keterangan = "Denah Bangunan "+p.nama_toko_obat
									elif kode == 'KTP':
										berkas.nama_berkas = "KTP "+p.pemohon.nama_lengkap
										berkas.keterangan = "KTP "+p.pemohon.nama_lengkap
								except TokoObat.ObjectDoesNotExist:
									pass

