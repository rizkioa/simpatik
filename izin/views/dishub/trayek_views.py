import json, os, datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from izin.models import DetilIUA, DetilTrayek, JenisPemohon, KategoriKendaraan, MerkTypeKendaraan, JenisPermohonanIzin
from master.models import Negara, Kecamatan
from izin.utils import get_tahun_choices
from accounts.utils import KETERANGAN_PEKERJAAN

def load_izin_iua(request):
	nomor_izin_iua = request.POST.get('nomor_izin_iua')
	if nomor_izin_iua and nomor_izin_iua is not None:
		data = {'success': False, 'pesan': 'Data tidak ditemukan'}
		detil_iua = DetilIUA.objects.filter(no_izin=nomor_izin_iua).last()
		if detil_iua and detil_iua is not None:
			pengajuan_obj = DetilTrayek.objects.filter(id=request.COOKIES['id_pengajuan']).last()
			# print pengajuan_obj
			detil_iua_no_izin = detil_iua.no_izin
			data = {'success': True, 'pesan': 'No Izin Terdaftar.', 'data': detil_iua}

		data = json.dumps(data)
		response = HttpResponse(data)
		return response
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Nomor Izin Gangguan tidak ditemukan'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def formulir_izin_angkutan_trayek(request, extra_context={}):
    negara = Negara.objects.all()
    jenis_pemohon = JenisPemohon.objects.all()
    katogri_kendaraan_list = KategoriKendaraan.objects.all()
    merk_type_list = MerkTypeKendaraan.objects.all()
    extra_context.update({
        'negara':negara,
        'kecamatan_perusahaan': Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35'),
        'jenis_pemohon':jenis_pemohon,
        'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
        'kategori_kendaraan':katogri_kendaraan_list,
        'merk_type' : merk_type_list,
        'tahun_choices': get_tahun_choices(1945),
        })
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '0':
            # print request.COOKIES['id_pengajuan']
            try:
                pengajuan_ = DetilTrayek.objects.get(id=request.COOKIES['id_pengajuan'])
                extra_context.update({'pengajuan_': pengajuan_})
                extra_context.update({'pengajuan_id': pengajuan_.id})
                if pengajuan_.pemohon:
                    ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
                    extra_context.update({ 'ktp': ktp_ })
                    paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
                    extra_context.update({ 'paspor': paspor_ })
            except ObjectDoesNotExist:
                extra_context.update({'pengajuan_id': '0'})

    if 'id_kelompok_izin' in request.COOKIES.keys():
        jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
        extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
    else:
        return HttpResponseRedirect(reverse('layanan'))
    return render(request, "front-end/formulir/izin_angkutan_trayek.html", extra_context)