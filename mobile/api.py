# from tastypie.resources import ModelResource
from izin.models import PengajuanIzin
from cors import CORSModelResource, CORSHttpResponse
from accounts.models import Account
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.serializers import Serializer
from tastypie.authorization import Authorization
import json
from tastypie.authentication import SessionAuthentication, ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization, DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from tastypie.models import ApiKey
from kepegawaian.models import Pegawai
# import uuid

class PengajuanIzinResource(CORSModelResource):
	class Meta:
		queryset = PengajuanIzin.objects.all()
		authorization = Authorization()
		allowed_methods = ['get']

class AccountsResource(CORSModelResource):
	class Meta:
		queryset = Account.objects.all()
		allowed_methods = ['get', 'post']
		resource_name = 'akun'
		excludes = ['password', 'verified_at',]
		# authentication = SessionAuthentication()
		authentication = ApiKeyAuthentication()
		# authorization  = DjangoAuthorization()

	def prepend_urls(self):
		return [
			url(r"^account/request-user/$", self.wrap_view('request_user'), name="api_request_user"),
		]

	def obj_get(self, bundle, **kwargs):
		# print bundle.request.user

		obj = super(AccountsResource, self).obj_get(bundle, **kwargs)
		# print bundle.request
		return obj

	def request_user(self, request, **kwargs):
		self.is_authenticated(request)
		user_ = request.user
		print user_.id
		user_ = Account.objects.filter(id=user_.id).last()

		data = {'data':{'nama_lengkap':user_.nama_lengkap, 'gelar_depan': user_.gelar_depan, 'gelar_belakang': user_.gelar_belakang}}
		data = json.dumps(data)
		return CORSHttpResponse(data)


class AuthResource(CORSModelResource):
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
			print user.username
			if user.is_active:
				print user.id
				a = login(request, user)
				apikey_, created = ApiKey.objects.get_or_create(user=user)
				apikey_.user = user
				# apikey_.key = str(uuid.uuid4())
				apikey_.save()
				apikey_.key = apikey_.generate_key()
				apikey_.save()
				# print a

				# print "login"

				if apikey_.key and apikey_.user:
					return self.create_response(request, {
						'success': True,
						'apikey': apikey_.key,
						'username': apikey_.user.username
					})
				else:
					return self.create_response(request, {
						'success': False,
						'reason': 'disabled',
						}, HttpForbidden )
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