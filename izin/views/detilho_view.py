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
from accounts.utils import KETERANGAN_PEKERJAAN

def formulir_ho(request, extra_context={}):
    jenis_pemohon = JenisPemohon.objects.all()
    negara = Negara.objects.all()
    kecamatan = Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35')

    extra_context.update({'jenis_lokasi_usaha_list': JENIS_LOKASI_USAHA})
    extra_context.update({'jenis_bangunan_list': JENIS_BANGUNAN})
    extra_context.update({'jenis_gangguan_list': JENIS_GANGGUAN})
    extra_context.update({'keterangan_pekerjaan': KETERANGAN_PEKERJAAN })
    extra_context.update({'negara': negara})
    extra_context.update({'kecamatan': kecamatan})
    extra_context.update({'jenis_pemohon': jenis_pemohon})
    if 'id_pengajuan' in request.COOKIES.keys():
      if request.COOKIES['id_pengajuan'] != "":
        print request.COOKIES['id_pengajuan']
        try:
          pengajuan_ = DetilHO.objects.get(id=request.COOKIES['id_pengajuan'])
          print pengajuan_
          alamat_ = ""
          alamat_perusahaan_ = ""
          if pengajuan_.pemohon:
            if pengajuan_.pemohon.desa:
              alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
              extra_context.update({ 'alamat_pemohon_konfirmasi': alamat_ })
            extra_context.update({ 'pemohon_konfirmasi': pengajuan_.pemohon })
            extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
            ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
            extra_context.update({ 'ktp': ktp_ })
            paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
            extra_context.update({ 'paspor': paspor_ })
            extra_context.update({'cookie_file_ktp': ktp_.berkas })
          if pengajuan_.perusahaan:
            if pengajuan_.perusahaan.desa:
              alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
              extra_context.update({ 'alamat_perusahaan_konfirmasi': alamat_perusahaan_ })
            extra_context.update({ 'perusahaan_konfirmasi': pengajuan_.perusahaan })
          # ukuran_ = "Lebar = "+str(int(pengajuan_.lebar))+" M , Tinggi = "+str(int(pengajuan_.tinggi))+" M"

          extra_context.update({ 'no_pengajuan_konfirmasi': pengajuan_.no_pengajuan })
          extra_context.update({ 'jenis_permohonan_konfirmasi': pengajuan_.jenis_permohonan })
          extra_context.update({ 'pengajuan_': pengajuan_ })
          # extra_context.update({ 'ukuran': ukuran_ })

          if pengajuan_.desa:
            letak_ = pengajuan_.alamat + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
          else:
            letak_ = ""
          extra_context.update({ 'letak': letak_ })
        except ObjectDoesNotExist:
          pass
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
                'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
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
      try:
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
        response.delete_cookie(key='kode_kelompok_jenis_izin') # set cookie
        response.delete_cookie(key='npwp_perusahaan') # set cookie
      except ObjectDoesNotExist:
        data = {'success': False, 'pesan': 'Data tidak ditemukan.' }
        response = HttpResponse(json.dumps(data))
    else:
      data = {'success': False, 'pesan': 'Data tidak ditemukan.' }
      response = HttpResponse(json.dumps(data))
  else:
    data = {'success': False, 'pesan': 'Data tidak ditemukan.' }
    response = HttpResponse(json.dumps(data))
  return response

def load_detilho(request, id_pengajuan):
  data = {'success': False, 'pesan': 'Terjadi Kesalahan. Data tidak ditemukan atau tidak.'}
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
      try:
        pengajuan_ = DetilHO.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
        id_perkiraan_modal = 0
        if pengajuan_.perkiraan_modal:
          id_perkiraan_modal = str(pengajuan_.perkiraan_modal)
        id_tujuan_gangguan = pengajuan_.tujuan_gangguan
        id_alamat = pengajuan_.alamat
        id_surat_tanah = pengajuan_.no_surat_tanah
        if pengajuan_.tanggal_surat_tanah:
          id_tanggal_surat_tanah = pengajuan_.tanggal_surat_tanah.strftime("%d-%m-%Y")
        else:
          id_tanggal_surat_tanah = ""
        if pengajuan_.desa:
          id_desa = str(pengajuan_.desa.id)
          id_kecamatan = str(pengajuan_.desa.kecamatan.id)
        else:
          id_desa = ""
          id_kecamatan = ""
        id_bahan_baku_dan_penolong = pengajuan_.bahan_baku_dan_penolong
        id_proses_produksi = pengajuan_.proses_produksi
        id_jenis_produksi = pengajuan_.jenis_produksi
        id_kapasitas_produksi = pengajuan_.kapasitas_produksi
        id_jumlah_tenaga_kerja = str(pengajuan_.jumlah_tenaga_kerja)
        id_jumlah_mesin = str(pengajuan_.jumlah_mesin)
        id_merk_mesin = pengajuan_.merk_mesin
        id_daya = pengajuan_.daya
        id_kekuatan = pengajuan_.kekuatan
        id_luas_ruang_tempat_usaha = str(pengajuan_.luas_ruang_tempat_usaha)
        id_luas_lahan_usaha = str(pengajuan_.luas_lahan_usaha)
        id_jenis_lokasi_usaha = pengajuan_.jenis_lokasi_usaha
        id_jenis_bangunan = pengajuan_.jenis_bangunan
        id_jenis_gangguan = pengajuan_.jenis_gangguan

        data = {'success': True, 'pesan': 'Data berhasil diload.',
            'data': {'id_perkiraan_modal': id_perkiraan_modal,'id_tujuan_gangguan': id_tujuan_gangguan,'id_alamat': id_alamat,'id_surat_tanah':id_surat_tanah,'id_tanggal_surat_tanah':id_tanggal_surat_tanah,'id_desa': id_desa,'id_kecamatan': id_kecamatan,'id_bahan_baku_dan_penolong': id_bahan_baku_dan_penolong,'id_proses_produksi': id_proses_produksi,'id_jenis_produksi': id_jenis_produksi,'id_kapasitas_produksi': id_kapasitas_produksi,'id_jumlah_tenaga_kerja': id_jumlah_tenaga_kerja,'id_jumlah_mesin': id_jumlah_mesin,'id_merk_mesin': id_merk_mesin,'id_daya': id_daya,'id_kekuatan': id_kekuatan,'id_luas_ruang_tempat_usaha': id_luas_ruang_tempat_usaha,'id_luas_lahan_usaha': id_luas_lahan_usaha,'id_jenis_lokasi_usaha': id_jenis_lokasi_usaha,'id_jenis_bangunan': id_jenis_bangunan,'id_jenis_gangguan': id_jenis_gangguan, 'batas_utara': pengajuan_.batas_utara, 'batas_selatan': pengajuan_.batas_selatan, 'batas_barat': pengajuan_.batas_barat, 'batas_timur': pengajuan_.batas_timur}}
      except ObjectDoesNotExist:
        pass
  response = HttpResponse(json.dumps(data))
  return response

def load_konfirmasi_detilho(request,id_pengajuan):
  data = {'success': False, 'pesan': 'Terjadi Kesalahan. Data tidak ditemukan atau tidak.'}
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
      try:
        pengajuan_ = DetilHO.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
        perkiraan_modal = str(pengajuan_.perkiraan_modal)
        tujuan_gangguan = pengajuan_.tujuan_gangguan
        alamat = pengajuan_.alamat
        desa = str(pengajuan_.desa)
        kecamatan = str(pengajuan_.desa.kecamatan)
        kabupaten = str(pengajuan_.desa.kecamatan.kabupaten)
        bahan_baku_dan_penolong = pengajuan_.bahan_baku_dan_penolong
        proses_produksi = pengajuan_.proses_produksi
        jenis_produksi = pengajuan_.jenis_produksi
        kapasitas_produksi = pengajuan_.kapasitas_produksi
        jumlah_tenaga_kerja = str(pengajuan_.jumlah_tenaga_kerja)
        jumlah_mesin = str(pengajuan_.jumlah_mesin)
        merk_mesin = pengajuan_.merk_mesin
        daya = pengajuan_.daya
        kekuatan = pengajuan_.kekuatan
        luas_ruang_tempat_usaha = str(pengajuan_.luas_ruang_tempat_usaha)
        luas_lahan_usaha = str(pengajuan_.luas_lahan_usaha)
        jenis_lokasi_usaha = pengajuan_.jenis_lokasi_usaha
        jenis_bangunan = pengajuan_.jenis_bangunan
        jenis_gangguan = pengajuan_.jenis_gangguan
        surat_tanah = pengajuan_.no_surat_tanah
        if pengajuan_.tanggal_surat_tanah:
          tanggal_surat_tanah = pengajuan_.tanggal_surat_tanah.strftime("%d-%m-%Y")
        else:
          tanggal_surat_tanah = ""
        data = {'success': True,
            'data': [
            {'perkiraan_modal': perkiraan_modal},
            {'tujuan_gangguan': tujuan_gangguan},
            {'alamat_ho': alamat},
            {'surat_tanah': surat_tanah},
            {'tanggal_surat_tanah': tanggal_surat_tanah},
            {'desa': desa},
            {'kecamatan': kecamatan},
            {'kabupaten': kabupaten},
            {'bahan_baku_dan_penolong': bahan_baku_dan_penolong},
            {'proses_produksi': proses_produksi},
            {'jenis_produksi': jenis_produksi},
            {'kapasitas_produksi': kapasitas_produksi},
            {'jumlah_tenaga_kerja': jumlah_tenaga_kerja},
            {'jumlah_mesin': jumlah_mesin},
            {'merk_mesin': merk_mesin},
            {'daya': daya},
            {'kekuatan': kekuatan},
            {'luas_ruang_tempat_usaha': luas_ruang_tempat_usaha},
            {'luas_lahan_usaha': luas_lahan_usaha},
            {'jenis_lokasi_usaha': jenis_lokasi_usaha},
            {'jenis_bangunan': jenis_bangunan},
            {'jenis_gangguan': jenis_gangguan}]}
      except ObjectDoesNotExist:
        pass
  response = HttpResponse(json.dumps(data))
  return response


def detilho_upload_berkas_pendukung(request):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
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
                berkas = form.save(commit=False)
                if request.POST.get('aksi') == "1":
                  berkas.nama_berkas = "File Izin Mendirikan Bangunan (IMB)"+p.no_pengajuan
                  berkas.keterangan = "File Izin Mendirikan Bangunan (IMB)"
                elif request.POST.get('aksi') == "2":
                  berkas.nama_berkas = "Surat Kepemilikan Tanah atau Surat Penguasaan Hak atas Tanah (Sertifikat / Akta Jual Beli / Petok D / Surat Keterangan Tanah)"+p.no_pengajuan
                  berkas.keterangan = "Surat Kepemilikan Tanah atau Surat Penguasaan Hak atas Tanah (Sertifikat / Akta Jual Beli / Petok D / Surat Keterangan Tanah)"
                elif request.POST.get('aksi') == "3":
                  berkas.nama_berkas = "File Rencana Teknis Bangunan Gedung(Denah Bangunan, Site Plan, Spesifikasi Teknis) yang disahkan oleh Instansi Teknis yang membidangi"+p.no_pengajuan
                  berkas.keterangan = "File Rencana Teknis Bangunan Gedung(Denah Bangunan, Site Plan, Spesifikasi Teknis) yang disahkan oleh Instansi Teknis yang membidangi"
                elif request.POST.get('aksi') == "4":
                  berkas.nama_berkas = "File KTP/Paspor (Dirut / Pemilik / Pengurus / Penanggung Jawab)"+p.no_pengajuan
                  berkas.keterangan = "File KTP/Paspor (Dirut / Pemilik / Pengurus / Penanggung Jawab)"
                elif request.POST.get('aksi') == "5":
                  berkas.nama_berkas = "File NPWP Pribadi"+p.no_pengajuan
                  berkas.keterangan = "File NPWP Pribadi"
                elif request.POST.get('aksi') == "6":
                  berkas.nama_berkas = "File NPWP Perusahaan"+p.no_pengajuan
                  berkas.keterangan = "File NPWP Perusahaan"
                else:
                  berkas.nama_berkas = "File Surat Kuasa bagi yang Mewakili Perusahaan/Badan Hukum"+p.no_pengajuan
                  berkas.keterangan = "File Surat Kuasa bagi yang Mewakili Perusahaan/Badan Hukum"
                  
                if request.user.is_authenticated():
                  berkas.created_by_id = request.user.id
                else:
                  berkas.created_by_id = request.COOKIES['id_pemohon']
                berkas.save()
                p.berkas_tambahan.add(berkas)
                p.berkas_terkait_izin.add(berkas)

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

def ajax_load_berkas_detilho(request, id_pengajuan):
  url_berkas = []
  id_elemen = []
  nm_berkas =[]
  id_berkas =[]
  if id_pengajuan:
    try:
      p = PengajuanIzin.objects.get(id=request.COOKIES['id_pengajuan'])

      file_izin_mendirikan_bangunan = Berkas.objects.filter(nama_berkas="File Izin Mendirikan Bangunan (IMB)"+p.no_pengajuan)
      if file_izin_mendirikan_bangunan.exists():
        file_izin_mendirikan_bangunan = file_izin_mendirikan_bangunan.last()
        url_berkas.append(file_izin_mendirikan_bangunan.berkas.url)
        id_elemen.append('file_izin_mendirikan_bangunan')
        nm_berkas.append("File Izin Mendirikan Bangunan (IMB)"+p.no_pengajuan)
        id_berkas.append(file_izin_mendirikan_bangunan.id)

      kepemilikan_tanah = Berkas.objects.filter(nama_berkas="Surat Kepemilikan Tanah atau Surat Penguasaan Hak atas Tanah (Sertifikat / Akta Jual Beli / Petok D / Surat Keterangan Tanah)"+p.no_pengajuan)
      if kepemilikan_tanah.exists():
        kepemilikan_tanah = kepemilikan_tanah.last()
        url_berkas.append(kepemilikan_tanah.berkas.url)
        id_elemen.append('kepemilikan_tanah')
        nm_berkas.append("Surat Kepemilikan Tanah atau Surat Penguasaan Hak atas Tanah (Sertifikat / Akta Jual Beli / Petok D / Surat Keterangan Tanah)"+p.no_pengajuan)
        id_berkas.append(kepemilikan_tanah.id)

      cetak_biru = Berkas.objects.filter(nama_berkas="File Rencana Teknis Bangunan Gedung(Denah Bangunan, Site Plan, Spesifikasi Teknis) yang disahkan oleh Instansi Teknis yang membidangi"+p.no_pengajuan)
      if cetak_biru.exists():
        cetak_biru = cetak_biru.last()
        url_berkas.append(cetak_biru.berkas.url)
        id_elemen.append('cetak_biru')
        nm_berkas.append("File Rencana Teknis Bangunan Gedung(Denah Bangunan, Site Plan, Spesifikasi Teknis) yang disahkan oleh Instansi Teknis yang membidangi"+p.no_pengajuan)
        id_berkas.append(cetak_biru.id)

      upload_gambar_ktp = Berkas.objects.filter(nama_berkas="File KTP/Paspor (Dirut / Pemilik / Pengurus / Penanggung Jawab)"+p.no_pengajuan)
      if upload_gambar_ktp.exists():
        upload_gambar_ktp = upload_gambar_ktp.last()
        url_berkas.append(upload_gambar_ktp.berkas.url)
        id_elemen.append('upload_gambar_ktp')
        nm_berkas.append("File KTP/Paspor (Dirut / Pemilik / Pengurus / Penanggung Jawab)"+p.no_pengajuan)
        id_berkas.append(upload_gambar_ktp.id)

      file_npwp_pribadi = Berkas.objects.filter(nama_berkas="File NPWP Pribadi"+p.no_pengajuan)
      if file_npwp_pribadi.exists():
        file_npwp_pribadi = file_npwp_pribadi.last()
        url_berkas.append(file_npwp_pribadi.berkas.url)
        id_elemen.append('file_npwp_pribadi')
        nm_berkas.append("File NPWP Pribadi"+p.no_pengajuan)
        id_berkas.append(file_npwp_pribadi.id)

      file_npwp_perusahaan = Berkas.objects.filter(nama_berkas="File NPWP Perusahaan"+p.no_pengajuan)
      if file_npwp_perusahaan.exists():
        file_npwp_perusahaan = file_npwp_perusahaan.last()
        url_berkas.append(file_npwp_perusahaan.berkas.url)
        id_elemen.append('file_npwp_perusahaan')
        nm_berkas.append("File NPWP Perusahaan"+p.no_pengajuan)
        id_berkas.append(file_npwp_perusahaan.id)

      file_surat_kuasa = Berkas.objects.filter(nama_berkas="File Surat Kuasa bagi yang Mewakili Perusahaan/Badan Hukum"+p.no_pengajuan)
      if file_surat_kuasa.exists():
        file_surat_kuasa = file_surat_kuasa.last()
        url_berkas.append(file_surat_kuasa.berkas.url)
        id_elemen.append('file_surat_kuasa')
        nm_berkas.append("File Surat Kuasa bagi yang Mewakili Perusahaan/Badan Hukum"+p.no_pengajuan)
        id_berkas.append(file_surat_kuasa.id)

      data = {'success': True, 'pesan': 'berkas pendukung Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
    except ObjectDoesNotExist:
      data = {'success': False, 'pesan': '' }
      
    
  response = HttpResponse(json.dumps(data))
  return response

def cetak_gangguan_ho(request, id_pengajuan_):
      extra_context = {}
      url_ = reverse('formulir_reklame')
      if id_pengajuan_:
        pengajuan_ = DetilHO.objects.get(id=id_pengajuan_)
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
          response = loader.get_template("front-end/include/formulir_ho/cetak.html")
        else:
          response = HttpResponseRedirect(url_)
          return response
      else:
        response = HttpResponseRedirect(url_)
        return response
      template = loader.get_template("front-end/include/formulir_ho/cetak.html")
      ec = RequestContext(request, extra_context)
      return HttpResponse(template.render(ec))

def cetak_bukti_pendaftaran_gangguan_ho(request,id_pengajuan_):
  extra_context = {}
  if id_pengajuan_:
    pengajuan_ = DetilHO.objects.get(id=id_pengajuan_)
    if pengajuan_.perusahaan != '':
      alamat_ = ""
      alamat_perusahaan_ = ""
      if pengajuan_.pemohon:
        if pengajuan_.pemohon.desa:
          alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.pemohon.desa.kecamatan.kabupaten.nama_kabupaten.title())
          extra_context.update({ 'alamat_pemohon': alamat_ })
        extra_context.update({ 'pemohon': pengajuan_.pemohon })
        paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
        ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
        extra_context.update({ 'paspor': paspor_ })
        extra_context.update({ 'ktp': ktp_ })
      if pengajuan_.perusahaan:
        if pengajuan_.perusahaan.desa:
          alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
          extra_context.update({ 'alamat_perusahaan': alamat_perusahaan_ })
        extra_context.update({ 'perusahaan': pengajuan_.perusahaan })
        syarat = Syarat.objects.filter(jenis_izin__jenis_izin__kode="HO")
      letak_ = pengajuan_.alamat + ", Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())

      extra_context.update({'letak_': letak_})
      extra_context.update({ 'pengajuan': pengajuan_ })
      extra_context.update({ 'syarat': syarat })
      extra_context.update({ 'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin })
      extra_context.update({ 'created_at': pengajuan_.created_at })
      response = loader.get_template("front-end/cetak_bukti_pendaftaran.html")
    else:
      response = HttpResponseRedirect(url_)
      return response
  else:
    response = HttpResponseRedirect(url_)
    return response 

  template = loader.get_template("front-end/include/formulir_ho/cetak_bukti_pendaftaran.html")
  ec = RequestContext(request, extra_context)
  return HttpResponse(template.render(ec))