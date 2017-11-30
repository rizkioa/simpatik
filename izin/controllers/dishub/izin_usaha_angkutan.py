from django.contrib import messages
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect

from izin.models import DetilIUA, Kendaraan, KategoriKendaraan, JenisPemohon, MerkTypeKendaraan, JenisPermohonanIzin
from master.models import Negara, Provinsi, Kabupaten, Kecamatan
from accounts.models import NomorIdentitasPengguna
from izin.utils import get_tahun_choices
from accounts.utils import KETERANGAN_PEKERJAAN

def formulir_iua(request):
	extra_context={}
	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
		extra_context.update({'title': 'Izin Usaha Angkutan'})
		negara = Negara.objects.all()
		provinsi = Provinsi.objects.all()
		kabupaten = Kabupaten.objects.all()
		kecamatan = Kecamatan.objects.all()
		jenis_pemohon = JenisPemohon.objects.all()
		katogri_kendaraan_list = KategoriKendaraan.objects.all()
		merk_type_list = MerkTypeKendaraan.objects.all()
		extra_context.update({
			'negara':negara, 
			'provinsi':provinsi, 
			'kabupaten':kabupaten, 
			'kecamatan':kecamatan,
			'kecamatan_perusahaan': kecamatan.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35'),
			'jenis_pemohon':jenis_pemohon,
			'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
			'kategori_kendaraan':katogri_kendaraan_list,
			'merk_type' : merk_type_list,
			'tahun_choices': get_tahun_choices(1945),
			})
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES.get('id_pengajuan', '0') != '0' and request.COOKIES['id_pengajuan'] != '':
				try:
					pengajuan_obj = DetilIUA.objects.get(id=request.COOKIES.get('id_pengajuan'))
					extra_context.update({'pengajuan_': pengajuan_obj})
					extra_context.update({'pengajuan_id': pengajuan_obj.id})
				except ObjectDoesNotExist:
					pass
		template = loader.get_template("admin/izin/izin/dishub/form_wizard_iua.html")
		ec = RequestContext(request, extra_context)
		response = HttpResponse(template.render(ec))	
		return response
	else:
		messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
		return HttpResponseRedirect(reverse('admin:add_wizard_izin'))