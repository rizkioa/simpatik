import json, decimal, time, base64, pdfkit, datetime, os
from decimal import *
from functools import wraps
from datetime import datetime

from django.http import Http404
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.contrib.admin import site
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template import RequestContext, loader
from django.utils.decorators import method_decorator, available_attrs
from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.safestring import mark_safe

from accounts.models import IdentitasPribadi, NomorIdentitasPengguna
from izin.models import JenisIzin, Syarat, KelompokJenisIzin, JenisPermohonanIzin, PengajuanIzin, DetilSIUP, DetilReklame, DetilTDP, IzinLain, Riwayat, PaketPekerjaan, DetilIUJK, AnggotaBadanUsaha, JenisKoperasi, BentukKoperasi, DetilTDUP, BidangUsahaPariwisata, KategoriKendaraan, MerkTypeKendaraan, DetilIUA, DetilIzinParkirIsidentil, DataAnggotaParkir, DetilTrayek, DetilReklameIzin, JenisKualifikasi
from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon, JenisReklame, ParameterBangunan, JenisTipeReklame, PengaduanIzin, PesanPengaduan
from perusahaan.models import BentukKegiatanUsaha, JenisPenanamanModal, Kelembagaan, KBLI, JenisLegalitas, Legalitas, JenisBadanUsaha, StatusPerusahaan, BentukKerjasama, JenisPengecer, KedudukanKegiatanUsaha, JenisPerusahaan, JenisKedudukan, DataPimpinan, PemegangSaham, Perusahaan

from izin.utils import formatrupiah,JENIS_IUJK, get_tahun_choices
from accounts.utils import KETERANGAN_PEKERJAAN

from izin.utils import render_to_pdf

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

# def page_404(request):
#     return render(request, "error/404.html")

def frontlogin(request):
	return render(request, "front-end/login.html")

def tentang(request):
	return render(request, "front-end/tentang.html")

def layanan(request):
	return render(request, "front-end/layanan.html")

def call_center(request):
	return render(request, "front-end/call_center.html")

def cari_pengajuan(request):
	return render(request, "front-end/cari_pengajuan.html")

def pengaduan_izin(request, extra_context={}):
	import locale, datetime
	locale.setlocale(locale.LC_ALL,'id_ID.UTF-8')
	from master.models import PengaduanIzin, PesanPengaduan
	kelompokjenisizin_list = KelompokJenisIzin.objects.filter(aktif=True)
	extra_context.update({
		'kelompokjenisizin' : kelompokjenisizin_list
		})
	no_ktp_pengaduan = request.COOKIES.get('no_ktp_pengaduan')
	if no_ktp_pengaduan:
		pengaduan_izin_obj = PengaduanIzin.objects.filter(no_ktp=no_ktp_pengaduan)
		if pengaduan_izin_obj :
			pengaduan_izin_obj = pengaduan_izin_obj.last()
			if pengaduan_izin_obj:
				pesan_pengaduan_list = pengaduan_izin_obj.pesanpengaduan_set.all()
				extra_context.update({
					'pengaduan_izin_obj': pengaduan_izin_obj,
					'pesan_pengaduan_list': pesan_pengaduan_list
					})
				if request.POST:
					if request.POST.get('pesan') is not None:
						pesan_pengaduan_obj = PesanPengaduan(
							pengaduan_izin_id = pengaduan_izin_obj.id,
							pesan = request.POST.get('pesan'),
							)
						pesan_pengaduan_obj.save()
				if request.GET:
					if request.GET.get('tutup-pengaduan'):
						if request.GET.get('tutup-pengaduan') == "true":
							extra_context.update({
							'pengaduan_izin_obj': None,})
							response = HttpResponseRedirect('/pengaduan-izin/')
							response.delete_cookie('no_ktp_pengaduan')
							return response
			else:
				extra_context.update({
					'pengaduan_izin_obj': None,})
				response = HttpResponseRedirect('/pengaduan-izin/')
				response.delete_cookie('no_ktp_pengaduan')
				return response
		else:
			extra_context.update({
				'pengaduan_izin_obj': None,})
			response = HttpResponseRedirect('/pengaduan-izin/')
			response.delete_cookie('no_ktp_pengaduan')
			return response
	return render(request, "front-end/pengaduan_izin.html", extra_context)

def cek_pengaduan_izin(request):
	return render(request, "front-end/cek_pengaduan.html")

def formulir_siup(request, extra_context={}):
	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) # Untuk SIUP
		negara = Negara.objects.all()
		provinsi = Provinsi.objects.all()
		kabupaten = Kabupaten.objects.all()
		kecamatan = Kecamatan.objects.all()
		desa = Desa.objects.all()
		jenis_pemohon = JenisPemohon.objects.all()
		jenis_legalitas_list = JenisLegalitas.objects.all()
		bentuk_kegiatan_usaha_list = BentukKegiatanUsaha.objects.all()
		jenis_penanaman_modal_list = JenisPenanamanModal.objects.all()
		kelembagaan_list = Kelembagaan.objects.all()
		kbli_list = KBLI.objects.all()
		kbli_list = kbli_list.extra(where=["CHAR_LENGTH(kode_kbli) = 5"])

		extra_context.update({
			'jenispermohonanizin_list': jenispermohonanizin_list,
			'negara': negara,
			'provinsi': provinsi,
			'kabupaten': kabupaten,
			'kecamatan': kecamatan,
			'desa': desa,
			'kecamatan_perusahaan': kecamatan.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35'),
			'jenis_pemohon': jenis_pemohon,
			'bentuk_kegiatan_usaha_list': bentuk_kegiatan_usaha_list,
			'jenis_penanaman_modal_list': jenis_penanaman_modal_list,
			'kelembagaan_list': kelembagaan_list,
			'kbli_list': kbli_list,
			'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,


			})

		# +++++++++++++++++++ jika cookie pengajuan ada dan di refrash +++++++++++++++++
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan'] != "":
				try:
					pengajuan_ = DetilSIUP.objects.get(id=request.COOKIES['id_pengajuan'])
					alamat_ = ""
					alamat_perusahaan_ = ""
					if pengajuan_.pemohon:
						if pengajuan_.pemohon.desa:
							alamat_ = str(pengajuan_.pemohon.alamat)+", Ds. "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
							extra_context.update({ 'alamat_pemohon_konfirmasi': alamat_ })
						extra_context.update({ 'pemohon_konfirmasi': pengajuan_.pemohon })
						ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
						extra_context.update({ 'ktp': ktp_ })
						paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
						extra_context.update({ 'paspor': paspor_ })
					if pengajuan_.perusahaan:
						if pengajuan_.perusahaan.desa:
							alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Ds. "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
							extra_context.update({ 'alamat_perusahaan_konfirmasi': alamat_perusahaan_ })
						extra_context.update({ 'perusahaan_konfirmasi': pengajuan_.perusahaan })
						legalitas_pendirian = pengajuan_.perusahaan.legalitas_set.filter(~Q(jenis_legalitas__id=2)).last()
						legalitas_perubahan= pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas__id=2).last()

						extra_context.update({ 'legalitas_pendirian': legalitas_pendirian })
						extra_context.update({ 'legalitas_perubahan': legalitas_perubahan })
					
					extra_context.update({ 'no_pengajuan_konfirmasi': pengajuan_.no_pengajuan })
					extra_context.update({ 'jenis_permohonan_konfirmasi': pengajuan_.jenis_permohonan })
					extra_context.update({ 'kelompok_jenis_izin_konfirmasi': pengajuan_.kelompok_jenis_izin })
					if pengajuan_.bentuk_kegiatan_usaha:
						extra_context.update({ 'bentuk_kegiatan_usaha_konfirmasi': pengajuan_.bentuk_kegiatan_usaha.kegiatan_usaha })
					if pengajuan_.jenis_penanaman_modal:
						extra_context.update({ 'status_penanaman_modal_konfirmasi': pengajuan_.jenis_penanaman_modal.jenis_penanaman_modal })
					if pengajuan_.kekayaan_bersih:
						extra_context.update({ 'kekayaan_bersih_konfirmasi': "Rp "+str(pengajuan_.kekayaan_bersih) })
					if pengajuan_.total_nilai_saham:
						extra_context.update({ 'total_nilai_saham_konfirmasi': "Rp "+str(pengajuan_.total_nilai_saham) })
					if pengajuan_.presentase_saham_nasional:
						extra_context.update({ 'presentase_saham_nasional_konfirmasi': str(pengajuan_.presentase_saham_nasional)+" %" })
					if pengajuan_.presentase_saham_asing:
						extra_context.update({ 'presentase_saham_asing_konfirmasi': str(pengajuan_.presentase_saham_asing)+" %" })
					if pengajuan_.kelembagaan:
						extra_context.update({ 'kelembagaan_konfirmasi': pengajuan_.kelembagaan.all })
					extra_context.update({ 'pengajuan_': pengajuan_ })
					
					template = loader.get_template("front-end/formulir/siup.html")
					ec = RequestContext(request, extra_context)
					response = HttpResponse(template.render(ec))

					if pengajuan_.pemohon:
						response.set_cookie(key='id_pemohon', value=pengajuan_.pemohon.id)
					if pengajuan_.perusahaan:
						response.set_cookie(key='id_perusahaan', value=pengajuan_.perusahaan.id)
						if legalitas_pendirian:
							response.set_cookie(key='id_legalitas', value=legalitas_pendirian.id)
						if legalitas_perubahan:
							response.set_cookie(key='id_legalitas_perubahan', value=legalitas_perubahan.id)
					if ktp_:
						response.set_cookie(key='nomor_ktp', value=ktp_)
				except ObjectDoesNotExist:
					template = loader.get_template("front-end/formulir/siup.html")
					ec = RequestContext(request, extra_context)
					response = HttpResponse(template.render(ec))
					response.set_cookie(key='id_pengajuan', value='0')
		else:
			template = loader.get_template("front-end/formulir/siup.html")
			ec = RequestContext(request, extra_context)
			response = HttpResponse(template.render(ec))
			response.set_cookie(key='id_pengajuan', value='0')
		return response
	else:
		return HttpResponseRedirect(reverse('layanan'))

def formulir_huller(request, extra_context={}):
	negara = Negara.objects.all()
	kecamatan = Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35')
	jenis_pemohon = JenisPemohon.objects.all()

	extra_context.update({
		'kecamatan': kecamatan,
		'negara': negara,
		'jenis_pemohon': jenis_pemohon,
		'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
		})

	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) 
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/huller.html", extra_context)

def formulir_reklame(request, extra_context={}):
	negara = Negara.objects.all()
	provinsi = Provinsi.objects.all()
	kabupaten = Kabupaten.objects.all()
	kecamatan = Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35')
	desa = Desa.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	reklame_jenis_list = JenisReklame.objects.all()
	tipe_reklame_list = JenisTipeReklame.objects.all()

	extra_context.update({
		'jenis_pemohon': jenis_pemohon,
		'reklame_jenis_list': reklame_jenis_list,
		'tipe_reklame_list': tipe_reklame_list,
		'desa': desa,
		'kecamatan': kecamatan,
		'kabupaten': kabupaten,
		'provinsi': provinsi,
		'negara': negara,
		'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
		})

	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != "":
			try:
				pengajuan_ = DetilReklame.objects.get(id=request.COOKIES['id_pengajuan'])
				alamat_ = ""
				alamat_perusahaan_ = ""
				if pengajuan_.pemohon:
					if pengajuan_.pemohon.desa:
						alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
						extra_context.update({ 'alamat_pemohon_konfirmasi': alamat_ })
					extra_context.update({ 'pemohon_konfirmasi': pengajuan_.pemohon })
					extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
					ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
					extra_context.update({ 'ktp': ktp_ })
					paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
					extra_context.update({ 'paspor': paspor_ })
					extra_context.update({'cookie_file_ktp': ktp_.berkas })
				if pengajuan_.perusahaan:
					if pengajuan_.perusahaan.desa:
						alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
						extra_context.update({ 'alamat_perusahaan_konfirmasi': alamat_perusahaan_ })
					extra_context.update({ 'perusahaan_konfirmasi': pengajuan_.perusahaan })
				detail_izin_reklame_list = DetilReklameIzin.objects.filter(detil_reklame=request.COOKIES['id_pengajuan'])
				extra_context.update({ 'detail_izin_reklame_list': detail_izin_reklame_list })
				extra_context.update({ 'no_pengajuan_konfirmasi': pengajuan_.no_pengajuan })
				extra_context.update({ 'jenis_permohonan_konfirmasi': pengajuan_.jenis_permohonan })
				extra_context.update({ 'pengajuan_': pengajuan_ })
				panjang = str(int(pengajuan_.panjang))
				lebar = str(int(pengajuan_.lebar))
				sisi = str(int(pengajuan_.sisi))
				ukuran_ = panjang+"x"+lebar+"x"+sisi
				extra_context.update({ 'panjang': panjang })
				extra_context.update({ 'lebar': lebar })
				extra_context.update({ 'sisi': sisi })
				extra_context.update({ 'ukuran': ukuran_ })
			except ObjectDoesNotExist:
				pass

	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) 
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/reklame.html", extra_context)


def formulir_tdp_pt(request, extra_context={}):
	negara = Negara.objects.all()
	provinsi = Provinsi.objects.all()
	kecamatan = Kecamatan.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	jenis_badan_usaha = JenisBadanUsaha.objects.all()
	status_perusahaan = StatusPerusahaan.objects.all()
	jenis_penanaman_modal = JenisPenanamanModal.objects.all()
	bentuk_kerjasama = BentukKerjasama.objects.all()
	jenis_pengecer = JenisPengecer.objects.all()
	kedudukan_kegiatan_usaha = KedudukanKegiatanUsaha.objects.all()
	kelompok_jenis_izin = KelompokJenisIzin.objects.all()
	jenis_kedudukan = JenisKedudukan.objects.all()
	bentuk_kegiatan_usaha_list = BentukKegiatanUsaha.objects.all()
	jenis_perusahaan = JenisPerusahaan.objects.all()

	extra_context.update({
		'negara': negara,
		'provinsi': provinsi,
		'kecamatan': kecamatan,
		'jenis_pemohon': jenis_pemohon,
		'jenis_badan_usaha': jenis_badan_usaha,
		'status_perusahaan': status_perusahaan,
		'jenis_penanaman_modal': jenis_penanaman_modal,
		'bentuk_kerjasama': bentuk_kerjasama,
		'jenis_pengecer': jenis_pengecer,
		'kedudukan_kegiatan_usaha': kedudukan_kegiatan_usaha,
		'kelompok_jenis_izin': kelompok_jenis_izin,
		'jenis_kedudukan': jenis_kedudukan,
		'kegiatan_usaha': bentuk_kegiatan_usaha_list,
		'jenis_perusahaan': jenis_perusahaan,
		'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,

		})
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0':
			try:
				pengajuan_ = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
				extra_context.update({'pengajuan_': pengajuan_})
				extra_context.update({'pengajuan_id': pengajuan_.id})
				if pengajuan_.pemohon:
					ktp_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
					extra_context.update({ 'ktp': ktp_ })
					paspor_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
					extra_context.update({ 'paspor': paspor_ })
				# if pengajuan_.perusahaan:
				#     perusahaan_cabang = Perusahaan.objects.filter(id=)
			except ObjectDoesNotExist:
				extra_context.update({'pengajuan_id': '0'})

	
	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/tdp_pt.html", extra_context)


def formulir_tdp_cv(request, extra_context={}):
	negara = Negara.objects.all()
	provinsi = Provinsi.objects.all()
	kabupaten = Kabupaten.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	bentuk_kerjasama = BentukKerjasama.objects.all()
	status_perusahaan = StatusPerusahaan.objects.all()
	jenis_penanaman_modal = JenisPenanamanModal.objects.all()
	kecamatan = Kecamatan.objects.all()
	jenis_kedudukan = JenisKedudukan.objects.all()
	jenis_pengecer = JenisPengecer.objects.all()
	jenis_perusahaan = JenisPerusahaan.objects.all()
	kedudukan_kegiatan_usaha = KedudukanKegiatanUsaha.objects.all()
	kelompok_jenis_izin = KelompokJenisIzin.objects.all()
	bentuk_kegiatan_usaha_list = BentukKegiatanUsaha.objects.all()
	extra_context.update({
		'negara': negara,
		'jenis_pemohon':jenis_pemohon, 
		'bentuk_kerjasama':bentuk_kerjasama, 
		'status_perusahaan':status_perusahaan, 
		'jenis_penanaman_modal':jenis_penanaman_modal, 
		'jenis_kedudukan':jenis_kedudukan, 
		'jenis_pengecer':jenis_pengecer, 
		'jenis_perusahaan':jenis_perusahaan, 
		'kedudukan_kegiatan_usaha':kedudukan_kegiatan_usaha, 
		'kelompok_jenis_izin':kelompok_jenis_izin, 
		'kegiatan_usaha':bentuk_kegiatan_usaha_list,
		'keterangan_pekerjaan': KETERANGAN_PEKERJAAN
		})
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0':
			try:
				pengajuan_ = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
				extra_context.update({'pengajuan_': pengajuan_})
				extra_context.update({'pengajuan_id': pengajuan_.id})
				if pengajuan_.pemohon:
					ktp_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
					extra_context.update({ 'ktp': ktp_ })
					paspor_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
					if paspor_:
						paspor_ = paspor_
					else:
						paspor_ = '0'
					extra_context.update({ 'paspor': paspor_ })
				# if pengajuan_.perusahaan:
				#     perusahaan_cabang = Perusahaan.objects.filter(id=)
			except ObjectDoesNotExist:
				extra_context.update({'pengajuan_id': '0'})

	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/tdp_cv.html", extra_context)

def formulir_tdp_firma(request, extra_context={}):
	negara = Negara.objects.all()
	provinsi = Provinsi.objects.all()
	kabupaten = Kabupaten.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	bentuk_kerjasama = BentukKerjasama.objects.all()
	status_perusahaan = StatusPerusahaan.objects.all()
	jenis_penanaman_modal = JenisPenanamanModal.objects.all()
	kecamatan = Kecamatan.objects.all()
	jenis_kedudukan = JenisKedudukan.objects.all()
	jenis_pengecer = JenisPengecer.objects.all()
	jenis_perusahaan = JenisPerusahaan.objects.all()
	kedudukan_kegiatan_usaha = KedudukanKegiatanUsaha.objects.all()
	kelompok_jenis_izin = KelompokJenisIzin.objects.all()
	bentuk_kegiatan_usaha_list = BentukKegiatanUsaha.objects.all()
	extra_context.update({'keterangan_pekerjaan': KETERANGAN_PEKERJAAN })
	extra_context.update({'negara': negara, 'jenis_pemohon':jenis_pemohon, 'bentuk_kerjasama':bentuk_kerjasama, 'status_perusahaan':status_perusahaan, 'jenis_penanaman_modal':jenis_penanaman_modal, 'jenis_kedudukan':jenis_kedudukan, 'jenis_pengecer':jenis_pengecer, 'jenis_perusahaan':jenis_perusahaan, 'kedudukan_kegiatan_usaha':kedudukan_kegiatan_usaha, 'kelompok_jenis_izin':kelompok_jenis_izin, 'kegiatan_usaha':bentuk_kegiatan_usaha_list})
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0':
			try:
				pengajuan_ = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
				extra_context.update({'pengajuan_': pengajuan_})
				extra_context.update({'pengajuan_id': pengajuan_.id})
				if pengajuan_.pemohon:
					ktp_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
					extra_context.update({ 'ktp': ktp_ })
					paspor_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
					if paspor_:
						paspor_ = paspor_
					else:
						paspor_ = '0'
					extra_context.update({ 'paspor': paspor_ })
				# if pengajuan_.perusahaan:
				#     perusahaan_cabang = Perusahaan.objects.filter(id=)
			except ObjectDoesNotExist:
				extra_context.update({'pengajuan_id': '0'})

	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/tdp_firma.html", extra_context)

def formulir_iujk(request, extra_context={}):

	extra_context.update({
		'title': 'Formulir IUJK',
		'negara': Negara.objects.all(),
		'jenis_pemohon': JenisPemohon.objects.all(),
		'bentuk_kegiatan_usaha_list': BentukKegiatanUsaha.objects.all(),
		'jenis_penanaman_modal_list': JenisPenanamanModal.objects.all(),
		'kelembagaan_list': Kelembagaan.objects.all(),
		'kbli_list': KBLI.objects.all(),
		'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
		'jenis_legalitas_list': JenisLegalitas.objects.all(),
		'jenis_iujk': JENIS_IUJK,
		'tahun_choices': get_tahun_choices(1945),
		'kecamatan_perusahaan': Kecamatan.objects.filter(kabupaten__kode="06", kabupaten__provinsi__kode="35")

		})
	extra_context.update({'jenis_kualifikasi': JenisKualifikasi.objects.all() })

	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan'] != "":
				# print PaketPekerjaan.objects.filter(detil_iujk__id=request.COOKIES['id_pengajuan'])
				extra_context.update({'paketpekerjaan_list': PaketPekerjaan.objects.filter(detil_iujk__id=request.COOKIES['id_pengajuan'])})

				try:
					pengajuan_ = DetilIUJK.objects.get(id=request.COOKIES['id_pengajuan'])
					
					if pengajuan_.pemohon:
						if pengajuan_.pemohon.desa:
							alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
							extra_context.update({ 'alamat_pemohon_konfirmasi': alamat_ })
						extra_context.update({ 'pemohon_konfirmasi': pengajuan_.pemohon })
						extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
						ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
						extra_context.update({ 'ktp': ktp_ })
						paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
						extra_context.update({ 'paspor': paspor_ })
						extra_context.update({'cookie_file_ktp': ktp_.berkas })

					if pengajuan_.perusahaan:
						if pengajuan_.perusahaan.desa:
							alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
							extra_context.update({ 'alamat_perusahaan_konfirmasi': alamat_perusahaan_ })
						extra_context.update({ 'perusahaan_konfirmasi': pengajuan_.perusahaan })
						legalitas_pendirian = pengajuan_.perusahaan.legalitas_set.filter(~Q(jenis_legalitas__id=2)).last()
						legalitas_perubahan= pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas__id=2).last()

						extra_context.update({ 'legalitas_pendirian': legalitas_pendirian })
						extra_context.update({ 'legalitas_perubahan': legalitas_perubahan })

					extra_context.update({ 'jenis_permohonan_konfirmasi': pengajuan_.jenis_permohonan })
					extra_context.update({'get_jenis_iujk': pengajuan_.jenis_iujk})
					
					anggota_list_deriktur = AnggotaBadanUsaha.objects.filter(detil_iujk__id=request.COOKIES['id_pengajuan'], jenis_anggota_badan='Direktur / Penanggung Jawab Badan Usaha')
					if anggota_list_deriktur.exists():
						extra_context.update({'anggota_list_deriktur': anggota_list_deriktur})

					anggota_list_teknik = AnggotaBadanUsaha.objects.filter(detil_iujk__id=request.COOKIES['id_pengajuan'], jenis_anggota_badan='Penanggung Jawab Teknik Badan Usaha')
					if anggota_list_teknik.exists():
						extra_context.update({'anggota_list_teknik': anggota_list_teknik})

					anggota_list_non = AnggotaBadanUsaha.objects.filter(detil_iujk__id=request.COOKIES['id_pengajuan'], jenis_anggota_badan='Tenaga Non Teknik')
					if anggota_list_non.exists():
						extra_context.update({'anggota_list_non': anggota_list_non})

					extra_context.update({ 'pengajuan_': pengajuan_ })

					template = loader.get_template("front-end/formulir/iujk.html")
					ec = RequestContext(request, extra_context)
					response =  HttpResponse(template.render(ec))

					if legalitas_pendirian:
						response.set_cookie(key='id_legalitas', value=legalitas_pendirian.id)
					if legalitas_perubahan:
						response.set_cookie(key='id_legalitas_perubahan', value=legalitas_perubahan.id)

					# extra_context.update({ 'kelompok_jenis_izin_konfirmasi': pengajuan_.kelompok_jenis_izin })
				except ObjectDoesNotExist:
					template = loader.get_template("front-end/formulir/iujk.html")
					ec = RequestContext(request, extra_context)
					response =  HttpResponse(template.render(ec))
					response.set_cookie(key='id_pengajuan', value='0')
			else:
				template = loader.get_template("front-end/formulir/iujk.html")
				ec = RequestContext(request, extra_context)
				response =  HttpResponse(template.render(ec))
				response.set_cookie(key='id_pengajuan', value='0')
		else:
			template = loader.get_template("front-end/formulir/iujk.html")
			ec = RequestContext(request, extra_context)
			response =  HttpResponse(template.render(ec))
	else:
		messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
		response = HttpResponseRedirect(reverse('layanan_iujk'))

	return response

def formulir_tdp_perorangan(request, extra_context={}):
	negara = Negara.objects.all()
	provinsi = Provinsi.objects.all()
	kabupaten = Kabupaten.objects.all()
	kecamatan = Kecamatan.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	bentuk_kerjasama = BentukKerjasama.objects.all()
	status_perusahaan = StatusPerusahaan.objects.all()
	jenis_penanaman_modal = JenisPenanamanModal.objects.all()
	jenis_kedudukan = JenisKedudukan.objects.all()
	jenis_pengecer = JenisPengecer.objects.all()
	jenis_perusahaan = JenisPerusahaan.objects.all()
	kedudukan_kegiatan_usaha = KedudukanKegiatanUsaha.objects.all()
	kelompok_jenis_izin = KelompokJenisIzin.objects.all()
	bentuk_kegiatan_usaha_list = BentukKegiatanUsaha.objects.all()
	extra_context.update({'keterangan_pekerjaan': KETERANGAN_PEKERJAAN })
	extra_context.update({'jenis_pemohon': jenis_pemohon, 'negara':negara, 'provinsi':provinsi, 'kabupaten':kabupaten, 'kecamatan':kecamatan, 'bentuk_kerjasama':bentuk_kerjasama, 'status_perusahaan':status_perusahaan, 'jenis_penanaman_modal':jenis_penanaman_modal, 'jenis_kedudukan':jenis_kedudukan, 'jenis_pengecer':jenis_pengecer, 'jenis_perusahaan':jenis_perusahaan, 'kedudukan_kegiatan_usaha':kedudukan_kegiatan_usaha, 'kelompok_jenis_izin':kelompok_jenis_izin, 'kegiatan_usaha':bentuk_kegiatan_usaha_list})
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0':
			try:
				pengajuan_ = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
				extra_context.update({'pengajuan_': pengajuan_})
				extra_context.update({'pengajuan_id': pengajuan_.id})
				if pengajuan_.pemohon:
					ktp_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
					extra_context.update({ 'ktp': ktp_ })
					paspor_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
					if paspor_:
						paspor_ = paspor_
					else:
						paspor_ = '0'
					extra_context.update({ 'paspor': paspor_ })
				# if pengajuan_.perusahaan:
				#     perusahaan_cabang = Perusahaan.objects.filter(id=)
			except ObjectDoesNotExist:
				extra_context.update({'pengajuan_id': '0'})

	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/tdp_po.html", extra_context)

def formulir_tdp_koperasi(request, extra_context={}):
	negara = Negara.objects.all()
	provinsi = Provinsi.objects.all()
	kabupaten = Kabupaten.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	bentuk_kerjasama = BentukKerjasama.objects.all()
	status_perusahaan = StatusPerusahaan.objects.all()
	jenis_penanaman_modal = JenisPenanamanModal.objects.all()
	kecamatan = Kecamatan.objects.all()
	jenis_kedudukan = JenisKedudukan.objects.all()
	jenis_pengecer = JenisPengecer.objects.all()
	jenis_perusahaan = JenisPerusahaan.objects.all()
	kedudukan_kegiatan_usaha = KedudukanKegiatanUsaha.objects.all()
	kelompok_jenis_izin = KelompokJenisIzin.objects.all()
	bentuk_kegiatan_usaha_list = BentukKegiatanUsaha.objects.all()
	jenis_koperasi = JenisKoperasi.objects.all()
	bentuk_koperasi = BentukKoperasi.objects.all()
	extra_context.update({'keterangan_pekerjaan': KETERANGAN_PEKERJAAN })
	extra_context.update({'negara': negara, 'jenis_pemohon':jenis_pemohon, 'bentuk_kerjasama':bentuk_kerjasama, 'status_perusahaan':status_perusahaan, 'jenis_penanaman_modal':jenis_penanaman_modal, 'jenis_kedudukan':jenis_kedudukan, 'jenis_pengecer':jenis_pengecer, 'jenis_perusahaan':jenis_perusahaan, 'kedudukan_kegiatan_usaha':kedudukan_kegiatan_usaha, 'kelompok_jenis_izin':kelompok_jenis_izin, 'kegiatan_usaha':bentuk_kegiatan_usaha_list, 'bentuk_koperasi': bentuk_koperasi, 'jenis_koperasi':jenis_koperasi})
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0':
			try:
				pengajuan_ = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
				extra_context.update({'pengajuan_': pengajuan_})
				extra_context.update({'pengajuan_id': pengajuan_.id})
				if pengajuan_.pemohon:
					ktp_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
					extra_context.update({ 'ktp': ktp_ })
					paspor_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
					if paspor_:
						paspor_ = paspor_
					else:
						paspor_ = '0'
					extra_context.update({ 'paspor': paspor_ })
				# if pengajuan_.perusahaan:
				#     perusahaan_cabang = Perusahaan.objects.filter(id=)
			except ObjectDoesNotExist:
				extra_context.update({'pengajuan_id': '0'})

	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/tdp_koperasi.html", extra_context)

def formulir_tdp_bul(request, extra_context={}):
	negara = Negara.objects.all()
	provinsi = Provinsi.objects.all()
	kabupaten = Kabupaten.objects.all()
	kecamatan = Kecamatan.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	bentuk_kerjasama = BentukKerjasama.objects.all()
	status_perusahaan = StatusPerusahaan.objects.all()
	jenis_penanaman_modal = JenisPenanamanModal.objects.all()
	jenis_kedudukan = JenisKedudukan.objects.all()
	jenis_pengecer = JenisPengecer.objects.all()
	jenis_perusahaan = JenisPerusahaan.objects.all()
	kedudukan_kegiatan_usaha = KedudukanKegiatanUsaha.objects.all()
	kelompok_jenis_izin = KelompokJenisIzin.objects.all()
	bentuk_kegiatan_usaha_list = BentukKegiatanUsaha.objects.all()
	extra_context.update({'keterangan_pekerjaan': KETERANGAN_PEKERJAAN })
	extra_context.update({'jenis_pemohon': jenis_pemohon, 'negara':negara, 'provinsi':provinsi, 'kabupaten':kabupaten, 'kecamatan':kecamatan, 'bentuk_kerjasama':bentuk_kerjasama, 'status_perusahaan':status_perusahaan, 'jenis_penanaman_modal':jenis_penanaman_modal, 'jenis_kedudukan':jenis_kedudukan, 'jenis_pengecer':jenis_pengecer, 'jenis_perusahaan':jenis_perusahaan, 'kedudukan_kegiatan_usaha':kedudukan_kegiatan_usaha, 'kelompok_jenis_izin':kelompok_jenis_izin, 'kegiatan_usaha':bentuk_kegiatan_usaha_list})
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0':
			try:
				pengajuan_ = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
				extra_context.update({'pengajuan_': pengajuan_})
				extra_context.update({'pengajuan_id': pengajuan_.id})
				if pengajuan_.pemohon:
					ktp_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
					extra_context.update({ 'ktp': ktp_ })
					paspor_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
					if paspor_:
						paspor_ = paspor_
					else:
						paspor_ = '0'
					extra_context.update({ 'paspor': paspor_ })
				# if pengajuan_.perusahaan:
				#     perusahaan_cabang = Perusahaan.objects.filter(id=)
			except ObjectDoesNotExist:
				extra_context.update({'pengajuan_id': '0'})

	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/tdp_bul.html", extra_context)

def formulir_tdup(request, extra_context={}):
	negara = Negara.objects.all()
	provinsi = Provinsi.objects.all()
	kabupaten = Kabupaten.objects.all()
	kecamatan = Kecamatan.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	bidang_usaha_pariwisata_list = BidangUsahaPariwisata.objects.all()
	extra_context.update({'keterangan_pekerjaan': KETERANGAN_PEKERJAAN })
	extra_context.update({'bidang_usaha_pariwisata': bidang_usaha_pariwisata_list, 'negara':negara, 'provinsi':provinsi, 'kabupaten':kabupaten, 'kecamatan':kecamatan, 'jenis_pemohon':jenis_pemohon})
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0' and request.COOKIES['id_pengajuan'] != '':
			try:
				pengajuan_ = DetilTDUP.objects.get(id=request.COOKIES['id_pengajuan'])
				print pengajuan_
				extra_context.update({'pengajuan_': pengajuan_})
				extra_context.update({'pengajuan_id': pengajuan_.id})
				if pengajuan_.pemohon:
					extra_context.update({ 'pemohon': pengajuan_.pemohon })
					# ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
					ktp_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
					if ktp_:
						extra_context.update({ 'ktp': ktp_ })
					# paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
					paspor_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
					if paspor_:
						paspor_ = paspor_
					else:
						paspor_ = '0'
					extra_context.update({ 'paspor': paspor_ })
			except ObjectDoesNotExist:
				extra_context.update({'pengajuan_id': '0'})
	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/tdup.html", extra_context)

def formulir_izin_usaha_angkutan(request, extra_context={}):
	negara = Negara.objects.all()
	provinsi = Provinsi.objects.all()
	kabupaten = Kabupaten.objects.all()
	kecamatan = Kecamatan.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	katogri_kendaraan_list = KategoriKendaraan.objects.all()
	merk_type_list = MerkTypeKendaraan.objects.all()
	extra_context.update({
		'negara':negara, 
		'provinsi':provinsi, 
		'kabupaten':kabupaten, 
		'kecamatan':kecamatan,
		'kecamatan_perusahaan': kecamatan.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35'),
		'jenis_pemohon':jenis_pemohon,
		'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
		'kategori_kendaraan':katogri_kendaraan_list,
		'merk_type' : merk_type_list,
		'tahun_choices': get_tahun_choices(1945),
		})
	# print str(request.COOKIES['id_pengajuan'])  
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0':
			print request.COOKIES['id_pengajuan']
			try:
				pengajuan_ = DetilIUA.objects.get(id=request.COOKIES['id_pengajuan'])
				extra_context.update({'pengajuan_': pengajuan_})
				extra_context.update({'pengajuan_id': pengajuan_.id})
				if pengajuan_.pemohon:
					ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
					extra_context.update({ 'ktp': ktp_ })
					paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
					extra_context.update({ 'paspor': paspor_ })
				# if pengajuan_.perusahaan:
				#     perusahaan_cabang = Perusahaan.objects.filter(id=)
			except ObjectDoesNotExist:
				extra_context.update({'pengajuan_id': '0'})

	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/izin_usaha_angkutan.html", extra_context)

def formulir_izin_parkir(request, extra_context={}):
	negara = Negara.objects.all()
	provinsi = Provinsi.objects.all()
	kabupaten = Kabupaten.objects.all()
	kecamatan = Kecamatan.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	katogri_kendaraan_list = KategoriKendaraan.objects.all()
	merk_type_list = MerkTypeKendaraan.objects.all()
	extra_context.update({
		'negara':negara, 
		'provinsi':provinsi, 
		'kabupaten':kabupaten, 
		'kecamatan':kecamatan,
		'kecamatan_perusahaan': kecamatan.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35'),
		'jenis_pemohon':jenis_pemohon,
		'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
		'kategori_kendaraan':katogri_kendaraan_list,
		'merk_type' : merk_type_list,
		'tahun_choices': get_tahun_choices(1945),
		})
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0':
			print request.COOKIES['id_pengajuan']
			try:
				pengajuan_ = DetilIzinParkirIsidentil.objects.get(id=request.COOKIES['id_pengajuan'])
				extra_context.update({'pengajuan_': pengajuan_})
				extra_context.update({'pengajuan_id': pengajuan_.id})
				if pengajuan_.pemohon:
					ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
					extra_context.update({ 'ktp': ktp_ })
					paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
					extra_context.update({ 'paspor': paspor_ })
				# if pengajuan_.perusahaan:
				#     perusahaan_cabang = Perusahaan.objects.filter(id=)
			except ObjectDoesNotExist:
				extra_context.update({'pengajuan_id': '0'})
	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/izin_parkir.html", extra_context)

def cetak_izin_parkir(request, id_pengajuan):
	extra_context = {}
	if id_pengajuan:
		pengajuan_ = get_object_or_404(DetilIzinParkirIsidentil, id=id_pengajuan)
		if pengajuan_:
			extra_context.update({'pengajuan': pengajuan_})
	return render(request, "front-end/include/formulir_izin_parkir/cetak.html", extra_context)

def cetak_bukti_pendaftaran_izin_parkir(request, id_pengajuan):
	extra_context = {}
	extra_context.update({'formulir_judul': 'FORMULIR PENDAFTARAN IZIN PARKIR'})
	if id_pengajuan:
		pengajuan_ = get_object_or_404(DetilIzinParkirIsidentil, id=id_pengajuan)
		if pengajuan_:
			data_anggota_list = DataAnggotaParkir.objects.filter(izin_parkir_isidentil_id=pengajuan_.id)
			# rincian_perusahaan_ = RincianPerusahaan.objects.filter(detil_tdp_id=pengajuan_.id).last()
			# id_kelompok_list = KelompokJenisIzin.objects.filter(jenis_izin__kode=25)
			syarat_ = Syarat.objects.filter(jenis_izin__kode="IZINPARKIR")
			extra_context.update({'pengajuan_':pengajuan_, 'data_anggota': data_anggota_list, 'syarat':syarat_})
	return render(request, "front-end/include/formulir_izin_parkir/cetak_bukti_pendaftaran.html", extra_context)

def cetak_tdup(request, id_pengajuan):
	extra_context = {}
	if id_pengajuan:
		pengajuan_ = get_object_or_404(DetilTDUP, id=id_pengajuan)
		if pengajuan_:
			extra_context.update({'pengajuan': pengajuan_})
	return render(request, "front-end/include/formulir_tdup/cetak.html", extra_context)

def cetak_bukti_pendaftaran_tdup(request, id_pengajuan):
	extra_context = {}
	extra_context.update({'formulir_judul': 'FORMULIR PENDAFTARAN PERUSAHAAN TDUP'})
	if id_pengajuan:
		pengajuan_ = get_object_or_404(DetilTDUP, id=id_pengajuan)
		if pengajuan_:
			no_pengajuan = pengajuan_.no_pengajuan
			jenis_izin = pengajuan_.kelompok_jenis_izin.kelompok_jenis_izin
			pemohon_ = pengajuan_.pemohon
			legalitas_ = pengajuan_.perusahaan.legalitas_set.all()
			rincian_sub_jenis_ = pengajuan_.rincian_sub_jenis

			# rincian_perusahaan_ = RincianPerusahaan.objects.filter(detil_tdp_id=pengajuan_.id).last()
			# id_kelompok_list = KelompokJenisIzin.objects.filter(jenis_izin__kode=25)
			syarat_ = Syarat.objects.filter(jenis_izin__jenis_izin__kode="TDUP")
			extra_context.update({'pengajuan_':pengajuan_, 'legalitas':legalitas_, 'rincian': rincian_sub_jenis_, 'syarat':syarat_})
	return render(request, "front-end/include/formulir_tdup/cetak_bukti_pendaftaran.html", extra_context)

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

def cetak_permohonan(request, id_pengajuan_):
	extra_context = {}
	url_ = reverse('formulir_siup')
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(DetilSIUP, id=id_pengajuan_)
		if pengajuan_:
			extra_context.update({ 'pengajuan': pengajuan_ })
			riwayat = Riwayat.objects.filter(pengajuan_izin=pengajuan_)
			if riwayat:
				extra_context.update({ 'riwayat': riwayat })
		template = loader.get_template("front-end/cetak.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

def cetak_permohonan_iujk(request, id_pengajuan_):
	extra_context = {}
	url_ = reverse('formulir_iujk')
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(DetilIUJK, id=id_pengajuan_)
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
			extra_context.update({ 'created_at': pengajuan_.created_at })
			template = loader.get_template("front-end/include/formulir_iujk/cetak.html")
		else:
			response = HttpResponseRedirect(url_)
			return response
	else:
		response = HttpResponseRedirect(url_)
		return response
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))

def cetak_bukti_pendaftaran(request, id_pengajuan_):
	import datetime
	extra_context = {}
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(DetilSIUP, id=id_pengajuan_)

		if pengajuan_:
			syarat = Syarat.objects.filter(jenis_izin__jenis_izin__kode="SIUP")
			extra_context.update({ 'pengajuan': pengajuan_ })
			extra_context.update({ 'syarat': syarat })
		response = render(request, "front-end/cetak_bukti_pendaftaran.html", extra_context)
		# response = render_to_pdf("front-end/cetak_bukti_pendaftaran_baru.html", "Cetak Bukti SIUP", extra_context, request)
	else:
		raise Http404
	return response
	# ec = RequestContext(request, extra_context)
	# return HttpResponse(template.render(ec))

def cetak_ho_baru(request, extra_context={}):
	return render(request, "front-end/include/formulir_ho_baru/cetak.html", extra_context)

def cetak_bukti_pendaftaran_ho_baru(request, extra_context={}):
	syarat = Syarat.objects.filter(jenis_izin__jenis_izin__kode="HO")
	extra_context.update({'syarat': syarat})
	return render(request, "front-end/include/formulir_ho_baru/cetak_bukti_pendaftaran.html", extra_context)

def cetak_reklame(request,id_pengajuan_):
	extra_context = {}
	url_ = reverse('formulir_reklame')
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_)
		if pengajuan_.perusahaan != '':
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.pemohon.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({ 'alamat_pemohon': alamat_ })
				extra_context.update({ 'pemohon': pengajuan_.pemohon })

			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({ 'alamat_perusahaan': alamat_perusahaan_ })
				extra_context.update({ 'perusahaan': pengajuan_.perusahaan })

			extra_context.update({ 'pengajuan': pengajuan_ })
			pengajuan_id = base64.b64encode(str(pengajuan_.id))
			extra_context.update({ 'pengajuan_id': pengajuan_id })

			riwayat = Riwayat.objects.filter(pengajuan_izin=pengajuan_)
			if riwayat:
				extra_context.update({ 'riwayat': riwayat })
			# extra_context.update({ 'jenis_permohonan': pengajuan_.jenis_permohonan })
			# extra_context.update({ 'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin })
			extra_context.update({ 'created_at': pengajuan_.created_at })
			response = loader.get_template("front-end/include/formulir_reklame/cetak.html")
		else:
			response = HttpResponseRedirect(url_)
			return response
	else:
		response = HttpResponseRedirect(url_)
		return response
	template = loader.get_template("front-end/include/formulir_reklame/cetak.html")
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))

def cetak_bukti_pendaftaran_reklame(request, id_pengajuan_):
	extra_context = {}
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_)
		if pengajuan_.perusahaan != '':
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.pemohon.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({ 'alamat_pemohon': alamat_ })
				extra_context.update({ 'pemohon': pengajuan_.pemohon })
				paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
				ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
				extra_context.update({ 'paspor': paspor_ })
				extra_context.update({ 'ktp': ktp_ })
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({ 'alamat_perusahaan': alamat_perusahaan_ })
				extra_context.update({ 'perusahaan': pengajuan_.perusahaan })
				syarat = Syarat.objects.filter(jenis_izin__jenis_izin__id="3")
			letak_ = pengajuan_.letak_pemasangan + ", Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())
			ukuran_ = str(int(pengajuan_.panjang))+"x"+str(int(pengajuan_.lebar))+"x"+str(int(pengajuan_.sisi))
			if pengajuan_.tanggal_mulai:
				awal = pengajuan_.tanggal_mulai
			else:
				awal = 0
			if pengajuan_.tanggal_akhir:
				akhir = pengajuan_.tanggal_akhir
			else:
				akhir = 0
			
			selisih = akhir-awal
			extra_context.update({'letak_pemasangan': letak_})
			extra_context.update({'selisih': selisih.days})
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

	template = loader.get_template("front-end/include/formulir_reklame/cetak_bukti_pendaftaran.html")
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))

def cetak_kekayaan(request, extra_context={}):
	return render(request, "front-end/include/formulir_kekayaan/cetak.html", extra_context)

def cetak_bukti_pendaftaran_kekayaan(request, extra_context={}):
	syarat = Syarat.objects.filter(jenis_izin__jenis_izin__id="5") 
	extra_context.update({'syarat': syarat})
	return render(request, "front-end/include/formulir_kekayaan/cetak_bukti_pendaftaran.html", extra_context)

def cetak_imb_umum(request, extra_context={}):
	return render(request, "front-end/include/imb_umum/cetak.html", extra_context)

def cetak_bukti_pendaftaran_imb_umum(request, extra_context={}):
	syarat = Syarat.objects.filter(jenis_izin__jenis_izin__kode="IMB") 
	extra_context.update({'syarat': syarat})
	return render(request, "front-end/include/imb_umum/cetak_bukti_pendaftaran.html", extra_context)

def cetak_imb_perumahan(request, extra_context={}):
	return render(request, "front-end/include/formulir_imb_perumahan/cetak.html", extra_context)

def cetak_bukti_pendaftaran_imb_perumahan(request, extra_context={}):
	syarat = Syarat.objects.filter(jenis_izin__jenis_izin__kode="IMB") 
	extra_context.update({'syarat': syarat})
	return render(request, "front-end/include/formulir_imb_perumahan/cetak_bukti_pendaftaran.html", extra_context)

def cetak_tdp_pt(request, id_pengajuan_):
	extra_context = {}
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_)
		extra_context.update({'pengajuan': pengajuan_})
	return render(request, "front-end/include/formulir_tdp_pt/cetak.html", extra_context)

def cetak_bukti_pendaftaran_tdp_pt(request, id_pengajuan_):
	extra_context = {}
	extra_context.update({'formulir_judul': 'FORMULIR PENDAFTARAN PERUSAHAAN TDP PERSEROAN TERBATAS (PT)'})
	if id_pengajuan_:
		# pengajuan_ = DetilTDP.objects.get(id=id_pengajuan_)
		pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_)
		if pengajuan_:
			perusahaan_ = pengajuan_.perusahaan
			legalitas_ = pengajuan_.perusahaan.legalitas_set.all()
			# rincian_perusahaan_ = RincianPerusahaan.objects.filter(detil_tdp_id=pengajuan_.id).last()
			izin_lain_ = IzinLain.objects.filter(pengajuan_izin_id=pengajuan_.id)
			data_pimpinan_ = DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id)
			pemegang_saham_ = PemegangSaham.objects.filter(pengajuan_izin_id=pengajuan_.id)
			perusahaan_cabang_ = Perusahaan.objects.filter(perusahaan_induk_id=pengajuan_.perusahaan.id)
			# id_kelompok_list = KelompokJenisIzin.objects.filter(jenis_izin__kode=25)
			wni = 0
			if pengajuan_.jumlah_karyawan_wni:
				wni = pengajuan_.jumlah_karyawan_wni
			wna = 0
			if pengajuan_.jumlah_karyawan_wna:
				wna = pengajuan_.jumlah_karyawan_wna
			total_karyawan = wni+wna
			syarat_ = Syarat.objects.filter(jenis_izin__kode="TDP-PT")
			jumlah_dirut = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=1))
			jumlah_direktur = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=2))
			jumlah_komisaris = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=3))
			extra_context.update({'pengajuan_':pengajuan_, 'legalitas':legalitas_, 'izin_lain':izin_lain_, 'data_pimpinan':data_pimpinan_, 'pemegang_saham':pemegang_saham_, 'perusahaan_cabang':perusahaan_cabang_, 'syarat':syarat_, 'total_karyawan':total_karyawan, 'jumlah_dirut':jumlah_dirut, 'jumlah_direktur':jumlah_direktur, 'jumlah_komisaris':jumlah_komisaris})
	return render(request, "front-end/include/formulir_tdp_pt/cetak_bukti_pendaftaran.html", extra_context)

def cetak_tdp_cv(request, id_pengajuan_):
	extra_context = {}
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_)
		perusahaan_ = pengajuan_.perusahaan
		extra_context.update({'pengajuan': pengajuan_})
	return render(request, "front-end/include/formulir_tdp_cv/cetak.html", extra_context)

def cetak_bukti_pendaftaran_tdp_cv(request, id_pengajuan_):
	extra_context = {}
	extra_context.update({'formulir_judul': 'FORMULIR PENDAFTARAN PERUSAHAAN TDP PERSEKUTUAN KOMANDITER (CV)'})
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_)
		if pengajuan_:
			legalitas_ = pengajuan_.perusahaan.legalitas_set.all()
			# rincian_perusahaan_ = RincianPerusahaan.objects.filter(detil_tdp_id=pengajuan_.id).last()
			izin_lain_ = IzinLain.objects.filter(pengajuan_izin_id=pengajuan_.id)
			data_pimpinan_ = DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id)
			pemegang_saham_ = PemegangSaham.objects.filter(pengajuan_izin_id=pengajuan_.id)
			perusahaan_cabang_ = Perusahaan.objects.filter(perusahaan_induk_id=pengajuan_.perusahaan.id)
			# id_kelompok_list = KelompokJenisIzin.objects.filter(jenis_izin__kode=25)
			syarat_ = Syarat.objects.filter(jenis_izin__kode="TDP-CV")
			wni = 0
			if pengajuan_.jumlah_karyawan_wni:
				wni = pengajuan_.jumlah_karyawan_wni
			wna = 0
			if pengajuan_.jumlah_karyawan_wna:
				wna = pengajuan_.jumlah_karyawan_wna
			total_karyawan = wni+wna
			jumlah_dirut = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=1))
			jumlah_direktur = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=2))
			jumlah_komisaris = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=3))
			extra_context.update({'pengajuan_':pengajuan_, 'legalitas':legalitas_, 'izin_lain':izin_lain_, 'data_pimpinan':data_pimpinan_, 'pemegang_saham':pemegang_saham_, 'perusahaan_cabang':perusahaan_cabang_, 'syarat':syarat_, 'total_karyawan':total_karyawan, 'jumlah_dirut':jumlah_dirut, 'jumlah_direktur':jumlah_direktur, 'jumlah_komisaris':jumlah_komisaris})
	return render(request, "front-end/include/formulir_tdp_pt/cetak_bukti_pendaftaran.html", extra_context)

def cetak_tdp_firma(request, id_pengajuan_):
	extra_context = {}
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_)
		perusahaan_ = pengajuan_.perusahaan
		extra_context.update({'pengajuan': pengajuan_})
	return render(request, "front-end/include/formulir_tdp_firma/cetak.html", extra_context)

def cetak_bukti_pendaftaran_tdp_firma(request, id_pengajuan_):
	extra_context = {}
	extra_context.update({'formulir_judul': 'FORMULIR PENDAFTARAN PERUSAHAAN TDP FIRMA'})
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_)
		if pengajuan_:
			legalitas_ = pengajuan_.perusahaan.legalitas_set.all()
			# rincian_perusahaan_ = RincianPerusahaan.objects.filter(detil_tdp_id=pengajuan_.id).last()
			izin_lain_ = IzinLain.objects.filter(pengajuan_izin_id=pengajuan_.id)
			data_pimpinan_ = DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id)
			pemegang_saham_ = PemegangSaham.objects.filter(pengajuan_izin_id=pengajuan_.id)
			perusahaan_cabang_ = Perusahaan.objects.filter(perusahaan_induk_id=pengajuan_.perusahaan.id)
			# id_kelompok_list = KelompokJenisIzin.objects.filter(jenis_izin__kode=25)
			syarat_ = Syarat.objects.filter(jenis_izin__kode="TDP-FIRMA")
			wni = 0
			if pengajuan_.jumlah_karyawan_wni:
				wni = pengajuan_.jumlah_karyawan_wni
			wna = 0
			if pengajuan_.jumlah_karyawan_wna:
				wna = pengajuan_.jumlah_karyawan_wna
			total_karyawan = wni+wna
			jumlah_dirut = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=1))
			jumlah_direktur = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=2))
			jumlah_komisaris = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=3))
			extra_context.update({'pengajuan_':pengajuan_, 'legalitas':legalitas_, 'izin_lain':izin_lain_, 'data_pimpinan':data_pimpinan_, 'pemegang_saham':pemegang_saham_, 'perusahaan_cabang':perusahaan_cabang_, 'syarat':syarat_, 'total_karyawan':total_karyawan, 'jumlah_dirut':jumlah_dirut, 'jumlah_direktur':jumlah_direktur, 'jumlah_komisaris':jumlah_komisaris})
	return render(request, "front-end/include/formulir_tdp_pt/cetak_bukti_pendaftaran.html", extra_context)

def cetak_tdp_po(request, id_pengajuan_):
	extra_context = {}
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_)
		perusahaan_ = pengajuan_.perusahaan
		extra_context.update({'pengajuan': pengajuan_})
	return render(request, "front-end/include/formulir_tdp_po/cetak.html", extra_context)

def cetak_bukti_pendaftaran_tdp_po(request, id_pengajuan_):
	extra_context = {}
	extra_context.update({'formulir_judul': 'FORMULIR PENDAFTARAN PERUSAHAAN TDP PERORANGAN (PO)'})
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_)
		if pengajuan_:
			legalitas_ = pengajuan_.perusahaan.legalitas_set.all()
			# rincian_perusahaan_ = RincianPerusahaan.objects.filter(detil_tdp_id=pengajuan_.id).last()
			izin_lain_ = IzinLain.objects.filter(pengajuan_izin_id=pengajuan_.id)
			data_pimpinan_ = DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id)
			pemegang_saham_ = PemegangSaham.objects.filter(pengajuan_izin_id=pengajuan_.id)
			perusahaan_cabang_ = Perusahaan.objects.filter(perusahaan_induk_id=pengajuan_.perusahaan.id)
			# id_kelompok_list = KelompokJenisIzin.objects.filter(jenis_izin__kode=25)
			syarat_ = Syarat.objects.filter(jenis_izin__kode="TDP-PERORANGAN")
			wni = 0
			if pengajuan_.jumlah_karyawan_wni:
				wni = pengajuan_.jumlah_karyawan_wni
			wna = 0
			if pengajuan_.jumlah_karyawan_wna:
				wna = pengajuan_.jumlah_karyawan_wna
			total_karyawan = wni+wna
			jumlah_dirut = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=1))
			jumlah_direktur = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=2))
			jumlah_komisaris = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=3))
			extra_context.update({'pengajuan_':pengajuan_, 'legalitas':legalitas_, 'izin_lain':izin_lain_, 'data_pimpinan':data_pimpinan_, 'pemegang_saham':pemegang_saham_, 'perusahaan_cabang':perusahaan_cabang_, 'syarat':syarat_, 'total_karyawan':total_karyawan, 'jumlah_dirut':jumlah_dirut, 'jumlah_direktur':jumlah_direktur, 'jumlah_komisaris':jumlah_komisaris})
	return render(request, "front-end/include/formulir_tdp_pt/cetak_bukti_pendaftaran.html", extra_context)

def cetak_tdp_koperasi(request, id_pengajuan_):
	extra_context = {}
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_)
		perusahaan_ = pengajuan_.perusahaan
		extra_context.update({'pengajuan': pengajuan_})
	return render(request, "front-end/include/formulir_tdp_koperasi/cetak.html", extra_context)

def cetak_bukti_pendaftaran_tdp_koperasi(request, id_pengajuan_):
	extra_context = {}
	extra_context.update({'formulir_judul': 'FORMULIR PENDAFTARAN PERUSAHAAN TDP KOPERASI'})
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_)
		if pengajuan_:
			no_pengajuan = pengajuan_.no_pengajuan
			jenis_izin = pengajuan_.kelompok_jenis_izin.kelompok_jenis_izin
			pemohon_ = pengajuan_.pemohon
			if pemohon_:
				nama_pemohon = pemohon_.nama_lengkap
				alamat_pemohon = str(pemohon_.alamat)+", Ds. "+str(pemohon_.desa.nama_desa)+", Kec."+str(pemohon_.desa.kecamatan.nama_kecamatan)+", "+str(pemohon_.desa.kecamatan.kabupaten.nama_kabupaten)
			perusahaan_ = pengajuan_.perusahaan
			if perusahaan_:
				nama_perusahaan = perusahaan_.nama_perusahaan
				alamat_perusahaan = str(perusahaan_.alamat_perusahaan)+", Ds. "+str(perusahaan_.desa.nama_desa)+", Kec."+str(perusahaan_.desa.kecamatan.nama_kecamatan)+", "+str(perusahaan_.desa.kecamatan.kabupaten.nama_kabupaten)
			tanggal_dibuat = pengajuan_.created_at
			legalitas_ = pengajuan_.perusahaan.legalitas_set.all()
			# rincian_perusahaan_ = RincianPerusahaan.objects.filter(detil_tdp_id=pengajuan_.id).last()
			izin_lain_ = IzinLain.objects.filter(pengajuan_izin_id=pengajuan_.id)
			data_pimpinan_ = DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id)
			pemegang_saham_ = PemegangSaham.objects.filter(pengajuan_izin_id=pengajuan_.id)
			perusahaan_cabang_ = Perusahaan.objects.filter(perusahaan_induk_id=pengajuan_.perusahaan.id)
			# id_kelompok_list = KelompokJenisIzin.objects.filter(jenis_izin__kode=25)
			syarat_ = Syarat.objects.filter(jenis_izin__kode="TDP-KOPERASI")
			wni = 0
			if pengajuan_.jumlah_karyawan_wni:
				wni = pengajuan_.jumlah_karyawan_wni
			wna = 0
			if pengajuan_.jumlah_karyawan_wna:
				wna = pengajuan_.jumlah_karyawan_wna
			total_karyawan = wni+wna
			jumlah_dirut = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=1))
			jumlah_direktur = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=2))
			jumlah_komisaris = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=3))
			extra_context.update({'no_pengajuan': no_pengajuan, 'jenis_izin':jenis_izin, 'nama_pemohon':nama_pemohon, 'alamat_pemohon':alamat_pemohon, 'nama_perusahaan':nama_perusahaan, 'alamat_perusahaan':alamat_perusahaan, 'created_at':tanggal_dibuat, 'id':pengajuan_.id, 'pengajuan_':pengajuan_, 'legalitas':legalitas_, 'izin_lain':izin_lain_, 'data_pimpinan':data_pimpinan_, 'pemegang_saham':pemegang_saham_, 'perusahaan_cabang':perusahaan_cabang_, 'syarat':syarat_, 'total_karyawan':total_karyawan, 'jumlah_dirut':jumlah_dirut, 'jumlah_direktur':jumlah_direktur, 'jumlah_komisaris':jumlah_komisaris})
	return render(request, "front-end/include/formulir_tdp_koperasi/cetak_bukti_pendaftaran.html", extra_context)

def cetak_tdp_bul(request, id_pengajuan_):
	extra_context = {}
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_)
		perusahaan_ = pengajuan_.perusahaan
		extra_context.update({'pengajuan': pengajuan_})
	return render(request, "front-end/include/formulir_tdp_bul/cetak.html", extra_context)

def cetak_bukti_pendaftaran_tdp_bul(request, id_pengajuan_):
	extra_context = {}
	extra_context.update({'formulir_judul': 'FORMULIR PENDAFTARAN PERUSAHAAN TDP BADAN USAHA LAINNYA (BUL)'})
	if id_pengajuan_:
		pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_)
		if pengajuan_:
			legalitas_ = pengajuan_.perusahaan.legalitas_set.all()
			# rincian_perusahaan_ = RincianPerusahaan.objects.filter(detil_tdp_id=pengajuan_.id).last()
			izin_lain_ = IzinLain.objects.filter(pengajuan_izin_id=pengajuan_.id)
			data_pimpinan_ = DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id)
			pemegang_saham_ = PemegangSaham.objects.filter(pengajuan_izin_id=pengajuan_.id)
			perusahaan_cabang_ = Perusahaan.objects.filter(perusahaan_induk_id=pengajuan_.perusahaan.id)
			# id_kelompok_list = KelompokJenisIzin.objects.filter(jenis_izin__kode=25)
			syarat_ = Syarat.objects.filter(jenis_izin__kode="TDP-BUL")
			wni = 0
			if pengajuan_.jumlah_karyawan_wni:
				wni = pengajuan_.jumlah_karyawan_wni
			wna = 0
			if pengajuan_.jumlah_karyawan_wna:
				wna = pengajuan_.jumlah_karyawan_wna
			total_karyawan = wni+wna
			jumlah_dirut = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=1))
			jumlah_direktur = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=2))
			jumlah_komisaris = len(DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id, kedudukan_id=3))
			extra_context.update({ 'pengajuan_':pengajuan_, 'legalitas':legalitas_, 'izin_lain':izin_lain_, 'data_pimpinan':data_pimpinan_, 'pemegang_saham':pemegang_saham_, 'perusahaan_cabang':perusahaan_cabang_, 'syarat':syarat_, 'total_karyawan':total_karyawan, 'jumlah_dirut':jumlah_dirut, 'jumlah_direktur':jumlah_direktur, 'jumlah_komisaris':jumlah_komisaris})
	return render(request, "front-end/include/formulir_tdp_pt/cetak_bukti_pendaftaran.html", extra_context)

def ajax_cek_pengajuan(request):
	no_pengajuan_ = request.POST.get('no_pengajuan_', None)
	# print no_pengajuan_
	if no_pengajuan_:
		try:
			pengajuan_list = PengajuanIzin.objects.get(no_pengajuan=no_pengajuan_)
			if pengajuan_list:
				url = reverse('list_track_pengajuan', kwargs={'id_pengajuan': pengajuan_list.id} )
				data = {'success': True, 'pesan': 'Pencarian pengajuan sukses.', 'url': url}
			else:
				url = reverse('ajax_cek_pengajuan')
				data = {'success': False, 'pesan': 'Pengajuan tidak ada dalam daftar.', 'url': url}
		except ObjectDoesNotExist:
			url = reverse('ajax_cek_pengajuan')
			data = {'success': False, 'pesan': 'Pengajuan tidak ada dalam daftar.', 'url': url}
	else:
		url = reverse('ajax_cek_pengajuan')
		data = {'success': False, 'pesan': 'Pengajuan tidak ada dalam daftar.', 'url': url}
	return HttpResponse(json.dumps(data))

def ajax_konfirmasi_kbli(request, id_pengajuan_izin_):
	kbli_ = ""
	if id_pengajuan_izin_:
		pengajuan_ = DetilSIUP.objects.get(id=id_pengajuan_izin_)
		kbli_list = pengajuan_.kbli.all()
		kbli_ = [ obj.as_dict() for obj in kbli_list ]
	data = {'success': True, 'pesan': 'Proses Selesai.', 'kbli': kbli_ }
	response = HttpResponse(json.dumps(data))
	return response

def ajax_konfirmasi_kelembagaan(request, id_pengajuan_izin_):
	kelembagaan_ = ""
	if id_pengajuan_izin_:
		pengajuan_ = DetilSIUP.objects.filter(id=id_pengajuan_izin_).last()
		if pengajuan_:
			kelembagaan_list = pengajuan_.kelembagaan.all()
			kelembagaan_ = [ obj.as_dict() for obj in kelembagaan_list ]
	data = {'success': True, 'pesan': 'Proses Selesai.', 'kelembagaan': kelembagaan_ }
	response = HttpResponse(json.dumps(data))
	return response

def ajax_kuasa_pemohon(request, id_pengajuan_izin_):
	nama_kuasa = ""
	no_identitas_kuasa = ""
	telephone_kuasa = ""
	if id_pengajuan_izin_:
		pengajuan_ = PengajuanIzin.objects.get(id=id_pengajuan_izin_)
		if pengajuan_.nama_kuasa:
			nama_kuasa = pengajuan_.nama_kuasa
			no_identitas_kuasa = pengajuan_.no_identitas_kuasa
			telephone_kuasa = pengajuan_.telephone_kuasa

	data = {'success': True, 'pesan': 'Proses Selesai.', 'nama_kuasa': nama_kuasa, 'no_identitas_kuasa':no_identitas_kuasa, 'telephone_kuasa': telephone_kuasa }
	response = HttpResponse(json.dumps(data))
	return response

def ajax_legalitas_konfirmasi(request, id_pengajuan_izin_):
	legalitas_ = ""
	if id_pengajuan_izin_:
		pengajuan_ = PengajuanIzin.objects.get(id=id_pengajuan_izin_)
		legalitas_list = pengajuan_.legalitas.all()
		legalitas_ = [ obj.as_dict() for obj in legalitas_list ]
	data = {'success': True, 'pesan': 'Proses Selesai.', 'legalitas': legalitas_ }
	response = HttpResponse(json.dumps(data))
	return response

def cek_izin_terdaftar(request, id_izin_, extra_context={}):
	if id_izin_:
		pengajuan_ = PengajuanIzin.objects.filter(no_izin=id_izin_).last()
		if pengajuan_:
			no_izin = str(pengajuan_.no_izin)
			extra_context.update({'no_izin': no_izin})
			jenis_izin = pengajuan_.kelompok_jenis_izin.jenis_izin.jenis_izin
			extra_context.update({'jenis_izin': jenis_izin})
			pemilik_izin = pengajuan_.pemohon.nama_lengkap
			extra_context.update({'pemilik_izin': pemilik_izin})
			extra_context.update({'pengajuan_status': pengajuan_.status})

			if pengajuan_.kelompok_jenis_izin.kode == '503.08':
				detilsiup = DetilSIUP.objects.filter(no_izin=id_izin_).last()
				if detilsiup.perusahaan:
					nama_perusahaan = detilsiup.perusahaan.nama_perusahaan
					alamat_ = str(detilsiup.perusahaan.alamat_perusahaan)+", Desa "+str(detilsiup.perusahaan.desa)+", KEC."+str(detilsiup.perusahaan.desa.kecamatan)+", "+str(detilsiup.perusahaan.desa.kecamatan.kabupaten)
					extra_context.update({'nama_perusahaan': nama_perusahaan})
					extra_context.update({'alamat_perusahaan': alamat_})
					extra_context.update({'lokasi': alamat_})
	return render(request, "front-end/cek_izin.html", extra_context)

def option_kbli(request):
	select = request.POST.get('select')
	select = eval(select)
	kbli = request.POST.get('kbli')
	kbli_list = KBLI.objects.filter(Q(nama_kbli__icontains=kbli) | Q(kode_kbli__icontains=kbli))
	if len(select) > 0:
		kbli_list = kbli_list.exclude(id__in=select)
	kbli_list = kbli_list.extra(where=["CHAR_LENGTH(kode_kbli) = 5"])
	pilihan = '<option></option>'
	return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in kbli_list)));

def decimal_default(obj):
	if isinstance(obj, decimal.Decimal):
		return float(obj)
	raise TypeError

def get_nilai_parameter(request):     
	id_parameter = request.POST.get('id_parameter', None)
	parameter = int(id_parameter)
	if parameter == 0:
		get_nilai = 0
	else:
		parameter = ParameterBangunan.objects.get(id=parameter)
		get_nilai = parameter.nilai
	return  HttpResponse(json.dumps(decimal.Decimal(get_nilai),default=decimal_default))
		
def cek_detil_izin(request, id_pengajuan_):
	if id_pengajuan_:
		if id_pengajuan_ != '0':
			pengajuan_ = PengajuanIzin.objects.filter(id=id_pengajuan_).last()
			if pengajuan_:
				if request.COOKIES['id_kelompok_izin']:
					kelompok_jenis_izin = str(pengajuan_.kelompok_jenis_izin.id)
					kelompok_izin_cookie = str(request.COOKIES['id_kelompok_izin'])
					if kelompok_jenis_izin == kelompok_izin_cookie:
						data = {'success': True, 'pesan': 'Proses Selesai.'}
					else:
						data = {'success': False, 'pesan': 'Proses Selesai.'} 
				else:
					data = {'success': False, 'pesan': 'Proses Selesai.'}
			else:
				data = {'success': False, 'pesan': 'Proses Selesai.'}
		else:
			data = {'success': True, 'pesan': 'Proses Selesai.'}
	else:
		data = {'success': False, 'pesan': 'Proses Selesai.'}
	response = HttpResponse(json.dumps(data))
	return response

def list_track_pengajuan(request, id_pengajuan, extra_context={}):
	if id_pengajuan:
		pengajuan = get_object_or_404(PengajuanIzin, id=id_pengajuan)
		if pengajuan:
			riwayat = Riwayat.objects.filter(pengajuan_izin_id=pengajuan.id)
			# print riwayat
			extra_context.update({'pengajuan':pengajuan, 'riwayats':riwayat})
			template = loader.get_template("front-end/list_track_pengajuan.html")
			ec = RequestContext(request, extra_context)
			return HttpResponse(template.render(ec))
		# else:
		#     return redirect(reverse('cari_pengajuan'))

def ajax_save_pengaduan(request):
	data = {"success": False, "pesan": "Terjadi Kesalahan"}
	no_ktp = request.POST.get("no_ktp", None)
	nama_lengkap = request.POST.get('nama_lengkap')
	no_telp = request.POST.get('nomor_telphone')
	email = request.POST.get('email', None)
	kelompok_jenis_izin = request.POST.get('kategori_pengaduan')
	isi_pengaduan = request.POST.get('isi_pengaduan')
	# print no_ktp
	# print isi_pengaduan
	if no_ktp and isi_pengaduan:
		pengaduan_obj = PengaduanIzin(
			no_ktp = no_ktp,
			nama_lengkap = nama_lengkap,
			no_telp = no_telp,
			email = email,
			kelompok_jenis_izin_id = kelompok_jenis_izin,
			isi_pengaduan=isi_pengaduan
			)
		pengaduan_obj.save()
		pesan_pengaduan_obj = PesanPengaduan(
			pengaduan_izin_id = pengaduan_obj.id,
			pesan = isi_pengaduan,
			)
		pesan_pengaduan_obj.save()
		data = {"success": True, "pesan": "berhasil", "nomor_ktp": pengaduan_obj.no_ktp}
	return HttpResponse(json.dumps(data))

def cek_pengaduan(request, no_ktp):
	data = []
	if no_ktp:
		p = PengaduanIzin.objects.filter(no_ktp=no_ktp)
		# p = p.last()
		data = [ob.as_json() for ob in p]
		response = HttpResponse(json.dumps(data), content_type="application/json")
		return response