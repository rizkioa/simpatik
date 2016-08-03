from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin import site
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

@login_required
def admin_home(request):
	if not request.user.is_admin:
		return HttpResponseRedirect(reverse('useradmin:index'))
	return site.index(request)

@login_required
def user_home(request):
	if request.user.is_admin:
		return HttpResponseRedirect(reverse('admin:index'))
	return site.index(request)

def frontindex(request):
	return render(
		request, "front-end/home.html"	
	)

def awal(request):
	return render(request, "front-end/index-awal.html")

def tentang(request):
	return render(request, "front-end/tentang.html")

def monitoring_berkas(request):
	return render(request, "front-end/Monitoring/Monitoringberkas.html")

def register(request):
	return render(request, "front-end/register.html")

def syarat(request):
	return render(request, "front-end/persyaratan/syarat.html")

def izingangguan(request):
	return render(request, "front-end/persyaratan/gangguan.html")

def jasa_titipan(request):
	return render(request, "front-end/persyaratan/jasa_titipan.html")

def lingkungan(request):
	return render(request, "front-end/persyaratan/lingkungan.html")

def lokasi(request):
	return render(request, "front-end/persyaratan/lokasi.html")

def mendirikan_bangunan(request):
	return render(request, "front-end/persyaratan/mendirikan_bangunan.html")

def mendirikan_tower(request):
	return render(request, "front-end/persyaratan/mendirikan_tower.html")
	
def konstruksi_ruang_sungai(request):
	return render(request, "front-end/persyaratan/konstruksi_ruang_sungai.html")

def mengubah_aliran_sungai(request):
	return render(request, "front-end/persyaratan/mengubah_aliran_sungai.html")

def tiang_pancang(request):
	return render(request, "front-end/persyaratan/tiang_pancang.html")

def pemanfaatan_bantaran_sungai(request):
	return render(request, "front-end/persyaratan/pemanfaatan_bantaran_sungai.html")

def pematangan_lahan(request):
	return render(request, "front-end/persyaratan/pematangan_lahan.html")

def pembuangan_limbah(request):
	return render(request, "front-end/persyaratan/pembuangan_limbah.html")

def pembuatan_jalan(request):
	return render(request, "front-end/persyaratan/pembuatan_jalan.html")

def jalan_masuk_pekarangan(request):
	return render(request, "front-end/persyaratan/jalan_masuk_pekarangan.html")

def tempat_parkir(request):
	return render(request, "front-end/persyaratan/tempatparkir.html")

def ruang_milik_jalan(request):
	return render(request, "front-end/persyaratan/ruangmilikjalan.html")

def penutupan_jalan(request):
	return render(request, "front-end/persyaratan/penutupantrotoar.html")

def reklame(request):
	return render(request, "front-end/persyaratan/reklame.html")

def trayek(request):
	return render(request, "front-end/persyaratan/trayek.html")

def usaha_angkutan(request):
	return render(request, "front-end/persyaratan/usaha_angkutan.html")

def usaha_industri(request):
	return render(request, "front-end/persyaratan/usaha_industri.html")

def usaha_jasa_konstruksi(request):
	return render(request, "front-end/persyaratan/usaha_jasakonstruksi.html")

def usaha_jasa_konstruksi(request):
	return render(request, "front-end/persyaratan/usaha_jasakonstruksi.html")

def usaha_perdagangan(request):
	return render(request, "front-end/persyaratan/usaha_perdagangan.html")

def daftar_gudang(request):
	return render(request, "front-end/persyaratan/daftar_gudang.html")

def daftar_industri(request):
	return render(request, "front-end/persyaratan/daftar_industri.html")

def daftar_perusahaan(request):
	return render(request, "front-end/persyaratan/daftar_perusahaan.html")

def daftar_usaha_kecil(request):
	return render(request, "front-end/persyaratan/daftar_usahakecil.html")

def daftar_usaha_mikro(request):
	return render(request, "front-end/persyaratan/daftar_usahamikro.html")
