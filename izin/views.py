from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin import site
from functools import wraps
from django.views.decorators.cache import cache_page
from django.utils.decorators import available_attrs
from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon
from izin.models import JenisIzin, Syarat, KelompokJenisIzin
from django.shortcuts import get_object_or_404

import json
from django.utils.decorators import method_decorator

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

def layanan_siup(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=17)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Surat Perizinan Usaha Perdagangan (SIUP)"})
	extra_context.update({'title_short': "SIUP"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "6" })
	extra_context.update({'id_kelompok_jenis_izin': "17" })
	response = render(request, "front-end/layanan/siup.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value=17)
	return response

def layanan_ho_baru(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=12)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Gangguan (HO) - Permohonan Baru"})
	extra_context.update({'title_short': "HO - Permohonan Baru"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "2" })
	extra_context.update({'id_kelompok_jenis_izin': "12" })
	return render(request, "front-end/layanan/ho_baru.html", extra_context)

def layanan_ho_daftar_ulang(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=13)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Gangguan (HO) - Daftar Ulang"})
	extra_context.update({'title_short': "HO - Daftar Ulang"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "2" })
	extra_context.update({'id_kelompok_jenis_izin': "13" })
	return render(request, "front-end/layanan/ho_daftar_ulang.html", extra_context)

def layanan_tdp_pt(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=25)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - PT"})
	extra_context.update({'title_short': "TDP - Persero Terbatas (PT)"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "7" })
	extra_context.update({'id_kelompok_jenis_izin': "25" })
	return render(request, "front-end/layanan/tdp_pt.html", extra_context)

def layanan_tdp_cv(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=26)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - CV"})
	extra_context.update({'title_short': "TDP - CV"})
	extra_context.update({'link_formulir': reverse("formulir_tdp_cv") })
	extra_context.update({'id_jenis_izin': "7" })
	extra_context.update({'id_kelompok_jenis_izin': "26" })
	return render(request, "front-end/layanan/tdp_cv.html", extra_context)

def layanan_tdp_firma(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=27)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - Firma"})
	extra_context.update({'title_short': "TDP - Firma"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "7" })
	extra_context.update({'id_kelompok_jenis_izin': "27" })
	return render(request, "front-end/layanan/tdp_firma.html", extra_context)

def layanan_tdp_perorangan(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=28)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - Perorangan"})
	extra_context.update({'title_short': "TDP - Perorangan"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "7" })
	extra_context.update({'id_kelompok_jenis_izin': "28" })
	return render(request, "front-end/layanan/tdp_perorangan.html", extra_context)

def layanan_tdp_koperasi(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=29)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - Koperasi"})
	extra_context.update({'title_short': "TDP - Koperasi"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "7" })
	extra_context.update({'id_kelompok_jenis_izin': "29" })
	return render(request, "front-end/layanan/tdp_koperasi.html", extra_context)

def layanan_tdp_bul(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=30)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - Bentuk Usaha Lainnya"})
	extra_context.update({'title_short': "TDP - BUL"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "7" })
	extra_context.update({'id_kelompok_jenis_izin': "30" })
	return render(request, "front-end/layanan/tdp_bul.html", extra_context)

def layanan_tdp_baru_cabang(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=31)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - Kantor Cabang"})
	extra_context.update({'title_short': "TDP - Kantor Cabang"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "7" })
	extra_context.update({'id_kelompok_jenis_izin': "31" })
	return render(request, "front-end/layanan/tdp_cabang.html", extra_context)

def layanan_tdp_daftar_ulang(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=32)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - Permohonan Ulang"})
	extra_context.update({'title_short': "TDP - Permohonan Ulang"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "7" })
	extra_context.update({'id_kelompok_jenis_izin': "32" })
	return render(request, "front-end/layanan/tdp_daftar_ulang.html", extra_context)

def layanan_imb_umum(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=2)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Mendirikan Bangunan (IMB) - Umum"})
	extra_context.update({'title_short': "IMB - Umum"})
	extra_context.update({'link_formulir': reverse("formulir_imb_umum") })
	extra_context.update({'id_jenis_izin': "1" })
	extra_context.update({'id_kelompok_jenis_izin': "2" })
	return render(request, "front-end/layanan/imb_umum.html", extra_context)

def layanan_imb_reklame(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=1)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Mendirikan Bangunan (IMB) - Papan Reklame"})
	extra_context.update({'title_short': "IMB - Umum"})
	extra_context.update({'link_formulir': reverse("formulir_imb_reklame") })
	extra_context.update({'id_jenis_izin': "1" })
	extra_context.update({'id_kelompok_jenis_izin': "1" })
	return render(request, "front-end/layanan/imb_reklame.html", extra_context)

def layanan_imb_perumahan(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=1)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Mendirikan Bangunan (IMB) - Perumahan"})
	extra_context.update({'title_short': "IMB - Perumahan"})
	extra_context.update({'link_formulir': reverse("formulir_imb_perumahan") })
	extra_context.update({'id_jenis_izin': "1" })
	extra_context.update({'id_kelompok_jenis_izin': "1" })
	return render(request, "front-end/layanan/imb_perumahan.html", extra_context)

def layanan_reklame(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=14)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Pemasangan Reklame"})
	extra_context.update({'title_short': "Izin Pemasangan Reklame"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "3" })
	extra_context.update({'id_kelompok_jenis_izin': "14" })
	return render(request, "front-end/layanan/reklame.html", extra_context)

def layanan_kekayaan(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=16)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Pemakaian Kekayaan Daerah"})
	extra_context.update({'title_short': "Izin Pemakaian Kekayaan Daerah"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "5" })
	extra_context.update({'id_kelompok_jenis_izin': "16" })
	return render(request, "front-end/layanan/kekayaan.html", extra_context)

def layanan_huller(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=15)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Usaha Perusahaan Penggilingan Padi & Huller"})
	extra_context.update({'title_short': "Huller"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "4" })
	extra_context.update({'id_kelompok_jenis_izin': "15" })
	return render(request, "front-end/layanan/huller.html", extra_context)

def layanan_izin_prinsip_penanaman_modal(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=33)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Prinsip Penanaman Modal"})
	extra_context.update({'title_short': "Izin Prinsip Penanaman Modal"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "8" })
	extra_context.update({'id_kelompok_jenis_izin': "33" })
	return render(request, "front-end/layanan/izin_prinsip_penanaman_modal.html", extra_context)

def layanan_izin_prinsip_perluasan_penanaman_modal(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=35)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Prinsip Perluasan Penanaman Modal"})
	extra_context.update({'title_short': "Izin Prinsip Perluasan Penanaman Modal"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "9" })
	extra_context.update({'id_kelompok_jenis_izin': "35" })
	return render(request, "front-end/layanan/izin_prinsip_perluasan_penanaman_modal.html", extra_context)

def layanan_izin_prinsip_perubahan_penanaman_modal(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=1)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Prinsip Perubahan Penanaman Modal"})
	extra_context.update({'title_short': "Izin Prinsip Perubahan Penanaman Modal"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "10" })
	extra_context.update({'id_kelompok_jenis_izin': "1" })
	return render(request, "front-end/layanan/izin_prinsip_perubahan_penanaman_modal.html", extra_context)

def layanan_izin_usaha_dan_izin_usaha_perluasan_penanaman_modal(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=1)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Usaha dan Izin Usaha Perluasan Penanaman Modal"})
	extra_context.update({'title_short': "Izin Usaha dan Izin Usaha Perluasan Penanaman Modal"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "11" })
	extra_context.update({'id_kelompok_jenis_izin': "1" })
	return render(request, "front-end/layanan/izin_usaha_dan_izin_usaha_perluasan_penanaman_modal.html", extra_context)

def layanan_izin_usaha_perubahan_penanaman_modal(request, extra_context={}): 
	kelompok = get_object_or_404(KelompokJenisIzin, id=1)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Usaha Perubahan Penanaman Modal"})
	extra_context.update({'title_short': "Izin Usaha Perubahan Penanaman Modal"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "12" })
	extra_context.update({'id_kelompok_jenis_izin': "1" })
	return render(request, "front-end/layanan/izin_usaha_perubahan_penanaman_modal.html", extra_context)

def layanan_izin_usaha_penggabunggan_penanaman_modal(request, extra_context={}): 
	kelompok = get_object_or_404(KelompokJenisIzin, id=1)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Usaha Penggabungan Penanaman Modal"})
	extra_context.update({'title_short': "Izin Usaha Penggabungan Penanaman Modal"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "13" })
	extra_context.update({'id_kelompok_jenis_izin': "1" })
	return render(request, "front-end/layanan/izin_usaha_penggabunggan_penanaman_modal.html", extra_context)

def cari_pengajuan(request):
	return render(request, "front-end/cari_pengajuan.html")

def layanan_sipa_sumur_bor(request, extra_context={}):
	return render(request, "front-end/layanan/sipa_sumur_bor.html")

def layanan_sipa_sumur_pasak(request, extra_context={}):
	return render(request, "front-end/layanan/sipa_sumur_pasak.html")

def layanan_pertambangan(request, extra_context={}):
	return render(request, "front-end/layanan/pertambangan.html")

def formulir_siup(request, extra_context={}):
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
	jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) # Untuk SIUP
	extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	return render(request, "front-end/formulir/siup.html", extra_context)

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

from izin.izin_forms import PemohonForm, PerusahaanForm
from izin.utils import get_nomor_pengajuan
from accounts.models import NomorIdentitasPengguna
from izin.models import PengajuanIzin, Pemohon, JenisPermohonanIzin
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

try:
	from django.utils.encoding import force_text
except ImportError:
	from django.utils.encoding import force_unicode as force_text

from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

def siup_identitas_pemohon_save_cookie(request):
	pemohon = PemohonForm(request.POST) 
	if pemohon.is_valid():
		# Untuk Nomor Identitas
		ktp_ = request.POST.get('ktp', None)
		paspor_ = request.POST.get('paspor', None)
		# End
		jenis_permohonan_ = request.POST.get('jenis_pengajuan', None)
		k = KelompokJenisIzin.objects.filter(id=request.COOKIES['id_kelompok_izin']).last()
		nomor_pengajuan_ = get_nomor_pengajuan(k.jenis_izin.kode)
		try:
			p = pemohon.save(commit=False)
			# print pemohon.cleaned_data
			p.username = ktp_
			p.save()
			if ktp_:
				try:
					i = NomorIdentitasPengguna.objects.get(nomor = ktp_)
				except ObjectDoesNotExist:
					i, created = NomorIdentitasPengguna.objects.get_or_create(
								nomor = ktp_,
								jenis_identitas_id=1, # untuk KTP harusnya membutuhkan kode lagi
								user_id=p.id,
								)
			if paspor_:
				try:
					i = NomorIdentitasPengguna.objects.get(nomor = paspor_)
				except ObjectDoesNotExist:
					i, created = NomorIdentitasPengguna.objects.get_or_create(
								nomor = paspor_,
								jenis_identitas_id=2,
								user_id=p.id,
								)

			# SIMPAN PENGAJUAN verified_at=datetime.datetime.now(),
			pengajuan = PengajuanIzin(no_pengajuan=nomor_pengajuan_,kelompok_jenis_izin_id=request.COOKIES['id_kelompok_izin'], pemohon_id=p.id,jenis_permohonan_id=jenis_permohonan_, created_by=request.user )
			pengajuan.save()
			data = {'success': True, 'pesan': 'Pemohon dan Pengajuan disimpan. Proses Selanjutnya.'  }
			response = HttpResponse(json.dumps(data))
		except IntegrityError as e:
			if ktp_:
				p = Pemohon.objects.get(username = ktp_)
			elif paspor_:
				p = Pemohon.objects.get(username = paspor_)
			elif ktp_ and paspor_:
				p = Pemohon.objects.get(username = ktp_)

			# print p.id
			# print p.desa
			
			pengajuan = PengajuanIzin(no_pengajuan=nomor_pengajuan_, kelompok_jenis_izin_id=request.COOKIES['id_kelompok_izin'], pemohon_id=p.id,jenis_permohonan_id=jenis_permohonan_, created_by=request.user  )
			pengajuan.save()

			data = {'success': True, 'pesan': 'Pengajuan disimpan. Proses Selanjutnya.'  }
			response = HttpResponse(json.dumps(data))	

		response.set_cookie(key='id_pemohon', value=p.id)
		response.set_cookie(key='nama_lengkap', value=p.nama_lengkap) # set cookie	
		if jenis_permohonan_:
			response.set_cookie(key='jenis_permohonan', value=pengajuan.jenis_permohonan) # set cookie	
		if ktp_ or paspor_:
			value = ""
			if ktp_:
				value += "KTP "+str(ktp_)
			if paspor_:
				value += ", PASPOR "+str(paspor_)
			response.set_cookie(key='ktp', value=value) # set cookie	
		if p.desa:
			alamat_ = str(p.alamat)+" "+str(p.desa)+", Kec. "+str(p.desa.kecamatan)+", Kab./Kota "+str(p.desa.kecamatan.kabupaten)
			response.set_cookie(key='alamat', value=alamat_) # set cookie	
		if p.jenis_pemohon:
			response.set_cookie(key='jenis_pemohon', value=p.jenis_pemohon) # set cookie	
		if p.hp:
			response.set_cookie(key='hp', value=p.hp) # set cookie	
		if p.telephone:
			response.set_cookie(key='telephone', value=p.telephone) # set cookie	
		if p.kewarganegaraan:
			response.set_cookie(key='kewarganegaraan', value=p.kewarganegaraan) # set cookie	
		if p.tempat_lahir:
			ttl_ = str(p.tempat_lahir)+", "+str(p.tanggal_lahir)
			response.set_cookie(key='ttl', value=ttl_) # set cookie
		if p.email:
			response.set_cookie(key='email', value=p.email) # set cookie	
	else:
		data = pemohon.errors.as_json() # untuk mengembalikan error form berupa json
		# data = {'success': False, 'pesan': 'Pengisian tidak lengkap.', 'error':pemohon.errors.as_json() }
		# response = HttpResponse(json.dumps(data))
		response = HttpResponse(data)
	return response

def siup_identitas_perusahan_save_cookie(request):
	# print request.COOKIES # Untuk Tes cookies
	perusahaan = PerusahaanForm(request.POST) 
	if perusahaan.is_valid():
		p = perusahaan.save(commit=False)
		p.pemohon_id = request.COOKIES['id_pemohon']
		p.save()

		data = {'success': True, 'pesan': 'Perusahaan disimpan. Proses Selanjutnya.'  }
		response = HttpResponse(json.dumps(data))
		
		response.set_cookie(key='npwp', value=p.npwp)
		response.set_cookie(key='nama_perusahaan', value=p.nama_perusahaan)
		alamat_ = str(p.alamat_perusahaan)+" "+str(p.desa)+", Kec. "+str(p.desa.kecamatan)+", Kab./Kota "+str(p.desa.kecamatan.kabupaten)
		response.set_cookie(key='alamat_perusahaan', value=alamat_)
		response.set_cookie(key='kode_pos', value=p.kode_pos)
		response.set_cookie(key='telepon', value=p.telepon)
		response.set_cookie(key='fax', value=p.fax)
		response.set_cookie(key='email', value=p.email)

	else:
		data = perusahaan.errors.as_json()
		response = HttpResponse(data)
	return response

def siup_legalitas_perusahaan_save_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.' }
	return HttpResponse(json.dumps(data))

def siup_kekayaan_save_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.' }
	return HttpResponse(json.dumps(data))

def siup_upload_dokumen_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.' }
	return HttpResponse(json.dumps(data))

def siup_done(request):
	data = {'success': True, 'pesan': 'Proses Selesai.' }
	response = HttpResponse(json.dumps(data))
	# For delete cookie
	response.delete_cookie(key='nama_lengkap') # set cookie	
	response.delete_cookie(key='id_pemohon') # set cookie	
	response.delete_cookie(key='jenis_permohonan') # set cookie
	response.delete_cookie(key='ktp') # set cookie	
	response.delete_cookie(key='alamat') # set cookie
	response.delete_cookie(key='jenis_pemohon') # set cookie
	response.delete_cookie(key='hp') # set cookie	
	response.delete_cookie(key='telephone') # set cookie
	response.delete_cookie(key='kewarganegaraan') # set cookie
	response.delete_cookie(key='ttl') # set cookie
	response.delete_cookie(key='email') # set cookie	
	response.delete_cookie(key='id_kelompok_izin') # set cookie	
	return response


def cetak_permohonan(request, extra_context={}):
	return render(request, "front-end/cetak.html", extra_context)

def cetak_bukti_pendaftaran(request, extra_context={}):
	syarat = Syarat.objects.filter(jenis_izin__jenis_izin__kode="SIUP")
	extra_context.update({'syarat': syarat})
	return render(request, "front-end/cetak_bukti_pendaftaran.html", extra_context)
