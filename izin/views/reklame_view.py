from izin.izin_forms import PengajuanReklameForm,DetilReklameIzinForm,UploadBerkasPendukungForm
import json
import os
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from master.models import Berkas
from izin.models import DetilReklame, PengajuanIzin,JenisPermohonanIzin,KelompokJenisIzin,DetilReklameIzin
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

def reklame_detilreklame_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			kelompok_izin = KelompokJenisIzin.objects.get(kode="503.03.01/")
			pengajuan_ = DetilReklame.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			detilReklame = PengajuanReklameForm(request.POST, instance=pengajuan_)
			if detilReklame.is_valid():

				if 'id_perusahaan' in request.COOKIES.keys():
					if request.COOKIES['id_perusahaan'] != '0':
						if pengajuan_.jenis_reklame.jenis_reklame == "Permanen":
							pengajuan_.kelompok_jenis_izin = kelompok_izin
							pengajuan_.perusahaan_id  = request.COOKIES['id_perusahaan']
							pengajuan_.save()
						else:
							pengajuan_.perusahaan_id  = request.COOKIES['id_perusahaan']
							pengajuan_.save()
					else:
						if pengajuan_.jenis_reklame.jenis_reklame == "Permanen":
							pengajuan_.kelompok_jenis_izin = kelompok_izin
						pengajuan_.save()

				data = {'success': True,
						'pesan': 'Data Reklame berhasil disimpan. Proses Selanjutnya.',
						'data': {}}
				data = json.dumps(data)
				response = HttpResponse(json.dumps(data))
			else:
				data = detilReklame.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response

def reklame_detilreklame_permanen_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys() or 'jenis_permohonan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '' or request.COOKIES['jenis_permohonan'] != '':
			jenis_pengajuan_ = JenisPermohonanIzin.objects.get(jenis_permohonan_izin=request.COOKIES['id_jenis_pengajuan'])
			id_jenis_pengajuan_ = jenis_pengajuan_.id

			if request.user.is_anonymous():
				created_by = request.COOKIES['id_pemohon']
			else:
				created_by =  request.user.id
			if request.COOKIES['id_pengajuan_reklame'] != '':
				pengajuan_ = DetilReklame.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan_reklame'])
			else:	
				pengajuan_ = DetilReklame.objects.create(status=11,pemohon_id=request.COOKIES['id_pemohon'],kelompok_jenis_izin_id=14,jenis_permohonan_id=id_jenis_pengajuan_,created_by_id=created_by)
			detilReklame = PengajuanReklameForm(request.POST, instance=pengajuan_)
			if detilReklame.is_valid():
				if 'id_perusahaan' in request.COOKIES.keys():
					if request.COOKIES['id_perusahaan'] != '0':
						if pengajuan_.jenis_reklame.jenis_reklame == "Permanen":
							pengajuan_.kelompok_jenis_izin = kelompok_izin
							pengajuan_.perusahaan_id  = request.COOKIES['id_perusahaan']
							pengajuan_.save()
						else:
							pengajuan_.perusahaan_id  = request.COOKIES['id_perusahaan']
							pengajuan_.save()
					else:
						pengajuan_.save()
				letak_ = pengajuan_.letak_pemasangan + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
				ukuran_ = str(int(pengajuan_.panjang))+"x"+str(int(pengajuan_.lebar))+"x"+str(int(pengajuan_.sisi))
				if pengajuan_.tanggal_mulai:
					awal = pengajuan_.tanggal_mulai
				else:
					awal = 0
				if pengajuan_.tanggal_akhir:
					akhir = pengajuan_.tanggal_akhir
				else:
					akhir = 0
				
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
				response.set_cookie(key='id_pengajuan_reklame', value=pengajuan_.id)
			else:
				data = detilReklame.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def detail_izin_reklame_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		pengajuan_ = DetilReklame.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
		if request.COOKIES['id_pengajuan'] != '':
			detail_izin_reklame = DetilReklameIzinForm(request.POST)
			if request.method == 'POST':
				if detail_izin_reklame.is_valid():
					p = detail_izin_reklame.save(commit=False)
					p.detil_reklame = pengajuan_
					p.save()
					data = {'success': True,
							'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
							'data': {'id_detil_reklame':p.id, 'kecamatan': p.desa.kecamatan.nama_kecamatan, 'desa':p.desa.nama_desa }}
					response = HttpResponse(json.dumps(data))
				else:
					data = detail_izin_reklame.errors.as_json()
					response = HttpResponse(data)
			else:
				detail_izin_reklame = DetilReklameIzinForm()
				data = {'Terjadi Kesalahan': [{'message': 'What....!!!!!'}]}
				response = HttpResponse(json.dumps(data))
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def edit_detail_izin_reklame(request,id_detail_izin_reklame):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilReklame.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			p = DetilReklameIzin.objects.get(id=id_detail_izin_reklame)
			detail_izin_reklame = DetilReklameIzinForm(request.POST,instance=p)
			if request.method == 'POST':
				if detail_izin_reklame.is_valid():
					r = detail_izin_reklame.save(commit=False)
					r.detil_reklame = pengajuan_
					r.save()
					data = {'success': True,
							'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
							'data': {'id_detil_reklame':p.id, 'kecamatan': p.desa.kecamatan.nama_kecamatan, 'desa':p.desa.nama_desa }}
					response = HttpResponse(json.dumps(data))
				else:
					data = detail_izin_reklame.errors.as_json()
			else:
				detail_izin_reklame = DetilReklameIzinForm()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def delete_detail_izin_reklame(request,id_detail_izin_reklame):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			tag_to_delete = get_object_or_404(DetilReklameIzin, id=id_detail_izin_reklame)
			tag_to_delete.delete()
			data = {'success': True,
					'pesan': 'Data berhasil Dihapus.'}
			response = HttpResponse(json.dumps(data))
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
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
						valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.jpeg', '.png', '.PDF', '.DOC', '.DOCX', '.JPG', '.JPEG', '.PNG']
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
								p.berkas_terkait_izin.add(berkas)

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
	# print request.COOKIES.keys()
	if 'id_pengajuan' in request.COOKIES.keys():
		# print "HALo"
		if request.COOKIES['id_pengajuan'] != '':
			# print "ASEM"
			pengajuan_ = DetilReklame.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
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
			data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan Kosong.'}]}
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
				p.berkas_terkait_izin.add(gambar_kontruksi)

			gambar_foto_lokasi = Berkas.objects.filter(nama_berkas="Gambar Foto Lokasi Pemasangan Reklame "+p.no_pengajuan)
			if gambar_foto_lokasi.exists():
				gambar_foto_lokasi = gambar_foto_lokasi.last()
				url_berkas.append(gambar_foto_lokasi.berkas.url)
				id_elemen.append('gambar_foto_lokasi_pemasangan_reklame')
				nm_berkas.append("Gambar Foto Lokasi Pemasangan Reklame "+p.no_pengajuan)
				id_berkas.append(gambar_foto_lokasi.id)
				p.berkas_terkait_izin.add(gambar_foto_lokasi)

			gambar_denah_lokasi = Berkas.objects.filter(nama_berkas="Gambar Denah Lokasi Pemasangan Rekalame "+p.no_pengajuan)
			if gambar_denah_lokasi.exists():
				gambar_denah_lokasi = gambar_denah_lokasi.last()
				url_berkas.append(gambar_denah_lokasi.berkas.url)
				id_elemen.append('gambar_denah_lokasi_pemasangan_reklame')
				nm_berkas.append("Gambar Denah Lokasi Pemasangan Rekalame "+p.no_pengajuan)
				id_berkas.append(gambar_denah_lokasi.id)
				p.berkas_terkait_izin.add(gambar_denah_lokasi)

			surat_ketetapan_pajak = Berkas.objects.filter(nama_berkas="Surat Ketetapan Pajak Daerah (SKPD) "+p.no_pengajuan)
			if surat_ketetapan_pajak.exists():
				surat_ketetapan_pajak = surat_ketetapan_pajak.last()
				url_berkas.append(surat_ketetapan_pajak.berkas.url)
				id_elemen.append('surat_ketetapan_pajak_daerah')
				nm_berkas.append("Surat Ketetapan Pajak Daerah (SKPD) "+p.no_pengajuan)
				id_berkas.append(surat_ketetapan_pajak.id)
				p.berkas_terkait_izin.add(surat_ketetapan_pajak)

			surat_setoran_pajak_daerah = Berkas.objects.filter(nama_berkas="Surat Setoran Pajak Daerah (SSPD) "+p.no_pengajuan)
			if surat_setoran_pajak_daerah.exists():
				surat_setoran_pajak_daerah = surat_setoran_pajak_daerah.last()
				url_berkas.append(surat_setoran_pajak_daerah.berkas.url)
				id_elemen.append('surat_setoran_pajak_daerah')
				nm_berkas.append("Surat Setoran Pajak Daerah (SSPD) "+p.no_pengajuan)
				id_berkas.append(surat_setoran_pajak_daerah.id)
				p.berkas_terkait_izin.add(surat_setoran_pajak_daerah)

			rekomendasi_satpo_pp = Berkas.objects.filter(nama_berkas="Rekomendasi dari Kantor SATPOL PP "+p.no_pengajuan)
			if rekomendasi_satpo_pp.exists():
				rekomendasi_satpo_pp = rekomendasi_satpo_pp.last()
				url_berkas.append(rekomendasi_satpo_pp.berkas.url)
				id_elemen.append('rekomendasi_satpol_pp')
				nm_berkas.append("Rekomendasi dari Kantor SATPOL PP "+p.no_pengajuan)
				id_berkas.append(rekomendasi_satpo_pp.id)
				p.berkas_terkait_izin.add(rekomendasi_satpo_pp)

			bap_perizinan = Berkas.objects.filter(nama_berkas="Berita Acara Perusahaan(BAP) Tim Perizinan "+p.no_pengajuan)
			if bap_perizinan.exists():
				bap_perizinan = bap_perizinan.last()
				url_berkas.append(bap_perizinan.berkas.url)
				id_elemen.append('berita_acara_perusahaan')
				nm_berkas.append("Berita Acara Perusahaan(BAP) Tim Perizinan "+p.no_pengajuan)
				id_berkas.append(bap_perizinan.id)
				p.berkas_terkait_izin.add(bap_perizinan)

			surat_perjanjian_kesepakatan = Berkas.objects.filter(nama_berkas="Surat Perjanjian Kesepakatan "+p.no_pengajuan)
			if surat_perjanjian_kesepakatan.exists():
				surat_perjanjian_kesepakatan = surat_perjanjian_kesepakatan.last()
				url_berkas.append(surat_perjanjian_kesepakatan.berkas.url)
				id_elemen.append('surat_perjanjian')
				nm_berkas.append("Surat Perjanjian Kesepakatan "+p.no_pengajuan)
				id_berkas.append(surat_perjanjian_kesepakatan.id)
				p.berkas_terkait_izin.add(surat_perjanjian_kesepakatan)

			berkas_tambahan = Berkas.objects.filter(nama_berkas="Berkas Tambahan Reklame"+p.no_pengajuan)
			if berkas_tambahan.exists():
				berkas_tambahan = berkas_tambahan.last()
				url_berkas.append(berkas_tambahan.berkas.url)
				id_elemen.append('tambahan')
				nm_berkas.append("Berkas Tambahan Reklame"+p.no_pengajuan)
				id_berkas.append(berkas_tambahan.id)
				p.berkas_terkait_izin.add(berkas_tambahan)

			data = {'success': True, 'pesan': 'berkas pendukung Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': '' }
			
		
	response = HttpResponse(json.dumps(data))
	return response

def ajax_delete_berkas_reklame(request, id_berkas):
	data = {'success': False, 'pesan': 'Terjadi kesalahan, data tidak ditemukan.' }
	if id_berkas:
		try:
			pengajuan_obj = PengajuanIzin.objects.get(id=request.COOKIES.get('id_pengajuan'))
			try:
				b = Berkas.objects.get(id=id_berkas)
				data = {'success': True, 'pesan': str(b)+" berhasil dihapus" }
				# pengajuan_obj.berkas_terkait_izin.remove(b)
				b.delete()
			except ObjectDoesNotExist:
				data = {'success': False, 'pesan': 'Berkas Tidak Ada' }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': 'Pengajuan Izin tidak ditemukan.'}
			
		response = HttpResponse(json.dumps(data))
		return response
		
def load_data_detail_izin_reklame(request,id_detail_izin_reklame):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			try:
				pengajuan_ = DetilReklame.objects.get(id=id_detail_izin_reklame)
				if pengajuan_.tipe_reklame:
					id_tipe_reklame = str(pengajuan_.tipe_reklame.id)
				else:
					id_tipe_reklame = ""

				id_judul_reklame = pengajuan_.judul_reklame

				if pengajuan_.jenis_reklame:
					id_jenis_reklame = str(pengajuan_.jenis_reklame.id)
				else:
					id_jenis_reklame = ""

				id_panjang = str(pengajuan_.panjang)
				id_lebar = str(pengajuan_.lebar)
				id_sisi = str(pengajuan_.sisi)
				id_letak_pemasangan = pengajuan_.letak_pemasangan
				id_jumlah = pengajuan_.jumlah
				if pengajuan_.desa:
					id_kecamatan = str(pengajuan_.desa.kecamatan.id)
					id_desa = str(pengajuan_.desa.id)
				else:
					id_desa = ""
					id_kecamatan = ""
				if pengajuan_.tanggal_mulai:
					id_tanggal_mulai = pengajuan_.tanggal_mulai.strftime("%d-%m-%Y")
				else:
					id_tanggal_mulai = ""
				if pengajuan_.tanggal_akhir:
					id_tanggal_akhir = pengajuan_.tanggal_akhir.strftime("%d-%m-%Y")
				else:
					id_tanggal_akhir = ""

				data = {'success': True,'data': {
				'id_tipe_reklame': id_tipe_reklame,
				'id_jenis_reklame': id_jenis_reklame,
				'id_judul_reklame': id_judul_reklame,
				'id_panjang': id_panjang,
				'id_lebar': id_lebar,
				'id_sisi': id_sisi,
				'id_letak_pemasangan': id_letak_pemasangan,
				'id_jumlah': id_jumlah,
				'id_kecamatan': id_kecamatan,
				'id_desa': id_desa,
				'id_tanggal_mulai': id_tanggal_mulai,
				'id_tanggal_akhir': id_tanggal_akhir,
				}}
				response = HttpResponse(json.dumps(data))
			except ObjectDoesNotExist:
				data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
				data = json.dumps(data)
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	return response

def load_data_lokasi_detail_izin_reklame(request, id_detail_izin_reklame):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilReklameIzin.objects.get(id=id_detail_izin_reklame)
			id_desa = 0
			id_kecamatan = 0
			if pengajuan_.desa:
				id_desa = pengajuan_.desa.id
				id_kecamatan = pengajuan_.desa.kecamatan.id
			data = {'success': True,'data': {
				'id_desa': id_desa,
				'id_kecamatan': id_kecamatan,
			}}
			response = HttpResponse(json.dumps(data))
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data pengajuan tidak terdaftar.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response


def load_data_tabel_detil_reklame(request,id_detil_reklame):
    if 'id_pengajuan' in request.COOKIES.keys():
        if request.COOKIES['id_pengajuan'] != '':
            data = []
            i = DetilReklameIzin.objects.filter(detil_reklame_id=request.COOKIES['id_pengajuan'])
            data = [ob.as_json() for ob in i]
            response = HttpResponse(json.dumps(data), content_type="application/json")
    return response