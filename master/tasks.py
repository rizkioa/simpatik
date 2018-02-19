from __future__ import absolute_import, division
from simpdu.celery import app
from master.models import NotificationSMS
import os, commands
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from celery.decorators import periodic_task


logger = get_task_logger(__name__)

@periodic_task(
	run_every=(crontab(minute='*/1/2')),
	name="task_jajal",
	ignore_result=True
)
def kirim_notifikasi_sms():
	sms_list = NotificationSMS.objects.filter(status=6).order_by('id')[:5]
	respon = "Tidak ada pesan untuk dikirim"
	if sms_list:
		for s in sms_list:
			send = os.system("gammu sendsms TEXT "+s.nomor_tujuan+" -text '"+s.pesan+"'")
			if send == 0:
				s.status = 1
				s.keterangan = "Sms telah terkirim"
				s.save()
				logger.info("SMS Notification Sukses")
				respon = "SMS berhasil terkirim"
			else:
				respon = "Terjadi Kesalahan saat mengirim pesan"
				logger.info("Terjadi Kesalahan saat mengirim pesan")
			# os.system("echo "+password+" | su -c 'python -c 'import sms; send_notification_sms("+str(sms_obj.pesan)+", "+str(sms_obj.nomor_tujuan)+")''")
			# commands.getstatusoutput("import utils; send_notification_sms("+sms_obj.pesan+", "+sms_obj.nomor_tujuan+");")
			# sms_obj.status = 1
			# sms_obj.keterangan = "Sms telah terkirim"
			# sms_obj.save()
			# logger.info("Sms Notification")
			# send_ = send_notification_sms(sms_obj.pesan, sms_obj.nomor_tujuan)
	return respon