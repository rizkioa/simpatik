from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon
from izin.models import JenisIzin, Syarat, KelompokJenisIzin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

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
	extra_context.update({'link_formulir': reverse("formulir_ho_pemohonan_baru") })
	extra_context.update({'id_jenis_izin': "2" })
	extra_context.update({'id_kelompok_jenis_izin': "12" })
	return render(request, "front-end/layanan/ho_baru.html", extra_context)

def layanan_ho_daftar_ulang(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=13)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Izin Gangguan (HO) - Daftar Ulang"})
	extra_context.update({'title_short': "HO - Daftar Ulang"})
	extra_context.update({'link_formulir': reverse("formulir_ho_daftar_ulang") })
	extra_context.update({'id_jenis_izin': "2" })
	extra_context.update({'id_kelompok_jenis_izin': "13" })
	return render(request, "front-end/layanan/ho_daftar_ulang.html", extra_context)

def layanan_tdp_pt(request, extra_context={}):
	kelompok = get_object_or_404(KelompokJenisIzin, id=25)
	extra_context.update({'kelompok': kelompok})
	extra_context.update({'title_long': "Tanda Daftar Perusahaan (TDP) - PT"})
	extra_context.update({'title_short': "TDP - Persero Terbatas (PT)"})
	extra_context.update({'link_formulir': reverse("formulir_tdp_pt") })
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
	extra_context.update({'link_formulir': reverse("formulir_reklame") })
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
	extra_context.update({'link_formulir': reverse("formulir_huller") })
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

def layanan_sipa_sumur_bor(request, extra_context={}):
	return render(request, "front-end/layanan/sipa_sumur_bor.html")

def layanan_sipa_sumur_pasak(request, extra_context={}):
	return render(request, "front-end/layanan/sipa_sumur_pasak.html")

def layanan_pertambangan(request, extra_context={}):
	return render(request, "front-end/layanan/pertambangan.html")