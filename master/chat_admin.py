from master.models import ChatRoom, Chat
from django.contrib import admin
from django.http import HttpResponse
import json

class ChatRoomAdmin(admin.ModelAdmin):
	list_login_chat = ('operator', 'no_ktp', 'nama_pemohon')
	search_login_chat = ('no_ktp')

	def login_chat(self, request):
		no_ktp = request.POST.get('nomor_ktp')
		nama_pemohon = request.POST.get('nama_lengkap')
		operator = request.POST.get('operator')
		chatroom_list = ChatRoom.objects.filter(no_ktp=no_ktp)
		if chatroom_list.exists():
			chatroom_obj = chatroom_list.last()
		else:
			chatroom_obj = ChatRoom(
				operator_id = operator,
				no_ktp = no_ktp,
				nama_pemohon = nama_pemohon
				)
			chatroom_obj.save()
		data = {'success':True, 'pesan': 'Berhasil Login', 'nama_pemohon':chatroom_obj.nama_pemohon, 'nomor_ktp':chatroom_obj.no_ktp}
		# data = {}
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
		return HttpResponse(json.dumps(request))

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