import telebot
from django.conf import settings
import xlrd
from .models import LogTelegram, NotifikasiTelegram


API_TOKEN = settings.TELGRAM_API_TOKEN

bot = telebot.TeleBot(API_TOKEN)

def kirim_notifikasi_telegram(chat_id, pesan, proses, dibuat_oleh, keterangan=""):
	try:
		p = NotifikasiTelegram.objects.get(chat_id=chat_id)
		p = p.pegawai
	except NotifikasiTelegram.DoesNotExist:
		p = None

	obj, created = LogTelegram.objects.get_or_create(
			kepada = p,
			proses = proses,
			pesan = pesan,
			keterangan = keterangan,
			created_by = dibuat_oleh
			)

	try:
		bot.send_message(chat_id, pesan)
		print "TES"
		obj.status_terkirim = True
		obj.save()
		return True
	except Exception as e:
		print "ASEM"
		# print e
		keterangan = "Kode Error: "+str(e.result.status_code)+", "+str(e.result.reason)
		obj.keterangan = keterangan
		obj.save()
		return False

def import_pegawai(nama_file):
	base_file = 'static/import/pegawai/'
	file = file(base_file+nama_file+'.csv', 'r')
	c1 = csv.reader(f1) # Data 
	row = 0 
	for kl in c1:
		print '######### START ########'
		row += 1
		print "Baris => "+str(row)
		username = row[0]
		nama_lengkap = row[1]
		tempat_lahir = row[2]
		email = row[5]
		desa_id = row[6]
		alamat = row[7]
		
		p, created = Pegawai.objects.get_or_create(username=username)
		p.nama_lengkap = nama_lengkap
		p.email = email
		p.desa_id = desa_id
		p.alamat = alamat
		p.save()
		nomor, created = NomorIdentitasPengguna.objects.get_or_create(nomor=nip,user_id=p.id,jenis_identitas_id=1)
		print '####### END #######'

def import_pegawai_xls(nama_file, unit_kerja):
	if unit_kerja and nama_file:
		try:
			print "############################## START #############################"
			book = xlrd.open_workbook('static/import/pegawai/'+nama_file+'.xlsx')
			first_sheet = book.sheet_by_index(0)
			print "Total Baris : "+str(first_sheet.nrows-2)
			success_count = 0
			fail_count = 0
			for row in range(first_sheet.nrows):
				if(row>1) :
					nip = first_sheet.cell(row,1).value
					nip = nip.strip()
					nip = nip.replace(" ", "")
					print "Baris #"+str(row)+" => "+str(nip)
					
					if nip != "":
						keterangan = []
						nama_lengkap = first_sheet.cell(row,2).value
						nama_lengkap = nama_lengkap.strip()

						# jabatan = first_sheet.cell(row,7).value
						# jabatan = jabatan.strip()

						print str(row)+". Proses menyimpan pegawai "+nama_lengkap+"...."

						p, created = Pegawai.objects.get_or_create(username=nip)
						p.nama_lengkap = nama_lengkap
						# p.pekerjaan = jabatan
						p.unit_kerja_id = unit_kerja
						p.save()

						nomor, created = NomorIdentitasPengguna.objects.get_or_create(nomor=nip,user_id=p.id,jenis_identitas_id=1)
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
		print "nama file & unit kerja kosong"