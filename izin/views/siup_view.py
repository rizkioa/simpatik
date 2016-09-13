from django.http import HttpResponse
import json

from izin.izin_forms import PemohonForm, PerusahaanForm
from izin.utils import get_nomor_pengajuan
from accounts.models import NomorIdentitasPengguna
from izin.models import PengajuanIzin, Pemohon, JenisPermohonanIzin, DetilSIUP
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

		data = {'success': True, 'pesan': 'Pengajuan disimpan. Proses Selanjutnya.'  }
		response = HttpResponse(json.dumps(data))	

		response.set_cookie(key='id_pemohon', value=p.id)
		response.set_cookie(key='nama_lengkap', value=p.nama_lengkap) # set cookie	
		if jenis_permohonan_:
			response.set_cookie(key='jenis_permohonan', value=pengajuan.jenis_permohonan) # set cookie	
		if ktp_ or paspor_:
			value = ""
			if ktp_:
				value += "KTP "+str(ktp_)
			if paspor_:
				value += ", PASPOR "+str(paspor_)
			response.set_cookie(key='ktp', value=value) # set cookie	
		if p.desa:
			alamat_ = str(p.alamat)+" "+str(p.desa)+", Kec. "+str(p.desa.kecamatan)+", Kab./Kota "+str(p.desa.kecamatan.kabupaten)
			response.set_cookie(key='alamat', value=alamat_) # set cookie	
		if p.jenis_pemohon:
			response.set_cookie(key='jenis_pemohon', value=p.jenis_pemohon) # set cookie	
		if p.hp:
			response.set_cookie(key='hp', value=p.hp) # set cookie	
		if p.telephone:
			response.set_cookie(key='telephone', value=p.telephone) # set cookie	
		if p.kewarganegaraan:
			response.set_cookie(key='kewarganegaraan', value=p.kewarganegaraan) # set cookie	
		if p.tempat_lahir:
			ttl_ = str(p.tempat_lahir)+", "+str(p.tanggal_lahir)
			response.set_cookie(key='ttl', value=ttl_) # set cookie
		if p.email:
			response.set_cookie(key='email', value=p.email) # set cookie	
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

		data = {'success': True, 'pesan': 'Perusahaan disimpan. Proses Selanjutnya.'  }
		response = HttpResponse(json.dumps(data))
		
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
	data = {'success': True, 'pesan': 'Proses Selanjutnya.' }
	return HttpResponse(json.dumps(data))

def siup_legalitas_perusahaan_save_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.' }
	return HttpResponse(json.dumps(data))

def siup_kekayaan_save_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.' }
	return HttpResponse(json.dumps(data))

def siup_upload_dokumen_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.' }
	return HttpResponse(json.dumps(data))

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