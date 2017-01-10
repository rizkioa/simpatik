from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin import site
from functools import wraps
from django.views.decorators.cache import cache_page
from django.utils.decorators import available_attrs
from django.core.exceptions import ObjectDoesNotExist

from django.template import RequestContext, loader
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.db.models import Q
from datetime import datetime
from django.conf import settings
from django.views import generic
from django.shortcuts import get_object_or_404
import base64
import time
import json
import os

from master.models import Negara, Kecamatan, JenisPemohon
from izin.models import JenisIzin, Syarat, KelompokJenisIzin, JenisPermohonanIzin,Riwayat
from izin.models import PengajuanIzin, InformasiTanah,Pemohon,PenggunaaTanahIPPTUsaha
from izin.izin_forms import UploadBerkasPendukungForm,InformasiTanahIPPTUsahaForm,PenggunaaTanahIPPTUsahaForm

def formulir_ippt_usaha(request, extra_context={}):
    jenis_pemohon = JenisPemohon.objects.all()
    negara = Negara.objects.all()
    kecamatan = Kecamatan.objects.filter(kabupaten_id=1083)

    extra_context.update({'negara': negara})
    extra_context.update({'kecamatan': kecamatan})
    extra_context.update({'jenis_pemohon': jenis_pemohon})
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            penggunaan_tanah_list = PenggunaaTanahIPPTUsaha.objects.filter(informasi_tanah=request.COOKIES['id_pengajuan'])
            extra_context.update({'penggunaan_tanah_list': penggunaan_tanah_list})
    if 'id_kelompok_izin' in request.COOKIES.keys():
        jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) 
        extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
    else:
        return HttpResponseRedirect(reverse('layanan'))
    return render(request, "front-end/formulir/ippt_usaha.html", extra_context)

def ippt_usaha_save_cookie(request):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            pengajuan_ = InformasiTanah.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
            ippt_usaha = InformasiTanahIPPTUsahaForm(request.POST, instance=pengajuan_)
            if ippt_usaha.is_valid():
                pengajuan_.perusahaan_id  = request.COOKIES['id_perusahaan']
                pengajuan_.save()
                data = {'success': True,
                        'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
                        'data': ['']}
                data = json.dumps(data)
                response = HttpResponse(json.dumps(data))
            else:
                data = ippt_usaha.errors.as_json()
        else:
            data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
            data = json.dumps(data)
    else:
        data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
        data = json.dumps(data)
    response = HttpResponse(data)
    return response

def informasi_penggunaan_tanah_sekarang_save_cookie(request):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            penggunaan_tanah_sekarang = PenggunaaTanahIPPTUsahaForm(request.POST)
            if request.method == 'POST':
                if penggunaan_tanah_sekarang.is_valid():
                    p = penggunaan_tanah_sekarang.save(commit=False)
                    p.informasi_tanah_id = request.COOKIES['id_pengajuan']
                    p.save()
                    data = {'success': True,
                            'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
                            'data': {'id_penggunaan_tanah_sekarang':p.id}}
                    data = json.dumps(data)
                    response = HttpResponse(json.dumps(data))
                else:
                    data = penggunaan_tanah_sekarang.errors.as_json()
            else:
                penggunaan_tanah_sekarang = PenggunaaTanahIPPTUsahaForm()
        else:
            data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
            data = json.dumps(data)
    else:
        data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
        data = json.dumps(data)
    response = HttpResponse(data)
    return response

def delete_informasi_penggunaan_tanah_sekarang(request,id_penggunaan_tanah):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
        tag_to_delete = get_object_or_404(PenggunaaTanahIPPTUsaha, id=id_penggunaan_tanah)
        tag_to_delete.delete()
        data = {'success': True,
                'pesan': 'Data berhasil Dihapus.'}
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