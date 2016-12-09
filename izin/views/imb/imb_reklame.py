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

from master.models import Negara, Kecamatan, JenisPemohon,JenisReklame,Berkas
from izin.models import JenisIzin, Syarat, KelompokJenisIzin, JenisPermohonanIzin,Riwayat
from izin.models import PengajuanIzin, DetilIMBPapanReklame,Pemohon
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna
from izin.izin_forms import UploadBerkasPendukungForm,PengajuanIMBReklameForm,UploadBerkasKTPForm
from accounts.models import NomorIdentitasPengguna

def formulir_imb_reklame(request, extra_context={}):
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
    return render(request, "front-end/formulir/imb_reklame.html", extra_context)

def cetak_imb_reklame(request, id_pengajuan_):
      extra_context = {}
      url_ = reverse('formulir_reklame')
      if id_pengajuan_:
        pengajuan_ = DetilIMBPapanReklame.objects.get(id=id_pengajuan_)
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
          response = loader.get_template("front-end/include/formulir_reklame/cetak.html")
        else:
          response = HttpResponseRedirect(url_)
          return response
      else:
        response = HttpResponseRedirect(url_)
        return response
      template = loader.get_template("front-end/include/formulir_imb_reklame/cetak.html")
      ec = RequestContext(request, extra_context)
      return HttpResponse(template.render(ec))

def cetak_bukti_pendaftaran_imb_reklame(request,id_pengajuan_):
  extra_context = {}
  if id_pengajuan_:
    pengajuan_ = DetilIMBPapanReklame.objects.get(id=id_pengajuan_)
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
        syarat = Syarat.objects.filter(jenis_izin__jenis_izin__kode="IMB")
      letak_ = pengajuan_.lokasi_pasang + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
      ukuran_ = "Lebar = "+str(int(pengajuan_.lebar))+" M , Tinggi = "+str(int(pengajuan_.tinggi))+" M"
      
      extra_context.update({'letak_pemasangan': letak_})
      extra_context.update({'ukuran': ukuran_})
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

  template = loader.get_template("front-end/include/formulir_imb_reklame/cetak_bukti_pendaftaran.html")
  ec = RequestContext(request, extra_context)
  return HttpResponse(template.render(ec))

def reklame_imbreklame_save_cookie(request):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            pengajuan_ = DetilIMBPapanReklame.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
            IMBReklame = PengajuanIMBReklameForm(request.POST, instance=pengajuan_)
            if IMBReklame.is_valid():
                pengajuan_.perusahaan_id  = request.COOKIES['id_perusahaan']
                pengajuan_.save()
                letak_ = pengajuan_.lokasi_pasang + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
                ukuran_ = "Lebar = "+str(int(pengajuan_.lebar))+" M, Tinggi = "+str(int(pengajuan_.tinggi))+" M"        
                data = {'success': True,
                        'pesan': 'Data Reklame berhasil disimpan. Proses Selanjutnya.',
                        'data': [
                        {'jenis_papan_reklame': pengajuan_.jenis_papan_reklame},
                        {'ukuran': ukuran_},
                        {'batas_utara': pengajuan_.batas_utara},
                        {'batas_timur': pengajuan_.batas_timur},
                        {'batas_selatan': pengajuan_.batas_selatan},
                        {'batas_barat': pengajuan_.batas_barat},
                        {'letak_pemasangan': letak_}]}
                data = json.dumps(data)
                response = HttpResponse(json.dumps(data))
            else:
                data = IMBReklame.errors.as_json()
        else:
            data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
            data = json.dumps(data)
    else:
        data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
        data = json.dumps(data)
    response = HttpResponse(data)
    return response

def imb_reklame_done(request):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
      pengajuan_ = DetilIMBPapanReklame.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
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

def imbreklame_upload_berkas_pendukung(request):
  if 'id_pengajuan' in request.COOKIES.keys() or 'id_pemohon' in request.COOKIES.keys():
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
                            berkas.nama_berkas = "Gambar Rencana Teknis/Konstruksi Bangunan Reklame"+p.no_pengajuan
                            berkas.keterangan = "Gambar Rencana Teknis/Konstruksi Bangunan Reklame"
                        elif request.POST.get('aksi') == "3":
                            berkas.nama_berkas = "Surat Persetujuan/Perjanjian/Izin Pemilik tanah untuk bangunan yang didirikan diatas tanah yang bukan miliknya"+p.no_pengajuan
                            berkas.keterangan = "Surat Persetujuan/Perjanjian/Izin Pemilik tanah untuk bangunan yang didirikan diatas tanah yang bukan miliknya"
                        elif request.POST.get('aksi') == "4":
                            berkas.nama_berkas = "Surat Ketetapan Pajak Daerah (SKPD) IMB Papan Reklame"+p.no_pengajuan
                            berkas.keterangan = "Surat Ketetapan Pajak Daerah (SKPD) IMB Papan Reklame"
                        elif request.POST.get('aksi') == "5":
                            berkas.nama_berkas = "Surat Setoran Pajak Daerah (SSPD) IMB Papan Reklame"+p.no_pengajuan
                            berkas.keterangan = "Surat Setoran Pajak Daerah (SSPD) IMB Papan Reklame"
                        else:
                            berkas.nama_berkas = "Rekomendasi/Retribusi Sewa Tanah, apabila bangunan diatas tanah milik pemerintah"+p.no_pengajuan
                            berkas.keterangan = "Rekomendasi/Retribusi Sewa Tanah, apabila bangunan diatas tanah milik pemerintah"
                            
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

def ajax_load_berkas_imbreklame(request, id_pengajuan):
  url_berkas = []
  id_elemen = []
  nm_berkas =[]
  id_berkas =[]
  if id_pengajuan:
      try:
          p = PengajuanIzin.objects.get(id=request.COOKIES['id_pengajuan'])
          foto_ktp_paspor = Berkas.objects.filter(nama_berkas="Berkas Foto KTP/PASPOR"+p.pemohon.username)
          if foto_ktp_paspor.exists():
              foto_ktp_paspor = foto_ktp_paspor.last()
              url_berkas.append(foto_ktp_paspor.berkas.url)
              id_elemen.append('ktp_paspor')
              nm_berkas.append("Berkas Foto KTP/PASPOR"+p.pemohon.username)
              id_berkas.append(foto_ktp_paspor.id)

          gambar_rencana_teknis  = Berkas.objects.filter(nama_berkas="Gambar Rencana Teknis/Konstruksi Bangunan Reklame"+p.no_pengajuan)
          if gambar_rencana_teknis.exists():
              gambar_rencana_teknis = gambar_rencana_teknis.last()
              url_berkas.append(gambar_rencana_teknis.berkas.url)
              id_elemen.append('rencana_teknis_kontruksi_bangunan_reklame')
              nm_berkas.append("Gambar Rencana Teknis/Konstruksi Bangunan Reklame"+p.no_pengajuan)
              id_berkas.append(gambar_rencana_teknis.id)

          surat_persetujuan_pemilik_tanah = Berkas.objects.filter(nama_berkas="Surat Persetujuan/Perjanjian/Izin Pemilik tanah untuk bangunan yang didirikan diatas tanah yang bukan miliknya"+p.no_pengajuan)
          if surat_persetujuan_pemilik_tanah.exists():
              surat_persetujuan_pemilik_tanah = surat_persetujuan_pemilik_tanah.last()
              url_berkas.append(surat_persetujuan_pemilik_tanah.berkas.url)
              id_elemen.append('surat_persetujuan_pemilik_tanah_untuk_bangunan_diatas_tanah_bukan_miliknya')
              nm_berkas.append("Surat Persetujuan/Perjanjian/Izin Pemilik tanah untuk bangunan yang didirikan diatas tanah yang bukan miliknya"+p.no_pengajuan)
              id_berkas.append(surat_persetujuan_pemilik_tanah.id)

          surat_ketetapan_pajak = Berkas.objects.filter(nama_berkas="Surat Ketetapan Pajak Daerah (SKPD) IMB Papan Reklame"+p.no_pengajuan)
          if surat_ketetapan_pajak.exists():
              surat_ketetapan_pajak = surat_ketetapan_pajak.last()
              url_berkas.append(surat_ketetapan_pajak.berkas.url)
              id_elemen.append('surat_ketetapan_pajak_daerah_imb')
              nm_berkas.append("Surat Ketetapan Pajak Daerah (SKPD) IMB Papan Reklame"+p.no_pengajuan)
              id_berkas.append(surat_ketetapan_pajak.id)

          surat_setoran_pajak_daerah = Berkas.objects.filter(nama_berkas="Surat Setoran Pajak Daerah (SSPD) IMB Papan Reklame"+p.no_pengajuan)
          if surat_setoran_pajak_daerah.exists():
              surat_setoran_pajak_daerah = surat_setoran_pajak_daerah.last()
              url_berkas.append(surat_setoran_pajak_daerah.berkas.url)
              id_elemen.append('surat_setoran_pajak_daerah_imb')
              nm_berkas.append("Surat Setoran Pajak Daerah (SSPD) IMB Papan Reklame "+p.no_pengajuan)
              id_berkas.append(surat_setoran_pajak_daerah.id)

          surat_rekomendasi = Berkas.objects.filter(nama_berkas="Rekomendasi/Retribusi Sewa Tanah, apabila bangunan diatas tanah milik pemerintah"+p.no_pengajuan)
          if surat_rekomendasi.exists():
              surat_rekomendasi = surat_rekomendasi.last()
              url_berkas.append(surat_rekomendasi.berkas.url)
              id_elemen.append('rekomendasi_sewa_tanah_bukan_tanah_milik_pemerintah')
              nm_berkas.append("Rekomendasi/Retribusi Sewa Tanah, apabila bangunan diatas tanah milik pemerintah"+p.no_pengajuan)
              id_berkas.append(surat_rekomendasi.id)

          data = {'success': True, 'pesan': 'berkas pendukung Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
      except ObjectDoesNotExist:
          data = {'success': False, 'pesan': '' }
            
        
  response = HttpResponse(json.dumps(data))
  return response

def ajax_delete_berkas_imbreklame(request, id_berkas):
  if id_berkas:
      try:
        if request.COOKIES['nomor_ktp'] != '':
          p = Pemohon.objects.get(username = request.COOKIES['nomor_ktp'])
          ktp_ = NomorIdentitasPengguna.objects.get(nomor=request.COOKIES['nomor_ktp'])
          nomr_ktp = ktp_.nomor
          jenis_nomor = ktp_.jenis_identitas.id

          b = Berkas.objects.get(id=id_berkas)
          data = {'success': True, 'pesan': str(b)+" berhasil dihapus" }
          b.delete()
        try:
          i = NomorIdentitasPengguna.objects.get(nomor = ktp_)
        except ObjectDoesNotExist:
          i, created = NomorIdentitasPengguna.objects.get_or_create(
                nomor = nomr_ktp,
                jenis_identitas_id=jenis_nomor, # untuk KTP harusnya membutuhkan kode lagi
                user_id=p.id,
                )
      except ObjectDoesNotExist:  
          data = {'success': False, 'pesan': 'Berkas Tidak Ada' }
            
      response = HttpResponse(json.dumps(data))
      return response

  return False
        