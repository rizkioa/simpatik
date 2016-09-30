from django.http import HttpResponse
import json
from sqlite3 import OperationalError

from izin.izin_forms import PemohonForm, PerusahaanForm, PengajuanSiupForm, LegalitasPerusahaanForm, UploadBerkasPendukungForm, UploadBerkasNPWPPerusahaanForm, UploadBerkasFotoForm, UploadBerkasKTPForm, UploadBerkasNPWPPribadiForm, UploadBerkasAktaPendirianForm, UploadBerkasAktaPerubahanForm, LegalitasPerusahaanPerubahanForm
from izin.utils import get_nomor_pengajuan
from accounts.models import NomorIdentitasPengguna
from izin.models import PengajuanIzin, Pemohon, JenisPermohonanIzin, DetilSIUP, KelompokJenisIzin
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from master.models import Berkas
from perusahaan.models import Legalitas, KBLI, ProdukUtama

try:
	from django.utils.encoding import force_text
except ImportError:
	from django.utils.encoding import force_unicode as force_text

from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from perusahaan.models import Perusahaan

def siup_identitas_pemohon_save_cookie(request):
	pemohon = PemohonForm(request.POST) 
	if pemohon.is_valid():
		# Untuk Nomor Identitas
		ktp_ = request.POST.get('ktp', None)
		paspor_ = request.POST.get('paspor', None)
		jenis_pemohon = request.POST.get('jenis_pemohon', None)
		# End
		jenis_permohonan_ = request.POST.get('jenis_pengajuan', None)
		k = KelompokJenisIzin.objects.filter(id=request.COOKIES['id_kelompok_izin']).last()
		nomor_pengajuan_ = get_nomor_pengajuan(k.jenis_izin.kode)
		nama_kuasa = request.POST.get('nama_kuasa', None)
		no_identitas_kuasa = request.POST.get('no_identitas_kuasa', None)
		telephone_kuasa = request.POST.get('telephone_kuasa', None)
		try:
			p = pemohon.save(commit=False)
			p.username = ktp_
			try:
				p.save()
				if ktp_:
					try:
						i = NomorIdentitasPengguna.objects.get(nomor = ktp_)
					except ObjectDoesNotExist:
						i, created = NomorIdentitasPengguna.objects.get_or_create(
									nomor = ktp_,
									jenis_identitas_id=1, # untuk KTP harusnya membutuhkan kode lagi
									user_id=p.id,
									)
				if paspor_:
					try:
						i = NomorIdentitasPengguna.objects.get(nomor = paspor_)
					except ObjectDoesNotExist:
						i, created = NomorIdentitasPengguna.objects.get_or_create(
									nomor = paspor_,
									jenis_identitas_id=2,
									user_id=p.id,
									)
			except OperationalError:
				pass
				

		except IntegrityError as e:
			if ktp_:
				p = Pemohon.objects.get(username = ktp_)
			elif paspor_:
				p = Pemohon.objects.get(username = paspor_)
			elif ktp_ and paspor_:
				p = Pemohon.objects.get(username = ktp_)
			
		pengajuan = DetilSIUP(no_pengajuan=nomor_pengajuan_, kelompok_jenis_izin_id=request.COOKIES['id_kelompok_izin'], pemohon_id=p.id,jenis_permohonan_id=jenis_permohonan_, created_by=request.user, nama_kuasa=nama_kuasa, no_identitas_kuasa=no_identitas_kuasa, telephone_kuasa=telephone_kuasa)
		pengajuan.save()

		jenis_ = ''
		if pemohon.cleaned_data['jenis_pemohon']:
			from master.models import JenisPemohon
			jenis_ = JenisPemohon.objects.filter(id=jenis_pemohon).last()
			jenis_ = jenis_.jenis_pemohon

		if jenis_permohonan_ :
			from izin.models import JenisPermohonanIzin
			jenis_permohonan_ = JenisPermohonanIzin.objects.filter(id=jenis_permohonan_).last()
			jenis_permohonan_ = jenis_permohonan_.jenis_permohonan_izin

		email_ = ''
		if pemohon.cleaned_data['email']:
			email_ = pemohon.cleaned_data['email']

		data = {'success': True, 'pesan': 'Identitas Pemohon berhasil tersimpan. Proses Selanjutnya.' ,'data': [
			{'nama_lengkap': pemohon.cleaned_data['nama_lengkap']},
			{'jenis_permohonan': jenis_permohonan_},
			{'jenis_pemohon': jenis_ },
			{'nomor_ktp': ktp_},
			{'alamat': pemohon.cleaned_data['alamat']},
			{'telephone': pemohon.cleaned_data['telephone']},
			{'hp': pemohon.cleaned_data['hp']},
			{'email': email_ },
			{'kewarganegaraan': pemohon.cleaned_data['kewarganegaraan']},
			{'pekerjaan': pemohon.cleaned_data['pekerjaan']},
			{'nama_kuasa': nama_kuasa},
			{'no_identitas_kuasa': no_identitas_kuasa},
			{'telephone_kuasa': telephone_kuasa}
			]}
		response = HttpResponse(json.dumps(data))	

		response.set_cookie(key='id_pengajuan', value=pengajuan.id)
		response.set_cookie(key='id_pemohon', value=p.id)
		response.set_cookie(key='nomor_ktp', value=ktp_)
		response.set_cookie(key='nomor_paspor', value=paspor_)
		# response.set_cookie(key='nama_lengkap', value=p.nama_lengkap) # set cookie	
		# if jenis_permohonan_:
		# 	response.set_cookie(key='jenis_permohonan', value=pengajuan.jenis_permohonan) # set cookie	
		# if ktp_ or paspor_:
		# 	value = ""
		# 	if ktp_:
		# 		value += "KTP "+str(ktp_)
		# 	if paspor_:
		# 		value += ", PASPOR "+str(paspor_)
		# 	response.set_cookie(key='ktp', value=value) # set cookie	
		# if p.desa:
		# 	alamat_ = str(p.alamat)+" "+str(p.desa)+", Kec. "+str(p.desa.kecamatan)+", Kab./Kota "+str(p.desa.kecamatan.kabupaten)
		# 	response.set_cookie(key='alamat', value=alamat_) # set cookie	
		# if p.jenis_pemohon:
		# 	response.set_cookie(key='jenis_pemohon', value=p.jenis_pemohon) # set cookie	
		# if p.hp:
		# 	response.set_cookie(key='hp', value=p.hp) # set cookie	
		# if p.telephone:
		# 	response.set_cookie(key='telephone', value=p.telephone) # set cookie	
		# if p.kewarganegaraan:
		# 	response.set_cookie(key='kewarganegaraan', value=p.kewarganegaraan) # set cookie	
		# if p.tempat_lahir:
		# 	ttl_ = str(p.tempat_lahir)+", "+str(p.tanggal_lahir)
		# 	response.set_cookie(key='ttl', value=ttl_) # set cookie
		# if p.email:
		# 	response.set_cookie(key='email', value=p.email) # set cookie	
	else:
		data = pemohon.errors.as_json() # untuk mengembalikan error form berupa json
		# data = {'success': False, 'pesan': 'Pengisian tidak lengkap.', 'error':pemohon.errors.as_json() }
		# response = HttpResponse(json.dumps(data))
		response = HttpResponse(data)
	return response

def siup_identitas_perusahan_save_cookie(request):
	# print request.COOKIES # Untuk Tes cookies
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			print "sesuatu"
			try:
				
				get_perusahaan = Perusahaan.objects.get(npwp=request.POST.get('npwp'))
				print get_perusahaan
				perusahaan = PerusahaanForm(request.POST, instance=get_perusahaan)
				if perusahaan.is_valid():
					perusahaan.pemohon_id = request.COOKIES['id_pemohon']
					perusahaan.save()
					alamat_ = str(get_perusahaan.alamat_perusahaan)+" "+str(get_perusahaan.desa)+", Kec. "+str(get_perusahaan.desa.kecamatan)+", Kab./Kota "+str(get_perusahaan.desa.kecamatan.kabupaten)
					data = {'success': True, 'pesan': 'Perusahaan disimpan. Proses Selanjutnya.','data' : [
					{'npwp_perusahaan': get_perusahaan.npwp},
					{'nama_perusahaan': get_perusahaan.nama_perusahaan},
					{'alamat_perusahaan': alamat_ },
					{'kode_pos_perusahaan': get_perusahaan.kode_pos},
					{'telepon_perusahaan': get_perusahaan.telepon},
					{'fax_perusahaan': get_perusahaan.fax},
					{'email_perusahaan': get_perusahaan.email}
					]}
					data = json.dumps(data)
					response = HttpResponse(json.dumps(data))
				else:
					data = perusahaan.errors.as_json()
			except Perusahaan.DoesNotExist:
				print "except"
				perusahaan = PerusahaanForm(request.POST) 
				if perusahaan.is_valid():
					print "valid"
					p = perusahaan.save(commit=False)
					perusahaan.pemohon_id = request.COOKIES['id_pemohon']
					perusahaan.save()
					alamat_ = str(p.alamat_perusahaan)+" "+str(p.desa)+", Kec. "+str(p.desa.kecamatan)+", Kab./Kota "+str(p.desa.kecamatan.kabupaten)
					data = {'success': True, 'pesan': 'Perusahaan disimpan. Proses Selanjutnya.','data' : [
						{'npwp_perusahaan': p.npwp},
						{'nama_perusahaan': p.nama_perusahaan},
						{'alamat_perusahaan': alamat_ },
						{'kode_pos_perusahaan': p.kode_pos},
						{'telepon_perusahaan': p.telepon},
						{'fax_perusahaan': p.fax},
						{'email_perusahaan': p.email}
						]}
					data = json.dumps(data)
					response = HttpResponse(json.dumps(data))
				else:
					data = perusahaan.errors.as_json()
					data = json.dumps(data)
			# response.set_cookie(key='npwp', value=p.npwp)
			# response.set_cookie(key='nama_perusahaan', value=p.nama_perusahaan)
			# alamat_ = str(p.alamat_perusahaan)+" "+str(p.desa)+", Kec. "+str(p.desa.kecamatan)+", Kab./Kota "+str(p.desa.kecamatan.kabupaten)
			# response.set_cookie(key='alamat_perusahaan', value=alamat_)
			# response.set_cookie(key='kode_pos', value=p.kode_pos)
			# response.set_cookie(key='telepon', value=p.telepon)
			# response.set_cookie(key='fax', value=p.fax)
			# response.set_cookie(key='email', value=p.email)
				
			# data = json.dumps(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pemohon tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pemohon tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
	# print "http respon"
	response = HttpResponse(data)
	try:
		get_perusahaan = Perusahaan.objects.get(npwp=request.POST.get('npwp'))
		response.set_cookie(key='id_perusahaan', value=get_perusahaan.id)
	except ObjectDoesNotExist:
		response.set_cookie(key='id_perusahaan', value=p.id)
	# if Perusahaan.objects.filter(npwp=request.POST.get('npwp')) is not None:
	# 	response.set_cookie(key='id_perusahaan', value=get_perusahaan.id)
	# else:
	# 	response.set_cookie(key='id_perusahaan', value=perusahaan.id)
	return response

def siup_detilsiup_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilSIUP.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			detilSIUP = PengajuanSiupForm(request.POST, instance=pengajuan_)
			if detilSIUP.is_valid():
				try:
					kbli_list = request.POST.getlist('kbli')
					produk_utama_list = request.POST.getlist('produk_utama')
					detilSIUP.perusahaan = request.COOKIES['id_perusahaan']
					detilSIUP.save()
					# print "kbli"+kbli_list
					# print str(produk_utama_list)
					#++++++++++++++++multi select manytomany ++++++++
					for kbli in kbli_list:
						pengajuan_.kbli.add(KBLI.objects.get(id=kbli))
					for produk_utama in produk_utama_list:
						pengajuan_.produk_utama.add(ProdukUtama.objects.get(id=produk_utama))
					#++++++++++++++++ end multi select manytomany ++++++++
					# pengajuan_.bentuk_kegiatan_usaha.kegiatan_usaha print
					# detilSIUP.bentuk_kegiatan_usaha.kegiatan_usaha
					kbli_json = [k.as_json() for k in KBLI.objects.filter(id__in=kbli_list)]
					data = {'success': True, 
						'pesan': 'Detail SIUP berhasil disimpan. Proses Selanjutnya.', 
						'data': [
							{'bentuk_kegiatan_usaha': pengajuan_.bentuk_kegiatan_usaha.kegiatan_usaha},
							{'kekayaan_bersih': str(pengajuan_.kekayaan_bersih)},
							{'status_penanaman_modal': pengajuan_.jenis_penanaman_modal.jenis_penanaman_modal },
							{'total_nilai_saham': str(pengajuan_.total_nilai_saham)},
							{'presentase_saham_nasional': str(pengajuan_.presentase_saham_nasional)+" %"},
							{'presentase_saham_asing': str(pengajuan_.presentase_saham_asing)+" %"},
							{'kelembagaan': pengajuan_.kelembagaan.kelembagaan},
							# {'produk_utama': pengajuan_.produk_utama.all()},
							{'kbli': kbli_json},
						]
					}
					data = json.dumps(data)
					response = HttpResponse(json.dumps(data))
				except ObjectDoesNotExist:
					data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar.'}]}
					data = json.dumps(data)
			else:
				data = detilSIUP.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	response.set_cookie(key='id_detail_siup', value=pengajuan_.id)
	return response

def siup_legalitas_perusahaan_save_cookie(request):
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			if 'id_pengajuan' in request.COOKIES.keys():
				if request.COOKIES['id_pengajuan'] != '':
					pengajuan_ = DetilSIUP.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
					form = LegalitasPerusahaanForm(request.POST)
					if form.is_valid():
						f = form.save(commit=False)
						f.perusahaan_id = request.COOKIES['id_perusahaan']
						f.save()
						pengajuan_.legalitas.add(f)
						if request.POST.get('onoffswitch') == 'on':
							formperubahan = LegalitasPerusahaanPerubahanForm(request.POST)
							if formperubahan.is_valid():
								legalitas = Legalitas(
									jenis_legalitas_id = 2,
									perusahaan_id = request.COOKIES['id_perusahaan'],
									nama_notaris=request.POST.get('nama_notaris_perubahan'), 
									alamat=request.POST.get('alamat_notaris_perubahan'), 
									telephone=request.POST.get('telephone_notaris_perubahan'), 
									nomor_pengesahan=request.POST.get('nomor_pengesahan_perubahan'), 
									tanggal_pengesahan=formperubahan.cleaned_data['tanggal_pengesahan_perubahan'])
								legalitas.save()
								pengajuan_.legalitas.add(legalitas)
							else:
								data = formperubahan.errors.as_json()
						else:
							data = {'Terjadi Kesalahan': [{'message': 'Data Perusahaan tidak ditemukan/data kosong'}]}
							data = json.dumps(data)
						# +++++++++++++++ change PengajuanIzin manytomany legalitas ++++++++
						
						
						# +++++++++++++++ end change PengajuanIzin manytomany legalitas ++++++++
						data = {'success': True, 'pesan': 'Legalitas Perusahaan berhasil disimpan. Proses Selanjutnya.', 'data': [
						{'jenis_legalitas': f.jenis_legalitas.jenis_legalitas},
						{'nama_notaris': f.nama_notaris},
						{'alamat_notaris': f.alamat},
						{'telephone_notaris': f.telephone},
						{'nomor_pengesahaan': f.nomor_pengesahan},
						{'tanggal_pengesahan': str(f.tanggal_pengesahan)},
						# # legalitas perubahaan
						{'jenis_legalitas_perubahan': legalitas.jenis_legalitas.jenis_legalitas},
						{'nama_notaris_perubahan': legalitas.nama_notaris},
						{'alamat_notaris_perubahan': legalitas.alamat},
						{'telephone_notaris_perubahan': legalitas.telephone},
						{'nomor_pengesahaan_perubahan': legalitas.nomor_pengesahan},
						{'tanggal_pengesahan_perubahan': str(legalitas.tanggal_pengesahan)}
						]}
						data = json.dumps(data)
					else:
						data = form.errors.as_json()
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
					data = json.dumps(data)
			else:
				data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/tidak ada'}]}
				data = json.dumps(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	response.set_cookie(key='id_legalitas', value=f.id)
	response.set_cookie(key='id_legalitas_perubahan', value=legalitas.id)
	return response

def siup_upload_dokumen_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': [] }
	return HttpResponse(json.dumps(data))

def siup_upload_berkas_foto_pemohon(request):
	if 'id_pemohon' in request.COOKIES.keys():
		if request.COOKIES['id_pemohon'] != '':
			form = UploadBerkasFotoForm(request.POST, request.FILES)
			# print request.FILES
			if request.method == "POST":
				if request.FILES.get('berkas'):
					if form.is_valid():
						try:
							berkas = form.save(commit=False)
							# update model yang lain.
							p = Pemohon.objects.get(id=request.COOKIES['id_pemohon'])
							berkas.nama_berkas = "Foto Pemohon "+p.nama_lengkap
							berkas.save()
							# save many to many table
							p.berkas_foto.add(berkas)

							data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
									{'status_upload': 'ok'},
								]}
						except ObjectDoesNotExist:
							data = {'Terjadi Kesalahan': [{'message': 'Pemohon tidak ada dalam daftar.'}]}
						data = json.dumps(data)
					else:
						data = form.errors.as_json()
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong.'}]}
					data = json.dumps(data)
			else:
				data = form.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload NPWP Perusahaan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload NPWP Perusahaan tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response

def siup_upload_berkas_ktp_pemohon(request):
	if 'id_pemohon' in request.COOKIES.keys():
		if request.COOKIES['id_pemohon'] and request.COOKIES['nomor_ktp'] != '':
			ktp_ = NomorIdentitasPengguna.objects.get(nomor="1222")
			form = UploadBerkasKTPForm(request.POST, request.FILES)
			if request.method == "POST":
				if request.FILES.get('berkas'):
					if form.is_valid():
						berkas = form.save(commit=False)
						berkas.nama_berkas = "Berkas KTP Pemohon"
						berkas.save()
						# update model yang lain.
						# p = Perushaan.object.get(id=request.COOKIES['id_perusahaan'])
						ktp_.berkas_id = berkas.id
						ktp_.save()

						data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
								{'status_upload': 'ok'},
							]}
						data = json.dumps(data)
					else:
						data = form.errors.as_json()
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong'}]}
					data = json.dumps(data)
			else:
				data = form.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload KTP/Paspor tidak ditemukan/data kosong.2'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload KTP/Paspor tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response

def siup_upload_berkas_npwp_pribadi(request):
	if 'id_pemohon' in request.COOKIES.keys():
		if request.COOKIES['id_pemohon'] != '':
			form = UploadBerkasNPWPPribadiForm(request.POST, request.FILES)
			# print request.FILES
			if request.method == "POST":
				if request.FILES.get('berkas'):
					if form.is_valid():
						# update model yang lain.
						try:
							berkas = form.save(commit=False)
							d = DetilSIUP.objects.get(id=request.COOKIES['id_detail_siup'])
							p = Pemohon.objects.get(id=request.COOKIES['id_pemohon'])
							berkas.nama_berkas = "NPWP Pribadi "+p.nama_lengkap
							berkas.save()
							p.berkas_npwp = berkas
							p.save()
							d.berkas_npwp_pemohon = berkas
							d.save()

							data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
									{'status_upload': 'ok'},
								]}
						except ObjectDoesNotExist:
							data = {'Terjadi Kesalahan': [{'message': 'Pemohon tidak ada dalam daftar'}]}
						data = json.dumps(data)
					else:
						data = form.errors.as_json()
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong'}]}
					data = json.dumps(data)
			else:
				data = form.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload NPWP Perusahaan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload NPWP Perusahaan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response

def siup_upload_berkas_npwp_perusahaan(request):
	# print request.COOKIES['id_perusahaan']
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			form = UploadBerkasNPWPPerusahaanForm(request.POST, request.FILES)
			if request.method == "POST":
				if request.FILES.get('berkas'):
					if form.is_valid():
						# update model yang lain.
						try:
							d = DetilSIUP.objects.get(id=request.COOKIES['id_detail_siup'])
							p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
							berkas = form.save(commit=False)
							berkas.nama_berkas = "NPWP Perusahaan "+p.nama_perusahaan
							berkas.save()
							p.berkas_npwp = berkas
							p.save()
							d.berkas_npwp_perusahaan = berkas
							d.save()
							data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
								{'status_upload': 'ok'},
							]}
						except ObjectDoesNotExist:
							data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar.'}]}					
						data = json.dumps(data)
					else:
						data = form.errors.as_json()
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong.'}]}
					data = json.dumps(data)
			else:
				data = form.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload NPWP Perusahaan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload NPWP Perusahaan tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response	

def siup_upload_berkas_akta_pendirian(request):
	# print request.COOKIES['id_legalitas']
	if 'id_legalitas' in request.COOKIES.keys():
		if request.COOKIES['id_legalitas'] != '':
			form = UploadBerkasAktaPendirianForm(request.POST, request.FILES)
			if request.method == "POST":
				if request.FILES.get('berkas'):
					if form.is_valid():
						try:
							a = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
							berkas = form.save(commit=False)
							berkas.nama_berkas = "Berkas Akta Pendirian "+a.nama_perusahaan
							berkas.save()
							# update model yang lain.

							p = Legalitas.objects.get(id=request.COOKIES['id_legalitas'])
							p.berkas = berkas
							p.save()
							data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
								{'status_upload': 'ok'},
							]}
						except ObjectDoesNotExist:
							data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar'}]}
						data = json.dumps(data)
					else:
						data = form.errors.as_json()
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong'}]}
					data = json.dumps(data)
			else:
				data = form.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload Akta Pendirian tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload Akta Pendirian tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response

def siup_upload_berkas_akta_perubahan(request):
	if 'id_legalitas_perubahan' in request.COOKIES.keys():
		if request.COOKIES['id_legalitas_perubahan'] != '':
			form = UploadBerkasAktaPerubahanForm(request.POST, request.FILES)
			if request.method == "POST":
				if request.FILES.get('berkas'):
					if form.is_valid():
						try:
							a = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
							berkas = form.save(commit=False)
							berkas.nama_berkas = "Berkas Akta Perubahan "+a.nama_perusahaan
							berkas.save()
							# update model yang lain.
							p = Legalitas.objects.get(id=request.COOKIES['id_legalitas_perubahan'])
							p.berkas = berkas
							p.save()

							data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
									{'status_upload': 'ok'},
								]}
						except ObjectDoesNotExist:
							data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar'}]}
						data = json.dumps(data)		
					else:
						data = form.errors.as_json()
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong'}]}
					data = json.dumps(data)
			else:
				data = form.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload Akta Perubahan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload Akta Perubahan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response

def siup_upload_berkas_pendukung(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			form = UploadBerkasPendukungForm(request.POST, request.FILES)
			# print request.FILES
			if request.method == "POST":
				if request.FILES.get('berkas'):
					if form.is_valid():
						try:
							p = PengajuanIzin.objects.get(id=request.COOKIES['id_pengajuan'])
							berkas = form.save(commit=False)
							berkas.nama_berkas = "Berkas Pendukung "+p.pemohon.nama_lengkap
							berkas.save()
							p.berkas_tambahan.add(berkas)

							data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
									{'status_upload': 'ok'},
								]}
						except ObjectDoesNotExist:
							data = {'Terjadi Kesalahan': [{'message': 'Pengajuan tidak ada dalam daftar'}]}
						data = json.dumps(data)
					else:
						data = form.errors.as_json()
				else:
					data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong'}]}
					data = json.dumps(data)
			else:
				data = form.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload berkas pendukung tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
	response = HttpResponse(data)
	return response

def siup_done(request):
	data = {'success': True, 'pesan': 'Proses Selesai.' }
	response = HttpResponse(json.dumps(data))
	# For delete cookie
	response.delete_cookie(key='nama_lengkap') # set cookie	
	response.delete_cookie(key='id_pemohon') # set cookie	
	response.delete_cookie(key='jenis_permohonan') # set cookie
	response.delete_cookie(key='ktp') # set cookie	
	response.delete_cookie(key='alamat') # set cookie
	response.delete_cookie(key='jenis_pemohon') # set cookie
	response.delete_cookie(key='hp') # set cookie	
	response.delete_cookie(key='telephone') # set cookie
	response.delete_cookie(key='kewarganegaraan') # set cookie
	response.delete_cookie(key='ttl') # set cookie
	response.delete_cookie(key='email') # set cookie	
	response.delete_cookie(key='id_kelompok_izin') # set cookie
	return response

def siup_front_done(request):
	data = {'success': True, 'pesan': 'Proses Selesai.' }
	response = HttpResponse(json.dumps(data))
	return response
