from formtools.wizard.views import SessionWizardView
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse


from master.models import Negara, JenisPemohon
from izin.models import JenisPermohonanIzin
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

	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
		template = loader.get_template("admin/izin/izin/wizard_iujk.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))
	else:
		messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
		return HttpResponseRedirect(reverse('admin:add_wizard_izin'))
	
	# if 'id_kelompok_izin' in request.COOKIES.keys():
	# 	extra_context.update({'title': 'SIUP Baru'})
	# 	negara = Negara.objects.all()
	# 	jenis_pemohon = JenisPemohon.objects.all()
	# 	bentuk_kegiatan_usaha_list = BentukKegiatanUsaha.objects.all()
	# 	jenis_penanaman_modal_list = JenisPenanamanModal.objects.all()
	# 	kelembagaan_list = Kelembagaan.objects.all()
	# 	kbli_list = KBLI.objects.all()
	# 	produk_utama_list = ProdukUtama.objects.all()
	# 	jenis_legalitas_list = JenisLegalitas.objects.all()

	# 	jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) # Untuk SIUP
	# 	extra_context.update({'negara': negara})
	# 	extra_context.update({'jenis_pemohon': jenis_pemohon})
	# 	# print request.COOKIES
	# 	extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	# 	extra_context.update({'bentuk_kegiatan_usaha_list': bentuk_kegiatan_usaha_list})
	# 	extra_context.update({'jenis_penanaman_modal_list': jenis_penanaman_modal_list})
	# 	extra_context.update({'kelembagaan_list': kelembagaan_list})
	# 	extra_context.update({'kbli_list': kbli_list})
	# 	extra_context.update({'produk_utama_list': produk_utama_list})
	# 	extra_context.update({'jenis_legalitas_list': jenis_legalitas_list})

	# 	# extra_context jika cookie masih ada
	# 	# konfirmasi_ec_pemohon = Pemohon.objects.filter(id=request.COOKIES['id_pemohon'])
	# 	# if request.COOKIES['id_detail_siup'] is not None:
	# 	#konfirmasi_ec_detilsiup = DetilSIUP.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
	# 	#extra_context.update({'konfirmasi_ec_detilsiup': konfirmasi_ec_detilsiup})
	# 	template = loader.get_template("admin/izin/izin/form_wizard_siup.html")
	# 	# template = loader.get_template("admin/izin/izin/izin_baru_form_pemohon.html")
	# 	ec = RequestContext(request, extra_context)
	# 	return HttpResponse(template.render(ec))
	# else:
	# 	messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
	# 	return HttpResponseRedirect(reverse('admin:add_wizard_izin'))