from izin.izin_forms import PengajuanReklameForm
import json
import os
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from master.models import Berkas
from izin.models import DetilReklame, PengajuanIzin
from izin.izin_forms import UploadBerkasPendukungForm
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.decorators.http import require_POST
from jfu.http import upload_receive, UploadResponse, JFUResponse

def reklame_detilreklame_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			print request.COOKIES['id_pengajuan']
			pengajuan_ = DetilReklame.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			detilReklame = PengajuanReklameForm(request.POST, instance=pengajuan_)
			if detilReklame.is_valid():
				pengajuan_.perusahaan_id  = request.COOKIES['id_perusahaan']
				pengajuan_.save()
				letak_ = pengajuan_.letak_pemasangan + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
				ukuran_ = str(int(pengajuan_.panjang))+"x"+str(int(pengajuan_.lebar))+"x"+str(int(pengajuan_.sisi))
				awal = pengajuan_.tanggal_mulai
				akhir = pengajuan_.tanggal_akhir
				selisih = akhir-awal
				data = {'success': True,
						'pesan': 'Data Reklame berhasil disimpan. Proses Selanjutnya.',
						'data': [
						{'jenis_reklame': pengajuan_.jenis_reklame.jenis_reklame},
						{'judul_reklame': pengajuan_.judul_reklame},
						{'ukuran': ukuran_},
						{'letak_pemasangan': letak_},
						{'selisih': selisih.days}]}
				data = json.dumps(data)
				response = HttpResponse(json.dumps(data))
			else:
				data = detilSIUP.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response

def reklame_upload_berkas_pendukung(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			form = UploadBerkasPendukungForm(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if request.method == "POST":
				if berkas_:
					if form.is_valid():
						ext = os.path.splitext(berkas_.name)[1]
						valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.png']
						if not ext in valid_extensions:
							data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
						else:
							try:
								p = PengajuanIzin.objects.get(id=request.COOKIES['id_pengajuan'])
								berkas = form.save(commit=False)
								if request.POST.get('aksi') == "1":
									berkas.nama_berkas = "Gambar Kontruksi Pemasangan Reklame "+p.no_pengajuan
									berkas.keterangan = "Gambar Kontruksi Pemasangan Reklame"
								elif request.POST.get('aksi') == "2":
									berkas.nama_berkas = "Gambar Foto Lokasi Pemasangan Reklame "+p.no_pengajuan
									berkas.keterangan = "Gambar Foto Lokasi Pemasangan Reklame"
								elif request.POST.get('aksi') == "3":
									berkas.nama_berkas = "Gambar Denah Lokasi Pemasangan Rekalame "+p.no_pengajuan
									berkas.keterangan = "Gambar Denah Lokasi Pemasangan Rekalame"
								elif request.POST.get('aksi') == "4":
									berkas.nama_berkas = "Surat Ketetapan Pajak Daerah (SKPD) "+p.no_pengajuan
									berkas.keterangan = "Surat Ketetapan Pajak Daerah (SKPD)"
								elif request.POST.get('aksi') == "5":
									berkas.nama_berkas = "Surat Setoran Pajak Daerah (SSPD) "+p.no_pengajuan
									berkas.keterangan = "Surat Setoran Pajak Daerah (SSPD)"
								elif request.POST.get('aksi') == "6":
									berkas.nama_berkas = "Rekomendasi dari Kantor SATPOL PP "+p.no_pengajuan
									berkas.keterangan = "Rekomendasi dari Kantor SATPOL PP"
								elif request.POST.get('aksi') == "7":
									berkas.nama_berkas = "Berita Acara Perusahaan(BAP) Tim Perizinan "+p.no_pengajuan
									berkas.keterangan = "Berita Acara Perusahaan(BAP) Tim Perizinan"
								elif request.POST.get('aksi') == "8":
									berkas.nama_berkas = "Surat Perjanjian Kesepakatan "+p.no_pengajuan
									berkas.keterangan = "Surat Perjanjian Kesepakatan"
								else:
									berkas.nama_berkas = "Berkas Tambahan "+p.no_pengajuan
									berkas.keterangan = "Berkas Tambahan"
									
								if request.user.is_authenticated():
									berkas.created_by_id = request.user.id
								else:
									berkas.created_by_id = request.COOKIES['id_pemohon']
								berkas.save()
								p.berkas_tambahan.add(berkas)

								data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
										{'status_upload': 'ok'},
									]}
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

def reklame_upload_dokumen_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': [] }
	return HttpResponse(json.dumps(data))

