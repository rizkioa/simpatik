from django.shortcuts import render
from master.models import Provinsi, Kabupaten, Kecamatan, Desa
from izin.models import Klasifikasi, Subklasifikasi
import csv

# Create your views here.
def import_klasifikasi():
	f1 = file('files/import/klasifikasi.csv', 'r') # Data

	c1 = csv.reader(f1) # Data 
	row = 0 
	for kl in c1:
		row += 1
		kode_ = kl[0]
		nama_ = kl[1].upper()
		print "Baris => "+str(row)

		k, created = Klasifikasi.objects.get_or_create(klasifikasi=nama_)
		k.klasifikasi = nama_
		k.save()
		print "simpan "+str(nama_)
	print row
	print "######################## DONE ########################"

def import_subklasifikasi():
	f1 = file('files/import/subklasifikasi.csv', 'r') # Data

	c1 = csv.reader(f1) # Data 
	row = 0
	un = 0
	for sb in c1:
		row += 1
		id_subklasifikasi_ = sb[0]
		if id_subklasifikasi_ != '':
			kode_ = sb[1]
			subklasifikasi_ = sb[2].upper()
			keterangan_ = sb[3]
			print "Baris => "+str(row)

			k, created = Subklasifikasi.objects.get_or_create(kode=kode_, klasifikasi_id=id_subklasifikasi_)
			k.keterangan = keterangan_
			k.subklasifikasi = subklasifikasi_
			k.save()
			print "simpan "+str(subklasifikasi_)+";  Kode : "+str(kode_)
		else:
			un += 1
	print "Total Input => "+str(row)
	print "Total ID KOSONG => "+str(un)
	print "######################## DONE ########################"

base_lokasi = 'static/import/lokasi/'
def import_provinsi():
	f1 = file(base_lokasi+'provinces.csv', 'r') # Data

	c1 = csv.reader(f1) # Data Golongan
	row = 0 
	for provinsi in c1:
		row += 1
		kode_ = provinsi[0]
		nama_ = provinsi[1].upper()
		print "Baris => "+str(row)
		# try:
		# 	p = Provinsi.objects.get(nama_provinsi=nama_, negara_id=1)
		# 	p.kode = kode_
		# 	p.save()

		# except Provinsi.DoesNotExist:
		# 	print nama_+" Tidak ada"
		p, created = Provinsi.objects.get_or_create(nama_provinsi=nama_, negara_id=1)
		p.kode = kode_
		p.save()
	print "######################## DONE ########################"

def import_kabupaten():
	f1 = file(base_lokasi+'regencies.csv', 'r') # Data

	c1 = csv.reader(f1) # Data Golongan
	row = 0 
	for reg in c1:
		row += 1
		kode_prov = reg[0][:2]
		kode_ = reg[0][2:]
		nama_ = reg[2]
		print "Baris => "+str(row)
		try:
			# print kode_prov
			# print kode_
			p = Provinsi.objects.get(kode=kode_prov)
			# try:
			# 	k = Kabupaten.objects.get(provinsi=p, nama_kabupaten=nama_)
			# 	k.kode = kode_
			# 	k.save()
			# except Kabupaten.DoesNotExist:
			# 	print "Kabupaten "+nama_+" Tidak ada"
			k, created = Kabupaten.objects.get_or_create(provinsi=p, nama_kabupaten=nama_)
			k.kode = kode_
			k.save()
		except Provinsi.DoesNotExist:
			print nama_+" Tidak ada"
	print "######################## DONE ########################"

def import_kecamatan():
	f1 = file(base_lokasi+'districts.csv', 'r')

	c1 = csv.reader(f1) # Data Golongan
	row = 0 
	for reg in c1:
		row += 1
		kode_kab = reg[1][2:]
		kode_prov = reg[1][:2]
		kode_ = reg[0][4:]
		nama_ = reg[2]
		print "Baris => "+str(row)
		print "kode prov => "+str(kode_prov)
		print "kode kab => "+str(kode_kab)
		try:
			p = Kabupaten.objects.get(kode=kode_kab, provinsi__kode=kode_prov)
			print p
			k, created = Kecamatan.objects.get_or_create(kabupaten=p, nama_kecamatan=nama_)
			k.kode = kode_
			k.save()
		except Kabupaten.DoesNotExist:
			print nama_+" Tidak ada"
	print "######################## DONE ########################"

def import_desa():
	f1 = file(base_lokasi+'villages.csv', 'r')

	c1 = csv.reader(f1) # Data Golongan
	row = 0 
	for reg in c1:
		row += 1
		kode_prov = reg[1][0:2]
		kode_kab = reg[1][2:4]
		kode_kec = reg[1][4:]
		kode_ = reg[0][7:]
		nama_ = reg[2]
		print "Baris => "+str(row)
		print "kode provinsi "+str(kode_prov)+"kode kab"+str(kode_kab)+"kode kec"+str(kode_kec)+"kode desa"+str(kode_)
		try:
			p = Kecamatan.objects.get(kode=kode_kec, kabupaten__kode=kode_kab, kabupaten__provinsi__kode=kode_prov)
			k, created = Desa.objects.get_or_create(kecamatan=p, nama_desa=nama_)
			k.kode = kode_
			k.save()
		except Kecamatan.DoesNotExist:
			print nama_+" Tidak ada"
	print "######################## DONE ########################"