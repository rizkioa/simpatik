from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import NomorIdentitasPengguna

from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon, JenisReklame
from perusahaan.models import BentukKegiatanUsaha, JenisPenanamanModal, Kelembagaan, KBLI, ProdukUtama, JenisLegalitas
from izin.models import PengajuanIzin, JenisPermohonanIzin, KelompokJenisIzin, Pemohon, DetilReklame

def formulir_reklame(request):
	extra_context={}
	if 'id_kelompok_izin' in request.COOKIES.keys():
		extra_context.update({'title': 'Reklame Baru'})
		negara = Negara.objects.all()
		kecamatan = Kecamatan.objects.filter(kabupaten__id=1)
		jenis_pemohon = JenisPemohon.objects.all()
		bentuk_kegiatan_usaha_list = BentukKegiatanUsaha.objects.all()
		jenis_penanaman_modal_list = JenisPenanamanModal.objects.all()
		kelembagaan_list = Kelembagaan.objects.all()
		kbli_list = KBLI.objects.all()
		produk_utama_list = ProdukUtama.objects.all()
		jenis_legalitas_list = JenisLegalitas.objects.all()
		jenis_reklame = JenisReklame.objects.all()

		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) # Untuk SIUP
		extra_context.update({'negara': negara})
		extra_context.update({'kecamatan': kecamatan})
		extra_context.update({'jenis_pemohon': jenis_pemohon})
		# print request.COOKIES
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
		extra_context.update({'bentuk_kegiatan_usaha_list': bentuk_kegiatan_usaha_list})
		extra_context.update({'jenis_penanaman_modal_list': jenis_penanaman_modal_list})
		extra_context.update({'kelembagaan_list': kelembagaan_list})
		extra_context.update({'kbli_list': kbli_list})
		extra_context.update({'produk_utama_list': produk_utama_list})
		extra_context.update({'jenis_legalitas_list': jenis_legalitas_list})
		extra_context.update({'jenis_reklame': jenis_reklame})

		# +++++++++++++++++++ jika cookie pengajuan ada dan di refrash +++++++++++++++++
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
						try:
							ktp_ = NomorIdentitasPengguna.objects.get(user_id=pengajuan_.pemohon.id)
							extra_context.update({'cookie_file_ktp': ktp_.berkas })
						except ObjectDoesNotExist:
							pass
					if pengajuan_.perusahaan:
						if pengajuan_.perusahaan.desa:
							alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
							extra_context.update({ 'alamat_perusahaan_konfirmasi': alamat_perusahaan_ })
						extra_context.update({ 'perusahaan_konfirmasi': pengajuan_.perusahaan })
					
					extra_context.update({ 'no_pengajuan_konfirmasi': pengajuan_.no_pengajuan })
					extra_context.update({ 'jenis_permohonan_konfirmasi': pengajuan_.jenis_permohonan })
					extra_context.update({ 'pengajuan_': pengajuan_ })

				except ObjectDoesNotExist:
					pass
		template = loader.get_template("admin/izin/izin/form_wizard_reklame.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))
	else:
		messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
		return HttpResponseRedirect(reverse('admin:add_wizard_izin'))