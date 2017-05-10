import json
import datetime
from django.contrib.auth import authenticate, login, logout
from django.conf.urls import url

from tastypie import fields
from tastypie.utils import trailing_slash
from tastypie.authentication import SessionAuthentication, ApiKeyAuthentication, BasicAuthentication
from tastypie.authorization import ReadOnlyAuthorization, DjangoAuthorization, Authorization
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.models import ApiKey
from cors import CORSModelResource, CORSHttpResponse

from izin.models import PengajuanIzin, Pemohon, KelompokJenisIzin, JenisPermohonanIzin, Riwayat, DetilSIUP, DetilTDP, SKIzin
from accounts.models import Account
from kepegawaian.models import Pegawai
from perusahaan.models import Perusahaan, Legalitas
from django.db.models import Q



class KelompokJenisIzinRecource(CORSModelResource):
	class Meta:
		queryset = KelompokJenisIzin.objects.all()
		# excludes = ['id','jenis_izin', 'kode', 'keterangan', 'masa_berlaku', 'standart_waktu', 'biaya', 'resource_uri']
		fields = ['kelompok_jenis_izin', 'kode']

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
	created_by = fields.ToOneField(KepegawaianResource, 'created_by', full=True, null=True)
	jenis_permohonan = fields.ToOneField(JenisPermohonanIzinResource, 'jenis_permohonan', full=True, null=True)
	class Meta:
		queryset = PengajuanIzin.objects.filter(~Q(status=11))
		# queryset = PengajuanIzin.objects.all()
		allowed_methods = ['get']
		fields = ['id', 'no_pengajuan', 'pemohon', 'kelompok_jenis_izin', 'created_at', 'created_by', 'verified_at', 'verified_by', 'jenis_permohonan', 'status']
		# authentication = ApiKeyAuthentication()
		filtering = {
			'no_pengajuan': ['contains'],
			# 'status': ALL,
		}

	def prepend_urls(self):
		return [
			url(r"^pengajuanizin/get-riwayat/$", self.wrap_view('get_riwayat_pengajuan'), name="api_get_riwayat_pengajuan"),
			url(r"^pengajuanizin/get-pengajuan-izin/$", self.wrap_view('get_data_pengajuan_izin'), name="api_get_data_pengajuan_izin"),
			url(r"^pengajuanizin/get-detil-siup/$", self.wrap_view('get_detil_siup'), name="api_get_detil_siup"),
			url(r"^pengajuanizin/get-detil-tdp-po/$", self.wrap_view('get_tdp_po'), name="api_get_tdp_po"),
		]

	def get_berkas_tambahan(self, id_pengajuan):
		data = {}
		if id_pengajuan:
			pengajuan_obj = PengajuanIzin.objects.filter(id=id_pengajuan).last()
			if pengajuan_obj:
				if pengajuan_obj.berkas_tambahan:
					berkas_tambahan = pengajuan_obj.berkas_tambahan.all()
					if berkas_tambahan:
						data = [x.as_json() for x in berkas_tambahan]
		return data

	def get_berkas_legalitas(self, id_pengajuan):
		data = {}
		if id_pengajuan:
			pengajuan_obj = PengajuanIzin.objects.filter(id=id_pengajuan).last()
			if pengajuan_obj:
				if pengajuan_obj.legalitas:
					legalitas_list = pengajuan_obj.legalitas.all()
					if legalitas_list:
						data = [x.get_berkas() for x in legalitas_list]
		return data

	def get_berkas_pemohon(self, id_pemohon):
		data = {}
		if id_pemohon:
			pemohon_obj = Pemohon.objects.filter(id=id_pemohon).last()
			if pemohon_obj:
				data = pemohon_obj.get_berkas()
		return data

	def get_berkas_perusahaan(self, id_perusahaan):
		data = {}
		if id_perusahaan:
			perusahaan_obj = Perusahaan.objects.filter(id=id_perusahaan).last()
			if perusahaan_obj:
				data = perusahaan_obj.get_berkas()
		return data

	def get_riwayat_pengajuan(self, request, **kwargs):
		id_pengajuan = request.GET['id_pengajuan']
		data = []
		if id_pengajuan:
			riwayat_list = Riwayat.objects.filter(pengajuan_izin_id=id_pengajuan)
			# print riwayat_list
			data = [x.as_json() for x in riwayat_list]
		return CORSHttpResponse(json.dumps(data))


	# get detail pengajuan izin
	def get_pengajuan_izin(self, id_pengajuan):
		data = {}
		if id_pengajuan:
			pengajuan_obj = PengajuanIzin.objects.filter(id=id_pengajuan).last()
			if pengajuan_obj:
				data = pengajuan_obj.as_json()
		return data

	def get_data_pengajuan_izin(self, request, **kwargs):
		id_pengajuan = request.GET['id_pengajuan']
		data = {'success':False}
		if id_pengajuan and id_pengajuan is not "":
			pengajuan_obj = self.get_pengajuan_izin(id_pengajuan)
			data = {'success':True, 'pengajuan_obj':pengajuan_obj}
		return CORSHttpResponse(json.dumps(data))


	def get_pemohon(self, id_pemohon):
		data = {}
		if id_pemohon:
			pemohon_list = Pemohon.objects.filter(id=id_pemohon).last()
			# print pemohon_list
			if pemohon_list:
				data = pemohon_list.as_json()
		return data

	def get_perusahaan(self, id_perusahaan):
		data = {}
		if id_perusahaan:
			perusahaan_list = Perusahaan.objects.filter(id=id_perusahaan).last()
			if perusahaan_list:
				data = perusahaan_list.as_json()
		return data

	def get_legalitas(self, id_perusahaan):
		data = []
		if id_perusahaan:
			legaitas_list = Legalitas.objects.filter(perusahaan_id=id_perusahaan)
			if legaitas_list:
				data = [x.as_json() for x in legaitas_list]
		return data

	def get_skizin(self, id_pengajuan):
		data = {}
		if id_pengajuan:
			skizin_obj = SKIzin.objects.filter(pengajuan_izin_id=id_pengajuan).last()
			if skizin_obj:
				data = skizin_obj.as_json()
		return data

	def get_detil_siup(self, request, **kwargs):
		id_pengajuan = request.GET['id_pengajuan']
		data = {'success':False}
		if id_pengajuan and id_pengajuan is not "":
			siup_list = DetilSIUP.objects.filter(id=id_pengajuan).last()
			if siup_list:
				detil_siup_obj = {}
				pengajuan_obj = {}
				skizin_obj = {}
				if siup_list:
					skizin_obj = self.get_skizin(siup_list.id)
					pengajuan_obj = self.get_pengajuan_izin(siup_list.id)
					pemohon_obj = {}
					if siup_list.pemohon:
						pemohon_obj = self.get_pemohon(siup_list.pemohon.id)
					perusahaan_obj = {}
					legalitas_list = {}
					if siup_list.perusahaan:
						perusahaan_obj = self.get_perusahaan(siup_list.perusahaan.id)
						legalitas_list = self.get_legalitas(siup_list.perusahaan.id)
					
					detil_siup_obj = siup_list.as_json()
					data = {'success':True, 'pemohon': pemohon_obj, 'perusahaan':perusahaan_obj, 'legalitas': legalitas_list, 'detil_siup_obj':detil_siup_obj, 'pengajuan_obj':pengajuan_obj, 'skizin_obj':skizin_obj}
		return CORSHttpResponse(json.dumps(data))

	def get_skizin_siup(self, request, **kwargs):
		id_pengajuan = request.GET['id_pengajuan']
		data = {'success':False}
		if id_pengajuan and id_pengajuan is not "":
			pass

	def get_tdp_po(self, request, **kwargs):
		id_pengajuan = request.GET['id_pengajuan']
		data = {}
		if id_pengajuan and id_pengajuan is not "":
			tdp_po_list = DetilTDP.objects.get(id=id_pengajuan)
			detil_tdp_po = {}
			if tdp_po_list:
				pemohon_obj = {}
				if tdp_po_list.pemohon:
					pemohon_obj = self.get_pemohon(request, tdp_po_list.pemohon.id)
				perusahaan_obj = {}
				legalitas_list = {}
				if tdp_po_list.perusahaan:
					perusahaan_obj = self.get_perusahaan(request, tdp_po_list.perusahaan.id)
					legalitas_list = self.get_legalitas(request, tdp_po_list.perusahaan.id)
				data = {'success':True, 'pemohon': pemohon_obj, 'perusahaan':perusahaan_obj, 'legalitas': legalitas_list}
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
		# print "#######################"
		# print user_.get_foto()
		
		# user_ = Account.objects.filter(id=user_.id).last()
		jabatan = ''
		group = user_.groups.all()
		# print group
		# print "#######################"
		if user_.is_superuser:
			jabatan = 'Superuser'
		elif group:
			pegawai_obj = Pegawai.objects.filter(id=user_.id).last()
			if pegawai_obj:
				if pegawai_obj.jabatan:
					jabatan = pegawai_obj.jabatan.nama_jabatan

		data = {'data':{'nama_lengkap':user_.nama_lengkap, 'gelar_depan': user_.gelar_depan, 'gelar_belakang': user_.gelar_belakang, 'foto': user_.get_foto(), 'jabatan':jabatan}}
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