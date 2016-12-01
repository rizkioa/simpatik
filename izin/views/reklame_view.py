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
									berkas.nama_berkas = "Berkas Tambahan Reklame"+p.no_pengajuan
									berkas.keterangan = "Berkas Tambahan Reklame"
									
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

def reklame_done(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilSIUP.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
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
			response.delete_cookie(key='id_legalitas') # set cookie
			response.delete_cookie(key='id_legalitas_perubahan') # set cookie
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response


def ajax_load_berkas_reklame(request, id_pengajuan):
	url_berkas = []
	id_elemen = []
	nm_berkas =[]
	id_berkas =[]
	if id_pengajuan:
		try:
			p = PengajuanIzin.objects.get(id=request.COOKIES['id_pengajuan'])
			gambar_kontruksi = Berkas.objects.filter(nama_berkas="Gambar Kontruksi Pemasangan Reklame "+p.no_pengajuan)
			if gambar_kontruksi.exists():
				gambar_kontruksi = gambar_kontruksi.last()
				url_berkas.append(gambar_kontruksi.berkas.url)
				id_elemen.append('gambar_konstruksi_pemasangan_reklame')
				nm_berkas.append("Gambar Kontruksi Pemasangan Reklame "+p.no_pengajuan)
				id_berkas.append(gambar_kontruksi.id)

			gambar_foto_lokasi = Berkas.objects.filter(nama_berkas="Gambar Foto Lokasi Pemasangan Reklame "+p.no_pengajuan)
			if gambar_foto_lokasi.exists():
				gambar_foto_lokasi = gambar_foto_lokasi.last()
				url_berkas.append(gambar_foto_lokasi.berkas.url)
				id_elemen.append('gambar_foto_lokasi_pemasangan_reklame')
				nm_berkas.append("Gambar Foto Lokasi Pemasangan Reklame "+p.no_pengajuan)
				id_berkas.append(gambar_foto_lokasi.id)

			gambar_denah_lokasi = Berkas.objects.filter(nama_berkas="Gambar Denah Lokasi Pemasangan Rekalame "+p.no_pengajuan)
			if gambar_denah_lokasi.exists():
				gambar_denah_lokasi = gambar_denah_lokasi.last()
				url_berkas.append(gambar_denah_lokasi.berkas.url)
				id_elemen.append('gambar_denah_lokasi_pemasangan_reklame')
				nm_berkas.append("Gambar Denah Lokasi Pemasangan Rekalame "+p.no_pengajuan)
				id_berkas.append(gambar_denah_lokasi.id)

			surat_ketetapan_pajak = Berkas.objects.filter(nama_berkas="Surat Ketetapan Pajak Daerah (SKPD) "+p.no_pengajuan)
			if surat_ketetapan_pajak.exists():
				surat_ketetapan_pajak = surat_ketetapan_pajak.last()
				url_berkas.append(surat_ketetapan_pajak.berkas.url)
				id_elemen.append('surat_ketetapan_pajak_daerah')
				nm_berkas.append("Surat Ketetapan Pajak Daerah (SKPD) "+p.no_pengajuan)
				id_berkas.append(surat_ketetapan_pajak.id)

			surat_setoran_pajak_daerah = Berkas.objects.filter(nama_berkas="Surat Setoran Pajak Daerah (SSPD) "+p.no_pengajuan)
			if surat_setoran_pajak_daerah.exists():
				surat_setoran_pajak_daerah = surat_setoran_pajak_daerah.last()
				url_berkas.append(surat_setoran_pajak_daerah.berkas.url)
				id_elemen.append('surat_setoran_pajak_daerah')
				nm_berkas.append("Surat Setoran Pajak Daerah (SSPD) "+p.no_pengajuan)
				id_berkas.append(surat_setoran_pajak_daerah.id)

			rekomendasi_satpo_pp = Berkas.objects.filter(nama_berkas="Rekomendasi dari Kantor SATPOL PP "+p.no_pengajuan)
			if rekomendasi_satpo_pp.exists():
				rekomendasi_satpo_pp = rekomendasi_satpo_pp.last()
				url_berkas.append(rekomendasi_satpo_pp.berkas.url)
				id_elemen.append('rekomendasi_satpol_pp')
				nm_berkas.append("Rekomendasi dari Kantor SATPOL PP "+p.no_pengajuan)
				id_berkas.append(rekomendasi_satpo_pp.id)

			bap_perizinan = Berkas.objects.filter(nama_berkas="Berita Acara Perusahaan(BAP) Tim Perizinan "+p.no_pengajuan)
			if bap_perizinan.exists():
				bap_perizinan = bap_perizinan.last()
				url_berkas.append(bap_perizinan.berkas.url)
				id_elemen.append('berita_acara_perusahaan')
				nm_berkas.append("Berita Acara Perusahaan(BAP) Tim Perizinan "+p.no_pengajuan)
				id_berkas.append(bap_perizinan.id)

			surat_perjanjian_kesepakatan = Berkas.objects.filter(nama_berkas="Surat Perjanjian Kesepakatan "+p.no_pengajuan)
			if surat_perjanjian_kesepakatan.exists():
				surat_perjanjian_kesepakatan = surat_perjanjian_kesepakatan.last()
				url_berkas.append(surat_perjanjian_kesepakatan.berkas.url)
				id_elemen.append('surat_perjanjian')
				nm_berkas.append("Surat Perjanjian Kesepakatan "+p.no_pengajuan)
				id_berkas.append(surat_perjanjian_kesepakatan.id)

			berkas_tambahan = Berkas.objects.filter(nama_berkas="Berkas Tambahan Reklame"+p.no_pengajuan)
			if berkas_tambahan.exists():
				berkas_tambahan = berkas_tambahan.last()
				url_berkas.append(berkas_tambahan.berkas.url)
				id_elemen.append('tambahan')
				nm_berkas.append("Berkas Tambahan Reklame"+p.no_pengajuan)
				id_berkas.append(berkas_tambahan.id)

			data = {'success': True, 'pesan': 'berkas pendukung Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': '' }
			
		
	response = HttpResponse(json.dumps(data))
	return response

def ajax_delete_berkas_reklame(request, id_berkas):
	if id_berkas:
		try:
			b = Berkas.objects.get(id=id_berkas)
			data = {'success': True, 'pesan': str(b)+" berhasil dihapus" }
			b.delete()
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': 'Berkas Tidak Ada' }
			
		response = HttpResponse(json.dumps(data))
		return response

	return False
		
