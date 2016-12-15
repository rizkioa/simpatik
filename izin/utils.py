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
import datetime

def get_tahun_choices(sejak):
	tahun_list = [(x, x) for x in range(sejak, (datetime.datetime.now().year+1))]
	tahun_list.reverse()
	return tahun_list

def get_nomor_pengajuan(kode_):
	now = datetime.datetime.now()
	nomor = ""
	print now.strftime("%f")[:4]
	if kode_:
		nomor += str(kode_)
		nomor += "/"+str(now.strftime("%f")[:4])
		nomor += "/"+str(now.strftime("%m"))+str(now.strftime("%d"))
		nomor += "/"+str(now.strftime("%Y"))
	return nomor

JENIS_IUJK = (
	('IUJK Pelaksana Kontruksi', 'IUJK Pelaksana Kontruksi'),
	('IUJK Perencana Kontruksi', 'IUJK Perencana Kontruksi'),
	('IUJK Pengawas Kontruksi', 'IUJK Pengawas Kontruksi'),
)

JENIS_ANGGOTA_BADAN_USAHA = (
	('Direktur / Penanggung Jawab Badan Usaha', 'Direktur / Penanggung Jawab Badan Usaha'),
	('Penanggung Jawab Teknik Badan Usaha', 'Penanggung Jawab Teknik Badan Usaha'),
	('Tenaga Non Teknik', 'Tenaga Non Teknik'),
)

def terbilang_(bil):
	# bil = nilai.replace(".", "")
	satuan = ['', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh','delapan', 'sembilan', 'sepuluh', 'sebelas']
	Hasil = " "
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


def terbilang(n):
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
def detil_pengajuan_siup_view(request, id_pengajuan_izin_, extra_context = {}):
	from izin.models import DetilSIUP
	from accounts.models import NomorIdentitasPengguna
	from izin.models import PengajuanIzin, Pemohon, Syarat, Riwayat, SKIzin
	if id_pengajuan_izin_:
		extra_context.update({'title': 'Proses Pengajuan'})
		pengajuan_ = DetilSIUP.objects.get(id=id_pengajuan_izin_)
		
		alamat_ = ""
		alamat_perusahaan_ = ""
		if pengajuan_.pemohon:
			if pengajuan_.pemohon.desa:
				alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
				extra_context.update({'alamat_pemohon': alamat_})
			extra_context.update({'pemohon': pengajuan_.pemohon})
			extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
			nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
			ktp_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(jenis_identitas_id=1).last()
			paspor_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(jenis_identitas_id=2).last()
			extra_context.update({'ktp': ktp_ })
			extra_context.update({'paspor': paspor_ })
			extra_context.update({'nomor_identitas': nomor_identitas_ })
			try:
				ktp_ = NomorIdentitasPengguna.objects.get(user_id=pengajuan_.pemohon.id, jenis_identitas__id=1)
				extra_context.update({'cookie_file_ktp': ktp_.berkas })
			except ObjectDoesNotExist:
				pass
		if pengajuan_.perusahaan:
			if pengajuan_.perusahaan.desa:
				alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
				extra_context.update({'alamat_perusahaan': alamat_perusahaan_ })
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