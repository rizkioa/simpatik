from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import NomorIdentitasPengguna
from izin.utils import STATUS_HAK_TANAH,KLASIFIKASI_JALAN,RUMIJA,RUWASJA,JENIS_LOKASI_USAHA
from accounts.utils import KETERANGAN_PEKERJAAN

from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon, JenisReklame,ParameterBangunan
from izin.models import PengajuanIzin, JenisPermohonanIzin, KelompokJenisIzin, Pemohon, DetilIMB

def formulir_imb_perumahan(request):
	extra_context={}
	if 'id_kelompok_izin' in request.COOKIES.keys():
		extra_context.update({'title': 'Izin IMB Perumahan'})
		negara = Negara.objects.all()
		kecamatan = Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35')
		jenis_pemohon = JenisPemohon.objects.all()
		reklame_jenis_list = JenisReklame.objects.all()
		kegiatan_pembangunan = ParameterBangunan.objects.filter(parameter="Kegiatan Pembangunan Gedung")
		fungsi_bangunan = ParameterBangunan.objects.filter(parameter="Fungsi Bangunan")
		kompleksitas_bangunan = ParameterBangunan.objects.filter(parameter="Tingkat Kompleksitas")
		permanensi_bangunan = ParameterBangunan.objects.filter(parameter="Tingkat Permanensi")
		ketinggian_bangunan = ParameterBangunan.objects.filter(parameter="Ketinggian Bangunan")
		lokasi_bangunan = ParameterBangunan.objects.filter(parameter="Lokasi Bangunan")
		kepemilikan_bangunan = ParameterBangunan.objects.filter(parameter="Kepemilikan Bangunan")
		lama_penggunaan_bangunan = ParameterBangunan.objects.filter(parameter="Lama Penggunaan Bangunan")
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) # Untuk Reklame
		extra_context.update({
			'klasifikasi_jalan': JENIS_LOKASI_USAHA,
			'rumija': RUMIJA,
			'ruwasja': RUWASJA,
			'fungsi_bangunan': fungsi_bangunan,
			'kompleksitas_bangunan': kompleksitas_bangunan,
			'permanensi_bangunan': permanensi_bangunan,
			'ketinggian_bangunan': ketinggian_bangunan,
			'lokasi_bangunan': lokasi_bangunan,
			'kepemilikan_bangunan': kepemilikan_bangunan,
			'lama_penggunaan_bangunan': lama_penggunaan_bangunan,
			'kegiatan_pembangunan': kegiatan_pembangunan,
			'status_hak_tanah': STATUS_HAK_TANAH,
			'negara': negara,
			'kecamatan': kecamatan,
			'jenis_pemohon': jenis_pemohon,
			'jenispermohonanizin_list': jenispermohonanizin_list,
			'reklame_jenis_list': reklame_jenis_list,
			'has_permission': True,
			'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,

			})
		# +++++++++++++++++++ jika cookie pengajuan ada dan di refrash +++++++++++++++++
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan'] != "":
				try:
					pengajuan_ = DetilIMB.objects.get(id=request.COOKIES['id_pengajuan'])
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

					extra_context.update({ 'no_pengajuan_konfirmasi': pengajuan_.no_pengajuan })
					extra_context.update({ 'jenis_permohonan_konfirmasi': pengajuan_.jenis_permohonan })
					extra_context.update({ 'pengajuan_': pengajuan_ })

					if pengajuan_.desa:
						letak_ = pengajuan_.lokasi + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
					else:
						letak_ = ""
					extra_context.update({ 'letak': letak_ })
				except ObjectDoesNotExist:
					pass
		template = loader.get_template("admin/izin/izin/form_wizard_imb_perumahan.html")
		ec = RequestContext(request, extra_context)
		response = HttpResponse(template.render(ec))
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan'] != "0":
				pengajuan_ = DetilIMB.objects.get(id=request.COOKIES['id_pengajuan'])
				if pengajuan_.pemohon:
					response.set_cookie(key='id_pemohon', value=pengajuan_.pemohon.id)
					response.set_cookie(key='kode_kelompok_jenis_izin', value=pengajuan_.kelompok_jenis_izin.kode)
				if ktp_:
					response.set_cookie(key='nomor_ktp', value=ktp_)
		return response
	else:
		messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
		return HttpResponseRedirect(reverse('admin:add_wizard_izin'))