def send_notification_sms(pesan, nomor_tujuan):
	import gammu
	try:
		sm = gammu.StateMachine()
		sm.ReadConfig()
		sm.Init()

		message = {
			'Text': pesan, 
			'SMSC': {'Location': 1},
			'Number': nomor_tujuan,
		}

		sm.SendSMS(message)
		return "Sukses mengirim"
	except gammu.ERR_DEVICENOTEXIST:
		return "Error opening device, it does not exist"