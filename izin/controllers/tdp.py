from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import NomorIdentitasPengguna

from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon, JenisReklame
from perusahaan.models import BentukKegiatanUsaha, JenisPenanamanModal, Kelembagaan, KBLI, ProdukUtama, JenisLegalitas, JenisBadanUsaha, StatusPerusahaan, BentukKerjasama, KedudukanKegiatanUsaha, JenisPerusahaan, JenisPengecer, Legalitas, Perusahaan
from izin.models import PengajuanIzin, JenisPermohonanIzin, KelompokJenisIzin, Pemohon, DetilTDP, RincianPerusahaan

def formulir_tdp_pt(request):
	extra_context={}
	if 'id_kelompok_izin' in request.COOKIES.keys():
		extra_context.update({'title': 'TDP PT Baru'})
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
		jenis_perusahaan = JenisPerusahaan.objects.all()
		extra_context.update({'jenis_perusahaan': jenis_perusahaan})
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan']:
				try:
					pengajuan_ = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
					alamat_ = ""
					alamat_perusahaan_ = ""
					if pengajuan_.pemohon:
						if pengajuan_.pemohon.desa:
							alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
							extra_context.update({'alamat_pemohon_konfirmasi': alamat_})
							extra_context.update({ 'pemohon_konfirmasi': pengajuan_.pemohon })
							ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
							extra_context.update({ 'ktp': ktp_ })
							paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
							extra_context.update({ 'paspor': paspor_ })
						if pengajuan_.perusahaan:
							alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
							extra_context.update({ 'alamat_perusahaan_konfirmasi': alamat_perusahaan_ })
							extra_context.update({ 'perusahaan_konfirmasi': pengajuan_.perusahaan })
							legalitas = Legalitas.objects.filter(perusahaan_id=pengajuan_.perusahaan.id)
							pendirian = legalitas.filter(jenis_legalitas_id=1).last()
							perubahan = legalitas.filter(jenis_legalitas_id=2).last()
							pengesahan_menteri = legalitas.filter(jenis_legalitas_id=3).last()
							persetujuan_menteri = legalitas.filter(jenis_legalitas_id=4).last()
							penerimaan_laporan = legalitas.filter(jenis_legalitas_id=6).last()
							penerimaan_pemberitahuan = legalitas.filter(jenis_legalitas_id=7).last()
							extra_context.update({ 'pendirian': pendirian })
							extra_context.update({ 'perubahan': perubahan })
							extra_context.update({ 'pengesahan_menteri': pengesahan_menteri })
							extra_context.update({ 'persetujuan_menteri': persetujuan_menteri })
							extra_context.update({ 'penerimaan_laporan': penerimaan_laporan })
							extra_context.update({ 'penerimaan_pemberitahuan': penerimaan_pemberitahuan })
						extra_context.update({ 'pengajuan_': pengajuan_ })
						perusahaan_induk = Perusahaan.objects.filter(id=request.COOKIES['id_perusahaan_induk']).last()
						extra_context.update({'perusahaan_induk': perusahaan_induk})
						try:
							rp = RincianPerusahaan.objects.get(detil_tdp_id=pengajuan_.id)
							extra_context.update({ 'rincianperusahaan': rp })
						except ObjectDoesNotExist:
							pass

						template = loader.get_template("admin/izin/izin/form_wizard_tdp_pt.html")
						ec = RequestContext(request, extra_context)
						response = HttpResponse(template.render(ec))

						if pengajuan_.pemohon:
							response.set_cookie(key='id_pemohon', value=pengajuan_.pemohon.id)
						if pengajuan_.perusahaan:
							response.set_cookie(key='id_perusahaan', value=pengajuan_.perusahaan.id)
				except ObjectDoesNotExist:
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
