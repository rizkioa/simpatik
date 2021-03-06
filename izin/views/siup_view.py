import os, json, datetime
from decimal import Decimal
from sqlite3 import OperationalError

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
try:
	from django.utils.encoding import force_text
except ImportError:
	from django.utils.encoding import force_unicode as force_text
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import IntegrityError

from izin.izin_forms import PemohonForm, PerusahaanForm, PengajuanSiupForm, LegalitasPerusahaanForm, UploadBerkasPendukungForm, UploadBerkasNPWPPerusahaanForm, UploadBerkasFotoForm, UploadBerkasKTPForm, UploadBerkasNPWPPribadiForm, UploadBerkasAktaPendirianForm, UploadBerkasAktaPerubahanForm, LegalitasPerusahaanPerubahanForm
from izin.utils import formatrupiah, get_model_detil, get_nomor_pengajuan

from izin import models as app_models
from izin.models import PengajuanIzin, Pemohon, JenisPermohonanIzin, DetilSIUP, KelompokJenisIzin, Riwayat, DetilReklame, DetilTDP,DetilIMBPapanReklame,DetilIMB,InformasiKekayaanDaerah,DetilHO,InformasiTanah,DetilHuller, Kelembagaan, DetilTDUP
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from perusahaan.models import Legalitas, KBLI, Perusahaan
from accounts.models import NomorIdentitasPengguna, Account
from master.models import Berkas
from django.db import connection
from izin_dinkes.models import Apotek

def set_cookie(response, key, value, days_expire = 7):
  if days_expire is None:
	max_age = 365 * 24 * 60 * 60  #one year
  else:
	max_age = days_expire * 24 * 60 * 60 
  expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

def siup_identitas_pemohon_save_cookie(request):
	try:
		p = Pemohon.objects.get(username = request.POST.get('ktp'))
		pemohon = PemohonForm(request.POST, instance=p)
	except ObjectDoesNotExist:		
		pemohon = PemohonForm(request.POST)		

	if pemohon.is_valid():
		# Untuk Nomor Identitas
		ktp_ = request.POST.get('ktp', None)
		paspor_ = request.POST.get('paspor', None)
		jenis_pemohon = request.POST.get('jenis_pemohon', None)
		# End
		jenis_permohonan_ = request.POST.get('jenis_pengajuan', None)
		# default query kelompok jenis izin berdasarkan id
		k = KelompokJenisIzin.objects.filter(id=request.COOKIES['id_kelompok_izin']).last()
		# dan jika cookie kode kelompok jenis izin ada id query berdasarkan kode
		# untuk memastikan keadaan benar atau tidak id itu 
		if 'kode_kelompok_jenis_izin' in request.COOKIES.keys():
			if request.COOKIES.get('kode_kelompok_jenis_izin', None) and request.COOKIES.get('kode_kelompok_jenis_izin', None) is not None:
				k = KelompokJenisIzin.objects.filter(kode=request.COOKIES.get('kode_kelompok_jenis_izin', None))
				if k.exists():
					k = k.last()
		nomor_pengajuan_ = get_nomor_pengajuan(k.jenis_izin.kode)
		nama_kuasa = request.POST.get('nama_kuasa', None)
		no_identitas_kuasa = request.POST.get('no_identitas_kuasa', None)
		telephone_kuasa = request.POST.get('telephone_kuasa', None)

		p = pemohon.save(commit=False)
		p.username = ktp_
		try:
			p.save()
		except IntegrityError:
			try:
				akun = Account.objects.get(username=ktp_)
				if not hasattr(akun, 'pemohon'):
					cursor = connection.cursor()
					cursor.execute('INSERT INTO izin_pemohon (account_ptr_id, jenis_pemohon_id) values (%s, %s)', (akun.id, jenis_permohonan_))
					akun = Account.objects.get(username=ktp_)
					if hasattr(akun, 'pemohon'):
						pemohon = PemohonForm(request.POST)
						p = pemohon.save(commit=False)
						p.username = ktp_
						p.save()
					else:
						data = {'success': False, 'pesan': 'Nomor Identitas KTP pemohon bermasalah.'}
						return HttpResponse(json.dumps(data))
			except Account.DoesNotExist:
				data = {'success': False, 'pesan': 'Nomor Identitas KTP pemohon bermasalah.'}
				return HttpResponse(json.dumps(data))
		if ktp_:
			try:
				i = NomorIdentitasPengguna.objects.get(nomor = ktp_, jenis_identitas_id=1, user_id=p.id)
			except ObjectDoesNotExist:
				i, created = NomorIdentitasPengguna.objects.get_or_create(
							nomor = ktp_,
							jenis_identitas_id=1, # untuk KTP harusnya membutuhkan kode lagi
							user_id=p.id,
							)
		if paspor_:
			try:
				i = NomorIdentitasPengguna.objects.get(nomor = paspor_, jenis_identitas_id=2, user_id=p.id)
			except ObjectDoesNotExist:
				i, created = NomorIdentitasPengguna.objects.get_or_create(
							nomor = paspor_,
							jenis_identitas_id=2,
							user_id=p.id,
							)

		i.save()

		# if k.kode == "503.08":
		# 	objects_ = getattr(app_models, 'DetilSIUP')
		# elif k.kode == "IUJK":
		# 	objects_ = getattr(app_models, 'DetilIUJK')
		# elif k.kode == "503.03.01/" or k.kode == "503.03.02/":
		# 	objects_ = getattr(app_models, 'DetilReklame')
		# elif k.kode == "TDP-PT" or k.kode == "TDP-CV" or k.kode == "TDP-FIRMA" or k.kode == "TDP-PERORANGAN" or k.kode == "TDP-BUL" or k.kode == "TDP-KOPERASI":
		# 	objects_ = getattr(app_models, 'DetilTDP')
		# elif k.kode == "503.01.06/":
		# 	objects_ = getattr(app_models, 'DetilIMBPapanReklame')
		# elif k.kode == "503.01.05/" or k.kode == "503.01.04/" :
		# 	objects_ = getattr(app_models, 'DetilIMB')
		# elif k.kode == "503.06.01/":
		# 	objects_ = getattr(app_models, 'InformasiKekayaanDaerah')
		# elif k.kode == "503.02/":
		# 	objects_ = getattr(app_models, 'DetilHO')
		# elif k.kode == "503.07/" or k.kode == "IPPT-Rumah" or k.kode == "IPPT-Usaha":
		# 	objects_ = getattr(app_models, 'InformasiTanah')
		# elif k.kode == "HULLER":
		# 	objects_ = getattr(app_models, 'DetilHuller')
		# elif k.kode == "TDUP":
		# 	objects_ = getattr(app_models, 'DetilTDUP')
		# elif k.kode == "IUA":
		# 	objects_ = getattr(app_models, 'DetilIUA')

		objects_ = get_model_detil(k.kode)
		print objects_	
		if request.user.is_anonymous():
			created_by = p.id
		else:
			created_by =  request.user.id

		if objects_:
			try:
				pengajuan = objects_.objects.get(id=request.COOKIES['id_pengajuan'])
				pengajuan.status = 11
				pengajuan.nama_kuasa = nama_kuasa
				pengajuan.no_identitas_kuasa = no_identitas_kuasa
				pengajuan.telephone_kuasa = telephone_kuasa
				pengajuan.jenis_permohonan_id = jenis_permohonan_
			except ObjectDoesNotExist:
				pengajuan = objects_(status=11,no_pengajuan=nomor_pengajuan_, kelompok_jenis_izin_id=request.COOKIES['id_kelompok_izin'], pemohon_id=p.id, jenis_permohonan_id=jenis_permohonan_, created_by_id=created_by, nama_kuasa=nama_kuasa, no_identitas_kuasa=no_identitas_kuasa, telephone_kuasa=telephone_kuasa)
			pengajuan.save()

		riwayat_ = Riwayat(
						pengajuan_izin_id = pengajuan.id,
						created_by_id = p.id,
						keterangan = "Draf (Pengajuan)",
						alasan=''
					)
		riwayat_.save()

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
		alamat_ = ""
		if pengajuan.pemohon.desa:
			alamat_ = str(pengajuan.pemohon.alamat)+", DESA "+str(pengajuan.pemohon.desa.nama_desa)+", KEC. "+str(pengajuan.pemohon.desa.kecamatan.nama_kecamatan)+", "+str(pengajuan.pemohon.desa.kecamatan.kabupaten.nama_kabupaten)

		data = {'success': True, 'pesan': 'Identitas Pemohon berhasil tersimpan. Proses Selanjutnya.' ,'data': [
			{'nama_lengkap': pemohon.cleaned_data['nama_lengkap']},
			{'jenis_permohonan': jenis_permohonan_},
			{'jenis_pemohon': jenis_ },
			{'nomor_ktp': ktp_},
			{'nomor_paspor': paspor_},
			{'alamat': alamat_},
			{'telephone': pemohon.cleaned_data['telephone']},
			{'hp': pemohon.cleaned_data['hp']},
			{'email': email_ },
			{'kewarganegaraan': pemohon.cleaned_data['kewarganegaraan']},
			{'pekerjaan': pemohon.cleaned_data['pekerjaan']},
			{'nama_kuasa': nama_kuasa},
			{'no_identitas_kuasa': no_identitas_kuasa},
			{'telephone_kuasa': telephone_kuasa}
			]}
		# domain_name =  request.get_full_path()
		# path_name =  request.META['HTTP_HOST']
		# path_name = request.POST.get('path_name', '/')
		response = HttpResponse(json.dumps(data))	
		response.set_cookie(key='id_pengajuan', value=pengajuan.id)
		response.set_cookie(key='id_pemohon', value=p.id)
		response.set_cookie(key='nomor_ktp', value=ktp_)
		if paspor_:
			response.set_cookie(key='nomor_paspor', value=paspor_)
		else:
			response.set_cookie(key='nomor_paspor', value='0')
		response.set_cookie(key='id_jenis_pengajuan', value=jenis_permohonan_)
	else:
		data = pemohon.errors.as_json() # untuk mengembalikan error form berupa json
		response = HttpResponse(data)
	return response

def siup_identitas_perusahan_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			k = KelompokJenisIzin.objects.filter(id=request.COOKIES['id_kelompok_izin']).last()
			# if k.kode == "503.08":
			# 	objects_ = getattr(app_models, 'DetilSIUP')
			# elif k.kode == "IUJK":
			# 	objects_ = getattr(app_models, 'DetilIUJK')
			# elif k.kode == "503.03.01/" or k.kode == "503.03.02/":
			# 	objects_ = getattr(app_models, 'DetilReklame')
			# elif k.kode == "TDP-PT" or k.kode == "TDP-CV" or k.kode == "TDP-FIRMA" or k.kode == "TDP-PERORANGAN" or k.kode == "TDP-BUL" or k.kode == "TDP-KOPERASI":
			# 	objects_ = getattr(app_models, 'DetilTDP')
			# elif k.kode == "503.01.06/":
			# 	objects_ = getattr(app_models, 'DetilIMBPapanReklame')
			# elif k.kode == "503.01.05/" or k.kode == "503.01.04/" :
			# 	objects_ = getattr(app_models, 'DetilIMB')
			# elif k.kode == "503.06.01/":
			# 	objects_ = getattr(app_models, 'InformasiKekayaanDaerah')
			# elif k.kode == "503.02/":
			# 	objects_ = getattr(app_models, 'DetilHO')
			# elif k.kode == "503.07/" or k.kode == "IPPT-Rumah" or k.kode == "IPPT-Usaha":
			# 	objects_ = getattr(app_models, 'InformasiTanah')
			# elif k.kode == "HULLER":
			# 	objects_ = getattr(app_models, 'DetilHuller')
			# elif k.kode == "TDUP":
			# 	objects_ = getattr(app_models, 'DetilTDUP')
			# elif k.kode == "IUA":
			# 	objects_ = getattr(app_models, 'DetilIUA')
			objects_ = get_model_detil(k.kode)
			try:
				get_perusahaan = Perusahaan.objects.get(npwp=request.POST.get('npwp'))
				print get_perusahaan
				perusahaan = PerusahaanForm(request.POST, instance=get_perusahaan)
				if perusahaan.is_valid():
					per = perusahaan.save(commit=False)
					per.penanggung_jawab_id = request.COOKIES['id_pemohon']
					if request.user.is_authenticated():
						per.created_by = request.user
					else:
						per.created_by_id = request.COOKIES['id_pemohon']
					per.save()
					
					if objects_:

						# print objects_
						# try:
						# 	print "masuk pengajuan  perusahaan try"
						# 	pengajuan = objects_.objects.get(id=request.COOKIES['id_pengajuan'])
						# 	pengajuan.perusahaan_id = per.id
						# 	print per.id
						# 	pengajuan.save()
						# except ObjectDoesNotExist:
						# 	pengajuan = objects_(perusahaan=per)
						# pengajuan.save()
						# print pengajuan
						pengajuan_ = objects_.objects.filter(id=request.COOKIES['id_pengajuan']).last()
						# print pengajuan_
						pengajuan_.perusahaan_id = per.id
						pengajuan_.save()
						# print pengajuan_.perusahaan

					email_ = ""
					if get_perusahaan.email:
						email_ = get_perusahaan.email
					alamat_ = str(get_perusahaan.alamat_perusahaan)+", DESA "+str(get_perusahaan.desa)+", KEC. "+str(get_perusahaan.desa.kecamatan)+", "+str(get_perusahaan.desa.kecamatan.kabupaten)
					data = {'success': True, 'pesan': 'Perusahaan disimpan. Proses Selanjutnya.','data' : [
						{'npwp_perusahaan': get_perusahaan.npwp},
						{'nama_perusahaan': get_perusahaan.nama_perusahaan},
						{'alamat_perusahaan': alamat_ },
						{'kode_pos_perusahaan': get_perusahaan.kode_pos},
						{'telepon_perusahaan': get_perusahaan.telepon},
						{'fax_perusahaan': get_perusahaan.fax},
						{'email_perusahaan': email_}
					]}
					data = json.dumps(data)
					response = HttpResponse(data)
					response.set_cookie(key='id_perusahaan', value=get_perusahaan.id)
					response.set_cookie(key='npwp_perusahaan', value=get_perusahaan.npwp)
				else:
					data = perusahaan.errors.as_json()
					response = HttpResponse(data)
			except Perusahaan.DoesNotExist:
				perusahaan = PerusahaanForm(request.POST) 
				if perusahaan.is_valid():
					p = perusahaan.save(commit=False)
					p.penanggung_jawab_id = request.COOKIES['id_pemohon']
					if request.user.is_authenticated():
						p.created_by = request.user
					else:
						p.created_by_id = request.COOKIES['id_pemohon']
					p.save()
					if objects_:
						# try:
						# 	print "masuk pengajuan  perusahaan except"
						# 	pengajuan = objects_.objects.get(id=request.COOKIES['id_pengajuan'])
						# 	print p.id
						# 	pengajuan.perusahaan_id = p.id
						# except ObjectDoesNotExist:
						# 	pengajuan = objects_(perusahaan=p)
						# pengajuan.save()
						# print pengajuan
						pengajuan_ = objects_.objects.filter(id=request.COOKIES['id_pengajuan']).last()
						pengajuan_.perusahaan_id = p.id
						pengajuan_.save()
						print pengajuan_.perusahaan
					email_ = ""
					if p.email:
						email_ = p.email
					alamat_ = str(p.alamat_perusahaan)+", DESA "+str(p.desa)+", KEC. "+str(p.desa.kecamatan)+", "+str(p.desa.kecamatan.kabupaten)
					data = {'success': True, 'pesan': 'Perusahaan disimpan. Proses Selanjutnya.','data' : [
						{'npwp_perusahaan': p.npwp},
						{'nama_perusahaan': p.nama_perusahaan},
						{'alamat_perusahaan': alamat_ },
						{'kode_pos_perusahaan': p.kode_pos},
						{'telepon_perusahaan': p.telepon},
						{'fax_perusahaan': p.fax},
						{'email_perusahaan': email_}
						]}
					data = json.dumps(data)
					response = HttpResponse(data)
					response.set_cookie(key='id_perusahaan', value=p.id)
					response.set_cookie(key='npwp_perusahaan', value=p.npwp)
				else:
					data = perusahaan.errors.as_json()
					response = HttpResponse(data)
		else:
			data = {'Terjadi Kesalahan': [{'message': 'Data Pemohon tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Data Pemohon tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def siup_detilsiup_save_cookie(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			pengajuan_ = DetilSIUP.objects.get(id=request.COOKIES['id_pengajuan'])
			detilSIUP = PengajuanSiupForm(request.POST, instance=pengajuan_)
			# kekayaan = unicode(request.POST.get('kekayaan_bersih', Decimal(0.00)).replace(".", ""))
			kekayaan_ = request.POST.get('kekayaan_bersih')
			print kekayaan_
			if kekayaan_ == '':
				# kekayaan = Decimal(0.00)
				kekayaan_ = '0' 
			# else:
				# kekayaan = kekayaan_.replace(".", "")
			total_saham = request.POST.get('total_nilai_saham')
			print total_saham
			if total_saham == '':
				# total_saham = Decimal(0.00)
				total_saham = '0'
			# else:
				# total_saham = tos.replace(".", "")
			if detilSIUP.is_valid():
				# print request.COOKIES['id_perusahaan']
				try:
					pengajuan_.kekayaan_bersih = kekayaan_
					pengajuan_.total_nilai_saham = total_saham
					# detilSIUP.save()
					kbli_list = request.POST.getlist('kbli')
					data_kelembagaan = []
					data_kelembagaan = request.POST.getlist('kelembagaan')
					# produk_utama_list = request.POST.getlist('produk_utama')
					pengajuan_.perusahaan_id = request.COOKIES['id_perusahaan']
					# pengajuan_.presentase_saham_nasional = request.POST.get('presentase_saham_nasional', Decimal('0.00'))
					# pengajuan_.presentase_saham_asing = request.POST.get('presentase_saham_asing', Decimal('0.00'))
					
					# print "kbli"+kbli_list
					# print str(produk_utama_list)
					#++++++++++++++++multi select manytomany ++++++++
					for kelembagaan in data_kelembagaan:
						kelembagaan_obj = Kelembagaan.objects.get(id=kelembagaan)
						pengajuan_.kelembagaan.add(kelembagaan_obj)

					nama_kbli = []
					# print kbli_list
					for kbli in kbli_list:
						kbli_obj = KBLI.objects.get(id=kbli)
						# print kbli_obj
						pengajuan_.kbli.add(kbli_obj)
						
						nama_kbli.append(kbli_obj.nama_kbli)			
					if len(nama_kbli) > 1:
						pengajuan_.produk_utama = ",".join(nama_kbli)
					detilSIUP.save()
					pengajuan_.save()

					# for produk_utama in produk_utama_list:
					# 	pengajuan_.produk_utama.add(ProdukUtama.objects.get(id=produk_utama))
					#++++++++++++++++ end multi select manytomany ++++++++
					# pengajuan_.bentuk_kegiatan_usaha.kegiatan_usaha print
					# detilSIUP.bentuk_kegiatan_usaha.kegiatan_usaha
					kbli_json = [k.as_json() for k in KBLI.objects.filter(id__in=kbli_list)]
					# produk_utama_json = [k.as_json() for k in ProdukUtama.objects.filter(id__in=produk_utama_list)]
					data = {'success': True, 
						'pesan': 'Detail SIUP berhasil disimpan. Proses Selanjutnya.', 
						'data': [
							{'bentuk_kegiatan_usaha': pengajuan_.bentuk_kegiatan_usaha.kegiatan_usaha},
							{'kekayaan_bersih': "Rp "+str(pengajuan_.kekayaan_bersih)},
							{'status_penanaman_modal': pengajuan_.jenis_penanaman_modal.jenis_penanaman_modal },
							{'total_nilai_saham': "Rp "+str(pengajuan_.total_nilai_saham)},
							{'presentase_saham_nasional': str(pengajuan_.presentase_saham_nasional)+" %"},
							{'presentase_saham_asing': str(pengajuan_.presentase_saham_asing)+" %"},
							# {'kelembagaan': pengajuan_.kelembagaan.kelembagaan},
							# {'produk_utama': produk_utama_json},
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
	# response.set_cookie(key='id_detail_siup', value=pengajuan_.id)
	return response

def siup_legalitas_perusahaan_save_cookie(request):
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			if 'id_pengajuan' in request.COOKIES.keys():
				if request.COOKIES['id_pengajuan'] != '':
					k = KelompokJenisIzin.objects.filter(id=request.COOKIES['id_kelompok_izin']).last()
					if k.kode == "TDP-CV" or k.kode == "TDP-FIRMA" or k.kode == "TDP-BUL":
						objects_ = getattr(app_models, 'DetilTDP')
					elif k.kode == "IPPT-Usaha":
						objects_ = getattr(app_models, 'InformasiTanah')
					elif k.kode == 'TDUP':
						objects_ = getattr(app_models, 'DetilTDUP')
					else:
						objects_ = getattr(app_models, 'DetilSIUP')	
					# print objects_
					try:
						pengajuan_ = objects_.objects.get(id=request.COOKIES['id_pengajuan'])
						# print pengajuan_
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
								f.created_at = datetime.datetime.now()
								f.perusahaan_id = request.COOKIES['id_perusahaan']
								f.jenis_legalitas_id = 1
								if request.user.is_authenticated():
									f.created_by_id = request.user.id
								else:
									f.created_by_id = pengajuan_.pemohon.id
								f.save()
								pengajuan_.legalitas.add(f)
								if request.POST.get('onoffswitch') != 'on':
									data = {'success': True, 'pesan': 'Legalitas Perusahaan berhasil disimpan. Proses Selanjutnya.', 'data': [
										{'jenis_legalitas': f.jenis_legalitas.jenis_legalitas},
										{'nama_notaris': f.nama_notaris},
										{'alamat_notaris': f.alamat},
										{'telephone_notaris': f.telephone},
										{'nomor_pengesahan': f.nomor_pengesahan},
										{'tanggal_pengesahan': str(f.tanggal_pengesahan)}
										]}
									data = json.dumps(data)
									response = HttpResponse(data)
									response.set_cookie(key='id_legalitas', value=f.id)

								if request.POST.get('onoffswitch') == 'on':
									# formperubahan = LegalitasPerusahaanPerubahanForm(request.POST)
									# if request.COOKIES['id_legalitas_perubahan'] == "":
									# 	formperubahan = LegalitasPerusahaanPerubahanForm(request.POST)
									# else:
									# 	try:
									# 		lp = Legalitas.objects.get(id=request.COOKIES['id_legalitas_perubahan'])
									# 		formperubahan = LegalitasPerusahaanPerubahanForm(request.POST, instance=lp)
									# 	except ObjectDoesNotExist:
									# 		formperubahan = LegalitasPerusahaanPerubahanForm(request.POST)
									
									# if formperubahan.is_valid():
									try:
										legalitas = Legalitas.objects.get(id=request.COOKIES.get('id_legalitas_perubahan'))
										legalitas.perusahaan_id=request.COOKIES.get('id_perusahaan', None)
										legalitas.nama_notaris = request.POST.get('nama_notaris_perubahan')
										legalitas.alamat = request.POST.get('alamat_notaris_perubahan')
										legalitas.nomor_akta = request.POST.get('nomor_akta_perubahan')
										legalitas.tanggal_akta = datetime.datetime.strptime(request.POST.get('tanggal_akta_perubahan'), '%d-%m-%Y').strftime('%Y-%m-%d')
										legalitas.telephone = request.POST.get('telephone_notaris_perubahan')
										legalitas.nomor_pengesahan = request.POST.get('nomor_pengesahan_perubahan')
									except ObjectDoesNotExist:
										legalitas = Legalitas(
											perusahaan_id=request.COOKIES.get('id_perusahaan', None),
											jenis_legalitas_id = 2,
											nama_notaris = request.POST.get('nama_notaris_perubahan'),
											alamat = request.POST.get('alamat_notaris_perubahan'),
											nomor_akta = request.POST.get('nomor_akta_perubahan'),
											tanggal_akta = datetime.datetime.strptime(request.POST.get('tanggal_akta_perubahan'), '%d-%m-%Y').strftime('%Y-%m-%d'),
											telephone = request.POST.get('telephone_notaris_perubahan'),
											nomor_pengesahan = request.POST.get('nomor_pengesahan_perubahan')
											)
									if request.POST.get('tanggal_pengesahan_perubahan', None) is not None:
										legalitas.tanggal_pengesahan = datetime.datetime.strptime(request.POST.get('tanggal_pengesahan_perubahan'), '%d-%m-%Y').strftime('%Y-%m-%d')
									if request.user.is_authenticated():
										legalitas.created_by_id = request.user.id
									else:
										legalitas.created_by_id = pengajuan_.pemohon.id
									legalitas.save()
									print legalitas.id
									# legalitas, created = Legalitas.objects.get_or_create(id=request.COOKIES.get('id_legalitas_perubahan', None), perusahaan_id=request.COOKIES.get('id_perusahaan', None), created_at=datetime.datetime.now())
									# legalitas.perusahaan_id = request.COOKIES['id_perusahaan']
									# legalitas.jenis_legalitas_id = 2
									# legalitas.nama_notaris = request.POST.get('nama_notaris_perubahan')
									# legalitas.alamat = request.POST.get('alamat_notaris_perubahan')
									# legalitas.nomor_akta = request.POST.get('nomor_akta_perubahan')
									# legalitas.tanggal_akta = datetime.datetime.strptime(request.POST.get('tanggal_akta_perubahan'), '%d-%m-%Y').strftime('%Y-%m-%d')
									# legalitas.telephone = request.POST.get('telephone_notaris_perubahan')
									# legalitas.nomor_pengesahan = request.POST.get('nomor_pengesahan_perubahan')
									
									# if request.user.is_authenticated():
									# 	legalitas.created_by_id = request.user.id
									# else:
									# 	legalitas.created_by_id = pengajuan_.pemohon.id
									# # legalitas.created_at = datetime.datetime.now()
									# legalitas.save()
									pengajuan_.legalitas.add(legalitas)
									data = {'success': True, 'pesan': 'Legalitas Perusahaan berhasil disimpan. Proses Selanjutnya.', 'data': [
										# # legalitas perubahaan
										{'jenis_legalitas_perubahan': legalitas.jenis_legalitas.jenis_legalitas},
										{'nama_notaris_perubahan': legalitas.nama_notaris},
										{'alamat_notaris_perubahan': legalitas.alamat},
										{'telephone_notaris_perubahan': legalitas.telephone},
										{'nomor_pengesahan_perubahan': legalitas.nomor_pengesahan},
										{'tanggal_pengesahan_perubahan': str(legalitas.tanggal_pengesahan)}
										]}
									data = json.dumps(data)
									response = HttpResponse(data)
									response.set_cookie(key='id_legalitas_perubahan', value=legalitas.id)
									response.set_cookie(key='id_legalitas', value=f.id)

							else:
								data = form.errors.as_json()
								response = HttpResponse(data)
						else:
							pengajuan_.jenis_pengajuan = 1
							pengajuan_.save()
							data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': []}
							data = json.dumps(data)
							response = HttpResponse(data)
					except ObjectDoesNotExist:
						data = {'Terjadi Kesalahan': [{'message': 'Data Pengajuan tidak ditemukan/data kosong'}]}
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

def siup_upload_dokumen_cookie(request):
	data = {'success': True, 'pesan': 'Proses Selanjutnya.', 'data': [] }
	return HttpResponse(json.dumps(data))

def siup_upload_berkas_foto_pemohon(request):
	if 'id_pemohon' in request.COOKIES.keys():
		if request.COOKIES['id_pemohon'] != '':
			form = UploadBerkasFotoForm(request.POST, request.FILES)
			berkas_ = request.FILES.get('berkas')
			# untuk membatas i maximal file size 2 artinya 2mb
			# print berkas_._size
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
									berkas = form.save(commit=False)
									# update model yang lain.
									pengajuan_obj = PengajuanIzin.objects.get(id=request.COOKIES.get('id_pengajuan'))
									# p = Pemohon.objects.get(id=request.COOKIES['id_pemohon'])
									if pengajuan_obj.pemohon:
										berkas.nama_berkas = "Foto Pemohon "+pengajuan_obj.pemohon.nama_lengkap
										berkas.keterangan = "foto"
										if request.user.is_authenticated():
											berkas.created_by_id = request.user.id
										else:
											berkas.created_by_id = request.COOKIES['id_pemohon']
										berkas.save()
										# save many to many table
										pengajuan_obj.pemohon.berkas_foto.add(berkas)
										pengajuan_obj.berkas_terkait_izin.add(berkas)
										pengajuan_obj.save()
										data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
												{'status_upload': 'ok'},
											]}
									else:
										data = {'Terjadi Kesalahan': [{'message': 'Pemohon tidak ada dalam daftar.'}]}
								except ObjectDoesNotExist:
									data = {'Terjadi Kesalahan': [{'message': 'Pemohon tidak ada dalam daftar.'}]}
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
			data = {'Terjadi Kesalahan': [{'message': 'Upload Berkas Foto tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload Berkas Foto tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def siup_upload_berkas_ktp_pemohon(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES.get('id_pengajuan', None) is not None:
			# ktp_ = NomorIdentitasPengguna.objects.get(nomor=request.COOKIES['nomor_ktp'])
			form = UploadBerkasKTPForm(request.POST, request.FILES)
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
									pengajuan_obj = PengajuanIzin.objects.get(id=request.COOKIES.get('id_pengajuan'))
									if pengajuan_obj.pemohon:
										berkas = form.save(commit=False)
										berkas.nama_berkas = "Berkas KTP Pemohon "+pengajuan_obj.pemohon.get_ktp()
										berkas.keterangan = "ktp"
										if request.user.is_authenticated():
											berkas.created_by_id = request.user.id
										else:
											berkas.created_by_id = request.COOKIES['id_pemohon']
										berkas.save()
										# update model yang lain.
										# p = Perushaan.object.get(id=request.COOKIES['id_perusahaan'])
										pengajuan_obj.pemohon.get_obj_ktp().berkas_id = berkas.id
										pengajuan_obj.pemohon.get_obj_ktp().save()
										pengajuan_obj.berkas_terkait_izin.add(berkas)

										data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
												{'status_upload': 'ok'},
											]}
									else:
										data = {'Terjadi Kesalahan': [{'message': 'Pemohon tidak ditemukan.'}]}
								except ObjectDoesNotExist:
									data = {'Terjadi Kesalahan': [{'message': 'Pengajuan tidak ditemukan.'}]}
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
			data = {'Terjadi Kesalahan': [{'message': 'Upload KTP/Paspor tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload KTP/Paspor tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def siup_upload_berkas_npwp_pribadi(request):
	if 'id_pemohon' in request.COOKIES.keys():
		if request.COOKIES['id_pemohon'] != '':
			form = UploadBerkasNPWPPribadiForm(request.POST, request.FILES)
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
									berkas = form.save(commit=False)
									kode = request.POST.get('kode')
									if kode == 'NPWP PRIBADI TDP':
										pengajuan_obj = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
									else:
										pengajuan_obj = DetilSIUP.objects.get(id=request.COOKIES['id_pengajuan'])
									if pengajuan_obj.pemohon:
										# p = Pemohon.objects.get(id=request.COOKIES['id_pemohon'])
										berkas.nama_berkas = "NPWP Pribadi "+pengajuan_obj.pemohon.nama_lengkap
										berkas.keterangan = "npwp pribadi"
										if request.user.is_authenticated():
											berkas.created_by_id = request.user.id
										else:
											berkas.created_by_id = request.COOKIES['id_pemohon']
										berkas.save()
										pengajuan_obj.pemohon.berkas_npwp = berkas
										pengajuan_obj.pemohon.save()
										# p.save()
										pengajuan_obj.berkas_npwp_pemohon = berkas
										pengajuan_obj.berkas_terkait_izin.add(berkas)
										pengajuan_obj.save()

										data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
												{'status_upload': 'ok'},
											]}
									else:
										data = {'Terjadi Kesalahan': [{'message': 'Pemohon tidak ada dalam daftar'}]}
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
			data = {'Terjadi Kesalahan': [{'message': 'Upload NPWP Perusahaan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload NPWP Perusahaan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

from izin.models import DetilIUA, DetilTrayek
def siup_upload_berkas_npwp_perusahaan(request):
	if 'id_perusahaan' in request.COOKIES.keys():
		if request.COOKIES['id_perusahaan'] != '':
			form = UploadBerkasNPWPPerusahaanForm(request.POST, request.FILES)
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
									# p = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
									kode = request.POST.get('kode', None)
									if kode == 'NPWP Perusahaan TDP':
										pengajuan_obj = DetilTDP.objects.get(id=request.COOKIES['id_pengajuan'])
									elif kode == 'NPWP Perusahaan TDUP':
										pengajuan_obj = DetilTDUP.objects.get(id=request.COOKIES['id_pengajuan'])
									elif kode == 'NPWP Perusahaan IUA':
										pengajuan_obj = DetilIUA.objects.get(id=request.COOKIES['id_pengajuan'])
									elif kode == 'NPWP Perusahaan TRAYEK':
										pengajuan_obj = DetilTrayek.objects.get(id=request.COOKIES['id_pengajuan'])
									else:
										pengajuan_obj = DetilSIUP.objects.get(id=request.COOKIES['id_pengajuan'])
									if pengajuan_obj.perusahaan:
										berkas = form.save(commit=False)
										berkas.nama_berkas = "NPWP Perusahaan "+pengajuan_obj.perusahaan.nama_perusahaan
										berkas.keterangan = "NPWP Perusahaan "+pengajuan_obj.perusahaan.npwp
										if request.user.is_authenticated():
											berkas.created_by_id = request.user.id
										else:
											berkas.created_by_id = request.COOKIES['id_pemohon']
										berkas.save()
										pengajuan_obj.perusahaan.berkas_npwp = berkas
										pengajuan_obj.perusahaan.save()
										pengajuan_obj.berkas_npwp_perusahaan = berkas
										pengajuan_obj.berkas_terkait_izin.add(berkas)
										pengajuan_obj.save()
										data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
											{'status_upload': 'ok'},
										]}
									else:
										data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar.'}]}
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
			data = {'Terjadi Kesalahan': [{'message': 'Upload NPWP Perusahaan tidak ditemukan/data kosong.'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload NPWP Perusahaan tidak ditemukan/tidak ada.'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response	

def siup_upload_berkas_akta_pendirian(request):
	if 'id_legalitas' in request.COOKIES.keys():
		if request.COOKIES['id_legalitas'] != '':
			form = UploadBerkasAktaPendirianForm(request.POST, request.FILES)
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
									pengajuan_obj = PengajuanIzin.objects.get(id=request.COOKIES.get('id_pengajuan'))
									try:
										perusahaan_obj = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
										if perusahaan_obj:
											berkas = form.save(commit=False)
											berkas.nama_berkas = "Berkas Akta Pendirian "+perusahaan_obj.nama_perusahaan
											berkas.keterangan = "akta pendirian "+perusahaan_obj.npwp
											if request.user.is_authenticated():
												berkas.created_by_id = request.user.id
											else:
												berkas.created_by_id = request.COOKIES['id_pemohon']
											berkas.save()
											# update model yang lain.
											try:
												p = Legalitas.objects.get(id=request.COOKIES['id_legalitas'])
												p.berkas = berkas
												p.save()
											except ObjectDoesNotExist:
												pass
											pengajuan_obj.berkas_terkait_izin.add(berkas)
											data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
												{'status_upload': 'ok'},
											]}
										else:
											data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar'}]}
									except ObjectDoesNotExist:
										data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar'}]}
								except ObjectDoesNotExist:
									data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar'}]}
								response = HttpResponse(json.dumps(data))
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
			data = {'Terjadi Kesalahan': [{'message': 'Upload Akta Pendirian tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload Akta Pendirian tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def siup_upload_berkas_akta_perubahan(request):
	if 'id_legalitas_perubahan' in request.COOKIES.keys():
		if request.COOKIES['id_legalitas_perubahan'] != '':
			form = UploadBerkasAktaPerubahanForm(request.POST, request.FILES)
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
									pengajuan_obj = PengajuanIzin.objects.get(id=request.COOKIES.get('id_pengajuan'))
									# a = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
									try:
										perusahaan_obj = Perusahaan.objects.get(id=request.COOKIES.get('id_perusahaan'))
										if pengajuan_obj and perusahaan_obj:
											berkas = form.save(commit=False)
											berkas.nama_berkas = "Berkas Akta Perubahan "+perusahaan_obj.nama_perusahaan
											berkas.keterangan = "akta perubahan "+perusahaan_obj.npwp
											if request.user.is_authenticated():
												berkas.created_by_id = request.user.id
											else:
												berkas.created_by_id = request.COOKIES['id_pemohon']
											berkas.save()
											# update model yang lain.
											try:
												p = Legalitas.objects.get(id=request.COOKIES['id_legalitas_perubahan'])
												p.berkas = berkas
												p.save()
											except ObjectDoesNotExist:
												pass

											pengajuan_obj.berkas_terkait_izin.add(berkas)
											data = {'success': True, 'pesan': 'Berkas Berhasil diupload' ,'data': [
													{'status_upload': 'ok'},
												]}
										else:
											data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar'}]}
									except ObjectDoesNotExist:
										data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar'}]}
								except ObjectDoesNotExist:
									data = {'Terjadi Kesalahan': [{'message': 'Perusahaan tidak ada dalam daftar'}]}
								response = HttpResponse(json.dumps(data))		
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
			data = {'Terjadi Kesalahan': [{'message': 'Upload Akta Perubahan tidak ditemukan/data kosong'}]}
			data = json.dumps(data)
			response = HttpResponse(data)
	else:
		data = {'Terjadi Kesalahan': [{'message': 'Upload Akta Perubahan tidak ditemukan/tidak ada'}]}
		data = json.dumps(data)
		response = HttpResponse(data)
	return response

def siup_upload_berkas_pendukung(request):
	if 'id_pengajuan' in request.COOKIES.keys():
		if request.COOKIES['id_pengajuan'] != '':
			form = UploadBerkasPendukungForm(request.POST, request.FILES)
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
									pengajuan_obj = PengajuanIzin.objects.get(id=request.COOKIES.get('id_pengajuan'))
										# perusahaan_ = Perusahaan.objects.get(id=request.COOKIES['id_perusahaan'])
									if pengajuan_obj.pemohon:
										berkas = form.save(commit=False)
										berkas.nama_berkas = "Berkas Pendukung "+pengajuan_obj.pemohon.nama_lengkap
										berkas.keterangan = "pendukung "+str(request.COOKIES.get('npwp_perusahaan', ""))
										if request.user.is_authenticated():
											berkas.created_by_id = request.user.id
										else:
											berkas.created_by_id = request.COOKIES['id_pemohon']
										berkas.save()
										pengajuan_obj.berkas_tambahan.add(berkas)
										pengajuan_obj.berkas_terkait_izin.add(berkas)

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

def siup_done(request):
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

def siup_front_done(request):
	data = {'success': True, 'pesan': 'Proses Selesai.' }
	response = HttpResponse(json.dumps(data))
	return response

def load_pemohon(request, ktp_):
	extra_context={}
	data = {'success': False, 'pesan': "Riwayat tidak ditemukan" }
	pemohon = None
	nomor_list = NomorIdentitasPengguna.objects.filter(nomor=ktp_, jenis_identitas_id=1).last()
	if nomor_list:
		pemohon_list = Pemohon.objects.filter(id=nomor_list.user.id)
		if pemohon_list.exists():
			try:
				pemohon = pemohon_list.latest("created_at")
			except Pemohon.DoesNotExist:
				pemohon = None
		if pemohon:
			paspor = ""
			jabatan_pemohon = ""
			nama_lengkap = ""
			tempat_lahir = ""
			tanggal_lahir = ""
			alamat = ""
			telephone = ""
			hp = ""
			email = ""
			kewarganegaraan = ""
			pekerjaan = ""
			paspor_ = pemohon.nomoridentitaspengguna_set.filter(jenis_identitas_id=2).last()
			if paspor_:
				paspor = paspor_.nomor
			if pemohon.jabatan_pemohon:
				jabatan_pemohon = pemohon.jabatan_pemohon
			if pemohon.nama_lengkap:
				nama_lengkap = pemohon.nama_lengkap
			if pemohon.tempat_lahir:
				tempat_lahir = pemohon.tempat_lahir
			if pemohon.tanggal_lahir:
				tanggal_lahir = pemohon.tanggal_lahir.strftime('%d-%m-%Y')				
			if pemohon.alamat:
				alamat = pemohon.alamat
			if pemohon.telephone:
				telephone = pemohon.telephone
			if pemohon.hp:
				hp = pemohon.hp
			if pemohon.email:
				email = pemohon.email
			if pemohon.kewarganegaraan:
				kewarganegaraan = pemohon.kewarganegaraan
			if pemohon.pekerjaan:
				pekerjaan = pemohon.pekerjaan
			if pemohon.desa:
				desa = pemohon.desa.id
			if pemohon.desa.kecamatan:
				kecamatan = pemohon.desa.kecamatan.id
			if pemohon.desa.kecamatan.kabupaten:
				kabupaten = pemohon.desa.kecamatan.kabupaten.id
			if pemohon.desa.kecamatan.kabupaten.provinsi:
				provinsi = pemohon.desa.kecamatan.kabupaten.provinsi.id
			if pemohon.desa.kecamatan.kabupaten.provinsi.negara:
				negara = pemohon.desa.kecamatan.kabupaten.provinsi.negara.id
			data = {'success': True, 'pesan': 'Load data berhasil.', 'data': {'jabatan_pemohon': jabatan_pemohon,'paspor': paspor, 'nama_lengkap': nama_lengkap,'tempat_lahir' : tempat_lahir,'tanggal_lahir' : tanggal_lahir, 'alamat': alamat, 'telephone': telephone, 'hp': hp, 'email': email, 'kewarganegaraan': kewarganegaraan, 'pekerjaan': pekerjaan,'desa': desa, 'kecamatan': kecamatan, 'kabupaten': kabupaten, 'provinsi': provinsi, 'negara': negara , 'keterangan_pekerjaan': pemohon.keterangan_pekerjaan}}
	else:
		data = {'success': False, 'pesan': "Riwayat tidak ditemukan" }
	return HttpResponse(json.dumps(data))

def load_perusahaan(request, npwp_):
	extra_context={}
	perusahaan = None
	perusahaan_list = Perusahaan.objects.filter(npwp=npwp_)
	if perusahaan_list.exists():
		try:
			perusahaan = perusahaan_list.latest("created_at")
		except Perusahaan.DoesNotExist:
			perusahaan = None
	if perusahaan:
		nama_perusahaan = ""
		alamat_perusahaan = ""
		desa = ""
		kecamatan = ""
		kabupaten = ""
		provinsi = ""
		negara = ""
		kode_pos = ""
		telepon = ""
		fax = ""
		email = ""
		nomor_tdp = ""

		if perusahaan.nomor_tdp:
			nomor_tdp = perusahaan.nomor_tdp
		if perusahaan.nama_perusahaan:
			nama_perusahaan = perusahaan.nama_perusahaan
		if perusahaan.alamat_perusahaan:
			alamat_perusahaan = perusahaan.alamat_perusahaan
		if perusahaan.kode_pos:
			kode_pos = perusahaan.kode_pos
		if perusahaan.telepon:
			telepon = perusahaan.telepon
		if perusahaan.fax:
			fax = perusahaan.fax
		if perusahaan.email:
			email = perusahaan.email
		if perusahaan.desa:
			desa = perusahaan.desa.id
		if perusahaan.desa.kecamatan:
			kecamatan = perusahaan.desa.kecamatan.id
		if perusahaan.desa.kecamatan.kabupaten:
			kabupaten = perusahaan.desa.kecamatan.kabupaten.id
		if perusahaan.desa.kecamatan.kabupaten.provinsi:
			provinsi = perusahaan.desa.kecamatan.kabupaten.provinsi.id
		if perusahaan.desa.kecamatan.kabupaten.provinsi.negara:
			negara = perusahaan.desa.kecamatan.kabupaten.provinsi.negara.id

		legalitas_pendirian_id = ""
		legalitas_pendirian_nama_notaris = ""
		legalitas_pendirian_alamat = ""
		legalitas_pendirian_telephone = ""
		legalitas_pendirian_no_akta = ""
		legalitas_pendirian_tanggal_akta = ""
		legalitas_pendirian_no_pengesahan = ""
		legalitas_pendirian_tanggal_pengesahan = ""
		legalitas_pendirian = perusahaan.legalitas_set.filter(jenis_legalitas_id=1).last()
		if legalitas_pendirian:
			legalitas_pendirian_id = legalitas_pendirian.id
			legalitas_pendirian_nama_notaris = legalitas_pendirian.nama_notaris
			legalitas_pendirian_alamat = legalitas_pendirian.alamat
			legalitas_pendirian_telephone = legalitas_pendirian.telephone
			legalitas_pendirian_no_akta = legalitas_pendirian.nomor_akta
			legalitas_pendirian_tanggal_akta = legalitas_pendirian.tanggal_akta.strftime('%d-%m-%Y')
			legalitas_pendirian_no_pengesahan = legalitas_pendirian.nomor_pengesahan
			if legalitas_pendirian.tanggal_pengesahan:
				legalitas_pendirian_tanggal_pengesahan = legalitas_pendirian.tanggal_pengesahan.strftime('%d-%m-%Y')
		legalitas_perubahan_id = ""
		legalitas_perubahan_nama_notaris = ""
		legalitas_perubahan_alamat = ""
		legalitas_perubahan_telephone = ""
		legalitas_perubahan_no_akta = ""
		legalitas_perubahan_tanggal_akta = ""
		legalitas_perubahan_no_pengesahan = ""
		legalitas_perubahan_tanggal_pengesahan = ""
		legalitas_perubahan = perusahaan.legalitas_set.filter(jenis_legalitas_id=2).last()
		if legalitas_perubahan:
			legalitas_perubahan_id = legalitas_perubahan.id
			legalitas_perubahan_nama_notaris = legalitas_perubahan.nama_notaris
			legalitas_perubahan_alamat = legalitas_perubahan.alamat
			legalitas_perubahan_telephone = legalitas_perubahan.telephone
			legalitas_perubahan_no_akta = legalitas_perubahan.nomor_akta
			legalitas_perubahan_tanggal_akta = legalitas_perubahan.tanggal_akta.strftime('%d-%m-%Y')
			legalitas_perubahan_no_pengesahan = legalitas_perubahan.nomor_pengesahan
			if legalitas_perubahan.tanggal_pengesahan:
				legalitas_perubahan_tanggal_pengesahan = legalitas_perubahan.tanggal_pengesahan.strftime('%d-%m-%Y')
		# Legalitas Pengesahan Menteri Hukum dan HAM
		legalitas_3 = perusahaan.legalitas_set.filter(jenis_legalitas_id=3).last()
		legalitas_3_no_pengesahan = ""
		legalitas_3_tanggal_pengesahan = ""
		if legalitas_3:
			legalitas_3_no_pengesahan = legalitas_3.nomor_pengesahan
			legalitas_3_tanggal_pengesahan = legalitas_3.tanggal_pengesahan.strftime('%d-%m-%Y')
		# Legalitas Persetujuan Menteri Hukum dan HAM Atas Perubahan Anggaran Dasar
		legalitas_4 = perusahaan.legalitas_set.filter(jenis_legalitas_id=4).last()
		legalitas_4_no_pengesahan = ""
		legalitas_4_tanggal_pengesahan = ""
		if legalitas_4:
			legalitas_4_no_pengesahan = legalitas_4.nomor_pengesahan
			legalitas_4_tanggal_pengesahan = legalitas_4.tanggal_pengesahan.strftime('%d-%m-%Y')
		# Legalitas Penerimaan Laporan Perubahan Anggaran Dasar
		legalitas_6 = perusahaan.legalitas_set.filter(jenis_legalitas_id=6).last()
		legalitas_6_no_pengesahan = ""
		legalitas_6_tanggal_pengesahan = ""
		if legalitas_6:
			legalitas_6_no_pengesahan = legalitas_6.nomor_pengesahan
			legalitas_6_tanggal_pengesahan = legalitas_6.tanggal_pengesahan.strftime('%d-%m-%Y')
		# Legalitas Penerimaan Pemberitahuan Perubahan Direksi/ Komisaris
		legalitas_7 = perusahaan.legalitas_set.filter(jenis_legalitas_id=7).last()
		legalitas_7_no_pengesahan = ""
		legalitas_7_tanggal_pengesahan = ""
		if legalitas_7:
			legalitas_7_no_pengesahan = legalitas_7.nomor_pengesahan
			legalitas_7_tanggal_pengesahan = legalitas_7.tanggal_pengesahan.strftime('%d-%m-%Y')
		legalitas_8 = perusahaan.legalitas_set.filter(jenis_legalitas_id=8).last()
		legalitas_8_no_pengesahan = ""
		legalitas_8_tanggal_pengesahan = ""
		if legalitas_8:
			legalitas_8_no_pengesahan  = legalitas_8.nomor_pengesahan
			legalitas_8_tanggal_pengesahan = legalitas_8.tanggal_pengesahan.strftime('%d-%m-%Y')
		legalitas_9 = perusahaan.legalitas_set.filter(jenis_legalitas_id=9).last()
		legalitas_9_no_pengesahan = ""
		legalitas_9_tanggal_pengesahan = ""
		if legalitas_9:
			legalitas_9_no_pengesahan = legalitas_9.nomor_pengesahan
			legalitas_9_tanggal_pengesahan = legalitas_9.tanggal_pengesahan.strftime('%d-%m-%Y')

		data = {'success': True, 'pesan': 'Load data berhasil.', 
		'data': 
		{'nomor_tdp':nomor_tdp, 'nama_perusahaan': nama_perusahaan, 'alamat_perusahaan': alamat_perusahaan, 'kode_pos': kode_pos, 'telepon': telepon, 'fax': fax, 'email': email ,'desa': desa, 'kecamatan': kecamatan, 'kabupaten': kabupaten, 'provinsi': provinsi, 'negara': negara, 'legalitas_pendirian_id': legalitas_pendirian_id, 'legalitas_pendirian_nama_notaris': legalitas_pendirian_nama_notaris, 'legalitas_pendirian_alamat': legalitas_pendirian_alamat, 'legalitas_pendirian_telephone': legalitas_pendirian_telephone, 'legalitas_pendirian_no_akta':legalitas_pendirian_no_akta, 'legalitas_pendirian_tanggal_akta': legalitas_pendirian_tanggal_akta, 'legalitas_pendirian_no_pengesahan': legalitas_pendirian_no_pengesahan, 'legalitas_pendirian_tanggal_pengesahan': legalitas_pendirian_tanggal_pengesahan, 'legalitas_perubahan_id': legalitas_perubahan_id, 'legalitas_perubahan_nama_notaris': legalitas_perubahan_nama_notaris, 'legalitas_perubahan_alamat': legalitas_perubahan_alamat, 'legalitas_perubahan_telephone': legalitas_perubahan_telephone, 'legalitas_perubahan_no_akta': legalitas_perubahan_no_akta, 'legalitas_perubahan_tanggal_akta': legalitas_perubahan_tanggal_akta, 'legalitas_perubahan_no_pengesahan':legalitas_perubahan_no_pengesahan, 'legalitas_perubahan_tanggal_pengesahan':legalitas_perubahan_tanggal_pengesahan, 'legalitas_3_no_pengesahan': legalitas_3_no_pengesahan, 'legalitas_3_tanggal_pengesahan': legalitas_3_tanggal_pengesahan, 'legalitas_4_no_pengesahan': legalitas_4_no_pengesahan, 'legalitas_4_tanggal_pengesahan': legalitas_4_tanggal_pengesahan, 'legalitas_6_no_pengesahan': legalitas_6_no_pengesahan, 'legalitas_6_tanggal_pengesahan': legalitas_6_tanggal_pengesahan, 'legalitas_7_no_pengesahan': legalitas_7_no_pengesahan, 'legalitas_7_tanggal_pengesahan': legalitas_7_tanggal_pengesahan, 'legalitas_8_no_pengesahan': legalitas_8_no_pengesahan, 'legalitas_8_tanggal_pengesahan': legalitas_8_tanggal_pengesahan, 'legalitas_9_no_pengesahan': legalitas_9_no_pengesahan, 'legalitas_9_tanggal_pengesahan': legalitas_9_tanggal_pengesahan}}
		response = HttpResponse(json.dumps(data))
		if legalitas_pendirian:
			response.set_cookie(key='id_legalitas', value=legalitas_pendirian.id)
		if legalitas_perubahan:
			response.set_cookie(key='id_legalitas_perubahan', value=legalitas_perubahan.id)
			print legalitas_perubahan.id
			print "legalitas perubahan cookie"
			print "legalitas perubahan cookie"
			print "legalitas perubahan cookie"
			print "legalitas perubahan cookie"
	else:
		response = HttpResponse(json.dumps({'success': False, 'pesan': "Data Perusahaan tidak ditemukan" }))
	return response

def ajax_load_berkas_siup(request, id_pengajuan):
	from master.models import Berkas
	url_berkas = []
	id_elemen = []
	nm_berkas =[]
	id_berkas =[]
	if id_pengajuan:
		try:
			siup = DetilSIUP.objects.get(id=id_pengajuan)
			p = siup.perusahaan
			pemohon = siup.pemohon
			berkas_ = siup.berkas_tambahan.all()
			legalitas_pendirian = p.legalitas_set.filter(jenis_legalitas_id=1).last()
			legalitas_perubahan= p.legalitas_set.filter(jenis_legalitas_id=2).last()

			foto = pemohon.berkas_foto.last()
			if foto:
				url_berkas.append(foto.berkas.url)
				id_elemen.append('foto')
				nm_berkas.append(foto.nama_berkas)
				id_berkas.append(foto.id)
				siup.berkas_terkait_izin.add(foto)

			nomor_ktp = request.COOKIES['nomor_ktp']
			if nomor_ktp:
				ktp_ = Berkas.objects.filter(nama_berkas="Berkas KTP Pemohon "+str(nomor_ktp)).last()
				if ktp_:
					url_berkas.append(ktp_.berkas.url)
					id_elemen.append('ktp')
					nm_berkas.append(ktp_.nama_berkas)
					id_berkas.append(ktp_.id)
					siup.berkas_terkait_izin.add(ktp_)

			if pemohon.berkas_npwp:
				npwp_pribadi = pemohon.berkas_npwp
			else:
				npwp_pribadi = siup.berkas_npwp_pemohon
			if npwp_pribadi:
				url_berkas.append(npwp_pribadi.berkas.url)
				id_elemen.append('npwp_pribadi')
				nm_berkas.append(npwp_pribadi.nama_berkas)
				id_berkas.append(npwp_pribadi.id)
				siup.berkas_terkait_izin.add(npwp_pribadi)

			npwp_perusahaan = p.berkas_npwp
			if npwp_perusahaan:
				url_berkas.append(npwp_perusahaan.berkas.url)
				id_elemen.append('npwp_perusahaan')
				nm_berkas.append(npwp_perusahaan.nama_berkas)
				id_berkas.append(npwp_perusahaan.id)
				siup.berkas_terkait_izin.add(npwp_perusahaan)

			# print legalitas_pendirian
			if legalitas_pendirian:
				if legalitas_pendirian.berkas:
					# print legalitas_pendirian.berkas
					url_berkas.append(legalitas_pendirian.berkas.berkas.url)
					id_elemen.append('akta_pendirian')
					nm_berkas.append(legalitas_pendirian.berkas.nama_berkas)
					id_berkas.append(legalitas_pendirian.berkas.id)
					siup.berkas_terkait_izin.add(legalitas_pendirian.berkas)

			if legalitas_perubahan:
				if legalitas_perubahan.berkas:
					# print legalitas_pendirian.berkas
					url_berkas.append(legalitas_perubahan.berkas.berkas.url)
					id_elemen.append('akta_perubahan')
					nm_berkas.append(legalitas_perubahan.berkas.nama_berkas)
					id_berkas.append(legalitas_perubahan.berkas.id)
					siup.berkas_terkait_izin.add(legalitas_perubahan.berkas)

			if berkas_:
				pendukung = berkas_.last()
				if pendukung:
					url_berkas.append(pendukung.berkas.url)
					id_elemen.append('pendukung')
					nm_berkas.append(pendukung.nama_berkas)
					id_berkas.append(pendukung.id)
					siup.berkas_terkait_izin.add(pendukung)

			data = {'success': True, 'pesan': 'Perusahaan Sudah Ada.', 'berkas': url_berkas, 'elemen':id_elemen, 'nm_berkas': nm_berkas, 'id_berkas': id_berkas }
		except ObjectDoesNotExist:
			data = {'success': False, 'pesan': '' }		
	response = HttpResponse(json.dumps(data))
	return response