from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import NomorIdentitasPengguna

from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon, JenisReklame
from perusahaan.models import BentukKegiatanUsaha, JenisPenanamanModal, Kelembagaan, KBLI, JenisLegalitas, JenisBadanUsaha, StatusPerusahaan, BentukKerjasama, KedudukanKegiatanUsaha, JenisPerusahaan, JenisPengecer, Legalitas, Perusahaan, JenisKedudukan
from izin.models import PengajuanIzin, JenisPermohonanIzin, KelompokJenisIzin, Pemohon, DetilTDP, RincianPerusahaan

def formulir_tdp_pt(request):
	extra_context={}
	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
		extra_context.update({'negara': negara})
		extra_context.update({'title': 'TDP PT Baru'})
		negara = Negara.objects.all()
		extra_context.update({'negara': negara})
		provinsi = Provinsi.objects.all()
		extra_context.update({'provinsi': provinsi})
		kecamatan = Kecamatan.objects.all()
		extra_context.update({'kecamatan': kecamatan})
		jenis_pemohon = JenisPemohon.objects.all()
		extra_context.update({'jenis_pemohon': jenis_pemohon})
		jenis_badan_usaha = JenisBadanUsaha.objects.all()
		extra_context.update({'jenis_badan_usaha': jenis_badan_usaha})
		status_perusahaan = StatusPerusahaan.objects.all()
		extra_context.update({'status_perusahaan': status_perusahaan})
		jenis_penanaman_modal = JenisPenanamanModal.objects.all()
		extra_context.update({'jenis_penanaman_modal': jenis_penanaman_modal})
		bentuk_kerjasama = BentukKerjasama.objects.all()
		extra_context.update({'bentuk_kerjasama': bentuk_kerjasama})
		jenis_pengecer = JenisPengecer.objects.all()
		extra_context.update({'jenis_pengecer': jenis_pengecer})
		kedudukan_kegiatan_usaha = KedudukanKegiatanUsaha.objects.all()
		extra_context.update({'kedudukan_kegiatan_usaha': kedudukan_kegiatan_usaha})
		kelompok_jenis_izin = KelompokJenisIzin.objects.all()
		extra_context.update({'kelompok_jenis_izin': kelompok_jenis_izin})
		jenis_kedudukan = JenisKedudukan.objects.all()
		extra_context.update({'jenis_kedudukan': jenis_kedudukan})
		bentuk_kegiatan_usaha_list = BentukKegiatanUsaha.objects.all()
		extra_context.update({'kegiatan_usaha': bentuk_kegiatan_usaha_list})
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan']:
				try:
					pengajuan_ = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
					extra_context.update({'pengajuan_': pengajuan_})
					extra_context.update({'pengajuan_id': pengajuan_.id})
					if pengajuan_.pemohon:
						ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
						extra_context.update({ 'ktp': ktp_ })
						paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
						extra_context.update({ 'paspor': paspor_ })
						template = loader.get_template("admin/izin/izin/form_wizard_tdp_pt.html")
						ec = RequestContext(request, extra_context)
						response = HttpResponse(template.render(ec))
				except ObjectDoesNotExist:
					extra_context.update({'pengajuan_id': '0'})
					template = loader.get_template("admin/izin/izin/form_wizard_tdp_pt.html")
					ec = RequestContext(request, extra_context)
					response = HttpResponse(template.render(ec))
		else:
			template = loader.get_template("admin/izin/izin/form_wizard_tdp_pt.html")
			ec = RequestContext(request, extra_context)
			response = HttpResponse(template.render(ec))	
		return response
	else:
		messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
		return HttpResponseRedirect(reverse('admin:add_wizard_izin'))
