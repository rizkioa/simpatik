from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


from master.models import Negara, JenisPemohon, Kecamatan
from izin.models import JenisPermohonanIzin, PaketPekerjaan, DetilIUJK
from izin.utils import JENIS_IUJK, get_tahun_choices
from perusahaan.models import BentukKegiatanUsaha, JenisPenanamanModal, Kelembagaan, KBLI, JenisLegalitas
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna


def IUJKWizard(request, extra_context={}):
	extra_context.update({'title': 'Formulir IUJK'})
	extra_context.update({'has_permission': True})
	extra_context.update({'negara': Negara.objects.all()})
	extra_context.update({'jenis_pemohon': JenisPemohon.objects.all()})
	extra_context.update({'bentuk_kegiatan_usaha_list': BentukKegiatanUsaha.objects.all()})
	extra_context.update({'jenis_penanaman_modal_list': JenisPenanamanModal.objects.all()})
	extra_context.update({'kelembagaan_list': Kelembagaan.objects.all()})
	extra_context.update({'kbli_list': KBLI.objects.all()})
	# extra_context.update({'produk_utama_list': ProdukUtama.objects.all()})
	extra_context.update({'jenis_legalitas_list': JenisLegalitas.objects.all()})
	extra_context.update({'jenis_iujk': JENIS_IUJK })
	extra_context.update({'tahun_choices': get_tahun_choices(1945) })
	extra_context.update({'kecamatan_perusahaan': Kecamatan.objects.filter(kabupaten=1) })

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
					# extra_context.update({ 'kelompok_jenis_izin_konfirmasi': pengajuan_.kelompok_jenis_izin })
				except ObjectDoesNotExist:
					pass
		template = loader.get_template("admin/izin/izin/wizard_iujk.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))
	else:
		messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
		return HttpResponseRedirect(reverse('admin:add_wizard_izin'))
