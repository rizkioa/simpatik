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

from master.models import Negara, Kecamatan, JenisPemohon,JenisReklame,Berkas,ParameterBangunan,JenisKontruksi
from izin.models import JenisIzin, Syarat, KelompokJenisIzin, JenisPermohonanIzin,Riwayat
from izin.models import PengajuanIzin, DetilIMB,Pemohon
from izin.utils import STATUS_HAK_TANAH,KLASIFIKASI_JALAN,RUMIJA,RUWASJA,JENIS_LOKASI_USAHA
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna
from izin.izin_forms import UploadBerkasKTPForm,UploadBerkasPendukungForm,DetilIMBForm,ParameterBangunanForm,JenisBangunanForm
from accounts.utils import KETERANGAN_PEKERJAAN

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
	jenis_kontruksi_list = JenisKontruksi.objects.all()
	
	extra_context.update({'jenis_kontruksi_list': jenis_kontruksi_list})
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
	return render(request, "front-end/formulir/imb_umum.html", extra_context)

def cetak_imb_umum(request, id_pengajuan_):
	extra_context = {}
	url_ = reverse('formulir_reklame')
	if id_pengajuan_:
		pengajuan_ = DetilIMB.objects.get(id=id_pengajuan_)
		if pengajuan_.pemohon:
			if pengajuan_.pemohon.desa:
				alamat_ = str(pengajuan_.pemohon.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.pemohon.desa.kecamatan.kabupaten.nama_kabupaten.title())
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
	template = loader.get_template("front-end/include/imb_umum/cetak.html")
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))

def cetak_bukti_pendaftaran_imb_umum(request,id_pengajuan_):
	extra_context = {}
	if id_pengajuan_:
		pengajuan_ = DetilIMB.objects.get(id=id_pengajuan_)
		if pengajuan_.pemohon:
			if pengajuan_.pemohon.desa:
			  alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.pemohon.desa.kecamatan.kabupaten.nama_kabupaten.title())
			  extra_context.update({ 'alamat_pemohon': alamat_ })
			extra_context.update({ 'pemohon': pengajuan_.pemohon })
			paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
			ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
			extra_context.update({ 'paspor': paspor_ })
			extra_context.update({ 'ktp': ktp_ })
			syarat = Syarat.objects.filter(jenis_izin__jenis_izin__kode="IMB")
			letak_ = pengajuan_.lokasi + ", Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())

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

	template = loader.get_template("front-end/include/imb_umum/cetak_bukti_pendaftaran.html")
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))

def imb_save_cookie(request):
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
						'pesan': 'Data IMB berhasil disimpan. Proses Selanjutnya.',
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
				pengajuan_.total_biaya  = request.POST.get('total_biaya')
				pengajuan_.save()
				if pengajuan_.parameter_bangunan.exists():
					pengajuan_.parameter_bangunan.clear() 
					for i in parameter:
						pengajuan_.parameter_bangunan.add(i)
				else:
					for i in parameter:
						pengajuan_.parameter_bangunan.add(i)
				total_biaya = pengajuan_.total_biaya 
				data = {'success': True,
						'pesan': 'Data IMB berhasil disimpan. Proses Selanjutnya.',
						'data': [
						{'total_biaya': total_biaya},
						]}
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

def jenis_bangunan_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilIMB.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			jenis_bangunan = JenisBangunanForm(request.POST, instance=pengajuan_)
			if jenis_bangunan.is_valid():
				pengajuan_.pemohon_id  = request.COOKIES['id_pemohon']
				pengajuan_.save()  
				data = {'success': True,
						'pesan': 'Data IMB berhasil disimpan. Proses Selanjutnya.',
						'data':{} }
				data = json.dumps(data)
				response = HttpResponse(json.dumps(data))
			else:
				data = jenis_bangunan.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response

def imb_done(request):
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

def load_data_imb(request,id_pengajuan):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilIMB.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			nama_bangunan = pengajuan_.bangunan
			luas_bangunan = str(pengajuan_.luas_bangunan)
			jumlah_bangunan = str(pengajuan_.jumlah_bangunan)
			id_lokasi = pengajuan_.lokasi
			if pengajuan_.desa:
			  id_kecamatan = str(pengajuan_.desa.kecamatan.id)
			  id_desa = str(pengajuan_.desa.id)
			else:
			  id_kecamatan = ""
			  id_desa = ""
			luas_tanah = str(pengajuan_.luas_tanah)
			status_tanah = pengajuan_.status_hak_tanah
			no_surat_tanah = pengajuan_.no_surat_tanah
			if pengajuan_.tanggal_surat_tanah:
				tanggal_surat_tanah = pengajuan_.tanggal_surat_tanah.strftime("%d-%m-%Y")
			else:
				tanggal_surat_tanah = ""
			if pengajuan_.luas_bangunan_lama:
				luas_bangunan_lama = pengajuan_.luas_bangunan_lama
			else:
				luas_bangunan_lama = ""
			no_imb_lama = pengajuan_.no_imb_lama
			if pengajuan_.tanggal_imb_lama:
				tanggal_imb_lama = pengajuan_.tanggal_imb_lama.strftime("%d-%m-%Y")
			else:
				tanggal_imb_lama = ""
			id_batas_utara = pengajuan_.batas_utara
			id_batas_timur = pengajuan_.batas_timur
			id_batas_selatan = pengajuan_.batas_selatan
			id_batas_barat = pengajuan_.batas_barat

			data = {'success': True,'data':{'nama_bangunan': nama_bangunan,'luas_bangunan': luas_bangunan,'jumlah_bangunan': jumlah_bangunan,'luas_tanah': luas_tanah,'status_tanah': status_tanah,'no_surat_tanah': no_surat_tanah,'id_lokasi':id_lokasi,'tanggal_surat_tanah': tanggal_surat_tanah,'luas_bangunan_lama': luas_bangunan_lama,'no_imb_lama': no_imb_lama,'tanggal_imb_lama': tanggal_imb_lama,'id_kecamatan':id_kecamatan,'id_desa':id_desa,'id_batas_utara': id_batas_utara,'id_batas_timur': id_batas_timur,'id_batas_selatan': id_batas_selatan,'id_batas_barat': id_batas_barat,}}
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

def load_identifikasi_bangunan_imb(request,id_pengajuan):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilIMB.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			# print pengajuan_.kelompok_jenis_izin.kode
			if pengajuan_.jenis_bangunan != None or pengajuan_.kelompok_jenis_izin.kode == "503.01.04/":
				if pengajuan_.kelompok_jenis_izin.kode == "503.01.04/":
					kode_izin = pengajuan_.kelompok_jenis_izin.kode
					if pengajuan_.jenis_bangunan:
						kode_kontruksi_bangunan = str(pengajuan_.jenis_bangunan.kode)
						id_kontruksi = str(pengajuan_.jenis_bangunan.jenis_kontruksi.id)
						id_jenis_bangunan = str(pengajuan_.jenis_bangunan.id)
					else:
						kode_kontruksi_bangunan = ""
						id_kontruksi = ""
						id_jenis_bangunan = ""
					if pengajuan_.parameter_bangunan.exists():
						kegiatan_pembangunan = pengajuan_.parameter_bangunan.get(parameter="Kegiatan Pembangunan Gedung")
						nilai_kegiatan_pembangunan = str(kegiatan_pembangunan.nilai)
						kegiatan_pembangunan = kegiatan_pembangunan.id

						fungsi_bangunan = pengajuan_.parameter_bangunan.get(parameter="Fungsi Bangunan")
						nilai_fungsi_bangunan = str(fungsi_bangunan.nilai)
						fungsi_bangunan = fungsi_bangunan.id

						kompleksitas_bangunan = pengajuan_.parameter_bangunan.get(parameter="Tingkat Kompleksitas")
						nilai_kompleksitas_bangunan = str(kompleksitas_bangunan.nilai)
						kompleksitas_bangunan = kompleksitas_bangunan.id

						permanensi_bangunan = pengajuan_.parameter_bangunan.get(parameter="Tingkat Permanensi")
						nilai_permanensi_bangunan = str(permanensi_bangunan.nilai)
						permanensi_bangunan = permanensi_bangunan.id

						ketinggian_bangunan = pengajuan_.parameter_bangunan.get(parameter="Ketinggian Bangunan")
						nilai_ketinggian_bangunan = str(ketinggian_bangunan.nilai)
						ketinggian_bangunan = ketinggian_bangunan.id

						letak_bangunan = pengajuan_.parameter_bangunan.get(parameter="Lokasi Bangunan")
						nilai_letak_bangunan = str(letak_bangunan.nilai)
						letak_bangunan = letak_bangunan.id

						kepemilikan_bangunan = pengajuan_.parameter_bangunan.get(parameter="Kepemilikan Bangunan")	
						nilai_kepemilikan_bangunan = str(kepemilikan_bangunan.nilai)
						kepemilikan_bangunan = kepemilikan_bangunan.id

						lama_penggunaan_bangunan = pengajuan_.parameter_bangunan.get(parameter="Lama Penggunaan Bangunan")
						nilai_lama_penggunaan_bangunan = str(lama_penggunaan_bangunan.nilai)
						lama_penggunaan_bangunan = lama_penggunaan_bangunan.id
						total_biaya = str(pengajuan_.total_biaya) 
					else:
						kegiatan_pembangunan = ""
						nilai_kegiatan_pembangunan = ""
						fungsi_bangunan = ""
						nilai_fungsi_bangunan = ""
						kompleksitas_bangunan = ""
						nilai_kompleksitas_bangunan = ""
						permanensi_bangunan = ""
						nilai_permanensi_bangunan = ""
						ketinggian_bangunan = ""
						nilai_ketinggian_bangunan = ""
						letak_bangunan = ""
						nilai_letak_bangunan = ""
						kepemilikan_bangunan = ""
						nilai_kepemilikan_bangunan = ""
						lama_penggunaan_bangunan = ""
						nilai_lama_penggunaan_bangunan = ""
						total_biaya = "0"
						
					total_biaya = str(pengajuan_.total_biaya) 
					data = {'success': True,
							'data': {
							'kode_izin':kode_izin,
							'kode_kontruksi_bangunan':kode_kontruksi_bangunan,
							'id_kontruksi':id_kontruksi,
							'id_jenis_bangunan':id_jenis_bangunan,
							'id_jenis_bangunan':id_jenis_bangunan,
							'nama_fungsi_bangunan': fungsi_bangunan,
							'nilai_fungsi_bangunan': nilai_fungsi_bangunan,
							'kegiatan_pembangunan': kegiatan_pembangunan,
							'nilai_kegiatan_pembangunan': nilai_kegiatan_pembangunan,
							'kompleksitas_bangunan': kompleksitas_bangunan,
							'nilai_kompleksitas_bangunan': nilai_kompleksitas_bangunan,
							'permanensi_bangunan': permanensi_bangunan,
							'nilai_permanensi_bangunan': nilai_permanensi_bangunan,
							'ketinggian_bangunan': ketinggian_bangunan,
							'nilai_ketinggian_bangunan': nilai_ketinggian_bangunan,
							'letak_bangunan': letak_bangunan,
							'nilai_letak_bangunan': nilai_letak_bangunan,
							'kepemilikan_bangunan': kepemilikan_bangunan,
							'nilai_kepemilikan_bangunan': nilai_kepemilikan_bangunan,
							'lama_penggunaan_bangunan': lama_penggunaan_bangunan,
							'nilai_lama_penggunaan_bangunan': nilai_lama_penggunaan_bangunan,
							'total_biaya': total_biaya}}
				elif  pengajuan_.jenis_bangunan.kode == "BK1" or pengajuan_.jenis_bangunan.kode == "BK23":
					kode_izin = pengajuan_.kelompok_jenis_izin.kode
					if pengajuan_.jenis_bangunan:
						kode_kontruksi_bangunan = str(pengajuan_.jenis_bangunan.kode)
						id_kontruksi = str(pengajuan_.jenis_bangunan.jenis_kontruksi.id)
						id_jenis_bangunan = str(pengajuan_.jenis_bangunan.id)
					else:
						kode_kontruksi_bangunan = ""
						id_kontruksi = ""
						id_jenis_bangunan = ""
					if pengajuan_.parameter_bangunan.exists():
						kegiatan_pembangunan = pengajuan_.parameter_bangunan.get(parameter="Kegiatan Pembangunan Gedung")
						nilai_kegiatan_pembangunan = str(kegiatan_pembangunan.nilai)
						kegiatan_pembangunan = kegiatan_pembangunan.id

						fungsi_bangunan = pengajuan_.parameter_bangunan.get(parameter="Fungsi Bangunan")
						nilai_fungsi_bangunan = str(fungsi_bangunan.nilai)
						fungsi_bangunan = fungsi_bangunan.id

						kompleksitas_bangunan = pengajuan_.parameter_bangunan.get(parameter="Tingkat Kompleksitas")
						nilai_kompleksitas_bangunan = str(kompleksitas_bangunan.nilai)
						kompleksitas_bangunan = kompleksitas_bangunan.id

						permanensi_bangunan = pengajuan_.parameter_bangunan.get(parameter="Tingkat Permanensi")
						nilai_permanensi_bangunan = str(permanensi_bangunan.nilai)
						permanensi_bangunan = permanensi_bangunan.id

						ketinggian_bangunan = pengajuan_.parameter_bangunan.get(parameter="Ketinggian Bangunan")
						nilai_ketinggian_bangunan = str(ketinggian_bangunan.nilai)
						ketinggian_bangunan = ketinggian_bangunan.id

						letak_bangunan = pengajuan_.parameter_bangunan.get(parameter="Lokasi Bangunan")
						nilai_letak_bangunan = str(letak_bangunan.nilai)
						letak_bangunan = letak_bangunan.id

						kepemilikan_bangunan = pengajuan_.parameter_bangunan.get(parameter="Kepemilikan Bangunan")	
						nilai_kepemilikan_bangunan = str(kepemilikan_bangunan.nilai)
						kepemilikan_bangunan = kepemilikan_bangunan.id

						lama_penggunaan_bangunan = pengajuan_.parameter_bangunan.get(parameter="Lama Penggunaan Bangunan")
						nilai_lama_penggunaan_bangunan = str(lama_penggunaan_bangunan.nilai)
						lama_penggunaan_bangunan = lama_penggunaan_bangunan.id
						total_biaya = str(pengajuan_.total_biaya) 
					else:
						kegiatan_pembangunan = ""
						nilai_kegiatan_pembangunan = ""
						fungsi_bangunan = ""
						nilai_fungsi_bangunan = ""
						kompleksitas_bangunan = ""
						nilai_kompleksitas_bangunan = ""
						permanensi_bangunan = ""
						nilai_permanensi_bangunan = ""
						ketinggian_bangunan = ""
						nilai_ketinggian_bangunan = ""
						letak_bangunan = ""
						nilai_letak_bangunan = ""
						kepemilikan_bangunan = ""
						nilai_kepemilikan_bangunan = ""
						lama_penggunaan_bangunan = ""
						nilai_lama_penggunaan_bangunan = ""
						total_biaya = "0"
					data = {'success': True,
							'data': {
							'kode_izin':kode_izin,
							'kode_kontruksi_bangunan':kode_kontruksi_bangunan,
							'id_kontruksi':id_kontruksi,
							'id_jenis_bangunan':id_jenis_bangunan,
							'id_jenis_bangunan':id_jenis_bangunan,
							'nama_fungsi_bangunan': fungsi_bangunan,
							'nilai_fungsi_bangunan': nilai_fungsi_bangunan,
							'kegiatan_pembangunan': kegiatan_pembangunan,
							'nilai_kegiatan_pembangunan': nilai_kegiatan_pembangunan,
							'kompleksitas_bangunan': kompleksitas_bangunan,
							'nilai_kompleksitas_bangunan': nilai_kompleksitas_bangunan,
							'permanensi_bangunan': permanensi_bangunan,
							'nilai_permanensi_bangunan': nilai_permanensi_bangunan,
							'ketinggian_bangunan': ketinggian_bangunan,
							'nilai_ketinggian_bangunan': nilai_ketinggian_bangunan,
							'letak_bangunan': letak_bangunan,
							'nilai_letak_bangunan': nilai_letak_bangunan,
							'kepemilikan_bangunan': kepemilikan_bangunan,
							'nilai_kepemilikan_bangunan': nilai_kepemilikan_bangunan,
							'lama_penggunaan_bangunan': lama_penggunaan_bangunan,
							'nilai_lama_penggunaan_bangunan': nilai_lama_penggunaan_bangunan,
							'total_biaya': total_biaya}}
				elif pengajuan_.jenis_bangunan.kode == "BK2" or pengajuan_.jenis_bangunan.kode == "BK17":
					kode_kontruksi_bangunan = str(pengajuan_.jenis_bangunan.kode)
					id_kontruksi = str(pengajuan_.jenis_bangunan.jenis_kontruksi.id)
					id_jenis_bangunan = str(pengajuan_.jenis_bangunan.id)
					id_panjang = str(pengajuan_.panjang)
					data = {'success': True,
							'data': {'kode_kontruksi_bangunan':kode_kontruksi_bangunan,'id_jenis_bangunan':id_jenis_bangunan,'id_panjang':id_panjang,'id_kontruksi':id_kontruksi}}
				else:
					id_kontruksi = str(pengajuan_.jenis_bangunan.jenis_kontruksi.id)
					id_jenis_bangunan = str(pengajuan_.jenis_bangunan.id)
					data = {'success': True,
							'data': {'id_jenis_bangunan':id_jenis_bangunan,'id_kontruksi':id_kontruksi}}
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


def load_konfirmasi_identifikasi_bangunan_imb(request,id_pengajuan):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilIMB.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			if pengajuan_.jenis_bangunan != None or pengajuan_.kelompok_jenis_izin.kode == "503.01.04/":
				if pengajuan_.kelompok_jenis_izin.kode == "503.01.04/":
					kode_izin = pengajuan_.kelompok_jenis_izin.kode
					if pengajuan_.jenis_bangunan:
						kode_kontruksi_bangunan = str(pengajuan_.jenis_bangunan.kode)
						id_kontruksi = str(pengajuan_.jenis_bangunan.jenis_kontruksi.id)
						id_jenis_bangunan = str(pengajuan_.jenis_bangunan.id)
					else:
						kode_kontruksi_bangunan = ""
						id_kontruksi = ""
						id_jenis_bangunan = ""
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
					data = {'success': True,
							'data': {'kode_izin':kode_izin,'kode_kontruksi_bangunan':kode_kontruksi_bangunan,'id_kontruksi':id_kontruksi,'id_jenis_bangunan':id_jenis_bangunan,'id_jenis_bangunan':id_jenis_bangunan,'nama_fungsi_bangunan': fungsi_bangunan.detil_parameter,'nilai_fungsi_bangunan': nilai_fungsi_bangunan,'kegiatan_pembangunan': kegiatan_pembangunan.detil_parameter,'nilai_kegiatan_pembangunan': nilai_kegiatan_pembangunan,'kompleksitas_bangunan': kompleksitas_bangunan.detil_parameter,'nilai_kompleksitas_bangunan': nilai_kompleksitas_bangunan,'permanensi_bangunan': permanensi_bangunan.detil_parameter,'nilai_permanensi_bangunan': nilai_permanensi_bangunan,'ketinggian_bangunan': ketinggian_bangunan.detil_parameter,'nilai_ketinggian_bangunan': nilai_ketinggian_bangunan,'letak_bangunan': letak_bangunan.detil_parameter,'nilai_letak_bangunan': nilai_letak_bangunan,'kepemilikan_bangunan': kepemilikan_bangunan.detil_parameter,'nilai_kepemilikan_bangunan': nilai_kepemilikan_bangunan,'lama_penggunaan_bangunan': lama_penggunaan_bangunan.detil_parameter,'nilai_lama_penggunaan_bangunan': nilai_lama_penggunaan_bangunan,'total_biaya': total_biaya}}
				elif pengajuan_.jenis_bangunan.kode == "BK1" or pengajuan_.jenis_bangunan.kode == "BK23":
					kode_kontruksi_bangunan = str(pengajuan_.jenis_bangunan.kode)
					id_kontruksi = pengajuan_.jenis_bangunan.jenis_kontruksi.nama_jenis_kontruksi
					id_jenis_bangunan = pengajuan_.jenis_bangunan.nama_bangunan

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
					data = {'success': True,
							'data': {'kode_kontruksi_bangunan':kode_kontruksi_bangunan,'id_kontruksi':id_kontruksi,'id_jenis_bangunan':id_jenis_bangunan,'id_jenis_bangunan':id_jenis_bangunan,'nama_fungsi_bangunan': fungsi_bangunan.detil_parameter,'nilai_fungsi_bangunan': nilai_fungsi_bangunan,'kegiatan_pembangunan': kegiatan_pembangunan.detil_parameter,'nilai_kegiatan_pembangunan': nilai_kegiatan_pembangunan,'kompleksitas_bangunan': kompleksitas_bangunan.detil_parameter,'nilai_kompleksitas_bangunan': nilai_kompleksitas_bangunan,'permanensi_bangunan': permanensi_bangunan.detil_parameter,'nilai_permanensi_bangunan': nilai_permanensi_bangunan,'ketinggian_bangunan': ketinggian_bangunan.detil_parameter,'nilai_ketinggian_bangunan': nilai_ketinggian_bangunan,'letak_bangunan': letak_bangunan.detil_parameter,'nilai_letak_bangunan': nilai_letak_bangunan,'kepemilikan_bangunan': kepemilikan_bangunan.detil_parameter,'nilai_kepemilikan_bangunan': nilai_kepemilikan_bangunan,'lama_penggunaan_bangunan': lama_penggunaan_bangunan.detil_parameter,'nilai_lama_penggunaan_bangunan': nilai_lama_penggunaan_bangunan,'total_biaya': total_biaya}}
				elif pengajuan_.jenis_bangunan.kode == "BK2" or pengajuan_.jenis_bangunan.kode == "BK17":
					kode_kontruksi_bangunan = str(pengajuan_.jenis_bangunan.kode)
					id_kontruksi = str(pengajuan_.jenis_bangunan.jenis_kontruksi.nama_jenis_kontruksi)
					id_jenis_bangunan = str(pengajuan_.jenis_bangunan.nama_bangunan)
					id_panjang = str(pengajuan_.panjang)
					data = {'success': True,
							'data': {'kode_kontruksi_bangunan':kode_kontruksi_bangunan,'id_jenis_bangunan':id_jenis_bangunan,'id_panjang':id_panjang,'id_kontruksi':id_kontruksi}}
				else:
					id_kontruksi = pengajuan_.jenis_bangunan.jenis_kontruksi.nama_jenis_kontruksi
					id_jenis_bangunan = pengajuan_.jenis_bangunan.nama_bangunan
					data = {'success': True,
						'data': {'id_jenis_bangunan':id_jenis_bangunan,'id_kontruksi':id_kontruksi}}
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

def load_identifikasi_jalan_imb(request,id_pengajuan):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != None:
			pengajuan_ = DetilIMB.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			if pengajuan_.klasifikasi_jalan != "":
				id_klasifikasi_jalan = pengajuan_.klasifikasi_jalan	 			
				id_ruang_milik_jalan = pengajuan_.ruang_milik_jalan				
				id_ruang_pengawasan_jalan = pengajuan_.ruang_pengawasan_jalan
				data = {'success': True,'data':{'id_klasifikasi_jalan': id_klasifikasi_jalan,'id_ruang_milik_jalan': id_ruang_milik_jalan,'id_ruang_pengawasan_jalan': id_ruang_pengawasan_jalan,}}
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

def load_konfirmasi_imb(request,id_pengajuan):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilIMB.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			nama_bangunan = pengajuan_.bangunan
			luas_bangunan = str(pengajuan_.luas_bangunan)
			jumlah_bangunan = str(pengajuan_.jumlah_bangunan)
			lokasi_bangunan = pengajuan_.lokasi + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
			luas_tanah = str(pengajuan_.luas_tanah)
			status_tanah = pengajuan_.status_hak_tanah
			no_surat_tanah = pengajuan_.no_surat_tanah
			if pengajuan_.tanggal_surat_tanah:
				tanggal_surat_tanah = pengajuan_.tanggal_surat_tanah.strftime("%d-%m-%Y")
			else:
				tanggal_surat_tanah = "-"
			if pengajuan_.luas_bangunan_lama:
				luas_bangunan_lama = pengajuan_.luas_bangunan_lama
			else:
				luas_bangunan_lama = "-"
			no_imb_lama = pengajuan_.no_imb_lama
			if pengajuan_.tanggal_imb_lama:
				tanggal_imb_lama = pengajuan_.tanggal_imb_lama.strftime("%d-%m-%Y")
			else:
				tanggal_imb_lama = "-"
			id_batas_utara = pengajuan_.batas_utara
			id_batas_timur = pengajuan_.batas_timur
			id_batas_selatan = pengajuan_.batas_selatan
			id_batas_barat = pengajuan_.batas_barat
			data = {'success': True,
					'data': [
					{'nama_bangunan': nama_bangunan},
					{'luas_bangunan': luas_bangunan},
					{'jumlah_bangunan': jumlah_bangunan},
					{'lokasi_bangunan': lokasi_bangunan},
					{'luas_tanah': luas_tanah},
					{'status_tanah': status_tanah},
					{'no_surat_tanah': no_surat_tanah},
					{'tanggal_surat_tanah': tanggal_surat_tanah},
					{'luas_bangunan_lama': luas_bangunan_lama},
					{'no_imb_lama': no_imb_lama},
					{'tanggal_imb_lama': tanggal_imb_lama},
					{'id_batas_utara': id_batas_utara},
					{'id_batas_timur': id_batas_timur},
					{'id_batas_selatan': id_batas_selatan},
					{'id_batas_barat': id_batas_barat}
					]}
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

def imbumum_upload_berkas_pendukung(request):
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
							berkas.nama_berkas = "Surat Kepemilikan Tanah atau Surat Penguasaan Hak atas Tanah"+p.no_pengajuan
							berkas.keterangan = "Surat Kepemilikan Tanah atau Surat Penguasaan Hak atas Tanah"
						elif request.POST.get('aksi') == "2":
							berkas.nama_berkas = "Berkas Foto KTP/PASPOR"+ktp_.nomor
							berkas.keterangan = "Berkas Foto KTP/PASPOR"
						elif request.POST.get('aksi') == "3":
							berkas.nama_berkas = "NPWP"+p.no_pengajuan
							berkas.keterangan = "NPWP"
						elif request.POST.get('aksi') == "4":
							berkas.nama_berkas = "Cetak Biru Bangunan"+p.no_pengajuan
							berkas.keterangan = "Cetak Biru Bangunan"
						elif request.POST.get('aksi') == "5":
							berkas.nama_berkas = "Surat Persetujuan/Perjanjian/Izin Pemilik tanah untuk bangunan yang didirikan diatas tanah yang bukan miliknya"+p.no_pengajuan
							berkas.keterangan = "Surat Persetujuan/Perjanjian/Izin Pemilik tanah untuk bangunan yang didirikan diatas tanah yang bukan miliknya"
						elif request.POST.get('aksi') == "6":
							berkas.nama_berkas = "Surat Persetujuan/Rekomendasi dari FKUB (Forum Komunikasi Umat Beragam) bagi bangunan fungsi keagamaan"+p.no_pengajuan
							berkas.keterangan = "Surat Persetujuan/Rekomendasi dari FKUB (Forum Komunikasi Umat Beragam) bagi bangunan fungsi keagamaan"
						else:
							berkas.nama_berkas = "Rekomendasi dari Instansi Teknis sesuai kegiatan/bangunan yang dimohonkan"+p.no_pengajuan
							berkas.keterangan = "Rekomendasi dari Instansi Teknis sesuai kegiatan/bangunan yang dimohonkan"
							
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

def ajax_load_berkas_imbumum(request, id_pengajuan):
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

		  surat_kepemilikan_tanah  = Berkas.objects.filter(nama_berkas="Surat Kepemilikan Tanah atau Surat Penguasaan Hak atas Tanah"+p.no_pengajuan)
		  if surat_kepemilikan_tanah.exists():
			  surat_kepemilikan_tanah = surat_kepemilikan_tanah.last()
			  url_berkas.append(surat_kepemilikan_tanah.berkas.url)
			  id_elemen.append('surat_kepemilikan_tanah')
			  nm_berkas.append("Surat Kepemilikan Tanah atau Surat Penguasaan Hak atas Tanah"+p.no_pengajuan)
			  id_berkas.append(surat_kepemilikan_tanah.id)

		  npwp = Berkas.objects.filter(nama_berkas="NPWP"+p.no_pengajuan)
		  if npwp.exists():
			  npwp = npwp.last()
			  url_berkas.append(npwp.berkas.url)
			  id_elemen.append('npwp')
			  nm_berkas.append("NPWP"+p.no_pengajuan)
			  id_berkas.append(npwp.id)

		  cetak_biru_bangunan = Berkas.objects.filter(nama_berkas="Cetak Biru Bangunan"+p.no_pengajuan)
		  if cetak_biru_bangunan.exists():
			  cetak_biru_bangunan = cetak_biru_bangunan.last()
			  url_berkas.append(cetak_biru_bangunan.berkas.url)
			  id_elemen.append('cetak_biru_bangunan')
			  nm_berkas.append("Cetak Biru Bangunan"+p.no_pengajuan)
			  id_berkas.append(cetak_biru_bangunan.id)

		  surat_persetujuan_pemilik_tanah = Berkas.objects.filter(nama_berkas="Surat Persetujuan/Perjanjian/Izin Pemilik tanah untuk bangunan yang didirikan diatas tanah yang bukan miliknya"+p.no_pengajuan)
		  if surat_persetujuan_pemilik_tanah.exists():
			  surat_persetujuan_pemilik_tanah = surat_persetujuan_pemilik_tanah.last()
			  url_berkas.append(surat_persetujuan_pemilik_tanah.berkas.url)
			  id_elemen.append('surat_persetujuan')
			  nm_berkas.append("Surat Persetujuan/Perjanjian/Izin Pemilik tanah untuk bangunan yang didirikan diatas tanah yang bukan miliknya"+p.no_pengajuan)
			  id_berkas.append(surat_persetujuan_pemilik_tanah.id)

		  surat_persetujuan_rekomendasi_fkub = Berkas.objects.filter(nama_berkas="Surat Persetujuan/Rekomendasi dari FKUB (Forum Komunikasi Umat Beragam) bagi bangunan fungsi keagamaan"+p.no_pengajuan)
		  if surat_persetujuan_rekomendasi_fkub.exists():
			  surat_persetujuan_rekomendasi_fkub = surat_persetujuan_rekomendasi_fkub.last()
			  url_berkas.append(surat_persetujuan_rekomendasi_fkub.berkas.url)
			  id_elemen.append('surat_persetujuan_rekomendasi_fkub')
			  nm_berkas.append("Surat Persetujuan/Rekomendasi dari FKUB (Forum Komunikasi Umat Beragam) bagi bangunan fungsi keagamaan"+p.no_pengajuan)
			  id_berkas.append(surat_persetujuan_rekomendasi_fkub.id)

		  surat_rekomendasi_instansi_teknis = Berkas.objects.filter(nama_berkas="Rekomendasi dari Instansi Teknis sesuai kegiatan/bangunan yang dimohonkan"+p.no_pengajuan)
		  if surat_rekomendasi_instansi_teknis.exists():
			  surat_rekomendasi_instansi_teknis = surat_rekomendasi_instansi_teknis.last()
			  url_berkas.append(surat_rekomendasi_instansi_teknis.berkas.url)
			  id_elemen.append('rekomendasi_instansi_teknis')
			  nm_berkas.append("Rekomendasi dari Instansi Teknis sesuai kegiatan/bangunan yang dimohonkan"+p.no_pengajuan)
			  id_berkas.append(surat_rekomendasi_instansi_teknis.id)

		  data = {'success': True, 'pesan': 'berkas pendukung Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
	  except ObjectDoesNotExist:
		  data = {'success': False, 'pesan': '' }
			
	response = HttpResponse(json.dumps(data))
	return response

def ajax_delete_berkas_imbumum(request, id_berkas):
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
		