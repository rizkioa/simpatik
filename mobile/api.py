import json
import datetime
from izin.models import PengajuanIzin, Pemohon, KelompokJenisIzin, JenisPermohonanIzin, Riwayat
from cors import CORSModelResource, CORSHttpResponse
from accounts.models import Account
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication, ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization, DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from tastypie.models import ApiKey
from kepegawaian.models import Pegawai
from tastypie import fields


class KelompokJenisIzinRecource(CORSModelResource):
	class Meta:
		queryset = KelompokJenisIzin.objects.all()
		# excludes = ['id','jenis_izin', 'kode', 'keterangan', 'masa_berlaku', 'standart_waktu', 'biaya', 'resource_uri']
		fields = ['kelompok_jenis_izin']

class PemohonResource(CORSModelResource):
	class Meta:
		queryset = Pemohon.objects.all()
		allowed_methods = ['get']
		fields = ['nama_lengkap']

class KepegawaianResource(CORSModelResource):
	class Meta:
		queryset = Pegawai.objects.all()
		fields = ['nama_lengkap']

class JenisPermohonanIzinResource(CORSModelResource):
	class Meta:
		queryset = JenisPermohonanIzin.objects.all()
		fields = ['jenis_permohonan_izin']

class PengajuanIzinResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True)
	kelompok_jenis_izin = fields.ToOneField(KelompokJenisIzinRecource, 'kelompok_jenis_izin', full = True)
	verified_by = fields.ToOneField(KepegawaianResource, 'verified_by', full=True, null=True)
	jenis_permohonan = fields.ToOneField(JenisPermohonanIzinResource, 'jenis_permohonan', full=True, null=True)
	class Meta:
		queryset = PengajuanIzin.objects.all()
		allowed_methods = ['get']
		fields = ['id', 'no_pengajuan', 'pemohon', 'kelompok_jenis_izin', 'created_at', 'verified_at', 'verified_by', 'jenis_permohonan']
		# authentication = ApiKeyAuthentication()
		filtering = {
			'no_pengajuan': ['contains'],
		}

	def prepend_urls(self):
		return [
			url(r"^pengajuanizin/get-riwayat/$", self.wrap_view('get_riwayat_pengajuan'), name="api_get_riwayat_pengajuan"),
		]

	def get_riwayat_pengajuan(self, request, **kwargs):
		id_pengajuan = request.GET['id_pengajuan']
		data = []
		if id_pengajuan:
			riwayat_list = Riwayat.objects.filter(pengajuan_izin_id=id_pengajuan)
			# print riwayat_list
			data = [x.as_json() for x in riwayat_list]
		return CORSHttpResponse(json.dumps(data))

	# def get_detil_pengajuan_izin(self, request, **kwargs):
	# 	id_pengajuan = request.GET['id']
	# 	pengajuan_izin = PengajuanIzin.objects.filter(id=id_pengajuan).last()
	# 	if kelompok_jenis_izin
	# 	kelompok_jenis_izin = pengajuan_izin.ke
	# 	data = {'success':True, 'data':}

class AccountsResource(CORSModelResource):
	class Meta:
		queryset = Account.objects.all()
		allowed_methods = ['get', 'post']
		resource_name = 'akun'
		# excludes = ['password', 'verified_at',]
		fields = ['nama_lengkap']
		authentication = ApiKeyAuthentication()

	def prepend_urls(self):
		return [
			url(r"^account/request-user/$", self.wrap_view('request_user'), name="api_request_user"),
			url(r"^account/request-menu/$", self.wrap_view('get_request_menu'), name="api_get_request_menu"),
		]

	def obj_get(self, bundle, **kwargs):

		obj = super(AccountsResource, self).obj_get(bundle, **kwargs)
		return obj

	def request_user(self, request, **kwargs):
		self.is_authenticated(request)
		user_ = request.user

		# user_ = Account.objects.filter(id=user_.id).last()

		data = {'data':{'nama_lengkap':user_.nama_lengkap, 'gelar_depan': user_.gelar_depan, 'gelar_belakang': user_.gelar_belakang}}
		data = json.dumps(data)
		return CORSHttpResponse(data)

	def get_request_menu(self, request, **kwargs):
		self.is_authenticated(request)
		user_ = request.user
		icon_menu = []
		nama_menu = []
		link_menu = []
		if user_.is_superuser:
			icon_menu.append("email")
			nama_menu.append("Pengajuan Izin")
			link_menu.append("pengajuan_izin.html")
		data = {'data':{'icon_menu':icon_menu, 'nama_menu':nama_menu, 'link_menu':link_menu}}
		data = json.dumps(data)
		return CORSHttpResponse(data)



class AuthResource(CORSModelResource):
	class Meta:
		queryset = Account.objects.all()
		fields = ['username', 'nama_lengkap']
		allowed_methods = ['get', 'post']
		resource_name = 'user'

	def prepend_urls(self):
		return [
			url(r"^user/login/$", self.wrap_view('login'), name="api_login"),
			url(r"^user/logout/$", self.wrap_view('logout'), name='api_logout'),
		]

	def login(self, request, **kwargs):

		username = request.POST.get('username', '')
		password = request.POST.get('password', '')

		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				a = login(request, user)
				apikey_, created = ApiKey.objects.get_or_create(user=user)
				apikey_.user = user
				# apikey_.key = str(uuid.uuid4())
				apikey_.save()
				apikey_.key = apikey_.generate_key()
				apikey_.save()
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