from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import NomorIdentitasPengguna
from izin.utils import STATUS_HAK_TANAH
from master.models import Negara, Provinsi, Kabupaten, Kecamatan, JenisPemohon, JenisReklame,ParameterBangunan
from izin.models import PengajuanIzin, JenisPermohonanIzin, KelompokJenisIzin, Pemohon, InformasiTanah,PenggunaanTanahIPPTUsaha,PerumahanYangDimilikiIPPTUsaha,SertifikatTanah,AktaJualBeliTanah,NoPTP
from accounts.utils import KETERANGAN_PEKERJAAN

def formulir_ippt_usaha(request):
	extra_context={}
	if 'id_kelompok_izin' in request.COOKIES.keys():
		extra_context.update({'title': 'IPPT - Usaha'})
		negara = Negara.objects.all()
		kecamatan = Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35')
		jenis_pemohon = JenisPemohon.objects.all()

		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) # Un
		
		extra_context.update({
			'negara': negara,
			'kecamatan': kecamatan,
			'jenis_pemohon': jenis_pemohon,
			'has_permission': True,
			'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
			'jenispermohonanizin_list': jenispermohonanizin_list,

			})

		# +++++++++++++++++++ jika cookie pengajuan ada dan di refrash +++++++++++++++++
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan'] != "":
				try:
					pengajuan_ = InformasiTanah.objects.get(id=request.COOKIES['id_pengajuan'])
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
					penggunaan_tanah_list = PenggunaanTanahIPPTUsaha.objects.filter(informasi_tanah=request.COOKIES['id_pengajuan'])
					perumahan_list = PerumahanYangDimilikiIPPTUsaha.objects.filter(informasi_tanah=request.COOKIES['id_pengajuan'])
					extra_context.update({'penggunaan_tanah_list': penggunaan_tanah_list})
					extra_context.update({'perumahan_list': perumahan_list})
					extra_context.update({ 'no_pengajuan_konfirmasi': pengajuan_.no_pengajuan })
					extra_context.update({ 'jenis_permohonan_konfirmasi': pengajuan_.jenis_permohonan })
					extra_context.update({ 'pengajuan_': pengajuan_ })
					if 'id_pengajuan' in request.COOKIES.keys():
						if request.COOKIES['id_pengajuan'] != '':
						  sertifikat_tanah_list = SertifikatTanah.objects.filter(informasi_tanah=request.COOKIES['id_pengajuan'])
						  akta_jual_beli_list = AktaJualBeliTanah.objects.filter(informasi_tanah=request.COOKIES['id_pengajuan'])
						  no_ptp_list = NoPTP.objects.filter(informasi_tanah=request.COOKIES['id_pengajuan'])

						  extra_context.update({'sertifikat_tanah_list': sertifikat_tanah_list})
						  extra_context.update({'akta_jual_beli_list': akta_jual_beli_list})
						  extra_context.update({'no_ptp_list': no_ptp_list})

					if pengajuan_.desa:
						letak_ = pengajuan_.alamat + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
					else:
						letak_ = ""
					extra_context.update({ 'letak': letak_ })
				except ObjectDoesNotExist:
					pass
		template = loader.get_template("admin/izin/izin/form_wizard_ippt_usaha.html")
		ec = RequestContext(request, extra_context)
		response = HttpResponse(template.render(ec))
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan'] != "0":
				pengajuan_ = InformasiTanah.objects.get(id=request.COOKIES['id_pengajuan'])
				if pengajuan_.pemohon:
					response.set_cookie(key='id_pemohon', value=pengajuan_.pemohon.id)
				if ktp_:
					response.set_cookie(key='nomor_ktp', value=ktp_)
		return response
	else:
		messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
		return HttpResponseRedirect(reverse('admin:add_wizard_izin'))