from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin import site
from functools import wraps
from django.views.decorators.cache import cache_page
from django.utils.decorators import available_attrs
from django.core.exceptions import ObjectDoesNotExist

from izin.izin_forms import PengajuanReklameForm
from django.template import RequestContext, loader
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.db.models import Q
from datetime import datetime
from django.conf import settings
from django.views import generic
import base64
import time
import json
import os
import urllib

from master.models import Negara, Kecamatan, JenisPemohon,JenisReklame,Berkas,ParameterBangunan
from izin.models import JenisIzin, Syarat, KelompokJenisIzin, JenisPermohonanIzin,Riwayat
from izin.models import PengajuanIzin, DetilHuller,Pemohon,MesinHuller,MesinPerusahaan
from izin.utils import STATUS_HAK_TANAH
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna
from izin.izin_forms import UploadBerkasPendukungForm,DetilHullerForm,MesinHullerForm,MesinPerusahaanForm

def detil_huller_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilHuller.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			detil_huller = DetilHullerForm(request.POST, instance=pengajuan_)
			if detil_huller.is_valid():
				pengajuan_.perusahaan_id  = request.COOKIES['id_perusahaan']
				pengajuan_.save()
				data = {'success': True,
						'pesan': 'Data Reklame berhasil disimpan. Proses Selanjutnya.',
						'data': ['']}
				data = json.dumps(data)
				response = HttpResponse(json.dumps(data))
			else:
				data = detil_huller.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response

def mesin_perusahaan_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			nama_mesin = request.POST.get('nama_mesin')
			mesin_huller = MesinHuller.objects.get(mesin_huller=nama_mesin)
			detilhuller = DetilHuller.objects.get(id=request.COOKIES['id_pengajuan'])
			try:
				p = MesinPerusahaan.objects.get(mesin_huller_id=mesin_huller.id) 
				mesin_perusahaan = MesinPerusahaanForm(request.POST, instance=p)
			except ObjectDoesNotExist:
				mesin_perusahaan = MesinPerusahaanForm(request.POST)
			if request.method == 'POST':
				if mesin_perusahaan.is_valid():
					p = mesin_perusahaan.save(commit=False)
					p.mesin_huller = mesin_huller
					p.detil_huller = detilhuller
					p.save()
					data = {'success': True,
							'pesan': 'Data Mesin Perusahaan berhasil disimpan. Proses Selanjutnya.',
							'data': ['']}
					data = json.dumps(data)
					response = HttpResponse(json.dumps(data))
				else:
					data = mesin_perusahaan.errors.as_json()
			else:
				mesin_perusahaan = MesinPerusahaanForm()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response

def load_konfirmasi_detilhuller(request,id_pengajuan):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
      pengajuan_ = DetilHuller.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
      pemilik_badan_usaha = pengajuan_.pemilik_badan_usaha
      pengusaha_badan_usaha = pengajuan_.pengusaha_badan_usaha

      data = {'success': True,
          'data': [
          {'pemilik_badan_usaha': pemilik_badan_usaha},
          {'pengusaha_badan_usaha': pengusaha_badan_usaha}]}
      response = HttpResponse(json.dumps(data))
    else:
      data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
      data = json.dumps(data)
      response = HttpResponse(data)
  else:
    data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
    data = json.dumps(data)
    response = HttpResponse(data)
  return response

def detilhuller_upload_berkas_pendukung(request):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
      form = UploadBerkasPendukungForm(request.POST, request.FILES)
      berkas_ = request.FILES.get('berkas')
      if request.method == "POST":
        if berkas_:
          if form.is_valid():
            ext = os.path.splitext(berkas_.name)[1]
            valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.png']
            if not ext in valid_extensions:
              data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
            else:
              try:
                p = PengajuanIzin.objects.get(id=request.COOKIES['id_pengajuan'])
                berkas = form.save(commit=False)
                if request.POST.get('aksi') == "1":
                  berkas.nama_berkas = "Keputusan Izin Gangguan (HO)"+p.no_pengajuan
                  berkas.keterangan = "Keputusan Izin Gangguan (HO)"
                elif request.POST.get('aksi') == "2":
                  berkas.nama_berkas = "Akta Pendirian Perusahaan"+p.no_pengajuan
                  berkas.keterangan = "Akta Pendirian Perusahaan"
                elif request.POST.get('aksi') == "3":
                  berkas.nama_berkas = "File KTP/Paspor (Dirut / Pemilik / Pengurus / Penanggung Jawab)"+p.no_pengajuan
                  berkas.keterangan = "File KTP/Paspor (Dirut / Pemilik / Pengurus / Penanggung Jawab)"
                elif request.POST.get('aksi') == "4":
                  berkas.nama_berkas = "Foto 4x6cm"+p.no_pengajuan
                  berkas.keterangan = "Foto 4x6cm"
                elif request.POST.get('aksi') == "5":
                  berkas.nama_berkas = "Denah Bangunan dan Tata Letak Bangunan"+p.no_pengajuan
                  berkas.keterangan = "Denah Bangunan dan Tata Letak Bangunan"
                elif request.POST.get('aksi') == "6":
                  berkas.nama_berkas = "Rekomendasi dari Dinas Pertanian Kabupaten Kediri"+p.no_pengajuan
                  berkas.keterangan = "Rekomendasi dari Dinas Pertanian Kabupaten Kediri"
                elif request.POST.get('aksi') == "7":
                  berkas.nama_berkas = "Struktur Organisasi Pemilik jika berupa badan usaha"+p.no_pengajuan
                  berkas.keterangan = "Struktur Organisasi Pemilik jika berupa badan usaha"
                elif request.POST.get('aksi') == "8":
                  berkas.nama_berkas = "Struktur Organisasi Pengusaha jika berupa badan usaha"+p.no_pengajuan
                  berkas.keterangan = "Struktur Organisasi Pengusaha jika berupa badan usaha"
                elif request.POST.get('aksi') == "9":
                  berkas.nama_berkas = "Akta Pendirian Perusahaan Pemilik jika berupa badan usaha"+p.no_pengajuan
                  berkas.keterangan = "Akta Pendirian Perusahaan Pemilik jika berupa badan usaha"
                else:
                  berkas.nama_berkas = "Akta Pendirian Perusahaan Pengusaha jika berupa badan usaha"+p.no_pengajuan
                  berkas.keterangan = "Akta Pendirian Perusahaan Pengusaha jika berupa badan usaha"
                  
                if request.user.is_authenticated():
                  berkas.created_by_id = request.user.id
                else:
                  berkas.created_by_id = request.COOKIES['id_pemohon']
                berkas.save()
                p.berkas_tambahan.add(berkas)

                data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
                    {'status_upload': 'ok'},
                  ]}
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

def ajax_load_berkas_detilhuller(request, id_pengajuan):
  url_berkas = []
  id_elemen = []
  nm_berkas =[]
  id_berkas =[]
  if id_pengajuan:
    try:
      p = PengajuanIzin.objects.get(id=request.COOKIES['id_pengajuan'])

      keputusan_izin_gangguan = Berkas.objects.filter(nama_berkas="Keputusan Izin Gangguan (HO)"+p.no_pengajuan)
      if keputusan_izin_gangguan.exists():
        keputusan_izin_gangguan = keputusan_izin_gangguan.last()
        url_berkas.append(keputusan_izin_gangguan.berkas.url)
        id_elemen.append('keputusan_izin_gangguan')
        nm_berkas.append("Keputusan Izin Gangguan (HO)"+p.no_pengajuan)
        id_berkas.append(keputusan_izin_gangguan.id)

      akta_pendirian_perusahaan = Berkas.objects.filter(nama_berkas="Akta Pendirian Perusahaan"+p.no_pengajuan)
      if akta_pendirian_perusahaan.exists():
        akta_pendirian_perusahaan = akta_pendirian_perusahaan.last()
        url_berkas.append(akta_pendirian_perusahaan.berkas.url)
        id_elemen.append('akta_pendirian_perusahaan')
        nm_berkas.append("Akta Pendirian Perusahaan"+p.no_pengajuan)
        id_berkas.append(akta_pendirian_perusahaan.id)

      upload_gambar_ktp = Berkas.objects.filter(nama_berkas="File KTP/Paspor (Dirut / Pemilik / Pengurus / Penanggung Jawab)"+p.no_pengajuan)
      if upload_gambar_ktp.exists():
        upload_gambar_ktp = upload_gambar_ktp.last()
        url_berkas.append(upload_gambar_ktp.berkas.url)
        id_elemen.append('file_ktp_paspor')
        nm_berkas.append("File KTP/Paspor (Dirut / Pemilik / Pengurus / Penanggung Jawab)"+p.no_pengajuan)
        id_berkas.append(upload_gambar_ktp.id)

      foto_4x6 = Berkas.objects.filter(nama_berkas="Foto 4x6cm"+p.no_pengajuan)
      if foto_4x6.exists():
        foto_4x6 = foto_4x6.last()
        url_berkas.append(foto_4x6.berkas.url)
        id_elemen.append('file_ktp_4x6')
        nm_berkas.append("Foto 4x6cm"+p.no_pengajuan)
        id_berkas.append(foto_4x6.id)

      denah_bangunan = Berkas.objects.filter(nama_berkas="Denah Bangunan dan Tata Letak Bangunan"+p.no_pengajuan)
      if denah_bangunan.exists():
        denah_bangunan = denah_bangunan.last()
        url_berkas.append(denah_bangunan.berkas.url)
        id_elemen.append('denah_bangunan')
        nm_berkas.append("Denah Bangunan dan Tata Letak Bangunan"+p.no_pengajuan)
        id_berkas.append(denah_bangunan.id)

      rekomendasi_dinas_pertanian = Berkas.objects.filter(nama_berkas="Rekomendasi dari Dinas Pertanian Kabupaten Kediri"+p.no_pengajuan)
      if rekomendasi_dinas_pertanian.exists():
        rekomendasi_dinas_pertanian = rekomendasi_dinas_pertanian.last()
        url_berkas.append(rekomendasi_dinas_pertanian.berkas.url)
        id_elemen.append('rekomendasi_dinas_pertanian')
        nm_berkas.append("Rekomendasi dari Dinas Pertanian Kabupaten Kediri"+p.no_pengajuan)
        id_berkas.append(rekomendasi_dinas_pertanian.id)

      struktur_organisasi_pemilik = Berkas.objects.filter(nama_berkas="Struktur Organisasi Pemilik jika berupa badan usaha"+p.no_pengajuan)
      if struktur_organisasi_pemilik.exists():
        struktur_organisasi_pemilik = struktur_organisasi_pemilik.last()
        url_berkas.append(struktur_organisasi_pemilik.berkas.url)
        id_elemen.append('struktur_organisasi_pemilik')
        nm_berkas.append("Struktur Organisasi Pemilik jika berupa badan usaha"+p.no_pengajuan)
        id_berkas.append(struktur_organisasi_pemilik.id)

      struktur_organisasi_pengusaha = Berkas.objects.filter(nama_berkas="Struktur Organisasi Pengusaha jika berupa badan usaha"+p.no_pengajuan)
      if struktur_organisasi_pengusaha.exists():
        struktur_organisasi_pengusaha = struktur_organisasi_pengusaha.last()
        url_berkas.append(struktur_organisasi_pengusaha.berkas.url)
        id_elemen.append('struktur_organisasi_pengusaha')
        nm_berkas.append("Struktur Organisasi Pengusaha jika berupa badan usaha"+p.no_pengajuan)
        id_berkas.append(struktur_organisasi_pengusaha.id)

      akta_perusahaan_pemilik = Berkas.objects.filter(nama_berkas="Akta Pendirian Perusahaan Pemilik jika berupa badan usaha"+p.no_pengajuan)
      if akta_perusahaan_pemilik.exists():
        akta_perusahaan_pemilik = akta_perusahaan_pemilik.last()
        url_berkas.append(akta_perusahaan_pemilik.berkas.url)
        id_elemen.append('akta_pendirian_perusahaan_pemilik_badan_usaha')
        nm_berkas.append("Akta Pendirian Perusahaan Pemilik jika berupa badan usaha"+p.no_pengajuan)
        id_berkas.append(akta_perusahaan_pemilik.id)

      akta_perusahaan_pengusaha = Berkas.objects.filter(nama_berkas="Akta Pendirian Perusahaan Pengusaha jika berupa badan usaha"+p.no_pengajuan)
      if akta_perusahaan_pengusaha.exists():
        akta_perusahaan_pengusaha = akta_perusahaan_pengusaha.last()
        url_berkas.append(akta_perusahaan_pengusaha.berkas.url)
        id_elemen.append('akta_pendirian_perusahaan_pengusaha_badan_usaha')
        nm_berkas.append("Akta Pendirian Perusahaan Pengusaha jika berupa badan usaha"+p.no_pengajuan)
        id_berkas.append(akta_perusahaan_pengusaha.id)

      data = {'success': True, 'pesan': 'berkas pendukung Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
    except ObjectDoesNotExist:
      data = {'success': False, 'pesan': '' }
      
    
  response = HttpResponse(json.dumps(data))
  return response