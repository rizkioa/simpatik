from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.template import RequestContext, loader
import json
import os

from izin.models import PaketPekerjaan, DetilIUJK, AnggotaBadanUsaha, Syarat
from izin.utils import formatrupiah
from perusahaan.models import Perusahaan, Legalitas
from master.models import Berkas
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna
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
				paket = PaketPekerjaan.objects.filter(detil_iujk_id=request.COOKIES['id_pengajuan'])
				if len(paket) > 0 :
					iujk = DetilIUJKForm_.save(commit=False)
					iujk.perusahaan_id = request.COOKIES['id_perusahaan']
					iujk.save()
					data = {'success': True, 
						'pesan': 'Data Paket Pekerjaan Berhasil Disimpan.',
						'data': [
							{'jenis_iujk': iujk.jenis_iujk }
						]
					}
					data = json.dumps(data)
					response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Paket Pekerjaan Kosong, Silahkan masukkkan Paket Pekerjaan'}]}
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
						if request.COOKIES['id_legalitas'] == "":
							form = LegalitasPerusahaanForm(request.POST)
						else:
							try:
								l = Legalitas.objects.get(id=request.COOKIES['id_legalitas'])
								form = LegalitasPerusahaanForm(request.POST, instance=l)
							except ObjectDoesNotExist:
								form = LegalitasPerusahaanForm(request.POST)

						if form.is_valid():
							f = form.save(commit=False)
							f.perusahaan_id = request.COOKIES['id_perusahaan']
							f.jenis_legalitas_id = 1
							if request.user.is_authenticated():
								f.created_by_id = request.user.id
							else:
								f.created_by_id = request.COOKIES['id_pemohon']
							f.save()
							pengajuan_.legalitas.add(f)
							if request.POST.get('onoffswitch') != 'on':
								data = {'success': True, 'pesan': 'Legalitas Perusahaan berhasil disimpanaaaa. Proses Selanjutnya.', 'data': [
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
								# formperubahan = LegalitasPerusahaanPerubahanForm(request.POST)
								if request.COOKIES['id_legalitas_perubahan'] == "":
									formperubahan = LegalitasPerusahaanPerubahanForm(request.POST)
								else:
									try:
										lp = Legalitas.objects.get(id=request.COOKIES['id_legalitas_perubahan'])
										formperubahan = LegalitasPerusahaanPerubahanForm(request.POST, instance=lp)
									except ObjectDoesNotExist:
										formperubahan = LegalitasPerusahaanPerubahanForm(request.POST)
								
								if formperubahan.is_valid():
									if request.user.is_authenticated():
										created = request.user.id
									else:
										created = request.COOKIES['id_pemohon']
									legalitas = formperubahan.save(commit=False)
									legalitas.perusahaan_id = request.COOKIES['id_perusahaan']
									legalitas.jenis_legalitas_id = 2
									legalitas.nama_notaris = request.POST.get('nama_notaris_perubahan')
									legalitas.alamat = request.POST.get('alamat_notaris_perubahan')
									legalitas.nomor_akta = request.POST.get('nomor_akta_perubahan')
									legalitas.tanggal_akta = datetime.datetime.strptime(request.POST.get('tanggal_akta_perubahan'), '%d-%m-%Y').strftime('%Y-%m-%d')
									legalitas.telephone = request.POST.get('telephone_notaris_perubahan')
									legalitas.nomor_pengesahan = request.POST.get('nomor_pengesahan_perubahan')
									legalitas.tanggal_pengesahan = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_perubahan'), '%d-%m-%Y').strftime('%Y-%m-%d')
									if request.user.is_authenticated():
										legalitas.created_by_id = request.user.id
									else:
										legalitas.created_by_id = request.COOKIES['id_pemohon']
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
									response.set_cookie(key='id_legalitas', value=f.id)
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
				valid_extensions = ['.pdf', '.jpg', '.png']
				if os.path.splitext(request.FILES.get('berkas_foto').name)[1] in valid_extensions:
					if os.path.splitext(request.FILES.get('berkas_ktp').name)[1] in valid_extensions:
						if os.path.splitext(request.FILES.get('berkas_pernyataan').name)[1] in valid_extensions:
							if os.path.splitext(request.FILES.get('berkas_merangkap').name)[1] in valid_extensions:
								da_ = form_.save(commit=False)
								da_.detil_iujk_id = request.COOKIES['id_pengajuan']
								da_.jenis_anggota_badan = 'Direktur / Penanggung Jawab Badan Usaha'
								da_.save()

								da_.berkas_tambahan.create(nama_berkas="Direktur / Penanggung Jawab Badan Usaha, Berkas FOTO 4X6 "+da_.nama, berkas=request.FILES.get('berkas_foto'))
								da_.berkas_tambahan.create(nama_berkas="Direktur / Penanggung Jawab Badan Usaha, Berkas KTP "+da_.nama, berkas=request.FILES.get('berkas_ktp'))
								da_.berkas_tambahan.create(nama_berkas="Direktur / Penanggung Jawab Badan Usaha, Berkas Pernyataan bukan PNS/TNI/POLRI "+da_.nama, berkas=request.FILES.get('berkas_pernyataan'))
								da_.berkas_tambahan.create(nama_berkas="Direktur / Penanggung Jawab Badan Usaha, Berkas Tidak Merangkap/Bekerja Pada BU Lain "+da_.nama, berkas=request.FILES.get('berkas_merangkap'))
								
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
				valid_extensions = ['.pdf', '.jpg', '.png']
				if os.path.splitext(request.FILES.get('berkas_foto').name)[1] in valid_extensions:
					if os.path.splitext(request.FILES.get('berkas_ktp').name)[1] in valid_extensions:
						if os.path.splitext(request.FILES.get('ijazah_sma').name)[1] in valid_extensions:
							if os.path.splitext(request.FILES.get('ska_skt').name)[1] in valid_extensions:
								if os.path.splitext(request.FILES.get('berkas_merangkap').name)[1] in valid_extensions:
									da_ = form_.save(commit=False)
									da_.detil_iujk_id = request.COOKIES['id_pengajuan']
									da_.jenis_anggota_badan = 'Penanggung Jawab Teknik Badan Usaha'
									da_.save()


									da_.berkas_tambahan.create(nama_berkas="Penanggung Jawab Teknik Badan Usaha, Berkas FOTO 4X6 "+da_.nama, berkas=request.FILES.get('berkas_foto'))
									da_.berkas_tambahan.create(nama_berkas="Penanggung Jawab Teknik Badan Usaha, Berkas KTP "+da_.nama, berkas=request.FILES.get('berkas_ktp'))
									da_.berkas_tambahan.create(nama_berkas="Penanggung Jawab Teknik Badan Usaha, Berkas Ijazah SMA "+da_.nama, berkas=request.FILES.get('ijazah_sma'))
									da_.berkas_tambahan.create(nama_berkas="Penanggung Jawab Teknik Badan Usaha, Berkas SKA/SKT "+da_.nama, berkas=request.FILES.get('ska_skt'))
									da_.berkas_tambahan.create(nama_berkas="Penanggung Jawab Teknik Badan Usaha, Berkas Tidak Merangkap/Bekerja Pada BU Lain "+da_.nama, berkas=request.FILES.get('berkas_merangkap'))
									
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
				valid_extensions = ['.pdf', '.jpg', '.png']
				if os.path.splitext(request.FILES.get('berkas_foto').name)[1] in valid_extensions:
					if os.path.splitext(request.FILES.get('berkas_ktp').name)[1] in valid_extensions:
						if os.path.splitext(request.FILES.get('ijazah_sma').name)[1] in valid_extensions:
							da_ = form_.save(commit=False)
							da_.detil_iujk_id = request.COOKIES['id_pengajuan']
							da_.jenis_anggota_badan = 'Tenaga Non Teknik'
							da_.save()

							da_.berkas_tambahan.create(nama_berkas="Tenaga Non Teknik, Berkas FOTO 4X6 "+da_.nama, berkas=request.FILES.get('berkas_foto'))
							da_.berkas_tambahan.create(nama_berkas="Tenaga Non Teknik, Berkas KTP "+da_.nama, berkas=request.FILES.get('berkas_ktp'))
							da_.berkas_tambahan.create(nama_berkas="Tenaga Non Teknik, Berkas Ijazah SMA "+da_.nama, berkas=request.FILES.get('ijazah_sma'))

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
						data['data'] = []
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

def upload_berkas_next(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '0':
			try:
				iujk = DetilIUJK.objects.get(id=request.COOKIES['id_pengajuan'])
				berkas_ = iujk.berkas_tambahan.all()
				p = iujk.perusahaan
				b = berkas_.filter(nama_berkas="Sertifikat Badan Usaha "+p.nama_perusahaan)
				if b.exists():
					b = berkas_.filter(nama_berkas="Kartu Teknis Badan Usaha "+p.nama_perusahaan)
					if b.exists():
						b = berkas_.filter(nama_berkas="Surat Pernyataaan Pengikatan Diri PJT-BU "+p.nama_perusahaan)
						if b.exists():
							b = berkas_.filter(nama_berkas="Surat Peryataan Pengikatan Diri Penanggung Jawab BUJK "+p.nama_perusahaan)
							if b.exists():
								# b = berkas_.filter(nama_berkas="NPWP "+p.nama_perusahaan)
								npwp = p.berkas_npwp
								if npwp:
									b = berkas_.filter(nama_berkas="Surat Keterangan Domisili Badan Usaha dari Kantor Desa Setempat "+p.nama_perusahaan)
									if b.exists():
										b = berkas_.filter(nama_berkas="Gambar denah lokasi/posisi badan usaha "+p.nama_perusahaan)
										if b.exists():
											b = berkas_.filter(nama_berkas="Gambar/foto papan nama badan usaha "+p.nama_perusahaan)
											if b.exists():
												data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': [] }
												data = json.dumps(data)
											else:
												data = {'Terjadi Kesalahan': [{'message': 'Gambar/foto papan nama badan usaha '+p.nama_perusahaan+' tidak ada'}]}
												data = json.dumps(data)
										else:
											data = {'Terjadi Kesalahan': [{'message': 'Gambar denah lokasi/posisi badan usaha '+p.nama_perusahaan+' tidak ada'}]}
											data = json.dumps(data)
									else:
										data = {'Terjadi Kesalahan': [{'message': 'Surat Keterangan Domisili Badan Usaha dari Kantor Desa Setempat '+p.nama_perusahaan+' tidak ada'}]}
										data = json.dumps(data)
								else:
									data = {'Terjadi Kesalahan': [{'message': 'NPWP '+p.nama_perusahaan+' tidak ada'}]}
									data = json.dumps(data)
							else:
								data = {'Terjadi Kesalahan': [{'message': 'Surat Peryataan Pengikatan Diri Penanggung Jawab BUJK '+p.nama_perusahaan+' tidak ada'}]}
								data = json.dumps(data)
						else:
							data = {'Terjadi Kesalahan': [{'message': 'Surat Pernyataaan Pengikatan Diri PJT-BU '+p.nama_perusahaan+' tidak ada'}]}
							data = json.dumps(data)
					else:
						data = {'Terjadi Kesalahan': [{'message': 'Kartu Teknis Badan Usaha '+p.nama_perusahaan+' tidak ada'}]}
						data = json.dumps(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Sertifikat Badan Usaha '+p.nama_perusahaan+' tidak ada'}]}
					data = json.dumps(data)

				
				# response = HttpResponse(data)
			except Perusahaan.DoesNotExist:
				data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar.'}]}
				data = json.dumps(data)
				# response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
			# response = HttpResponse(data)
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

								d.berkas_tambahan.add(berkas)
								# d.save()
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

								d.berkas_tambahan.add(berkas)
								# d.save()
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

								d.berkas_tambahan.add(berkas)
								# d.save()
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

								d.berkas_tambahan.add(berkas)
								# d.save()
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
						valid_extensions = ['.jpg', '.png']
						if not ext in valid_extensions:
							data = {'Terjadi Kesalahan': [{'message': 'Type file tidak valid hanya boleh pdf, jpg, png, doc, docx.'}]}
							data = json.dumps(data)
							response = HttpResponse(data)
						else:
							try:
								# d = DetilIUJK.objects.get(id=request.COOKIES['id_pengajuan'])
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

								d.berkas_tambahan.add(berkas)
								# d.save()
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

								d.berkas_tambahan.add(berkas)
								# d.save()
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
								
								d.berkas_tambahan.add(berkas)
								# d.save()
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

								l = Legalitas.objects.get(id=request.COOKIES['id_legalitas'])
								l.berkas = berkas
								l.save()
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

								l = Legalitas.objects.get(id=request.COOKIES['id_legalitas'])
								l.berkas = berkas
								l.save()
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

def iujk_done(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilIUJK.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
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

def ajax_konfirmasi_nama_paket_pekerjaan(request, id_pengajuan):
	paket_ = ""
	if id_pengajuan:
		paket_list = PaketPekerjaan.objects.filter(detil_iujk__id=id_pengajuan)
		paket_ = [ obj.as_dict() for obj in paket_list ]
		paket_list = paket_list.first()
		if paket_list:
			data = {'success': True, 'pesan': 'Proses Selesai.', 'paket': paket_, 'jenis':paket_list.detil_iujk.jenis_iujk }
		else:
			data = {'success': True, 'pesan': 'Proses Selesai.', 'paket': paket_, 'jenis':paket_list }

	response = HttpResponse(json.dumps(data))
	return response

def ajax_konfirmasi_anggota_badan_direktur(request, id_pengajuan):
	anggota = ""
	if id_pengajuan:
		anggota_list = AnggotaBadanUsaha.objects.filter(detil_iujk__id=id_pengajuan, jenis_anggota_badan='Direktur / Penanggung Jawab Badan Usaha')
		anggota_ = [ obj.as_dict() for obj in anggota_list ]
		# anggota_list = anggota_list.last()
	data = {'success': True, 'pesan': 'Proses Selesai.', 'anggota': anggota_, }
	response = HttpResponse(json.dumps(data))
	return response

def ajax_konfirmasi_anggota_badan_teknik(request, id_pengajuan):
	anggota = ""
	if id_pengajuan:
		anggota_list = AnggotaBadanUsaha.objects.filter(detil_iujk__id=id_pengajuan, jenis_anggota_badan='Penanggung Jawab Teknik Badan Usaha')
		anggota_ = [ obj.as_dict() for obj in anggota_list ]
	data = {'success': True, 'pesan': 'Proses Selesai.', 'anggota': anggota_ }
	response = HttpResponse(json.dumps(data))
	return response


def ajax_konfirmasi_anggota_badan_non_teknik(request, id_pengajuan):
	anggota = ""
	if id_pengajuan:
		anggota_list = AnggotaBadanUsaha.objects.filter(detil_iujk__id=id_pengajuan, jenis_anggota_badan='Tenaga Non Teknik')
		anggota_ = [ obj.as_dict() for obj in anggota_list ]
	data = {'success': True, 'pesan': 'Proses Selesai.', 'anggota': anggota_ }
	response = HttpResponse(json.dumps(data))
	return response

def ajax_load_berkas(request, id_pengajuan):
	url_berkas = []
	id_elemen = []
	nm_berkas =[]
	id_berkas =[]
	if id_pengajuan:
		try:
			iujk = DetilIUJK.objects.get(id=id_pengajuan)
			p = iujk.perusahaan
			berkas_ = iujk.berkas_tambahan.all()
			legalitas_pendirian = p.legalitas_set.filter(~Q(jenis_legalitas__id=2)).last()
			legalitas_perubahan= p.legalitas_set.filter(jenis_legalitas__id=2).last()

			npwp = p.berkas_npwp
			if npwp:
				url_berkas.append(npwp.berkas.url)
				id_elemen.append('npwp')
				nm_berkas.append("NPWP "+p.nama_perusahaan)
				id_berkas.append(npwp.id)

			# print legalitas_pendirian
			if legalitas_pendirian:
				if legalitas_pendirian.berkas:
					# print legalitas_pendirian.berkas
					url_berkas.append(legalitas_pendirian.berkas.berkas.url)
					id_elemen.append('akta_pendirian')
					nm_berkas.append(legalitas_pendirian.berkas.nama_berkas)
					id_berkas.append(legalitas_pendirian.berkas.id)

			if legalitas_perubahan:
				if legalitas_perubahan.berkas:
					# print legalitas_pendirian.berkas
					url_berkas.append(legalitas_perubahan.berkas.berkas.url)
					id_elemen.append('akta_perubahan')
					nm_berkas.append(legalitas_perubahan.berkas.nama_berkas)
					id_berkas.append(legalitas_perubahan.berkas.id)

			sertifikat = berkas_.filter(nama_berkas="Sertifikat Badan Usaha "+p.nama_perusahaan)
			if sertifikat.exists():
				sertifikat = sertifikat.last()
				url_berkas.append(sertifikat.berkas.url)
				id_elemen.append('sertifikat')
				nm_berkas.append("Sertifikat Badan Usaha "+p.nama_perusahaan)
				id_berkas.append(sertifikat.id)

			kartu_teknis = berkas_.filter(nama_berkas="Kartu Teknis Badan Usaha "+p.nama_perusahaan)
			if kartu_teknis.exists():
				kartu_teknis = kartu_teknis.last()
				url_berkas.append(kartu_teknis.berkas.url)
				id_elemen.append('kartu_teknis_bu')
				nm_berkas.append("Kartu Teknis Badan Usaha "+p.nama_perusahaan)
				id_berkas.append(kartu_teknis.id)

			pernyataan = berkas_.filter(nama_berkas="Surat Pernyataaan Pengikatan Diri PJT-BU "+p.nama_perusahaan)
			if pernyataan.exists():
				pernyataan = pernyataan.last()
				url_berkas.append(pernyataan.berkas.url)
				id_elemen.append('pernyataan_pengikat')
				nm_berkas.append("Surat Pernyataaan Pengikatan Diri PJT-BU "+p.nama_perusahaan)
				id_berkas.append(pernyataan.id)

			pernyataan2 = berkas_.filter(nama_berkas="Surat Peryataan Pengikatan Diri Penanggung Jawab BUJK "+p.nama_perusahaan)
			if pernyataan2.exists():
				pernyataan2 = pernyataan2.last()
				url_berkas.append(pernyataan2.berkas.url)
				id_elemen.append('pernyataan')
				nm_berkas.append("Surat Peryataan Pengikatan Diri Penanggung Jawab BUJK "+p.nama_perusahaan)
				id_berkas.append(pernyataan2.id)

			domisli = berkas_.filter(nama_berkas="Surat Keterangan Domisili Badan Usaha dari Kantor Desa Setempat "+p.nama_perusahaan)
			if domisli.exists():
				domisli = domisli.last()
				url_berkas.append(domisli.berkas.url)
				id_elemen.append('keterangan_domisili')
				nm_berkas.append("Surat Keterangan Domisili Badan Usaha dari Kantor Desa Setempat "+p.nama_perusahaan)
				id_berkas.append(domisli.id)

			lokasi = berkas_.filter(nama_berkas="Gambar denah lokasi/posisi badan usaha "+p.nama_perusahaan)
			if lokasi.exists():
				lokasi = lokasi.last()
				url_berkas.append(lokasi.berkas.url)
				id_elemen.append('denah_lokasi')
				nm_berkas.append("Gambar denah lokasi/posisi badan usaha "+p.nama_perusahaan)
				id_berkas.append(lokasi.id)

			papan = berkas_.filter(nama_berkas="Gambar/foto papan nama badan usaha "+p.nama_perusahaan)
			if papan.exists():
				papan = papan.last()
				url_berkas.append(papan.berkas.url)
				id_elemen.append('foto_papan')
				nm_berkas.append("Gambar/foto papan nama badan usaha "+p.nama_perusahaan)
				id_berkas.append(papan.id)

			data = {'success': True, 'pesan': 'Perusahaan Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': '' }
			
		
	response = HttpResponse(json.dumps(data))
	return response

def ajax_delete_berkas(request, id_berkas, kode):
	if id_berkas:
		if kode == 'akta_pendirian':
			p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
			legalitas_pendirian = p.legalitas_set.filter(~Q(jenis_legalitas__id=2)).last()
			legalitas_pendirian.berkas = None
			legalitas_pendirian.save()
		elif kode == 'akta_perubahan':
			p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
			legalitas_perubahan= p.legalitas_set.filter(jenis_legalitas__id=2).last()
			legalitas_perubahan.berkas = None
			legalitas_perubahan.save()
		elif kode == 'npwp':
			p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
			p.berkas_npwp = None
			p.save()
		else:
			pass

		try:
			b = Berkas.objects.get(id=id_berkas)
			data = {'success': True, 'pesan': str(b)+" berhasil dihapus" }
			b.delete()
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': 'Berkas Tidak Ada' }
			
		response = HttpResponse(json.dumps(data))
		return response

	return False

def cetak_bukti_pendaftaran_iujk(request, id_pengajuan_):
	# id_pengajuan_ = base64.b64decode(id_pengajuan_)
	extra_context = {}
	if id_pengajuan_:
		pengajuan_ = DetilIUJK.objects.get(id=id_pengajuan_)
		if pengajuan_.perusahaan != '':
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", DESA "+str(pengajuan_.pemohon.desa)+", KEC. "+str(pengajuan_.pemohon.desa.kecamatan)+", "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
					extra_context.update({ 'alamat_pemohon': alamat_ })
				extra_context.update({ 'pemohon': pengajuan_.pemohon })
				paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
				ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
				extra_context.update({ 'paspor': paspor_ })
				extra_context.update({ 'ktp': ktp_ })
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", DESA "+str(pengajuan_.perusahaan.desa)+", KEC. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
					extra_context.update({ 'alamat_perusahaan': alamat_perusahaan_ })
				extra_context.update({ 'perusahaan': pengajuan_.perusahaan })
			syarat = Syarat.objects.filter(jenis_izin__jenis_izin__kode="IUJK")

			extra_context.update({ 'pengajuan': pengajuan_ })

			extra_context.update({ 'syarat': syarat })

			extra_context.update({ 'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin })
			extra_context.update({ 'created_at': pengajuan_.created_at })
			
			response = loader.get_template("front-end/include/formulir_iujk/cetak_bukti_pendaftaran.html")
		else:
			response = HttpResponseRedirect(url_)
			return response
	else:
		response = HttpResponseRedirect(url_)
		return response	

	template = loader.get_template("front-end/include/formulir_iujk/cetak_bukti_pendaftaran.html")
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))