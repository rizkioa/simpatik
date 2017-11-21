AKTA = (
	('Akta pendirian', 'AKTA PENDIRIAN'),
	('Akta pengesahan', 'AKTA PENGESAHAN'),
)
KEDUDUKAN = (
	('dirut/ dir cabang/penanggung jawab','Dirut/ Dir cabang/Penanggung jawab'),
	('direktur','Direktur'),
	('komisaris','Komisaris'),
)

import xlrd
from perusahaan.models import KBLI

def import_kbli():
	try:
		print "############################## START #############################"
		book = xlrd.open_workbook('files/import/KBLI_2015_New_2.xlsx')
		first_sheet = book.sheet_by_index(0)
		print "Total Baris : "+str(first_sheet.nrows-1)
		success_count = 0
		fail_count = 0
		for row in range(first_sheet.nrows):
			if(row>0) :
				kode = first_sheet.cell(row,0).value
				judul = first_sheet.cell(row,1).value
				judul = judul.strip()
				versi = first_sheet.cell(row,2).value
				versi = versi.strip()
				status_data = first_sheet.cell(row,3).value
				status_data = status_data.strip()
				keterangan = first_sheet.cell(row,4).value
				keterangan = keterangan.strip()
				print "Baris #"+str(row)+" => "+str(kode)+" : "+str(judul)

				kbli, created = KBLI.objects.get_or_create(kode_kbli=kode, nama_kbli=judul, versi=versi)
				kbli.keterangan = keterangan

				# kbli.status_data = status_data
				kbli.save()
				success_count += 1
		print "############################## START #############################"
		print "Total Data Masuk: "+str(success_count)
		print "Total Data Gagal Masuk: "+str(fail_count)
	except IOError:
		print "File tidak ditemukan."