JENIS_IZIN = (
	('Izin Daerah', 'IZIN DAERAH'),
	('Izin Penanaman Modal', 'IZIN PENANAMAN MODAL'),
	('Izin Pembangunan', 'IZIN PEMBANGUNAN'),
)


JENIS_PERMOHONAN = (
	('Rekomendasi', 'Rekomendasi'),
	('Berita Acara', 'Berita Acara'),
)

STATUS_HAK_TANAH = (
	('Hak Milik', 'Hak Milik'),
	('Hak Guna', 'Hak Guna'),
	('Milik', 'Milik'),
	('Yang dikuasai', 'Yang dikuasai'),
)

KEPEMILIKAN_TANAH = (
	('Sendiri', 'Sendiri'),
	('Orang Tua', 'Orang Tua'),
	('Pihak Lain', 'Pihak Lain'),
)

KLASIFIKASI_JALAN = (
	('Arteri', 'Arteri'),
	('Kolektor Primer', 'Kolektor Primer'),
	('Lokal Primer', 'Lokal Primer'),
	('Kolektor Sekunder', 'Kolektor Sekunder'),
	('Lokal Sekunder', 'Lokal Sekunder'),
	('Strategis', 'Strategis'),
)

JENIS_LOKASI_USAHA = (
	('Jalan Nasional','Jalan Nasional'),
	('Jalan Provinsi','Jalan Provinsi'),
	('Jalan Kabupaten','Jalan Kabupaten'),
	('Jalan Strategis','Jalan Strategis'),
	('Jalan Desa','Jalan Desa'),
)

JENIS_BANGUNAN = (
	('Permanen','Permanen'),
	('Semi Permanen','Semi Permanen'),
	('Darurat','Darurat'),
)

JENIS_GANGGUAN = (
	('Padat','Padat'),
	('Cair','Cair'),
	('Kebisingan','Kebisingan'),
	('Getaran','Getaran'),
)

JENIS_PENGGUNAAN = (
	('Kios','Kios'),
	('Tanah','Tanah'),
)


RUMIJA = (
	(30, 30),
	(25, 25),
	(22, 22),
	(19, 19),
	(15, 15),
	(11, 11),
)

RUWASJA = (
	(36, 36),
	(30, 30),
	(26, 26),
	(20, 20),
	(10, 10),
	(7, 7),
	(5, 5),
	(3, 3),
)

SATUAN = (
	('M','M'),
	('M&sup1;','M&sup1;'),
	('M&sup2;','M&sup2;'),
)

import datetime
from django.shortcuts import render

def get_tahun_choices(sejak):
	tahun_list = [(x, x) for x in range(sejak, (datetime.datetime.now().year+1))]
	tahun_list.reverse()
	return tahun_list

def get_nomor_pengajuan(kode_):
	now = datetime.datetime.now()
	nomor = ""
	# print now.strftime("%f")[:4]
	if kode_:
		nomor += str(kode_)
		nomor += "/"+str(now.strftime("%f")[:4])
		nomor += "/"+str(now.strftime("%m"))+str(now.strftime("%d"))
		nomor += "/"+str(now.strftime("%Y"))
	return nomor

def get_nomor_kwitansi(kode_, nomor_urut, unit_kerja):
	now = datetime.datetime.now()
	nomor = ""
	if kode_:
		nomor += str(kode_)
		nomor += "/"+str(nomor_urut)
		nomor += "/"+str(unit_kerja)
		nomor += "/"+str(now.strftime("%-m"))
		nomor += "/"+str(now.strftime("%Y"))
	return nomor

def generate_kode_bank_jatim(no_urut):
	now = datetime.datetime.now()
	nomor = ""
	panjang_ = len(str(no_urut))
	if no_urut:
		nomor = str(now.strftime("%d"))+str(now.strftime("%m"))+str(now.strftime("%Y"))
		if panjang_ == 1:
			nomor += "0000000"
		elif panjang_ == 2:
			nomor += "000000"
		elif panjang_ == 3:
			nomor += "00000"
		elif panjang_ == 4:
			nomor += "0000"
		elif panjang_ == 5:
			nomor += "000"
		elif panjang_ == 6:
			nomor += "00"
		elif panjang_ == 7:
			nomor += "0"
		nomor += str(no_urut)
	return nomor

JENIS_IUJK = (
	('IUJK Perencanaan Konstruksi', 'IUJK Perencanaan Konstruksi'),
	('IUJK Pelaksana Konstruksi', 'IUJK Pelaksana Konstruksi'),
	('IUJK Pengawasan Konstruksi', 'IUJK Pengawasan Konstruksi'),
	('IUJK Perencanaan dan Pengawasan Konstruksi', 'IUJK Perencanaan dan Pengawasan Konstruksi'),
)

JENIS_ANGGOTA_BADAN_USAHA = (
	('Direktur / Penanggung Jawab Badan Usaha', 'Direktur / Penanggung Jawab Badan Usaha'),
	('Penanggung Jawab Teknik Badan Usaha', 'Penanggung Jawab Teknik Badan Usaha'),
	('Tenaga Non Teknik', 'Tenaga Non Teknik'),
)

JENIS_MESIN_PERALATAN = (
	('Mesin', 'Mesin'),
	('Peralatan', 'Peralatan'),
)

def terbilang_(bil):
	# bil = bil.replace(".", "")
	satuan = ['','satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh','delapan', 'sembilan', 'sepuluh', 'sebelas']
	Hasil = " "
	# print bil
	n = int(bil)
	if n >= 0 and n <= 11:
		hasil = [satuan[n]]
	elif n >= 12 and n <= 19:
		hasil = terbilang_(n % 10) + ['belas']
	elif n >= 20 and n <= 99:
		hasil = terbilang_(n / 10) + ['puluh'] + terbilang_(n % 10)
	elif n >= 100 and n <= 199:
		hasil = ['seratus'] + terbilang_(n - 100)
	elif n >= 200 and n <= 999:
		hasil = terbilang_(n / 100) + ['ratus'] + terbilang_(n % 100)
	elif n >= 1000 and n <= 1999:
		hasil = ['seribu'] + terbilang_(n - 1000)
	elif n >= 2000 and n <= 999999:
		hasil = terbilang_(n / 1000) + ['ribu'] + terbilang_(n % 1000)
	elif n >= 1000000 and n <= 999999999:
		hasil = terbilang_(n / 1000000) + ['juta'] + terbilang_(n % 1000000)
	else:
		hasil = terbilang_(n / 1000000000) + ['milyar'] + terbilang_(n % 100000000)
	return hasil

def konversi(x):
	satuan = [' ', 'satu ', 'dua ', 'tiga ', 'empat ', 'lima ', 'enam ', 'tujuh ', 'delapan ', 'sembilan ', 'sepuluh ', 'sebelas ']
	hasil = ""
	x = int(x)
	# if x <= 0:
	#     hasil += 'Bilangan Haruslah Positif dan Bilangan Asli'
	if x < 12 :
		hasil += satuan[x]
	elif x < 20 :
		hasil += konversi(x-10) + "belas "
	elif x < 100:
		hasil += konversi(int(x/10)) + "puluh " + konversi(x%10)
	elif x < 200 :
		hasil += "seratus " + konversi(x-100)
	elif x < 1000 :
		hasil += konversi(int(x/100)) + "ratus " + konversi(x%100)
	elif x < 2000 :
		hasil += "seribu " + konversi(x-1000)
	elif x < 1000000 :
		hasil += konversi(int(x/1000)) + "ribu" + konversi(x%1000)
	elif x < 1000000000 :
		hasil += konversi(int(x/1000000)) + "juta " + konversi(x%1000000)
	elif x >= 1000000000 :
		hasil += konversi(int(x/1000000000)) + "milyar " + konversi(x%1000000000)
	return hasil


def terbilang(n):
	# print n
	if n == 0:
		return 'nol'
	t = terbilang_(n)
	while '' in t:
		t.remove('')
	return ' '.join(t)

if __name__ == '__main__':        
	n = [0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 19, 20, 21, 50, 99, 100, 102,
		 989, 1000, 1001, 9891, 10000, 100000, 200001, 987123, 1000000,
		 10000000, 10000000000]
		 
	for i in n:
		s = '{:,}'.format(i)
	print('{i} -> {t}'.format(i=s, t=terbilang(i)))

def formatrupiah(uang):
	i = int(uang)
	y = str(i)
	if len(y) <= 3 :
		return y     
	else :
		p = y[-3:]
		q = y[:-3]
		return   formatrupiah(q) + '.' + p


from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
def detil_pengajuan_siup_view(request, id_pengajuan_izin_, extra_context = {}):
	from izin.models import DetilSIUP
	from accounts.models import NomorIdentitasPengguna
	from izin.models import PengajuanIzin, Pemohon, Syarat, Riwayat, SKIzin
	if id_pengajuan_izin_:
		extra_context.update({'title': 'Proses Pengajuan'})
		pengajuan_ = get_object_or_404(DetilSIUP, id=id_pengajuan_izin_)
		# pengajuan_ = DetilSIUP.objects.get(id=id_pengajuan_izin_)
		if pengajuan_.pemohon:
			# if pengajuan_.pemohon.desa:
				# alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
				# extra_context.update({'alamat_pemohon': alamat_})
			extra_context.update({'pemohon': pengajuan_.pemohon})
			extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
			# nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
			# ktp_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(jenis_identitas_id=1).last()
			# paspor_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(jenis_identitas_id=2).last()
			# extra_context.update({'ktp': ktp_ })
			# extra_context.update({'paspor': paspor_ })
			# extra_context.update({'nomor_identitas': nomor_identitas_ })
			# try:
				# ktp_ = NomorIdentitasPengguna.objects.get(user_id=pengajuan_.pemohon.id, jenis_identitas__id=1)
				# extra_context.update({'cookie_file_ktp': ktp_.berkas })
			# except ObjectDoesNotExist:
				# pass
		if pengajuan_.perusahaan:
			# if pengajuan_.perusahaan.desa:
				# alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
				# extra_context.update({'alamat_perusahaan': alamat_perusahaan_ })
			extra_context.update({'perusahaan': pengajuan_.perusahaan})
			legalitas_pendirian = pengajuan_.legalitas.filter(~Q(jenis_legalitas_id=2)).last()
			legalitas_perubahan = pengajuan_.legalitas.filter(jenis_legalitas_id=2).last()
			extra_context.update({ 'legalitas_pendirian': legalitas_pendirian })
			extra_context.update({ 'legalitas_perubahan': legalitas_perubahan })

		# extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})
		
		extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
		extra_context.update({'created_at': pengajuan_.created_at})
		extra_context.update({'status': pengajuan_.status})
		extra_context.update({'pengajuan': pengajuan_})
		# encode_pengajuan_id = base64.b64encode(str(pengajuan_.id))
		# extra_context.update({'pengajuan_id': encode_pengajuan_id})
		#+++++++++++++ page logout ++++++++++
		extra_context.update({'has_permission': True })
		#+++++++++++++ end page logout ++++++++++
		banyak = len(DetilSIUP.objects.all())
		extra_context.update({'banyak': banyak})
		syarat_ = Syarat.objects.filter(jenis_izin__jenis_izin__kode="SIUP")
		extra_context.update({'syarat': syarat_})
		kekayaan_bersih = pengajuan_.kekayaan_bersih
		extra_context.update({'kekayaan_bersih': "Rp "+str(kekayaan_bersih)})
		total_nilai_saham = pengajuan_.total_nilai_saham
		extra_context.update({'total_nilai_saham': "Rp "+str(total_nilai_saham)})

		riwayat_penolakan = Riwayat.objects.filter(pengajuan_izin_id=pengajuan_.id, pengajuan_izin__status=7).last()
		extra_context.update({'riwayat_penolakan': riwayat_penolakan })

		try:
			skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
			if skizin_:
				extra_context.update({'skizin': skizin_ })
				extra_context.update({'skizin_status': skizin_.status })
		except ObjectDoesNotExist:
			pass
		try:
			riwayat_ = Riwayat.objects.filter(pengajuan_izin_id = id_pengajuan_izin_).order_by('created_at')
			if riwayat_:
				extra_context.update({'riwayat': riwayat_ })
		except ObjectDoesNotExist:
			pass
	template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_siup.html")
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))


from django.db import IntegrityError
def insert_riwayat(obj_sk_id = None, id_pengajuan_= None, user_= None, keterangan_= None):
	from izin.models import Riwayat
	if id_pengajuan_ is not None:
		riwayat_ = Riwayat(
			pengajuan_izin_id = id_pengajuan_,
			created_by_id = user_,
			keterangan = keterangan_
		)

		if obj_sk_ is not None:
			riwayat_.sk_izin_id = obj_sk_id

		try:
			riwayat_.save()
			return True
		except IntegrityError:
			return False
	else:
		return False

def send_email_notifikasi(emailto, subject, html_content):
	from django.core.mail import EmailMessage
	from django.conf import settings

	email = EmailMessage(subject, html_content, settings.DEFAULT_FROM_EMAIL, [emailto])
	email.content_subtype = "html"
	res = email.send()

	return res

def send_email(emailto, subject, objects_):
	from django.core.mail import EmailMessage
	from django.conf import settings
	from django.template import Context
	from django.template.loader import get_template

	html_content = get_template('admin/izin/email_template.html').render(Context({'obj': objects_}))
	
	email = EmailMessage(subject, html_content, settings.DEFAULT_FROM_EMAIL, [emailto])
	email.content_subtype = "html"
	res = email.send()

	return res

def send_email_html(emailto, subject, objects_, template_):
	from django.core.mail import EmailMessage
	from django.conf import settings
	from django.template import Context
	from django.template.loader import get_template

	html_content = get_template(template_).render(Context({'obj': objects_}))
	
	email = EmailMessage(subject, html_content, settings.DEFAULT_FROM_EMAIL, [emailto])
	email.content_subtype = "html"
	res = email.send()

	return res

def get_kode_izin(obj_):
	kode = ''
	if obj_.pengajuan.kelompok_jenis_izin:
		kode = obj_.pengajuan.kelompok_jenis_izin.kode
	return kode


def get_appmodels_based_kode_jenis(kode_ijin):
	from izin import models as app_models
	from izin_dinkes import models as app_models_dinkes
	objects_ = False

	if kode_ijin == "IUJK":
		objects_ = getattr(app_models, 'DetilIUJK')
	elif kode_ijin == "503.03.01/" or kode_ijin == "503.03.02/":
		objects_ = getattr(app_models, 'DetilReklame')
	elif kode_ijin == "503.02/":
		objects_ = getattr(app_models, 'DetilHO')
	elif kode_ijin == "TDUP":
		objects_ = getattr(app_models, 'DetilTDUP')
	elif kode_ijin == "503.07/" or kode_ijin == "IPPT-Rumah" or kode_ijin == "IPPT-Usaha":
		objects_ = getattr(app_models, 'InformasiTanah')
	elif kode_ijin == "503.01.06/":
		objects_ = getattr(app_models, 'DetilIMBPapanReklame')
	elif kode_ijin == "503.01.04/" or kode_ijin == "503.01.05/":
		objects_ = getattr(app_models, 'DetilIMB')
	elif kode_ijin == "HULLER":
		objects_ = getattr(app_models, 'DetilHuller')
	# elif kode_ijin == "ITO":
	# 	objects_ = getattr(app_models_dinkes, 'TokoObat')
	# elif kode_ijin == "IAP":
	# 	objects_ = getattr(app_models_dinkes, 'Apotek')
	# elif kode_ijin == "IOP":
	# 	objects_ = getattr(app_models_dinkes, 'Optikal')
	# elif kode_ijin == "ILB":
	# 	objects_ = getattr(app_models_dinkes, 'Laboratorium')
	# elif kode_ijin == "IPK":
	# 	objects_ = getattr(app_models_dinkes, 'PenutupanApotek')
	# elif kode_ijin == "IMK":
	# 	objects_ = getattr(app_models_dinkes, 'MendirikanKlinik')
	# elif kode_ijin == "IOP":
	# 	objects_ = getattr(app_models_dinkes, 'OperasionaKlinik')
	return objects_



def get_model_detil(kode):
	from izin import models as app_models
	from izin_dinkes import models as app_models_dinkes
	objects_ = None
	if kode and kode is not None:
		if kode == "503.08":
			objects_ = getattr(app_models, 'DetilSIUP')
		elif kode == "IUJK":
			objects_ = getattr(app_models, 'DetilIUJK')
		elif kode == "503.03.01/" or kode == "503.03.02/":
			objects_ = getattr(app_models, 'DetilReklame')
		elif kode == "TDP-PT" or kode == "TDP-CV" or kode == "TDP-FIRMA" or kode == "TDP-PERORANGAN" or kode == "TDP-BUL" or kode == "TDP-KOPERASI":
			objects_ = getattr(app_models, 'DetilTDP')
		elif kode == "503.01.06/":
			objects_ = getattr(app_models, 'DetilIMBPapanReklame')
		elif kode == "503.01.05/" or kode == "503.01.04/":
			objects_ = getattr(app_models, 'DetilIMB')
		elif kode == "503.06.01/":
			objects_ = getattr(app_models, 'InformasiKekayaanDaerah')
		elif kode == "503.02/":
			objects_ = getattr(app_models, 'DetilHO')
		elif kode == "503.07/" or kode == "IPPT-Rumah" or kode == "IPPT-Usaha":
			objects_ = getattr(app_models, 'InformasiTanah')
		elif kode == "HULLER":
			objects_ = getattr(app_models, 'DetilHuller')
		elif kode == "TDUP":
			objects_ = getattr(app_models, 'DetilTDUP')
		elif kode == "IUA":
			objects_ = getattr(app_models, 'DetilIUA')
		elif kode == "TRAYEK":
			objects_ = getattr(app_models, 'DetilTrayek')
		elif kode == "IZINPARKIR":
			objects_ = getattr(app_models, 'DetilIzinParkirIsidentil')
		elif kode == "503.01.04/" or kode == "503.01.05/":
			objects_ = getattr(app_models, 'DetilIMB')
		elif kode == "IAP":
			objects_ = getattr(app_models_dinkes, 'Apotek')
		elif kode == "ITO":
			objects_ = getattr(app_models_dinkes, 'TokoObat')
		elif kode == "ILB":
			objects_ = getattr(app_models_dinkes, 'Laboratorium')
		elif kode == "IOP":
			objects_ = getattr(app_models_dinkes, 'Optikal')
		elif kode == "IMK":
			objects_ = getattr(app_models_dinkes, 'MendirikanKlinik')
		elif kode == "IOK":
			objects_ = getattr(app_models_dinkes, 'OperasionalKlinik')
		elif kode == "IPA":
			objects_ = getattr(app_models_dinkes, 'PenutupanApotek')
	return objects_


import drest, json
def push_api_dishub(request, id_pengajuan):
	from izin.models import PengajuanIzin, Riwayat
	data = {'success': False, 'pesan': 'Terjadi Kesalahan, data tidak ditemukan'}
	if request.user.groups.filter(name='Kabid'):
		if id_pengajuan:
			try:
				pengajuan_obj = PengajuanIzin.objects.get(id=id_pengajuan)
				if pengajuan_obj.kelompok_jenis_izin:
					objects_ = get_model_detil(pengajuan_obj.kelompok_jenis_izin.kode)
					# print objects_
					# print pengajuan_obj
					if objects_:
						try:
							pengajuan_obj = objects_.objects.get(id=id_pengajuan)
							try:
								try:
									api = drest.api.TastyPieAPI('http://192.168.100.210:8000/api/v1/')
									api.auth('dishub', 'jgHwLBYweHsfKSZiJHfmIQ2L5KZDNh4J')
									api.request.add_header('X-CSRFToken', '{{csrf_token}}')
									api.request.add_header('Content-Type', 'application/json')
									nama_lengkap = ""
									if pengajuan_obj.pemohon:
										nama_lengkap = pengajuan_obj.pemohon.nama_lengkap
									perusahaan = ""
									if pengajuan_obj.perusahaan:
										perusahaan = pengajuan_obj.perusahaan.nama_perusahaan
									data_izin = dict(
										pemohon=nama_lengkap,
										jenis_pengajuan=2,
										id=pengajuan_obj.id,
										perusahaan=perusahaan,
										no_pengajuan=pengajuan_obj.no_pengajuan,
										tgl_pengajuan=pengajuan_obj.created_at.strftime("%Y-%m-%d")
									)
									response = api.izin.post(data_izin)
									if response.status in (200, 201, 202):
										data = {'success': True, 'pesan': 'Berhasil mengirim rekomendasi ke Dishub.'}
										riwayat_obj = Riwayat(
											pengajuan_izin_id = pengajuan_obj.id,
											created_by_id = request.user.id,
											keterangan = "Survey Pengajuan Izin"
											)
										riwayat_obj.save()
										pengajuan_obj.status = 8 # Survey
										pengajuan_obj.save()
								except drest.exc.dRestAPIError as e:
									# resp.pesan = '[E002] '+str(e.msg)
									data = {'success': False, 'pesan': str(e.msg)}
							except drest.exc.dRestRequestError as e:
								# resp.pesan = '[E001] '+str(e.msg)
								data = {'success': False, 'pesan': str(e.msg)}
						except ObjectDoesNotExist:
							pass
			except ObjectDoesNotExist:
				pass
	else:
		data = {'success': False, 'pesan': 'Terjadi Kesalahan, Anda tidak memiliki hak akses untuk memverifikasi ini.'}
	return HttpResponse(json.dumps(data))


import drest, json
def push_api_dinkes(request, id_pengajuan):
	from izin.models import PengajuanIzin, Riwayat
	data = {'success': False, 'pesan': 'Terjadi Kesalahan, data tidak ditemukan'}
	if request.user.groups.filter(name='Kabid'):
		if id_pengajuan:
			try:
				pengajuan_obj = PengajuanIzin.objects.get(id=id_pengajuan)
				if pengajuan_obj.kelompok_jenis_izin:
					objects_ = get_model_detil(pengajuan_obj.kelompok_jenis_izin.kode)
					# print objects_
					# print pengajuan_obj
					if objects_:
						try:
							pengajuan_obj = objects_.objects.get(id=id_pengajuan)
							try:
								try:
									api = drest.api.TastyPieAPI('https://180.250.255.185:8877/pengajuan-izin-list/')
									# api.auth('dishub', 'jgHwLBYweHsfKSZiJHfmIQ2L5KZDNh4J')
									api.request.add_header('Authorization', 'Token '+'9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b')
									api.request.add_header('X-CSRFToken', '{{csrf_token}}')
									api.request.add_header('Content-Type', 'application/json')
									nama_lengkap = ""
									if pengajuan_obj.pemohon:
										nama_lengkap = pengajuan_obj.pemohon.nama_lengkap
									perusahaan = ""
									if pengajuan_obj.perusahaan:
										perusahaan = pengajuan_obj.perusahaan.nama_perusahaan
									data_izin = dict(
										pemohon=nama_lengkap,
										jenis_pengajuan=2,
										id_pengajuan_simpatik=pengajuan_obj.id,
										perusahaan=perusahaan,
										no_pengajuan=pengajuan_obj.no_pengajuan,
										tgl_pengajuan=pengajuan_obj.created_at.strftime("%Y-%m-%d")
									)
									response = api.izin.post(data_izin)
									if response.status in (200, 201, 202):
										data = {'success': True, 'pesan': 'Berhasil mengirim rekomendasi ke Dinkes.'}
										riwayat_obj = Riwayat(
											pengajuan_izin_id = pengajuan_obj.id,
											created_by_id = request.user.id,
											keterangan = "Survey Pengajuan Izin"
											)
										riwayat_obj.save()
										pengajuan_obj.status = 8 # Survey
										pengajuan_obj.save()
								except drest.exc.dRestAPIError as e:
									# resp.pesan = '[E002] '+str(e.msg)
									data = {'success': False, 'pesan': str(e.msg)}
							except drest.exc.dRestRequestError as e:
								# resp.pesan = '[E001] '+str(e.msg)
								data = {'success': False, 'pesan': str(e.msg)}
						except ObjectDoesNotExist:
							pass
			except ObjectDoesNotExist:
				pass
	else:
		data = {'success': False, 'pesan': 'Terjadi Kesalahan, Anda tidak memiliki hak akses untuk memverifikasi ini.'}
	return HttpResponse(json.dumps(data))

class holder(object):
	success = False
	pesan = ''


def render_to_pdf(template_src, context_dict, extra_context, request):
	import pdfkit, datetime, os
	from django.template import RequestContext, loader
	from django.http import HttpResponse
	options = {
			'page-width': '21.1cm',
			'page-height': '33cm',
			'margin-top': '1cm',
			'margin-bottom': '1cm',
			'margin-right': '1.5cm',
			'margin-left': '1.5cm',
		}
	template = loader.get_template(template_src)
	context = RequestContext(request, extra_context)
	html = template.render(context)
	date_time = datetime.datetime.now().strftime("%Y-%B-%d %H:%M:%S")
	attachment_file_name = context_dict+'['+str(date_time)+'].pdf'
	output_file_name = 'files/media/'+str(attachment_file_name)

	pdfkit.from_string(html, output_file_name, options=options)
	pdf = open(output_file_name)

	response = HttpResponse(pdf.read(), content_type='application/pdf')
	response['Content-Disposition'] = 'filename='+str(attachment_file_name)
	pdf.close()
	os.remove(output_file_name)  # remove the locally created pdf file.
	return response


def cek_apikey(apikey, username):
	# from izin.detilsiup_admin import cek_apikey
	# from kepegawaian.models import Pegawai
	from accounts.models import Account
	respon = False
	if apikey and username:
		try:
			accounts_obj = Account.objects.get(username=username)
			if accounts_obj.api_key:
				if accounts_obj.api_key.key:
					# print accounts_obj.api_key.key
					# print apikey
					if str(accounts_obj.api_key.key) == str(apikey):
						respon = True
		except ObjectDoesNotExist:
			pass
	return respon

def pretty_date(time=False):
	"""
	Get a datetime object or a int() Epoch timestamp and return a
	pretty string like 'an hour ago', 'Yesterday', '3 months ago',
	'just now', etc
	"""
	from datetime import datetime
	now = datetime.now()
	if type(time) is int:
		diff = now - datetime.fromtimestamp(time)
	elif isinstance(time,datetime):
		diff = now - time
	elif not time:
		diff = now - now
	second_diff = diff.seconds
	day_diff = diff.days

	if day_diff < 0:
		return ''

	if day_diff == 0:
		if second_diff < 10:
			return "baru saja"
		if second_diff < 60:
			return str(second_diff) + " detik yang lalu"
		if second_diff < 120:
			return "a minute ago"
		if second_diff < 3600:
			return str(second_diff / 60) + " menit yang lalu"
		if second_diff < 7200:
			return "an hour ago"
		if second_diff < 86400:
			return str(second_diff / 3600) + " jam yang lalu"
	if day_diff == 1:
		return "kemarin"
	if day_diff < 7:
		return str(day_diff) + " hari yang lalu"
	if day_diff < 31:
		return str(day_diff / 7) + " minggu yang lalu"
	if day_diff < 365:
		return str(day_diff / 30) + " bulan yang lalu"
	return str(day_diff / 365) + " tahun yang lalu"