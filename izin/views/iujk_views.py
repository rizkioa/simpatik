from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import json
import os

from izin.models import PaketPekerjaan, DetilIUJK, AnggotaBadanUsaha
from perusahaan.models import Perusahaan
from master.models import Berkas
from izin.iujk_forms import PaketPekerjaanForm, DetilIUJKForm, DataAnggotaForm, BerkasFom
from izin.izin_forms import LegalitasPerusahaanForm, LegalitasPerusahaanPerubahanForm



def iujk_paketpekerjaan_save(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			PaketPekerjaan_ = PaketPekerjaanForm(request.POST)
			if PaketPekerjaan_.is_valid():
				p = PaketPekerjaan_.save(commit=False)
				p.detil_iujk_id = request.COOKIES['id_pengajuan']
				p.save()

				data = {'success': True, 
				'pesan': 'Paket Pekerjaan Berhasil Disimpan.',
				'data': [
							{'id': p.id},
							{'klasifikasi_usaha': p.klasifikasi_usaha},
							{'nama_paket_pekerjaan': p.nama_paket_pekerjaan},
							{'tahun': p.tahun},
							{'nilai_paket_pekerjaan': 'Rp. '+'{:,.2f}'.format(float(p.nilai_paket_pekerjaan))},
							{'nilai_str': str(p.nilai_paket_pekerjaan)},
							{'delete':False},
						]
				}
				data = json.dumps(data)
				response = HttpResponse(data)
			else:
				data = PaketPekerjaan_.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	# response.set_cookie(key='id_detail_siup', value=pengajuan_.id)
	return response

def iujk_paketpekerjaan_edit(request, id_paket_):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			paket_ = PaketPekerjaan.objects.get(id=id_paket_)
			PaketPekerjaan_ = PaketPekerjaanForm(request.POST, instance=paket_)
			if PaketPekerjaan_.is_valid():
				p = PaketPekerjaan_.save(commit=False)
				p.detil_iujk_id = request.COOKIES['id_pengajuan']
				p.save()

				data = {'success': True, 
				'pesan': 'Perubahan Paket Pekerjaan Berhasil Disimpan.',
				'data': [
							{'id': p.id},
							{'klasifikasi_usaha': p.klasifikasi_usaha},
							{'nama_paket_pekerjaan': p.nama_paket_pekerjaan},
							{'tahun': p.tahun},
							{'nilai_paket_pekerjaan': 'Rp. '+'{:,.2f}'.format(float(p.nilai_paket_pekerjaan))},
							{'nilai_str': str(p.nilai_paket_pekerjaan)},
							{'delete':True},
						]
				}
				data = json.dumps(data)
				response = HttpResponse(data)
			else:
				data = PaketPekerjaan_.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	# response.set_cookie(key='id_detail_siup', value=pengajuan_.id)
	return response


# IUJK DETIL TIDAK ADA LEGALITAS
def iujk_detiliujk_save(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilIUJK.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			DetilIUJKForm_ = DetilIUJKForm(request.POST, instance=pengajuan_)
			if DetilIUJKForm_.is_valid():
				iujk = DetilIUJKForm_.save(commit=False)
				iujk.perusahaan_id = request.COOKIES['id_perusahaan']
				iujk.save()
				data = {'success': True, 
					'pesan': 'Data IUJK Berhasil Disimpan.',
					'data': []
				}
				data = json.dumps(data)
				response = HttpResponse(data)
			else:
				data = DetilIUJKForm_.errors.as_json()
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

def iujk_legalitas_perusahaan_save(request):
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			if 'id_pengajuan' in request.COOKIES.keys():
				if request.COOKIES['id_pengajuan'] != '':
					pengajuan_ = DetilIUJK.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
					if request.POST.get('onoffswitch_pendirian') == 'on':
						form = LegalitasPerusahaanForm(request.POST)
						if form.is_valid():
							f = form.save(commit=False)
							f.perusahaan_id = request.COOKIES['id_perusahaan']
							if request.user.is_authenticated():
								f.created_by_id = request.user.id
							else:
								f.created_by_id = request.COOKIES['id_pemohon']
							f.save()
							pengajuan_.legalitas.add(f)
							data = {'success': True, 'pesan': 'Legalitas Perusahaan berhasil disimpan. Proses Selanjutnya.', 'data': [
								{'jenis_legalitas': f.jenis_legalitas.jenis_legalitas},
								{'nama_notaris': f.nama_notaris},
								{'alamat_notaris': f.alamat},
								{'telephone_notaris': f.telephone},
								{'nomor_pengesahaan': f.nomor_pengesahan},
								{'tanggal_pengesahan': str(f.tanggal_pengesahan)}
								]}
							data = json.dumps(data)
							response = HttpResponse(data)
							response.set_cookie(key='id_legalitas', value=f.id)

							if request.POST.get('onoffswitch') == 'on':
								formperubahan = LegalitasPerusahaanPerubahanForm(request.POST)
								
								if formperubahan.is_valid():
									if request.user.is_authenticated():
										created = request.user.id
									else:
										created = request.COOKIES['id_pemohon']
									legalitas = Legalitas(
										created_by_id = created,	
										jenis_legalitas_id = 2,
										perusahaan_id = request.COOKIES['id_perusahaan'],
										nama_notaris=request.POST.get('nama_notaris_perubahan'), 
										alamat=request.POST.get('alamat_notaris_perubahan'), 
										telephone=request.POST.get('telephone_notaris_perubahan'), 
										nomor_pengesahan=request.POST.get('nomor_pengesahan_perubahan'), 
										tanggal_pengesahan=formperubahan.cleaned_data['tanggal_pengesahan_perubahan'])
									legalitas.save()
									pengajuan_.legalitas.add(legalitas)
									data = {'success': True, 'pesan': 'Legalitas Perusahaan berhasil disimpan. Proses Selanjutnya.', 'data': [
										# # legalitas perubahaan
										{'jenis_legalitas_perubahan': legalitas.jenis_legalitas.jenis_legalitas},
										{'nama_notaris_perubahan': legalitas.nama_notaris},
										{'alamat_notaris_perubahan': legalitas.alamat},
										{'telephone_notaris_perubahan': legalitas.telephone},
										{'nomor_pengesahaan_perubahan': legalitas.nomor_pengesahan},
										{'tanggal_pengesahan_perubahan': str(legalitas.tanggal_pengesahan)}
										]}
									data = json.dumps(data)
									response = HttpResponse(data)
									response.set_cookie(key='id_legalitas_perubahan', value=legalitas.id)
								else:
									data = formperubahan.errors.as_json()
									response = HttpResponse(data)
						# else:
						# 	data = {'Terjadi Kesalahan': [{'message': 'Data Perusahaan tidak ditemukan/data kosong'}]}
						# 	data = json.dumps(data)
						# 	response = HttpResponse(data)

						else:
							data = form.errors.as_json()
							response = HttpResponse(data)
					else:
						pengajuan_.jenis_pengajuan = 1
						pengajuan_.save()
						data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': []}
						data = json.dumps(data)
						response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
				data = json.dumps(data)
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response


def penanggung_jawab_save_bu(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		# print request.POST
		# print request.FILES
		# print os.path.splitext(request.FILES.get('berkas_foto').name)[1]
		if request.COOKIES['id_pengajuan'] != '0':
			form_ = DataAnggotaForm(request.POST)
			if form_.is_valid():
				# ext = os.path.splitext(berkas_.name)[1]
				valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.png']
				if os.path.splitext(request.FILES.get('berkas_foto').name)[1] in valid_extensions:
					if os.path.splitext(request.FILES.get('berkas_ktp').name)[1] in valid_extensions:
						if os.path.splitext(request.FILES.get('berkas_pernyataan').name)[1] in valid_extensions:
							if os.path.splitext(request.FILES.get('berkas_merangkap').name)[1] in valid_extensions:
								da_ = form_.save(commit=False)
								da_.detil_iujk_id = request.COOKIES['id_pengajuan']
								da_.jenis_anggota_badan = 'Direktur / Penanggung Jawab Badan Usaha'
								da_.save()

								da_.berkas_tambahan.create(nama_berkas="Berkas FOTO 4X6 "+da_.nama, berkas=request.FILES.get('berkas_foto'))
								da_.berkas_tambahan.create(nama_berkas="Berkas KTP "+da_.nama, berkas=request.FILES.get('berkas_ktp'))
								da_.berkas_tambahan.create(nama_berkas="Berkas Pernyataan bukan PNS/TNI/POLRI "+da_.nama, berkas=request.FILES.get('berkas_pernyataan'))
								da_.berkas_tambahan.create(nama_berkas="Berkas Tidak Merangkap/Bekerja Pada BU Lain "+da_.nama, berkas=request.FILES.get('berkas_merangkap'))
								
								# berkas_ = ", ".join(str(row.nama_berkas) for row in da_.berkas_tambahan.all().order_by('id'))
								# print request.META['HTTP_REFERER']
								berkas_ = ", ".join(str(row.berkas.url) for row in da_.berkas_tambahan.all().order_by('id'))

								data = {'success': True, 'pesan': request.POST.get('nama')+' berhasil disimpan. Proses Selanjutnya.', 
										'data': [
										# # legalitas perubahaan
											{ 'id': da_.id },
											{ 'nama': da_.nama },
											{ 'berkas': berkas_}
										]}

								data = json.dumps(data)
								response = HttpResponse(data)

							else:
								data = {'Terjadi Kesalahan': [{'message': 'Berkas Pernyataan Tidak Merangkap format tidak sesuai (*.pdf, *.doc, *.docx, *.jpg, *.png)'}]}
								data = json.dumps(data)
								response = HttpResponse(data)

						else:
							data = {'Terjadi Kesalahan': [{'message': 'Berkas Pernyataan bukan PNS/TNI/POLRI format tidak sesuai (*.pdf, *.doc, *.docx, *.jpg, *.png)'}]}
							data = json.dumps(data)
							response = HttpResponse(data)

					else:
						data = {'Terjadi Kesalahan': [{'message': 'Berkas Pernyataan bukan PNS/TNI/POLRI format tidak sesuai (*.pdf, *.doc, *.docx, *.jpg, *.png)'}]}
						data = json.dumps(data)
						response = HttpResponse(data)

				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas Foto format tidak sesuai (*.pdf, *.doc, *.docx, *.jpg, *.png)'}]}
					data = json.dumps(data)
					response = HttpResponse(data)

			else:
				data = form_.errors.as_json()
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

def penanggung_jawab_delete_bu(request):
	id_ = request.POST.get('id')
	if id_:
		try:
			obj = AnggotaBadanUsaha.objects.get(id = id_)
			obj.berkas_tambahan.all().delete()
			pesan_ = "Anggota Badan Usaha "+str(obj.nama)+" Berhasil Dihapus"
			data = {'success': True, 'pesan': pesan_, 'id':obj.id}
			obj.delete()
		except AnggotaBadanUsaha.DoesNotExist:
			data = {'success': False, 'pesan':'Anggota Badan Usaha Tidak ada'}
	else:
		data = {'success': False, 'pesan':'Anggota Badan Usaha Kosong'}

	data = json.dumps(data)
	response = HttpResponse(data)
	# print response

	return response


def penanggung_jawab_teknik_save_bu(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		# print request.POST
		# print request.FILES
		if request.COOKIES['id_pengajuan'] != '0':
			form_ = DataAnggotaForm(request.POST)
			if form_.is_valid():
				valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.png']
				if os.path.splitext(request.FILES.get('berkas_foto').name)[1] in valid_extensions:
					if os.path.splitext(request.FILES.get('berkas_ktp').name)[1] in valid_extensions:
						if os.path.splitext(request.FILES.get('ijazah_sma').name)[1] in valid_extensions:
							if os.path.splitext(request.FILES.get('ska_skt').name)[1] in valid_extensions:
								if os.path.splitext(request.FILES.get('berkas_merangkap').name)[1] in valid_extensions:
									da_ = form_.save(commit=False)
									da_.detil_iujk_id = request.COOKIES['id_pengajuan']
									da_.jenis_anggota_badan = 'Penanggung Jawab Teknik Badan Usaha'
									da_.save()


									da_.berkas_tambahan.create(nama_berkas="Berkas FOTO 4X6 "+da_.nama, berkas=request.FILES.get('berkas_foto'))
									da_.berkas_tambahan.create(nama_berkas="Berkas KTP "+da_.nama, berkas=request.FILES.get('berkas_ktp'))
									da_.berkas_tambahan.create(nama_berkas="Berkas Ijazah SMA "+da_.nama, berkas=request.FILES.get('ijazah_sma'))
									da_.berkas_tambahan.create(nama_berkas="Berkas SKA/SKT "+da_.nama, berkas=request.FILES.get('ska_skt'))
									da_.berkas_tambahan.create(nama_berkas="Berkas Tidak Merangkap/Bekerja Pada BU Lain "+da_.nama, berkas=request.FILES.get('berkas_merangkap'))
									
									# berkas_ = ", ".join(str(row.nama_berkas) for row in da_.berkas_tambahan.all().order_by('id'))
									# print request.META['HTTP_REFERER']
									berkas_ = ", ".join(str(row.berkas.url) for row in da_.berkas_tambahan.all().order_by('id'))

									data = {'success': True, 'pesan': request.POST.get('nama')+' berhasil disimpan. Proses Selanjutnya.', 
											'data': [
											# # legalitas perubahaan
												{ 'id': da_.id },
												{ 'nama': da_.nama },
												{ 'berkas': berkas_}
											]}

									data = json.dumps(data)
									response = HttpResponse(data)
								else:
									data = {'Terjadi Kesalahan': [{'message': 'Berkas Pernyataan Tidak Merangkap format tidak sesuai (*.pdf, *.doc, *.docx, *.jpg, *.png)'}]}
									data = json.dumps(data)
									response = HttpResponse(data)
							else:
								data = {'Terjadi Kesalahan': [{'message': 'Berkas SKA/SKT format tidak sesuai (*.pdf, *.doc, *.docx, *.jpg, *.png)'}]}
								data = json.dumps(data)
								response = HttpResponse(data)
						else:
							data = {'Terjadi Kesalahan': [{'message': 'Berkas Ijazah SMA format tidak sesuai (*.pdf, *.doc, *.docx, *.jpg, *.png)'}]}
							data = json.dumps(data)
							response = HttpResponse(data)
					else:
						data = {'Terjadi Kesalahan': [{'message': 'Berkas KTP format tidak sesuai (*.pdf, *.doc, *.docx, *.jpg, *.png)'}]}
						data = json.dumps(data)
						response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas Foto format tidak sesuai (*.pdf, *.doc, *.docx, *.jpg, *.png)'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
					
			else:
				data = form_.errors.as_json()
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

def penanggung_jawab_non_teknik_save_bu(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		# print request.POST
		# print request.FILES
		if request.COOKIES['id_pengajuan'] != '0':
			form_ = DataAnggotaForm(request.POST)
			if form_.is_valid():
				valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.png']
				if os.path.splitext(request.FILES.get('berkas_foto').name)[1] in valid_extensions:
					if os.path.splitext(request.FILES.get('berkas_ktp').name)[1] in valid_extensions:
						if os.path.splitext(request.FILES.get('ijazah_sma').name)[1] in valid_extensions:
							da_ = form_.save(commit=False)
							da_.detil_iujk_id = request.COOKIES['id_pengajuan']
							da_.jenis_anggota_badan = 'Tenaga Non Teknik'
							da_.save()

							da_.berkas_tambahan.create(nama_berkas="Berkas FOTO 4X6 "+da_.nama, berkas=request.FILES.get('berkas_foto'))
							da_.berkas_tambahan.create(nama_berkas="Berkas KTP "+da_.nama, berkas=request.FILES.get('berkas_ktp'))
							da_.berkas_tambahan.create(nama_berkas="Berkas Ijazah SMA "+da_.nama, berkas=request.FILES.get('ijazah_sma'))

							berkas_ = ", ".join(str(row.berkas.url) for row in da_.berkas_tambahan.all().order_by('id'))

							data = {'success': True, 'pesan': request.POST.get('nama')+' berhasil disimpan. Proses Selanjutnya.', 
									'data': [
									# # legalitas perubahaan
										{ 'id': da_.id },
										{ 'nama': da_.nama },
										{ 'berkas': berkas_}
									]}

							data = json.dumps(data)
							response = HttpResponse(data)
								
						else:
							data = {'Terjadi Kesalahan': [{'message': 'Berkas Ijazah SMA format tidak sesuai (*.pdf, *.doc, *.docx, *.jpg, *.png)'}]}
							data = json.dumps(data)
							response = HttpResponse(data)
					else:
						data = {'Terjadi Kesalahan': [{'message': 'Berkas KTP format tidak sesuai (*.pdf, *.doc, *.docx, *.jpg, *.png)'}]}
						data = json.dumps(data)
						response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas Foto format tidak sesuai (*.pdf, *.doc, *.docx, *.jpg, *.png)'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
					
			else:
				data = form_.errors.as_json()
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

def penanggung_jawab_next(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		# print request.POST
		# print request.FILES
		if request.COOKIES['id_pengajuan'] != '0':

			data = {}

			da_ = AnggotaBadanUsaha.objects.filter(detil_iujk__id=request.COOKIES['id_pengajuan'], jenis_anggota_badan='Direktur / Penanggung Jawab Badan Usaha')
			if len(da_) > 0 :
				da_t = AnggotaBadanUsaha.objects.filter(detil_iujk__id=request.COOKIES['id_pengajuan'], jenis_anggota_badan='Penanggung Jawab Teknik Badan Usaha')
				if len(da_t) > 0 :
					da_n = AnggotaBadanUsaha.objects.filter(detil_iujk__id=request.COOKIES['id_pengajuan'], jenis_anggota_badan='Tenaga Non Teknik')
					if len(da_n) > 0 :
						data['success'] = True
						data['pesan'] = 'Data Anggota Selesai, Proses Selanjutnya'
					else:
						data['Terjadi Kesalahan'] = [{'message': 'Tenaga Non Teknik Belum Ada'}]
				else:
					data['Terjadi Kesalahan'] = [{'message': 'Penanggung Jawab Teknik Badan Usaha Belum Ada'}]
			else:
				data['Terjadi Kesalahan'] = [{'message': 'Direktur / Penanggung Jawab Badan Usaha Belum Ada'}]


			data = json.dumps(data)
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


def upload_sertifikat_badan_usaha(request):
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			form = BerkasFom(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if request.method == "POST":
				if berkas_:
					if form.is_valid():
						ext = os.path.splitext(berkas_.name)[1]
						valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.png']
						if not ext in valid_extensions:
							data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
							data = json.dumps(data)
							response = HttpResponse(data)
						else:
							try:
								d = DetilIUJK.objects.get(id=request.COOKIES['id_pengajuan'])
								p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
								berkas = form.save(commit=False)
								berkas.nama_berkas = "Sertifikat Badan Usaha "+p.nama_perusahaan
								berkas.keterangan = "sertifikat Badan Usaha"+p.nama_perusahaan
								if request.user.is_authenticated():
									berkas.created_by_id = request.user.id
								else:
									berkas.created_by_id = request.COOKIES['id_pemohon']
								berkas.save()
								p.berkas_npwp = berkas
								p.save()
								d.berkas_npwp_perusahaan = berkas
								d.save()
								data = {'success': True, 'pesan': 'Sertifikat Badan Usaha '+p.nama_perusahaan+' berhasil diupload' ,'data': [
									{'status_upload': 'ok'},
								]}
							except ObjectDoesNotExist:
								data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar.'}]}					
							data = json.dumps(data)
							response = HttpResponse(data)
					else:
						data = form.errors.as_json()
						response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong.'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = form.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload Sertifikat Badan Usaha, Perusahaan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload Sertifikat Badan Usaha, Perusahaan tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response	

def upload_kartu_teknis_badan_usaha(request):
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			form = BerkasFom(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if request.method == "POST":
				if berkas_:
					if form.is_valid():
						ext = os.path.splitext(berkas_.name)[1]
						valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.png']
						if not ext in valid_extensions:
							data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
							data = json.dumps(data)
							response = HttpResponse(data)
						else:
							try:
								d = DetilIUJK.objects.get(id=request.COOKIES['id_pengajuan'])
								p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
								berkas = form.save(commit=False)
								berkas.nama_berkas = "Kartu Teknis Badan Usaha "+p.nama_perusahaan
								berkas.keterangan = "Kartu Teknis Usaha"+p.nama_perusahaan
								if request.user.is_authenticated():
									berkas.created_by_id = request.user.id
								else:
									berkas.created_by_id = request.COOKIES['id_pemohon']
								berkas.save()
								p.berkas_npwp = berkas
								p.save()
								d.berkas_npwp_perusahaan = berkas
								d.save()
								data = {'success': True, 'pesan': 'Kartu Teknis Badan Usaha '+p.nama_perusahaan+'Berhasil diupload' ,'data': [
									{'status_upload': 'ok'},
								]}
							except ObjectDoesNotExist:
								data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar.'}]}					
							data = json.dumps(data)
							response = HttpResponse(data)
					else:
						data = form.errors.as_json()
						response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong.'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = form.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload Kartu Teknis Badan Usaha, Perusahaan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload Kartu Teknis Badan Usaha, Perusahaan tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response	


def upload_pernyataan_pengikat_badan_usaha(request):
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			form = BerkasFom(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if request.method == "POST":
				if berkas_:
					if form.is_valid():
						ext = os.path.splitext(berkas_.name)[1]
						valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.png']
						if not ext in valid_extensions:
							data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
							data = json.dumps(data)
							response = HttpResponse(data)
						else:
							try:
								d = DetilIUJK.objects.get(id=request.COOKIES['id_pengajuan'])
								p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
								berkas = form.save(commit=False)
								berkas.nama_berkas = "Surat Pernyataaan Pengikatan Diri PJT-BU "+p.nama_perusahaan
								berkas.keterangan = "Surat Pernyataaan Pengikatan Diri PJT-BU "+p.nama_perusahaan
								if request.user.is_authenticated():
									berkas.created_by_id = request.user.id
								else:
									berkas.created_by_id = request.COOKIES['id_pemohon']
								berkas.save()
								p.berkas_npwp = berkas
								p.save()
								d.berkas_npwp_perusahaan = berkas
								d.save()
								data = {'success': True, 'pesan': 'Surat Pernyataaan Pengikatan Diri PJT-BU '+p.nama_perusahaan+' Berhasil diupload' ,'data': [
									{'status_upload': 'ok'},
								]}
							except ObjectDoesNotExist:
								data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar.'}]}					
							data = json.dumps(data)
							response = HttpResponse(data)
					else:
						data = form.errors.as_json()
						response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong.'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = form.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload Surat Pernyataaan Pengikatan Diri PJT-BU, Perusahaan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload Surat Pernyataaan Pengikatan Diri PJT-BU, Perusahaan tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response	

def upload_pernyataan_badan_usaha(request):
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			form = BerkasFom(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if request.method == "POST":
				if berkas_:
					if form.is_valid():
						ext = os.path.splitext(berkas_.name)[1]
						valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.png']
						if not ext in valid_extensions:
							data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
							data = json.dumps(data)
							response = HttpResponse(data)
						else:
							try:
								d = DetilIUJK.objects.get(id=request.COOKIES['id_pengajuan'])
								p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
								berkas = form.save(commit=False)
								berkas.nama_berkas = "Surat Peryataan Pengikatan Diri Penanggung Jawab BUJK "+p.nama_perusahaan
								berkas.keterangan = "Surat Peryataan Pengikatan Diri Penanggung Jawab BUJK "+p.nama_perusahaan
								if request.user.is_authenticated():
									berkas.created_by_id = request.user.id
								else:
									berkas.created_by_id = request.COOKIES['id_pemohon']
								berkas.save()
								p.berkas_npwp = berkas
								p.save()
								d.berkas_npwp_perusahaan = berkas
								d.save()
								data = {'success': True, 'pesan': 'Surat Peryataan Pengikatan Diri Penanggung Jawab BUJK '+p.nama_perusahaan+' Berhasil diupload' ,'data': [
									{'status_upload': 'ok'},
								]}
							except ObjectDoesNotExist:
								data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar.'}]}					
							data = json.dumps(data)
							response = HttpResponse(data)
					else:
						data = form.errors.as_json()
						response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong.'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = form.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload Surat Peryataan Pengikatan Diri Penanggung Jawab BUJK, Perusahaan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload Surat Peryataan Pengikatan Diri Penanggung Jawab BUJK, Perusahaan tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response	

def upload_npwp_badan_usaha(request):
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			form = BerkasFom(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if request.method == "POST":
				if berkas_:
					if form.is_valid():
						ext = os.path.splitext(berkas_.name)[1]
						valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.png']
						if not ext in valid_extensions:
							data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
							data = json.dumps(data)
							response = HttpResponse(data)
						else:
							try:
								d = DetilIUJK.objects.get(id=request.COOKIES['id_pengajuan'])
								p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
								berkas = form.save(commit=False)
								berkas.nama_berkas = "NPWP "+p.nama_perusahaan
								berkas.keterangan = "NPWP "+p.nama_perusahaan
								if request.user.is_authenticated():
									berkas.created_by_id = request.user.id
								else:
									berkas.created_by_id = request.COOKIES['id_pemohon']
								berkas.save()
								p.berkas_npwp = berkas
								p.save()
								d.berkas_npwp_perusahaan = berkas
								d.save()
								data = {'success': True, 'pesan': 'NPWP '+p.nama_perusahaan+' Berhasil diupload' ,'data': [
									{'status_upload': 'ok'},
								]}
							except ObjectDoesNotExist:
								data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar.'}]}					
							data = json.dumps(data)
							response = HttpResponse(data)
					else:
						data = form.errors.as_json()
						response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong.'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = form.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload NPWP, Perusahaan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload NPWP, Perusahaan tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def upload_keterangan_domisili_badan_usaha(request):
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			form = BerkasFom(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if request.method == "POST":
				if berkas_:
					if form.is_valid():
						ext = os.path.splitext(berkas_.name)[1]
						valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.png']
						if not ext in valid_extensions:
							data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
							data = json.dumps(data)
							response = HttpResponse(data)
						else:
							try:
								d = DetilIUJK.objects.get(id=request.COOKIES['id_pengajuan'])
								p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
								berkas = form.save(commit=False)
								berkas.nama_berkas = "Surat Keterangan Domisili Badan Usaha dari Kantor Desa Setempat "+p.nama_perusahaan
								berkas.keterangan = "Surat Keterangan Domisili Badan Usaha dari Kantor Desa Setempat "+p.nama_perusahaan
								if request.user.is_authenticated():
									berkas.created_by_id = request.user.id
								else:
									berkas.created_by_id = request.COOKIES['id_pemohon']
								berkas.save()
								p.berkas_npwp = berkas
								p.save()
								d.berkas_npwp_perusahaan = berkas
								d.save()
								data = {'success': True, 'pesan': 'Surat Keterangan Domisili Badan Usaha dari Kantor Desa Setempat '+p.nama_perusahaan+' Berhasil diupload' ,'data': [
									{'status_upload': 'ok'},
								]}
							except ObjectDoesNotExist:
								data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar.'}]}					
							data = json.dumps(data)
							response = HttpResponse(data)
					else:
						data = form.errors.as_json()
						response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong.'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = form.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload Surat Keterangan Domisili Badan Usaha dari Kantor Desa Setempat, Perusahaan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload Surat Keterangan Domisili Badan Usaha dari Kantor Desa Setempat, Perusahaan tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response	

def upload_denah_lokasi_badan_usaha(request):
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			form = BerkasFom(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if request.method == "POST":
				if berkas_:
					if form.is_valid():
						ext = os.path.splitext(berkas_.name)[1]
						valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.png']
						if not ext in valid_extensions:
							data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
							data = json.dumps(data)
							response = HttpResponse(data)
						else:
							try:
								d = DetilIUJK.objects.get(id=request.COOKIES['id_pengajuan'])
								p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
								berkas = form.save(commit=False)
								berkas.nama_berkas = "Gambar denah lokasi/posisi badan usaha "+p.nama_perusahaan
								berkas.keterangan = "Gambar denah lokasi/posisi badan usaha "+p.nama_perusahaan
								if request.user.is_authenticated():
									berkas.created_by_id = request.user.id
								else:
									berkas.created_by_id = request.COOKIES['id_pemohon']
								berkas.save()
								p.berkas_npwp = berkas
								p.save()
								d.berkas_npwp_perusahaan = berkas
								d.save()
								data = {'success': True, 'pesan': 'Gambar denah lokasi/posisi badan usaha '+p.nama_perusahaan+' Berhasil diupload' ,'data': [
									{'status_upload': 'ok'},
								]}
							except ObjectDoesNotExist:
								data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar.'}]}					
							data = json.dumps(data)
							response = HttpResponse(data)
					else:
						data = form.errors.as_json()
						response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong.'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = form.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload Gambar denah lokasi/posisi badan usaha, Perusahaan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload Gambar denah lokasi/posisi badan usaha, Perusahaan tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response	

def upload_foto_papan_badan_usaha(request):
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			form = BerkasFom(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if request.method == "POST":
				if berkas_:
					if form.is_valid():
						ext = os.path.splitext(berkas_.name)[1]
						valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.png']
						if not ext in valid_extensions:
							data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
							data = json.dumps(data)
							response = HttpResponse(data)
						else:
							try:
								d = DetilIUJK.objects.get(id=request.COOKIES['id_pengajuan'])
								p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
								berkas = form.save(commit=False)
								berkas.nama_berkas = "Gambar/foto papan nama badan usaha "+p.nama_perusahaan
								berkas.keterangan = "Gambar/foto papan nama badan usaha "+p.nama_perusahaan
								if request.user.is_authenticated():
									berkas.created_by_id = request.user.id
								else:
									berkas.created_by_id = request.COOKIES['id_pemohon']
								berkas.save()
								p.berkas_npwp = berkas
								p.save()
								d.berkas_npwp_perusahaan = berkas
								d.save()
								data = {'success': True, 'pesan': 'Gambar/foto papan nama badan usaha '+p.nama_perusahaan+' Berhasil diupload' ,'data': [
									{'status_upload': 'ok'},
								]}
							except ObjectDoesNotExist:
								data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar.'}]}					
							data = json.dumps(data)
							response = HttpResponse(data)
					else:
						data = form.errors.as_json()
						response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong.'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = form.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload Gambar/foto papan nama badan usaha, Perusahaan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload Gambar/foto papan nama badan usaha, Perusahaan tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response	

def upload_akta_pendirian_badan_usaha(request):
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			form = BerkasFom(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if request.method == "POST":
				if berkas_:
					if form.is_valid():
						ext = os.path.splitext(berkas_.name)[1]
						valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.png']
						if not ext in valid_extensions:
							data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
							data = json.dumps(data)
							response = HttpResponse(data)
						else:
							try:
								d = DetilIUJK.objects.get(id=request.COOKIES['id_pengajuan'])
								p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
								berkas = form.save(commit=False)
								berkas.nama_berkas = "Akta Pendirian "+p.nama_perusahaan
								berkas.keterangan = "Akta Pendirian "+p.nama_perusahaan
								if request.user.is_authenticated():
									berkas.created_by_id = request.user.id
								else:
									berkas.created_by_id = request.COOKIES['id_pemohon']
								berkas.save()
								p.berkas_npwp = berkas
								p.save()
								d.berkas_npwp_perusahaan = berkas
								d.save()
								data = {'success': True, 'pesan': 'Akta Pendirian '+p.nama_perusahaan +' Berhasil diupload' ,'data': [
									{'status_upload': 'ok'},
								]}
							except ObjectDoesNotExist:
								data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar.'}]}					
							data = json.dumps(data)
							response = HttpResponse(data)
					else:
						data = form.errors.as_json()
						response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong.'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = form.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload Akta Pendirian, Perusahaan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload Akta Pendirian, Perusahaan tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response	


def upload_akta_perubahan_badan_usaha(request):
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			form = BerkasFom(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			if request.method == "POST":
				if berkas_:
					if form.is_valid():
						ext = os.path.splitext(berkas_.name)[1]
						valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.png']
						if not ext in valid_extensions:
							data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
							data = json.dumps(data)
							response = HttpResponse(data)
						else:
							try:
								d = DetilIUJK.objects.get(id=request.COOKIES['id_pengajuan'])
								p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
								berkas = form.save(commit=False)
								berkas.nama_berkas = "Akta Perubahan "+p.nama_perusahaan
								berkas.keterangan = "Akta Perubahan "+p.nama_perusahaan
								if request.user.is_authenticated():
									berkas.created_by_id = request.user.id
								else:
									berkas.created_by_id = request.COOKIES['id_pemohon']
								berkas.save()
								p.berkas_npwp = berkas
								p.save()
								d.berkas_npwp_perusahaan = berkas
								d.save()
								data = {'success': True, 'pesan': 'Akta Perubahan '+p.nama_perusahaan+' Berhasil diupload' ,'data': [
									{'status_upload': 'ok'},
								]}
							except ObjectDoesNotExist:
								data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar.'}]}					
							data = json.dumps(data)
							response = HttpResponse(data)
					else:
						data = form.errors.as_json()
						response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong.'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = form.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload Akta Perubahan, Perusahaan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload Akta Perubahan, Perusahaan tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response		
