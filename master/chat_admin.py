from master.models import ChatRoom, Chat, ChatUserPemohon
from django.contrib import admin
from django.http import HttpResponse
import json, datetime
from django.core.exceptions import ObjectDoesNotExist

class ChatRoomAdmin(admin.ModelAdmin):
	list_login_chat = ('operator', 'no_ktp', 'nama_pemohon')
	search_login_chat = ('no_ktp')

	# def login_chat(self, request):
	# 	no_ktp = request.POST.get('nomor_ktp')
	# 	nama_pemohon = request.POST.get('nama_lengkap')
	# 	operator = request.POST.get('operator')
	# 	chatroom_list = ChatRoom.objects.filter(no_ktp=no_ktp)
	# 	if chatroom_list.exists():
	# 		chatroom_obj = chatroom_list.last()
	# 	else:
	# 		chatroom_obj = ChatRoom(
	# 			operator_id = operator,
	# 			no_ktp = no_ktp,
	# 			nama_pemohon = nama_pemohon
	# 			)
	# 		chatroom_obj.save()
	# 	data = {'success':True, 'pesan': 'Berhasil Login', 'nama_pemohon':chatroom_obj.nama_pemohon, 'nomor_ktp':chatroom_obj.no_ktp}
	# 	# data = {}
	# 	return HttpResponse(json.dumps(data))

	def login_chat(self, request):
		data = {"success": False, "pesan": "Terjadi Kesalahan"}
		no_ktp = request.POST.get('chat_nomor_ktp', '')
		nama_lengkap = request.POST.get('chat_nama_lengkap', '')
		operator = request.POST.get('chat_operator', None)
		# user_id = None
		# chat_room_id = None
		# try:
		user_list = ChatUserPemohon.objects.filter(no_ktp=no_ktp)
		if user_list.exists():
			user_obj = user_list.last()
			user_obj.nama_pemohon = nama_lengkap
		else:
			user_obj = ChatUserPemohon(
				no_ktp = no_ktp,
				nama_pemohon = nama_lengkap,
				)
		user_obj.save()

		chat_room_list = ChatRoom.objects.filter(userpemohon_id=user_obj.id)
		if chat_room_list.exists() and chat_room_list:
			chat_room_list = chat_room_list.filter(operator_id=operator)
			# print chat_room_list
			if chat_room_list.exists() and chat_room_list:
				chat_room_obj = chat_room_obj.last()
			else:
				# print "masuk add"
				chat_room_obj = ChatRoom(
					operator_id = operator,
					userpemohon_id = user_obj.id,
					created_at = datetime.datetime.now()
				)
		else:
			chat_room_obj = ChatRoom(
				operator_id = operator,
				userpemohon_id = user_obj.id,
				created_at = datetime.datetime.now()
				)
			# print "masuk"
		chat_room_obj.save()
		# nama_pemohon = request.POST.get('nama_lengkap')
		# kelompokjenisizin = request.POST.get('login_kelompokjenisizin')
		# chatroom_list = ChatRoom.objects.filter(no_ktp=no_ktp, nama_pemohon=nama_pemohon, kelompok_jenis_izin_id=kelompokjenisizin)
		# if chatroom_list.exists():
		# 	chatroom_obj = chatroom_list.last()
		# 	data = {"success": True, "pesan": "Berhasil Get", "id": chatroom_obj.id}
		# else:
		# 	chatroom_obj = ChatRoom(
		# 		no_ktp=no_ktp,
		# 		nama_pemohon=nama_pemohon,
		# 		kelompok_jenis_izin_id=kelompokjenisizin
		# 		)
		# 	chatroom_obj.save()
		if user_obj:
			data = {"success": True, "pesan": "Berhasil", "user_id": user_obj.id, "chat_room_id": chat_room_obj.id}
		return HttpResponse(json.dumps(data))


	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(ChatRoomAdmin, self).get_urls()
		my_urls = patterns('',
			# url(r'^option/$', self.option_provinsi, name='option_provinsi'),
			url(r'^login$', self.login_chat, name='login_chat')
			)
		return my_urls + urls

# def get_chat(request):
# 	chat_list = Chat.objects.all()

# 	nomor_ktp = request.POST.get('nomor_ktp', None)



class ChatAdmin(admin.ModelAdmin):
	list_chat = ('chat_room', 'isi_pesan')
	search_login_chat = ('isi_pesan')

	def chat(self, request):
		chat_room_list = ChatRoom.objects.last()
		chat_room_id = chat_room_list.id
		print chat_room_id
		isi_pesan = request.POST.get('isi_pesan')
		chat_list = Chat.objects.filter(isi_pesan=isi_pesan)
		if chat_list.exists():
			chat_obj = chat_list.last()
		else:
			chat_obj = Chat(
				chat_room_id= chat_room_id,
				isi_pesan = isi_pesan,
				)
			chat_obj.save()
		data = {'success': True, 'pesan': 'Berhasil disimpan', 'isi_pesan': chat_obj.isi_pesan}
		return HttpResponse(json.dumps(data))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(ChatAdmin, self).get_urls()
		my_urls = patterns('',
			# url(r'^option/$', self.option_provinsi, name='option_provinsi'),
			url(r'^chat$', self.chat, name='chat')
			)
		return my_urls + urls

admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Chat, ChatAdmin)