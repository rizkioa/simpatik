import json
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from izin.models import DetilTDP, RincianPerusahaan
from izin.tdp_forms import DataUmumPerusahaanPTForm, DataKegiatanPTForm, RincianPerusahaanForm, LegalitasForm
from perusahaan.models import Legalitas, Perusahaan

def tdp_data_umum_perusahaan_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilTDP.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			data_umum_form = DataUmumPerusahaanPTForm(request.POST, instance=pengajuan_)
			onoffkantorcabang = request.POST.get('onoffkantorcabang')
			onoffunitproduksi = request.POST.get('onoffunitproduksi')
			no_tdp = request.POST.get('no_tdp')
			if data_umum_form.is_valid():
				p = data_umum_form.save(commit=False)
				p.jenis_badan_usaha_id = 1
				if onoffkantorcabang == 'on':
					p.nomor_tdp_kantor_pusat = no_tdp
				p.save()
				if onoffkantorcabang == 'on':
					npwp = request.POST.get('npwp_perusahaan_induk')
					nama = request.POST.get('nama_perusahaan_induk')
					alamat = request.POST.get('alamat_perusahaan_induk')
					desa = request.POST.get('desa_perusahaan_induk')
					perusahaan_cabang = request.COOKIES.get('id_perusahaan')
					try:
						per = Perusahaan.objects.get(npwp=npwp)
						per.perusahaan_induk_id = request.COOKIES['id_perusahaan_induk']
						per.nama_perusahaan = nama
						per.alamat_perusahaan = alamat
						per.desa_id = desa
						per.save()
					except ObjectDoesNotExist:
						per = Perusahaan(npwp=npwp, nama_perusahaan=nama, alamat_perusahaan=alamat, desa_id=desa)
						per.save(force_insert=True)
					try:
						per_cabang = Perusahaan.objects.get(id=perusahaan_cabang)
						per_cabang.perusahaan_induk_id = per.id
						per_cabang.save()
					except ObjectDoesNotExist:
						pass
				if onoffunitproduksi == 'on':
					alamat = request.POST.get('alamat_unit_produksi')
					desa = request.POST.get('desa_unit_prosuksi')
					try:
						unit = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
						unit.alamat_unit_produksi = alamat
						unit.desa_unit_produksi_id = desa
						unit.save()
					except ObjectDoesNotExist:
						pass
				data = {'success': True, 'pesan': 'Data Umum Perusahaan berhasil tersimpan.', 'data': []}
				data = json.dumps(data)
				response = HttpResponse(data)
				if onoffkantorcabang == 'on':
					response.set_cookie(key='id_perusahaan_induk', value=per.id)
			else:
				data = data_umum_form.errors.as_json()
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

def tdp_data_kegiatan_pt_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilTDP.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			data_kegiatan_form = DataKegiatanPTForm(request.POST, instance=pengajuan_)
			if data_kegiatan_form.is_valid():
				p = data_kegiatan_form.save(commit=False)
				p.save()
				try:
					rincian_ = RincianPerusahaan.objects.get(detil_tdp_id=p.id)
					rincianperusahaan_form = RincianPerusahaanForm(request.POST, instance=rincian_)
				except ObjectDoesNotExist:
					rincianperusahaan_form = RincianPerusahaanForm(request.POST)
				
				if rincianperusahaan_form.is_valid():
					rp = rincianperusahaan_form.save(commit=False)
					rp.detil_tdp_id = p.id
					rp.save()
					data = {'success': True, 'pesan': 'Data Kegiatan Perusahaan, berhasil tersimpan.', 'data': []}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = data_kegiatan_form.errors.as_json()
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def tdp_legalitas_pt_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilTDP.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			if 'id_perusahaan' in request.COOKIES.keys():
				if request.COOKIES['id_perusahaan'] != '':
					perusahaan = request.COOKIES['id_perusahaan']
					nama_notaris_pendirian = request.POST.get('nama_notaris_pendirian')
					alamat_pendirian = request.POST.get('alamat_pendirian')
					telephone_pendirian = request.POST.get('telephone_pendirian')
					nomor_pengesahan_pendirian = request.POST.get('nomor_pengesahan_pendirian')
					tanggal_pengesahan_pendirian = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_pendirian'), '%d-%m-%Y').strftime('%Y-%m-%d')
					# save legalitas pendirian
					try:
						legalitas_pendirian = Legalitas.objects.get(perusahaan_id=perusahaan, jenis_legalitas_id=1)
						if legalitas_pendirian.jenis_legalitas_id == 1:
							legalitas_pendirian.jenis_legalitas_id=1
							legalitas_pendirian.perusahaan_id = perusahaan
							legalitas_pendirian.nama_notaris = nama_notaris_pendirian
							legalitas_pendirian.alamat = alamat_pendirian
							legalitas_pendirian.telephone = telephone_pendirian
							legalitas_pendirian.nomor_pengesahan = nomor_pengesahan_pendirian
							legalitas_pendirian.tanggal_pengesahan = tanggal_pengesahan_pendirian
							legalitas_pendirian.save()
						else:
							pass
					except ObjectDoesNotExist:
						legalitas_pendirian = Legalitas(perusahaan_id=perusahaan, jenis_legalitas_id=1,  nama_notaris=nama_notaris_pendirian, alamat=alamat_pendirian, telephone=telephone_pendirian, nomor_pengesahan=nomor_pengesahan_pendirian, tanggal_pengesahan=tanggal_pengesahan_pendirian)
						legalitas_pendirian.save(force_insert=True)
					# +++++++ save akta perubahan ++++
					onoffaktaperubahan = request.POST.get('onoffaktaperubahan')
					if onoffaktaperubahan == 'on':
						nama_notaris_perubahan = request.POST.get('nama_notaris_akta_perubahan')
						alamat_perubahan = request.POST.get('alamat_akta_perubahan')
						telephone_perubahan = request.POST.get('telephone_akta_perubahan')
						nomor_pengesahan_perubahan = request.POST.get('nomor_pengesahan_akta_perubahan')
						tanggal_pengesahan_perubahan = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_akta_perubahan'), '%d-%m-%Y').strftime('%Y-%m-%d')
						try:
							legalitas_perubahan = Legalitas.objects.get(perusahaan_id=perusahaan, jenis_legalitas_id=2)
							legalitas_perubahan.jenis_legalitas_id = 2
							legalitas_perubahan.nama_notaris = nama_notaris_perubahan
							legalitas_perubahan.alamat = alamat_perubahan
							legalitas_perubahan.telephone = telephone_perubahan
							legalitas_perubahan.nomor_pengesahan = nomor_pengesahan_perubahan
							legalitas_perubahan.tanggal_pengesahan = tanggal_pengesahan_perubahan
							legalitas_perubahan.save()
						except ObjectDoesNotExist:
							legalitas_perubahan = Legalitas(perusahaan_id=perusahaan, jenis_legalitas_id=2,  nama_notaris=nama_notaris_perubahan, alamat=alamat_perubahan, telephone=telephone_perubahan, nomor_pengesahan=nomor_pengesahan_perubahan, tanggal_pengesahan=tanggal_pengesahan_perubahan)
							legalitas_perubahan.save(force_insert=True)
					# +++++++ end save akta perubahan ++++
					# +++++++ save pengesahan menteri +++++
					onoffpengesahanmenteri = request.POST.get('onoffpengesahanmenteri')
					if onoffpengesahanmenteri == 'on':
						noppm1 = request.POST.get('nomor_pengesahan_pengesahan_menteri')
						tglppm1 = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_pengesahan_menteri'), '%d-%m-%Y').strftime('%Y-%m-%d')
						try:
							legalitas_pengesahan_menteri = Legalitas.objects.get(perusahaan_id=perusahaan, jenis_legalitas_id=3)
							legalitas_pengesahan_menteri.jenis_legalitas_id = 3
							legalitas_pengesahan_menteri.perusahaan_id = perusahaan
							legalitas_pengesahan_menteri.nomor_pengesahan = noppm1
							legalitas_pengesahan_menteri.tanggal_pengesahan = tglppm1
							legalitas_pengesahan_menteri.save()
						except ObjectDoesNotExist:
							legalitas_pengesahan_menteri = Legalitas(nomor_pengesahan=noppm1, tanggal_pengesahan=tglppm1, jenis_legalitas_id=3, perusahaan_id=perusahaan)
							legalitas_pengesahan_menteri.save(force_insert=True)
					# +++++++ end save pengesahan menteri +++++
					# +++++++ save persetujuan menteri +++++
					onoffpersetujuanmenteri = request.POST.get('onoffpersetujuanmenteri')
					if onoffpersetujuanmenteri == 'on':
						noppm2 = request.POST.get('nomor_pengesahan_persetujuan_menteri')
						tglppm2 = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_persetujuan_menteri'), '%d-%m-%Y').strftime('%Y-%m-%d')
						try:
							legalitas_persetujuan_menteri = Legalitas.objects.get(perusahaan_id=perusahaan, jenis_legalitas_id=4)
							legalitas_persetujuan_menteri.jenis_legalitas_id = 4
							legalitas_persetujuan_menteri.perusahaan_id = perusahaan
							legalitas_persetujuan_menteri.nomor_pengesahan = noppm2
							legalitas_persetujuan_menteri.tanggal_pengesahan = tglppm2
							legalitas_persetujuan_menteri.save()
						except ObjectDoesNotExist:
							legalitas_persetujuan_menteri = Legalitas(nomor_pengesahan=noppm2, tanggal_pengesahan=tglppm2, jenis_legalitas_id=4, perusahaan_id=perusahaan)
							legalitas_persetujuan_menteri.save(force_insert=True)
					# +++++++ end save persetujuan menteri +++++
					# +++++++ save penerima laporan +++++
					onoffpenerimalaporan = request.POST.get('onoffpenerimalaporan')
					if onoffpenerimalaporan == 'on':
						noppm3 = request.POST.get('nomor_pengesahan_penerima_laporan')
						tglppm3 = datetime.datetime.strptime(request.POST.get('tanggal_pengesahaan_penerima_laporan'), '%d-%m-%Y').strftime('%Y-%m-%d')
						try:
							legalitas_penerima_laporan = Legalitas.objects.get(perusahaan_id=perusahaan, jenis_legalitas_id=6)
							legalitas_penerima_laporan.jenis_legalitas_id = 6
							legalitas_penerima_laporan.perusahaan_id = perusahaan
							legalitas_penerima_laporan.nomor_pengesahan = noppm3
							legalitas_penerima_laporan.tanggal_pengesahan = tglppm3
							legalitas_penerima_laporan.save()
						except ObjectDoesNotExist:
							legalitas_penerima_laporan = Legalitas(nomor_pengesahan=noppm3, tanggal_pengesahan=tglppm3, jenis_legalitas_id=6, perusahaan_id=perusahaan)
							legalitas_penerima_laporan.save(force_insert=True)
					# +++++++ end save penerima laporan +++++
					onoffpenerimaanpemberitahuan = request.POST.get('onoffpenerimaanpemberitahuan')
					if onoffpenerimaanpemberitahuan == 'on':
						noppm4 = request.POST.get('nomor_pengesahan_penerimaan_pemberitahuan')
						tglppm4 = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_penerimaan_pemberitahuan'), '%d-%m-%Y').strftime('%Y-%m-%d')
						try:
							legalitas_penerimaan_pemberitahuan = Legalitas.objects.get(perusahaan_id=perusahaan, jenis_legalitas_id=7)
							legalitas_penerimaan_pemberitahuan.jenis_legalitas_id = 7
							legalitas_penerimaan_pemberitahuan.perusahaan_id = perusahaan
							legalitas_penerimaan_pemberitahuan.nomor_pengesahan = noppm4
							legalitas_penerimaan_pemberitahuan.tanggal_pengesahan = tglppm4
							legalitas_penerimaan_pemberitahuan.save()
						except ObjectDoesNotExist:
							legalitas_penerimaan_pemberitahuan = Legalitas(nomor_pengesahan=noppm4, tanggal_pengesahan=tglppm4, jenis_legalitas_id=7, perusahaan_id=perusahaan)
							legalitas_penerimaan_pemberitahuan.save(force_insert=True)
					# +++++++ save penerimaan pemberitahuan +++++

					# +++++++ end save penerimaan pemberitahuan +++++

					data = {'success': True, 'pesan': 'Data Kegiatan Perusahaan, berhasil tersimpan.', 'data': []}
					data = json.dumps(data)
					response = HttpResponse(data)
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Data Perusahaan tidak ditemukan/data kosong'}]}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = {'Terjadi Kesalahan': [{'message': 'Data Perusahaan tidak ditemukan/data kosong'}]}
				data = json.dumps(data)
				response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response