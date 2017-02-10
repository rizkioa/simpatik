import os, json, datetime
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from izin.models import DetilTDUP, BidangUsahaPariwisata, SubJenisBidangUsaha

def tdup_data_usaha_pariwisata(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				pengajuan = DetilTDUP.objects.get(id=request.COOKIES['id_pengajuan'])
				bidang_usaha_list = request.POST.getlist('bidang_usaha_pariwisata')
				sub_jenis_bidang_usaha_list = request.POST.getlist('sub_jenis_bidang_usaha')
				# save many to many bidang usaha pariwisata
				for bidang_usaha in bidang_usaha_list:
					bidang_usaha_obj = BidangUsahaPariwisata.objects.get(id=bidang_usaha)
					pengajuan.bidang_usaha_pariwisata.add(kbli_obj)
				for sub_jenis_bidang_usaha in sub_jenis_bidang_usaha_list:
					sub_jenis_bidang_usaha_obj = SubJenisBidangUsaha.objects.get(id=sub_jenis_bidang_usaha)
					pengajuan.sub_jenis_bidang_usaha.add(sub_jenis_bidang_usaha_obj)

				pengajuan.save()