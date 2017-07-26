import json, os, datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from izin.models import DetilIUA, DetilTrayek, JenisPemohon, KategoriKendaraan, MerkTypeKendaraan, JenisPermohonanIzin, Kendaraan, Trayek
from master.models import Negara, Kecamatan, Berkas
from izin.utils import get_tahun_choices
from accounts.utils import KETERANGAN_PEKERJAAN
from izin.iua_forms import DataKendaraanForm

def load_izin_iua(request):
	data = {'success': False, 'pesan': 'Izin Angkutan tidak / belum terdaftar.'}
	response = HttpResponse(json.dumps(data))
	response.set_cookie(key='id_pengajuan_iua', value="0")
	nomor_izin_iua = request.POST.get('nomor_izin_iua')
	if nomor_izin_iua and nomor_izin_iua is not None:
		try:
			detil_iua = DetilIUA.objects.get(no_izin=nomor_izin_iua)
			if detil_iua.no_izin:
				data = {'success': True, 'pesan': 'No Izin Terdaftar.', 'data': {'no_izin': detil_iua.no_izin, 'nama_pemohon': detil_iua.pemohon.nama_lengkap, 'nama_perusahaan': detil_iua.perusahaan.nama_perusahaan}}
				response = HttpResponse(json.dumps(data))
				response.set_cookie(key='id_pengajuan_iua', value=detil_iua.id)
				if detil_iua.no_izin:
					response.set_cookie(key='no_izin_iua', value=detil_iua.no_izin)
				if detil_iua.perusahaan:
					response.set_cookie(key='npwp_perusahaan', value=detil_iua.perusahaan.npwp)
				if detil_iua.pemohon:
					if detil_iua.pemohon.get_ktp():
						response.set_cookie(key='nomor_ktp', value=detil_iua.pemohon.get_ktp())
		except ObjectDoesNotExist:
			pass
	return response

def formulir_izin_angkutan_trayek(request, extra_context={}):
	negara = Negara.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	katogri_kendaraan_list = KategoriKendaraan.objects.all()
	merk_type_list = MerkTypeKendaraan.objects.all()
	trayek_list = Trayek.objects.all()
	extra_context.update({
		'trayek_list': trayek_list,
		'negara':negara,
		'kecamatan_perusahaan': Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35'),
		'jenis_pemohon':jenis_pemohon,
		'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
		'kategori_kendaraan':katogri_kendaraan_list,
		'merk_type' : merk_type_list,
		'tahun_choices': get_tahun_choices(1945),
		})
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0' and request.COOKIES['id_pengajuan'] != '':
			print request.COOKIES['id_pengajuan']
			try:
				pengajuan_ = DetilTrayek.objects.get(id=request.COOKIES['id_pengajuan'])
				# print pengajuan_
				extra_context.update({'pengajuan_': pengajuan_})
				extra_context.update({'pengajuan_id': pengajuan_.id})
			except ObjectDoesNotExist:
				extra_context.update({'pengajuan_id': '0'})

	if 'id_kelompok_izin' in request.COOKIES.keys():
		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin'])
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
	else:
		return HttpResponseRedirect(reverse('layanan'))
	return render(request, "front-end/formulir/izin_angkutan_trayek.html", extra_context)

def save_data_kendaraan_trayek(request):
	data = {'success': False, 'pesan': 'Data Kendaraan gagal disimpan.'}
	data = json.dumps(data)
	response = HttpResponse(data)
	# print request.POST.get('id_kendaraan')
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			try:
				pengajuan_obj = DetilTrayek.objects.get(id=request.COOKIES['id_pengajuan'])
				if pengajuan_obj:
					# kendaraan_obj = Kendaraan.objects.none()
					data_kendaraan_form = DataKendaraanForm(request.POST)
					if request.POST.get('id_kendaraan'):
						try:
							kendaraan_obj = Kendaraan.objects.get(id=request.POST.get('id_kendaraan'))
							data_kendaraan_form = DataKendaraanForm(request.POST, instance=kendaraan_obj)
						except ObjectDoesNotExist:
							pass
					
					if data_kendaraan_form.is_valid():
						i = data_kendaraan_form.save(commit=False)
						i.pengajuan_izin_id = pengajuan_obj.id
						i.save()
						# ###########   berkas scan stnk #############
						if request.FILES.get('berkas_scan_stnk', None) and request.FILES.get('berkas_scan_stnk', None) is not None:
							berkas_stnk, created = Berkas.objects.get_or_create(id=i.berkas_stnk_id)
							berkas_stnk.berkas = request.FILES.get('berkas_scan_stnk')
							berkas_stnk.nama_berkas = "Berkas SCAN STNK Kendaraan "+pengajuan_obj.no_pengajuan
							berkas_stnk.keterangan = "scan_stnk"
							berkas_stnk.save()
							i.berkas_stnk_id = berkas_stnk.id
						# ########### 	berkas kartu pengawasan ###########
						if request.FILES.get('berkas_kartu_pengawasan', None) and request.FILES.get('berkas_kartu_pengawasan', None) is not None:
							berkas_kartu_pengawasan, created = Berkas.objects.get_or_create(id=i.berkas_kartu_pengawasan_id)
							berkas_kartu_pengawasan.berkas = request.FILES.get('berkas_kartu_pengawasan')
							berkas_kartu_pengawasan.nama_berkas = "Berkas Kartu Pengawasan "+pengajuan_obj.no_pengajuan
							berkas_kartu_pengawasan.keterangan = "kartu_pengawasan"
							berkas_kartu_pengawasan.save()
							i.berkas_kartu_pengawasan_id = berkas_kartu_pengawasan.id
						i.save()
						data = {'success': True, 'pesan': 'Data Kendaraan berhasil disimpan.'}
						data = json.dumps(data)
						response = HttpResponse(data)
					else:
						data = data_kendaraan_form.errors.as_json()
						response = HttpResponse(data)
			except ObjectDoesNotExist:
				pass
	return response

def delete_berkas_kendaraan(request):
	id_kendaraan = request.GET.get('id_kendaraan', None)
	id_berkas = request.GET.get('id_berkas', None)
	jenis = request.GET.get('jenis', None)
	data = {'success': False, 'pesan': 'Data Kendaraan tidak ditemukan.'}
	if id_kendaraan and id_berkas and jenis:
		try:
			kendaraan_obj = Kendaraan.objects.get(id=id_kendaraan)
			if jenis == "scan_stnk":
				if kendaraan_obj.berkas_stnk:
					kendaraan_obj.berkas_stnk.delete()
					kendaraan_obj.berkas_stnk = None
			elif jenis == "kartu_pengawasan":
				if kendaraan_obj.berkas_kartu_pengawasan:
					kendaraan_obj.berkas_kartu_pengawasan.delete()
					kendaraan_obj.berkas_kartu_pengawasan = None
			kendaraan_obj.save()
			data = {'success': True, 'pesan': 'Berkas berhasil dihapus.', 'jenis':jenis}
		except ObjectDoesNotExist:
			pass
	response = HttpResponse(json.dumps(data))
	return response

def ajax_load_berkas_trayek(request, id_pengajuan):
	url_berkas = []
	id_elemen = []
	nm_berkas = []
	id_berkas = []
	data = {'success': False, 'pesan': "Terjadi Kesalahan. Data tidak ditemukan." }
	if id_pengajuan:
		try:
			trayek_obj = DetilTrayek.objects.get(id=id_pengajuan)

			if trayek_obj.perusahaan:
				npwp_perusahaan = trayek_obj.perusahaan.berkas_npwp
				if npwp_perusahaan:
					url_berkas.append(npwp_perusahaan.berkas.url)
					id_elemen.append('npwp_perusahaan')
					nm_berkas.append(npwp_perusahaan.nama_berkas)
					id_berkas.append(npwp_perusahaan.id)
			if trayek_obj.pemohon:
				berkas_ktp = trayek_obj.pemohon.get_berkas_ktp()
				if berkas_ktp:
					url_berkas.append(berkas_ktp.berkas.url)
					id_elemen.append('ktp')
					nm_berkas.append(berkas_ktp.nama_berkas)
					id_berkas.append(berkas_ktp.id)
			data = {'success': True, 'pesan': 'Berkas berhasil diload.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			pass
	return HttpResponse(json.dumps(data))