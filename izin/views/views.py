from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin import site
from functools import wraps
from django.views.decorators.cache import cache_page
from django.utils.decorators import available_attrs


from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon
from izin.models import JenisIzin, Syarat, KelompokJenisIzin, JenisPermohonanIzin
from perusahaan.models import BentukKegiatanUsaha, JenisPenanamanModal, Kelembagaan, KBLI, ProdukUtama, JenisLegalitas
from izin.models import PengajuanIzin, DetilSIUP


from django.template import RequestContext, loader
import json
from django.utils.decorators import method_decorator
import time
from datetime import datetime

def passes_test_cache(test_func, timeout=None, using=None, key_prefix=None):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request):
                return cache_page(timeout, cache=using, key_prefix=key_prefix)(view_func)(request, *args, **kwargs)
            else:
                return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def frontindex(request):
	return render(request, "front-end/index.html")

def page_404(request):
	return render(request, "error/404.html")

def frontlogin(request):
	return render(request, "front-end/login.html")

def tentang(request):
	return render(request, "front-end/tentang.html")

def layanan(request):
	return render(request, "front-end/layanan.html")

def cari_pengajuan(request):
	return render(request, "front-end/cari_pengajuan.html")

def formulir_siup(request, extra_context={}):
	negara = Negara.objects.all()
	provinsi = Provinsi.objects.all()
	kabupaten = Kabupaten.objects.all()
	kecamatan = Kecamatan.objects.all()
	desa = Desa.objects.all()

	extra_context.update({'negara': negara})
	extra_context.update({'provinsi': provinsi})
	extra_context.update({'kabupaten': kabupaten})
	extra_context.update({'kecamatan': kecamatan})
	extra_context.update({'desa': desa})

	jenis_pemohon = JenisPemohon.objects.all()
	jenis_legalitas_list = JenisLegalitas.objects.all()
	bentuk_kegiatan_usaha_list = BentukKegiatanUsaha.objects.all()
	jenis_penanaman_modal_list = JenisPenanamanModal.objects.all()
	kelembagaan_list = Kelembagaan.objects.all()
	kbli_list = KBLI.objects.all()
	produk_utama_list = ProdukUtama.objects.all()

	extra_context.update({'jenis_pemohon': jenis_pemohon})
	extra_context.update({'bentuk_kegiatan_usaha_list': bentuk_kegiatan_usaha_list})
	extra_context.update({'jenis_penanaman_modal_list': jenis_penanaman_modal_list})
	extra_context.update({'kelembagaan_list': kelembagaan_list})
	extra_context.update({'kbli_list': kbli_list})
	extra_context.update({'produk_utama_list': produk_utama_list})
	extra_context.update({'jenis_legalitas_list': jenis_legalitas_list})

	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) # Untuk SIUP
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/siup.html", extra_context)

def formulir_ho_pemohonan_baru(request, extra_context={}):
	negara = Negara.objects.all()
	extra_context.update({'negara': negara})
	provinsi = Provinsi.objects.all()
	extra_context.update({'provinsi': provinsi})
	kabupaten = Kabupaten.objects.all()
	extra_context.update({'kabupaten': kabupaten})
	kecamatan = Kecamatan.objects.all()
	extra_context.update({'kecamatan': kecamatan})
	desa = Desa.objects.all()
	extra_context.update({'desa': desa})
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) 
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/ho_baru.html", extra_context)

def formulir_ho_daftar_ulang(request, extra_context={}):
	negara = Negara.objects.all()
	extra_context.update({'negara': negara})
	provinsi = Provinsi.objects.all()
	extra_context.update({'provinsi': provinsi})
	kabupaten = Kabupaten.objects.all()
	extra_context.update({'kabupaten': kabupaten})
	kecamatan = Kecamatan.objects.all()
	extra_context.update({'kecamatan': kecamatan})
	desa = Desa.objects.all()
	extra_context.update({'desa': desa})
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/ho_baru.html", extra_context)

def formulir_huller(request, extra_context={}):
	negara = Negara.objects.all()
	extra_context.update({'negara': negara})
	provinsi = Provinsi.objects.all()
	extra_context.update({'provinsi': provinsi})
	kabupaten = Kabupaten.objects.all()
	extra_context.update({'kabupaten': kabupaten})
	kecamatan = Kecamatan.objects.all()
	extra_context.update({'kecamatan': kecamatan})
	desa = Desa.objects.all()
	extra_context.update({'desa': desa})
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) 
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/huller.html", extra_context)

def formulir_reklame(request, extra_context={}):
	negara = Negara.objects.all()
	extra_context.update({'negara': negara})
	provinsi = Provinsi.objects.all()
	extra_context.update({'provinsi': provinsi})
	kabupaten = Kabupaten.objects.all()
	extra_context.update({'kabupaten': kabupaten})
	kecamatan = Kecamatan.objects.all()
	extra_context.update({'kecamatan': kecamatan})
	desa = Desa.objects.all()
	extra_context.update({'desa': desa})
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) 
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/reklame.html", extra_context)

def formulir_kekayaan(request, extra_context={}):
	negara = Negara.objects.all()
	extra_context.update({'negara': negara})
	provinsi = Provinsi.objects.all()
	extra_context.update({'provinsi': provinsi})
	kabupaten = Kabupaten.objects.all()
	extra_context.update({'kabupaten': kabupaten})
	kecamatan = Kecamatan.objects.all()
	extra_context.update({'kecamatan': kecamatan})
	desa = Desa.objects.all()
	extra_context.update({'desa': desa})
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) 
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/kekayaan.html", extra_context)

def formulir_tdp_pt(request, extra_context={}):
	negara = Negara.objects.all()
	extra_context.update({'negara': negara})
	provinsi = Provinsi.objects.all()
	extra_context.update({'provinsi': provinsi})
	kabupaten = Kabupaten.objects.all()
	extra_context.update({'kabupaten': kabupaten})
	kecamatan = Kecamatan.objects.all()
	extra_context.update({'kecamatan': kecamatan})
	desa = Desa.objects.all()
	extra_context.update({'desa': desa})
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	return render(request, "front-end/formulir/tdp_pt.html", extra_context)

def formulir_imb_umum(request, extra_context={}):
	negara = Negara.objects.all()
	extra_context.update({'negara': negara})
	provinsi = Provinsi.objects.all()
	extra_context.update({'provinsi': provinsi})
	kabupaten = Kabupaten.objects.all()
	extra_context.update({'kabupaten': kabupaten})
	kecamatan = Kecamatan.objects.all()
	extra_context.update({'kecamatan': kecamatan})
	desa = Desa.objects.all()
	extra_context.update({'desa': desa})
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	return render(request, "front-end/formulir/imb_umum.html", extra_context)

def formulir_imb_perumahan(request, extra_context={}):
	negara = Negara.objects.all()
	extra_context.update({'negara': negara})
	provinsi = Provinsi.objects.all()
	extra_context.update({'provinsi': provinsi})
	kabupaten = Kabupaten.objects.all()
	extra_context.update({'kabupaten': kabupaten})
	kecamatan = Kecamatan.objects.all()
	extra_context.update({'kecamatan': kecamatan})
	desa = Desa.objects.all()
	extra_context.update({'desa': desa})
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	return render(request, "front-end/formulir/imb_perumahan.html", extra_context)

def formulir_imb_reklame(request, extra_context={}):
	negara = Negara.objects.all()
	extra_context.update({'negara': negara})
	provinsi = Provinsi.objects.all()
	extra_context.update({'provinsi': provinsi})
	kabupaten = Kabupaten.objects.all()
	extra_context.update({'kabupaten': kabupaten})
	kecamatan = Kecamatan.objects.all()
	extra_context.update({'kecamatan': kecamatan})
	desa = Desa.objects.all()
	extra_context.update({'desa': desa})
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	return render(request, "front-end/formulir/imb_reklame.html", extra_context)

def formulir_tdp_cv(request, extra_context={}):
	negara = Negara.objects.all()
	extra_context.update({'negara': negara})
	provinsi = Provinsi.objects.all()
	extra_context.update({'provinsi': provinsi})
	kabupaten = Kabupaten.objects.all()
	extra_context.update({'kabupaten': kabupaten})
	kecamatan = Kecamatan.objects.all()
	extra_context.update({'kecamatan': kecamatan})
	desa = Desa.objects.all()
	extra_context.update({'desa': desa})
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	return render(request, "front-end/formulir/tdp_cv.html", extra_context)

def formulir_tdp_firma(request, extra_context={}):
	negara = Negara.objects.all()
	extra_context.update({'negara': negara})
	provinsi = Provinsi.objects.all()
	extra_context.update({'provinsi': provinsi})
	kabupaten = Kabupaten.objects.all()
	extra_context.update({'kabupaten': kabupaten})
	kecamatan = Kecamatan.objects.all()
	extra_context.update({'kecamatan': kecamatan})
	desa = Desa.objects.all()
	extra_context.update({'desa': desa})
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	return render(request, "front-end/formulir/tdp_firma.html", extra_context)

def formulir_tdp_perorangan(request, extra_context={}):
	negara = Negara.objects.all()
	extra_context.update({'negara': negara})
	provinsi = Provinsi.objects.all()
	extra_context.update({'provinsi': provinsi})
	kabupaten = Kabupaten.objects.all()
	extra_context.update({'kabupaten': kabupaten})
	kecamatan = Kecamatan.objects.all()
	extra_context.update({'kecamatan': kecamatan})
	desa = Desa.objects.all()
	extra_context.update({'desa': desa})
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	return render(request, "front-end/formulir/tdp_po.html", extra_context)

def formulir_tdp_koperasi(request, extra_context={}):
	negara = Negara.objects.all()
	extra_context.update({'negara': negara})
	provinsi = Provinsi.objects.all()
	extra_context.update({'provinsi': provinsi})
	kabupaten = Kabupaten.objects.all()
	extra_context.update({'kabupaten': kabupaten})
	kecamatan = Kecamatan.objects.all()
	extra_context.update({'kecamatan': kecamatan})
	desa = Desa.objects.all()
	extra_context.update({'desa': desa})
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	return render(request, "front-end/formulir/tdp_koperasi.html", extra_context)

def formulir_tdp_bul(request, extra_context={}):
	negara = Negara.objects.all()
	extra_context.update({'negara': negara})
	provinsi = Provinsi.objects.all()
	extra_context.update({'provinsi': provinsi})
	kabupaten = Kabupaten.objects.all()
	extra_context.update({'kabupaten': kabupaten})
	kecamatan = Kecamatan.objects.all()
	extra_context.update({'kecamatan': kecamatan})
	desa = Desa.objects.all()
	extra_context.update({'desa': desa})
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	return render(request, "front-end/formulir/tdp_bul.html", extra_context)

def identitas_pemohon(request, extra_context={}):
	nama_lengkap = request.POST.get("nama_lengkap", None)
	tempat_lahir = request.POST.get("tempat_lahir", None)
	tanggal_lahir = request.POST.get("tanggal_lahir", None)
	email = request.POST.get("email", None)
	provinsi = request.POST.get("provinsi", None)
	kabupaten = request.POST.get("kabupaten", None)
	kecamatan = request.POST.get("kecamatan", None)
	desa = request.POST.get("desa", None)
	kewarganegaraan = request.POST.get("kewarganegaraan", None)
	pekerjaan = request.POSt.get("pekerjaan", None)
	data = {'success': True, 'pesan': 'Simpan data siswa berhasil.', 'id_siswa': siswa.id }
	return HttpResponse(json.dumps(data))

def cetak_permohonan(request, extra_context={}):
	extra_context = {}
	url_ = reverse('formulir_siup')
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilSIUP.objects.get(id=request.COOKIES['id_pengajuan'])
			if pengajuan_.perusahaan != '':
				alamat_ = ""
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
				extra_context.update({ 'alamat_pemohon': alamat_ })
				extra_context.update({ 'alamat_perusahaan': alamat_perusahaan_ })
				extra_context.update({ 'pemohon': pengajuan_.pemohon })
				extra_context.update({ 'no_pengajuan': pengajuan_.no_pengajuan })
				extra_context.update({ 'perusahaan': pengajuan_.perusahaan })
				extra_context.update({ 'jenis_permohonan': pengajuan_.jenis_permohonan })
				extra_context.update({ 'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin })
				extra_context.update({ 'created_at': pengajuan_.created_at })
				response = loader.get_template("front-end/cetak.html")
			else:
				response = HttpResponseRedirect(url_)
				return response
		else:
			response = HttpResponseRedirect(url_)
			return response
	else:
		response = HttpResponseRedirect(url_)
		return response		 

	# pengajuan_list = PengajuanIzin.objects.filter(id=request.COOKIES['id_pengajuan'])
	# extra_context.update({'pengajuan_list': pengajuan_list})
	template = loader.get_template("front-end/cetak.html")
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))
	# return render(request, response , extra_context)

def cetak_bukti_pendaftaran(request, extra_context={}):
	extra_context = {}
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilSIUP.objects.get(id=request.COOKIES['id_pengajuan'])
			if pengajuan_.perusahaan != '':
				alamat_ = ""
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
				syarat = Syarat.objects.filter(jenis_izin__jenis_izin__kode="SIUP")
				extra_context.update({'syarat': syarat})
				extra_context.update({ 'alamat_pemohon': alamat_ })
				extra_context.update({ 'alamat_perusahaan': alamat_perusahaan_ })
				extra_context.update({ 'pemohon': pengajuan_.pemohon })
				extra_context.update({ 'no_pengajuan': pengajuan_.no_pengajuan })
				extra_context.update({ 'perusahaan': pengajuan_.perusahaan })
				extra_context.update({ 'jenis_permohonan': pengajuan_.jenis_permohonan })
				extra_context.update({ 'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin })
				extra_context.update({ 'created_at': pengajuan_.created_at })
				extra_context.update({ 'bentuk_kegiatan_usaha': pengajuan_.bentuk_kegiatan_usaha.kegiatan_usaha })
				extra_context.update({ 'status_penanaman_modal': pengajuan_.jenis_penanaman_modal.jenis_penanaman_modal })
				extra_context.update({ 'kekayaan_bersih': pengajuan_.kekayaan_bersih })
				extra_context.update({ 'total_nilai_saham': pengajuan_.total_nilai_saham })
				extra_context.update({ 'presentase_saham_nasional': pengajuan_.presentase_saham_nasional })
				extra_context.update({ 'presentase_saham_asing': pengajuan_.presentase_saham_asing })
				extra_context.update({ 'kelembagaan': pengajuan_.kelembagaan.kelembagaan })
				response = loader.get_template("front-end/cetak_bukti_pendaftaran.html")
			else:
				response = HttpResponseRedirect(url_)
				return response
		else:
			response = HttpResponseRedirect(url_)
			return response
	else:
		response = HttpResponseRedirect(url_)
		return response	

	template = loader.get_template("front-end/cetak_bukti_pendaftaran.html")
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))

def cetak_ho_baru(request, extra_context={}):
	return render(request, "front-end/include/formulir_ho_baru/cetak.html", extra_context)

def cetak_bukti_pendaftaran_ho_baru(request, extra_context={}):
	syarat = Syarat.objects.filter(jenis_izin__jenis_izin__kode="HO")
	extra_context.update({'syarat': syarat})
	return render(request, "front-end/include/formulir_ho_baru/cetak_bukti_pendaftaran.html", extra_context)

def cetak_reklame(request, extra_context={}):
	return render(request, "front-end/include/formulir_reklame/cetak.html", extra_context)

def cetak_bukti_pendaftaran_reklame(request, extra_context={}):
	syarat = Syarat.objects.filter(jenis_izin__jenis_izin__id="3")
	extra_context.update({'syarat': syarat})
	return render(request, "front-end/include/formulir_reklame/cetak_bukti_pendaftaran.html", extra_context)

def cetak_ho_perpanjang(request, extra_context={}):
	return render(request, "front-end/include/formulir_ho_baru/cetak_perpanjang.html", extra_context)

def cetak_bukti_pendaftaran_ho_perpanjang(request, extra_context={}):
	syarat = Syarat.objects.filter(jenis_izin__jenis_izin__kode="HO")
	extra_context.update({'syarat': syarat})
	return render(request, "front-end/include/formulir_ho_baru/cetak_bukti_perpanjangan.html", extra_context)

def cetak_huller(request, extra_context={}):
	return render(request, "front-end/include/formulir_huller/cetak.html", extra_context)

def cetak_bukti_pendaftaran_huller(request, extra_context={}):
	syarat = Syarat.objects.filter(jenis_izin__jenis_izin__id="4") #cetak bukti blm ada
	extra_context.update({'syarat': syarat})
	return render(request, "front-end/include/formulir_huller/cetak_bukti_pendaftaran.html", extra_context)

def cetak_kekayaan(request, extra_context={}):
	return render(request, "front-end/include/formulir_kekayaan/cetak.html", extra_context)

def cetak_bukti_pendaftaran_kekayaan(request, extra_context={}):
	syarat = Syarat.objects.filter(jenis_izin__jenis_izin__id="5") #cetak bukti blm ada
	extra_context.update({'syarat': syarat})
	return render(request, "front-end/include/formulir_kekayaan/cetak_bukti_pendaftaran.html", extra_context)
