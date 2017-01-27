from django.shortcuts import render
import csv
import xlrd
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from models import *
from accounts.models import NomorIdentitasPengguna
from kepegawaian.models import *
# Import kepegawaian

def import_kepegawaian(unit, id_unit):
	if unit:
		if id_unit:
			try:
				print "############################## START #############################"
				book = xlrd.open_workbook('static/import/'+unit+'.xlsx')
				first_sheet = book.sheet_by_index(0)
				print "Total Baris : "+str(first_sheet.nrows)
				success_count = 0
				fail_count = 0
				for row in range(first_sheet.nrows):
					if(row>1) :
						nip = first_sheet.cell(row,0).value
						nip = nip.strip()
						nip = nip.replace(" ", "")
						print "Baris #"+str(row)+" => "+str(nip)
						if nip != "":
							# keterangan = []
							nama_lengkap = first_sheet.cell(row,1).value
							nama_lengkap = nama_lengkap.strip()

							unit_kerja = first_sheet.cell(row,4).value
							# print unit_kerja
							# print first_sheet.cell(row,6).value
							# print last_sheet.value

							jabatan = first_sheet.cell(row,6).value
							jabatan = jabatan.upper()
							if "KEPALA DINAS" in jabatan:
								jabatan_id = 1
							elif "SEKERTARIS" in jabatan:
								jabatan_id = 2
							elif "KABID" in jabatan:
								jabatan_id = 4
							elif "KASI" in jabatan:
								jabatan_id = 7
							elif "KASUBAG" in jabatan:
								jabatan_id = 3
							elif "STAF" in jabatan:
								jabatan_id = 6
							elif "KASUBID" in jabatan:
								jabatan_id = 5
							else:
								jabatan_id = None
								
							unit_kerja_id = id_unit

							print str(row)+". Proses menyimpan pegawai "+nama_lengkap+"...."
							try:
								pegawai = Pegawai.objects.get(username=nip)
								print "Pegawai NIP "+str(nip)+" ada!!!!" 
							except ObjectDoesNotExist:

								user = Pegawai (
									username = nip,
									nama_lengkap = nama_lengkap,
									jabatan_id = jabatan_id,
									unit_kerja_id = unit_kerja_id
									)
								user.save()
							try:
								nomor_identitas = NomorIdentitasPengguna.objects.get(nomor=nip)
								print "Pegawai NIP "+str(nip)+" ada!!!!"
							except ObjectDoesNotExist:
								nomor = NomorIdentitasPengguna(
									nomor = nip,
									user_id = user.id,
									jenis_identitas_id = 3
									)
								nomor.save()
							success_count += 1
						else:
							fail_count += 1
							print "Baris #"+str(row)+" NIP Kosong!!!!"
				print "############################## DONE #############################"
				print "Total Data Masuk: "+str(success_count)
				print "Total Data Gagal Masuk: "+str(fail_count)
			except IOError:
				print "File tidak ditemukan."
		else:
			print "unit kosong"
	else:
		print "error unit kosong"



