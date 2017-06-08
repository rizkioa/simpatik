from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon
from izin.models import JenisIzin, Syarat, KelompokJenisIzin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

def layanan_iujk(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=37)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Ijin Usaha Jasa Konstruksi (IUJK)"})
	extra_context.update({'title_short': "IUJK"})
	extra_context.update({'link_formulir': reverse("formulir_iujk") })
	extra_context.update({'id_jenis_izin': "15" })
	extra_context.update({'id_kelompok_jenis_izin': "37" })
	response = render(request, "front-end/layanan/iujk.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="37")
	return response

def layanan_izin_parkir(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, kode='IZINPARKIR')
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Parkir"})
	extra_context.update({'title_short': "Izin Parkir"})
	extra_context.update({'link_formulir': reverse("formulir_izin_parkir") })
	extra_context.update({'id_jenis_izin': "31" })
	extra_context.update({'id_kelompok_jenis_izin': "55" })
	response = render(request, "front-end/layanan/iujk.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="55")
	response.set_cookie(key='kode_kelompok_jenis_izin', value="IZINPARKIR")
	return response

def layanan_tdup(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, kode='TDUP')
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Usaha Pariwisata"})
	extra_context.update({'title_short': "TDUP"})
	extra_context.update({'link_formulir': reverse("formulir_tdup") })
	extra_context.update({'id_jenis_izin': "17" })
	extra_context.update({'id_kelompok_jenis_izin': "41" })
	response = render(request, "front-end/layanan/iujk.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="41")
	response.set_cookie(key='kode_kelompok_jenis_izin', value="TDUP")
	return response

def layanan_siup(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, kode='503.08')
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Surat Perizinan Usaha Perdagangan (SIUP)"})
	extra_context.update({'title_short': "SIUP"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "6" })
	extra_context.update({'id_kelompok_jenis_izin': "17" })
	response = render(request, "front-end/layanan/siup.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="17")
	response.set_cookie(key='kode_kelompok_jenis_izin', value="503.08")
	return response

def layanan_ho(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=12)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Gangguan (HO)"})
	extra_context.update({'title_short': "HO"})
	extra_context.update({'link_formulir': reverse("formulir_ho") })
	extra_context.update({'id_jenis_izin': "2" })
	extra_context.update({'id_kelompok_jenis_izin': "12" })
	response = render(request, "front-end/layanan/ho_baru.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="12")
	return response

def layanan_izin_lokasi(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, kode="503.07/")
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Lokasi"})
	extra_context.update({'title_short': "Izin Lokasi"})
	extra_context.update({'link_formulir': reverse("formulir_izin_lokasi") })
	extra_context.update({'id_jenis_izin': "14" })
	extra_context.update({'id_kelompok_jenis_izin': kelompok.id })
	response = render(request, "front-end/layanan/izin_lokasi.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value=kelompok.id)
	return response

# def layanan_ho_daftar_ulang(request, extra_context={}):
# 	kelompok = get_object_or_404(KelompokJenisIzin, id=13)
# 	extra_context.update({'kelompok': kelompok})
# 	extra_context.update({'title_long': "Izin Gangguan (HO) - Daftar Ulang"})
# 	extra_context.update({'title_short': "HO - Daftar Ulang"})
# 	extra_context.update({'link_formulir': reverse("formulir_ho_daftar_ulang") })
# 	extra_context.update({'id_jenis_izin': "2" })
# 	extra_context.update({'id_kelompok_jenis_izin': "13" })
# 	response = render(request, "front-end/layanan/ho_daftar_ulang.html", extra_context)
# 	response.set_cookie(key='id_kelompok_izin', value="13")
# 	return response

def layanan_ippt_rumah(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, kode="IPPT-Rumah")
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Perubahan Penggunaan Tanah (IPPT) - Rumah"})
	extra_context.update({'title_short': "Izin Perubahan Penggunaan Tanah (IPPT) - Rumah"})
	extra_context.update({'link_formulir': reverse("formulir_ippt_rumah") })
	extra_context.update({'id_jenis_izin': "15" })
	extra_context.update({'id_kelompok_jenis_izin': kelompok.id })
	response = render(request, "front-end/layanan/ippt_rumah.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value=kelompok.id)
	return response

def layanan_ippt_usaha(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, kode="IPPT-Usaha")
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Perubahan Penggunaan Tanah (IPPT) - Usaha"})
	extra_context.update({'title_short': "Izin Perubahan Penggunaan Tanah (IPPT) - Usaha"})
	extra_context.update({'link_formulir': reverse("formulir_ippt_usaha") })
	extra_context.update({'id_jenis_izin': "15" })
	extra_context.update({'id_kelompok_jenis_izin': kelompok.id })
	response = render(request, "front-end/layanan/ippt_usaha.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value=kelompok.id)
	return response

def layanan_tdp_pt(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=25)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - PT"})
	extra_context.update({'title_short': "TDP - Persero Terbatas (PT)"})
	extra_context.update({'link_formulir': reverse("formulir_tdp_pt") })
	extra_context.update({'id_jenis_izin': "7" })
	extra_context.update({'id_kelompok_jenis_izin': "25" })
	response = render(request, "front-end/layanan/tdp_pt.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="25")
	return response

def layanan_tdp_cv(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=26)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - CV"})
	extra_context.update({'title_short': "TDP - CV"})
	extra_context.update({'link_formulir': reverse("formulir_tdp_cv") })
	extra_context.update({'id_jenis_izin': "7" })
	extra_context.update({'id_kelompok_jenis_izin': "26" })
	response = render(request, "front-end/layanan/tdp_cv.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="26")
	return response

def layanan_tdp_firma(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=27)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - Firma"})
	extra_context.update({'title_short': "TDP - Firma"})
	extra_context.update({'link_formulir': reverse("formulir_tdp_firma") })
	extra_context.update({'id_jenis_izin': "7" })
	extra_context.update({'id_kelompok_jenis_izin': "27" })
	response = render(request, "front-end/layanan/tdp_firma.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="27")
	return response

def layanan_tdp_perorangan(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=28)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - Perorangan"})
	extra_context.update({'title_short': "TDP - Perorangan"})
	extra_context.update({'link_formulir': reverse("formulir_tdp_perorangan") })
	extra_context.update({'id_jenis_izin': "7" })
	extra_context.update({'id_kelompok_jenis_izin': "28" })
	response = render(request, "front-end/layanan/tdp_perorangan.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="28")
	return response

def layanan_tdp_koperasi(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=29)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - Koperasi"})
	extra_context.update({'title_short': "TDP - Koperasi"})
	extra_context.update({'link_formulir': reverse("formulir_tdp_koperasi") })
	extra_context.update({'id_jenis_izin': "7" })
	extra_context.update({'id_kelompok_jenis_izin': "29" })
	response = render(request, "front-end/layanan/tdp_koperasi.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="29")
	return response

def layanan_tdp_bul(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=30)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - Bentuk Usaha Lainnya"})
	extra_context.update({'title_short': "TDP - BUL"})
	extra_context.update({'link_formulir': reverse("formulir_tdp_bul") })
	extra_context.update({'id_jenis_izin': "7" })
	extra_context.update({'id_kelompok_jenis_izin': "30" })
	response = render(request, "front-end/layanan/tdp_bul.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="30")
	return response

def layanan_tdp_baru_cabang(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=31)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - Kantor Cabang"})
	extra_context.update({'title_short': "TDP - Kantor Cabang"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "7" })
	extra_context.update({'id_kelompok_jenis_izin': "31" })
	response = render(request, "front-end/layanan/tdp_cabang.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="31")
	return response

def layanan_tdp_daftar_ulang(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=32)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - Permohonan Ulang"})
	extra_context.update({'title_short': "TDP - Permohonan Ulang"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "7" })
	extra_context.update({'id_kelompok_jenis_izin': "32" })
	response = render(request, "front-end/layanan/tdp_daftar_ulang.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="32")
	return response

def layanan_imb_umum(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=2)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Mendirikan Bangunan (IMB) - Umum"})
	extra_context.update({'title_short': "IMB - Umum"})
	extra_context.update({'link_formulir': reverse("formulir_imb_umum") })
	extra_context.update({'id_jenis_izin': "1" })
	extra_context.update({'id_kelompok_jenis_izin': "2" })
	response = render(request, "front-end/layanan/imb_umum.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="2")
	return response

def layanan_imb_reklame(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=1)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Mendirikan Bangunan (IMB) - Papan Reklame"})
	extra_context.update({'title_short': "IMB - Umum"})
	extra_context.update({'link_formulir': reverse("formulir_imb_reklame") })
	extra_context.update({'id_jenis_izin': "1" })
	extra_context.update({'id_kelompok_jenis_izin': "1" })
	response = render(request, "front-end/layanan/imb_reklame.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="1")
	return response

def layanan_imb_perumahan(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=11)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Mendirikan Bangunan (IMB) - Perumahan"})
	extra_context.update({'title_short': "IMB - Perumahan"})
	extra_context.update({'link_formulir': reverse("formulir_imb_perumahan") })
	extra_context.update({'id_jenis_izin': "1" })
	extra_context.update({'id_kelompok_jenis_izin': "11" })
	response = render(request, "front-end/layanan/imb_perumahan.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="11")
	return response

def layanan_reklame(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=14)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Pemasangan Reklame"})
	extra_context.update({'title_short': "Izin Pemasangan Reklame"})
	extra_context.update({'link_formulir': reverse("formulir_reklame") })
	extra_context.update({'id_jenis_izin': "3" })
	extra_context.update({'id_kelompok_jenis_izin': "14" })
	response = render(request, "front-end/layanan/reklame.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="14")
	return response

def layanan_kekayaan(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=16)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Pemakaian Kekayaan Daerah"})
	extra_context.update({'title_short': "Izin Pemakaian Kekayaan Daerah"})
	extra_context.update({'link_formulir': reverse("formulir_kekayaan") })
	extra_context.update({'id_jenis_izin': "5" })
	extra_context.update({'id_kelompok_jenis_izin': "16" })
	response = render(request, "front-end/layanan/kekayaan.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="16")
	return response

def layanan_huller(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=15)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Usaha Perusahaan Penggilingan Padi & Huller"})
	extra_context.update({'title_short': "Huller"})
	extra_context.update({'link_formulir': reverse("formulir_huller") })
	extra_context.update({'id_jenis_izin': "4" })
	extra_context.update({'id_kelompok_jenis_izin': "15" })
	response = render(request, "front-end/layanan/huller.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="15")
	return response

def layanan_izin_prinsip_penanaman_modal(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=33)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Prinsip Penanaman Modal"})
	extra_context.update({'title_short': "Izin Prinsip Penanaman Modal"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "8" })
	extra_context.update({'id_kelompok_jenis_izin': "33" })
	response = render(request, "front-end/layanan/izin_prinsip_penanaman_modal.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="33")
	return response

def layanan_izin_prinsip_perluasan_penanaman_modal(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=35)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Prinsip Perluasan Penanaman Modal"})
	extra_context.update({'title_short': "Izin Prinsip Perluasan Penanaman Modal"})
	extra_context.update({'link_formulir': reverse("formulir_siup") })
	extra_context.update({'id_jenis_izin': "9" })
	extra_context.update({'id_kelompok_jenis_izin': "35" })
	response = render(request, "front-end/layanan/izin_prinsip_perluasan_penanaman_modal.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="35")
	return response

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

def layanan_izin_usaha_angkutan(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=3)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Usaha Angkutan"})
	extra_context.update({'title_short': "Izin Usaha Angkutan"})
	extra_context.update({'link_formulir': reverse("formulir_izin_usaha_angkutan") })
	extra_context.update({'id_jenis_izin': "30" })
	extra_context.update({'id_kelompok_jenis_izin': "3" })
	response = render(request, "front-end/layanan/izin_usaha_angkutan.html", extra_context)
	response.set_cookie(key='id_kelompok_izin', value="3")
	return response

def layanan_sipa_sumur_bor(request, extra_context={}):
	return render(request, "front-end/layanan/sipa_sumur_bor.html")

def layanan_sipa_sumur_pasak(request, extra_context={}):
	return render(request, "front-end/layanan/sipa_sumur_pasak.html")

def layanan_pertambangan(request, extra_context={}):
	return render(request, "front-end/layanan/pertambangan.html")