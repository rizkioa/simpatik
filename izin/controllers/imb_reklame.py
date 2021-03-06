from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import NomorIdentitasPengguna
from izin.utils import KLASIFIKASI_JALAN
from accounts.utils import KETERANGAN_PEKERJAAN

from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon, JenisReklame
from perusahaan.models import BentukKegiatanUsaha, JenisPenanamanModal, Kelembagaan, KBLI, JenisLegalitas
from izin.models import PengajuanIzin, JenisPermohonanIzin, KelompokJenisIzin, Pemohon, DetilIMBPapanReklame,JENIS_LOKASI_USAHA

def formulir_imb_reklame(request):
	extra_context={}
	if 'id_kelompok_izin' in request.COOKIES.keys():
		extra_context.update({'title': 'Reklame Baru'})
		negara = Negara.objects.all()
		kecamatan = Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35')
		jenis_pemohon = JenisPemohon.objects.all()
		bentuk_kegiatan_usaha_list = BentukKegiatanUsaha.objects.all()
		jenis_penanaman_modal_list = JenisPenanamanModal.objects.all()
		kelembagaan_list = Kelembagaan.objects.all()
		kbli_list = KBLI.objects.all()
		jenis_legalitas_list = JenisLegalitas.objects.all()
		reklame_jenis_list = JenisReklame.objects.all()

		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) # Untuk Reklame
		
		extra_context.update({
			'negara': negara,
			'kecamatan': kecamatan,
			'jenis_pemohon': jenis_pemohon,
			'klasifikasi_jalan': JENIS_LOKASI_USAHA,
			'jenispermohonanizin_list': jenispermohonanizin_list,
			'bentuk_kegiatan_usaha_list': bentuk_kegiatan_usaha_list,
			'jenis_penanaman_modal_list': jenis_penanaman_modal_list,
			'kelembagaan_list': kelembagaan_list,
			'kbli_list': kbli_list,
			'jenis_legalitas_list': jenis_legalitas_list,
			'reklame_jenis_list': reklame_jenis_list,
			'has_permission': True,
			'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
			})

		# +++++++++++++++++++ jika cookie pengajuan ada dan di refrash +++++++++++++++++
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan'] != "":
				try:
					pengajuan_ = DetilIMBPapanReklame.objects.get(id=request.COOKIES['id_pengajuan'])
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
					ukuran_ = "Lebar = "+str(int(pengajuan_.lebar))+" M , Tinggi = "+str(int(pengajuan_.tinggi))+" M"

					extra_context.update({ 'no_pengajuan_konfirmasi': pengajuan_.no_pengajuan })
					extra_context.update({ 'jenis_permohonan_konfirmasi': pengajuan_.jenis_permohonan })
					extra_context.update({ 'pengajuan_': pengajuan_ })
					extra_context.update({ 'ukuran': ukuran_ })

					if pengajuan_.desa:
						letak_ = pengajuan_.lokasi_pasang + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
					else:
						letak_ = ""
					extra_context.update({ 'letak': letak_ })
				except ObjectDoesNotExist:
					pass
		template = loader.get_template("admin/izin/izin/form_wizard_imb_reklame.html")
		ec = RequestContext(request, extra_context)
		response = HttpResponse(template.render(ec))
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan'] != "0":
				pengajuan_ = DetilIMBPapanReklame.objects.get(id=request.COOKIES['id_pengajuan'])
				if pengajuan_.pemohon:
					response.set_cookie(key='id_pemohon', value=pengajuan_.pemohon.id)
					response.set_cookie(key='kode_kelompok_jenis_izin', value=pengajuan_.kelompok_jenis_izin.kode)
				if pengajuan_.perusahaan:
					response.set_cookie(key='id_perusahaan', value=pengajuan_.perusahaan.id)
				if ktp_:
					response.set_cookie(key='nomor_ktp', value=ktp_)
		return response
	else:
		messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
		return HttpResponseRedirect(reverse('admin:add_wizard_izin'))