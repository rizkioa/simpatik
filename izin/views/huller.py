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
import urllib

from master.models import Negara, Kecamatan, JenisPemohon,JenisReklame,Berkas,ParameterBangunan
from izin.models import JenisIzin, Syarat, KelompokJenisIzin, JenisPermohonanIzin,Riwayat
from izin.models import PengajuanIzin, DetilHuller,Pemohon,MesinHuller,MesinPerusahaan
from izin.utils import STATUS_HAK_TANAH
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna
from izin.izin_forms import UploadBerkasPendukungForm,DetilHullerForm,MesinHullerForm,MesinPerusahaanForm,DeilHllerKapaSitasPotensialForm

def detil_huller_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilHuller.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			detil_huller = DetilHullerForm(request.POST, instance=pengajuan_)
			if detil_huller.is_valid():
				pengajuan_.perusahaan_id  = request.COOKIES['id_perusahaan']
				pengajuan_.save()
				data = {'success': True,
						'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
						'data': ['']}
				data = json.dumps(data)
				response = HttpResponse(json.dumps(data))
			else:
				data = detil_huller.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response

def detil_huller_kapasitas_potensial_save_cookie(request):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
      pengajuan_ = DetilHuller.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
      kapasitas_potensial = DeilHllerKapaSitasPotensialForm(request.POST, instance=pengajuan_)
      if kapasitas_potensial.is_valid():
        kapasitas_potensial.save()
        data = {'success': True,
            'pesan': 'Data Kapasitas Potensial berhasil disimpan. Proses Selanjutnya.',
            'data': ['']}
        data = json.dumps(data)
        response = HttpResponse(json.dumps(data))
      else:
        data = kapasitas_potensial.errors.as_json()
    else:
      data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
      data = json.dumps(data)
  else:
    data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
    data = json.dumps(data)
  response = HttpResponse(data)
  return response

def mesin_perusahaan_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			nama_mesin = request.POST.get('nama_mesin')
			mesin_huller = MesinHuller.objects.get(mesin_huller=nama_mesin)
			detilhuller = DetilHuller.objects.get(id=request.COOKIES['id_pengajuan'])
			try:
				p = MesinPerusahaan.objects.get(mesin_huller_id=mesin_huller.id) 
				mesin_perusahaan = MesinPerusahaanForm(request.POST, instance=p)
			except ObjectDoesNotExist:
				mesin_perusahaan = MesinPerusahaanForm(request.POST)
			if request.method == 'POST':
				if mesin_perusahaan.is_valid():
					p = mesin_perusahaan.save(commit=False)
					p.mesin_huller = mesin_huller
					p.detil_huller = detilhuller
					p.save()
					data = {'success': True,
							'pesan': 'Data Mesin Perusahaan berhasil disimpan. Proses Selanjutnya.',
							'data': ['']}
					data = json.dumps(data)
					response = HttpResponse(json.dumps(data))
				else:
					data = mesin_perusahaan.errors.as_json()
			else:
				mesin_perusahaan = MesinPerusahaanForm()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response

def load_konfirmasi_detilhuller(request,id_pengajuan):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
      pengajuan_ = DetilHuller.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
      pemilik_badan_usaha = pengajuan_.pemilik_badan_usaha
      pengusaha_badan_usaha = pengajuan_.pengusaha_badan_usaha
      hubungan_pemilik_pengusaha = pengajuan_.hubungan_pemilik_pengusaha 
      pemilik_nama_badan_usaha = pengajuan_.pemilik_nama_badan_usaha
      pemilik_nama_perorangan = pengajuan_.pemilik_nama_perorangan 
      pemilik_alamat = pengajuan_.pemilik_alamat
      pengusaha_nama_perorangan = pengajuan_.pengusaha_nama_perorangan
      pengusaha_alamat = pengajuan_.pengusaha_alamat
      pengusaha_nama_badan_usaha = pengajuan_.pengusaha_nama_badan_usaha

      data = {'success': True,
          'data': {'pemilik_badan_usaha': pemilik_badan_usaha,'pengusaha_badan_usaha': pengusaha_badan_usaha,'hubungan_pemilik_pengusaha': hubungan_pemilik_pengusaha,'pemilik_nama_badan_usaha':pemilik_nama_badan_usaha,'pemilik_nama_perorangan':pemilik_nama_perorangan,'pemilik_alamat':pemilik_alamat,'pengusaha_nama_perorangan':pengusaha_nama_perorangan,'pengusaha_alamat':pengusaha_alamat,'pengusaha_nama_badan_usaha':pengusaha_nama_badan_usaha}}
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

def load_true_false_detilhuller(request,id_pengajuan):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
      pengajuan_ = DetilHuller.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
      pemilik_badan_usaha = pengajuan_.pemilik_badan_usaha
      pengusaha_badan_usaha = pengajuan_.pengusaha_badan_usaha
      data = {'success': True,
              'data': [
              {'id_badan_hukum_perorangan_form': pemilik_badan_usaha},
              {'switch_badan_hukum_pengusaha': pengusaha_badan_usaha}]}
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

def load_data_detilhuller(request,id_pengajuan):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
      pengajuan_ = DetilHuller.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
      pemilik_badan_usaha = pengajuan_.pemilik_badan_usaha
      pengusaha_badan_usaha = pengajuan_.pengusaha_badan_usaha
      hubungan_pemilik_pengusaha = pengajuan_.hubungan_pemilik_pengusaha 
      if pemilik_badan_usaha == True and pengusaha_badan_usaha == True:
          pemilik_nama_badan_usaha = pengajuan_.pemilik_nama_badan_usaha
          pengusaha_nama_badan_usaha = pengajuan_.pengusaha_nama_badan_usaha
          data = {'success': True,
                      'data': 
                      {'nama_badan_hukum_pemilik': pemilik_nama_badan_usaha,'nama_badan_hukum_pengusaha': pengusaha_nama_badan_usaha,'hubungan_pemilik_pengusaha': hubungan_pemilik_pengusaha}}

      elif pemilik_badan_usaha == True and pengusaha_badan_usaha == False:
          pengusaha_nama_perorangan = pengajuan_.pengusaha_nama_perorangan
          pengusaha_alamat = pengajuan_.pengusaha_alamat
          pengusaha_desa = "0"
          pengusaha_kecamatan = "0"
          pengusaha_kabupaten = "0"
          pengusaha_provinsi = "0"
          pengusaha_negara = "0"
          if pengajuan_.pengusaha_desa:
            pengusaha_desa = str(pengajuan_.pengusaha_desa.id)
            pengusaha_kecamatan = str(pengajuan_.pengusaha_desa.kecamatan.id)
            pengusaha_kabupaten = str(pengajuan_.pengusaha_desa.kecamatan.kabupaten.id)
            pengusaha_provinsi = str(pengajuan_.pengusaha_desa.kecamatan.kabupaten.provinsi.id)
            pengusaha_negara = str(pengajuan_.pengusaha_desa.kecamatan.kabupaten.provinsi.negara.id)
          pengusaha_kwarganegaraan = pengajuan_.pengusaha_kewarganegaraan
          pemilik_nama_badan_usaha = pengajuan_.pemilik_nama_badan_usaha
          data = {'success': True,
                      'data': 
                      {'id_pengusaha_nama_perorangan': pengusaha_nama_perorangan,'id_pengusaha_alamat': pengusaha_alamat,'pengusaha_desa': pengusaha_desa,'id_kecamatan_pengusaha': pengusaha_kecamatan,'id_kabupaten_pengusaha': pengusaha_kabupaten,'id_provinsi_pengusaha': pengusaha_provinsi,'id_negara_pengusaha': pengusaha_negara,'pengusaha_kewarganegaraan': pengusaha_kwarganegaraan,'nama_badan_hukum_pemilik': pemilik_nama_badan_usaha,'hubungan_pemilik_pengusaha': hubungan_pemilik_pengusaha}}
      elif pemilik_badan_usaha == False and pengusaha_badan_usaha == True:
          pemilik_nama_perorangan = pengajuan_.pemilik_nama_perorangan
          pemilik_alamat = pengajuan_.pemilik_alamat
          pemilik_desa = "0"
          pemilik_kecamatan = "0"
          pemilik_kabupaten = "0"
          pemilik_provinsi = "0"
          pemilik_negara = "0"
          if pengajuan_.pemilik_desa:
            pemilik_desa = str(pengajuan_.pemilik_desa.id)
            pemilik_kecamatan = str(pengajuan_.pemilik_desa.kecamatan.id)
            pemilik_kabupaten = str(pengajuan_.pemilik_desa.kecamatan.kabupaten.id)
            pemilik_provinsi = str(pengajuan_.pemilik_desa.kecamatan.kabupaten.provinsi.id)
            pemilik_negara = str(pengajuan_.pemilik_desa.kecamatan.kabupaten.provinsi.negara.id)
          pemilik_kwarganegaraan = pengajuan_.pemilik_kewarganegaraan
          pengusaha_nama_badan_usaha = pengajuan_.pengusaha_nama_badan_usaha
          data = {'success': True,
                      'data': 
                      {'id_pemilik_nama_perorangan': pemilik_nama_perorangan,'id_pemilik_alamat': pemilik_alamat,'id_desa_perorangan': pemilik_desa,'id_kecamatan_perorangan': pemilik_kecamatan,'id_kabupaten_perorangan': pemilik_kabupaten,'id_provinsi_perorangan': pemilik_provinsi,'id_negara_perorangan': pemilik_negara,'id_pemilik_kewarganegaraan': pemilik_kwarganegaraan,'nama_badan_hukum_pengusaha': pengusaha_nama_badan_usaha,'hubungan_pemilik_pengusaha': hubungan_pemilik_pengusaha}}
      else:
          pengusaha_nama_perorangan = pengajuan_.pengusaha_nama_perorangan
          pengusaha_alamat = pengajuan_.pengusaha_alamat
          pemilik_nama_perorangan = pengajuan_.pemilik_nama_perorangan
          pemilik_alamat = pengajuan_.pemilik_alamat
          pemilik_kwarganegaraan = pengajuan_.pemilik_kewarganegaraan
          pengusaha_kwarganegaraan = pengajuan_.pengusaha_kewarganegaraan
          pengusaha_desa = "0"
          pengusaha_kecamatan = "0"
          pengusaha_kabupaten = "0"
          pengusaha_provinsi = "0"
          pengusaha_negara = "0"
          if pengajuan_.pengusaha_desa:
            pengusaha_desa = str(pengajuan_.pengusaha_desa.id)
            pengusaha_kecamatan = str(pengajuan_.pengusaha_desa.kecamatan.id)
            pengusaha_kabupaten = str(pengajuan_.pengusaha_desa.kecamatan.kabupaten.id)
            pengusaha_provinsi = str(pengajuan_.pengusaha_desa.kecamatan.kabupaten.provinsi.id)
            pengusaha_negara = str(pengajuan_.pengusaha_desa.kecamatan.kabupaten.provinsi.negara.id)
          pemilik_desa = "0"
          pemilik_kecamatan = "0"
          pemilik_kabupaten = "0"
          pemilik_provinsi = "0"
          pemilik_negara = "0"
          if pengajuan_.pemilik_desa:
            pemilik_desa = str(pengajuan_.pemilik_desa.id)
            pemilik_kecamatan = str(pengajuan_.pemilik_desa.kecamatan.id)
            pemilik_kabupaten = str(pengajuan_.pemilik_desa.kecamatan.kabupaten.id)
            pemilik_provinsi = str(pengajuan_.pemilik_desa.kecamatan.kabupaten.provinsi.id)
            pemilik_negara = str(pengajuan_.pemilik_desa.kecamatan.kabupaten.provinsi.negara.id)
          data = {'success': True,
                      'data': 
                      {'id_pengusaha_nama_perorangan': pengusaha_nama_perorangan,'id_pengusaha_alamat': pengusaha_alamat,'id_pemilik_nama_perorangan': pemilik_nama_perorangan,'id_pemilik_alamat': pemilik_alamat,'pengusaha_desa': pengusaha_desa,'id_kecamatan_pengusaha': pengusaha_kecamatan,'id_kabupaten_pengusaha': pengusaha_kabupaten,'id_provinsi_pengusaha': pengusaha_provinsi,'id_negara_pengusaha': pengusaha_negara,'id_desa_perorangan': pemilik_desa,'id_kecamatan_perorangan': pemilik_kecamatan,'id_kabupaten_perorangan': pemilik_kabupaten,'id_provinsi_perorangan': pemilik_provinsi,'id_negara_perorangan': pemilik_negara,'id_pemilik_kewarganegaraan': pemilik_kwarganegaraan,'pengusaha_kewarganegaraan': pengusaha_kwarganegaraan,'hubungan_pemilik_pengusaha': hubungan_pemilik_pengusaha}}
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

def load_data_mesin_detilhuller(request,id_pengajuan):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
      detilhuller = DetilHuller.objects.get(id=request.COOKIES['id_pengajuan'])
      mesin_perusahaan = MesinPerusahaan.objects.filter(detil_huller=request.COOKIES['id_pengajuan'])
      id_type_model_motor_bensin = ""
      id_pk_mesin_motor_bensin = ""
      id_buatan_motor_bensin = ""
      id_jumlah_unit_motor_bensin = ""

      id_type_model_motor_diesel = ""
      id_pk_mesin_motor_diesel = ""
      id_buatan_motor_diesel = ""
      id_jumlah_unit_motor_diesel = ""

      id_type_model_diesel_generating = ""
      id_pk_mesin_diesel_generating = ""
      id_buatan_diesel_generating = ""
      id_jumlah_unit_diesel_generating = ""

      id_type_model_rubber_roll = ""
      id_pk_mesin_rubber_roll = ""
      id_kapasitas_mesin_rubber_roll = ""
      id_buatan_rubber_roll = ""
      id_jumlah_unit_rubber_roll = ""

      id_type_model_flash_type = ""
      id_pk_mesin_flash_type = ""
      id_kapasitas_mesin_flash_type = ""
      id_buatan_flash_type = ""
      id_jumlah_unit_flash_type = ""

      id_type_model_gedogan = ""
      id_pk_mesin_gedogan = ""
      id_kapasitas_mesin_gedogan = ""
      id_buatan_gedogan = ""
      id_jumlah_unit_gedogan = ""

      id_type_model_dimple_plate = ""
      id_pk_mesin_dimple_plate = ""
      id_kapasitas_mesin_dimple_plate = ""
      id_buatan_dimple_plate = ""
      id_jumlah_unit_dimple_plate = ""

      id_type_model_screen = ""
      id_pk_mesin_screen = ""
      id_kapasitas_mesin_screen = ""
      id_buatan_screen = ""
      id_jumlah_unit_screen = ""

      id_type_model_slip_horizontal = ""
      id_pk_mesin_slip_horizontal = ""
      id_kapasitas_mesin_slip_horizontal = ""
      id_buatan_slip_horizontal = ""
      id_jumlah_unit_slip_horizontal = ""

      id_type_model_slip_vertikal = ""
      id_pk_mesin_slip_vertikal = ""
      id_kapasitas_mesin_slip_vertikal = ""
      id_buatan_slip_vertikal = ""
      id_jumlah_unit_slip_vertikal = ""

      id_type_model_paddy_cleaner = ""
      id_pk_mesin_paddy_cleaner = ""
      id_kapasitas_mesin_paddy_cleaner = ""
      id_buatan_paddy_cleaner = ""
      id_jumlah_unit_paddy_cleaner = ""

      id_type_model_polis_brushe = ""
      id_pk_mesin_polis_brushe = ""
      id_kapasitas_mesin_polis_brushe = ""
      id_buatan_polis_brushe = ""
      id_jumlah_unit_polis_brushe = ""

      id_type_model_grader = ""
      id_pk_mesin_grader = ""
      id_kapasitas_mesin_grader = ""
      id_buatan_grader = ""
      id_jumlah_unit_grader = ""

      id_type_model_kualitas = ""
      id_pk_mesin_kualitas = ""
      id_kapasitas_mesin_kualitas = ""
      id_buatan_kualitas = ""
      id_jumlah_unit_kualitas = ""

      motor_bensin = ""
      motor_diesel = ""
      diesel_generating_set = ""
      rubber_roll = ""
      flash_type = ""
      gedogan = ""
      dimple_plate = ""
      screen = ""
      mesin_slip_horisontal = ""
      mesin_slip_vertikal = ""
      paddy_cleaner = ""
      mesin_polis = ""
      grader = ""
      kualitas = ""
      try:
        motor_bensin = mesin_perusahaan.get(mesin_huller__mesin_huller="Motor Bensin")
        motor_diesel = mesin_perusahaan.get(mesin_huller__mesin_huller="Motor Diesel")
        diesel_generating_set = mesin_perusahaan.get(mesin_huller__mesin_huller="Diesel Generating Set")
        rubber_roll = mesin_perusahaan.get(mesin_huller__mesin_huller="Rubber Roll / Roll Karet")
        flash_type = mesin_perusahaan.get(mesin_huller__mesin_huller="Flash Type / Type Banting")
        gedogan = mesin_perusahaan.get(mesin_huller__mesin_huller="Gedogan")
        dimple_plate = mesin_perusahaan.get(mesin_huller__mesin_huller="Dimple Plate")
        screen = mesin_perusahaan.get(mesin_huller__mesin_huller="Screen")
        mesin_slip_horisontal = mesin_perusahaan.get(mesin_huller__mesin_huller="Mesin Slip Horizontal")
        mesin_slip_vertikal = mesin_perusahaan.get(mesin_huller__mesin_huller="Mesin Slip Vertikal")
        paddy_cleaner = mesin_perusahaan.get(mesin_huller__mesin_huller="Paddy Cleaner / Pembersih Gabah (Blower)")
        mesin_polis = mesin_perusahaan.get(mesin_huller__mesin_huller="Mesin Polis Brushe")
        grader = mesin_perusahaan.get(mesin_huller__mesin_huller="Grader / Mesin Pemisah")
        kualitas = mesin_perusahaan.get(mesin_huller__mesin_huller="Kualitas")
      except ObjectDoesNotExist:
        data = {'Terjadi Kesalahan': [{'message': 'Data Mesin tidak ada dalam daftar'}]}

      if motor_bensin:
        id_type_model_motor_bensin = motor_bensin.type_model
        id_pk_mesin_motor_bensin = motor_bensin.pk_mesin
        id_buatan_motor_bensin = motor_bensin.buatan
        id_jumlah_unit_motor_bensin = motor_bensin.jumlah_unit

      if motor_diesel:
        id_type_model_motor_diesel = motor_diesel.type_model
        id_pk_mesin_motor_diesel = motor_diesel.pk_mesin
        id_buatan_motor_diesel = motor_diesel.buatan
        id_jumlah_unit_motor_diesel = motor_diesel.jumlah_unit

      if diesel_generating_set:
        id_type_model_diesel_generating = diesel_generating_set.type_model
        id_pk_mesin_diesel_generating = diesel_generating_set.pk_mesin
        id_buatan_diesel_generating = diesel_generating_set.buatan
        id_jumlah_unit_diesel_generating = diesel_generating_set.jumlah_unit

      if rubber_roll:
        id_type_model_rubber_roll = rubber_roll.type_model
        id_pk_mesin_rubber_roll = rubber_roll.pk_mesin
        id_kapasitas_mesin_rubber_roll = rubber_roll.kapasitas
        id_buatan_rubber_roll = rubber_roll.buatan
        id_jumlah_unit_rubber_roll = rubber_roll.jumlah_unit

      if flash_type:
        id_type_model_flash_type = flash_type.type_model
        id_pk_mesin_flash_type = flash_type.pk_mesin
        id_kapasitas_mesin_flash_type = flash_type.kapasitas
        id_buatan_flash_type = flash_type.buatan
        id_jumlah_unit_flash_type = flash_type.jumlah_unit  

      if gedogan:
        id_type_model_gedogan = gedogan.type_model
        id_pk_mesin_gedogan = gedogan.pk_mesin
        id_kapasitas_mesin_gedogan = gedogan.kapasitas
        id_buatan_gedogan = gedogan.buatan
        id_jumlah_unit_gedogan = gedogan.jumlah_unit

      if dimple_plate:
        id_type_model_dimple_plate = dimple_plate.type_model
        id_pk_mesin_dimple_plate = dimple_plate.pk_mesin
        id_kapasitas_mesin_dimple_plate = dimple_plate.kapasitas
        id_buatan_dimple_plate = dimple_plate.buatan
        id_jumlah_unit_dimple_plate = dimple_plate.jumlah_unit

      if screen:
        id_type_model_screen = screen.type_model
        id_pk_mesin_screen = screen.pk_mesin
        id_kapasitas_mesin_screen = screen.kapasitas
        id_buatan_screen = screen.buatan
        id_jumlah_unit_screen = screen.jumlah_unit
      
      if mesin_slip_horisontal:
        id_type_model_slip_horizontal = mesin_slip_horisontal.type_model
        id_pk_mesin_slip_horizontal = mesin_slip_horisontal.pk_mesin
        id_kapasitas_mesin_slip_horizontal = mesin_slip_horisontal.kapasitas
        id_buatan_slip_horizontal = mesin_slip_horisontal.buatan
        id_jumlah_unit_slip_horizontal = mesin_slip_horisontal.jumlah_unit

      if mesin_slip_vertikal:
        id_type_model_slip_vertikal = mesin_slip_vertikal.type_model
        id_pk_mesin_slip_vertikal = mesin_slip_vertikal.pk_mesin
        id_kapasitas_mesin_slip_vertikal = mesin_slip_vertikal.kapasitas
        id_buatan_slip_vertikal = mesin_slip_vertikal.buatan
        id_jumlah_unit_slip_vertikal = mesin_slip_vertikal.jumlah_unit

      if paddy_cleaner:
        id_type_model_paddy_cleaner = paddy_cleaner.type_model
        id_pk_mesin_paddy_cleaner = paddy_cleaner.pk_mesin
        id_kapasitas_mesin_paddy_cleaner = paddy_cleaner.kapasitas
        id_buatan_paddy_cleaner = paddy_cleaner.buatan
        id_jumlah_unit_paddy_cleaner = paddy_cleaner.jumlah_unit

      if mesin_polis:
        id_type_model_polis_brushe = mesin_polis.type_model
        id_pk_mesin_polis_brushe = mesin_polis.pk_mesin
        id_kapasitas_mesin_polis_brushe = mesin_polis.kapasitas
        id_buatan_polis_brushe = mesin_polis.buatan
        id_jumlah_unit_polis_brushe = mesin_polis.jumlah_unit

      if grader:
        id_type_model_grader = grader.type_model
        id_pk_mesin_grader = grader.pk_mesin
        id_kapasitas_mesin_grader = grader.kapasitas
        id_buatan_grader = grader.buatan
        id_jumlah_unit_grader = grader.jumlah_unit

      if kualitas:
        id_type_model_kualitas = kualitas.type_model
        id_pk_mesin_kualitas = kualitas.pk_mesin
        id_kapasitas_mesin_kualitas = kualitas.kapasitas
        id_buatan_kualitas = kualitas.buatan
        id_jumlah_unit_kualitas = kualitas.jumlah_unit
 
      id_kapasitas_potensial_giling_beras_per_jam = str(detilhuller.kapasitas_potensial_giling_beras_per_jam)
      id_kapasitas_potensial_giling_beras_per_tahun = str(detilhuller.kapasitas_potensial_giling_beras_per_tahun)
      data = {'success': True,
              'data': [

              {'id_kapasitas_potensial_giling_beras_per_jam': id_kapasitas_potensial_giling_beras_per_jam},
              {'id_kapasitas_potensial_giling_beras_per_tahun': id_kapasitas_potensial_giling_beras_per_tahun},

              {'id_type_model_kualitas': id_type_model_kualitas},
              {'id_pk_mesin_kualitas': id_pk_mesin_kualitas},
              {'id_kapasitas_mesin_kualitas': id_kapasitas_mesin_kualitas},
              {'id_buatan_kualitas': id_buatan_kualitas},
              {'id_jumlah_unit_kualitas': id_jumlah_unit_kualitas},

              {'id_type_model_grader': id_type_model_grader},
              {'id_pk_mesin_grader': id_pk_mesin_grader},
              {'id_kapasitas_mesin_grader': id_kapasitas_mesin_grader},
              {'id_buatan_grader': id_buatan_grader},
              {'id_jumlah_unit_grader': id_jumlah_unit_grader},

              {'id_type_model_polis_brushe': id_type_model_polis_brushe},
              {'id_pk_mesin_polis_brushe': id_pk_mesin_polis_brushe},
              {'id_kapasitas_mesin_polis_brushe': id_kapasitas_mesin_polis_brushe},
              {'id_buatan_polis_brushe': id_buatan_polis_brushe},
              {'id_jumlah_unit_polis_brushe': id_jumlah_unit_polis_brushe},

              {'id_type_model_paddy_cleaner': id_type_model_paddy_cleaner},
              {'id_pk_mesin_paddy_cleaner': id_pk_mesin_paddy_cleaner},
              {'id_kapasitas_mesin_paddy_cleaner': id_kapasitas_mesin_paddy_cleaner},
              {'id_buatan_paddy_cleaner': id_buatan_paddy_cleaner},
              {'id_jumlah_unit_paddy_cleaner': id_jumlah_unit_paddy_cleaner},

              {'id_type_model_slip_vertikal': id_type_model_slip_vertikal},
              {'id_pk_mesin_slip_vertikal': id_pk_mesin_slip_vertikal},
              {'id_kapasitas_mesin_slip_vertikal': id_kapasitas_mesin_slip_vertikal},
              {'id_buatan_slip_vertikal': id_buatan_slip_vertikal},
              {'id_jumlah_unit_slip_vertikal': id_jumlah_unit_slip_vertikal},

              {'id_type_model_slip_horizontal': id_type_model_slip_horizontal},
              {'id_pk_mesin_slip_horizontal': id_pk_mesin_slip_horizontal},
              {'id_kapasitas_mesin_slip_horizontal': id_kapasitas_mesin_slip_horizontal},
              {'id_buatan_slip_horizontal': id_buatan_slip_horizontal},
              {'id_jumlah_unit_slip_horizontal': id_jumlah_unit_slip_horizontal},

              {'id_type_model_screen': id_type_model_screen},
              {'id_pk_mesin_screen': id_pk_mesin_screen},
              {'id_kapasitas_mesin_screen': id_kapasitas_mesin_screen},
              {'id_buatan_screen': id_buatan_screen},
              {'id_jumlah_unit_screen': id_jumlah_unit_screen},

              {'id_type_model_dimple_plate': id_type_model_dimple_plate},
              {'id_pk_mesin_dimple_plate': id_pk_mesin_dimple_plate},
              {'id_kapasitas_mesin_dimple_plate': id_kapasitas_mesin_dimple_plate},
              {'id_buatan_dimple_plate': id_buatan_dimple_plate},
              {'id_jumlah_unit_dimple_plate': id_jumlah_unit_dimple_plate},

              {'id_type_model_gedogan': id_type_model_gedogan},
              {'id_pk_mesin_gedogan': id_pk_mesin_gedogan},
              {'id_kapasitas_mesin_gedogan': id_kapasitas_mesin_gedogan},
              {'id_buatan_gedogan': id_buatan_gedogan},
              {'id_jumlah_unit_gedogan': id_jumlah_unit_gedogan},

              {'id_type_model_flash_type': id_type_model_flash_type},
              {'id_pk_mesin_flash_type': id_pk_mesin_flash_type},
              {'id_kapasitas_mesin_flash_type': id_kapasitas_mesin_flash_type},
              {'id_buatan_flash_type': id_buatan_flash_type},
              {'id_jumlah_unit_flash_type': id_jumlah_unit_flash_type},

              {'id_type_model_rubber_roll': id_type_model_rubber_roll},
              {'id_pk_mesin_rubber_roll': id_pk_mesin_rubber_roll},
              {'id_kapasitas_mesin_rubber_roll': id_kapasitas_mesin_rubber_roll},
              {'id_buatan_rubber_roll': id_buatan_rubber_roll},
              {'id_jumlah_unit_rubber_roll': id_jumlah_unit_rubber_roll},

              {'id_type_model_motor_diesel': id_type_model_motor_diesel},
              {'id_pk_mesin_motor_diesel': id_pk_mesin_motor_diesel},
              {'id_buatan_motor_diesel': id_buatan_motor_diesel},
              {'id_jumlah_unit_motor_diesel': id_jumlah_unit_motor_diesel},

              {'id_type_model_diesel_generating': id_type_model_diesel_generating},
              {'id_pk_mesin_diesel_generating': id_pk_mesin_diesel_generating},
              {'id_buatan_diesel_generating': id_buatan_diesel_generating},
              {'id_jumlah_unit_diesel_generating': id_jumlah_unit_diesel_generating},

              {'id_type_model_motor_bensin': id_type_model_motor_bensin},
              {'id_pk_mesin_motor_bensin': id_pk_mesin_motor_bensin},
              {'id_buatan_motor_bensin': id_buatan_motor_bensin},
              {'id_jumlah_unit_motor_bensin': id_jumlah_unit_motor_bensin}]}
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

def detilhuller_done(request):
  if 'id_pengajuan' in request.COOKIES.keys():
    if request.COOKIES['id_pengajuan'] != '':
      pengajuan_ = DetilHuller.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
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

def detilhuller_upload_berkas_pendukung(request):
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
                  berkas.nama_berkas = "Keputusan Izin Gangguan (HO)"+p.no_pengajuan
                  berkas.keterangan = "Keputusan Izin Gangguan (HO)"
                elif request.POST.get('aksi') == "2":
                  berkas.nama_berkas = "Akta Pendirian Perusahaan"+p.no_pengajuan
                  berkas.keterangan = "Akta Pendirian Perusahaan"
                elif request.POST.get('aksi') == "3":
                  berkas.nama_berkas = "File KTP/Paspor (Dirut / Pemilik / Pengurus / Penanggung Jawab)"+p.no_pengajuan
                  berkas.keterangan = "File KTP/Paspor (Dirut / Pemilik / Pengurus / Penanggung Jawab)"
                elif request.POST.get('aksi') == "4":
                  berkas.nama_berkas = "Foto 4x6cm"+p.no_pengajuan
                  berkas.keterangan = "Foto 4x6cm"
                elif request.POST.get('aksi') == "5":
                  berkas.nama_berkas = "Denah Bangunan dan Tata Letak Bangunan"+p.no_pengajuan
                  berkas.keterangan = "Denah Bangunan dan Tata Letak Bangunan"
                elif request.POST.get('aksi') == "6":
                  berkas.nama_berkas = "Rekomendasi dari Dinas Pertanian Kabupaten Kediri"+p.no_pengajuan
                  berkas.keterangan = "Rekomendasi dari Dinas Pertanian Kabupaten Kediri"
                elif request.POST.get('aksi') == "7":
                  berkas.nama_berkas = "Struktur Organisasi Pemilik jika berupa badan usaha"+p.no_pengajuan
                  berkas.keterangan = "Struktur Organisasi Pemilik jika berupa badan usaha"
                elif request.POST.get('aksi') == "8":
                  berkas.nama_berkas = "Struktur Organisasi Pengusaha jika berupa badan usaha"+p.no_pengajuan
                  berkas.keterangan = "Struktur Organisasi Pengusaha jika berupa badan usaha"
                elif request.POST.get('aksi') == "9":
                  berkas.nama_berkas = "Akta Pendirian Perusahaan Pemilik jika berupa badan usaha"+p.no_pengajuan
                  berkas.keterangan = "Akta Pendirian Perusahaan Pemilik jika berupa badan usaha"
                else:
                  berkas.nama_berkas = "Akta Pendirian Perusahaan Pengusaha jika berupa badan usaha"+p.no_pengajuan
                  berkas.keterangan = "Akta Pendirian Perusahaan Pengusaha jika berupa badan usaha"
                  
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

def ajax_load_berkas_detilhuller(request, id_pengajuan):
  url_berkas = []
  id_elemen = []
  nm_berkas =[]
  id_berkas =[]
  if id_pengajuan:
    try:
      p = PengajuanIzin.objects.get(id=request.COOKIES['id_pengajuan'])

      keputusan_izin_gangguan = Berkas.objects.filter(nama_berkas="Keputusan Izin Gangguan (HO)"+p.no_pengajuan)
      if keputusan_izin_gangguan.exists():
        keputusan_izin_gangguan = keputusan_izin_gangguan.last()
        url_berkas.append(keputusan_izin_gangguan.berkas.url)
        id_elemen.append('keputusan_izin_gangguan')
        nm_berkas.append("Keputusan Izin Gangguan (HO)"+p.no_pengajuan)
        id_berkas.append(keputusan_izin_gangguan.id)

      akta_pendirian_perusahaan = Berkas.objects.filter(nama_berkas="Akta Pendirian Perusahaan"+p.no_pengajuan)
      if akta_pendirian_perusahaan.exists():
        akta_pendirian_perusahaan = akta_pendirian_perusahaan.last()
        url_berkas.append(akta_pendirian_perusahaan.berkas.url)
        id_elemen.append('akta_pendirian_perusahaan')
        nm_berkas.append("Akta Pendirian Perusahaan"+p.no_pengajuan)
        id_berkas.append(akta_pendirian_perusahaan.id)

      upload_gambar_ktp = Berkas.objects.filter(nama_berkas="File KTP/Paspor (Dirut / Pemilik / Pengurus / Penanggung Jawab)"+p.no_pengajuan)
      if upload_gambar_ktp.exists():
        upload_gambar_ktp = upload_gambar_ktp.last()
        url_berkas.append(upload_gambar_ktp.berkas.url)
        id_elemen.append('file_ktp_paspor')
        nm_berkas.append("File KTP/Paspor (Dirut / Pemilik / Pengurus / Penanggung Jawab)"+p.no_pengajuan)
        id_berkas.append(upload_gambar_ktp.id)

      foto_4x6 = Berkas.objects.filter(nama_berkas="Foto 4x6cm"+p.no_pengajuan)
      if foto_4x6.exists():
        foto_4x6 = foto_4x6.last()
        url_berkas.append(foto_4x6.berkas.url)
        id_elemen.append('file_ktp_4x6')
        nm_berkas.append("Foto 4x6cm"+p.no_pengajuan)
        id_berkas.append(foto_4x6.id)

      denah_bangunan = Berkas.objects.filter(nama_berkas="Denah Bangunan dan Tata Letak Bangunan"+p.no_pengajuan)
      if denah_bangunan.exists():
        denah_bangunan = denah_bangunan.last()
        url_berkas.append(denah_bangunan.berkas.url)
        id_elemen.append('denah_bangunan')
        nm_berkas.append("Denah Bangunan dan Tata Letak Bangunan"+p.no_pengajuan)
        id_berkas.append(denah_bangunan.id)

      rekomendasi_dinas_pertanian = Berkas.objects.filter(nama_berkas="Rekomendasi dari Dinas Pertanian Kabupaten Kediri"+p.no_pengajuan)
      if rekomendasi_dinas_pertanian.exists():
        rekomendasi_dinas_pertanian = rekomendasi_dinas_pertanian.last()
        url_berkas.append(rekomendasi_dinas_pertanian.berkas.url)
        id_elemen.append('rekomendasi_dinas_pertanian')
        nm_berkas.append("Rekomendasi dari Dinas Pertanian Kabupaten Kediri"+p.no_pengajuan)
        id_berkas.append(rekomendasi_dinas_pertanian.id)

      struktur_organisasi_pemilik = Berkas.objects.filter(nama_berkas="Struktur Organisasi Pemilik jika berupa badan usaha"+p.no_pengajuan)
      if struktur_organisasi_pemilik.exists():
        struktur_organisasi_pemilik = struktur_organisasi_pemilik.last()
        url_berkas.append(struktur_organisasi_pemilik.berkas.url)
        id_elemen.append('struktur_organisasi_pemilik')
        nm_berkas.append("Struktur Organisasi Pemilik jika berupa badan usaha"+p.no_pengajuan)
        id_berkas.append(struktur_organisasi_pemilik.id)

      struktur_organisasi_pengusaha = Berkas.objects.filter(nama_berkas="Struktur Organisasi Pengusaha jika berupa badan usaha"+p.no_pengajuan)
      if struktur_organisasi_pengusaha.exists():
        struktur_organisasi_pengusaha = struktur_organisasi_pengusaha.last()
        url_berkas.append(struktur_organisasi_pengusaha.berkas.url)
        id_elemen.append('struktur_organisasi_pengusaha')
        nm_berkas.append("Struktur Organisasi Pengusaha jika berupa badan usaha"+p.no_pengajuan)
        id_berkas.append(struktur_organisasi_pengusaha.id)

      akta_perusahaan_pemilik = Berkas.objects.filter(nama_berkas="Akta Pendirian Perusahaan Pemilik jika berupa badan usaha"+p.no_pengajuan)
      if akta_perusahaan_pemilik.exists():
        akta_perusahaan_pemilik = akta_perusahaan_pemilik.last()
        url_berkas.append(akta_perusahaan_pemilik.berkas.url)
        id_elemen.append('akta_pendirian_perusahaan_pemilik_badan_usaha')
        nm_berkas.append("Akta Pendirian Perusahaan Pemilik jika berupa badan usaha"+p.no_pengajuan)
        id_berkas.append(akta_perusahaan_pemilik.id)

      akta_perusahaan_pengusaha = Berkas.objects.filter(nama_berkas="Akta Pendirian Perusahaan Pengusaha jika berupa badan usaha"+p.no_pengajuan)
      if akta_perusahaan_pengusaha.exists():
        akta_perusahaan_pengusaha = akta_perusahaan_pengusaha.last()
        url_berkas.append(akta_perusahaan_pengusaha.berkas.url)
        id_elemen.append('akta_pendirian_perusahaan_pengusaha_badan_usaha')
        nm_berkas.append("Akta Pendirian Perusahaan Pengusaha jika berupa badan usaha"+p.no_pengajuan)
        id_berkas.append(akta_perusahaan_pengusaha.id)

      data = {'success': True, 'pesan': 'berkas pendukung Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
    except ObjectDoesNotExist:
      data = {'success': False, 'pesan': '' }
      
    
  response = HttpResponse(json.dumps(data))
  return response

def cetak_huller(request, id_pengajuan_):
      extra_context = {}
      url_ = reverse('formulir_huller')
      if id_pengajuan_:
        pengajuan_ = DetilHuller.objects.get(id=id_pengajuan_)
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
          response = loader.get_template("front-end/include/formulir_huller/cetak.html")
        else:
          response = HttpResponseRedirect(url_)
          return response
      else:
        response = HttpResponseRedirect(url_)
        return response
      template = loader.get_template("front-end/include/formulir_huller/cetak.html")
      ec = RequestContext(request, extra_context)
      return HttpResponse(template.render(ec))

def cetak_bukti_pendaftaran_huller(request, id_pengajuan_):
    extra_context = {}
    if id_pengajuan_:
      pengajuan_ = DetilHuller.objects.get(id=id_pengajuan_)
      data_mesin = MesinPerusahaan.objects.filter(detil_huller=id_pengajuan_)

      try:
        motor_bensin = data_mesin.get(mesin_huller__mesin_huller="Motor Bensin")
        motor_diesel = data_mesin.get(mesin_huller__mesin_huller="Motor Diesel")
        diesel_generating_set = data_mesin.get(mesin_huller__mesin_huller="Diesel Generating Set")
        rubber_roll = data_mesin.get(mesin_huller__mesin_huller="Rubber Roll / Roll Karet")
        flash_type = data_mesin.get(mesin_huller__mesin_huller="Flash Type / Type Banting")
        gedogan = data_mesin.get(mesin_huller__mesin_huller="Gedogan")
        dimple_plate = data_mesin.get(mesin_huller__mesin_huller="Dimple Plate")
        screen = data_mesin.get(mesin_huller__mesin_huller="Screen")
        mesin_slip_horisontal = data_mesin.get(mesin_huller__mesin_huller="Mesin Slip Horizontal")
        mesin_slip_vertikal = data_mesin.get(mesin_huller__mesin_huller="Mesin Slip Vertikal")
        paddy_cleaner = data_mesin.get(mesin_huller__mesin_huller="Paddy Cleaner / Pembersih Gabah (Blower)")
        mesin_polis = data_mesin.get(mesin_huller__mesin_huller="Mesin Polis Brushe")
        grader = data_mesin.get(mesin_huller__mesin_huller="Grader / Mesin Pemisah")
        kualitas = data_mesin.get(mesin_huller__mesin_huller="Kualitas")
      except ObjectDoesNotExist:
        motor_bensin = ""
        motor_diesel = ""
        diesel_generating_set = ""
        rubber_roll = ""
        flash_type = ""
        gedogan = ""
        dimple_plate = ""
        screen = ""
        mesin_slip_horisontal = ""
        mesin_slip_vertikal = ""
        paddy_cleaner = ""
        mesin_polis = ""
        grader = ""
        kualitas = ""
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

        extra_context.update({ 'motor_bensin': motor_bensin })
        extra_context.update({ 'motor_diesel': motor_diesel })
        extra_context.update({ 'diesel_generating_set': diesel_generating_set })
        extra_context.update({ 'rubber_roll': rubber_roll })
        extra_context.update({ 'flash_type': flash_type })
        extra_context.update({ 'gedogan': gedogan })
        extra_context.update({ 'dimple_plate': dimple_plate })
        extra_context.update({ 'screen': screen })
        extra_context.update({ 'mesin_slip_horisontal': mesin_slip_horisontal })
        extra_context.update({ 'mesin_slip_vertikal': mesin_slip_vertikal })
        extra_context.update({ 'paddy_cleaner': paddy_cleaner })
        extra_context.update({ 'mesin_polis': mesin_polis })
        extra_context.update({ 'grader': grader })
        extra_context.update({ 'kualitas': kualitas })
        
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

    template = loader.get_template("front-end/include/formulir_huller/cetak_bukti_pendaftaran.html")
    ec = RequestContext(request, extra_context)
    return HttpResponse(template.render(ec))