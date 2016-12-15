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
from izin.utils import STATUS_HAK_TANAH
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna
from izin.izin_forms import UploadBerkasPendukungForm,DetilIMBForm,ParameterBangunanForm
from accounts.models import NomorIdentitasPengguna

def formulir_imb_umum(request, extra_context={}):
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
	extra_context.update({'negara': negara})
	extra_context.update({'kecamatan': kecamatan})
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) 
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/imb_umum.html", extra_context)

def cetak_imb_umum(request, id_pengajuan_):
	  extra_context = {}
	  url_ = reverse('formulir_reklame')
	  if id_pengajuan_:
		pengajuan_ = DetilIMB.objects.get(id=id_pengajuan_)
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

def cetak_bukti_pendaftaran_imb_umum(request,id_pengajuan_):
  extra_context = {}
  if id_pengajuan_:
	pengajuan_ = DetilIMB.objects.get(id=id_pengajuan_)
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

def imbumum_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilIMB.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			IMBUmum = DetilIMBForm(request.POST, instance=pengajuan_)
			if IMBUmum.is_valid():
				pengajuan_.pemohon_id  = request.COOKIES['id_pemohon']
				pengajuan_.save()
				letak_ = pengajuan_.lokasi + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
				ukuran_ = "Luas Bangunan = "+str(int(pengajuan_.luas_bangunan))+", Luas Tanah"+str(int(pengajuan_.luas_tanah))      
				data = {'success': True,
						'pesan': 'Data IMB UMUM berhasil disimpan. Proses Selanjutnya.',
						'data': [
						{'ukuran': ukuran_},
  
						{'letak_pemasangan': letak_}]}
				data = json.dumps(data)
				response = HttpResponse(json.dumps(data))
			else:
				data = IMBUmum.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response

def parameter_bangunan_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilIMB.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			IMBParameterBangunan = ParameterBangunanForm(request.POST, instance=pengajuan_)
			parameter = request.POST.getlist('parameter_bangunan')
			if IMBParameterBangunan.is_valid():
				if pengajuan_.parameter_bangunan.exists():
					pengajuan_.parameter_bangunan.clear() 
					for i in parameter:
						pengajuan_.parameter_bangunan.add(i)
				else:
					for i in parameter:
						pengajuan_.parameter_bangunan.add(i) 
				data = {'success': True,
						'pesan': 'Data IMB UMUM berhasil disimpan. Proses Selanjutnya.',
						'data': ['']}
				data = json.dumps(data)
				response = HttpResponse(json.dumps(data))
			else:
				data = IMBParameterBangunan.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response

def imb_umum_done(request):
  if 'id_pengajuan' in request.COOKIES.keys():
	if request.COOKIES['id_pengajuan'] != '':
	  pengajuan_ = DetilIMB.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
	  pengajuan_.status = 6
	  pengajuan_.save()
	  data = {'success': True, 'pesan': 'Proses Selesai.' }
	  response = HttpResponse(json.dumps(data))
	  response.delete_cookie(key='id_pengajuan') # set cookie 
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