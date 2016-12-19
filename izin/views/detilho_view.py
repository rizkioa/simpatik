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

from master.models import Negara, Kecamatan, JenisPemohon,JenisReklame,Berkas,ParameterBangunan
from izin.models import JenisIzin, Syarat, KelompokJenisIzin, JenisPermohonanIzin,Riwayat
from izin.models import PengajuanIzin, DetilHO,Pemohon
from izin.utils import JENIS_LOKASI_USAHA,JENIS_BANGUNAN,JENIS_GANGGUAN
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna
from izin.izin_forms import UploadBerkasPendukungForm,DetilHOForm

def formulir_ho(request, extra_context={}):
    jenis_pemohon = JenisPemohon.objects.all()
    negara = Negara.objects.all()
    kecamatan = Kecamatan.objects.filter(kabupaten_id=1083)

    extra_context.update({'jenis_lokasi_usaha_list': JENIS_LOKASI_USAHA})
    extra_context.update({'jenis_bangunan_list': JENIS_BANGUNAN})
    extra_context.update({'jenis_gangguan_list': JENIS_GANGGUAN})
    extra_context.update({'negara': negara})
    extra_context.update({'kecamatan': kecamatan})
    extra_context.update({'jenis_pemohon': jenis_pemohon})
    if 'id_kelompok_izin' in request.COOKIES.keys():
        jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) 
        extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
    else:
        return HttpResponseRedirect(reverse('layanan'))
    return render(request, "front-end/formulir/ho.html", extra_context)

def detilho_save_cookie(request):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            pengajuan_ = DetilHO.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
            detilHO = DetilHOForm(request.POST, instance=pengajuan_)
            if detilHO.is_valid():
                pengajuan_.perusahaan_id  = request.COOKIES['id_perusahaan']
                pengajuan_.save()
                data = {'success': True,
                        'pesan': 'Data Reklame berhasil disimpan. Proses Selanjutnya.',
                        'data': ['']}
                data = json.dumps(data)
                response = HttpResponse(json.dumps(data))
            else:
                data = detilHO.errors.as_json()
        else:
            data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
            data = json.dumps(data)
    else:
        data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
        data = json.dumps(data)
    response = HttpResponse(data)
    return response

def detilho_done(request):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
      pengajuan_ = DetilHO.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
      pengajuan_.status = 6
      pengajuan_.save()
      data = {'success': True, 'pesan': 'Proses Selesai.' }
      response = HttpResponse(json.dumps(data))
      response.delete_cookie(key='id_pengajuan') # set cookie 
      response.delete_cookie(key='id_perusahaan') # set cookie 
      response.delete_cookie(key='nomor_ktp') # set cookie  
      response.delete_cookie(key='nomor_paspor') # set cookie 
      response.delete_cookie(key='id_pemohon') # set cookie 
      response.delete_cookie(key='id_kelompok_izin') # set cookie
      response.delete_cookie(key='id_legalitas') # set cookie
      response.delete_cookie(key='id_legalitas_perubahan') # set cookie
    else:
      data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
      data = json.dumps(data)
      response = HttpResponse(data)
  else:
    data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
    data = json.dumps(data)
    response = HttpResponse(data)
  return response
