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

def layanan_siup_pt(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=17)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Surat Perizinan Usaha Perdagangan (SIUP) - PT"})
	extra_context.update({'title_short': "SIUP - PT"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "6" })
	extra_context.update({'id_kelompok_jenis_izin': "17" })
	return render(request, "front-end/layanan/siup_pt.html", extra_context)

def layanan_siup_koperasi(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=18)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Surat Perizinan Usaha Perdagangan (SIUP) - Koperasi"})
	extra_context.update({'title_short': "SIUP - Koperasi"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "6" })
	extra_context.update({'id_kelompok_jenis_izin': "18" })
	return render(request, "front-end/layanan/siup_koperasi.html", extra_context)

def layanan_siup_cv(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=19)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Surat Perizinan Usaha Perdagangan (SIUP) - CV dan Firma"})
	extra_context.update({'title_short': "SIUP - CV dan Firma"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "6" })
	extra_context.update({'id_kelompok_jenis_izin': "19" })
	return render(request, "front-end/layanan/siup_cv.html", extra_context)

def layanan_siup_perorangan(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=20)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Surat Perizinan Usaha Perdagangan (SIUP) - Perorangan"})
	extra_context.update({'title_short': "SIUP - Perorangan"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "6" })
	extra_context.update({'id_kelompok_jenis_izin': "20" })
	return render(request, "front-end/layanan/siup_perorangan.html", extra_context)

def layanan_siup_pendaftaran_ulang(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=21)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Surat Perizinan Usaha Perdagangan (SIUP) - Pendaftaran Ulang"})
	extra_context.update({'title_short': "SIUP - Pendaftaran Ulang"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "6" })
	extra_context.update({'id_kelompok_jenis_izin': "21" })
	return render(request, "front-end/layanan/siup_pendaftaran_ulang.html", extra_context)

def layanan_siup_perubahan(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=22)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Surat Perizinan Usaha Perdagangan (SIUP) - Perubahan"})
	extra_context.update({'title_short': "SIUP - Perubahan"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "6" })
	extra_context.update({'id_kelompok_jenis_izin': "22" })
	return render(request, "front-end/layanan/siup_perubahan.html", extra_context)

def layanan_siup_pergantian_hilang(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=23)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Surat Perizinan Usaha Perdagangan (SIUP) - Pergantian Hilang"})
	extra_context.update({'title_short': "SIUP - Pergantian Hilang"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "6" })
	extra_context.update({'id_kelompok_jenis_izin': "23" })
	return render(request, "front-end/layanan/siup_pergantian_hilang.html", extra_context)

def layanan_siup_pergantian_rusak(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=24)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Surat Perizinan Usaha Perdagangan (SIUP) - Pergantian Rusak"})
	extra_context.update({'title_short': "SIUP - Pergantian Rusak"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "6" })
	extra_context.update({'id_kelompok_jenis_izin': "24" })
	return render(request, "front-end/layanan/siup_pergantian_rusak.html", extra_context)

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

from izin.izin_forms import PemohonForm

def siup_identitas_pemohon_save_cookie(request):
	pemohon = PemohonForm(request.POST)
	if pemohon.is_valid():
		nama_lengkap = pemohon.cleaned_data.get('nama_lengkap')
		data = {'success': True, 'pesan': 'Proses Selanjutnya.' }
		response = HttpResponse(json.dumps(data))	
		response.set_cookie(key='nama_lengkap', value=nama_lengkap) # set cookie
	else:
		# data = pemohon.errors.as_json() # untuk mengembalikan error form berupa json
		data = {'success': False, 'pesan': 'Pengisian tidak lengkap.' }
		response = HttpResponse(json.dumps(data))
	return response

def siup_identitas_perusahan_save_cookie(request):
	# print request.COOKIES # Untuk Tes cookies
	data = {'success': True, 'pesan': 'Proses Selanjutnya.' }
	return HttpResponse(json.dumps(data))

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
	return HttpResponse(json.dumps(data))
