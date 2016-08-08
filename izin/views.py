from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin import site
from functools import wraps
from django.views.decorators.cache import cache_page
from django.utils.decorators import available_attrs

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

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def tentang(request):
	return render(request, "front-end/tentang.html")

#@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan(request):
	return render(request, "front-end/layanan.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_siup(request):
	return render(request, "front-end/layanan/siup.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_ho(request):
	return render(request, "front-end/layanan/ho.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_sipa_sumur_bor(request):
	return render(request, "front-end/layanan/sipa_sumur_bor.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_sipa_sumur_pasak(request):
	return render(request, "front-end/layanan/sipa_sumur_pasak.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_pertambangan(request):
	return render(request, "front-end/layanan/pertambangan.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_tdp_pt(request):
	return render(request, "front-end/layanan/tdp_pt.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_tdp_cv(request):
	return render(request, "front-end/layanan/tdp_cv.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_tdp_firma(request):
	return render(request, "front-end/layanan/tdp_firma.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_tdp_perorangan(request):
	return render(request, "front-end/layanan/tdp_perorangan.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_tdp_koperasi(request):
	return render(request, "front-end/layanan/tdp_koperasi.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_tdp_bul(request):
	return render(request, "front-end/layanan/tdp_bul.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_reklame(request):
	return render(request, "front-end/layanan/reklame.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_kekayaan(request):
	return render(request, "front-end/layanan/kekayaan.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_huller(request):
	return render(request, "front-end/layanan/huller.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_imb_umum(request):
	return render(request, "front-end/layanan/imb_umum.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_imb_reklame(request):
	return render(request, "front-end/layanan/imb_reklame.html")

@passes_test_cache(lambda request: request.user.is_anonymous(), 3600)
def layanan_imb_perumahan(request):
	return render(request, "front-end/layanan/imb_perumahan.html")

def monitoring(request):
	return render(request, "front-end/monitoring.html")