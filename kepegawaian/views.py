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
	