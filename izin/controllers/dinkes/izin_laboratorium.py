from django.contrib import messages
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, resolve

from izin.models import DetilIzinParkirIsidentil, JenisPermohonanIzin, JenisPemohon
from master.models import Negara, Provinsi, Kabupaten, Kecamatan
from accounts.models import NomorIdentitasPengguna

def formulir_izin_laboratorium(request):
	extra_context={}
	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
		extra_context.update({'title': 'Izin Laboratorium'})
		negara = Negara.objects.all()
		provinsi = Provinsi.objects.all()
		kabupaten = Kabupaten.objects.all()
		kecamatan = Kecamatan.objects.all()
		jenis_pemohon = JenisPemohon.objects.all()
		extra_context.update({'negara':negara, 'provinsi':provinsi, 'kabupaten':kabupaten, 'kecamatan':kecamatan, 'jenis_pemohon':jenis_pemohon})
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES.get('id_pengajuan', None) is not None and request.COOKIES.get('id_pengajuan') != '0':
				try:
					pengajuan_obj = DetilIzinParkirIsidentil.objects.get(id=request.COOKIES.get('id_pengajuan'))
					extra_context.update({'pengajuan_': pengajuan_obj})
					extra_context.update({'pengajuan_id': pengajuan_obj.id})
				except ObjectDoesNotExist:
					pass
		template = loader.get_template("admin/izin/izin/dinkes/form_wizard_izin_laboratorium.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))
	else:
		messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
		return HttpResponseRedirect(reverse('admin:add_wizard_izin'))