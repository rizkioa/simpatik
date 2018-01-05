def send_notification_sms():
	import gammu
	try:
		sm = gammu.StateMachine()
		sm.ReadConfig()
		sm.Init()

		message = {
			'Text': "hello", 
			'SMSC': {'Location': 1},
			'Number': "085645989229",
		}

		sm.SendSMS(message)
		return "Sukses mengirim"
	except gammu.ERR_DEVICENOTEXIST:
		return "Error opening device, it does not exist"