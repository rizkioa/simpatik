from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
import os
import sys
import signal
import telebot
from telebot import types
from django.conf import settings 

from kepegawaian.models import Pegawai, NotifikasiTelegram


# from daemon import runner

def telegram_bot_setting():
	API_TOKEN = settings.TELGRAM_API_TOKEN

	commands = {  # command description used in the "help" command
				  'start': 'Untuk menggunakan Bot',
				  'bantuan': 'Memberikan anda informasi tetang perintah yang tersedia',
				  'daftar': 'Mendaftarkan ID anda kedalam aplikasi SIMPATIK untuk notifikasi jika ada izin yang harus diproses',
	}


	# error handling if user isn't known yet
	# (obsolete once known users are saved to file, because all users
	#   had to use the /start command and are therefore known to the bot)
	def get_user_step(uid):
		if uid in userStep:
			return userStep[uid]
		else:
			knownUsers.append(uid)
			userStep[uid] = 0
			print "New user detected, who hasn't used \"/start\" yet"
			return 0


	# only used for console output now
	def listener(messages):
		"""
		When new messages arrive TeleBot will call this function.
		"""
		for m in messages:
			if m.content_type == 'text':
				# print the sent message to the console
				print str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text


	bot = telebot.TeleBot(API_TOKEN)
	bot.set_update_listener(listener)  # register listener

	# bantuan page
	@bot.message_handler(commands=['start'])
	def command_help(m):
		cid = m.chat.id
		help_text = "Selamat Datang, Simpatik Bot ini hanya untuk notifikasi aplikasi SIMPATIK Kab. Kediri\n"
		help_text += "Perintah yang tersedia : \n"
		for key in commands:  # generate help text out of the commands dictionary defined at the top
			help_text += "/" + key + ": "
			help_text += commands[key] + "\n"
		bot.send_message(cid, help_text)  # send the generated help page

	# bantuan page
	@bot.message_handler(commands=['bantuan'])
	def command_help(m):
		cid = m.chat.id
		help_text = "Perintah yang tersedia : \n"
		for key in commands:  # generate help text out of the commands dictionary defined at the top
			help_text += "/" + key + ": "
			help_text += commands[key] + "\n"
		bot.send_message(cid, help_text)  # send the generated help page


	@bot.message_handler(commands=['daftar'])
	def send_welcome(message):
		msg = bot.reply_to(message, """
			Selamat datang, Pendaftaran Step 1. Silahkan masukkan NIP/NIK anda
			""")
		bot.register_next_step_handler(msg, process_verify_step)

	def process_verify_step(message):
		try:
			chat_id = message.chat.id
			nip = message.text
			if not nip.isdigit():
				msg = bot.reply_to(message, 'NIP/NIK harus angka, Silahkan masukkan NIP/NIK anda')
				bot.register_next_step_handler(msg, process_verify_step)
				return
			# cek didatabase berdasarkan NIP/NIK
			try:
				p = Pegawai.objects.get(username=nip)
				obj, created = NotifikasiTelegram.objects.get_or_create(
					pegawai=p,
					chat_id=chat_id,
				)
				if created:
					text = 'Terimakasih, '
					text += str(p.get_full_name())+' \n'
					text += 'Silahkan klik tautan berikut'+' \n'
					text += "http://simpatik.kedirikab.go.id%s" % reverse('admin:verifikasi_telegram', args=(obj.uuid,) )
					text += 'untuk verifikasi'
				else:
					text = 'Pegawai '+str(p.get_full_name())+' sudah terdaftar. Silahkan hubungi admin.'
					
				bot.reply_to(message, text)
			except Pegawai.DoesNotExist:
				msg = bot.reply_to(message, 'NIP/NIK Tidak ditemukan, silahkan masukkan NIP/NIK dengan benar')
				bot.register_next_step_handler(msg, process_verify_step)
				return
		except Exception as e:
			# bot.reply_to(message, e)
			bot.reply_to(message, "Maaf! Ada kesalahan teknis, Silahkan hubungi admin")


	print "* RUNNING"

	bot.polling()

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/telegram_bot.pid'
        self.pidfile_timeout = 5

    def run(self):
		telegram_bot_setting()


class Command(BaseCommand):

	def check_pid(self, pid):        
		""" Check For the existence of a unix pid. """
		try:
			os.kill(pid, 0)
		except OSError:
			return False
		else:
			return True

	def add_arguments(self, parser):
		parser.add_argument('command', nargs='+', type=str)

	def handle(self, *args, **options):
		pidfile = "/tmp/telegram_bot.pid"
		if options['command'][0]=="start":
			pid = str(os.getpid())
			print pid

			if os.path.isfile(pidfile):
				if self.check_pid(int( file(pidfile,'r').read())):
					sys.exit()
				
			file(pidfile, 'w+').write(pid)

			try:	
				# App.run()
				telegram_bot_setting()
			finally:
				os.unlink(pidfile)
		# elif options['command'][0]=="daemon":
		# 	app = App()
		# 	daemon_runner = runner.DaemonRunner(app)
		# 	daemon_runner.do_action()
		elif options['command'][0]=="stop":
			pid = file(pidfile,'r').read()
			try:
				os.kill(int(pid), signal.SIGTERM)
			finally:
				os.unlink(pidfile)


		