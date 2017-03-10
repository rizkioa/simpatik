from django.shortcuts import render
from django.contrib.auth import authenticate, login

def auth_login(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	if username and password:
		user = authenticate(username=username, password=password)
		login(request, user)
# Create your views here.
