import json, os, datetime
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from izin.models import DetilIUA, DetilTrayek

def load_izin_iua(request):
	nomor_izin_iua = request.POST.get('nomor_izin_iua')
	if nomor_izin_iua and nomor_izin_iua is not None:
		data = {'success': False, 'pesan': 'Data tidak ditemukan'}
		detil_iua = DetilIUA.objects.filter(no_izin=nomor_izin_iua).last()
		if detil_iua and detil_iua is not None:
			pengajuan_obj = DetilTrayek.objects.filter(id=request.COOKIES['id_pengajuan']).last()
			# print pengajuan_obj
			detil_iua_no_izin = detil_iua.no_izin
			data = {'success': True, 'pesan': 'No Izin Terdaftar.', 'data': detil_iua}

		data = json.dumps(data)
		response = HttpResponse(data)
		return response
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Nomor Izin Gangguan tidak ditemukan'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response