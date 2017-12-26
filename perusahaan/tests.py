# from django.test import TestCase
from izin.models import *
from izin.utils import get_model_detil
# Create your tests here.

def pemohon_pengajuan_izin_add_berkas_terkait():
	pengajuan_list = PengajuanIzin.objects.all()
	for p in pengajuan_list:
		berkas_foto = p.pemohon.berkas_foto.last()
		if berkas_foto is not None and berkas_foto:
			p.berkas_terkait_izin.add(berkas_foto)
			print "***************"
			print berkas_foto
			print "***************"
		berkas_npwp = p.pemohon.berkas_npwp
		if berkas_npwp is not None and berkas_npwp:
			p.berkas_terkait_izin.add(berkas_npwp)
			print "################"
			print berkas_npwp
			print "################"	

def legalitas_pengajuan_izin_add_berkas_terkait():
	pengajuan_list = PengajuanIzin.objects.all()
	for p in pengajuan_list:
		legalitas = p.legalitas.all()
		for l in legalitas:
			berkas  = l.berkas
			if berkas is not None and berkas:
				p.berkas_terkait_izin.add(berkas)
				print berkas

# problem jika detil pengajuan tidak memiliki perusahaan
# harus ada pengecekan add berkas terkit jika hanya detil pengajuan ada perusahaannya
def perusahaan_pengajuan_izin_add_berkas_terkait():
	pengajuan_list = PengajuanIzin.objects.all()
	for p in pengajuan_list:
		k = p.kelompok_jenis_izin.kode
		objects = None
		if k is not None and k:
			if k != "503.01.05/" and k != "503.01.04/":
				objects_ = get_model_detil(k)
				if objects_:
					detil_list = objects_.objects.all()
					for d in detil_list:
						if d.perusahaan:
							berkas = d.perusahaan.berkas_npwp
							if berkas is not None and berkas:
								d.berkas_terkait_izin.add(berkas)
								print berkas


def pengajuan_berkas_tambahan_add_berkas_terkait():
	pengajuan_list = PengajuanIzin.objects.all()
	for p in pengajuan_list:
		for b in p.berkas_tambahan.all():
			p.berkas_terkait_izin.add(b)
			print b