from __future__ import absolute_import, division
from simpdu.celery import app
from master.models import NotificationSMS
from master.utils import send_notification_sms
import os, commands
from django.conf import settings
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
	sms_obj = NotificationSMS.objects.filter(status=6).last()
	if sms_obj:
		password = settings.COMPUTER_PASSWORD
		os.system("echo "+password+" | su -c 'python -c 'import utils; send_notification_sms("+str(sms_obj.pesan)+", "+str(sms_obj.nomor_tujuan)+")''")
		# commands.getstatusoutput("import utils; send_notification_sms("+sms_obj.pesan+", "+sms_obj.nomor_tujuan+");")
		sms_obj.status = 1
		sms_obj.keterangan = "Sms telah terkirim"
		sms_obj.save()
		logger.info("Sms Notification")
		# send_ = send_notification_sms(sms_obj.pesan, sms_obj.nomor_tujuan)
		return "Send Sms Berhasil"
	return "Terjadi Kesalahan saat mengirim"