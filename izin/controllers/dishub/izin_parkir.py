from django.contrib import messages
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect

from izin.models import DetilTDUP, BidangUsahaPariwisata, JenisPermohonanIzin, JenisPemohon
from master.models import Negara, Provinsi, Kabupaten, Kecamatan
from accounts.models import NomorIdentitasPengguna

def formulir_tdup(request):
	extra_context={}
	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
		extra_context.update({'title': 'Izin Parkir'})
		negara = Negara.objects.all()
		provinsi = Provinsi.objects.all()
		kabupaten = Kabupaten.objects.all()
		kecamatan = Kecamatan.objects.all()
		jenis_pemohon = JenisPemohon.objects.all()
		bidang_usaha_pariwisata_list = BidangUsahaPariwisata.objects.all()
		extra_context.update({'bidang_usaha_pariwisata': bidang_usaha_pariwisata_list, 'negara':negara, 'provinsi':provinsi, 'kabupaten':kabupaten, 'kecamatan':kecamatan, 'jenis_pemohon':jenis_pemohon})
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan'] != '0' and request.COOKIES['id_pengajuan'] != '':
				try:
					pengajuan_ = DetilTDUP.objects.get(id=request.COOKIES['id_pengajuan'])
					extra_context.update({'pengajuan_': pengajuan_})
					extra_context.update({'pengajuan_id': pengajuan_.id})
					if pengajuan_.pemohon:
						ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
						extra_context.update({ 'ktp': ktp_ })
						paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
						extra_context.update({ 'paspor': paspor_ })
						template = loader.get_template("admin/izin/izin/form_wizard_tdup.html")
						ec = RequestContext(request, extra_context)
						response = HttpResponse(template.render(ec))
				except ObjectDoesNotExist:
					extra_context.update({'pengajuan_id': '0'})
					template = loader.get_template("admin/izin/izin/form_wizard_tdup.html")
					ec = RequestContext(request, extra_context)
					response = HttpResponse(template.render(ec))
			else:
				template = loader.get_template("admin/izin/izin/form_wizard_tdup.html")
				ec = RequestContext(request, extra_context)
				response = HttpResponse(template.render(ec))
		else:
			template = loader.get_template("admin/izin/izin/form_wizard_tdup.html")
			ec = RequestContext(request, extra_context)
			response = HttpResponse(template.render(ec))	
		return response
	else:
		messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
		return HttpResponseRedirect(reverse('admin:add_wizard_izin'))