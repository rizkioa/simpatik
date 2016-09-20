from django.http import HttpResponse
import json

from izin.izin_forms import PemohonForm, PerusahaanForm, PengajuanSiupForm, LegalitasPerusahaanForm, AktaPerusahaanForm, NPWPPerusahaanForm
from izin.utils import get_nomor_pengajuan
from accounts.models import NomorIdentitasPengguna
from izin.models import PengajuanIzin, Pemohon, JenisPermohonanIzin, DetilSIUP, KelompokJenisIzin
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

try:
	from django.utils.encoding import force_text
except ImportError:
	from django.utils.encoding import force_unicode as force_text

from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

def siup_identitas_pemohon_save_cookie(request):
	pemohon = PemohonForm(request.POST) 
	if pemohon.is_valid():
		# Untuk Nomor Identitas
		ktp_ = request.POST.get('ktp', None)
		paspor_ = request.POST.get('paspor', None)
		jenis_pemohon = request.POST.get('jenis_pemohon', None)
		# print jenis_pemohon
		# End
		jenis_permohonan_ = request.POST.get('jenis_pengajuan', None)
		k = KelompokJenisIzin.objects.filter(id=request.COOKIES['id_kelompok_izin']).last()
		nomor_pengajuan_ = get_nomor_pengajuan(k.jenis_izin.kode)
		try:
			p = pemohon.save(commit=False)
			# print pemohon.cleaned_data
			p.username = ktp_
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

		except IntegrityError as e:
			if ktp_:
				p = Pemohon.objects.get(username = ktp_)
			elif paspor_:
				p = Pemohon.objects.get(username = paspor_)
			elif ktp_ and paspor_:
				p = Pemohon.objects.get(username = ktp_)

			# print p.id
			# print p.desa
			
		pengajuan = DetilSIUP(no_pengajuan=nomor_pengajuan_, kelompok_jenis_izin_id=request.COOKIES['id_kelompok_izin'], pemohon_id=p.id,jenis_permohonan_id=jenis_permohonan_, created_by=request.user  )
		pengajuan.save()

		# data = {'success': True, 'pesan': 'Pengajuan disimpan. Proses Selanjutnya.'  }
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

		data = {'success': True, 'pesan': 'Proses Selanjutnya' ,'data': [
			{'nama_lengkap': pemohon.cleaned_data['nama_lengkap']},
			{'jenis_permohonan': jenis_permohonan_},
			{'jenis_pemohon': jenis_ },
			{'nomor_ktp': ktp_},
			{'alamat': pemohon.cleaned_data['alamat']},
			{'telephone': pemohon.cleaned_data['telephone']},
			{'hp': pemohon.cleaned_data['hp']},
			{'email': email_ },
			{'kewarganegaraan': pemohon.cleaned_data['kewarganegaraan']},
			{'pekerjaan': pemohon.cleaned_data['pekerjaan']}
			]}
		response = HttpResponse(json.dumps(data))	

		response.set_cookie(key='id_pengajuan', value=pengajuan.id)
		response.set_cookie(key='id_pemohon', value=p.id)
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
	perusahaan = PerusahaanForm(request.POST) 
	if perusahaan.is_valid():
		p = perusahaan.save(commit=False)
		p.pemohon_id = request.COOKIES['id_pemohon']
		p.save()

		data = {'success': True, 'pesan': 'Perusahaan disimpan. Proses Selanjutnya.','data': [
			
			]  }
		response = HttpResponse(json.dumps(data))
		
		response.set_cookie(key='id_perusahaan', value=p.id)
		response.set_cookie(key='npwp', value=p.npwp)
		response.set_cookie(key='nama_perusahaan', value=p.nama_perusahaan)
		alamat_ = str(p.alamat_perusahaan)+" "+str(p.desa)+", Kec. "+str(p.desa.kecamatan)+", Kab./Kota "+str(p.desa.kecamatan.kabupaten)
		response.set_cookie(key='alamat_perusahaan', value=alamat_)
		response.set_cookie(key='kode_pos', value=p.kode_pos)
		response.set_cookie(key='telepon', value=p.telepon)
		response.set_cookie(key='fax', value=p.fax)
		response.set_cookie(key='email', value=p.email)

	else:
		data = perusahaan.errors.as_json()
		response = HttpResponse(data)
	return response

def siup_detilsiup_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilSIUP.objects.get(pengajuanizin_ptr_id=request.COOKIES['id_pengajuan'])
			detilSIUP = PengajuanSiupForm(request.POST, instance=pengajuan_)
			if detilSIUP.is_valid():
				detilSIUP.save()
				data = {'success': True, 'pesan': 'Detail SIUP berhasil disimpan. Proses Selanjutnya.'}
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

	return response

from perusahaan.models import Perusahaan
def siup_legalitas_perusahaan_save_cookie(request):
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			form = LegalitasPerusahaanForm(request.POST)
			if form.is_valid():
				f = form.save(commit=False)
				f.perusahaan_id = request.COOKIES['id_perusahaan']
				f.save()

				data = {'success': True, 'pesan': 'Legalitas Perusahaan berhasil disimpan. Proses Selanjutnya.'}
				data = json.dumps(data)
			else:
				data = form.errors.as_json()
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Perusahaan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Perusahaan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)

	response = HttpResponse(data)
	return response

def siup_kekayaan_save_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.' }
	return HttpResponse(json.dumps(data))

def siup_upload_dokumen_cookie(request):
	form = NPWPPerusahaanForm(request.POST, request.FILES)
	print request.FILES
	if request.method == "POST":
		if request.FILES.get('npwp_perusahaan'):
			perusahaan = Perusahaan.objects.get(id=100)
			perusahaan.berkas_npwp = request.FILES.get('npwp_perusahaan')
			perusahaan.save()
			data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
						{'status_upload': 'ok'},
					]}
			data = json.dumps(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Berkas kosong'}]}
			data = json.dumps(data)
	else:
		data = form.errors.as_json()
	# if 'id_perusahaan' in request.COOKIES.keys():
	# 	if request.COOKIES['id_perusahaan'] != '':
	# 		form = NPWPPerusahaanForm(request.POST, request.FILES)
	# 		if form.is_valid():
	# 			perusahaan = Perusahaan(berkas_npwp=request.FILES['file'])
	# 			perusahaan.save()
	# 			data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
	# 						{'status_upload': 'ok'},
	# 					]}
	# 			data = json.dumps(data)
	# 		else:
	# 			data = form.errors.as_json()
	# 	else:
	# 		data = {'Terjadi Kesalahan': [{'message': 'Data Perusahaan tidak ditemukan/data kosong'}]}
	# 		data = json.dumps(data)
	# else:
	# 	data = {'Terjadi Kesalahan': [{'message': 'Data Perusahaan tidak ditemukan/tidak ada'}]}
	# 	data = json.dumps(data)

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