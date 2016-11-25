from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib import messages


from master.models import Negara, JenisPemohon, Kecamatan
from izin.models import JenisPermohonanIzin, PaketPekerjaan
from izin.utils import JENIS_IUJK, get_tahun_choices
from perusahaan.models import BentukKegiatanUsaha, JenisPenanamanModal, Kelembagaan, KBLI, ProdukUtama, JenisLegalitas


def IUJKWizard(request, extra_context={}):
	extra_context.update({'title': 'Formulir IUJK'})
	extra_context.update({'has_permission': True})
	extra_context.update({'negara': Negara.objects.all()})
	extra_context.update({'jenis_pemohon': JenisPemohon.objects.all()})
	extra_context.update({'bentuk_kegiatan_usaha_list': BentukKegiatanUsaha.objects.all()})
	extra_context.update({'jenis_penanaman_modal_list': JenisPenanamanModal.objects.all()})
	extra_context.update({'kelembagaan_list': Kelembagaan.objects.all()})
	extra_context.update({'kbli_list': KBLI.objects.all()})
	extra_context.update({'produk_utama_list': ProdukUtama.objects.all()})
	extra_context.update({'jenis_legalitas_list': JenisLegalitas.objects.all()})
	extra_context.update({'jenis_iujk': JENIS_IUJK })
	extra_context.update({'tahun_choices': get_tahun_choices(1945) })
	extra_context.update({'kecamatan_perusahaan': Kecamatan.objects.filter(kabupaten=1) })

	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan'] != "":
				extra_context.update({'paketpekerjaan_list': PaketPekerjaan.objects.filter(detil_iujk_id=request.COOKIES['id_pengajuan'])})
		template = loader.get_template("admin/izin/izin/wizard_iujk.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))
	else:
		messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
		return HttpResponseRedirect(reverse('admin:add_wizard_izin'))
