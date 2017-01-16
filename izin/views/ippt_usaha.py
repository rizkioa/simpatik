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
from izin.models import PengajuanIzin, InformasiTanah,Pemohon,PenggunaanTanahIPPTUsaha,PerumahanYangDimilikiIPPTUsaha
from izin.izin_forms import UploadBerkasKTPForm,UploadBerkasPendukungForm,InformasiTanahIPPTUsahaForm,PenggunaanTanahIPPTUsahaForm,RencanaPembangunanIPPTUsahaForm,RencanaPembiayanDanPemodalanIPPTUsahaForm,PerumahanYangDimilikiIPPTUsahaForm,KebutuhanLainnyaIPPTUsahaForm
from accounts.models import NomorIdentitasPengguna

def formulir_ippt_usaha(request, extra_context={}):
    jenis_pemohon = JenisPemohon.objects.all()
    negara = Negara.objects.all()
    kecamatan = Kecamatan.objects.filter(kabupaten_id=1083)

    extra_context.update({'negara': negara})
    extra_context.update({'kecamatan': kecamatan})
    extra_context.update({'jenis_pemohon': jenis_pemohon})
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            penggunaan_tanah_list = PenggunaanTanahIPPTUsaha.objects.filter(informasi_tanah=request.COOKIES['id_pengajuan'])
            perumahan_list = PerumahanYangDimilikiIPPTUsaha.objects.filter(informasi_tanah=request.COOKIES['id_pengajuan'])
            extra_context.update({'penggunaan_tanah_list': penggunaan_tanah_list})
            extra_context.update({'perumahan_list': perumahan_list})
        PerumahanYangDimilikiIPPTUsaha
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

def ippt_usaha_rencana_pembangunan_save_cookie(request):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            pengajuan_ = InformasiTanah.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
            ippt_usaha_rencana_pembangunan = RencanaPembangunanIPPTUsahaForm(request.POST, instance=pengajuan_)
            if ippt_usaha_rencana_pembangunan.is_valid():
                p = ippt_usaha_rencana_pembangunan.save(commit=False)
                p.save()
                data = {'success': True,
                        'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
                        'data': ['']}
                data = json.dumps(data)
                response = HttpResponse(json.dumps(data))
            else:
                data = ippt_usaha_rencana_pembangunan.errors.as_json()
        else:
            data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
            data = json.dumps(data)
    else:
        data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
        data = json.dumps(data)
    response = HttpResponse(data)
    return response

def ippt_usaha_rencana_pembiayaan_dan_pemodalan_save_cookie(request):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            pengajuan_ = InformasiTanah.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
            ippt_usaha_rencana_pembiayaan = RencanaPembiayanDanPemodalanIPPTUsahaForm(request.POST, instance=pengajuan_)
            if ippt_usaha_rencana_pembiayaan.is_valid():
                p = ippt_usaha_rencana_pembiayaan.save(commit=False)
                p.save()
                data = {'success': True,
                        'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
                        'data': ['']}
                data = json.dumps(data)
                response = HttpResponse(json.dumps(data))
            else:
                data = ippt_usaha_rencana_pembiayaan.errors.as_json()
        else:
            data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
            data = json.dumps(data)
    else:
        data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
        data = json.dumps(data)
    response = HttpResponse(data)
    return response

def ippt_usaha_kebutuhan_lainnya_save_cookie(request):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            pengajuan_ = InformasiTanah.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
            kebutuhan_lainnya = KebutuhanLainnyaIPPTUsahaForm(request.POST, instance=pengajuan_)
            if kebutuhan_lainnya.is_valid():
                p = kebutuhan_lainnya.save(commit=False)
                p.save()
                data = {'success': True,
                        'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
                        'data': ['']}
                data = json.dumps(data)
                response = HttpResponse(json.dumps(data))
            else:
                data = kebutuhan_lainnya.errors.as_json()
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
            penggunaan_tanah_sekarang = PenggunaanTanahIPPTUsahaForm(request.POST)
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
                penggunaan_tanah_sekarang = PenggunaanTanahIPPTUsahaForm()
        else:
            data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
            data = json.dumps(data)
    else:
        data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
        data = json.dumps(data)
    response = HttpResponse(data)
    return response

def edit_informasi_penggunaan_tanah_sekarang(request,id_penggunaan_tanah):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            p = PenggunaanTanahIPPTUsaha.objects.get(id=id_penggunaan_tanah)
            penggunaan_tanah_sekarang = PenggunaanTanahIPPTUsahaForm(request.POST,instance=p)
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
                penggunaan_tanah_sekarang = PenggunaanTanahIPPTUsahaForm()
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
        tag_to_delete = get_object_or_404(PenggunaanTanahIPPTUsaha, id=id_penggunaan_tanah)
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


def perumahan_yang_sudah_dimiliki_save_cookie(request):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            perumahan_yang_sudah_dimiliki = PerumahanYangDimilikiIPPTUsahaForm(request.POST)
            if request.method == 'POST':
                if perumahan_yang_sudah_dimiliki.is_valid():
                    p = perumahan_yang_sudah_dimiliki.save(commit=False)
                    p.informasi_tanah_id = request.COOKIES['id_pengajuan']
                    p.save()
                    data = {'success': True,
                            'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
                            'data': {'id_perumahan_yang_sudah_dimiliki':p.id}}
                    data = json.dumps(data)
                    response = HttpResponse(json.dumps(data))
                else:
                    data = perumahan_yang_sudah_dimiliki.errors.as_json()
            else:
                perumahan_yang_sudah_dimiliki = PerumahanYangDimilikiIPPTUsahaForm()
        else:
            data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
            data = json.dumps(data)
    else:
        data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
        data = json.dumps(data)
    response = HttpResponse(data)
    return response

def edit_perumahan_yang_sudah_dimiliki(request,id_perumahan):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            p = PerumahanYangDimilikiIPPTUsaha.objects.get(id=id_perumahan)
            perumahan_yang_sudah_dimiliki = PerumahanYangDimilikiIPPTUsahaForm(request.POST,instance=p)
            if request.method == 'POST':
                if perumahan_yang_sudah_dimiliki.is_valid():
                    p = perumahan_yang_sudah_dimiliki.save(commit=False)
                    p.informasi_tanah_id = request.COOKIES['id_pengajuan']
                    p.save()
                    data = {'success': True,
                            'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
                            'data': {'id_perumahan_yang_sudah_dimiliki':p.id}}
                    data = json.dumps(data)
                    response = HttpResponse(json.dumps(data))
                else:
                    data = perumahan_yang_sudah_dimiliki.errors.as_json()
            else:
                perumahan_yang_sudah_dimiliki = PerumahanYangDimilikiIPPTUsahaForm()
        else:
            data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
            data = json.dumps(data)
    else:
        data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
        data = json.dumps(data)
    response = HttpResponse(data)
    return response

def delete_perumahan_yang_sudah_dimiliki(request,id_perumahan):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
        tag_to_delete = get_object_or_404(PerumahanYangDimilikiIPPTUsaha, id=id_perumahan)
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

def ipptusaha_upload_berkas_pendukung(request):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '' or request.COOKIES['id_pemohon'] and request.COOKIES['nomor_ktp'] != '':
            form_ktp = UploadBerkasKTPForm(request.POST, request.FILES)
            form = UploadBerkasPendukungForm(request.POST, request.FILES)
            berkas_ = request.FILES.get('berkas')
            if request.method == "POST":
                if berkas_:
                    if form.is_valid() or form_ktp.is_valid():
                        ext = os.path.splitext(berkas_.name)[1]
                        valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.png']
                        if not ext in valid_extensions:
                          data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
                        else:
                            try:
                                p = PengajuanIzin.objects.get(id=request.COOKIES['id_pengajuan'])
                                ktp_ = NomorIdentitasPengguna.objects.get(nomor=request.COOKIES['nomor_ktp'])
                                berkas = form.save(commit=False)
                                if request.POST.get('aksi') == "1":
                                    berkas.nama_berkas = "Berkas Foto KTP/PASPOR"+ktp_.nomor
                                    berkas.keterangan = "Berkas Foto KTP/PASPOR"
                                elif request.POST.get('aksi') == "2":
                                    berkas.nama_berkas = "Kartu Keluarga"+p.no_pengajuan
                                    berkas.keterangan = "Kartu Keluarga"
                                elif request.POST.get('aksi') == "3":
                                    berkas.nama_berkas = "NPWP Pribadi"+p.no_pengajuan
                                    berkas.keterangan = "NPWP Pribadi"
                                elif request.POST.get('aksi') == "4":
                                    berkas.nama_berkas = "NPWP Perusahaan"+p.no_pengajuan
                                    berkas.keterangan = "NPWP Perusahaan"
                                elif request.POST.get('aksi') == "5":
                                    berkas.nama_berkas = "Bukti Kepimilikan Tanah"+p.no_pengajuan
                                    berkas.keterangan = "Bukti Kepimilikan Tanah"
                                elif request.POST.get('aksi') == "6":
                                    berkas.nama_berkas = "Sketsa Lokasi Tanah Yang Dimohon"+p.no_pengajuan
                                    berkas.keterangan = "Sketsa Lokasi Tanah Yang Dimohon"
                                elif request.POST.get('aksi') == "7":
                                    berkas.nama_berkas = "Gambar / Denah Rencana Penggunaan Tanah"+p.no_pengajuan
                                    berkas.keterangan = "Gambar / Denah Rencana Penggunaan Tanah"
                                elif request.POST.get('aksi') == "8":
                                    berkas.nama_berkas = "Sertifikat Rumah"+p.no_pengajuan
                                    berkas.keterangan = "Sertifikat Rumah"
                                elif request.POST.get('aksi') == "9":
                                    berkas.nama_berkas = "Akta Jual Beli"+p.no_pengajuan
                                    berkas.keterangan = "Akta Jual Beli"
                                elif request.POST.get('aksi') == "10":
                                    berkas.nama_berkas = "Site Plan"+p.no_pengajuan
                                    berkas.keterangan = "Site Plan"
                                elif request.POST.get('aksi') == "11":
                                    berkas.nama_berkas = "SPPT Tahun Terakhir"+p.no_pengajuan
                                    berkas.keterangan = "SPPT Tahun Terakhir"
                                elif request.POST.get('aksi') == "12":
                                    berkas.nama_berkas = "Rekomendasi Bupati / Izin-izin lain yang diperoleh"+p.no_pengajuan
                                    berkas.keterangan = "Rekomendasi Bupati / Izin-izin lain yang diperoleh"
                                elif request.POST.get('aksi') == "13":
                                    berkas.nama_berkas = "Rencana Jadwal Pelaksanaan"+p.no_pengajuan
                                    berkas.keterangan = "Rencana Jadwal Pelaksanaan"
                                elif request.POST.get('aksi') == "14":
                                    berkas.nama_berkas = "Block Plan / Rencana Tapak"+p.no_pengajuan
                                    berkas.keterangan = "Block Plan / Rencana Tapak"
                                else:
                                    berkas.nama_berkas = "Analisis Air"+p.no_pengajuan
                                    berkas.keterangan = "Analisis Air"

                                if request.user.is_authenticated():
                                    berkas.created_by_id = request.user.id
                                else:
                                    berkas.created_by_id = request.COOKIES['id_pemohon']
                                    berkas.save()
                                    p.berkas_tambahan.add(berkas)
                                    ktp_.berkas_id = berkas.id
                                    ktp_.save()
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


# ktp_paspor
# kartu_keluarga
# npwp_pribadi
# npwp_perusahaan
# bukti_kepemilikan_tanah
# sketsa_tanah_yang_dimohon
# gambar_rencana_penggunaan_tanah
# sertifikat_rumah
# akta_jual_beli
# site_plan
# sppt_tahun_terakhir
# rekomendasi_bupati
# rencana_jadwal_perencanaan
# block_plan
# analisis_air