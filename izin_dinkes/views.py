import os
import json
import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from izin_dinkes.forms import ApotekForm, TokoObatForm
from izin_dinkes.models import Apotek, TokoObat

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
