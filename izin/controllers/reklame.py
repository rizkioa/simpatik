from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib import messages

from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon, JenisReklame
from perusahaan.models import BentukKegiatanUsaha, JenisPenanamanModal, Kelembagaan, KBLI, ProdukUtama, JenisLegalitas
from izin.models import PengajuanIzin, JenisPermohonanIzin, KelompokJenisIzin, Pemohon, DetilSIUP

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

		# extra_context jika cookie masih ada
		# konfirmasi_ec_pemohon = Pemohon.objects.filter(id=request.COOKIES['id_pemohon'])
		# if request.COOKIES['id_detail_siup'] is not None:
		#konfirmasi_ec_detilsiup = DetilSIUP.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
		#extra_context.update({'konfirmasi_ec_detilsiup': konfirmasi_ec_detilsiup})
		template = loader.get_template("admin/izin/izin/form_wizard_reklame.html")
		# template = loader.get_template("admin/izin/izin/izin_baru_form_pemohon.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))
	else:
		messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
		return HttpResponseRedirect(reverse('admin:add_wizard_izin'))