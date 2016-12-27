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
from izin.models import PengajuanIzin, InformasiTanah,Pemohon
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna
from izin.izin_forms import UploadBerkasPendukungForm,InformasiTanahForm

def formulir_izin_lokasi(request, extra_context={}):
    jenis_pemohon = JenisPemohon.objects.all()
    negara = Negara.objects.all()
    kecamatan = Kecamatan.objects.filter(kabupaten_id=1083)

    extra_context.update({'negara': negara})
    extra_context.update({'kecamatan': kecamatan})
    extra_context.update({'jenis_pemohon': jenis_pemohon})
    if 'id_kelompok_izin' in request.COOKIES.keys():
        jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) 
        extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
    else:
        return HttpResponseRedirect(reverse('layanan'))
    return render(request, "front-end/formulir/izin_lokasi.html", extra_context)

def informasitanah_save_cookie(request):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            pengajuan_ = InformasiTanah.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
            informasitanah = InformasiTanahForm(request.POST, instance=pengajuan_)
            if informasitanah.is_valid():
                pengajuan_.perusahaan_id  = request.COOKIES['id_perusahaan']
                pengajuan_.save()
                data = {'success': True,
                        'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
                        'data': ['']}
                data = json.dumps(data)
                response = HttpResponse(json.dumps(data))
            else:
                data = informasitanah.errors.as_json()
        else:
            data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
            data = json.dumps(data)
    else:
        data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
        data = json.dumps(data)
    response = HttpResponse(data)
    return response

def izinlokasi_done(request):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
      pengajuan_ = InformasiTanah.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
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

def izinlokasi_upload_berkas_pendukung(request):
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
                  berkas.nama_berkas = "Bukti Kepemilikan Tanah"+p.no_pengajuan
                  berkas.keterangan = "Bukti Kepemilikan Tanah"
                elif request.POST.get('aksi') == "2":
                  berkas.nama_berkas = "Sketsa Lokasi Tanah Yang Dimohonkan"+p.no_pengajuan
                  berkas.keterangan = "Sketsa Lokasi Tanah Yang Dimohonkan"
                elif request.POST.get('aksi') == "3":
                  berkas.nama_berkas = "Gambar/Denah Rencana Penggunaan Tanah"+p.no_pengajuan
                  berkas.keterangan = "Gambar/Denah Rencana Penggunaan Tanah"
                elif request.POST.get('aksi') == "4":
                  berkas.nama_berkas = "Sertifikat Tanah"+p.no_pengajuan
                  berkas.keterangan = "Sertifikat Tanah"
                elif request.POST.get('aksi') == "5":
                  berkas.nama_berkas = "Akta Jual Beli"+p.no_pengajuan
                  berkas.keterangan = "Akta Jual Beli"
                else:
                  berkas.nama_berkas = "Rekomendasi Bupati/Izinizin lain yang diperoleh"+p.no_pengajuan
                  berkas.keterangan = "Rekomendasi Bupati/Izinizin lain yang diperoleh"
                  
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

def ajax_load_berkas_izinlokasi(request, id_pengajuan):
  url_berkas = []
  id_elemen = []
  nm_berkas =[]
  id_berkas =[]
  if id_pengajuan:
    try:
      p = PengajuanIzin.objects.get(id=request.COOKIES['id_pengajuan'])

      bukti_kepemilikan_tanah = Berkas.objects.filter(nama_berkas="Bukti Kepemilikan Tanah"+p.no_pengajuan)
      if bukti_kepemilikan_tanah.exists():
        bukti_kepemilikan_tanah = bukti_kepemilikan_tanah.last()
        url_berkas.append(bukti_kepemilikan_tanah.berkas.url)
        id_elemen.append('bukti_kepemilikan_tanah')
        nm_berkas.append("Bukti Kepemilikan Tanah"+p.no_pengajuan)
        id_berkas.append(bukti_kepemilikan_tanah.id)

      sketsa_lokasi_tanah = Berkas.objects.filter(nama_berkas="Sketsa Lokasi Tanah Yang Dimohonkan"+p.no_pengajuan)
      if sketsa_lokasi_tanah.exists():
        sketsa_lokasi_tanah = sketsa_lokasi_tanah.last()
        url_berkas.append(sketsa_lokasi_tanah.berkas.url)
        id_elemen.append('sketsa_lokasi_tanah')
        nm_berkas.append("Sketsa Lokasi Tanah Yang Dimohonkan"+p.no_pengajuan)
        id_berkas.append(sketsa_lokasi_tanah.id)

      gambar_rencana_penggunaan_tanah = Berkas.objects.filter(nama_berkas="Gambar/Denah Rencana Penggunaan Tanah"+p.no_pengajuan)
      if gambar_rencana_penggunaan_tanah.exists():
        gambar_rencana_penggunaan_tanah = gambar_rencana_penggunaan_tanah.last()
        url_berkas.append(gambar_rencana_penggunaan_tanah.berkas.url)
        id_elemen.append('gambar_rencana_penggunaan_tanah')
        nm_berkas.append("Gambar/Denah Rencana Penggunaan Tanah"+p.no_pengajuan)
        id_berkas.append(gambar_rencana_penggunaan_tanah.id)

      sertifikat_tanah = Berkas.objects.filter(nama_berkas="Sertifikat Tanah"+p.no_pengajuan)
      if sertifikat_tanah.exists():
        sertifikat_tanah = sertifikat_tanah.last()
        url_berkas.append(sertifikat_tanah.berkas.url)
        id_elemen.append('sertifikat_tanah')
        nm_berkas.append("Sertifikat Tanah"+p.no_pengajuan)
        id_berkas.append(sertifikat_tanah.id)

      akta_jual_beli = Berkas.objects.filter(nama_berkas="Akta Jual Beli"+p.no_pengajuan)
      if akta_jual_beli.exists():
        akta_jual_beli = akta_jual_beli.last()
        url_berkas.append(akta_jual_beli.berkas.url)
        id_elemen.append('akta_jual_beli')
        nm_berkas.append("Akta Jual Beli"+p.no_pengajuan)
        id_berkas.append(akta_jual_beli.id)

      rekomendasi_bupati = Berkas.objects.filter(nama_berkas="Rekomendasi Bupati/Izinizin lain yang diperoleh"+p.no_pengajuan)
      if rekomendasi_bupati.exists():
        rekomendasi_bupati = rekomendasi_bupati.last()
        url_berkas.append(rekomendasi_bupati.berkas.url)
        id_elemen.append('rekomendasi_bupati')
        nm_berkas.append("Rekomendasi Bupati/Izinizin lain yang diperoleh"+p.no_pengajuan)
        id_berkas.append(rekomendasi_bupati.id)

      data = {'success': True, 'pesan': 'berkas pendukung Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
    except ObjectDoesNotExist:
      data = {'success': False, 'pesan': '' }
      
    
  response = HttpResponse(json.dumps(data))
  return response

def load_konfirmasi_izin_lokasi(request,id_pengajuan):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
      pengajuan_ = InformasiTanah.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
      no_surat_kuasa = pengajuan_.no_surat_kuasa
      tanggal_surat_kuasa = str(pengajuan_.tanggal_surat_kuasa)
      alamat = pengajuan_.alamat
      desa = str(pengajuan_.desa)
      kecamatan = str(pengajuan_.desa.kecamatan)
      kabupaten = str(pengajuan_.desa.kecamatan.kabupaten)
      luas = str(pengajuan_.luas)
      status_tanah = pengajuan_.status_tanah
      no_sertifikat_petak = pengajuan_.no_sertifikat_petak
      luas_sertifikat_petak = str(pengajuan_.luas_sertifikat_petak)
      atas_nama_sertifikat_petak = pengajuan_.atas_nama_sertifikat_petak
      no_persil = pengajuan_.no_persil
      klas_persil = pengajuan_.klas_persil
      atas_nama_persil = pengajuan_.atas_nama_persil
      penggunaan_sekarang = pengajuan_.penggunaan_sekarang
      rencana_penggunaan = pengajuan_.rencana_penggunaan

      data = {'success': True,
          'data': [
          {'no_surat_kuasa': no_surat_kuasa},
          {'tanggal_surat_kuasa': tanggal_surat_kuasa},
          {'alamat_informasi_tanah': alamat},
          {'desa': desa},
          {'kecamatan': kecamatan},
          {'kabupaten': kabupaten},
          {'luas': luas},
          {'status_tanah': status_tanah},
          {'no_sertifikat_petak': no_sertifikat_petak},
          {'luas_sertifikat_petak': luas_sertifikat_petak},
          {'atas_nama_sertifikat_petak': atas_nama_sertifikat_petak},
          {'no_persil': no_persil},
          {'klas_persil': klas_persil},
          {'atas_nama_persil': atas_nama_persil},
          {'penggunaan_sekarang': penggunaan_sekarang},
          {'rencana_penggunaan': rencana_penggunaan}]}
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


def cetak_izin_lokasi(request, id_pengajuan_):
      extra_context = {}
      url_ = reverse('formulir_reklame')
      if id_pengajuan_:
        pengajuan_ = InformasiTanah.objects.get(id=id_pengajuan_)
        if pengajuan_.perusahaan != '':
          alamat_ = ""
          alamat_perusahaan_ = ""
          if pengajuan_.pemohon:
            if pengajuan_.pemohon.desa:
              alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
              extra_context.update({ 'alamat_pemohon': alamat_ })
            extra_context.update({ 'pemohon': pengajuan_.pemohon })

          if pengajuan_.perusahaan:
            if pengajuan_.perusahaan.desa:
              alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", DESA "+str(pengajuan_.perusahaan.desa)+", KEC. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
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
          response = loader.get_template("front-end/include/formulir_izin_lokasi/cetak.html")
        else:
          response = HttpResponseRedirect(url_)
          return response
      else:
        response = HttpResponseRedirect(url_)
        return response
      template = loader.get_template("front-end/include/formulir_izin_lokasi/cetak.html")
      ec = RequestContext(request, extra_context)
      return HttpResponse(template.render(ec))

def cetak_bukti_pendaftaran_izin_lokasi(request,id_pengajuan_):
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
        extra_context.update({ 'paspor': paspor_ })
        extra_context.update({ 'ktp': ktp_ })
      if pengajuan_.perusahaan:
        if pengajuan_.perusahaan.desa:
          alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", DESA "+str(pengajuan_.perusahaan.desa)+", KEC. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
          extra_context.update({ 'alamat_perusahaan': alamat_perusahaan_ })
        extra_context.update({ 'perusahaan': pengajuan_.perusahaan })
        syarat = Syarat.objects.filter(jenis_izin__jenis_izin__kode="IL")
      letak_ = pengajuan_.alamat + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)

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

  template = loader.get_template("front-end/include/formulir_izin_lokasi/cetak_bukti_pendaftaran.html")
  ec = RequestContext(request, extra_context)
  return HttpResponse(template.render(ec))