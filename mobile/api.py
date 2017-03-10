# from tastypie.resources import ModelResource
from izin.models import PengajuanIzin
from cors import CORSModelResource
from accounts.models import Account
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.serializers import Serializer

class PengajuanIzinResource(CORSModelResource):
	class Meta:
		queryset = PengajuanIzin.objects.all()
		allowed_methods = ['get']


class AccountsResource(CORSModelResource):
	class Meta:
		queryset = Account.objects.all()
		fields = ['username', 'nama_lengkap']
		allowed_methods = ['get', 'post']
		resource_name = 'user'

	# def override_urls(self):
	# 	return [
	# 		url(r"^(?P<resource_name>%s)/login%s$" %
	# 			(self._meta.resource_name, trailing_slash()),
	# 			self.wrap_view('login'), name="api_login"),
	# 		url(r'^(?P<resource_name>%s)/logout%s$' %
	# 			(self._meta.resource_name, trailing_slash()),
	# 			self.wrap_view('logout'), name='api_logout'),
	# 	]

	def prepend_urls(self):
		return [
			url(r"^user/login/$", self.wrap_view('login'), name="api_login"),
			url(r"^user/logout/$", self.wrap_view('logout'), name='api_logout'),
		]

	def login(self, request, **kwargs):
		# self.method_check(request, allowed=['post'])
		# print "askjdlkajsdk"
		# print request.GET
		# print request.POST
		# print request.POST.get('username')
		# print request.POST.get('password')


		# data = self.deserialize(request, request.raw_post_data, format=request.META.get('CONTENT_TYPE', 'application/json'))
		# data = Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'plist'])

		# print data

		username = request.POST.get('username', '')
		password = request.POST.get('password', '')

		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				print "login"
				return self.create_response(request, {
					'success': True
				})
			else:
				return self.create_response(request, {
					'success': False,
					'reason': 'disabled',
					}, HttpForbidden )
		else:
			return self.create_response(request, {
				'success': False,
				'reason': 'incorrect',
				}, HttpUnauthorized )

	def logout(self, request, **kwargs):
		self.method_check(request, allowed=['get'])
		if request.user and request.user.is_authenticated():
			logout(request)
			return self.create_response(request, { 'success': True })
		else:
			return self.create_response(request, { 'success': False }, HttpUnauthorized)