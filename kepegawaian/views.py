import telebot
from django.conf import settings

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