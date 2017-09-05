from master.models import ChatRoom
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

	def json_login_chat(self, request):
		login_chat_list = get_login_chat(request)
		request = [ob.as_json() for ob in login_chat_list]
		return  HttpResponse(json.dumps(request))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(ChatRoomAdmin, self).get_urls()
		my_urls = patterns('',
			# url(r'^option/$', self.option_provinsi, name='option_provinsi'),
			url(r'^login$', self.login_chat, name='login_chat')
			)
		return my_urls + urls


admin.site.register(ChatRoom, ChatRoomAdmin)