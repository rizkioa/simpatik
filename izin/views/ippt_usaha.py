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

from master.models import Negara, Kecamatan, JenisPemohon,Berkas
from izin.models import JenisIzin, Syarat, KelompokJenisIzin, JenisPermohonanIzin,Riwayat
from izin.models import PengajuanIzin, InformasiTanah,Pemohon,PenggunaanTanahIPPTUsaha,PerumahanYangDimilikiIPPTUsaha
from izin.izin_forms import UploadBerkasKTPForm,UploadBerkasPendukungForm,InformasiTanahIPPTUsahaForm,PenggunaanTanahIPPTUsahaForm,RencanaPembangunanIPPTUsahaForm,RencanaPembiayanDanPemodalanIPPTUsahaForm,PerumahanYangDimilikiIPPTUsahaForm,KebutuhanLainnyaIPPTUsahaForm
from accounts.models import NomorIdentitasPengguna
from accounts.utils import KETERANGAN_PEKERJAAN

def formulir_ippt_usaha(request, extra_context={}):
    jenis_pemohon = JenisPemohon.objects.all()
    negara = Negara.objects.all()
    kecamatan = Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35')

    extra_context.update({'negara': negara})
    extra_context.update({'kecamatan': kecamatan})
    extra_context.update({'jenis_pemohon': jenis_pemohon})
    extra_context.update({'keterangan_pekerjaan': KETERANGAN_PEKERJAAN })
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
                if 'id_perusahaan' in request.COOKIES.keys():
                    if request.COOKIES['id_perusahaan'] != '0':
                        pengajuan_.perusahaan_id  = request.COOKIES['id_perusahaan']
                        pengajuan_.save()
                        data = {'success': True,
                            'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
                            'data': {}}
                        response = HttpResponse(json.dumps(data))
                    else:
                        ippt_usaha.save(commit=False)
                        data = {'success': True,
                              'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
                              'data': {}}
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
            response = HttpResponse(data)
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
            response = HttpResponse(data)
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
            # form_ktp = UploadBerkasKTPForm(request.POST, request.FILES)
            form = UploadBerkasPendukungForm(request.POST, request.FILES)
            berkas_ = request.FILES.get('berkas')
            if request.method == "POST":
                if berkas_:
                    if form.is_valid():
                        ext = os.path.splitext(berkas_.name)[1]
                        valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.jpeg', '.png', '.PDF', '.DOC', '.DOCX', '.JPG', '.JPEG', '.PNG']
                        if not ext in valid_extensions:
                          data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
                        else:
                            try:
                                p = PengajuanIzin.objects.get(id=request.COOKIES['id_pengajuan'])
                                print p
                                ktp_ = NomorIdentitasPengguna.objects.get(nomor=request.COOKIES['nomor_ktp'])
                                print ktp_
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
                                    berkas.nama_berkas = "Sketsa Lokasi Tanah Yang Dimohon"+p.no_pengajuan
                                    berkas.keterangan = "Sketsa Lokasi Tanah Yang Dimohon"
                                elif request.POST.get('aksi') == "6":
                                    berkas.nama_berkas = "Gambar / Denah Rencana Penggunaan Tanah"+p.no_pengajuan
                                    berkas.keterangan = "Gambar / Denah Rencana Penggunaan Tanah"
                                elif request.POST.get('aksi') == "7":
                                    berkas.nama_berkas = "Bukti Kepemilikan Tanah 01"+p.no_pengajuan
                                    berkas.keterangan = "Bukti Kepemilikan Tanah 01"
                                elif request.POST.get('aksi') == "8":
                                    berkas.nama_berkas = "Bukti Kepemilikan Tanah 02"+p.no_pengajuan
                                    berkas.keterangan = "Bukti Kepemilikan Tanah 02"
                                elif request.POST.get('aksi') == "9":
                                    berkas.nama_berkas = "Bukti Kepemilikan Tanah 03"+p.no_pengajuan
                                    berkas.keterangan = "Bukti Kepemilikan Tanah 03"
                                elif request.POST.get('aksi') == "10":
                                    berkas.nama_berkas = "SPPT Tahun Terakhir"+p.no_pengajuan
                                    berkas.keterangan = "SPPT Tahun Terakhir"
                                elif request.POST.get('aksi') == "11":
                                    berkas.nama_berkas = "Rekomendasi Bupati / Izin-izin lain yang diperoleh"+p.no_pengajuan
                                    berkas.keterangan = "Rekomendasi Bupati / Izin-izin lain yang diperoleh"
                                else:
                                    berkas.nama_berkas = "Rencana Jadwal Pelaksanaan"+p.no_pengajuan
                                    berkas.keterangan = "Rencana Jadwal Pelaksanaan"

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

def ajax_load_berkas_ipptusaha(request, id_pengajuan):
    url_berkas = []
    id_elemen = []
    nm_berkas =[]
    id_berkas =[]
    if id_pengajuan:
        try:
            p = PengajuanIzin.objects.get(id=request.COOKIES['id_pengajuan'])
            ktp_paspor = Berkas.objects.filter(nama_berkas="Berkas Foto KTP/PASPOR"+p.pemohon.username)
            if ktp_paspor.exists():
                ktp_paspor = ktp_paspor.last()
                url_berkas.append(ktp_paspor.berkas.url)
                id_elemen.append('ktp_paspor')
                nm_berkas.append("Berkas Foto KTP/PASPOR"+p.pemohon.username)
                id_berkas.append(ktp_paspor.id)

            kartu_keluarga  = Berkas.objects.filter(nama_berkas="Kartu Keluarga"+p.no_pengajuan)
            if kartu_keluarga.exists():
                kartu_keluarga = kartu_keluarga.last()
                url_berkas.append(kartu_keluarga.berkas.url)
                id_elemen.append('kartu_keluarga')
                nm_berkas.append("Kartu Keluarga"+p.no_pengajuan)
                id_berkas.append(kartu_keluarga.id)

            npwp_pribadi = Berkas.objects.filter(nama_berkas="NPWP Pribadi"+p.no_pengajuan)
            if npwp_pribadi.exists():
                npwp_pribadi = npwp_pribadi.last()
                url_berkas.append(npwp_pribadi.berkas.url)
                id_elemen.append('npwp_pribadi')
                nm_berkas.append("NPWP Pribadi"+p.no_pengajuan)
                id_berkas.append(npwp_pribadi.id)

            npwp_perusahaan = Berkas.objects.filter(nama_berkas="NPWP Perusahaan"+p.no_pengajuan)
            if npwp_perusahaan.exists():
                npwp_perusahaan = npwp_perusahaan.last()
                url_berkas.append(npwp_perusahaan.berkas.url)
                id_elemen.append('npwp_perusahaan')
                nm_berkas.append("NPWP Perusahaan"+p.no_pengajuan)
                id_berkas.append(npwp_perusahaan.id)

            sketsa_tanah_yang_dimohon = Berkas.objects.filter(nama_berkas="Sketsa Lokasi Tanah Yang Dimohon"+p.no_pengajuan)
            if sketsa_tanah_yang_dimohon.exists():
                sketsa_tanah_yang_dimohon = sketsa_tanah_yang_dimohon.last()
                url_berkas.append(sketsa_tanah_yang_dimohon.berkas.url)
                id_elemen.append('sketsa_tanah_yang_dimohon')
                nm_berkas.append("Sketsa Lokasi Tanah Yang Dimohon"+p.no_pengajuan)
                id_berkas.append(sketsa_tanah_yang_dimohon.id)

            gambar_rencana_penggunaan_tanah = Berkas.objects.filter(nama_berkas="Gambar / Denah Rencana Penggunaan Tanah"+p.no_pengajuan)
            if gambar_rencana_penggunaan_tanah.exists():
                gambar_rencana_penggunaan_tanah = gambar_rencana_penggunaan_tanah.last()
                url_berkas.append(gambar_rencana_penggunaan_tanah.berkas.url)
                id_elemen.append('gambar_rencana_penggunaan_tanah')
                nm_berkas.append("Gambar / Denah Rencana Penggunaan Tanah"+p.no_pengajuan)
                id_berkas.append(gambar_rencana_penggunaan_tanah.id)

            sertifikat_rumah = Berkas.objects.filter(nama_berkas="Bukti Kepemilikan Tanah 01"+p.no_pengajuan)
            if sertifikat_rumah.exists():
                sertifikat_rumah = sertifikat_rumah.last()
                url_berkas.append(sertifikat_rumah.berkas.url)
                id_elemen.append('sertifikat_rumah')
                nm_berkas.append("Bukti Kepemilikan Tanah 01"+p.no_pengajuan)
                id_berkas.append(sertifikat_rumah.id)

            akta_jual_beli = Berkas.objects.filter(nama_berkas="Bukti Kepemilikan Tanah 02"+p.no_pengajuan)
            if akta_jual_beli.exists():
                akta_jual_beli = akta_jual_beli.last()
                url_berkas.append(akta_jual_beli.berkas.url)
                id_elemen.append('akta_jual_beli')
                nm_berkas.append("Bukti Kepemilikan Tanah 02"+p.no_pengajuan)
                id_berkas.append(akta_jual_beli.id)

            site_plan = Berkas.objects.filter(nama_berkas="Bukti Kepemilikan Tanah 03"+p.no_pengajuan)
            if site_plan.exists():
                site_plan = site_plan.last()
                url_berkas.append(site_plan.berkas.url)
                id_elemen.append('site_plan')
                nm_berkas.append("Bukti Kepemilikan Tanah 03"+p.no_pengajuan)
                id_berkas.append(site_plan.id)

            sppt_tahun_terakhir = Berkas.objects.filter(nama_berkas="SPPT Tahun Terakhir"+p.no_pengajuan)
            if sppt_tahun_terakhir.exists():
                sppt_tahun_terakhir = sppt_tahun_terakhir.last()
                url_berkas.append(sppt_tahun_terakhir.berkas.url)
                id_elemen.append('sppt_tahun_terakhir')
                nm_berkas.append("SPPT Tahun Terakhir"+p.no_pengajuan)
                id_berkas.append(sppt_tahun_terakhir.id)

            rekomendasi_bupati = Berkas.objects.filter(nama_berkas="Rekomendasi Bupati / Izin-izin lain yang diperoleh"+p.no_pengajuan)
            if rekomendasi_bupati.exists():
                rekomendasi_bupati = rekomendasi_bupati.last()
                url_berkas.append(rekomendasi_bupati.berkas.url)
                id_elemen.append('rekomendasi_bupati')
                nm_berkas.append("Rekomendasi Bupati / Izin-izin lain yang diperoleh"+p.no_pengajuan)
                id_berkas.append(rekomendasi_bupati.id)

            rencana_jadwal_perencanaan = Berkas.objects.filter(nama_berkas="Rencana Jadwal Pelaksanaan"+p.no_pengajuan)
            if rencana_jadwal_perencanaan.exists():
                rencana_jadwal_perencanaan = rencana_jadwal_perencanaan.last()
                url_berkas.append(rencana_jadwal_perencanaan.berkas.url)
                id_elemen.append('rencana_jadwal_perencanaan')
                nm_berkas.append("Rencana Jadwal Pelaksanaan"+p.no_pengajuan)
                id_berkas.append(rencana_jadwal_perencanaan.id)

            data = {'success': True, 'pesan': 'berkas pendukung Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
        except ObjectDoesNotExist:
            data = {'success': False, 'pesan': '' }
    response = HttpResponse(json.dumps(data))
    return response

def load_data_informasi_tanah_ipptusaha(request,id_pengajuan):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            pengajuan_ = InformasiTanah.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
            if pengajuan_.no_surat_kuasa:
                id_no_surat_kuasa = pengajuan_.no_surat_kuasa
            else:
                id_no_surat_kuasa = ""
            if pengajuan_.tanggal_surat_kuasa:
                id_tanggal_surat_kuasa = pengajuan_.tanggal_surat_kuasa.strftime("%d-%m-%Y")
            else:
                id_tanggal_surat_kuasa = ""
            if pengajuan_.tahun_sertifikat:
                id_tahun_sertifikat = pengajuan_.tahun_sertifikat.strftime("%d-%m-%Y")
            else:
                id_tahun_sertifikat = ""

            id_alamat = pengajuan_.alamat
            kabupaten = ""
            kecamatan = ""
            desa = ""
            if pengajuan_.desa:
                kabupaten = str(pengajuan_.desa.kecamatan.kabupaten)
                kecamatan = str(pengajuan_.desa.kecamatan)
                desa = str(pengajuan_.desa)
                id_kecamatan = str(pengajuan_.desa.kecamatan.id)
                id_desa = str(pengajuan_.desa.id)
            else:
                id_kecamatan = ""
                id_desa = ""
            id_luas = str(pengajuan_.luas)
            id_status_tanah = pengajuan_.status_tanah
            id_no_sertifikat_petak = pengajuan_.no_sertifikat_petak
            id_luas_sertifikat_petak = str(pengajuan_.luas_sertifikat_petak)
            id_atas_nama_sertifikat_petak = pengajuan_.atas_nama_sertifikat_petak
            id_no_persil = pengajuan_.no_persil
            id_klas_persil = pengajuan_.klas_persil
            id_atas_nama_persil = pengajuan_.atas_nama_persil
            id_rencana_penggunaan = pengajuan_.rencana_penggunaan
            id_penggunaan_tanah_sebelumnya = pengajuan_.penggunaan_tanah_sebelumnya
            id_arahan_fungsi_kawasan = pengajuan_.arahan_fungsi_kawasan
            id_batas_utara = pengajuan_.batas_utara
            id_batas_timur = pengajuan_.batas_timur
            id_batas_selatan = pengajuan_.batas_selatan
            id_batas_barat = pengajuan_.batas_barat

            id_tanah_negara_belum_dikuasai = str(pengajuan_.tanah_negara_belum_dikuasai)
            id_tanah_kas_desa_belum_dikuasai = str(pengajuan_.tanah_kas_desa_belum_dikuasai)
            id_tanah_hak_pakai_belum_dikuasai = str(pengajuan_.tanah_hak_pakai_belum_dikuasai)
            id_tanah_hak_guna_bangunan_belum_dikuasai = str(pengajuan_.tanah_hak_guna_bangunan_belum_dikuasai)
            id_tanah_hak_milik_sertifikat_belum_dikuasai = str(pengajuan_.tanah_hak_milik_sertifikat_belum_dikuasai)
            id_tanah_adat_belum_dikuasai = str(pengajuan_.tanah_adat_belum_dikuasai)
            if pengajuan_.pemegang_hak_semula_dari_tanah_belum_dikuasai != None:
                id_pemegang_hak_semula_dari_tanah_belum_dikuasai = str(pengajuan_.pemegang_hak_semula_dari_tanah_belum_dikuasai)
            else:
                id_pemegang_hak_semula_dari_tanah_belum_dikuasai = ""
            if pengajuan_.tanah_belum_dikuasai_melalui != None:
                id_tanah_belum_dikuasai_melalui = str(pengajuan_.tanah_belum_dikuasai_melalui)
            else:
                id_tanah_belum_dikuasai_melalui = ""
            id_jumlah_tanah_belum_dikuasai = str(pengajuan_.jumlah_tanah_belum_dikuasai)
            id_tanah_negara_sudah_dikuasai = str(pengajuan_.tanah_negara_sudah_dikuasai)
            id_tanah_kas_desa_sudah_dikuasai = str(pengajuan_.tanah_kas_desa_sudah_dikuasai)
            id_tanah_hak_pakai_sudah_dikuasai = str(pengajuan_.tanah_hak_pakai_sudah_dikuasai)

            id_tanah_hak_guna_bangunan_sudah_dikuasai = str(pengajuan_.tanah_hak_guna_bangunan_sudah_dikuasai)
            id_tanah_hak_milik_sertifikat_sudah_dikuasai = str(pengajuan_.tanah_hak_milik_sertifikat_sudah_dikuasai)
            id_tanah_adat_sudah_dikuasai = str(pengajuan_.tanah_adat_sudah_dikuasai)
            if pengajuan_.pemegang_hak_semula_dari_tanah_sudah_dikuasai != None:
                id_pemegang_hak_semula_dari_tanah_sudah_dikuasai = str(pengajuan_.pemegang_hak_semula_dari_tanah_sudah_dikuasai)
            else:
                id_pemegang_hak_semula_dari_tanah_sudah_dikuasai = ""
            if pengajuan_.tanah_sudah_dikuasai_melalui != None:
                id_tanah_sudah_dikuasai_melalui = str(pengajuan_.tanah_sudah_dikuasai_melalui)
            else:
                id_tanah_sudah_dikuasai_melalui = ""            
            id_jumlah_tanah_sudah_dikuasai = str(pengajuan_.jumlah_tanah_sudah_dikuasai)

            data = {'success': True,'data': {
            'id_no_surat_kuasa': id_no_surat_kuasa,
            'id_tanggal_surat_kuasa': id_tanggal_surat_kuasa,
            'id_alamat': id_alamat,
            'id_kecamatan': id_kecamatan,
            'id_desa': id_desa,
            'id_luas': id_luas,
            'id_penggunaan_tanah_sebelumnya': id_penggunaan_tanah_sebelumnya,
            'id_arahan_fungsi_kawasan': id_arahan_fungsi_kawasan,
            'id_status_tanah': id_status_tanah,
            'id_no_sertifikat_petak': id_no_sertifikat_petak,
            'id_luas_sertifikat_petak': id_luas_sertifikat_petak,
            'id_atas_nama_sertifikat_petak': id_atas_nama_sertifikat_petak,
            'id_tahun_sertifikat': id_tahun_sertifikat,
            'id_no_persil': id_no_persil,
            'id_klas_persil': id_klas_persil,
            'id_atas_nama_persil': id_atas_nama_persil,
            'id_rencana_penggunaan': id_rencana_penggunaan,
            'id_batas_utara': id_batas_utara,
            'id_batas_timur': id_batas_timur,
            'id_batas_selatan': id_batas_selatan,
            'id_batas_barat': id_batas_barat,
            'id_tanah_negara_belum_dikuasai': id_tanah_negara_belum_dikuasai,
            'id_tanah_kas_desa_belum_dikuasai': id_tanah_kas_desa_belum_dikuasai,
            'id_tanah_hak_pakai_belum_dikuasai': id_tanah_hak_pakai_belum_dikuasai,
            'id_tanah_hak_guna_bangunan_belum_dikuasai': id_tanah_hak_guna_bangunan_belum_dikuasai,
            'id_tanah_hak_milik_sertifikat_belum_dikuasai': id_tanah_hak_milik_sertifikat_belum_dikuasai,
            'id_tanah_adat_belum_dikuasai': id_tanah_adat_belum_dikuasai,
            'id_pemegang_hak_semula_dari_tanah_belum_dikuasai': id_pemegang_hak_semula_dari_tanah_belum_dikuasai,
            'id_tanah_belum_dikuasai_melalui': id_tanah_belum_dikuasai_melalui,
            'id_jumlah_tanah_belum_dikuasai': id_jumlah_tanah_belum_dikuasai,
            'id_tanah_negara_sudah_dikuasai': id_tanah_negara_sudah_dikuasai,
            'id_tanah_kas_desa_sudah_dikuasai': id_tanah_kas_desa_sudah_dikuasai,
            'id_tanah_hak_pakai_sudah_dikuasai': id_tanah_hak_pakai_sudah_dikuasai,
            'id_tanah_hak_guna_bangunan_sudah_dikuasai': id_tanah_hak_guna_bangunan_sudah_dikuasai,
            'id_tanah_hak_milik_sertifikat_sudah_dikuasai': id_tanah_hak_milik_sertifikat_sudah_dikuasai,
            'id_tanah_adat_sudah_dikuasai': id_tanah_adat_sudah_dikuasai,
            'id_pemegang_hak_semula_dari_tanah_sudah_dikuasai': id_pemegang_hak_semula_dari_tanah_sudah_dikuasai,
            'id_tanah_sudah_dikuasai_melalui': id_tanah_sudah_dikuasai_melalui,
            'id_jumlah_tanah_sudah_dikuasai': id_jumlah_tanah_sudah_dikuasai,
            'kabupaten' : kabupaten,
            'kecamatan' : kecamatan,
            'desa' : desa,
            }}
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

def load_data_rencana_pembangunan_ipptusaha(request,id_pengajuan):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            pengajuan_ = InformasiTanah.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
            id_tipe1 = pengajuan_.tipe1
            id_tipe2 = pengajuan_.tipe2
            id_tipe3 = pengajuan_.tipe3
            id_gudang1 = str(pengajuan_.gudang1)
            id_gudang2 = str(pengajuan_.gudang2)
            id_gudang3 = str(pengajuan_.gudang3)
            id_luas_tipe1 = str(pengajuan_.luas_tipe1)
            id_luas_tipe2 = str(pengajuan_.luas_tipe2)
            id_luas_tipe3 = str(pengajuan_.luas_tipe3)

            id_luas_lapangan = str(pengajuan_.luas_lapangan)
            id_luas_kantor = str(pengajuan_.luas_kantor)
            id_luas_saluran = str(pengajuan_.luas_saluran)
            id_luas_taman = str(pengajuan_.luas_taman)
            id_jumlah_perincian_penggunaan_tanah = str(pengajuan_.jumlah_perincian_penggunaan_tanah)
            id_pematangan_tanah_tahap1 = str(pengajuan_.pematangan_tanah_tahap1)
            id_pematangan_tanah_tahap2 = str(pengajuan_.pematangan_tanah_tahap2)
            id_pematangan_tanah_tahap3 = str(pengajuan_.pematangan_tanah_tahap3)
            id_pembangunan_gedung_tahap1 = str(pengajuan_.pembangunan_gedung_tahap1)
            id_pembangunan_gedung_tahap2 = str(pengajuan_.pembangunan_gedung_tahap2)
            id_pembangunan_gedung_tahap3 = str(pengajuan_.pembangunan_gedung_tahap3)

            id_jangka_waktu_selesai = str(pengajuan_.jangka_waktu_selesai)
            id_presentase_luas_tipe1 = str(pengajuan_.presentase_luas_tipe1)
            id_presentase_luas_tipe2 = str(pengajuan_.presentase_luas_tipe2)
            id_presentase_luas_tipe3 = str(pengajuan_.presentase_luas_tipe3)
            id_presentase_luas_lapangan = str(pengajuan_.presentase_luas_lapangan)
            id_presentase_luas_kantor = str(pengajuan_.presentase_luas_kantor)
            id_presentase_luas_saluran = str(pengajuan_.presentase_luas_saluran)
            id_presentase_luas_taman = str(pengajuan_.presentase_luas_taman)
            id_presentase_jumlah_perincian_penggunaan_tanah = str(pengajuan_.presentase_jumlah_perincian_penggunaan_tanah)

            data = {'success': True,'data': {
            'id_tipe1': id_tipe1,
            'id_tipe2': id_tipe2,
            'id_tipe3': id_tipe3,
            'id_gudang1': id_gudang1,
            'id_gudang2': id_gudang2,
            'id_gudang3': id_gudang3,
            'id_luas_tipe1': id_luas_tipe1,
            'id_luas_tipe2': id_luas_tipe2,
            'id_luas_tipe3': id_luas_tipe3,
            'id_luas_lapangan': id_luas_lapangan,
            'id_luas_kantor': id_luas_kantor,
            'id_luas_saluran': id_luas_saluran,
            'id_luas_taman': id_luas_taman,
            'id_jumlah_perincian_penggunaan_tanah': id_jumlah_perincian_penggunaan_tanah,
            'id_pematangan_tanah_tahap1': id_pematangan_tanah_tahap1,
            'id_pematangan_tanah_tahap2': id_pematangan_tanah_tahap2,
            'id_pematangan_tanah_tahap3': id_pematangan_tanah_tahap3,
            'id_pembangunan_gedung_tahap1': id_pembangunan_gedung_tahap1,
            'id_pembangunan_gedung_tahap2': id_pembangunan_gedung_tahap2,
            'id_pembangunan_gedung_tahap3': id_pembangunan_gedung_tahap3,

            'id_jangka_waktu_selesai': id_jangka_waktu_selesai,
            'id_presentase_luas_tipe1': id_presentase_luas_tipe1,
            'id_presentase_luas_tipe2': id_presentase_luas_tipe2,
            'id_presentase_luas_tipe3': id_presentase_luas_tipe3,
            'id_presentase_luas_lapangan': id_presentase_luas_lapangan,
            'id_presentase_luas_kantor': id_presentase_luas_kantor,
            'id_presentase_luas_saluran': id_presentase_luas_saluran,
            'id_presentase_luas_taman': id_presentase_luas_taman,
            'id_presentase_jumlah_perincian_penggunaan_tanah': id_presentase_jumlah_perincian_penggunaan_tanah
            }}
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

def load_data_pembiayaan_dan_pemodalan_ipptusaha(request,id_pengajuan):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            pengajuan_ = InformasiTanah.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
            id_modal_tetap_tanah = pengajuan_.modal_tetap_tanah
            id_modal_tetap_bangunan = pengajuan_.modal_tetap_bangunan
            id_modal_tetap_mesin = pengajuan_.modal_tetap_mesin
            id_modal_tetap_angkutan = pengajuan_.modal_tetap_angkutan
            id_modal_tetap_inventaris = pengajuan_.modal_tetap_inventaris
            id_modal_tetap_lainnya = pengajuan_.modal_tetap_lainnya
            id_jumlah_modal_tetap = pengajuan_.jumlah_modal_tetap

            id_modal_kerja_bahan = pengajuan_.modal_kerja_bahan
            id_modal_kerja_gaji = pengajuan_.modal_kerja_gaji
            id_modal_kerja_alat_angkut = pengajuan_.modal_kerja_alat_angkut
            id_modal_kerja_lainnya = pengajuan_.modal_kerja_lainnya
            id_jumlah_modal_kerja = pengajuan_.jumlah_modal_kerja

            if pengajuan_.jumlah_modal_tetap or pengajuan_.jumlah_modal_kerja != '':
                id_jumlah_rencana_biaya = int(id_jumlah_modal_tetap.replace(".",""))+int(id_jumlah_modal_kerja.replace(".",""))
            else:
                id_jumlah_rencana_biaya = 0

            id_modal_dasar = pengajuan_.modal_dasar
            id_modal_ditetapkan = pengajuan_.modal_ditetapkan
            id_modal_disetor = pengajuan_.modal_disetor

            id_modal_bank_pemerintah = pengajuan_.modal_bank_pemerintah
            id_modal_bank_swasta = pengajuan_.modal_bank_swasta
            id_modal_lembaga_non_bank = pengajuan_.modal_lembaga_non_bank
            id_modal_pihak_ketiga = pengajuan_.modal_pihak_ketiga

            if id_modal_bank_pemerintah or id_modal_bank_swasta or id_modal_lembaga_non_bank or id_modal_pihak_ketiga != '':
                id_jumlah_pinjaman_dalam = int(id_modal_bank_pemerintah.replace(".",""))+int(id_modal_bank_swasta.replace(".",""))+int(id_modal_lembaga_non_bank.replace(".",""))+int(id_modal_pihak_ketiga.replace(".",""))
            else:
                id_jumlah_pinjaman_dalam = 0

            id_modal_pinjaman_luar_negeri = pengajuan_.modal_pinjaman_luar_negeri
            id_jumlah_investasi = pengajuan_.jumlah_investasi

            id_saham_indonesia = str(pengajuan_.saham_indonesia)
            id_saham_asing = str(pengajuan_.saham_asing)
            id_jumlah_saham = str(pengajuan_.saham_indonesia + pengajuan_.saham_asing)

            data = {'success': True,'data': {
            'id_modal_tetap_tanah': id_modal_tetap_tanah,
            'id_modal_tetap_bangunan': id_modal_tetap_bangunan,
            'id_modal_tetap_mesin': id_modal_tetap_mesin,
            'id_modal_tetap_angkutan': id_modal_tetap_angkutan,
            'id_modal_tetap_inventaris': id_modal_tetap_inventaris,
            'id_modal_tetap_lainnya': id_modal_tetap_lainnya,
            'id_jumlah_modal_tetap': id_jumlah_modal_tetap,

            'id_modal_kerja_bahan': id_modal_kerja_bahan,
            'id_modal_kerja_gaji': id_modal_kerja_gaji,
            'id_modal_kerja_alat_angkut': id_modal_kerja_alat_angkut,
            'id_modal_kerja_lainnya': id_modal_kerja_lainnya,
            'id_jumlah_modal_kerja': id_jumlah_modal_kerja,
            'id_jumlah_rencana_biaya':id_jumlah_rencana_biaya,

            'id_modal_dasar': id_modal_dasar,
            'id_modal_ditetapkan': id_modal_ditetapkan,
            'id_modal_disetor': id_modal_disetor,
            'id_modal_bank_pemerintah': id_modal_bank_pemerintah,
            'id_modal_bank_swasta': id_modal_bank_swasta,
            'id_modal_lembaga_non_bank': id_modal_lembaga_non_bank,
            'id_modal_pihak_ketiga': id_modal_pihak_ketiga,
            'id_jumlah_pinjaman_dalam': id_jumlah_pinjaman_dalam,
            'id_modal_pinjaman_luar_negeri': id_modal_pinjaman_luar_negeri,
            'id_jumlah_investasi': id_jumlah_investasi,

            'id_saham_indonesia': id_saham_indonesia,
            'id_saham_asing': id_saham_asing,
            'id_jumlah_saham':id_jumlah_saham,

            }}
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

def load_data_kebutuhan_lainnya_ipptusaha(request,id_pengajuan):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            pengajuan_ = InformasiTanah.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
            id_tenaga_ahli = pengajuan_.tenaga_ahli
            id_pegawai_tetap = pengajuan_.pegawai_tetap
            id_pegawai_harian_tetap = pengajuan_.pegawai_harian_tetap
            id_pegawai_harian_tidak_tetap = pengajuan_.pegawai_harian_tidak_tetap
            id_kebutuhan_listrik = pengajuan_.kebutuhan_listrik
            id_kebutuhan_listrik_sehari_hari = pengajuan_.kebutuhan_listrik_sehari_hari
            id_jumlah_daya_genset = pengajuan_.jumlah_daya_genset
            id_jumlah_listrik_kebutuhan_dari_pln = pengajuan_.jumlah_listrik_kebutuhan_dari_pln

            id_air_untuk_rumah_tangga = str(pengajuan_.air_untuk_rumah_tangga)
            id_air_untuk_produksi = str(pengajuan_.air_untuk_produksi)
            id_air_lainnya = str(pengajuan_.air_lainnya)
            id_air_dari_pdam = str(pengajuan_.air_dari_pdam)
            id_air_dari_sumber = str(pengajuan_.air_dari_sumber)
            id_air_dari_sungai = str(pengajuan_.air_dari_sungai)

            id_tenaga_kerja_wni = pengajuan_.tenaga_kerja_wni
            id_tenaga_kerja_wna = pengajuan_.tenaga_kerja_wna
            id_tenaga_kerja_tetap = pengajuan_.tenaga_kerja_tetap
            id_tenaga_kerja_tidak_tetap = pengajuan_.tenaga_kerja_tidak_tetap

            data = {'success': True,'data': {
            'id_tenaga_ahli': id_tenaga_ahli,
            'id_pegawai_tetap': id_pegawai_tetap,
            'id_pegawai_harian_tetap': id_pegawai_harian_tetap,
            'id_pegawai_harian_tidak_tetap': id_pegawai_harian_tidak_tetap,
            'id_kebutuhan_listrik': id_kebutuhan_listrik,
            'id_kebutuhan_listrik_sehari_hari': id_kebutuhan_listrik_sehari_hari,
            'id_jumlah_daya_genset': id_jumlah_daya_genset,
            'id_jumlah_listrik_kebutuhan_dari_pln': id_jumlah_listrik_kebutuhan_dari_pln,
            'id_air_untuk_rumah_tangga': id_air_untuk_rumah_tangga,
            'id_air_untuk_produksi': id_air_untuk_produksi,
            'id_air_lainnya': id_air_lainnya,
            'id_air_dari_pdam': id_air_dari_pdam,
            'id_air_dari_sumber': id_air_dari_sumber,
            'id_air_dari_sungai': id_air_dari_sungai,
            'id_tenaga_kerja_wni': id_tenaga_kerja_wni,
            'id_tenaga_kerja_wna': id_tenaga_kerja_wna,
            'id_tenaga_kerja_tetap': id_tenaga_kerja_tetap,
            'id_tenaga_kerja_tidak_tetap': id_tenaga_kerja_tidak_tetap,


            }}
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

def load_data_penggunaan_tanah_ipptusaha(request,id_pengajuan):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            data = []
            i = PenggunaanTanahIPPTUsaha.objects.filter(informasi_tanah_id=request.COOKIES['id_pengajuan'])
            data = [ob.as_json() for ob in i]
            response = HttpResponse(json.dumps(data), content_type="application/json")
    return response

def load_data_perumahan_yang_dimiliki_ipptusaha(request,id_pengajuan):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            data = []
            i = PerumahanYangDimilikiIPPTUsaha.objects.filter(informasi_tanah_id=request.COOKIES['id_pengajuan'])
            data = [ob.as_json() for ob in i]
            response = HttpResponse(json.dumps(data), content_type="application/json")
    return response

def cetak_ippt_usaha(request, id_pengajuan_):
      extra_context = {}
      url_ = reverse('formulir_reklame')
      if id_pengajuan_:
        pengajuan_ = InformasiTanah.objects.get(id=id_pengajuan_)
        if pengajuan_.perusahaan != '':
          alamat_ = ""
          alamat_perusahaan_ = ""
          if pengajuan_.pemohon:
            if pengajuan_.pemohon.desa:
              alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.pemohon.desa.kecamatan.kabupaten.nama_kabupaten.title())
              extra_context.update({ 'alamat_pemohon': alamat_ })
            extra_context.update({ 'pemohon': pengajuan_.pemohon })

          if pengajuan_.perusahaan:
            if pengajuan_.perusahaan.desa:
              alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
              extra_context.update({ 'alamat_perusahaan': alamat_perusahaan_ })
            extra_context.update({ 'perusahaan': pengajuan_.perusahaan })

          extra_context.update({ 'pengajuan': pengajuan_ })
          pengajuan_id = base64.b64encode(str(pengajuan_.id))
          extra_context.update({ 'pengajuan_id': pengajuan_id })

          riwayat = Riwayat.objects.filter(pengajuan_izin=pengajuan_)
          if riwayat:
            extra_context.update({ 'riwayat': riwayat })
            extra_context.update({ 'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin })
            extra_context.update({ 'created_at': pengajuan_.created_at })
          response = loader.get_template("front-end/include/formulir_ippt_usaha/cetak.html")
        else:
          response = HttpResponseRedirect(url_)
          return response
      else:
        response = HttpResponseRedirect(url_)
        return response
      template = loader.get_template("front-end/include/formulir_ippt_usaha/cetak.html")
      ec = RequestContext(request, extra_context)
      return HttpResponse(template.render(ec))

def formatrupiah(uang):
    y = str(uang)
    if len(y) <= 3 :
        return y     
    else :
        p = y[-3:]
        q = y[:-3]
        return   formatrupiah(q) + '.' + p

def cetak_bukti_pendaftaran_ippt_usaha(request,id_pengajuan_):
  extra_context = {}
  if id_pengajuan_:
    pengajuan_ = InformasiTanah.objects.get(id=id_pengajuan_)
    if pengajuan_.perusahaan != '':
      alamat_ = ""
      alamat_perusahaan_ = ""
      if pengajuan_.pemohon:
        if pengajuan_.pemohon.desa:
          alamat_ = str(pengajuan_.pemohon.alamat)+", DESA "+str(pengajuan_.pemohon.desa)+", KEC. "+str(pengajuan_.pemohon.desa.kecamatan)+", "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
          extra_context.update({ 'alamat_pemohon': alamat_ })
        extra_context.update({ 'pemohon': pengajuan_.pemohon })
        paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
        ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
        legalitas_list = pengajuan_.perusahaan.legalitas_set.all()
        penggunaan_tanah_list = pengajuan_.penggunaantanahipptusaha_set.all()
        perumahan_yang_dimiliki_list = pengajuan_.perumahanyangdimilikiipptusaha_set.all()

        if pengajuan_.jumlah_modal_tetap or pengajuan_.jumlah_modal_kerja != '':
            jumlah_rencana_biaya = int(pengajuan_.jumlah_modal_tetap.replace(".",""))+int(pengajuan_.jumlah_modal_kerja.replace(".",""))
        else:
            jumlah_rencana_biaya = ""

        if pengajuan_.modal_bank_pemerintah or pengajuan_.modal_bank_swasta or pengajuan_.modal_lembaga_non_bank or pengajuan_.modal_pihak_ketiga != '':
            jumlah_pinjaman_dalam = int(pengajuan_.modal_bank_pemerintah.replace(".",""))+int(pengajuan_.modal_bank_swasta.replace(".",""))+int(pengajuan_.modal_lembaga_non_bank.replace(".",""))+int(pengajuan_.modal_pihak_ketiga.replace(".",""))
        else:
            jumlah_pinjaman_dalam = ""

        jumlah_saham = str(pengajuan_.saham_indonesia + pengajuan_.saham_asing)
        jumlah_kebutuhan_air = str(pengajuan_.air_untuk_rumah_tangga + pengajuan_.air_untuk_produksi + pengajuan_.air_lainnya)
        jumlah_minimal_kebutuhan_air = str(pengajuan_.air_dari_pdam + pengajuan_.air_dari_sumber + pengajuan_.air_dari_sungai)

        if pengajuan_.tenaga_kerja_wni or pengajuan_.tenaga_kerja_wna or pengajuan_.tenaga_kerja_tetap or pengajuan_.tenaga_kerja_tidak_tetap != None:
            jumlah_tenaga_kerja = pengajuan_.tenaga_kerja_wni + pengajuan_.tenaga_kerja_wna + pengajuan_.tenaga_kerja_tetap + pengajuan_.tenaga_kerja_tidak_tetap
        else:
            jumlah_tenaga_kerja = ""

        extra_context.update({ 'paspor': paspor_ })
        extra_context.update({ 'ktp': ktp_ })
        extra_context.update({ 'legalitas_list': legalitas_list })
        extra_context.update({ 'penggunaan_tanah_list': penggunaan_tanah_list })
        extra_context.update({ 'perumahan_yang_dimiliki_list': perumahan_yang_dimiliki_list })
        extra_context.update({ 'jumlah_rencana_biaya': jumlah_rencana_biaya })
        extra_context.update({ 'jumlah_pinjaman_dalam': formatrupiah(jumlah_pinjaman_dalam) })
        extra_context.update({ 'jumlah_saham': jumlah_saham })
        extra_context.update({ 'jumlah_kebutuhan_air': jumlah_kebutuhan_air })
        extra_context.update({ 'jumlah_minimal_kebutuhan_air': jumlah_minimal_kebutuhan_air })
        extra_context.update({ 'jumlah_tenaga_kerja': jumlah_tenaga_kerja })
      if pengajuan_.perusahaan:
        if pengajuan_.perusahaan.desa:
          alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", DESA "+str(pengajuan_.perusahaan.desa)+", KEC. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
          extra_context.update({ 'alamat_perusahaan': alamat_perusahaan_ })
        extra_context.update({ 'perusahaan': pengajuan_.perusahaan })
        syarat_ = Syarat.objects.filter(jenis_izin__jenis_izin__kode="IL")
        extra_context.update({ 'syarat': syarat_ })
      if pengajuan_.desa:
        letak_ = pengajuan_.alamat + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
      else:
        letak_ = pengajuan_.alamat

      extra_context.update({'letak_': letak_})
      extra_context.update({ 'pengajuan': pengajuan_ })
      extra_context.update({ 'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin })
      extra_context.update({ 'created_at': pengajuan_.created_at })
      response = loader.get_template("front-end/include/formulir_ippt_usaha/cetak_bukti_pendaftaran.html")
    else:
      response = HttpResponseRedirect(url_)
      return response
  else:
    response = HttpResponseRedirect(url_)
    return response 

  template = loader.get_template("front-end/include/formulir_ippt_usaha/cetak_bukti_pendaftaran.html")
  ec = RequestContext(request, extra_context)
  return HttpResponse(template.render(ec))