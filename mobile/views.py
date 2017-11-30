from django.shortcuts import render
from django.contrib.auth import authenticate, login
from mobile.cors import CORSHttpResponse

def auth_login(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	if username and password:
		user = authenticate(username=username, password=password)
		login(request, user)
# Create your views here.

def request_user(request):
	# user_ = request.user
	# print user_
	data = {'data':{'nama_lengkap':'Febri Ahmad Nurhidayat', }}
	data = json.dumps(data)
	return CORSHttpResponse(data)
