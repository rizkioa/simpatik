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
from izin.models import PengajuanIzin, DetilIMB,Pemohon
from izin.utils import STATUS_HAK_TANAH,KLASIFIKASI_JALAN,RUMIJA,RUWASJA,JENIS_LOKASI_USAHA
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna
from izin.izin_forms import UploadBerkasPendukungForm,IdentifikasiJalanForm,UploadBerkasKTPForm
from accounts.models import NomorIdentitasPengguna
from accounts.utils import KETERANGAN_PEKERJAAN

def formulir_imb_perumahan(request, extra_context={}):
	negara = Negara.objects.all()
	kecamatan = Kecamatan.objects.filter(kabupaten_id=1083)
	jenis_pemohon = JenisPemohon.objects.all()
	kegiatan_pembangunan = ParameterBangunan.objects.filter(parameter="Kegiatan Pembangunan Gedung")
	fungsi_bangunan = ParameterBangunan.objects.filter(parameter="Fungsi Bangunan")
	kompleksitas_bangunan = ParameterBangunan.objects.filter(parameter="Tingkat Kompleksitas")
	permanensi_bangunan = ParameterBangunan.objects.filter(parameter="Tingkat Permanensi")
	ketinggian_bangunan = ParameterBangunan.objects.filter(parameter="Ketinggian Bangunan")
	lokasi_bangunan = ParameterBangunan.objects.filter(parameter="Lokasi Bangunan")
	kepemilikan_bangunan = ParameterBangunan.objects.filter(parameter="Kepemilikan Bangunan")
	lama_penggunaan_bangunan = ParameterBangunan.objects.filter(parameter="Lama Penggunaan Bangunan")

	extra_context.update({'fungsi_bangunan': fungsi_bangunan })
	extra_context.update({'kompleksitas_bangunan': kompleksitas_bangunan })
	extra_context.update({'permanensi_bangunan': permanensi_bangunan })
	extra_context.update({'ketinggian_bangunan': ketinggian_bangunan })
	extra_context.update({'lokasi_bangunan': lokasi_bangunan })
	extra_context.update({'kepemilikan_bangunan': kepemilikan_bangunan })
	extra_context.update({'lama_penggunaan_bangunan': lama_penggunaan_bangunan })
	extra_context.update({'kegiatan_pembangunan': kegiatan_pembangunan })
	extra_context.update({'status_hak_tanah': STATUS_HAK_TANAH })
	extra_context.update({'klasifikasi_jalan': JENIS_LOKASI_USAHA })
	extra_context.update({'rumija': RUMIJA })
	extra_context.update({'ruwasja': RUWASJA })
	extra_context.update({'keterangan_pekerjaan': KETERANGAN_PEKERJAAN })
	extra_context.update({'negara': negara})
	extra_context.update({'kecamatan': kecamatan})
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) 

		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/imb_perumahan.html", extra_context)

def cetak_imb_perumahan(request, id_pengajuan_):
      extra_context = {}
      url_ = reverse('formulir_reklame')
      if id_pengajuan_:
        pengajuan_ = DetilIMB.objects.get(id=id_pengajuan_)
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

def cetak_bukti_pendaftaran_imb_perumahan(request,id_pengajuan_):
  extra_context = {}
  if id_pengajuan_:
    pengajuan_ = DetilIMB.objects.get(id=id_pengajuan_)
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
        syarat = Syarat.objects.filter(jenis_izin__jenis_izin__kode="IMB")
      letak_ = pengajuan_.lokasi_pasang +", Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())
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

def identifikasi_jalan_save_cookie(request):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            pengajuan_ = DetilIMB.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
            IMBIdentifikasiJalan = IdentifikasiJalanForm(request.POST, instance=pengajuan_)
            parameter = request.POST.getlist('parameter_bangunan')
            if IMBIdentifikasiJalan.is_valid():
                pengajuan_.klasifikasi_jalan  = request.POST.get('klasifikasi_jalan')
                pengajuan_.ruang_milik_jalan  = request.POST.get('ruang_milik_jalan')
                pengajuan_.ruang_pengawasan_jalan  = request.POST.get('ruang_pengawasan_jalan')
                pengajuan_.save()
                klasifikasi_jalan = pengajuan_.klasifikasi_jalan
                ruang_milik_jalan = pengajuan_.ruang_milik_jalan
                ruang_pengawasan_jalan = pengajuan_.ruang_pengawasan_jalan
                data = {'success': True,
                        'pesan': 'Data IMB berhasil disimpan. Proses Selanjutnya.',
                        'data': [
                        {'klasifikasi_jalan': klasifikasi_jalan},
                        {'ruang_milik_jalan': ruang_milik_jalan},
                        {'ruang_pengawasan_jalan': ruang_pengawasan_jalan},
                        ]}
                data = json.dumps(data)
                response = HttpResponse(data)
            else:
                data = IMBIdentifikasiJalan.errors.as_json()
                response = HttpResponse(data)
        else:
            data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
            data = json.dumps(data)
            response = HttpResponse(data)
    else:
        data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
        data = json.dumps(data)
        response = HttpResponse(data)
    return response

def identifikasi_jalan_pembuat_surat_save_cookie(request):
    if request.POST:
        pengajuan_izin_id = request.POST.get('pengajuan_izin', None)
        pengajuan_ = DetilIMB.objects.get(pengajuanizin_ptr_id=pengajuan_izin_id)
        IMBIdentifikasiJalan = IdentifikasiJalanForm(request.POST, instance=pengajuan_)
        parameter = request.POST.getlist('parameter_bangunan')
        if IMBIdentifikasiJalan.is_valid():
            pengajuan_.klasifikasi_jalan  = request.POST.get('klasifikasi_jalan')
            pengajuan_.ruang_milik_jalan  = request.POST.get('ruang_milik_jalan')
            pengajuan_.ruang_pengawasan_jalan  = request.POST.get('ruang_pengawasan_jalan')
            pengajuan_.save()
            klasifikasi_jalan = pengajuan_.klasifikasi_jalan
            ruang_milik_jalan = pengajuan_.ruang_milik_jalan
            ruang_pengawasan_jalan = pengajuan_.ruang_pengawasan_jalan
            data = {'success': True,
                    'pesan': 'Data IMB berhasil disimpan. Proses Selanjutnya.',
                    'data': [
                    {'klasifikasi_jalan': klasifikasi_jalan},
                    {'ruang_milik_jalan': ruang_milik_jalan},
                    {'ruang_pengawasan_jalan': ruang_pengawasan_jalan},
                    ]}
            data = json.dumps(data)
            response = HttpResponse(data)
        else:
            data = IMBIdentifikasiJalan.errors.as_json()
        return response


def cetak_imb_perumahan(request, id_pengajuan_):
    extra_context = {}
    url_ = reverse('formulir_reklame')
    if id_pengajuan_:
        pengajuan_ = DetilIMB.objects.get(id=id_pengajuan_)
        if pengajuan_.pemohon:
            if pengajuan_.pemohon.desa:
                alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())
            extra_context.update({ 'alamat_pemohon': alamat_ })
        extra_context.update({ 'pemohon': pengajuan_.pemohon })

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
    template = loader.get_template("front-end/include/formulir_imb_perumahan/cetak.html")
    ec = RequestContext(request, extra_context)
    return HttpResponse(template.render(ec))

def cetak_bukti_pendaftaran_imb_perumahan(request,id_pengajuan_):
    extra_context = {}
    if id_pengajuan_:
        pengajuan_ = DetilIMB.objects.get(id=id_pengajuan_)
        if pengajuan_.pemohon:
            if pengajuan_.pemohon.desa:
              alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())
              extra_context.update({ 'alamat_pemohon': alamat_ })
            extra_context.update({ 'pemohon': pengajuan_.pemohon })
            paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
            ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
            extra_context.update({ 'paspor': paspor_ })
            extra_context.update({ 'ktp': ktp_ })
            syarat = Syarat.objects.filter(jenis_izin__jenis_izin__kode="IMB")
            letak_ = pengajuan_.lokasi +", Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())

            kegiatan_pembangunan = pengajuan_.parameter_bangunan.get(parameter="Kegiatan Pembangunan Gedung")
            nilai_kegiatan_pembangunan = str(kegiatan_pembangunan.nilai)
            
            fungsi_bangunan = pengajuan_.parameter_bangunan.get(parameter="Fungsi Bangunan")
            nilai_fungsi_bangunan = str(fungsi_bangunan.nilai)

            kompleksitas_bangunan = pengajuan_.parameter_bangunan.get(parameter="Tingkat Kompleksitas")
            nilai_kompleksitas_bangunan = str(kompleksitas_bangunan.nilai)

            permanensi_bangunan = pengajuan_.parameter_bangunan.get(parameter="Tingkat Permanensi")
            nilai_permanensi_bangunan = str(permanensi_bangunan.nilai)

            ketinggian_bangunan = pengajuan_.parameter_bangunan.get(parameter="Ketinggian Bangunan")
            nilai_ketinggian_bangunan = str(ketinggian_bangunan.nilai)

            letak_bangunan = pengajuan_.parameter_bangunan.get(parameter="Lokasi Bangunan")
            nilai_letak_bangunan = str(letak_bangunan.nilai)

            kepemilikan_bangunan = pengajuan_.parameter_bangunan.get(parameter="Kepemilikan Bangunan")
            nilai_kepemilikan_bangunan = str(kepemilikan_bangunan.nilai)

            lama_penggunaan_bangunan = pengajuan_.parameter_bangunan.get(parameter="Lama Penggunaan Bangunan")
            nilai_lama_penggunaan_bangunan = str(lama_penggunaan_bangunan.nilai)
            total_biaya = str(pengajuan_.total_biaya) 

            extra_context.update({'nama_fungsi_bangunan': fungsi_bangunan.detil_parameter})
            extra_context.update({'nilai_fungsi_bangunan': nilai_fungsi_bangunan})
            extra_context.update({'kegiatan_pembangunan': kegiatan_pembangunan.detil_parameter})
            extra_context.update({'nilai_kegiatan_pembangunan': nilai_kegiatan_pembangunan})
            extra_context.update({'kompleksitas_bangunan': kompleksitas_bangunan.detil_parameter})
            extra_context.update({'nilai_kompleksitas_bangunan': nilai_kompleksitas_bangunan})
            extra_context.update({'permanensi_bangunan': permanensi_bangunan.detil_parameter})
            extra_context.update({'nilai_permanensi_bangunan': nilai_permanensi_bangunan})
            extra_context.update({'ketinggian_bangunan': ketinggian_bangunan.detil_parameter})
            extra_context.update({'nilai_ketinggian_bangunan': nilai_ketinggian_bangunan})
            extra_context.update({'letak_bangunan': letak_bangunan.detil_parameter})
            extra_context.update({'nilai_letak_bangunan': nilai_letak_bangunan})
            extra_context.update({'kepemilikan_bangunan': kepemilikan_bangunan.detil_parameter})
            extra_context.update({'nilai_kepemilikan_bangunan': nilai_kepemilikan_bangunan})
            extra_context.update({'lama_penggunaan_bangunan': lama_penggunaan_bangunan.detil_parameter})
            extra_context.update({'nilai_lama_penggunaan_bangunan': nilai_lama_penggunaan_bangunan})

            extra_context.update({'letak_pembangunan': letak_})
            extra_context.update({ 'pengajuan': pengajuan_ })
            extra_context.update({ 'syarat': syarat })
            extra_context.update({ 'total_biaya': total_biaya })
            extra_context.update({ 'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin })
            extra_context.update({ 'created_at': pengajuan_.created_at })
            response = loader.get_template("front-end/cetak_bukti_pendaftaran.html")
        else:
            response = HttpResponseRedirect(url_)
            return response
    else:
        response = HttpResponseRedirect(url_)
        return response 

    template = loader.get_template("front-end/include/formulir_imb_perumahan/cetak_bukti_pendaftaran.html")
    ec = RequestContext(request, extra_context)
    return HttpResponse(template.render(ec))

def imbperumahan_upload_berkas_pendukung(request):
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
                            berkas.nama_berkas = "Izin Prinsip Penananaman Modal"+p.no_pengajuan
                            berkas.keterangan = "Izin Prinsip Penananaman Modal"
                        elif request.POST.get('aksi') == "2":
                            berkas.nama_berkas = "Izin Perubahan Penggunaan Tanah(IPPT)"+p.no_pengajuan
                            berkas.keterangan = "Izin Perubahan Penggunaan Tanah(IPPT)"
                        elif request.POST.get('aksi') == "3":
                            berkas.nama_berkas = "Bukti pendaftaran perubahan/penghapusan hak atas Fasum/Fasos"+p.no_pengajuan
                            berkas.keterangan = "Bukti pendaftaran perubahan/penghapusan hak atas Fasum/Fasos"
                        elif request.POST.get('aksi') == "4":
                            berkas.nama_berkas = "Gambar Teknis Bangunan Gedung /Denah Bangunan/Site Plan yang disahkan oleh Dinans PU"+p.no_pengajuan
                            berkas.keterangan = "Gambar Teknis Bangunan Gedung /Denah Bangunan/Site Plan yang disahkan oleh Dinans PU"
                        elif request.POST.get('aksi') == "5":
                            berkas.nama_berkas = "Dokumen UKL-UPL"+p.no_pengajuan
                            berkas.keterangan = "Dokumen UKL-UPL"                       
                        elif request.POST.get('aksi') == "6":
                            berkas.nama_berkas = "Surat Kepemilikan Tanah"+p.no_pengajuan
                            berkas.keterangan = "Surat Kepemilikan Tanah"
                        elif request.POST.get('aksi') == "7":
                            berkas.nama_berkas = "Berkas Foto KTP/PASPOR"+ktp_.nomor
                            berkas.keterangan = "Berkas Foto KTP/PASPOR"
                        elif request.POST.get('aksi') == "8":
                            berkas.nama_berkas = "NPWP"+p.no_pengajuan
                            berkas.keterangan = "NPWP"
                        else:
                            berkas.nama_berkas = "Perhitungan Kontruksi Beton (Untuk Bangunan lebih dari satu lantai)"+p.no_pengajuan
                            berkas.keterangan = "Perhitungan Kontruksi Beton (Untuk Bangunan lebih dari satu lantai)"
                            
                        if request.user.is_authenticated():
                          berkas.created_by_id = request.user.id
                        else:
                          berkas.created_by_id = request.COOKIES['id_pemohon']
                        berkas.save()
                        p.berkas_tambahan.add(berkas)
                        p.berkas_terkait_izin.add(berkas)
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

def ajax_load_berkas_imbperumahan(request, id_pengajuan):
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
                p.berkas_terkait_izin.add(foto_ktp_paspor)

            izin_prinsip_penanaman_modal  = Berkas.objects.filter(nama_berkas="Izin Prinsip Penananaman Modal"+p.no_pengajuan)
            if izin_prinsip_penanaman_modal.exists():
                izin_prinsip_penanaman_modal = izin_prinsip_penanaman_modal.last()
                url_berkas.append(izin_prinsip_penanaman_modal.berkas.url)
                id_elemen.append('prinsip_penanaman_modal')
                nm_berkas.append("Izin Prinsip Penananaman Modal"+p.no_pengajuan)
                id_berkas.append(izin_prinsip_penanaman_modal.id)
                p.berkas_terkait_izin.add(izin_prinsip_penanaman_modal)

            npwp = Berkas.objects.filter(nama_berkas="NPWP"+p.no_pengajuan)
            if npwp.exists():
                npwp = npwp.last()
                url_berkas.append(npwp.berkas.url)
                id_elemen.append('npwp')
                nm_berkas.append("NPWP"+p.no_pengajuan)
                id_berkas.append(npwp.id)
                p.berkas_terkait_izin.add(npwp)

            cetak_biru_bangunan = Berkas.objects.filter(nama_berkas="Gambar Teknis Bangunan Gedung /Denah Bangunan/Site Plan yang disahkan oleh Dinans PU"+p.no_pengajuan)
            if cetak_biru_bangunan.exists():
                cetak_biru_bangunan = cetak_biru_bangunan.last()
                url_berkas.append(cetak_biru_bangunan.berkas.url)
                id_elemen.append('cetak_biru_bangunan')
                nm_berkas.append("Gambar Teknis Bangunan Gedung /Denah Bangunan/Site Plan yang disahkan oleh Dinans PU"+p.no_pengajuan)
                id_berkas.append(cetak_biru_bangunan.id)
                p.berkas_terkait_izin.add(cetak_biru_bangunan)

            perubahan_penggunaan_tanah = Berkas.objects.filter(nama_berkas="Izin Perubahan Penggunaan Tanah(IPPT)"+p.no_pengajuan)
            if perubahan_penggunaan_tanah.exists():
                perubahan_penggunaan_tanah = perubahan_penggunaan_tanah.last()
                url_berkas.append(perubahan_penggunaan_tanah.berkas.url)
                id_elemen.append('perubahan_penggunaan_tanah')
                nm_berkas.append("Izin Perubahan Penggunaan Tanah(IPPT)"+p.no_pengajuan)
                id_berkas.append(perubahan_penggunaan_tanah.id)
                p.berkas_terkait_izin.add(perubahan_penggunaan_tanah)

            bukti_pendaftaran_perubahan = Berkas.objects.filter(nama_berkas="Bukti pendaftaran perubahan/penghapusan hak atas Fasum/Fasos"+p.no_pengajuan)
            if bukti_pendaftaran_perubahan.exists():
                bukti_pendaftaran_perubahan = bukti_pendaftaran_perubahan.last()
                url_berkas.append(bukti_pendaftaran_perubahan.berkas.url)
                id_elemen.append('bukti_pendaftaran_perubahan')
                nm_berkas.append("Bukti pendaftaran perubahan/penghapusan hak atas Fasum/Fasos"+p.no_pengajuan)
                id_berkas.append(bukti_pendaftaran_perubahan.id)
                p.berkas_terkait_izin.add(bukti_pendaftaran_perubahan)

            dokumen_ukl_upl = Berkas.objects.filter(nama_berkas="Dokumen UKL-UPL"+p.no_pengajuan)
            if dokumen_ukl_upl.exists():
                dokumen_ukl_upl = dokumen_ukl_upl.last()
                url_berkas.append(dokumen_ukl_upl.berkas.url)
                id_elemen.append('dokumen_ukl_upl')
                nm_berkas.append("Dokumen UKL-UPL"+p.no_pengajuan)
                id_berkas.append(dokumen_ukl_upl.id)
                p.berkas_terkait_izin.add(dokumen_ukl_upl)

            kepemilikan_tanah = Berkas.objects.filter(nama_berkas="Surat Kepemilikan Tanah"+p.no_pengajuan)
            if kepemilikan_tanah.exists():
                kepemilikan_tanah = kepemilikan_tanah.last()
                url_berkas.append(kepemilikan_tanah.berkas.url)
                id_elemen.append('kepemilikan_tanah')
                nm_berkas.append("Surat Kepemilikan Tanah"+p.no_pengajuan)
                id_berkas.append(kepemilikan_tanah.id)
                p.berkas_terkait_izin.add(kepemilikan_tanah)

            perhitungan_kontruksi_beton = Berkas.objects.filter(nama_berkas="Perhitungan Kontruksi Beton (Untuk Bangunan lebih dari satu lantai)"+p.no_pengajuan)
            if perhitungan_kontruksi_beton.exists():
                perhitungan_kontruksi_beton = perhitungan_kontruksi_beton.last()
                url_berkas.append(perhitungan_kontruksi_beton.berkas.url)
                id_elemen.append('perhitungan_kontruksi_beton')
                nm_berkas.append("Perhitungan Kontruksi Beton (Untuk Bangunan lebih dari satu lantai)"+p.no_pengajuan)
                id_berkas.append(perhitungan_kontruksi_beton.id)
                p.berkas_terkait_izin.add(perhitungan_kontruksi_beton)

            data = {'success': True, 'pesan': 'berkas pendukung Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
        except ObjectDoesNotExist:
            data = {'success': False, 'pesan': '' }
            
    response = HttpResponse(json.dumps(data))
    return response