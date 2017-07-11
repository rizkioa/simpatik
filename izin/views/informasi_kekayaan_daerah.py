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
from izin.models import PengajuanIzin, InformasiKekayaanDaerah, Pemohon
from izin.utils import STATUS_HAK_TANAH,JENIS_PENGGUNAAN
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna
from izin.izin_forms import UploadBerkasPendukungForm,InformasiKekayaanDaerahForm
from accounts.utils import KETERANGAN_PEKERJAAN
from django.shortcuts import get_object_or_404

def formulir_kekayaan(request, extra_context={}):
	jenis_pemohon = JenisPemohon.objects.all()
	negara = Negara.objects.all()
	kecamatan = Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35')

	extra_context.update({'negara': negara})
	extra_context.update({'kecamatan': kecamatan})
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	extra_context.update({'keterangan_pekerjaan': KETERANGAN_PEKERJAAN })
	extra_context.update({'jenis_penggunaan_list': JENIS_PENGGUNAAN })
	# print request.COOKIES['id_pengajuan']
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != "" and request.COOKIES['id_pengajuan'] != "0":
			try:
				kekayaan_obj = InformasiKekayaanDaerah.objects.get(id=request.COOKIES['id_pengajuan'])
				print kekayaan_obj
				print "###############"
				print request.COOKIES['id_pengajuan']
				print "###############"
				if kekayaan_obj:
					extra_context.update({'pengajuan_': kekayaan_obj })
			except ObjectDoesNotExist:
				pass
	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) 
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/kekayaan.html", extra_context)

def informasi_kekayaan_daerah_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = InformasiKekayaanDaerah.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			informasikekayaan = InformasiKekayaanDaerahForm(request.POST, instance=pengajuan_)
			if informasikekayaan.is_valid():
				if request.COOKIES['id_perusahaan'] != '0':
					pengajuan_.perusahaan_id  = request.COOKIES['id_perusahaan']
					pengajuan_.save()
					data = {'success': True,
						  'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
						  'data': ['']}
					response = HttpResponse(json.dumps(data))
				else:
					informasikekayaan.save()
					data = {'success': True,
						  'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
						  'data': {}}
					response = HttpResponse(json.dumps(data))
			else:
				data = informasikekayaan.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			response = HttpResponse(json.dumps(data))
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		response = HttpResponse(json.dumps(data))
	return response

def kekayaan_done(request):
  if 'id_pengajuan' in request.COOKIES.keys():
	if request.COOKIES['id_pengajuan'] != '':
	  pengajuan_ = InformasiKekayaanDaerah.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
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

def load_informasi_kekayaan_daerah(request,id_pengajuan):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = InformasiKekayaanDaerah.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			id_lokasi = pengajuan_.lokasi
			id_luas = str(pengajuan_.luas)
			id_penggunaan = pengajuan_.penggunaan
			if pengajuan_.desa:
				id_desa = str(pengajuan_.desa.id) 
				id_kecamatan = str(pengajuan_.desa.kecamatan.id)
			else:
				id_desa = ""
				id_kecamatan = ""

			data = {'success': True,
					'data': {'id_lokasi':id_lokasi,'id_luas': id_luas,'id_penggunaan': id_penggunaan,'id_desa': id_desa,'id_kecamatan':id_kecamatan}}
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


def load_konfirmasi_informasi_kekayaan_daerah(request,id_pengajuan):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = InformasiKekayaanDaerah.objects.filter(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan']).last()
			if pengajuan_:
				luas = str(pengajuan_.luas)
				penggunaan = pengajuan_.penggunaan
				lokasi = pengajuan_.lokasi + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)

				data = {'success': True,
						'data': [
						{'luas': luas},
						{'penggunaan': penggunaan},
						{'lokasi': lokasi},
						{'jenis_penggunaan': pengajuan_.jenis_penggunaan}
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
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response


def informasi_kekayaan_daerah_upload_berkas_pendukung(request):
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
									berkas.nama_berkas = "File KTP/Paspor (Dirut / Pemilik / Pengurus / Penanggung Jawab)"+p.no_pengajuan
									berkas.keterangan = "File KTP/Paspor (Dirut / Pemilik / Pengurus / Penanggung Jawab)"
								elif request.POST.get('aksi') == "2":
									berkas.nama_berkas = "Surat Tanda Lunas Retribusi"+p.no_pengajuan
									berkas.keterangan = "Surat Tanda Lunas Retribusi"
								else:
									berkas.nama_berkas = "Rekomendasi dari Dinas terkait (DISPENDA, BPKAD, Dinas Perhubungan/Dinas/Bagian.........)"+p.no_pengajuan
									berkas.keterangan = "Rekomendasi dari Dinas terkait (DISPENDA, BPKAD, Dinas Perhubungan/Dinas/Bagian.........)"
									
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

def ajax_load_berkas_informasi_kekayaan_daerah(request, id_pengajuan):
	url_berkas = []
	id_elemen = []
	nm_berkas =[]
	id_berkas =[]
	if id_pengajuan:
		try:
			p = PengajuanIzin.objects.get(id=request.COOKIES['id_pengajuan'])
			upload_gambar_ktp = Berkas.objects.filter(nama_berkas="File KTP/Paspor (Dirut / Pemilik / Pengurus / Penanggung Jawab)"+p.no_pengajuan)
			if upload_gambar_ktp.exists():
				upload_gambar_ktp = upload_gambar_ktp.last()
				url_berkas.append(upload_gambar_ktp.berkas.url)
				id_elemen.append('upload_gambar_ktp')
				nm_berkas.append("File KTP/Paspor (Dirut / Pemilik / Pengurus / Penanggung Jawab)"+p.no_pengajuan)
				id_berkas.append(upload_gambar_ktp.id)

			upload_gambar_surat_lunas_retribusi = Berkas.objects.filter(nama_berkas="Surat Tanda Lunas Retribusi"+p.no_pengajuan)
			if upload_gambar_surat_lunas_retribusi.exists():
				upload_gambar_surat_lunas_retribusi = upload_gambar_surat_lunas_retribusi.last()
				url_berkas.append(upload_gambar_surat_lunas_retribusi.berkas.url)
				id_elemen.append('upload_gambar_surat_lunas_retribusi')
				nm_berkas.append("Surat Tanda Lunas Retribusi"+p.no_pengajuan)
				id_berkas.append(upload_gambar_surat_lunas_retribusi.id)

			upload_gambar_rekomendasi_dinas_terkait = Berkas.objects.filter(nama_berkas="Rekomendasi dari Dinas terkait (DISPENDA, BPKAD, Dinas Perhubungan/Dinas/Bagian.........)"+p.no_pengajuan)
			if upload_gambar_rekomendasi_dinas_terkait.exists():
				upload_gambar_rekomendasi_dinas_terkait = upload_gambar_rekomendasi_dinas_terkait.last()
				url_berkas.append(upload_gambar_rekomendasi_dinas_terkait.berkas.url)
				id_elemen.append('upload_gambar_rekomendasi_dinas_terkait')
				nm_berkas.append("Rekomendasi dari Dinas terkait (DISPENDA, BPKAD, Dinas Perhubungan/Dinas/Bagian.........)"+p.no_pengajuan)
				id_berkas.append(upload_gambar_rekomendasi_dinas_terkait.id)


			data = {'success': True, 'pesan': 'berkas pendukung Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': '' }
	response = HttpResponse(json.dumps(data))
	return response

def cetak_informasi_kekayaan_daerah(request, id_pengajuan_):
	extra_context = {}
	url_ = reverse('formulir_reklame')
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(InformasiKekayaanDaerah, id=id_pengajuan_)
		extra_context.update({ 'pengajuan': pengajuan_ })
		pengajuan_id = base64.b64encode(str(pengajuan_.id))
		extra_context.update({ 'pengajuan_id': pengajuan_id })

		riwayat = Riwayat.objects.filter(pengajuan_izin=pengajuan_)
		if riwayat:
			extra_context.update({ 'riwayat': riwayat })
			extra_context.update({ 'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin })
			extra_context.update({ 'created_at': pengajuan_.created_at })
		response = loader.get_template("front-end/include/formulir_kekayaan/cetak.html")
	else:
		response = HttpResponseRedirect(url_)
		return response
	template = loader.get_template("front-end/include/formulir_kekayaan/cetak.html")
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))

def cetak_bukti_pendaftaran_informasi_kekayaan_daerah(request,id_pengajuan_):
	extra_context = {}
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(InformasiKekayaanDaerah, id=id_pengajuan_)
		if pengajuan_.perusahaan != '':
			syarat = Syarat.objects.filter(jenis_izin__jenis_izin__kode="IMB")
			extra_context.update({ 'pengajuan': pengajuan_ })
			extra_context.update({ 'syarat': syarat })
			response = loader.get_template("front-end/cetak_bukti_pendaftaran.html")
		else:
			response = HttpResponseRedirect(url_)
			return response
	else:
		response = HttpResponseRedirect(url_)
		return response 
	template = loader.get_template("front-end/include/formulir_kekayaan/cetak_bukti_pendaftaran.html")
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))