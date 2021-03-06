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
from izin.models import PengajuanIzin, InformasiTanah,Pemohon,SertifikatTanah,AktaJualBeliTanah,NoPTP
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna
from izin.izin_forms import LuasTanahYangDisetujuiForm,AktaJualBeliTanahForm, NoPTPForm
from accounts.utils import KETERANGAN_PEKERJAAN

def formulir_ippt_rumah(request, extra_context={}):
    jenis_pemohon = JenisPemohon.objects.all()
    negara = Negara.objects.all()
    kecamatan = Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35')

    extra_context.update({'negara': negara})
    extra_context.update({'kecamatan': kecamatan})
    extra_context.update({'jenis_pemohon': jenis_pemohon})
    extra_context.update({'keterangan_pekerjaan': KETERANGAN_PEKERJAAN })
    if 'id_kelompok_izin' in request.COOKIES.keys():
        jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) 
        extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
    else:
        return HttpResponseRedirect(reverse('layanan'))
    if 'id_pengajuan' in request.COOKIES.keys():
      if request.COOKIES['id_pengajuan'] != "":
        try:
          pengajuan_ = InformasiTanah.objects.get(id=request.COOKIES['id_pengajuan'])
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
          if 'id_pengajuan' in request.COOKIES.keys():
            if request.COOKIES['id_pengajuan'] != '':
              sertifikat_tanah_list = SertifikatTanah.objects.filter(informasi_tanah=request.COOKIES['id_pengajuan'])
              akta_jual_beli_list = AktaJualBeliTanah.objects.filter(informasi_tanah=request.COOKIES['id_pengajuan'])
              no_ptp_list = NoPTP.objects.filter(informasi_tanah=request.COOKIES['id_pengajuan'])

              extra_context.update({'sertifikat_tanah_list': sertifikat_tanah_list})
              extra_context.update({'akta_jual_beli_list': akta_jual_beli_list})
              extra_context.update({'no_ptp_list': no_ptp_list})

          extra_context.update({ 'no_pengajuan_konfirmasi': pengajuan_.no_pengajuan })
          extra_context.update({ 'jenis_permohonan_konfirmasi': pengajuan_.jenis_permohonan })
          extra_context.update({ 'pengajuan_': pengajuan_ })

          if pengajuan_.desa:
            letak_ = pengajuan_.alamat + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
          else:
            letak_ = ""
          extra_context.update({ 'letak': letak_ })
        except ObjectDoesNotExist:
          pass
    return render(request, "front-end/formulir/ippt_rumah.html", extra_context)

def load_konfirmasi_ippt_rumah(request,id_pengajuan):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
      pengajuan_ = InformasiTanah.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
      alamat = pengajuan_.alamat
      desa = str(pengajuan_.desa)
      kecamatan = str(pengajuan_.desa.kecamatan)
      kabupaten = str(pengajuan_.desa.kecamatan.kabupaten)
      luas = str(pengajuan_.luas)
      status_tanah = pengajuan_.status_tanah
      no_sertifikat_petak = pengajuan_.no_sertifikat_petak
      luas_sertifikat_petak = str(pengajuan_.luas_sertifikat_petak)
      atas_nama_sertifikat_petak = pengajuan_.atas_nama_sertifikat_petak
      if pengajuan_.tahun_sertifikat:
        id_tanggal_sertifikat = pengajuan_.tahun_sertifikat.strftime("%d-%m-%Y")
      else:
        id_tanggal_sertifikat = " "
      no_persil = pengajuan_.no_persil
      klas_persil = pengajuan_.klas_persil
      atas_nama_persil = pengajuan_.atas_nama_persil
      penggunaan_sekarang = pengajuan_.penggunaan_sekarang
      rencana_penggunaan = pengajuan_.rencana_penggunaan

      data = {'success': True,
          'data': [
          {'alamat_informasi_tanah': alamat},
          {'desa': desa},
          {'kecamatan': kecamatan},
          {'kabupaten': kabupaten},
          {'luas': luas},
          {'status_tanah': status_tanah},
          {'no_sertifikat_petak': no_sertifikat_petak},
          {'luas_sertifikat_petak': luas_sertifikat_petak},
          {'atas_nama_sertifikat_petak': atas_nama_sertifikat_petak},
          {'id_tanggal_sertifikat':id_tanggal_sertifikat},
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

def load_informasi_tanah(request,id_pengajuan):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
      pengajuan_ = InformasiTanah.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
      if pengajuan_.kelompok_jenis_izin.kode == "IPPT-Rumah":
        kode_izin = pengajuan_.kelompok_jenis_izin.kode
        id_alamat = pengajuan_.alamat
        if pengajuan_.desa:
          id_kecamatan = str(pengajuan_.desa.kecamatan.id)
          id_desa = str(pengajuan_.desa.id)
        else:
          id_kecamatan = ""
          id_desa = ""
        id_luas = str(pengajuan_.luas)
        id_status_tanah = pengajuan_.status_tanah
        id_no_surat_pemberitahuan = pengajuan_.no_surat_pemberitahuan
        id_no_sertifikat_petak = pengajuan_.no_sertifikat_petak
        id_luas_sertifikat_petak = str(pengajuan_.luas_sertifikat_petak)
        id_atas_nama_sertifikat_petak = pengajuan_.atas_nama_sertifikat_petak

        if pengajuan_.tahun_sertifikat:
          id_tahun_sertifikat = pengajuan_.tahun_sertifikat.strftime("%d-%m-%Y")
        else:
          id_tahun_sertifikat = ""

        if pengajuan_.tanggal_surat_pemberitahuan:
          id_tanggal_surat_pemberitahuan = pengajuan_.tanggal_surat_pemberitahuan.strftime("%d-%m-%Y")
        else:
          id_tanggal_surat_pemberitahuan = ""

        id_no_persil = pengajuan_.no_persil
        id_klas_persil = pengajuan_.klas_persil
        id_atas_nama_persil = pengajuan_.atas_nama_persil
        id_penggunaan_sekarang = pengajuan_.penggunaan_sekarang
        id_rencana_penggunaan = pengajuan_.rencana_penggunaan
        id_penggunaan_tanah_sebelumnya = pengajuan_.penggunaan_tanah_sebelumnya
        id_arahan_fungsi_kawasan = pengajuan_.arahan_fungsi_kawasan

        data = {'success': True,'data':{'kode_izin':kode_izin,'id_alamat':id_alamat ,'id_kecamatan':id_kecamatan ,'id_desa':id_desa,'id_luas':id_luas,'id_status_tanah':id_status_tanah,'id_no_surat_pemberitahuan':id_no_surat_pemberitahuan,'id_tanggal_surat_pemberitahuan':id_tanggal_surat_pemberitahuan,'id_no_sertifikat_petak':id_no_sertifikat_petak,'id_luas_sertifikat_petak':id_luas_sertifikat_petak,'id_atas_nama_sertifikat_petak':id_atas_nama_sertifikat_petak,'id_tahun_sertifikat':id_tahun_sertifikat,'id_no_persil':id_no_persil,'id_klas_persil':id_klas_persil,'id_atas_nama_persil':id_atas_nama_persil,'id_penggunaan_sekarang':id_penggunaan_sekarang,'id_rencana_penggunaan':id_rencana_penggunaan,'id_penggunaan_tanah_sebelumnya': id_penggunaan_tanah_sebelumnya,'id_arahan_fungsi_kawasan': id_arahan_fungsi_kawasan}}

      elif pengajuan_.kelompok_jenis_izin.kode == "503.07/":
        kode_izin = pengajuan_.kelompok_jenis_izin.kode

        id_alamat = pengajuan_.alamat
        if pengajuan_.desa:
          id_kecamatan = str(pengajuan_.desa.kecamatan.id)
          id_desa = str(pengajuan_.desa.id)
        else:
          id_kecamatan = ""
          id_desa = ""
        id_luas = str(pengajuan_.luas)
        id_status_tanah = pengajuan_.status_tanah

        id_no_jual_beli = pengajuan_.no_jual_beli
        if pengajuan_.tanggal_jual_beli:
          id_tanggal_jual_beli = pengajuan_.tanggal_jual_beli.strftime("%d-%m-%Y")
        else:
          id_tanggal_jual_beli = ""
        id_atas_nama_jual_beli = pengajuan_.atas_nama_jual_beli
        id_no_surat_pemberitahuan = pengajuan_.no_surat_pemberitahuan

        if pengajuan_.tanggal_surat_pemberitahuan:
          id_tanggal_surat_pemberitahuan = pengajuan_.tanggal_surat_pemberitahuan.strftime("%d-%m-%Y")
        else:
          id_tanggal_surat_pemberitahuan = ""
          
        id_penggunaan_sekarang = pengajuan_.penggunaan_sekarang
        id_rencana_penggunaan = pengajuan_.rencana_penggunaan


        data = {'success': True,'data':{'kode_izin':kode_izin,'id_alamat':id_alamat ,'id_kecamatan':id_kecamatan ,'id_desa':id_desa,'id_no_surat_pemberitahuan':id_no_surat_pemberitahuan,'id_tanggal_surat_pemberitahuan':id_tanggal_surat_pemberitahuan,'id_luas':id_luas,'id_status_tanah':id_status_tanah,'id_no_jual_beli':id_no_jual_beli,'id_tanggal_jual_beli':id_tanggal_jual_beli,'id_atas_nama_jual_beli':id_atas_nama_jual_beli,'id_penggunaan_sekarang':id_penggunaan_sekarang,'id_rencana_penggunaan':id_rencana_penggunaan}}

      else:
        data = {'success': True,'data':{}}
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

def cetak_ippt_rumah(request, id_pengajuan_):
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
              alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
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
          response = loader.get_template("front-end/include/formulir_ippt_rumah/cetak.html")
        else:
          response = HttpResponseRedirect(url_)
          return response
      else:
        response = HttpResponseRedirect(url_)
        return response
      template = loader.get_template("front-end/include/formulir_ippt_rumah/cetak.html")
      ec = RequestContext(request, extra_context)
      return HttpResponse(template.render(ec))

def cetak_bukti_pendaftaran_ippt_rumah(request,id_pengajuan_):
  extra_context = {}
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
        paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
        ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
        extra_context.update({ 'paspor': paspor_ })
        extra_context.update({ 'ktp': ktp_ })
      if pengajuan_.perusahaan:
        if pengajuan_.perusahaan.desa:
          alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
          extra_context.update({ 'alamat_perusahaan': alamat_perusahaan_ })
        extra_context.update({ 'perusahaan': pengajuan_.perusahaan })
        syarat_ = Syarat.objects.filter(jenis_izin__jenis_izin__kode="IL")
        extra_context.update({ 'syarat': syarat_ })
      if pengajuan_.desa:
        letak_ = pengajuan_.alamat + ", Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())
      else:
        letak_ = pengajuan_.alamat

      extra_context.update({'letak_': letak_})
      extra_context.update({ 'pengajuan': pengajuan_ })
      extra_context.update({ 'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin })
      extra_context.update({ 'created_at': pengajuan_.created_at })
      response = loader.get_template("front-end/include/formulir_ippt_rumah/cetak_bukti_pendaftaran.html")
    else:
      response = HttpResponseRedirect(url_)
      return response
  else:
    response = HttpResponseRedirect(url_)
    return response 

  template = loader.get_template("front-end/include/formulir_ippt_rumah/cetak_bukti_pendaftaran.html")
  ec = RequestContext(request, extra_context)
  return HttpResponse(template.render(ec))


def luas_tanah_yang_disetujui_save(request):
  if request.POST:
    pengajuan_izin_id = request.POST.get('id_pengajuan', None)
    pengajuan_ = InformasiTanah.objects.get(pengajuanizin_ptr_id=pengajuan_izin_id)
    luas_tanah_yang_disetujui = LuasTanahYangDisetujuiForm(request.POST, instance=pengajuan_)
    if luas_tanah_yang_disetujui.is_valid():
      p = luas_tanah_yang_disetujui.save(commit=False)
      p.save()
      pengajuan_.status = 2
      pengajuan_.save()
      riwayat_ = Riwayat(
        pengajuan_izin_id = pengajuan_izin_id,
        created_by_id = request.user.id,
        keterangan = "Kabid Verified (Pengajuan)"
      )
      riwayat_.save()
      data = {'success': True,
          'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
          'data': ['']}
      response = HttpResponse(json.dumps(data))
    else:
      data = luas_tanah_yang_disetujui.errors.as_json()
      response = HttpResponse(data)

  return response

def akta_jual_beli_save_cookie(request):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            akta_jual_beli = AktaJualBeliTanahForm(request.POST)
            if request.method == 'POST':
                if akta_jual_beli.is_valid():
                    p = akta_jual_beli.save(commit=False)
                    p.informasi_tanah_id = request.COOKIES['id_pengajuan']
                    p.save()
                    data = {'success': True,
                            'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
                            'data': {'id_akta_jual_beli':p.id}}
                    data = json.dumps(data)
                    response = HttpResponse(data)
                else:
                    data = akta_jual_beli.errors.as_json()
                    response = HttpResponse(json.dumps(data))
            else:
                akta_jual_beli = AktaJualBeliTanahForm()
        else:
            data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
            data = json.dumps(json.dumps(data))
    else:
        data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
        response = HttpResponse(json.dumps(data))
    return response

def edit_akta_jual_beli(request,id_akta_jual_beli):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            p = AktaJualBeliTanah.objects.get(id=id_akta_jual_beli)
            akta_jual_beli = AktaJualBeliTanahForm(request.POST,instance=p)
            if request.method == 'POST':
                if akta_jual_beli.is_valid():
                    p = akta_jual_beli.save(commit=False)
                    p.informasi_tanah_id = request.COOKIES['id_pengajuan']
                    p.save()
                    data = {'success': True,
                            'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
                            'data': {'id_akta_jual_beli':p.id}}
                    data = json.dumps(data)
                    response = HttpResponse(json.dumps(data))
                else:
                    data = akta_jual_beli.errors.as_json()
            else:
                akta_jual_beli = AktaJualBeliTanahForm()
        else:
            data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
            data = json.dumps(data)
    else:
        data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
        data = json.dumps(data)
    response = HttpResponse(data)
    return response

def delete_akta_jual_beli(request,id_akta_jual_beli):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
        tag_to_delete = get_object_or_404(AktaJualBeliTanah, id=id_akta_jual_beli)
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

def no_ptp_save_cookie(request):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            no_ptp = NoPTPForm(request.POST)
            if request.method == 'POST':
                if no_ptp.is_valid():
                    p = no_ptp.save(commit=False)
                    p.informasi_tanah_id = request.COOKIES['id_pengajuan']
                    p.save()
                    data = {'success': True,
                            'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
                            'data': {'id_no_ptp':p.id}}
                    data = json.dumps(data)
                    response = HttpResponse(data)
                else:
                    data = no_ptp.errors.as_json()
                    response = HttpResponse(json.dumps(data))
            else:
                no_ptp = NoPTPForm()
        else:
            data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
            data = json.dumps(json.dumps(data))
    else:
        data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
        response = HttpResponse(json.dumps(data))
    return response

def edit_no_ptp(request,id_no_ptp):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            p = NoPTP.objects.get(id=id_no_ptp)
            no_ptp = NoPTPForm(request.POST,instance=p)
            if request.method == 'POST':
                if no_ptp.is_valid():
                    p = no_ptp.save(commit=False)
                    p.informasi_tanah_id = request.COOKIES['id_pengajuan']
                    p.save()
                    data = {'success': True,
                            'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
                            'data': {'id_no_ptp':p.id}}
                    data = json.dumps(data)
                    response = HttpResponse(json.dumps(data))
                else:
                    data = no_ptp.errors.as_json()
            else:
                no_ptp = AktaJualBeliTanahForm()
        else:
            data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
            data = json.dumps(data)
    else:
        data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
        data = json.dumps(data)
    response = HttpResponse(data)
    return response

def delete_no_ptp(request,id_no_ptp):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
        tag_to_delete = get_object_or_404(NoPTP, id=id_no_ptp)
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


def load_data_tabel_akta_jual_beli(request,id_akta_jual_beli):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            data = []
            i = AktaJualBeliTanah.objects.filter(informasi_tanah_id=request.COOKIES['id_pengajuan'])
            data = [ob.as_json() for ob in i]
            response = HttpResponse(json.dumps(data), content_type="application/json")
    return response

def load_data_tabel_ptp(request,id_no_ptp):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            data = []
            i = NoPTP.objects.filter(informasi_tanah_id=request.COOKIES['id_pengajuan'])
            data = [ob.as_json() for ob in i]
            response = HttpResponse(json.dumps(data), content_type="application/json")
    return response