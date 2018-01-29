import os
import json
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from master.models import Negara, Kecamatan, Berkas
from izin_dinkes.forms import ApotekForm, TokoObatForm, LaboratoriumForm, PeralatanLaboratoriumForm, OptikalForm, MendirikanKlinikForm, OperasionalKlinikForm, PenutupanApotekForm
from izin_dinkes.models import Apotek, Sarana, TokoObat, Laboratorium, PeralatanLaboratorium, BangunanLaboratorium, Optikal, MendirikanKlinik, OperasionalKlinik, PenutupanApotek, PengunduranApoteker, JenisKlinik
from izin.izin_forms import BerkasForm
from izin.models import PengajuanIzin, JenisPemohon, JenisPermohonanIzin
from accounts.utils import KETERANGAN_PEKERJAAN

def formulir_izin_apotek(request, extra_context={}):
	negara = Negara.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	sarana_list = Sarana.objects.all()
	extra_context.update({
		'sarana_list': sarana_list,
		'negara':negara,
		'kecamatan': Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35'),
		'jenis_pemohon':jenis_pemohon,
		'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
		})
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0' and request.COOKIES['id_pengajuan'] != '':
			print request.COOKIES['id_pengajuan']
			try:
				pengajuan_ = Apotek.objects.get(id=request.COOKIES['id_pengajuan'])
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
	return render(request, "front-end/formulir/dinkes/izin_apotek.html", extra_context)

def cetak_izin_apotek(request, id_pengajuan):
	extra_context = {}
	if id_pengajuan:
		print id_pengajuan
		pengajuan_ = get_object_or_404(Apotek, id=id_pengajuan)
		print pengajuan_
		if pengajuan_:
			extra_context.update({'pengajuan': pengajuan_})
	return render(request, "front-end/include/formulir_izin_apotik/cetak.html", extra_context)

def cetak_bukti_pendaftaran_izin_apotek(request, id_pengajuan):
	extra_context = {}
	extra_context.update({'formulir_judul': 'FORMULIR PENDAFTARAN IZIN APOTEK'})
	if id_pengajuan:
		pengajuan_ = get_object_or_404(Apotek, id=id_pengajuan)
		if pengajuan_:
			# sarana_list = Sarana.objects.filter(apotek_id=pengajuan_.id)
			extra_context.update({'pengajuan_':pengajuan_})
	return render(request, "front-end/include/formulir_izin_apotik/cetak_bukti_pendaftaran.html", extra_context)

def formulir_izin_toko_obat(request, extra_context={}):
	negara = Negara.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({
		'negara':negara,
		'kecamatan': Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35'),
		'jenis_pemohon':jenis_pemohon,
		'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
		})
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0' and request.COOKIES['id_pengajuan'] != '':
			try:
				pengajuan_ = TokoObat.objects.get(id=request.COOKIES['id_pengajuan'])
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
	return render(request, "front-end/formulir/dinkes/izin_toko_obat.html", extra_context)

def cetak_izin_toko_obat(request, id_pengajuan):
	extra_context = {}
	if id_pengajuan:
		pengajuan_ = get_object_or_404(TokoObat, id=id_pengajuan)
		if pengajuan_:
			extra_context.update({'pengajuan': pengajuan_})
	return render(request, "front-end/include/formulir_izin_toko_obat/cetak.html", extra_context)

def cetak_bukti_pendaftaran_izin_toko_obat(request, id_pengajuan):
	extra_context = {}
	extra_context.update({'formulir_judul': 'FORMULIR PENDAFTARAN IZIN TOKO OBAT'})
	if id_pengajuan:
		pengajuan_ = get_object_or_404(TokoObat, id=id_pengajuan)
		if pengajuan_:
			# sarana_list = Sarana.objects.filter(apotek_id=pengajuan_.id)
			extra_context.update({'pengajuan_':pengajuan_})
	return render(request, "front-end/include/formulir_izin_toko_obat/cetak_bukti_pendaftaran.html", extra_context)

def formulir_izin_optikal(request, extra_context={}):
	negara = Negara.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({
		'negara':negara,
		'kecamatan': Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35'),
		'jenis_pemohon':jenis_pemohon,
		'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
		})
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0' and request.COOKIES['id_pengajuan'] != '':
			try:
				pengajuan_ = Optikal.objects.get(id=request.COOKIES['id_pengajuan'])
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
	return render(request, "front-end/formulir/dinkes/izin_optikal.html", extra_context)

def cetak_izin_optikal(request, id_pengajuan):
	extra_context = {}
	if id_pengajuan:
		pengajuan_ = get_object_or_404(Optikal, id=id_pengajuan)
		if pengajuan_:
			extra_context.update({'pengajuan': pengajuan_})
	return render(request, "front-end/include/formulir_izin_optikal/cetak.html", extra_context)

def cetak_bukti_pendaftaran_izin_optikal(request, id_pengajuan):
	extra_context = {}
	extra_context.update({'formulir_judul': 'FORMULIR PENDAFTARAN IZIN OPTIKAL'})
	if id_pengajuan:
		pengajuan_ = get_object_or_404(Optikal, id=id_pengajuan)
		if pengajuan_:
			# sarana_list = Sarana.objects.filter(apotek_id=pengajuan_.id)
			extra_context.update({'pengajuan_':pengajuan_})
	return render(request, "front-end/include/formulir_izin_optikal/cetak_bukti_pendaftaran.html", extra_context)

def formulir_izin_laboratorium(request, extra_context={}):
	negara = Negara.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({
		'negara':negara,
		'kecamatan': Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35'),
		'jenis_pemohon':jenis_pemohon,
		'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
		})
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0' and request.COOKIES['id_pengajuan'] != '':
			try:
				pengajuan_ = Laboratorium.objects.get(id=request.COOKIES['id_pengajuan'])
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
	return render(request, "front-end/formulir/dinkes/izin_laboratorium.html", extra_context)

def cetak_izin_laboratorium(request, id_pengajuan):
	extra_context = {}
	if id_pengajuan:
		pengajuan_ = get_object_or_404(Laboratorium, id=id_pengajuan)
		if pengajuan_:
			extra_context.update({'pengajuan': pengajuan_})
	return render(request, "front-end/include/formulir_izin_laboratorium/cetak.html", extra_context)

def cetak_bukti_pendaftaran_izin_laboratorium(request, id_pengajuan):
	extra_context = {}
	extra_context.update({'formulir_judul': 'FORMULIR PENDAFTARAN IZIN LABORATORIUM'})
	if id_pengajuan:
		pengajuan_ = get_object_or_404(Laboratorium, id=id_pengajuan)
		if pengajuan_:
			peralatan_list = PeralatanLaboratorium.objects.filter(laboratorium_id=pengajuan_.id)
			bangunan_list = BangunanLaboratorium.objects.filter(laboratorium_id=pengajuan_.id)
			extra_context.update({'pengajuan_':pengajuan_, 'peralatan_list':peralatan_list, 'bangunan_list':bangunan_list})
	return render(request, "front-end/include/formulir_izin_laboratorium/cetak_bukti_pendaftaran.html", extra_context)

def formulir_izin_penutupan_apotek(request, extra_context={}):
	negara = Negara.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({
		'negara':negara,
		'kecamatan': Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35'),
		'jenis_pemohon':jenis_pemohon,
		'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
		})
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0' and request.COOKIES['id_pengajuan'] != '':
			try:
				pengajuan_ = PenutupanApotek.objects.get(id=request.COOKIES['id_pengajuan'])
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
	return render(request, "front-end/formulir/dinkes/izin_penutupan_apotek.html", extra_context)

def cetak_izin_penutupan_apotek(request, id_pengajuan):
	extra_context = {}
	if id_pengajuan:
		pengajuan_ = get_object_or_404(PenutupanApotek, id=id_pengajuan)
		if pengajuan_:
			extra_context.update({'pengajuan': pengajuan_})
	return render(request, "front-end/include/formulir_izin_penutupan_apotek/cetak.html", extra_context)

def cetak_bukti_pendaftaran_izin_penutupan_apotek(request, id_pengajuan):
	extra_context = {}
	extra_context.update({'formulir_judul': 'FORMULIR PENDAFTARAN IZIN LABORATORIUM'})
	if id_pengajuan:
		pengajuan_ = get_object_or_404(PenutupanApotek, id=id_pengajuan)
		if pengajuan_:
			pengunduran_list = PengunduranApoteker.objects.filter(nama_apotek_id=pengajuan_.id)
			extra_context.update({'pengajuan_':pengajuan_})
	return render(request, "front-end/include/formulir_izin_penutupan_apotek/cetak_bukti_pendaftaran.html", extra_context)


def formulir_izin_mendirikan_klinik(request, extra_context={}):
	negara = Negara.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	jenis_klinik = JenisKlinik.objects.all()
	extra_context.update({
		'negara':negara,
		'kecamatan': Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35'),
		'jenis_pemohon':jenis_pemohon,
		'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
		'jenis_klinik': jenis_klinik,
		})
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0' and request.COOKIES['id_pengajuan'] != '':
			try:
				pengajuan_ = MendirikanKlinik.objects.get(id=request.COOKIES['id_pengajuan'])
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
	return render(request, "front-end/formulir/dinkes/izin_mendirikan_klinik.html", extra_context)

def cetak_izin_mendirikan_klinik(request, id_pengajuan):
	extra_context = {}
	if id_pengajuan:
		pengajuan_ = get_object_or_404(MendirikanKlinik, id=id_pengajuan)
		if pengajuan_:
			extra_context.update({'pengajuan': pengajuan_})
	return render(request, "front-end/include/formulir_mendirikan_klinik/cetak.html", extra_context)

def cetak_bukti_pendaftaran_izin_mendirikan_klinik(request, id_pengajuan):
	extra_context = {}
	extra_context.update({'formulir_judul': 'FORMULIR PENDAFTARAN IZIN MENDIRIKAN KLINIK'})
	if id_pengajuan:
		pengajuan_ = get_object_or_404(MendirikanKlinik, id=id_pengajuan)
		if pengajuan_:
			extra_context.update({'pengajuan_':pengajuan_})
	return render(request, "front-end/include/formulir_mendirikan_klinik/cetak_bukti_pendaftaran.html", extra_context)

def formulir_izin_operasional_klinik(request, extra_context={}):
	negara = Negara.objects.all()
	jenis_pemohon = JenisPemohon.objects.all()
	jenis_klinik = JenisKlinik.objects.all()
	extra_context.update({
		'negara':negara,
		'kecamatan': Kecamatan.objects.filter(kabupaten__kode='06', kabupaten__provinsi__kode='35'),
		'jenis_pemohon':jenis_pemohon,
		'keterangan_pekerjaan': KETERANGAN_PEKERJAAN,
		'jenis_klinik': jenis_klinik,
		})
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0' and request.COOKIES['id_pengajuan'] != '':
			try:
				pengajuan_ = OperasionalKlinik.objects.get(id=request.COOKIES['id_pengajuan'])
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
	return render(request, "front-end/formulir/dinkes/izin_operasional_klinik.html", extra_context)

def cetak_izin_operasional_klinik(request, id_pengajuan):
	extra_context = {}
	if id_pengajuan:
		pengajuan_ = get_object_or_404(OperasionalKlinik, id=id_pengajuan)
		if pengajuan_:
			extra_context.update({'pengajuan': pengajuan_})
	return render(request, "front-end/include/formulir_operasional_klinik/cetak.html", extra_context)

def cetak_bukti_pendaftaran_izin_operasional_klinik(request, id_pengajuan):
	extra_context = {}
	extra_context.update({'formulir_judul': 'FORMULIR PENDAFTARAN IZIN OPERASIONAL KLINIK'})
	if id_pengajuan:
		pengajuan_ = get_object_or_404(OperasionalKlinik, id=id_pengajuan)
		if pengajuan_:
			extra_context.update({'pengajuan_':pengajuan_})
	return render(request, "front-end/include/formulir_operasional_klinik/cetak_bukti_pendaftaran.html", extra_context)
# ================================================================================================================
def save_izin_apotek(request):
	data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
	if 'id_pengajuan' in request.COOKIES.keys():
		print request.COOKIES['id_pengajuan']	
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				try:
					pengajuan_obj = Apotek.objects.get(id=request.COOKIES['id_pengajuan'])
					form_apotek = ApotekForm(request.POST, instance=pengajuan_obj)
					if form_apotek.is_valid():
						p = form_apotek.save(commit=False)
						p.save()
						data = {'success': True, 'pesan': 'Data Izin Apotek berhasil tersimpan.'}
					else:
						data = form_apotek.errors.as_json()
						data = {'success': False, 'pesan': 'Data Izin Apotek gagal.', 'data': data}
				except Apotek.DoesNotExist:
					pass
	return HttpResponse(json.dumps(data))

def load_izin_apotek(request, id_pengajuan):
	data = {}
	response = {'success': False, 'pesan': 'Data Apotek berhasil tersimpan.', 'data': data}
	if id_pengajuan:
		pengajuan_obj = Apotek.objects.filter(id=id_pengajuan).last()
		if pengajuan_obj:
			data = pengajuan_obj.as_json()
			response = {'success': True, 'pesan': 'Data Apotek berhasil tersimpan.', 'data': data}
	return HttpResponse(json.dumps(response))

def save_izin_toko_obat(request):
	data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES.get('id_pengajuan') != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				try:
					pengajuan_obj = TokoObat.objects.get(id=request.COOKIES.get('id_pengajuan'))
					pengajuan_obj.nama_toko_obat = request.POST.get("nama_toko_obat")
					pengajuan_obj.nama_ttk_penanggung_jawab = request.POST.get("nama_ttk_penanggung_jawab")
					pengajuan_obj.alamat_ttk = request.POST.get("alamat_ttk")
					pengajuan_obj.alamat_tempat_usaha = request.POST.get("alamat_tempat_usaha")
					pengajuan_obj.save()
					data = {'success':True, 'pesan': 'Data izin toko obat berhasil disimpan.'}
				except ObjectDoesNotExist:
					data = {'success': False, 'pesan': 'Proses simpaan data izin toko obat terjadi kesalahan.', 'data': ""}
				# if pengajuan_obj:
				# 	form_ = TokoObatForm(request.POST, instance=pengajuan_obj)
				# 	if form_.is_valid():
				# 		p = form_.save(commit=False)
				# 		p.save()
				# 		data = {'success': True, 'pesan': 'Data Izin Apotek berhasil tersimpan.'}
				# 	else:
				# 		data_error = form_apotek.errors.as_json()
				# 		data = {'success': False, 'pesan': 'Data Izin Apotek gagal.', 'data': data_error}
	return HttpResponse(json.dumps(data))

def upload_berkas_toko_obat(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			form = BerkasForm(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if berkas_._size > 4*1024*1024:
				data = {'Terjadi Kesalahan': [{'message': 'Ukuran file tidak boleh melebihi dari 4mb.'}]}
				data = json.dumps(data)
				response = HttpResponse(data)
			else:
				if request.method == "POST":
					if berkas_:
						if form.is_valid():
							ext = os.path.splitext(berkas_.name)[1]
							valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.jpeg', '.png', '.PDF', '.DOC', '.DOCX', '.JPG', '.JPEG', '.PNG']
							if not ext in valid_extensions:
								data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
								data = json.dumps(data)
								response = HttpResponse(data)
							else:
								try:
									p = TokoObat.objects.get(id=request.COOKIES.get('id_pengajuan'))
									berkas = form.save(commit=False)
									kode = request.POST.get('kode')
									if kode == 'Ijazah STRTTK':
										berkas.nama_berkas = "Ijazah STRTTK "+p.no_pengajuan
										berkas.keterangan = "Ijazah STRTTK "+p.no_pengajuan
									elif kode == 'Denah Lokasi':
										berkas.nama_berkas = "Denah Lokasi "+p.no_pengajuan
										berkas.keterangan = "Denah Lokasi "+p.no_pengajuan
									elif kode == 'Denah Bangunan':
										berkas.nama_berkas = "Denah Bangunan "+p.no_pengajuan
										berkas.keterangan = "Denah Bangunan "+p.no_pengajuan
									elif kode == 'KTP':
										berkas.nama_berkas = "KTP "+p.pemohon.get_ktp()
										berkas.keterangan = "KTP "+p.pemohon.get_ktp()
									elif kode == 'Status Bangunan':
										berkas.nama_berkas = "Surat yang mengatakan status bangunan dalam bentuk akta hak milik/sewa/kontrak "+p.no_pengajuan
										berkas.keterangan = "Surat yang mengatakan status bangunan dalam bentuk akta hak milik/sewa/kontrak "+p.no_pengajuan
									elif kode == 'IMB dan Izin Gangguan':
										berkas.nama_berkas = "IMB dan Izin Gangguan "+p.no_pengajuan
										berkas.keterangan = "IMB dan Izin Gangguan "+p.no_pengajuan
									elif kode == 'Akte Perjanjian Kerjasama':
										berkas.nama_berkas = "Akte Perjanjian Kerjasama Tenaga Teknis Kefarmasian dengan Pemilik Sarana "+p.no_pengajuan
										berkas.keterangan = "Akte Perjanjian Kerjasama Tenaga Teknis Kefarmasian dengan Pemilik Sarana "+p.no_pengajuan
									elif kode == 'Pernyataan dari Tenaga Teknis':
										berkas.nama_berkas = "Surat Pernyataan dari Tenaga Teknis Kefarmasian sebagai Penanggung jawab teknis (bermaterai) "+p.no_pengajuan
										berkas.keterangan = "Surat Pernyataan dari Tenaga Teknis Kefarmasian sebagai Penanggung jawab teknis (bermaterai) "+p.no_pengajuan
									elif kode == 'Surat Pernyataan Peraturan':
										berkas.nama_berkas = "Surat Tenaga Teknis Kefarmasian dan Pemilik Sarana bersedia mematuhi Peraturan Perundang undangan yang berlaku "+p.no_pengajuan
										berkas.keterangan = "Surat Tenaga Teknis Kefarmasian dan Pemilik Sarana bersedia mematuhi Peraturan Perundang undangan yang berlaku "+p.no_pengajuan
									elif kode == 'Pernyataan Pelanggaran':
										berkas.nama_berkas = "Surat Tenaga Teknis Kefarmasian dan Pemilik Sarana tidak terlibat pelanggaran Peraturan Perundang undangan yang berlaku dibidang obat "+p.no_pengajuan
										berkas.keterangan = "Surat Tenaga Teknis Kefarmasian dan Pemilik Sarana tidak terlibat pelanggaran Peraturan Perundang undangan yang berlaku dibidang obat "+p.no_pengajuan
									elif kode == 'Rekomendasi Organisasi':
										berkas.nama_berkas = "Rekomendasi dari organisasi profesi PAFI untuk asisten Apoteker Penanggung jawab Toko Obat "+p.no_pengajuan
										berkas.keterangan = "Rekomendasi dari organisasi profesi PAFI untuk asisten Apoteker Penanggung jawab Toko Obat "+p.no_pengajuan
									if request.user.is_authenticated():
										berkas.created_by_id = request.user.id
									else:
										berkas.created_by_id = request.COOKIES['id_pemohon']
									berkas.save()
									p.berkas_terkait_izin.add(berkas)

									data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
											{'status_upload': 'ok'},
										]}
									data = json.dumps(data)
									response = HttpResponse(data)
								except ObjectDoesNotExist:
									data = {'Terjadi Kesalahan': [{'message': 'Pengajuan tidak ada dalam daftar'}]}
									data = json.dumps(data)
									response = HttpResponse(data)
						else:
							data = form.errors.as_json()
							response = HttpResponse(data)
					else:
						data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong'}]}
						data = json.dumps(data)
						response = HttpResponse(data)
				else:
					data = form.errors.as_json()
					response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def load_berkas_toko_obat(request, id_pengajuan):
	url_berkas = []
	id_elemen = []
	nm_berkas =[]
	id_berkas =[]
	if id_pengajuan:
		try:
			pengajuan_obj = TokoObat.objects.get(id=id_pengajuan)
			berkas_ = pengajuan_obj.berkas_terkait_izin.all()

			if berkas_:
				ijazah_strttk = berkas_.filter(keterangan="Ijazah STRTTK "+pengajuan_obj.no_pengajuan).last()
				if ijazah_strttk:
					url_berkas.append(ijazah_strttk.berkas.url)
					id_elemen.append('ijazah_strttk')
					nm_berkas.append(ijazah_strttk.nama_berkas)
					id_berkas.append(ijazah_strttk.id)
					pengajuan_obj.berkas_terkait_izin.add(ijazah_strttk)

				denah_lokasi = berkas_.filter(keterangan="Denah Lokasi "+pengajuan_obj.no_pengajuan).last()
				if denah_lokasi:
					url_berkas.append(denah_lokasi.berkas.url)
					id_elemen.append('denah_lokasi')
					nm_berkas.append(denah_lokasi.nama_berkas)
					id_berkas.append(denah_lokasi.id)
					pengajuan_obj.berkas_terkait_izin.add(denah_lokasi)

				denah_bangunan = berkas_.filter(keterangan="Denah Bangunan "+pengajuan_obj.no_pengajuan).last()
				if denah_bangunan:
					url_berkas.append(denah_bangunan.berkas.url)
					id_elemen.append('denah_bangunan')
					nm_berkas.append(denah_bangunan.nama_berkas)
					id_berkas.append(denah_bangunan.id)
					pengajuan_obj.berkas_terkait_izin.add(denah_bangunan)

				ktp = berkas_.filter(keterangan="KTP "+pengajuan_obj.pemohon.get_ktp()).last()
				if ktp:
					url_berkas.append(ktp.berkas.url)
					id_elemen.append('ktp')
					nm_berkas.append(ktp.nama_berkas)
					id_berkas.append(ktp.id)
					pengajuan_obj.berkas_terkait_izin.add(ktp)

				status_bangunan = berkas_.filter(keterangan="Surat yang mengatakan status bangunan dalam bentuk akta hak milik/sewa/kontrak "+pengajuan_obj.no_pengajuan).last()
				if status_bangunan:
					url_berkas.append(status_bangunan.berkas.url)
					id_elemen.append('status_bangunan')
					nm_berkas.append(status_bangunan.nama_berkas)
					id_berkas.append(status_bangunan.id)
					pengajuan_obj.berkas_terkait_izin.add(status_bangunan)

				izin_gangguan = berkas_.filter(keterangan="IMB dan Izin Gangguan "+pengajuan_obj.no_pengajuan).last()
				if izin_gangguan:
					url_berkas.append(izin_gangguan.berkas.url)
					id_elemen.append('izin_gangguan')
					nm_berkas.append(izin_gangguan.nama_berkas)
					id_berkas.append(izin_gangguan.id)
					pengajuan_obj.berkas_terkait_izin.add(izin_gangguan)

				perjanjian_kerjasama = berkas_.filter(keterangan="Akte Perjanjian Kerjasama Tenaga Teknis Kefarmasian dengan Pemilik Sarana "+pengajuan_obj.no_pengajuan).last()
				if perjanjian_kerjasama:
					url_berkas.append(perjanjian_kerjasama.berkas.url)
					id_elemen.append('perjanjian_kerjasama')
					nm_berkas.append(perjanjian_kerjasama.nama_berkas)
					id_berkas.append(perjanjian_kerjasama.id)
					pengajuan_obj.berkas_terkait_izin.add(perjanjian_kerjasama)

				pernyataan_tenaga_teknis = berkas_.filter(keterangan="Surat Pernyataan dari Tenaga Teknis Kefarmasian sebagai Penanggung jawab teknis (bermaterai) "+pengajuan_obj.no_pengajuan).last()
				if pernyataan_tenaga_teknis:
					url_berkas.append(pernyataan_tenaga_teknis.berkas.url)
					id_elemen.append('pernyataan_tenaga_teknis')
					nm_berkas.append(pernyataan_tenaga_teknis.nama_berkas)
					id_berkas.append(pernyataan_tenaga_teknis.id)
					pengajuan_obj.berkas_terkait_izin.add(pernyataan_tenaga_teknis)

				surat_pernyataan_peraturan = berkas_.filter(keterangan="Surat Tenaga Teknis Kefarmasian dan Pemilik Sarana bersedia mematuhi Peraturan Perundang undangan yang berlaku "+pengajuan_obj.no_pengajuan).last()
				if surat_pernyataan_peraturan:
					url_berkas.append(surat_pernyataan_peraturan.berkas.url)
					id_elemen.append('surat_pernyataan_peraturan')
					nm_berkas.append(surat_pernyataan_peraturan.nama_berkas)
					id_berkas.append(surat_pernyataan_peraturan.id)
					pengajuan_obj.berkas_terkait_izin.add(surat_pernyataan_peraturan)

				pernyataan_pelanggaran = berkas_.filter(keterangan="Surat Tenaga Teknis Kefarmasian dan Pemilik Sarana tidak terlibat pelanggaran Peraturan Perundang undangan yang berlaku dibidang obat "+pengajuan_obj.no_pengajuan).last()
				if pernyataan_pelanggaran:
					url_berkas.append(pernyataan_pelanggaran.berkas.url)
					id_elemen.append('pernyataan_pelanggaran')
					nm_berkas.append(pernyataan_pelanggaran.nama_berkas)
					id_berkas.append(pernyataan_pelanggaran.id)
					pengajuan_obj.berkas_terkait_izin.add(pernyataan_pelanggaran)

				rekomendasi_organisasi = berkas_.filter(keterangan="Rekomendasi dari organisasi profesi PAFI untuk asisten Apoteker Penanggung jawab Toko Obat "+pengajuan_obj.no_pengajuan).last()
				if rekomendasi_organisasi:
					url_berkas.append(rekomendasi_organisasi.berkas.url)
					id_elemen.append('rekomendasi_organisasi')
					nm_berkas.append(rekomendasi_organisasi.nama_berkas)
					id_berkas.append(rekomendasi_organisasi.id)
					pengajuan_obj.berkas_terkait_izin.add(rekomendasi_organisasi)

			data = {'success': True, 'pesan': 'Perusahaan Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': '' }
	return HttpResponse(json.dumps(data))

def validasi_berkas_toko_obat(request):
	data = {'Terjadi Kesalahan': [{'message': 'Pengajuan tidak ditemukan.'}]}
	id_pengajuan = request.COOKIES.get("id_pengajuan")
	if id_pengajuan:
		try:
			pengajuan_obj = TokoObat.objects.get(id=request.COOKIES.get("id_pengajuan"))
			berkas_ = pengajuan_obj.berkas_terkait_izin.all()
			if berkas_:
				if berkas_.filter(keterangan="Ijazah STRTTK "+pengajuan_obj.no_pengajuan).last():
					if berkas_.filter(keterangan="Denah Lokasi "+pengajuan_obj.no_pengajuan).last():
						if berkas_.filter(keterangan="Denah Bangunan "+pengajuan_obj.no_pengajuan).last():
							if berkas_.filter(keterangan="KTP "+pengajuan_obj.pemohon.get_ktp()).last():
								if berkas_.filter(keterangan="Surat yang mengatakan status bangunan dalam bentuk akta hak milik/sewa/kontrak "+pengajuan_obj.no_pengajuan).last():
									if berkas_.filter(keterangan="IMB dan Izin Gangguan "+pengajuan_obj.no_pengajuan).last():
										data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': [] }
									else:
										data = {'Terjadi Kesalahan': [{'message': 'Berkas IMB dan Izin Gangguan tidak ada'}]}
								else:
									data = {'Terjadi Kesalahan': [{'message': 'Berkas Surat yang mengatakan status bangunan dalam bentuk akta hak milik/sewa/kontrak tidak ada'}]}
							else:
								data = {'Terjadi Kesalahan': [{'message': 'Berkas KTP tidak ada'}]}
						else:
							data = {'Terjadi Kesalahan': [{'message': 'Berkas Denah Bangunan tidak ada'}]}
					else:
						data = {'Terjadi Kesalahan': [{'message': 'Berkas Denah Lokasi tidak ada'}]}
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas Ijazah STRTTK tidak ada'}]}
			else:
				data = {'Terjadi Kesalahan': [{'message': 'Berkas yang diwajibkan belum terisi.'}]}
		except ObjectDoesNotExist:
			pass
	return HttpResponse(json.dumps(data))

def load_konfirmasi_toko_obat(request, id_pengajuan):
	data = {'success': False, 'pesan': 'Terjadi Kesalahan. Pengajuan Izin tidak ditemukan atau tidak ada dalam daftar.'}
	try:
		pengajuan_obj = TokoObat.objects.get(id=id_pengajuan)
		pemohon_json = {}
		if pengajuan_obj.pemohon:
			pemohon_json = pengajuan_obj.pemohon.as_json()
		data = {'success': True, 'pesan': 'Berhasil load data pengajuan izin.', 'data': {'pemohon_json': pemohon_json, 'pengajuan_json': pengajuan_obj.as_json(), 'detil_json': pengajuan_obj.as_json__toko_obat()}}
	except ObjectDoesNotExist:
		pass
	return HttpResponse(json.dumps(data))

def upload_berkas(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			form = BerkasForm(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if berkas_._size > 4*1024*1024:
				data = {'Terjadi Kesalahan': [{'message': 'Ukuran file tidak boleh melebihi dari 4mb.'}]}
				data = json.dumps(data)
				response = HttpResponse(data)
			else:
				if request.method == "POST":
					if berkas_:
						if form.is_valid():
							ext = os.path.splitext(berkas_.name)[1]
							valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.jpeg', '.png', '.PDF', '.DOC', '.DOCX', '.JPG', '.JPEG', '.PNG']
							if not ext in valid_extensions:
								data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
								data = json.dumps(data)
								response = HttpResponse(data)
							else:
								try:
									p = Apotek.objects.get(id=request.COOKIES['id_pengajuan'])
									berkas = form.save(commit=False)
									kode = request.POST.get('kode')
									if kode == 'Ijazah Apoteker':
										berkas.nama_berkas = "Ijazah Apoteker "+p.no_pengajuan
										berkas.keterangan = "Ijazah Apoteker "+p.no_pengajuan
									elif kode == 'STRA Apoteker':
										berkas.nama_berkas = "STRA Apoteker "+p.no_pengajuan
										berkas.keterangan = "STRA Apoteker "+p.no_pengajuan
									elif kode == 'Surat Rekomendasi IAI':
										berkas.nama_berkas = "Surat Rekomendasi IAI "+p.no_pengajuan
										berkas.keterangan = "Surat Rekomendasi IAI "+p.no_pengajuan
									elif kode == 'KTP':
										berkas.nama_berkas = "KTP "+p.pemohon.get_ktp()
										berkas.keterangan = "KTP "+p.pemohon.get_ktp()
									elif kode == 'Denah Lokasi':
										berkas.nama_berkas = "Denah Lokasi "+p.no_pengajuan
										berkas.keterangan = "Denah Lokasi "+p.no_pengajuan
									elif kode == 'Denah Bangunan':
										berkas.nama_berkas = "Denah Bangunan "+p.no_pengajuan
										berkas.keterangan = "Denah Bangunan "+p.no_pengajuan
									elif kode == 'Status Bangunan':
										berkas.nama_berkas = "Status Bangunan "+p.no_pengajuan
										berkas.keterangan = "Status Bangunan "+p.no_pengajuan
									elif kode == 'IMB dan Izin Gangguan':
										berkas.nama_berkas = "IMB dan Izin Gangguan "+p.no_pengajuan
										berkas.keterangan = "IMB dan Izin Gangguan "+p.no_pengajuan
									elif kode == 'Ijazah STRTTK':
										berkas.nama_berkas = "Ijazah STRTTK "+p.no_pengajuan
										berkas.keterangan = "Ijazah STRTTK "+p.no_pengajuan
									elif kode == 'Daftar Tenaga Teknis':
										berkas.nama_berkas = "Daftar Tenaga Teknis "+p.no_pengajuan
										berkas.keterangan = "Daftar Tenaga Teknis "+p.no_pengajuan
									elif kode == 'Daftar Perlengkapan Apotek':
										berkas.nama_berkas = "Daftar Perlengkapan Apotek "+p.no_pengajuan
										berkas.keterangan = "Daftar Perlengkapan Apotek "+p.no_pengajuan
									elif kode == 'Surat Izin Atasan':
										berkas.nama_berkas = "Surat Izin Atasan "+p.no_pengajuan
										berkas.keterangan = "Surat Izin Atasan "+p.no_pengajuan
									elif kode == 'Akta Perjanjian Kerjasama Apoteker':
										berkas.nama_berkas = "Akta Perjanjian Kerjasama Apoteker "+p.no_pengajuan
										berkas.keterangan = "Akta Perjanjian Kerjasama Apoteker "+p.no_pengajuan
									elif kode == 'Surat Pernyataan Apoteker (Peraturan)':
										berkas.nama_berkas = "Surat Pernyataan Apoteker (Peraturan) "+p.no_pengajuan
										berkas.keterangan = "Surat Pernyataan Apoteker (Peraturan) "+p.no_pengajuan
									elif kode == 'Surat Pernyataan Pemilik (Peraturan)':
										berkas.nama_berkas = "Surat Pernyataan Pemilik (Peraturan) "+p.no_pengajuan
										berkas.keterangan = "Surat Pernyataan Pemilik (Peraturan) "+p.no_pengajuan
									elif kode == 'SIA':
										berkas.nama_berkas = "SIA "+p.no_pengajuan
										berkas.keterangan = "SIA "+p.no_pengajuan
									elif kode == 'SIPA':
										berkas.nama_berkas = "SIPA "+p.no_pengajuan
										berkas.keterangan = "SIPA "+p.no_pengajuan
									elif kode == 'SIPTTK(AA)':
										berkas.nama_berkas = "SIPTTK(AA) "+p.no_pengajuan
										berkas.keterangan = "SIPTTK(AA) "+p.no_pengajuan
									elif kode == 'Surat Pernyataan Pemilik':
										berkas.nama_berkas = "Surat Pernyataan Pemilik "+p.no_pengajuan
										berkas.keterangan = "Surat Pernyataan Pemilik "+p.no_pengajuan
									elif kode == 'Surat Pernyataan Apoteker':
										berkas.nama_berkas = "Surat Pernyataan Apoteker "+p.no_pengajuan
										berkas.keterangan = "Surat Pernyataan Apoteker "+p.no_pengajuan
									if request.user.is_authenticated():
										berkas.created_by_id = request.user.id
									else:
										berkas.created_by_id = request.COOKIES['id_pemohon']
									berkas.save()
									p.berkas_terkait_izin.add(berkas)

									data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
											{'status_upload': 'ok'},
										]}
									data = json.dumps(data)
									response = HttpResponse(data)
								except ObjectDoesNotExist:
									data = {'Terjadi Kesalahan': [{'message': 'Pengajuan tidak ada dalam daftar'}]}
									data = json.dumps(data)
									response = HttpResponse(data)
						else:
							data = form.errors.as_json()
							response = HttpResponse(data)
					else:
						data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong'}]}
						data = json.dumps(data)
						response = HttpResponse(data)
				else:
					data = form.errors.as_json()
					response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

# # def validasi_berkas_apotek(request):
# 	data = {'Terjadi Kesalahan': [{'message': 'Pengajuan tidak ditemukan.'}]}
# 	id_pengajuan = request.COOKIES.get("id_pengajuan")
# 	if id_pengajuan:
# 		try:
# 			pengajuan_obj = Apotek.objects.get(id=request.COOKIES.get("id_pengajuan"))
# 			berkas_ = pengajuan_obj.berkas_terkait_izin.all()
# 			if berkas_:
# 				if berkas_.filter(keterangan='Ijazah Apoteker '+npwp).last():
# 					if berkas_.filter(keterangan='STRA Apoteker '+npwp).last():
# 						if berkas_.filter(keterangan='Surat Rekomendasi IAI '+npwp).last():
# 							if berkas_.filter(keterangan="KTP "+npwp).last():
# 								if berkas_.filter(keterangan='Denah Lokasi '+npwp).last():
# 									if berkas_.filter(keterangan='Denah Bangunan '+npwp).last():
# 										if berkas_.filter(keterangan='Status Bangunan '+npwp).last():
# 											if berkas_.filter(keterangan='IMB dan Izin Gangguan '+npwp).last():
# 												if berkas_.filter(keterangan='Ijazah STRTTK '+npwp).last():
# 													if berkas_.filter(keterangan='Daftar Tenaga Teknis '+npwp).last():
# 														if berkas_.filter(keterangan='Daftar Perlengkapan Apotek '+npwp).last():
# 															if berkas_.filter(keterangan='Surat Izin Atasan '+npwp).last():
# 																if berkas_.filter(keterangan='Akta Perjanjian Kerjasama Apoteker '+npwp).last():
# 																	if berkas_.filter(keterangan='Surat Pernyataan Apoteker (Peraturan) '+npwp).last():
# 																		if berkas_.filter(keterangan='SIA '+npwp).last():
# 																			if berkas_.filter(keterangan='SIPA '+npwp).last():
# 																				if berkas_.filter(keterangan='SIPTTK(AA) '+npwp).last():
# 																					if berkas_.filter(keterangan='Surat Pernyataan Pemilik '+npwp).last():
# 																						if berkas_.filter(keterangan='Surat Pernyataan Apoteker '+npwp).last():
# 																							data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': [] }
# 																						else:
# 																							data = {'Terjadi Kesalahan': [{'message': 'Surat Pernyataan Apoteker tidak ada'}]}	
# 																					else:
# 																						data = {'Terjadi Kesalahan': [{'message': 'Surat Pernyataan Pemilik tidak ada'}]}	
# 																				else:
# 																					data = {'Terjadi Kesalahan': [{'message': 'SIPTTK(AA) tidak ada'}]}				
# 																			else:
# 																				data = {'Terjadi Kesalahan': [{'message': 'SIPA tidak ada'}]}					
# 																		else:
# 																			data = {'Terjadi Kesalahan': [{'message': 'SIA tidak ada'}]}						
# 																	else:
# 																		data = {'Terjadi Kesalahan': [{'message': 'Surat Pernyataan Apoteker (Peraturan) tidak ada'}]}							
# 																else:
# 																	data = {'Terjadi Kesalahan': [{'message': 'Akta Perjanjian Kerjasama Apoteker tidak ada'}]}						
# 															else:
# 																data = {'Terjadi Kesalahan': [{'message': 'Surat Izin Atasan tidak ada'}]}								
# 														else:
# 															data = {'Terjadi Kesalahan': [{'message': 'Daftar Perlengkapan Apotek tidak ada'}]}									
# 													else:
# 														data = {'Terjadi Kesalahan': [{'message': 'Daftar Tenaga Teknis tidak ada'}]}										
# 												else:
# 													data = {'Terjadi Kesalahan': [{'message': 'Berkas Ijazah STRTTK tidak ada'}]}											
# 											else:
# 												data = {'Terjadi Kesalahan': [{'message': 'Berkas IMB dan Izin Gangguan tidak ada'}]}				
# 										else:
# 											data = {'Terjadi Kesalahan': [{'message': 'Berkas Status Bangunan tidak ada'}]}
# 									else:
# 										data = {'Terjadi Kesalahan': [{'message': 'Denah Bangunan tidak ada'}]}
# 								else:
# 									data = {'Terjadi Kesalahan': [{'message': 'Berkas Denah Lokasi tidak ada'}]}
# 							else:
# 								data = {'Terjadi Kesalahan': [{'message': 'Berkas KTP tidak ada'}]}
# 						else:
# 							data = {'Terjadi Kesalahan': [{'message': 'Berkas Surat Rekomendasi IAI tidak ada'}]}
# 					else:
# 						data = {'Terjadi Kesalahan': [{'message': 'Berkas STRA Apoteker tidak ada'}]}
# 				else:
# 					data = {'Terjadi Kesalahan': [{'message': 'Berkas Ijazah Apoteker tidak ada'}]}
# 			else:
# 				data = {'Terjadi Kesalahan': [{'message': 'Berkas yang diwajibkan belum terisi.'}]}
# 		except ObjectDoesNotExist:
# 			pass
# 	return HttpResponse(json.dumps(data))

def apotek_upload_dokumen_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': [] }
	return HttpResponse(json.dumps(data))

def ajax_load_berkas_apotek(request, id_pengajuan):
	url_berkas = []
	id_elemen = []
	nm_berkas =[]
	id_berkas =[]
	if id_pengajuan:
		try:
			apotek = Apotek.objects.get(id=id_pengajuan)
			npwp = apotek.npwp
			berkas_ = apotek.berkas_terkait_izin.all()
			pemohon_ = apotek.pemohon

			if berkas_:
				ijazah_apoteker = berkas_.filter(keterangan='Ijazah Apoteker '+pengajuan_obj.no_pengajuan).last()
				if ijazah_apoteker:
					url_berkas.append(ijazah_apoteker.berkas.url)
					id_elemen.append('ijazah_apoteker')
					nm_berkas.append(ijazah_apoteker.nama_berkas)
					id_berkas.append(ijazah_apoteker.id)
					apotek.berkas_terkait_izin.add(ijazah_apoteker)

				stra_apoteker = berkas_.filter(keterangan='STRA Apoteker '+pengajuan_obj.no_pengajuan).last()
				if stra_apoteker:
					url_berkas.append(stra_apoteker.berkas.url)
					id_elemen.append('stra_apoteker')
					nm_berkas.append(stra_apoteker.nama_berkas)
					id_berkas.append(stra_apoteker.id)
					apotek.berkas_terkait_izin.add(stra_apoteker)

				rekom_iai = berkas_.filter(keterangan='Surat Rekomendasi IAI '+pengajuan_obj.no_pengajuan).last()
				if rekom_iai:
					url_berkas.append(rekom_iai.berkas.url)
					id_elemen.append('rekom_iai')
					nm_berkas.append(rekom_iai.nama_berkas)
					id_berkas.append(rekom_iai.id)
					apotek.berkas_terkait_izin.add(rekom_iai)

				ktp = berkas_.filter(keterangan="KTP "+pengajuan_obj.pemohon.get_ktp()).last()
				if ktp:
					url_berkas.append(ktp.berkas.url)
					id_elemen.append('ktp')
					nm_berkas.append(ktp.nama_berkas)
					id_berkas.append(ktp.id)
					apotek.berkas_terkait_izin.add(ktp)

				denah_lokasi = berkas_.filter(keterangan='Denah Lokasi '+pengajuan_obj.no_pengajuan).last()
				if denah_lokasi:
					url_berkas.append(denah_lokasi.berkas.url)
					id_elemen.append('denah_lokasi')
					nm_berkas.append(denah_lokasi.nama_berkas)
					id_berkas.append(denah_lokasi.id)
					apotek.berkas_terkait_izin.add(denah_lokasi)

				denah_bangunan = berkas_.filter(keterangan='Denah Bangunan '+pengajuan_obj.no_pengajuan).last()
				if denah_bangunan:
					url_berkas.append(denah_bangunan.berkas.url)
					id_elemen.append('denah_bangunan')
					nm_berkas.append(denah_bangunan.nama_berkas)
					id_berkas.append(denah_bangunan.id)
					apotek.berkas_terkait_izin.add(denah_bangunan)

				status_bangunan = berkas_.filter(keterangan='Status Bangunan '+pengajuan_obj.no_pengajuan).last()
				if status_bangunan:
					url_berkas.append(status_bangunan.berkas.url)
					id_elemen.append('status_bangunan')
					nm_berkas.append(status_bangunan.nama_berkas)
					id_berkas.append(status_bangunan.id)
					apotek.berkas_terkait_izin.add(status_bangunan)

				izin_gangguan = berkas_.filter(keterangan='IMB dan Izin Gangguan '+pengajuan_obj.no_pengajuan).last()
				if izin_gangguan:
					url_berkas.append(izin_gangguan.berkas.url)
					id_elemen.append('izin_gangguan')
					nm_berkas.append(izin_gangguan.nama_berkas)
					id_berkas.append(izin_gangguan.id)
					apotek.berkas_terkait_izin.add(izin_gangguan)

				ijazah_strttk = berkas_.filter(keterangan='Ijazah STRTTK '+pengajuan_obj.no_pengajuan).last()
				if ijazah_strttk:
					url_berkas.append(ijazah_strttk.berkas.url)
					id_elemen.append('ijazah_strttk')
					nm_berkas.append(ijazah_strttk.nama_berkas)
					id_berkas.append(ijazah_strttk.id)
					apotek.berkas_terkait_izin.add(ijazah_strttk)

				daftar_tenaga_teknis = berkas_.filter(keterangan='Daftar Tenaga Teknis '+pengajuan_obj.no_pengajuan).last()
				if daftar_tenaga_teknis:
					url_berkas.append(daftar_tenaga_teknis.berkas.url)
					id_elemen.append('daftar_tenaga_teknis')
					nm_berkas.append(daftar_tenaga_teknis.nama_berkas)
					id_berkas.append(daftar_tenaga_teknis.id)
					apotek.berkas_terkait_izin.add(daftar_tenaga_teknis)

				alat_perlengkapan_apotek = berkas_.filter(keterangan='Daftar Perlengkapan Apotek '+pengajuan_obj.no_pengajuan).last()
				if alat_perlengkapan_apotek:
					url_berkas.append(alat_perlengkapan_apotek.berkas.url)
					id_elemen.append('alat_perlengkapan_apotek')
					nm_berkas.append(alat_perlengkapan_apotek.nama_berkas)
					id_berkas.append(alat_perlengkapan_apotek.id)
					apotek.berkas_terkait_izin.add(alat_perlengkapan_apotek)

				izin_atasan = berkas_.filter(keterangan='Surat Izin Atasan '+pengajuan_obj.no_pengajuan).last()
				if izin_atasan:
					url_berkas.append(izin_atasan.berkas.url)
					id_elemen.append('izin_atasan')
					nm_berkas.append(izin_atasan.nama_berkas)
					id_berkas.append(izin_atasan.id)
					apotek.berkas_terkait_izin.add(izin_atasan)

				perjanjian_apoteker = berkas_.filter(keterangan='Akta Perjanjian Kerjasama Apoteker '+pengajuan_obj.no_pengajuan).last()
				if perjanjian_apoteker:
					url_berkas.append(perjanjian_apoteker.berkas.url)
					id_elemen.append('perjanjian_apoteker')
					nm_berkas.append(perjanjian_apoteker.nama_berkas)
					id_berkas.append(perjanjian_apoteker.id)
					apotek.berkas_terkait_izin.add(perjanjian_apoteker)

				pernyataan_peraturan_apoteker = berkas_.filter(keterangan='Surat Pernyataan Apoteker (Peraturan) '+pengajuan_obj.no_pengajuan).last()
				if pernyataan_peraturan_apoteker:
					url_berkas.append(pernyataan_peraturan_apoteker.berkas.url)
					id_elemen.append('pernyataan_peraturan_apoteker')
					nm_berkas.append(pernyataan_peraturan_apoteker.nama_berkas)
					id_berkas.append(pernyataan_peraturan_apoteker.id)
					apotek.berkas_terkait_izin.add(pernyataan_peraturan_apoteker)

				pernyataan_peraturan_pemilik = berkas_.filter(keterangan='Surat Pernyataan Pemilik (Peraturan) '+pengajuan_obj.no_pengajuan).last()
				if pernyataan_peraturan_pemilik:
					url_berkas.append(pernyataan_peraturan_pemilik.berkas.url)
					id_elemen.append('pernyataan_peraturan_pemilik')
					nm_berkas.append(pernyataan_peraturan_pemilik.nama_berkas)
					id_berkas.append(pernyataan_peraturan_pemilik.id)
					apotek.berkas_terkait_izin.add(pernyataan_peraturan_pemilik)

				sia = berkas_.filter(keterangan='SIA '+pengajuan_obj.no_pengajuan).last()
				if sia:
					url_berkas.append(sia.berkas.url)
					id_elemen.append('sia')
					nm_berkas.append(sia.nama_berkas)
					id_berkas.append(sia.id)
					apotek.berkas_terkait_izin.add(sia)

				sipa = berkas_.filter(keterangan='SIPA '+pengajuan_obj.no_pengajuan).last()
				if sipa:
					url_berkas.append(sipa.berkas.url)
					id_elemen.append('sipa')
					nm_berkas.append(sipa.nama_berkas)
					id_berkas.append(sipa.id)
					apotek.berkas_terkait_izin.add(sipa)

				sipttk = berkas_.filter(keterangan='SIPTTK(AA) '+pengajuan_obj.no_pengajuan).last()
				if sipttk:
					url_berkas.append(sipttk.berkas.url)
					id_elemen.append('sipttk')
					nm_berkas.append(sipttk.nama_berkas)
					id_berkas.append(sipttk.id)
					apotek.berkas_terkait_izin.add(sipttk)

				pernyataan_pemilik = berkas_.filter(keterangan='Surat Pernyataan Pemilik '+pengajuan_obj.no_pengajuan).last()
				if pernyataan_pemilik:
					url_berkas.append(pernyataan_pemilik.berkas.url)
					id_elemen.append('pernyataan_pemilik')
					nm_berkas.append(pernyataan_pemilik.nama_berkas)
					id_berkas.append(pernyataan_pemilik.id)
					apotek.berkas_terkait_izin.add(pernyataan_pemilik)
				
				pernyataan_apoteker = berkas_.filter(keterangan='Surat Pernyataan Apoteker '+pengajuan_obj.no_pengajuan).last()
				if pernyataan_apoteker:
					url_berkas.append(pernyataan_apoteker.berkas.url)
					id_elemen.append('pernyataan_apoteker')
					nm_berkas.append(pernyataan_apoteker.nama_berkas)
					id_berkas.append(pernyataan_apoteker.id)
					apotek.berkas_terkait_izin.add(pernyataan_apoteker)

			data = {'success': True, 'pesan': 'Sukses.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': '' }
	response = HttpResponse(json.dumps(data))
	return response

def load_konfirmasi_apotek(request, id_pengajuan):
	data = {'success': False, 'pesan': 'Data tidak ditemukan.' }
	if id_pengajuan:
		try:
			pengajuan_obj = PengajuanIzin.objects.get(id=id_pengajuan)
			apotek_obj = Apotek.objects.filter(id=id_pengajuan).last()
			pengajuan_json = {}
			pemohon_json = {}
			apotek_json = {}
			data_anggota_json = []
			if pengajuan_obj:
				pengajuan_json = pengajuan_obj.as_json()
				if pengajuan_obj.pemohon:
					pemohon_json = pengajuan_obj.pemohon.as_json()

				if apotek_obj:
					apotek_json = apotek_obj.as_json()
			data = {'success': True, 'pesan': 'Sukses.', 'data': { 'pengajuan_json':pengajuan_json, 'pemohon_json': pemohon_json, 'apotek_json': apotek_json}}
		except ObjectDoesNotExist:
			pass
	return HttpResponse(json.dumps(data))

def apotek_done(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = Apotek.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			pengajuan_.status = 6
			pengajuan_.save()
					
			data = {'success': True, 'pesan': 'Proses Selesai.' }
			response = HttpResponse(json.dumps(data))
			response.delete_cookie(key='id_pengajuan') # set cookie	
			response.delete_cookie(key='id_perusahaan') # set cookie	
			response.delete_cookie(key='nomor_ktp') # set cookie	
			response.delete_cookie(key='nomor_paspor') # set cookie	
			response.delete_cookie(key='id_pemohon') # set cookie	
			response.delete_cookie(key='id_kelompok_izin') # set cookie
			response.delete_cookie(key='npwp_perusahaan') # set cookie
			response.delete_cookie(key='id_jenis_pengajuan') # set cookie
			response.delete_cookie(key='kode_kelompok_jenis_izin') # set cookie
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def save_izin_laboratorium(request):
	data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				try:
					print request.POST.get("desa1")
					pengajuan_obj = Laboratorium.objects.get(id=request.COOKIES['id_pengajuan'])
					pengajuan_obj.klasifikasi_laboratorium = request.POST.get("klasifikasi_laboratorium")
					pengajuan_obj.nama_laboratorium = request.POST.get("nama_laboratorium")
					pengajuan_obj.alamat_laboratorium = request.POST.get("alamat_laboratorium")
					pengajuan_obj.desa_id = request.POST.get("desa1")
					pengajuan_obj.penanggung_jawab_teknis = request.POST.get("penanggung_jawab_teknis")
					pengajuan_obj.save()
					data = {'success':True, 'pesan': 'Data izin Laboratorium berhasil disimpan.'}
				except Laboratorium.DoesNotExist:
					pass

	return HttpResponse(json.dumps(data))

def upload_berkas_laboratorium(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			form = BerkasForm(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if berkas_._size > 4*1024*1024:
				data = {'Terjadi Kesalahan': [{'message': 'Ukuran file tidak boleh melebihi dari 4mb.'}]}
				data = json.dumps(data)
				response = HttpResponse(data)
			else:
				if request.method == "POST":
					if berkas_:
						if form.is_valid():
							ext = os.path.splitext(berkas_.name)[1]
							valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.jpeg', '.png', '.PDF', '.DOC', '.DOCX', '.JPG', '.JPEG', '.PNG']
							if not ext in valid_extensions:
								data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
								data = json.dumps(data)
								response = HttpResponse(data)
							else:
								try:
									p = Laboratorium.objects.get(id=request.COOKIES['id_pengajuan'])
									berkas = form.save(commit=False)
									kode = request.POST.get('kode')
									if kode == 'KTP':
										berkas.nama_berkas = "KTP "+p.pemohon.get_ktp()
										berkas.keterangan = "KTP "+p.pemohon.get_ktp()
									elif kode == 'IMB dan Izin Gangguan':
										berkas.nama_berkas = "IMB dan Izin Gangguan "+p.nama_laboratorium
										berkas.keterangan = "IMB dan Izin Gangguan "+p.no_pengajuan
									elif kode == 'Akte Pendirian Badan Hukum':
										berkas.nama_berkas = "Akte Pendirian Badan Hukum "+p.nama_laboratorium
										berkas.keterangan = "Akte Pendirian Badan Hukum "+p.no_pengajuan
									elif kode == 'Denah Lokasi':
										berkas.nama_berkas = "Denah Lokasi "+p.nama_laboratorium
										berkas.keterangan = "Denah Lokasi "+p.no_pengajuan
									elif kode == 'Pernyataan Tanggung Jawab':
										berkas.nama_berkas = "Pernyataan Tanggung Jawab "+p.nama_laboratorium
										berkas.keterangan = "Pernyataan Tanggung Jawab "+p.no_pengajuan
									elif kode == 'Pernyataan Kesanggupan':
										berkas.nama_berkas = "Pernyataan Kesanggupan "+p.nama_laboratorium
										berkas.keterangan = "Pernyataan Kesanggupan "+p.no_pengajuan
									elif kode == 'Surat Pengalaman Kerja':
										berkas.nama_berkas = "Surat Pengalaman Kerja "+p.nama_laboratorium
										berkas.keterangan = "Surat Pengalaman Kerja "+p.no_pengajuan
									elif kode == 'Ijazah Kesarjanaan':
										berkas.nama_berkas = "Ijazah Kesarjanaan "+p.nama_laboratorium
										berkas.keterangan = "Ijazah Kesarjanaan "+p.no_pengajuan
									elif kode == 'Surat Pernyataan kesediaan':
										berkas.nama_berkas = "Surat Pernyataan kesediaan "+p.nama_laboratorium
										berkas.keterangan = "Surat Pernyataan kesediaan "+p.no_pengajuan
									
									if request.user.is_authenticated():
										berkas.created_by_id = request.user.id
									else:
										berkas.created_by_id = request.COOKIES['id_pemohon']
									berkas.save()
									p.berkas_terkait_izin.add(berkas)

									data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
											{'status_upload': 'ok'},
										]}
									data = json.dumps(data)
									response = HttpResponse(data)
								except ObjectDoesNotExist:
									data = {'Terjadi Kesalahan': [{'message': 'Pengajuan tidak ada dalam daftar'}]}
									data = json.dumps(data)
									response = HttpResponse(data)
						else:
							data = form.errors.as_json()
							response = HttpResponse(data)
					else:
						data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong'}]}
						data = json.dumps(data)
						response = HttpResponse(data)
				else:
					data = form.errors.as_json()
					response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def laboratorium_upload_dokumen_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': [] }
	return HttpResponse(json.dumps(data))

def ajax_load_berkas_laboratorium(request, id_pengajuan):
	url_berkas = []
	id_elemen = []
	nm_berkas =[]
	id_berkas =[]
	if id_pengajuan:
		try:
			pengajuan_obj = Laboratorium.objects.get(id=id_pengajuan)
			berkas_ = pengajuan_obj.berkas_terkait_izin.all()

			if berkas_:
				ktp = berkas_.filter(keterangan="KTP "+pengajuan_obj.pemohon.get_ktp()).last()
				if ktp:
					url_berkas.append(ktp.berkas.url)
					id_elemen.append('ktp')
					nm_berkas.append(ktp.nama_berkas)
					id_berkas.append(ktp.id)
					pengajuan_obj.berkas_terkait_izin.add(ktp)

				izin_gangguan = berkas_.filter(keterangan='IMB dan Izin Gangguan '+pengajuan_obj.no_pengajuan).last()
				if izin_gangguan:
					url_berkas.append(izin_gangguan.berkas.url)
					id_elemen.append('izin_gangguan')
					nm_berkas.append(izin_gangguan.nama_berkas)
					id_berkas.append(izin_gangguan.id)
					pengajuan_obj.berkas_terkait_izin.add(izin_gangguan)

				akte_pendirian = berkas_.filter(keterangan='Akte Pendirian Badan Hukum '+pengajuan_obj.no_pengajuan).last()
				if akte_pendirian:
					url_berkas.append(akte_pendirian.berkas.url)
					id_elemen.append('akte_pendirian')
					nm_berkas.append(akte_pendirian.nama_berkas)
					id_berkas.append(akte_pendirian.id)
					pengajuan_obj.berkas_terkait_izin.add(akte_pendirian)

				denah_lokasi = berkas_.filter(keterangan='Denah Lokasi '+pengajuan_obj.no_pengajuan).last()
				if denah_lokasi:
					url_berkas.append(denah_lokasi.berkas.url)
					id_elemen.append('denah_lokasi')
					nm_berkas.append(denah_lokasi.nama_berkas)
					id_berkas.append(denah_lokasi.id)
					pengajuan_obj.berkas_terkait_izin.add(denah_lokasi)

				pernyataan_tanggung_jawab = berkas_.filter(keterangan='Pernyataan Tanggung Jawab '+pengajuan_obj.no_pengajuan).last()
				if pernyataan_tanggung_jawab:
					url_berkas.append(pernyataan_tanggung_jawab.berkas.url)
					id_elemen.append('pernyataan_tanggung_jawab')
					nm_berkas.append(pernyataan_tanggung_jawab.nama_berkas)
					id_berkas.append(pernyataan_tanggung_jawab.id)
					pengajuan_obj.berkas_terkait_izin.add(pernyataan_tanggung_jawab)

				pernyataan_kesanggupan = berkas_.filter(keterangan='Pernyataan Kesanggupan '+pengajuan_obj.no_pengajuan).last()
				if pernyataan_kesanggupan:
					url_berkas.append(pernyataan_kesanggupan.berkas.url)
					id_elemen.append('pernyataan_kesanggupan')
					nm_berkas.append(pernyataan_kesanggupan.nama_berkas)
					id_berkas.append(pernyataan_kesanggupan.id)
					pengajuan_obj.berkas_terkait_izin.add(pernyataan_kesanggupan)

				pengalaman_kerja = berkas_.filter(keterangan='Surat Pengalaman Kerja '+pengajuan_obj.no_pengajuan).last()
				if pengalaman_kerja:
					url_berkas.append(pengalaman_kerja.berkas.url)
					id_elemen.append('pengalaman_kerja')
					nm_berkas.append(pengalaman_kerja.nama_berkas)
					id_berkas.append(pengalaman_kerja.id)
					pengajuan_obj.berkas_terkait_izin.add(pengalaman_kerja)

				ijazah_kesarjanaan = berkas_.filter(keterangan='Ijazah Kesarjanaan '+pengajuan_obj.no_pengajuan).last()
				if ijazah_kesarjanaan:
					url_berkas.append(ijazah_kesarjanaan.berkas.url)
					id_elemen.append('ijazah_kesarjanaan')
					nm_berkas.append(ijazah_kesarjanaan.nama_berkas)
					id_berkas.append(ijazah_kesarjanaan.id)
					pengajuan_obj.berkas_terkait_izin.add(ijazah_kesarjanaan)

				pernyataan_kesediaan = berkas_.filter(keterangan='Surat Pernyataan kesediaan '+pengajuan_obj.no_pengajuan).last()
				if pernyataan_kesediaan:
					url_berkas.append(pernyataan_kesediaan.berkas.url)
					id_elemen.append('pernyataan_kesediaan')
					nm_berkas.append(pernyataan_kesediaan.nama_berkas)
					id_berkas.append(pernyataan_kesediaan.id)
					pengajuan_obj.berkas_terkait_izin.add(pernyataan_kesediaan)


			data = {'success': True, 'pesan': 'Sukses.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': '' }
	response = HttpResponse(json.dumps(data))
	return response

def load_konfirmasi_laboratorium(request, id_pengajuan):
	data = {'success': False, 'pesan': 'Data tidak ditemukan.' }
	if id_pengajuan:
		try:
			pengajuan_obj = PengajuanIzin.objects.get(id=id_pengajuan)
			laboratorium_obj = Laboratorium.objects.filter(id=id_pengajuan).last()
			pengajuan_json = {}
			pemohon_json = {}
			laboratorium_json = {}
			data_anggota_json = []
			if pengajuan_obj:
				pengajuan_json = pengajuan_obj.as_json()
				if pengajuan_obj.pemohon:
					pemohon_json = pengajuan_obj.pemohon.as_json()

				if laboratorium_obj:
					laboratorium_json = laboratorium_obj.as_json()
			data = {'success': True, 'pesan': 'Sukses.', 'data': { 'pengajuan_json':pengajuan_json, 'pemohon_json': pemohon_json, 'laboratorium_json': laboratorium_json}}
		except ObjectDoesNotExist:
			pass
	return HttpResponse(json.dumps(data))

def save_peralatan_lab(request):
	data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				try:
					pengajuan_obj = Laboratorium.objects.get(id=request.COOKIES.get("id_pengajuan"))
					print request.POST.get("id_bangunan_lab")
					if request.POST.get("id_bangunan_lab") != "" and request.POST.get("id_bangunan_lab") is not None:
						peralatan_lab_obj, created = PeralatanLaboratorium.objects.get_or_create(id=request.POST.get("id_peralatan_lab"))
						peralatan_lab_obj.laboratorium_id = pengajuan_obj.id
						peralatan_lab_obj.jenis_peralatan = request.POST.get("jenis_peralatan")
						peralatan_lab_obj.jumlah = request.POST.get("jumlah")
						peralatan_lab_obj.keterangan = request.POST.get("keterangan")
						peralatan_lab_obj.save()
						data = {'success': True, 'pesan': 'Data peralatan berhasil tersimpan.'}
					else:
						peralatan_lab_obj = PeralatanLaboratorium(laboratorium_id=pengajuan_obj.id, jenis_peralatan = request.POST.get("jenis_peralatan"), jumlah = request.POST.get("jumlah"), keterangan = request.POST.get("keterangan"))
						peralatan_lab_obj.save()
						data = {'success': True, 'pesan': 'Data peralatan berhasil tersimpan.'}
				except Laboratorium.DoesNotExist:
					pass
	return HttpResponse(json.dumps(data))

def load_peralatan_lab(request, id_pengajuan):
	data = []
	response = {'success': False, 'pesan': 'Data gagal diload.', 'data': data} 
	if id_pengajuan:
		print id_pengajuan
		peralatan_list = PeralatanLaboratorium.objects.filter(laboratorium_id=id_pengajuan)
		print peralatan_list
		if peralatan_list:
			data = [x.as_json() for x in peralatan_list]
			response = {'success': True, 'pesan': 'Data berhasil diload.', 'data': data}
	return HttpResponse(json.dumps(response))

def load_edit_peralatan_lab(request, id_peralatan_lab):
	data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
	as_json = {}
	if id_peralatan_lab:
		try:
			i = PeralatanLaboratorium.objects.get(id=id_peralatan_lab)
			as_json = i.as_json()
			data = {'success': True, 'pesan': 'Data berhasil diload.', 'data':as_json}
		except ObjectDoesNotExist:
			pass
	return HttpResponse(json.dumps(data))

def delete_peralatan_lab(request, id_peralatan_lab):
	data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
	if id_peralatan_lab:
		try:
			i = PeralatanLaboratorium.objects.get(id=id_peralatan_lab)
			i.delete()
			data = {'success': True, 'pesan': 'Data berhasil dihapus.'}
		except ObjectDoesNotExist:
			pass
	return HttpResponse(json.dumps(data))

def save_bangunan_lab(request):
	data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				try:
					pengajuan_obj = Laboratorium.objects.get(id=request.COOKIES['id_pengajuan'])
					if request.POST.get("id_bangunan_lab") != "":
						bangunan_lab_obj, created = BangunanLaboratorium.objects.get_or_create(id=request.POST.get("id_bangunan_lab"))
						
						bangunan_lab_obj.laboratorium = pengajuan_obj.id
						bangunan_lab_obj.jenis_kelengkapan_bangunan_id = request.POST.get("jenis_kelengkapan")
						bangunan_lab_obj.nama_kelengkapan_bangunan = request.POST.get("nama_kelengkapan")
						bangunan_lab_obj.keterangan = request.POST.get("keterangan")
						bangunan_lab_obj.save()
						data = {'success': True, 'pesan': 'Data Bangunan berhasil diperbaharui.'}
					else:
						bangunan_lab_obj = BangunanLaboratorium(laboratorium_id=pengajuan_obj.id, jenis_kelengkapan_bangunan_id = request.POST.get("jenis_kelengkapan"), nama_kelengkapan_bangunan = request.POST.get("nama_kelengkapan"), keterangan = request.POST.get("keterangan"))
						bangunan_lab_obj.save()
						data = {'success': True, 'pesan': 'Data Bangunan berhasil tersimpan.'}
				except Laboratorium.DoesNotExist:
					pass
	return HttpResponse(json.dumps(data))

def load_bangunan_lab(request, id_pengajuan):
	data = []
	response = {'success': False, 'pesan': 'Data gagal diload.', 'data': data} 
	if id_pengajuan:
		bangunan_list = BangunanLaboratorium.objects.filter(laboratorium_id=id_pengajuan)
		if bangunan_list:
			data = [x.as_json() for x in bangunan_list]
			response = {'success': True, 'pesan': 'Data berhasil diload.', 'data': data}
	return HttpResponse(json.dumps(response))

def load_edit_bangunan_lab(request, id_bangunan_lab):
	data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
	as_json = {}
	if id_bangunan_lab:
		try:
			i = BangunanLaboratorium.objects.get(id=id_bangunan_lab)
			as_json = i.as_json()
			data = {'success': True, 'pesan': 'Data berhasil diload.', 'data':as_json}
		except ObjectDoesNotExist:
			pass
	return HttpResponse(json.dumps(data))

def delete_bangunan_lab(request, id_bangunan_lab):
	data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
	if id_bangunan_lab:
		try:
			i = BangunanLaboratorium.objects.get(id=id_bangunan_lab)
			i.delete()
			data = {'success': True, 'pesan': 'Data berhasil dihapus.'}
		except ObjectDoesNotExist:
			pass
	return HttpResponse(json.dumps(data))

def load_konfirmasi_laboratorium(request, id_pengajuan):
	data = {'success': False, 'pesan': 'Data tidak ditemukan.' }
	if id_pengajuan:
		try:
			pengajuan_obj = PengajuanIzin.objects.get(id=id_pengajuan)
			laboratorium_obj = Laboratorium.objects.filter(id=id_pengajuan).last()
			peralatan_obj = PeralatanLaboratorium.objects.filter(id=id_pengajuan).last()
			bangunan_obj = BangunanLaboratorium.objects.filter(id=id_pengajuan).last()
			pengajuan_json = {}
			pemohon_json = {}
			laboratorium_json = {}
			peralatan_json = {}
			bangunan_json = {}
			if pengajuan_obj:
				pengajuan_json = pengajuan_obj.as_json()
				if pengajuan_obj.pemohon:
					pemohon_json = pengajuan_obj.pemohon.as_json()

				if laboratorium_obj:
					laboratorium_json = laboratorium_obj.as_json()

				if peralatan_obj:
					peralatan_json = peralatan_obj.as_json()

				if bangunan_obj:
					bangunan_json = bangunan_obj.as_json()
			data = {'success': True, 'pesan': 'Sukses.', 'data': { 'pengajuan_json':pengajuan_json, 'pemohon_json': pemohon_json, 'laboratorium_json': laboratorium_json, 'peralatan_json':peralatan_json, 'bangunan_json':bangunan_json}}
		except ObjectDoesNotExist:
			pass
	return HttpResponse(json.dumps(data))

def next_tab_peralatan_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': [] }
	return HttpResponse(json.dumps(data))

def next_tab_bangunan_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': [] }
	return HttpResponse(json.dumps(data))

def laboratorium_done(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = Laboratorium.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			pengajuan_.status = 6
			pengajuan_.save()
					
			data = {'success': True, 'pesan': 'Proses Selesai.' }
			response = HttpResponse(json.dumps(data))
			response.delete_cookie(key='id_pengajuan') # set cookie	
			response.delete_cookie(key='id_perusahaan') # set cookie	
			response.delete_cookie(key='nomor_ktp') # set cookie	
			response.delete_cookie(key='nomor_paspor') # set cookie	
			response.delete_cookie(key='id_pemohon') # set cookie	
			response.delete_cookie(key='id_kelompok_izin') # set cookie
			response.delete_cookie(key='npwp_perusahaan') # set cookie
			response.delete_cookie(key='id_jenis_pengajuan') # set cookie
			response.delete_cookie(key='kode_kelompok_jenis_izin') # set cookie
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def save_izin_penutupan_apotek(request):
	data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				try:
					pengajuan_obj = PenutupanApotek.objects.get(id=request.COOKIES['id_pengajuan'])
					form__penutupan = PenutupanApotekForm(request.POST, instance=pengajuan_obj)
					if form__penutupan.is_valid():
						p = form__penutupan.save(commit=False)
						p.save()
						data = {'success': True, 'pesan': 'Data Izin Penutupan Apotek berhasil tersimpan.'}
					else:
						data = form__penutupan.errors.as_json()
						data = {'success': False, 'pesan': 'Data Izin Penutupan Apotek gagal.', 'data': data}
				except PenutupanApotek.DoesNotExist:
					pass
	return HttpResponse(json.dumps(data))

def save_izin_optikal(request):
	data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				try:
					pengajuan_obj = Optikal.objects.get(id=request.COOKIES['id_pengajuan'])
					form_optikal = OptikalForm(request.POST, instance=pengajuan_obj)
					if form_optikal.is_valid():
						p = form_optikal.save(commit=False)
						p.save()
						data = {'success': True, 'pesan': 'Data Izin Optikal berhasil tersimpan.'}
					else:
						data = form_optikal.errors.as_json()
						data = {'success': False, 'pesan': 'Data Izin Optikal gagal.', 'data': data}
				except Optikal.DoesNotExist:
					pass
	return HttpResponse(json.dumps(data))

def save_pengunduran_apoteker(request):
	data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				try:
					pengajuan_obj = PenutupanApotek.objects.get(id=request.COOKIES['id_pengajuan'])
					print request.POST.get("id_pengunduran_apoteker")
					if request.POST.get("id_pengunduran_apoteker") != "":
						print 'masuk sini'
						pengunduran_obj, created = PengunduranApoteker.objects.get_or_create(id=request.POST.get("id_pengunduran_apoteker"))
						
						pengunduran_obj.nama_apotek_id = pengajuan_obj.id
						pengunduran_obj.nama_apoteker = request.POST.get("nama_apoteker")
						pengunduran_obj.tempat_lahir = request.POST.get("tempat_lahir")
						pengunduran_obj.tanggal_lahir = datetime.datetime.strptime(request.POST.get('tanggal_lahir'), '%d-%m-%Y')
						pengunduran_obj.alamat_apoteker = request.POST.get("alamat")
						pengunduran_obj.telepon_apoteker = request.POST.get("no_telepon")
						pengunduran_obj.keterangan = request.POST.get("keterangan")
						pengunduran_obj.save()
						data = {'success': True, 'pesan': 'Data berhasil diperbaharui.'}
					else:
						print 'masuk sini'
						pengunduran_obj = PengunduranApoteker(nama_apotek_id=pengajuan_obj.id, nama_apoteker = request.POST.get("nama_apoteker"), tempat_lahir = request.POST.get("tempat_lahir"),tanggal_lahir = datetime.datetime.strptime(request.POST.get('tanggal_lahir'), '%d-%m-%Y'), alamat_apoteker = request.POST.get("alamat"),
							telepon_apoteker = request.POST.get("no_telepon"), keterangan = request.POST.get("keterangan"))
						pengunduran_obj.save()
						data = {'success': True, 'pesan': 'Data berhasil tersimpan.'}
				except PengunduranApoteker.DoesNotExist:
					pass
	return HttpResponse(json.dumps(data))

def load_pengunduran_apoteker(request, id_pengajuan):
	data = []
	response = {'success': False, 'pesan': 'Data gagal diload.', 'data': data} 
	if id_pengajuan:
		apoteker_list = PengunduranApoteker.objects.filter(nama_apotek_id=id_pengajuan)
		if apoteker_list:
			data = [x.as_json__pengunduran_apoteker() for x in apoteker_list]
			response = {'success': True, 'pesan': 'Data berhasil diload.', 'data': data}
	return HttpResponse(json.dumps(response))

def load_edit_pengunduran_apoteker(request, id_pengunduran):
	data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
	as_json = {}
	if id_pengunduran:
		try:
			i = PengunduranApoteker.objects.get(id=id_pengunduran)
			as_json = i.as_json__pengunduran_apoteker()
			data = {'success': True, 'pesan': 'Data berhasil diload.', 'data':as_json}
		except ObjectDoesNotExist:
			pass
	return HttpResponse(json.dumps(data))

def delete_pengunduran_apoteker(request, id_pengunduran):
	data = {'success': False, 'pesan': 'Data tidak ditemukan.'}
	if id_pengunduran:
		try:
			i = PengunduranApoteker.objects.get(id=id_pengunduran)
			i.delete()
			data = {'success': True, 'pesan': 'Data berhasil dihapus.'}
		except ObjectDoesNotExist:
			pass
	return HttpResponse(json.dumps(data))

def load_izin_penutupan_apotek(request, id_pengajuan):
	data = {}
	response = {'success': False, 'pesan': 'Data Penutupan Apotek berhasil tersimpan.', 'data': data}
	if id_pengajuan:
		pengajuan_obj = PenutupanApotek.objects.filter(id=id_pengajuan).last()
		if pengajuan_obj:
			data = pengajuan_obj.as_json__penutupan_apotek()
			response = {'success': True, 'pesan': 'Data Penutupan Apotek berhasil tersimpan.', 'data': data}
	return HttpResponse(json.dumps(response))

def upload_berkas_penutupan_apotek(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			form = BerkasForm(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if berkas_._size > 4*1024*1024:
				data = {'Terjadi Kesalahan': [{'message': 'Ukuran file tidak boleh melebihi dari 4mb.'}]}
				data = json.dumps(data)
				response = HttpResponse(data)
			else:
				if request.method == "POST":
					if berkas_:
						if form.is_valid():
							ext = os.path.splitext(berkas_.name)[1]
							valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.jpeg', '.png', '.PDF', '.DOC', '.DOCX', '.JPG', '.JPEG', '.PNG']
							if not ext in valid_extensions:
								data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
								data = json.dumps(data)
								response = HttpResponse(data)
							else:
								try:
									p = PenutupanApotek.objects.get(id=request.COOKIES['id_pengajuan'])
									berkas = form.save(commit=False)
									kode = request.POST.get('kode')
									if kode == 'KTP':
										berkas.nama_berkas = "KTP "+p.no_pengajuan
										berkas.keterangan = "KTP "+p.no_pengajuan
									elif kode == 'Berita Acara':
										berkas.nama_berkas = "Berita Acara "+p.no_pengajuan
										berkas.keterangan = "Berita Acara "+p.no_pengajuan
									elif kode == 'Surat izin Apotek':
										berkas.nama_berkas = "Surat izin Apotek "+p.no_pengajuan
										berkas.keterangan = "Surat izin Apotek "+p.no_pengajuan
									
									if request.user.is_authenticated():
										berkas.created_by_id = request.user.id
									else:
										berkas.created_by_id = request.COOKIES['id_pemohon']
									berkas.save()
									p.berkas_terkait_izin.add(berkas)

									data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
											{'status_upload': 'ok'},
										]}
									data = json.dumps(data)
									response = HttpResponse(data)
								except ObjectDoesNotExist:
									data = {'Terjadi Kesalahan': [{'message': 'Pengajuan tidak ada dalam daftar'}]}
									data = json.dumps(data)
									response = HttpResponse(data)
						else:
							data = form.errors.as_json()
							response = HttpResponse(data)
					else:
						data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong'}]}
						data = json.dumps(data)
						response = HttpResponse(data)
				else:
					data = form.errors.as_json()
					response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def penutupan_apotek_upload_dokumen_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': [] }
	return HttpResponse(json.dumps(data))

def next_tab_penutupan_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': [] }
	return HttpResponse(json.dumps(data))

def ajax_load_berkas_penutupan_apotek(request, id_pengajuan):
	url_berkas = []
	id_elemen = []
	nm_berkas =[]
	id_berkas =[]
	if id_pengajuan:
		try:
			pengajuan_obj = PenutupanApotek.objects.get(id=id_pengajuan)
			berkas_ = pengajuan_obj.berkas_terkait_izin.all()

			if berkas_:
				ktp = berkas_.filter(keterangan='KTP '+pengajuan_obj.no_pengajuan).last()
				if ktp:
					url_berkas.append(ktp.berkas.url)
					id_elemen.append('ktp')
					nm_berkas.append(ktp.nama_berkas)
					id_berkas.append(ktp.id)
					pengajuan_obj.berkas_terkait_izin.add(ktp)

				berita_acara = berkas_.filter(keterangan='Berita Acara '+pengajuan_obj.no_pengajuan).last()
				if berita_acara:
					url_berkas.append(berita_acara.berkas.url)
					id_elemen.append('berita_acara')
					nm_berkas.append(berita_acara.nama_berkas)
					id_berkas.append(berita_acara.id)
					pengajuan_obj.berkas_terkait_izin.add(berita_acara)

				surat_izin = berkas_.filter(keterangan='Surat izin Apotek '+pengajuan_obj.no_pengajuan).last()
				if surat_izin:
					url_berkas.append(surat_izin.berkas.url)
					id_elemen.append('surat_izin')
					nm_berkas.append(surat_izin.nama_berkas)
					id_berkas.append(surat_izin.id)
					pengajuan_obj.berkas_terkait_izin.add(surat_izin)

			data = {'success': True, 'pesan': 'Sukses.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': '' }
	response = HttpResponse(json.dumps(data))
	return response

def load_konfirmasi_penutupan_apotek(request, id_pengajuan):
	data = {'success': False, 'pesan': 'Data tidak ditemukan.' }
	if id_pengajuan:
		try:
			pengajuan_obj = PengajuanIzin.objects.get(id=id_pengajuan)
			penutupan_obj = PenutupanApotek.objects.filter(id=id_pengajuan).last()
			pengunduran_obj= PengunduranApoteker.objects.filter(nama_apotek_id=id_pengajuan).last()
			pengajuan_json = {}
			pemohon_json = {}
			penutupan_json = {}
			pengunduran_json = {}
			if pengajuan_obj:
				pengajuan_json = pengajuan_obj.as_json()
				if pengajuan_obj.pemohon:
					pemohon_json = pengajuan_obj.pemohon.as_json()

				if penutupan_obj:
					penutupan_json = penutupan_obj.as_json__penutupan_apotek()

				if pengunduran_obj:
					print 'asdasd'
					pengunduran_json = pengunduran_obj.as_json__pengunduran_apoteker()

			data = {'success': True, 'pesan': 'Sukses.', 'data': { 'pengajuan_json':pengajuan_json, 'pemohon_json': pemohon_json, 'penutupan_json': penutupan_json, 'pengunduran_json':pengunduran_json}}
		except ObjectDoesNotExist:
			pass
	return HttpResponse(json.dumps(data))

def penutupan_apotek_done(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = PenutupanApotek.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			pengajuan_.status = 6
			pengajuan_.save()
					
			data = {'success': True, 'pesan': 'Proses Selesai.' }
			response = HttpResponse(json.dumps(data))
			response.delete_cookie(key='id_pengajuan') # set cookie	
			response.delete_cookie(key='id_perusahaan') # set cookie	
			response.delete_cookie(key='nomor_ktp') # set cookie	
			response.delete_cookie(key='nomor_paspor') # set cookie	
			response.delete_cookie(key='id_pemohon') # set cookie	
			response.delete_cookie(key='id_kelompok_izin') # set cookie
			response.delete_cookie(key='npwp_perusahaan') # set cookie
			response.delete_cookie(key='id_jenis_pengajuan') # set cookie
			response.delete_cookie(key='kode_kelompok_jenis_izin') # set cookie
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response


def upload_berkas_optikal(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			form = BerkasForm(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if berkas_._size > 4*1024*1024:
				data = {'Terjadi Kesalahan': [{'message': 'Ukuran file tidak boleh melebihi dari 4mb.'}]}
				data = json.dumps(data)
				response = HttpResponse(data)
			else:
				if request.method == "POST":
					if berkas_:
						if form.is_valid():
							ext = os.path.splitext(berkas_.name)[1]
							valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.jpeg', '.png', '.PDF', '.DOC', '.DOCX', '.JPG', '.JPEG', '.PNG']
							if not ext in valid_extensions:
								data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
								data = json.dumps(data)
								response = HttpResponse(data)
							else:
								try:
									p = Optikal.objects.get(id=request.COOKIES['id_pengajuan'])
									berkas = form.save(commit=False)
									kode = request.POST.get('kode')
									if kode == 'Akte Pendirian':
										berkas.nama_berkas = "Akte Pendirian "+p.no_pengajuan
										berkas.keterangan = "Akte Pendirian "+p.no_pengajuan
									elif kode == 'SK Pejabat Setempat':
										berkas.nama_berkas = "SK Pejabat Setempat "+p.no_pengajuan
										berkas.keterangan = "SK Pejabat Setempat "+p.no_pengajuan
									elif kode == 'IMB dan Izin Gangguan':
										berkas.nama_berkas = "IMB dan Izin Gangguan "+p.no_pengajuan
										berkas.keterangan = "IMB dan Izin Gangguan "+p.no_pengajuan
									elif kode == 'Surat Perjanjian Pemilik Dengan Refreksionis':
										berkas.nama_berkas = "Surat Perjanjian Pemilik Dengan Refreksionis "+p.no_pengajuan
										berkas.keterangan = "Surat Perjanjian Pemilik Dengan Refreksionis "+p.no_pengajuan
									elif kode == 'SK Tempat Tinggal':
										berkas.nama_berkas = "SK Tempat Tinggal "+p.no_pengajuan
										berkas.keterangan = "SK Tempat Tinggal "+p.no_pengajuan
									elif kode == 'Ijazah Refreksionis':
										berkas.nama_berkas = "Ijazah Refreksionis "+p.no_pengajuan
										berkas.keterangan = "Ijazah Refreksionis "+p.no_pengajuan
									elif kode == 'SK Sehat Dokter':
										berkas.nama_berkas = "SK Sehat Dokter "+p.no_pengajuan
										berkas.keterangan = "SK Sehat Dokter "+p.no_pengajuan
									elif kode == 'Pas Foto':
										berkas.nama_berkas = "Pas Foto "+p.no_pengajuan
										berkas.keterangan = "Pas Foto "+p.no_pengajuan
									elif kode == 'Surat Pernyataan Kerjasama':
										berkas.nama_berkas = "Surat Pernyataan Kerjasama "+p.no_pengajuan
										berkas.keterangan = "Surat Pernyataan Kerjasama "+p.no_pengajuan
									elif kode == 'Daftar Sarana Peralatan':
										berkas.nama_berkas = "Daftar Sarana Peralatan "+p.no_pengajuan
										berkas.keterangan = "Daftar Sarana Peralatan "+p.no_pengajuan
									elif kode == 'Daftar Pegawai':
										berkas.nama_berkas = "Daftar Pegawai "+p.no_pengajuan
										berkas.keterangan = "Daftar Pegawai "+p.no_pengajuan
									elif kode == 'Peta Lokasi':
										berkas.nama_berkas = "Peta Lokasi "+p.no_pengajuan
										berkas.keterangan = "Peta Lokasi "+p.no_pengajuan
									elif kode == 'Denah Ruangan':
										berkas.nama_berkas = "Denah Ruangan "+p.no_pengajuan
										berkas.keterangan = "Denah Ruangan "+p.no_pengajuan
									elif kode == 'SK Organisasi Profesi':
										berkas.nama_berkas = "SK Organisasi Profesi "+p.no_pengajuan
										berkas.keterangan = "SK Organisasi Profesi "+p.no_pengajuan
									
									if request.user.is_authenticated():
										berkas.created_by_id = request.user.id
									else:
										berkas.created_by_id = request.COOKIES['id_pemohon']
									berkas.save()
									p.berkas_terkait_izin.add(berkas)

									data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
											{'status_upload': 'ok'},
										]}
									data = json.dumps(data)
									response = HttpResponse(data)
								except ObjectDoesNotExist:
									data = {'Terjadi Kesalahan': [{'message': 'Pengajuan tidak ada dalam daftar'}]}
									data = json.dumps(data)
									response = HttpResponse(data)
						else:
							data = form.errors.as_json()
							response = HttpResponse(data)
					else:
						data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong'}]}
						data = json.dumps(data)
						response = HttpResponse(data)
				else:
					data = form.errors.as_json()
					response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def optikal_upload_dokumen_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': [] }
	return HttpResponse(json.dumps(data))

def ajax_load_berkas_optikal(request, id_pengajuan):
	url_berkas = []
	id_elemen = []
	nm_berkas =[]
	id_berkas =[]
	if id_pengajuan:
		try:
			pengajuan_obj = Optikal.objects.get(id=id_pengajuan)
			berkas_ = pengajuan_obj.berkas_terkait_izin.all()

			if berkas_:
				akte_pendirian = berkas_.filter(keterangan='Akte Pendirian '+pengajuan_obj.no_pengajuan).last()
				if akte_pendirian:
					url_berkas.append(akte_pendirian.berkas.url)
					id_elemen.append('akte_pendirian')
					nm_berkas.append(akte_pendirian.nama_berkas)
					id_berkas.append(akte_pendirian.id)
					pengajuan_obj.berkas_terkait_izin.add(akte_pendirian)

				sk_pejabat = berkas_.filter(keterangan='SK Pejabat Setempat '+pengajuan_obj.no_pengajuan).last()
				if sk_pejabat:
					url_berkas.append(sk_pejabat.berkas.url)
					id_elemen.append('sk_pejabat')
					nm_berkas.append(sk_pejabat.nama_berkas)
					id_berkas.append(sk_pejabat.id)
					pengajuan_obj.berkas_terkait_izin.add(sk_pejabat)

				izin_gangguan = berkas_.filter(keterangan='IMB dan Izin Gangguan '+pengajuan_obj.no_pengajuan).last()
				if izin_gangguan:
					url_berkas.append(izin_gangguan.berkas.url)
					id_elemen.append('izin_gangguan')
					nm_berkas.append(izin_gangguan.nama_berkas)
					id_berkas.append(izin_gangguan.id)
					pengajuan_obj.berkas_terkait_izin.add(izin_gangguan)

				surat_perjanjian_pemilik	 = berkas_.filter(keterangan='Surat Perjanjian Pemilik Dengan Refreksionis '+pengajuan_obj.no_pengajuan).last()
				if surat_perjanjian_pemilik	:
					url_berkas.append(surat_perjanjian_pemilik	.berkas.url)
					id_elemen.append('surat_perjanjian_pemilik	')
					nm_berkas.append(surat_perjanjian_pemilik	.nama_berkas)
					id_berkas.append(surat_perjanjian_pemilik	.id)
					pengajuan_obj.berkas_terkait_izin.add(surat_perjanjian_pemilik	)

				sk_tempat_tinggal = berkas_.filter(keterangan='SK Tempat Tinggal '+pengajuan_obj.no_pengajuan).last()
				if sk_tempat_tinggal:
					url_berkas.append(sk_tempat_tinggal.berkas.url)
					id_elemen.append('sk_tempat_tinggal')
					nm_berkas.append(sk_tempat_tinggal.nama_berkas)
					id_berkas.append(sk_tempat_tinggal.id)
					pengajuan_obj.berkas_terkait_izin.add(sk_tempat_tinggal)

				ijazah_refreksionis = berkas_.filter(keterangan='Ijazah Refreksionis '+pengajuan_obj.no_pengajuan).last()
				if ijazah_refreksionis:
					url_berkas.append(ijazah_refreksionis.berkas.url)
					id_elemen.append('ijazah_refreksionis')
					nm_berkas.append(ijazah_refreksionis.nama_berkas)
					id_berkas.append(ijazah_refreksionis.id)
					pengajuan_obj.berkas_terkait_izin.add(ijazah_refreksionis)

				sk_sehat = berkas_.filter(keterangan='SK Sehat Dokter '+pengajuan_obj.no_pengajuan).last()
				if sk_sehat:
					url_berkas.append(sk_sehat.berkas.url)
					id_elemen.append('sk_sehat')
					nm_berkas.append(sk_sehat.nama_berkas)
					id_berkas.append(sk_sehat.id)
					pengajuan_obj.berkas_terkait_izin.add(sk_sehat)

				pas_foto = berkas_.filter(keterangan='Pas Foto '+pengajuan_obj.no_pengajuan).last()
				if pas_foto:
					url_berkas.append(pas_foto.berkas.url)
					id_elemen.append('pas_foto')
					nm_berkas.append(pas_foto.nama_berkas)
					id_berkas.append(pas_foto.id)
					pengajuan_obj.berkas_terkait_izin.add(pas_foto)

				pernyataan_kerjasama = berkas_.filter(keterangan='Surat Pernyataan Kerjasama '+pengajuan_obj.no_pengajuan).last()
				if pernyataan_kerjasama:
					url_berkas.append(pernyataan_kerjasama.berkas.url)
					id_elemen.append('pernyataan_kerjasama')
					nm_berkas.append(pernyataan_kerjasama.nama_berkas)
					id_berkas.append(pernyataan_kerjasama.id)
					pengajuan_obj.berkas_terkait_izin.add(pernyataan_kerjasama)

				daftar_sarana = berkas_.filter(keterangan='Daftar Sarana Peralatan '+pengajuan_obj.no_pengajuan).last()
				if daftar_sarana:
					url_berkas.append(daftar_sarana.berkas.url)
					id_elemen.append('daftar_sarana')
					nm_berkas.append(daftar_sarana.nama_berkas)
					id_berkas.append(daftar_sarana.id)
					pengajuan_obj.berkas_terkait_izin.add(daftar_sarana)

				daftar_pegawai = berkas_.filter(keterangan='Daftar Pegawai '+pengajuan_obj.no_pengajuan).last()
				if daftar_pegawai:
					url_berkas.append(daftar_pegawai.berkas.url)
					id_elemen.append('daftar_pegawai')
					nm_berkas.append(daftar_pegawai.nama_berkas)
					id_berkas.append(daftar_pegawai.id)
					pengajuan_obj.berkas_terkait_izin.add(daftar_pegawai)

				peta_lokasi = berkas_.filter(keterangan='Peta Lokasi '+pengajuan_obj.no_pengajuan).last()
				if peta_lokasi:
					url_berkas.append(peta_lokasi.berkas.url)
					id_elemen.append('peta_lokasi')
					nm_berkas.append(peta_lokasi.nama_berkas)
					id_berkas.append(peta_lokasi.id)
					pengajuan_obj.berkas_terkait_izin.add(peta_lokasi)

				denah_ruangan = berkas_.filter(keterangan='Denah Ruangan '+pengajuan_obj.no_pengajuan).last()
				if denah_ruangan:
					url_berkas.append(denah_ruangan.berkas.url)
					id_elemen.append('denah_ruangan')
					nm_berkas.append(denah_ruangan.nama_berkas)
					id_berkas.append(denah_ruangan.id)
					pengajuan_obj.berkas_terkait_izin.add(denah_ruangan)

				sk_organisasi_profesi = berkas_.filter(keterangan='SK Organisasi Profesi '+pengajuan_obj.no_pengajuan).last()
				if sk_organisasi_profesi:
					url_berkas.append(sk_organisasi_profesi.berkas.url)
					id_elemen.append('sk_organisasi_profesi')
					nm_berkas.append(sk_organisasi_profesi.nama_berkas)
					id_berkas.append(sk_organisasi_profesi.id)
					pengajuan_obj.berkas_terkait_izin.add(sk_organisasi_profesi)


			data = {'success': True, 'pesan': 'Sukses.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': '' }
	response = HttpResponse(json.dumps(data))
	return response

def load_konfirmasi_optikal(request, id_pengajuan):
	data = {'success': False, 'pesan': 'Data tidak ditemukan.' }
	if id_pengajuan:
		try:
			pengajuan_obj = PengajuanIzin.objects.get(id=id_pengajuan)
			optikal_obj = Optikal.objects.filter(id=id_pengajuan).last()
			pengajuan_json = {}
			pemohon_json = {}
			optikal_json = {}
			if pengajuan_obj:
				pengajuan_json = pengajuan_obj.as_json()
				if pengajuan_obj.pemohon:
					pemohon_json = pengajuan_obj.pemohon.as_json()

				if optikal_obj:
					optikal_json = optikal_obj.as_json()

			data = {'success': True, 'pesan': 'Sukses.', 'data': { 'pengajuan_json':pengajuan_json, 'pemohon_json': pemohon_json, 'optikal_json': optikal_json}}
		except ObjectDoesNotExist:
			pass
	return HttpResponse(json.dumps(data))

def optikal_done(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = Optikal.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			pengajuan_.status = 6
			pengajuan_.save()
					
			data = {'success': True, 'pesan': 'Proses Selesai.' }
			response = HttpResponse(json.dumps(data))
			response.delete_cookie(key='id_pengajuan') # set cookie	
			response.delete_cookie(key='id_perusahaan') # set cookie	
			response.delete_cookie(key='nomor_ktp') # set cookie	
			response.delete_cookie(key='nomor_paspor') # set cookie	
			response.delete_cookie(key='id_pemohon') # set cookie	
			response.delete_cookie(key='id_kelompok_izin') # set cookie
			response.delete_cookie(key='npwp_perusahaan') # set cookie
			response.delete_cookie(key='id_jenis_pengajuan') # set cookie
			response.delete_cookie(key='kode_kelompok_jenis_izin') # set cookie
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def save_izin_mendirikan_klinik(request):
	data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			if 'id_kelompok_izin' in request.COOKIES.keys():
				try:
					jenis_klinik = request.POST.get('jenis_klinik')
					if jenis_klinik and jenis_klinik is not None:
						pengajuan_obj = MendirikanKlinik.objects.get(id=request.COOKIES['id_pengajuan'])

						form_mendirikan_klinik = MendirikanKlinikForm(request.POST, instance=pengajuan_obj)
						if form_mendirikan_klinik.is_valid():
							p = form_mendirikan_klinik.save(commit=False)
							p.save()
							pengajuan_obj.jenis_klinik_id = jenis_klinik
							pengajuan_obj.save()
							data = {'success': True, 'pesan': 'Data Izin Mendirikan Klinik berhasil tersimpan.'}
						else:
							data = form_mendirikan_klinik.errors.as_json()
							data = {'success': False, 'pesan': 'Data Izin Mendirikan Klinik gagal.', 'data': data}
					else:
						data = {'success': False, 'pesan': 'Jenis Izin Kosong, Perlu Diisi.'}
				except MendirikanKlinik.DoesNotExist:
					pass
	return HttpResponse(json.dumps(data))

def load_izin_mendirikan_klinik(request, id_pengajuan):
	data = {}
	response = {'success': False, 'pesan': 'Data Mendirikan Klinik berhasil tersimpan.', 'data': data}
	if id_pengajuan:
		pengajuan_obj = MendirikanKlinik.objects.filter(id=id_pengajuan).last()
		if pengajuan_obj:
			data = pengajuan_obj.as_json__mendirikan_klinik()
			response = {'success': True, 'pesan': 'Data Mendirikan Klinik berhasil tersimpan.', 'data': data}
	return HttpResponse(json.dumps(response))

def mendirikan_klinik_upload_dokumen_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': [] }
	return HttpResponse(json.dumps(data))

def upload_berkas_mendirikan_klinik(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			form = BerkasForm(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if berkas_._size > 4*1024*1024:
				data = {'Terjadi Kesalahan': [{'message': 'Ukuran file tidak boleh melebihi dari 4mb.'}]}
				data = json.dumps(data)
				response = HttpResponse(data)
			else:
				if request.method == "POST":
					if berkas_:
						if form.is_valid():
							ext = os.path.splitext(berkas_.name)[1]
							valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.jpeg', '.png', '.PDF', '.DOC', '.DOCX', '.JPG', '.JPEG', '.PNG']
							if not ext in valid_extensions:
								data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
								data = json.dumps(data)
								response = HttpResponse(data)
							else:
								try:
									p = MendirikanKlinik.objects.get(id=request.COOKIES['id_pengajuan'])
									berkas = form.save(commit=False)
									kode = request.POST.get('kode')
									if kode == 'KTP':
										berkas.nama_berkas = "KTP "+p.pemohon.get_ktp()
										berkas.keterangan = "KTP "+p.pemohon.get_ktp()
									elif kode == 'NPWP':
										berkas.nama_berkas = "NPWP "+p.no_pengajuan
										berkas.keterangan = "NPWP "+p.no_pengajuan
									elif kode == 'Pendirian Badan Hukum':
										berkas.nama_berkas = "Pendirian Badan Hukum "+p.no_pengajuan
										berkas.keterangan = "Pendirian Badan Hukum "+p.no_pengajuan
									elif kode == 'Sertifikat Tanah / Bangunan':
										berkas.nama_berkas = "Sertifikat Tanah / Bangunan "+p.no_pengajuan
										berkas.keterangan = "Sertifikat Tanah / Bangunan "+p.no_pengajuan
									elif kode == 'Dokumen Lingkungan':
										berkas.nama_berkas = "Dokumen Lingkungan "+p.no_pengajuan
										berkas.keterangan = "Dokumen Lingkungan "+p.no_pengajuan
									elif kode == 'Profil Klinik':
										berkas.nama_berkas = "Profil Klinik "+p.no_pengajuan
										berkas.keterangan = "Profil Klinik "+p.no_pengajuan
									elif kode == 'Gambar/Denah Bangunan':
										berkas.nama_berkas = "Gambar/Denah Bangunan "+p.no_pengajuan
										berkas.keterangan = "Gambar/Denah Bangunan "+p.no_pengajuan
									elif kode == 'IPPM':
										berkas.nama_berkas = "IPPM "+p.no_pengajuan
										berkas.keterangan = "IPPM "+p.no_pengajuan
									elif kode == 'Izin Mendirikan Bangunan (IMB)':
										berkas.nama_berkas = "Izin Mendirikan Bangunan (IMB) "+p.no_pengajuan
										berkas.keterangan = "Izin Mendirikan Bangunan (IMB) "+p.no_pengajuan
									elif kode == 'Izin Gangguan':
										berkas.nama_berkas = "Izin Gangguan "+p.no_pengajuan
										berkas.keterangan = "Izin Gangguan "+p.no_pengajuan
									elif kode == 'Izin Mendirikan Klinik lama':
										berkas.nama_berkas = "Izin Mendirikan Klinik lama "+p.no_pengajuan
										berkas.keterangan = "Izin Mendirikan Klinik lama "+p.no_pengajuan
									
									if request.user.is_authenticated():
										berkas.created_by_id = request.user.id
									else:
										berkas.created_by_id = request.COOKIES['id_pemohon']
									berkas.save()
									p.berkas_terkait_izin.add(berkas)

									data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
											{'status_upload': 'ok'},
										]}
									data = json.dumps(data)
									response = HttpResponse(data)
								except ObjectDoesNotExist:
									data = {'Terjadi Kesalahan': [{'message': 'Pengajuan tidak ada dalam daftar'}]}
									data = json.dumps(data)
									response = HttpResponse(data)
						else:
							data = form.errors.as_json()
							response = HttpResponse(data)
					else:
						data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong'}]}
						data = json.dumps(data)
						response = HttpResponse(data)
				else:
					data = form.errors.as_json()
					response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def ajax_load_berkas_mendirikan_klinik(request, id_pengajuan):
	url_berkas = []
	id_elemen = []
	nm_berkas =[]
	id_berkas =[]
	if id_pengajuan:
		try:
			pengajuan_obj = MendirikanKlinik.objects.get(id=id_pengajuan)
			berkas_ = pengajuan_obj.berkas_terkait_izin.all()

			if berkas_:
				ktp = berkas_.filter(keterangan="KTP "+pengajuan_obj.pemohon.get_ktp()).last()
				if ktp:
					url_berkas.append(ktp.berkas.url)
					id_elemen.append('ktp')
					nm_berkas.append(ktp.nama_berkas)
					id_berkas.append(ktp.id)
					pengajuan_obj.berkas_terkait_izin.add(ktp)

				npwp = berkas_.filter(keterangan='NPWP '+pengajuan_obj.no_pengajuan).last()
				if npwp:
					url_berkas.append(npwp.berkas.url)
					id_elemen.append('npwp')
					nm_berkas.append(npwp.nama_berkas)
					id_berkas.append(npwp.id)
					pengajuan_obj.berkas_terkait_izin.add(npwp)

				pendirian_hukum = berkas_.filter(keterangan='Pendirian Badan Hukum '+pengajuan_obj.no_pengajuan).last()
				if pendirian_hukum:
					url_berkas.append(pendirian_hukum.berkas.url)
					id_elemen.append('pendirian_hukum')
					nm_berkas.append(pendirian_hukum.nama_berkas)
					id_berkas.append(pendirian_hukum.id)
					pengajuan_obj.berkas_terkait_izin.add(pendirian_hukum)

				sertifikat_tanah = berkas_.filter(keterangan='Sertifikat Tanah / Bangunan '+pengajuan_obj.no_pengajuan).last()
				if sertifikat_tanah:
					url_berkas.append(sertifikat_tanah.berkas.url)
					id_elemen.append('sertifikat_tanah')
					nm_berkas.append(sertifikat_tanah.nama_berkas)
					id_berkas.append(sertifikat_tanah.id)
					pengajuan_obj.berkas_terkait_izin.add(sertifikat_tanah)

				dokumen_lingkungan = berkas_.filter(keterangan='Dokumen Lingkungan '+pengajuan_obj.no_pengajuan).last()
				if dokumen_lingkungan:
					url_berkas.append(dokumen_lingkungan.berkas.url)
					id_elemen.append('dokumen_lingkungan')
					nm_berkas.append(dokumen_lingkungan.nama_berkas)
					id_berkas.append(dokumen_lingkungan.id)
					pengajuan_obj.berkas_terkait_izin.add(dokumen_lingkungan)

				profil_klinik = berkas_.filter(keterangan='Profil Klinik '+pengajuan_obj.no_pengajuan).last()
				if profil_klinik:
					url_berkas.append(profil_klinik.berkas.url)
					id_elemen.append('profil_klinik')
					nm_berkas.append(profil_klinik.nama_berkas)
					id_berkas.append(profil_klinik.id)
					pengajuan_obj.berkas_terkait_izin.add(profil_klinik)

				gambar_bangunan = berkas_.filter(keterangan='Gambar/Denah Bangunan '+pengajuan_obj.no_pengajuan).last()
				if gambar_bangunan:
					url_berkas.append(gambar_bangunan.berkas.url)
					id_elemen.append('gambar_bangunan')
					nm_berkas.append(gambar_bangunan.nama_berkas)
					id_berkas.append(gambar_bangunan.id)
					pengajuan_obj.berkas_terkait_izin.add(gambar_bangunan)

				ippm = berkas_.filter(keterangan='IPPM '+pengajuan_obj.no_pengajuan).last()
				if ippm:
					url_berkas.append(ippm.berkas.url)
					id_elemen.append('ippm')
					nm_berkas.append(ippm.nama_berkas)
					id_berkas.append(ippm.id)
					pengajuan_obj.berkas_terkait_izin.add(ippm)

				imb = berkas_.filter(keterangan='Izin Mendirikan Bangunan (IMB) '+pengajuan_obj.no_pengajuan).last()
				if imb:
					url_berkas.append(imb.berkas.url)
					id_elemen.append('imb')
					nm_berkas.append(imb.nama_berkas)
					id_berkas.append(imb.id)
					pengajuan_obj.berkas_terkait_izin.add(imb)

				izin_gangguan = berkas_.filter(keterangan='Izin Gangguan '+pengajuan_obj.no_pengajuan).last()
				if izin_gangguan:
					url_berkas.append(izin_gangguan.berkas.url)
					id_elemen.append('izin_gangguan')
					nm_berkas.append(izin_gangguan.nama_berkas)
					id_berkas.append(izin_gangguan.id)
					pengajuan_obj.berkas_terkait_izin.add(izin_gangguan)

				izin_klinik_lama = berkas_.filter(keterangan='Izin Mendirikan Klinik lama '+pengajuan_obj.no_pengajuan).last()
				if izin_klinik_lama:
					url_berkas.append(izin_klinik_lama.berkas.url)
					id_elemen.append('izin_klinik_lama')
					nm_berkas.append(izin_klinik_lama.nama_berkas)
					id_berkas.append(izin_klinik_lama.id)
					pengajuan_obj.berkas_terkait_izin.add(izin_klinik_lama)

				
			data = {'success': True, 'pesan': 'Sukses.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': '' }
	response = HttpResponse(json.dumps(data))
	return response

def load_konfirmasi_mendirikan_klinik(request, id_pengajuan):
	data = {'success': False, 'pesan': 'Terjadi Kesalahan. Pengajuan Izin tidak ditemukan atau tidak ada dalam daftar.'}
	try:
		pengajuan_obj = MendirikanKlinik.objects.get(id=id_pengajuan)
		pemohon_json = {}
		if pengajuan_obj.pemohon:
			pemohon_json = pengajuan_obj.pemohon.as_json()
		data = {'success': True, 'pesan': 'Berhasil load data pengajuan izin.', 'data': {'pemohon_json': pemohon_json, 'pengajuan_json': pengajuan_obj.as_json(), 'detil_json': pengajuan_obj.as_json__mendirikan_klinik()}}
	except ObjectDoesNotExist:
		pass
	return HttpResponse(json.dumps(data))

def mendirikan_klinik_done(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = MendirikanKlinik.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			pengajuan_.status = 6
			pengajuan_.save()
					
			data = {'success': True, 'pesan': 'Proses Selesai.' }
			response = HttpResponse(json.dumps(data))
			response.delete_cookie(key='id_pengajuan') # set cookie	
			response.delete_cookie(key='id_perusahaan') # set cookie	
			response.delete_cookie(key='nomor_ktp') # set cookie	
			response.delete_cookie(key='nomor_paspor') # set cookie	
			response.delete_cookie(key='id_pemohon') # set cookie	
			response.delete_cookie(key='id_kelompok_izin') # set cookie
			response.delete_cookie(key='npwp_perusahaan') # set cookie
			response.delete_cookie(key='id_jenis_pengajuan') # set cookie
			response.delete_cookie(key='kode_kelompok_jenis_izin') # set cookie
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def save_izin_operasional_klinik(request):
	data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
	print 'asdasdasd'
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			print request.COOKIES['id_pengajuan']
			if 'id_kelompok_izin' in request.COOKIES.keys():
				try:
					jenis_klinik = request.POST.get('jenis_klinik')
					if jenis_klinik and jenis_klinik is not None:
						jenis_klinik_obj = request.POST.get('jenis_klinik')
						pengajuan_obj = OperasionalKlinik.objects.get(id=request.COOKIES['id_pengajuan'])
						form_operasional_klinik = OperasionalKlinikForm(request.POST, instance=pengajuan_obj)
						if form_operasional_klinik.is_valid():
							p = form_operasional_klinik.save(commit=False)
							p.save()
							data = {'success': True, 'pesan': 'Data Izin Operasional Klinik berhasil tersimpan.'}
						else:
							data = form_operasional_klinik.errors.as_json__operasional_klinik()
							data = {'success': False, 'pesan': 'Data Izin Operasional Klinik gagal.', 'data': data}
					else:
						data = {'success': False, 'pesan': 'Jenis Izin Kosong, Perlu Diisi.'}
				except OperasionalKlinik.DoesNotExist:
					pass
	return HttpResponse(json.dumps(data))

def load_izin_operasional_klinik(request, id_pengajuan):
	data = {}
	response = {'success': False, 'pesan': 'Data Operasional Klinik berhasil tersimpan.', 'data': data}
	if id_pengajuan:
		pengajuan_obj = OperasionalKlinik.objects.filter(id=id_pengajuan).last()
		if pengajuan_obj:
			data = pengajuan_obj.as_json__operasional_klinik()
			response = {'success': True, 'pesan': 'Data Operasional Klinik berhasil tersimpan.', 'data': data}
	return HttpResponse(json.dumps(response))

def operasional_klinik_upload_dokumen_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': [] }
	return HttpResponse(json.dumps(data))

def upload_berkas_operasional_klinik(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			form = BerkasForm(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if berkas_._size > 4*1024*1024:
				data = {'Terjadi Kesalahan': [{'message': 'Ukuran file tidak boleh melebihi dari 4mb.'}]}
				data = json.dumps(data)
				response = HttpResponse(data)
			else:
				if request.method == "POST":
					if berkas_:
						if form.is_valid():
							ext = os.path.splitext(berkas_.name)[1]
							valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.jpeg', '.png', '.PDF', '.DOC', '.DOCX', '.JPG', '.JPEG', '.PNG']
							if not ext in valid_extensions:
								data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
								data = json.dumps(data)
								response = HttpResponse(data)
							else:
								try:
									p = OperasionalKlinik.objects.get(id=request.COOKIES['id_pengajuan'])
									berkas = form.save(commit=False)
									kode = request.POST.get('kode')
									if kode == 'IMK':
										berkas.nama_berkas = "IMK "+p.no_pengajuan
										berkas.keterangan = "IMK "+p.no_pengajuan
									elif kode == 'Data klinik':
										berkas.nama_berkas = "Data klinik "+p.no_pengajuan
										berkas.keterangan = "Data klinik "+p.no_pengajuan
									elif kode == 'Surat Pernyataan':
										berkas.nama_berkas = "Surat Pernyataan "+p.no_pengajuan
										berkas.keterangan = "Surat Pernyataan "+p.no_pengajuan
									if kode == 'KTP':
										berkas.nama_berkas = "KTP "+p.pemohon.get_ktp()
										berkas.keterangan = "KTP "+p.pemohon.get_ktp()
									elif kode == 'NPWP':
										berkas.nama_berkas = "NPWP "+p.no_pengajuan
										berkas.keterangan = "NPWP "+p.no_pengajuan
									elif kode == 'Pendirian Badan Hukum':
										berkas.nama_berkas = "Pendirian Badan Hukum "+p.no_pengajuan
										berkas.keterangan = "Pendirian Badan Hukum "+p.no_pengajuan
									elif kode == 'Sertifikat Tanah / Bangunan':
										berkas.nama_berkas = "Sertifikat Tanah / Bangunan "+p.no_pengajuan
										berkas.keterangan = "Sertifikat Tanah / Bangunan "+p.no_pengajuan
									elif kode == 'Dokumen Lingkungan':
										berkas.nama_berkas = "Dokumen Lingkungan "+p.no_pengajuan
										berkas.keterangan = "Dokumen Lingkungan "+p.no_pengajuan
									elif kode == 'Profil Klinik':
										berkas.nama_berkas = "Profil Klinik "+p.no_pengajuan
										berkas.keterangan = "Profil Klinik "+p.no_pengajuan
									elif kode == 'Gambar/Denah Bangunan':
										berkas.nama_berkas = "Gambar/Denah Bangunan "+p.no_pengajuan
										berkas.keterangan = "Gambar/Denah Bangunan "+p.no_pengajuan
									elif kode == 'IPPM':
										berkas.nama_berkas = "IPPM "+p.no_pengajuan
										berkas.keterangan = "IPPM "+p.no_pengajuan
									elif kode == 'Izin Mendirikan Bangunan (IMB)':
										berkas.nama_berkas = "Izin Mendirikan Bangunan (IMB) "+p.no_pengajuan
										berkas.keterangan = "Izin Mendirikan Bangunan (IMB) "+p.no_pengajuan
									elif kode == 'Izin Gangguan':
										berkas.nama_berkas = "Izin Gangguan "+p.no_pengajuan
										berkas.keterangan = "Izin Gangguan "+p.no_pengajuan
									elif kode == 'Perjanjian Kerjasama':
										berkas.nama_berkas = "Perjanjian Kerjasama "+p.no_pengajuan
										berkas.keterangan = "Perjanjian Kerjasama "+p.no_pengajuan
									elif kode == 'Izin Mendirikan Klinik lama':
										berkas.nama_berkas = "Izin Mendirikan Klinik lama "+p.no_pengajuan
										berkas.keterangan = "Izin Mendirikan Klinik lama "+p.no_pengajuan
									elif kode == 'Data Perubahan Izin':
										berkas.nama_berkas = "Data Perubahan Izin "+p.no_pengajuan
										berkas.keterangan = "Data Perubahan Izin "+p.no_pengajuan
									
									if request.user.is_authenticated():
										berkas.created_by_id = request.user.id
									else:
										berkas.created_by_id = request.COOKIES['id_pemohon']
									berkas.save()
									p.berkas_terkait_izin.add(berkas)

									data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
											{'status_upload': 'ok'},
										]}
									data = json.dumps(data)
									response = HttpResponse(data)
								except ObjectDoesNotExist:
									data = {'Terjadi Kesalahan': [{'message': 'Pengajuan tidak ada dalam daftar'}]}
									data = json.dumps(data)
									response = HttpResponse(data)
						else:
							data = form.errors.as_json()
							response = HttpResponse(data)
					else:
						data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong'}]}
						data = json.dumps(data)
						response = HttpResponse(data)
				else:
					data = form.errors.as_json()
					response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def ajax_load_berkas_operasional_klinik(request, id_pengajuan):
	url_berkas = []
	id_elemen = []
	nm_berkas =[]
	id_berkas =[]
	if id_pengajuan:
		try:
			pengajuan_obj = OperasionalKlinik.objects.get(id=id_pengajuan)
			berkas_ = pengajuan_obj.berkas_terkait_izin.all()

			if berkas_:
				imk = berkas_.filter(keterangan='IMK '+pengajuan_obj.no_pengajuan).last()
				if imk:
					url_berkas.append(imk.berkas.url)
					id_elemen.append('imk')
					nm_berkas.append(imk.nama_berkas)
					id_berkas.append(imk.id)
					pengajuan_obj.berkas_terkait_izin.add(imk)

				data_klinik = berkas_.filter(keterangan='Data klinik '+pengajuan_obj.no_pengajuan).last()
				if data_klinik:
					url_berkas.append(data_klinik.berkas.url)
					id_elemen.append('data_klinik')
					nm_berkas.append(data_klinik.nama_berkas)
					id_berkas.append(data_klinik.id)
					pengajuan_obj.berkas_terkait_izin.add(data_klinik)

				surat_pernyataan = berkas_.filter(keterangan='Surat Pernyataan '+pengajuan_obj.no_pengajuan).last()
				if surat_pernyataan:
					url_berkas.append(surat_pernyataan.berkas.url)
					id_elemen.append('surat_pernyataan')
					nm_berkas.append(surat_pernyataan.nama_berkas)
					id_berkas.append(surat_pernyataan.id)
					pengajuan_obj.berkas_terkait_izin.add(surat_pernyataan)

				ktp = berkas_.filter(keterangan="KTP "+pengajuan_obj.pemohon.get_ktp()).last()
				if ktp:
					url_berkas.append(ktp.berkas.url)
					id_elemen.append('ktp')
					nm_berkas.append(ktp.nama_berkas)
					id_berkas.append(ktp.id)
					pengajuan_obj.berkas_terkait_izin.add(ktp)

				npwp = berkas_.filter(keterangan='NPWP '+pengajuan_obj.no_pengajuan).last()
				if npwp:
					url_berkas.append(npwp.berkas.url)
					id_elemen.append('npwp')
					nm_berkas.append(npwp.nama_berkas)
					id_berkas.append(npwp.id)
					pengajuan_obj.berkas_terkait_izin.add(npwp)

				pendirian_hukum = berkas_.filter(keterangan='Pendirian Badan Hukum '+pengajuan_obj.no_pengajuan).last()
				if pendirian_hukum:
					url_berkas.append(pendirian_hukum.berkas.url)
					id_elemen.append('pendirian_hukum')
					nm_berkas.append(pendirian_hukum.nama_berkas)
					id_berkas.append(pendirian_hukum.id)
					pengajuan_obj.berkas_terkait_izin.add(pendirian_hukum)

				sertifikat_tanah = berkas_.filter(keterangan='Sertifikat Tanah / Bangunan '+pengajuan_obj.no_pengajuan).last()
				if sertifikat_tanah:
					url_berkas.append(sertifikat_tanah.berkas.url)
					id_elemen.append('sertifikat_tanah')
					nm_berkas.append(sertifikat_tanah.nama_berkas)
					id_berkas.append(sertifikat_tanah.id)
					pengajuan_obj.berkas_terkait_izin.add(sertifikat_tanah)

				dokumen_lingkungan = berkas_.filter(keterangan='Dokumen Lingkungan '+pengajuan_obj.no_pengajuan).last()
				if dokumen_lingkungan:
					url_berkas.append(dokumen_lingkungan.berkas.url)
					id_elemen.append('dokumen_lingkungan')
					nm_berkas.append(dokumen_lingkungan.nama_berkas)
					id_berkas.append(dokumen_lingkungan.id)
					pengajuan_obj.berkas_terkait_izin.add(dokumen_lingkungan)

				profil_klinik = berkas_.filter(keterangan='Profil Klinik '+pengajuan_obj.no_pengajuan).last()
				if profil_klinik:
					url_berkas.append(profil_klinik.berkas.url)
					id_elemen.append('profil_klinik')
					nm_berkas.append(profil_klinik.nama_berkas)
					id_berkas.append(profil_klinik.id)
					pengajuan_obj.berkas_terkait_izin.add(profil_klinik)

				gambar_bangunan = berkas_.filter(keterangan='Gambar/Denah Bangunan '+pengajuan_obj.no_pengajuan).last()
				if gambar_bangunan:
					url_berkas.append(gambar_bangunan.berkas.url)
					id_elemen.append('gambar_bangunan')
					nm_berkas.append(gambar_bangunan.nama_berkas)
					id_berkas.append(gambar_bangunan.id)
					pengajuan_obj.berkas_terkait_izin.add(gambar_bangunan)

				ippm = berkas_.filter(keterangan='IPPM '+pengajuan_obj.no_pengajuan).last()
				if ippm:
					url_berkas.append(ippm.berkas.url)
					id_elemen.append('ippm')
					nm_berkas.append(ippm.nama_berkas)
					id_berkas.append(ippm.id)
					pengajuan_obj.berkas_terkait_izin.add(ippm)

				imb = berkas_.filter(keterangan='Izin Mendirikan Bangunan (IMB) '+pengajuan_obj.no_pengajuan).last()
				if imb:
					url_berkas.append(imb.berkas.url)
					id_elemen.append('imb')
					nm_berkas.append(imb.nama_berkas)
					id_berkas.append(imb.id)
					pengajuan_obj.berkas_terkait_izin.add(imb)

				izin_gangguan = berkas_.filter(keterangan='Izin Gangguan '+pengajuan_obj.no_pengajuan).last()
				if izin_gangguan:
					url_berkas.append(izin_gangguan.berkas.url)
					id_elemen.append('izin_gangguan')
					nm_berkas.append(izin_gangguan.nama_berkas)
					id_berkas.append(izin_gangguan.id)
					pengajuan_obj.berkas_terkait_izin.add(izin_gangguan)

				perjanjian_kerjasama = berkas_.filter(keterangan='Perjanjian Kerjasama '+pengajuan_obj.no_pengajuan).last()
				if perjanjian_kerjasama:
					url_berkas.append(perjanjian_kerjasama.berkas.url)
					id_elemen.append('perjanjian_kerjasama')
					nm_berkas.append(perjanjian_kerjasama.nama_berkas)
					id_berkas.append(perjanjian_kerjasama.id)
					pengajuan_obj.berkas_terkait_izin.add(perjanjian_kerjasama)

				izin_klinik_lama = berkas_.filter(keterangan='Izin Mendirikan Klinik lama '+pengajuan_obj.no_pengajuan).last()
				if izin_klinik_lama:
					url_berkas.append(izin_klinik_lama.berkas.url)
					id_elemen.append('izin_klinik_lama')
					nm_berkas.append(izin_klinik_lama.nama_berkas)
					id_berkas.append(izin_klinik_lama.id)
					pengajuan_obj.berkas_terkait_izin.add(izin_klinik_lama)

				data_perubahan_izin = berkas_.filter(keterangan='Data Perubahan Izin '+pengajuan_obj.no_pengajuan).last()
				if data_perubahan_izin:
					url_berkas.append(data_perubahan_izin.berkas.url)
					id_elemen.append('data_perubahan_izin')
					nm_berkas.append(data_perubahan_izin.nama_berkas)
					id_berkas.append(data_perubahan_izin.id)
					pengajuan_obj.berkas_terkait_izin.add(data_perubahan_izin)

				
			data = {'success': True, 'pesan': 'Sukses.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': '' }
	response = HttpResponse(json.dumps(data))
	return response

def load_konfirmasi_operasional_klinik(request, id_pengajuan):
	data = {'success': False, 'pesan': 'Terjadi Kesalahan. Pengajuan Izin tidak ditemukan atau tidak ada dalam daftar.'}
	try:
		pengajuan_obj = OperasionalKlinik.objects.get(id=id_pengajuan)
		pemohon_json = {}
		if pengajuan_obj.pemohon:
			pemohon_json = pengajuan_obj.pemohon.as_json()
		data = {'success': True, 'pesan': 'Berhasil load data pengajuan izin.', 'data': {'pemohon_json': pemohon_json, 'pengajuan_json': pengajuan_obj.as_json(), 'detil_json': pengajuan_obj.as_json__operasional_klinik()}}
	except ObjectDoesNotExist:
		pass
	return HttpResponse(json.dumps(data))

def operasional_klinik_done(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			print request.COOKIES['id_pengajuan']
			pengajuan_ = OperasionalKlinik.objects.filter(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan']).last()
			print pengajuan_
			pengajuan_.status = 6
			pengajuan_.save()
					
			data = {'success': True, 'pesan': 'Proses Selesai.' }
			response = HttpResponse(json.dumps(data))
			response.delete_cookie(key='id_pengajuan') # set cookie	
			response.delete_cookie(key='id_perusahaan') # set cookie	
			response.delete_cookie(key='nomor_ktp') # set cookie	
			response.delete_cookie(key='nomor_paspor') # set cookie	
			response.delete_cookie(key='id_pemohon') # set cookie	
			response.delete_cookie(key='id_kelompok_izin') # set cookie
			response.delete_cookie(key='npwp_perusahaan') # set cookie
			response.delete_cookie(key='id_jenis_pengajuan') # set cookie
			response.delete_cookie(key='kode_kelompok_jenis_izin') # set cookie
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response
