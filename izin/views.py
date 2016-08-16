from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin import site
from functools import wraps
from django.views.decorators.cache import cache_page
from django.utils.decorators import available_attrs
from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon

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

#@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
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

def layanan_siup(request):
	return render(request, "front-end/layanan/siup.html")

def layanan_ho(request):
	return render(request, "front-end/layanan/ho.html")

def layanan_sipa_sumur_bor(request):
	return render(request, "front-end/layanan/sipa_sumur_bor.html")

def layanan_sipa_sumur_pasak(request):
	return render(request, "front-end/layanan/sipa_sumur_pasak.html")

def layanan_pertambangan(request):
	return render(request, "front-end/layanan/pertambangan.html")

def layanan_tdp_pt(request):
	return render(request, "front-end/layanan/tdp_pt.html")

def layanan_tdp_cv(request):
	return render(request, "front-end/layanan/tdp_cv.html")

def layanan_tdp_firma(request):
	return render(request, "front-end/layanan/tdp_firma.html")

def layanan_tdp_perorangan(request):
	return render(request, "front-end/layanan/tdp_perorangan.html")

def layanan_tdp_koperasi(request):
	return render(request, "front-end/layanan/tdp_koperasi.html")

def layanan_tdp_bul(request):
	return render(request, "front-end/layanan/tdp_bul.html")

def layanan_reklame(request):
	return render(request, "front-end/layanan/reklame.html")

def layanan_kekayaan(request):
	return render(request, "front-end/layanan/kekayaan.html")

def layanan_huller(request):
	return render(request, "front-end/layanan/huller.html")

def layanan_imb_umum(request):
	return render(request, "front-end/layanan/imb_umum.html")

def layanan_imb_reklame(request):
	return render(request, "front-end/layanan/imb_reklame.html")

def layanan_imb_perumahan(request):
	return render(request, "front-end/layanan/imb_perumahan.html")

def cari_pengajuan(request):
	return render(request, "front-end/cari_pengajuan.html")

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