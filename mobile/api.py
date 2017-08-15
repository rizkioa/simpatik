import json
import datetime
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.conf.urls import url

from tastypie import fields
from tastypie.utils import trailing_slash
from tastypie.authentication import SessionAuthentication, ApiKeyAuthentication, BasicAuthentication
from tastypie.authorization import ReadOnlyAuthorization, DjangoAuthorization, Authorization
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.models import ApiKey
from cors import CORSModelResource, CORSHttpResponse

from izin.models import PengajuanIzin, Pemohon, KelompokJenisIzin, JenisPermohonanIzin, Riwayat, DetilSIUP, DetilTDP, SKIzin, IzinLain
from accounts.models import Account
from kepegawaian.models import Pegawai
from perusahaan.models import Perusahaan, Legalitas, DataPimpinan, PemegangSaham
from django.db.models import Q
from izin import models as app_models
from utils import get_model_detil
from izin.utils import render_to_pdf

class KelompokJenisIzinRecource(CORSModelResource):
	class Meta:
		queryset = KelompokJenisIzin.objects.all()
		# excludes = ['id','jenis_izin', 'kode', 'keterangan', 'masa_berlaku', 'standart_waktu', 'biaya', 'resource_uri']
		fields = ['id', 'kelompok_jenis_izin', 'kode']

class PemohonResource1(CORSModelResource):
	class Meta:
		queryset = Pemohon.objects.all()
		allowed_methods = ['get']
		fields = ['id', 'nama_lengkap']

class KepegawaianResource(CORSModelResource):
	class Meta:
		queryset = Pegawai.objects.all()
		fields = ['id', 'nama_lengkap']

class JenisPermohonanIzinResource(CORSModelResource):
	class Meta:
		queryset = JenisPermohonanIzin.objects.all()
		fields = ['jenis_permohonan_izin']

class PengajuanIzinResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource1, 'pemohon', full = True)
	kelompok_jenis_izin = fields.ToOneField(KelompokJenisIzinRecource, 'kelompok_jenis_izin', full = True)
	verified_by = fields.ToOneField(KepegawaianResource, 'verified_by', full=True, null=True)
	created_by = fields.ToOneField(KepegawaianResource, 'created_by', full=True, null=True)
	jenis_permohonan = fields.ToOneField(JenisPermohonanIzinResource, 'jenis_permohonan', full=True, null=True)
	class Meta:
		queryset = PengajuanIzin.objects.filter(~Q(status=11))
		# queryset = PengajuanIzin.objects.all()
		allowed_methods = ['get', 'post']
		fields = ['id', 'no_pengajuan', 'pemohon', 'kelompok_jenis_izin', 'created_at', 'created_by', 'verified_at', 'verified_by', 'jenis_permohonan', 'status']
		authentication = ApiKeyAuthentication()
		filtering = {
			'no_pengajuan': ['contains'],
			# 'status': ALL,
		}

	# untuk list filter berdasarkanuser
	def get_object_list(self, request):
		id_pengajuan_list = []
		data = super(PengajuanIzinResource, self).get_object_list(request)
		if request.user.groups.filter(name='Kadin'):
			# return object_list.filter(status=1)
			data = data.filter(status=2)
			id_list = SKIzin.objects.filter(status=4).values_list('pengajuan_izin_id', flat=True)
			id_pengajuan_list += id_list
			data = data.filter(id__in=id_pengajuan_list)
		elif request.user.groups.filter(name='Bupati'):
			# print "DISINI"
			data = data.filter(status=12)
			# print data
			id_list = SKIzin.objects.filter(status=12).values_list('pengajuan_izin_id', flat=True)
			# print id_list
			id_pengajuan_list += id_list
			data = data.filter(id__in=id_pengajuan_list)
			print data
			# print data
		data = data.order_by('-updated_at')
		return data

	def prepend_urls(self):
		return [
			url(r"^pengajuanizin/get-riwayat/$", self.wrap_view('get_riwayat_pengajuan'), name="api_get_riwayat_pengajuan"),
			url(r"^pengajuanizin/get-berkas-pengajuan/$", self.wrap_view('get_berkas_pengajuan'), name="api_get_berkas_pengajuan"),
			url(r"^pengajuanizin/get-pengajuan-izin/$", self.wrap_view('get_data_pengajuan_izin'), name="api_get_data_pengajuan_izin"),
			url(r"^pengajuanizin/get-detil-siup/$", self.wrap_view('get_detil_siup'), name="api_get_detil_siup"),
			url(r"^pengajuanizin/get-detil-tdp-pt/$", self.wrap_view('get_tdp_pt'), name="api_get_tdp_pt"),
			url(r"^pengajuanizin/get-detil-tdp-po/$", self.wrap_view('get_tdp_po'), name="api_get_tdp_po"),
			url(r"^pengajuanizin/get-pemohon/$", self.wrap_view('get_pemohon_'), name="api_get_pemohon_"),
			url(r"^pengajuanizin/get-skizin-pdf/$", self.wrap_view('get_skizin_pdf'), name="api_get_skizin_pdf"),
			# url(r"^pengajuanizin/verifikasi-pengajuan/$", self.wrap_view('api_verifikasi_pengajuan'), name="api_verifikasi_pengajuan"),
		]

	def get_skizin_pdf(self, request, **kwargs):
		import datetime
		extra_context = {}
		response = render_to_pdf("front-end/cetak_bukti_pendaftaran_baru.html", "Cetak Bukti SIUP", extra_context, request)
		return response

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
				if perusahaan_obj.berkas_npwp:
					data = perusahaan_obj.berkas_npwp.as_json()
		return data

	def get_riwayat_pengajuan(self, request, **kwargs):
		id_pengajuan = request.GET['id_pengajuan']
		data = []
		if id_pengajuan:
			riwayat_list = Riwayat.objects.filter(pengajuan_izin_id=id_pengajuan)
			data = [x.as_json() for x in riwayat_list]
		return CORSHttpResponse(json.dumps(data))

	def get_berkas_pengajuan(self, request, **kwargs):
		id_pengajuan = request.GET['id_pengajuan']
		data = {'success':False}
		if id_pengajuan:
			pengajuan_obj = PengajuanIzin.objects.filter(id=id_pengajuan).last()
			if pengajuan_obj:
				berkas_tambahan = self.get_berkas_tambahan(pengajuan_obj.id)
				berkas_legalitas = self.get_berkas_legalitas(pengajuan_obj.id)
				berkas_pemohon = {}
				if pengajuan_obj.pemohon:
					berkas_pemohon = self.get_berkas_pemohon(pengajuan_obj.pemohon.id)

				berkas_perusahaan = {}
				################# untuk mencari objects perusahaan ########
				k = pengajuan_obj.kelompok_jenis_izin
				if k.kode:
					objects_ = get_model_detil(k.kode)					
					if objects_:
						pengajuan_obj = objects_.objects.filter(id=id_pengajuan).last()
						if pengajuan_obj:
							if pengajuan_obj.perusahaan:
								berkas_perusahaan = self.get_berkas_perusahaan(pengajuan_obj.perusahaan.id)
				data = {'success':True, 'berkas_tambahan': berkas_tambahan, 'berkas_legalitas': berkas_legalitas, 'berkas_pemohon':berkas_pemohon, 'berkas_perusahaan': berkas_perusahaan}
		return CORSHttpResponse(json.dumps(data))

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
			if pemohon_list:
				data = pemohon_list.as_json()
		return data

	def get_pemohon_(self, request, **kwargs):
		data = {'success': False}
		id_pemohon = request.GET['id_pemohon']
		if id_pemohon:
			pemohon_obj = Pemohon.objects.filter(id=id_pemohon).last()
			if pemohon_obj:
				pemohon_json = self.get_pemohon(id_pemohon)
				data = {'success':True, 'pemohon_json': pemohon_json,}
		return CORSHttpResponse(json.dumps(data))

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
			legalitas_list = Legalitas.objects.filter(perusahaan_id=id_perusahaan)
			if legalitas_list:
				data = [x.as_json() for x in legalitas_list]
		return data

	def get_skizin(self, id_pengajuan):
		data = {}
		if id_pengajuan:
			skizin_obj = SKIzin.objects.filter(pengajuan_izin_id=id_pengajuan).last()
			if skizin_obj:
				data = skizin_obj.as_json()
		return data

	##################### TDP #################
	def get_data_pimpinan(self, id_pengajuan):
		data = []
		if id_pengajuan:
			data_pimpinan_list = DataPimpinan.objects.filter(detil_tdp_id=id_pengajuan)
			if data_pimpinan_list:
				data = [x.as_json() for x in data_pimpinan_list]
		return data

	def get_pemegang_saham(self, id_pengajuan):
		data = []
		if id_pengajuan:
			pemegang_saham_list = PemegangSaham.objects.filter(pengajuan_izin_id=id_pengajuan)
			if pemegang_saham_list:
				data = [x.as_json() for x in pemegang_saham_list]
		return data

	def get_izin_lain(self, id_pengajuan):
		data = []
		if id_pengajuan:
			izin_lain_list = IzinLain.objects.filter(pengajuan_izin_id=id_pengajuan)
			if izin_lain_list:
				data = [x.as_json() for x in izin_lain_list]
		return data

	def get_perusahaan_lain(self, no_tdp):
		data = []
		if no_tdp:
			perusahaan_lain_list = Perusahaan.objects.filter(nomor_tdp=no_tdp)
			if perusahaan_lain_list:
				data = [x.as_json() for x in perusahaan_lain_list]
		return data
	##################### TDP #################

	def get_detil_siup(self, request, **kwargs):
		print request.user
		id_pengajuan = request.GET['id_pengajuan']
		data = {'success':False}
		if id_pengajuan and id_pengajuan is not "":
			siup_list = DetilSIUP.objects.filter(id=id_pengajuan).last()
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

	def get_detil_tdp(self, id_pengajuan):
		data = {}
		if id_pengajuan:
			detil_tdp_obj = DetilTDP.objects.filter(id=id_pengajuan).last()
			if detil_tdp_obj:
				data = detil_tdp_obj.as_json()
		return data

	def get_tdp_pt(self, request, **kwargs):
		data = {'success':False}
		id_pengajuan = request.GET['id_pengajuan']
		if id_pengajuan and id_pengajuan is not "":
			tdp_pt_obj = DetilTDP.objects.get(id=id_pengajuan)
			detil_tdp_obj = {}
			pengajuan_obj = {}
			skizin_obj = {}
			if tdp_pt_obj:
				skizin_obj = self.get_skizin(tdp_pt_obj.id)
				pengajuan_obj = self.get_pengajuan_izin(tdp_pt_obj.id)
				detil_tdp_obj = self.get_detil_tdp(tdp_pt_obj.id)
				pemohon_obj = {}
				if tdp_pt_obj.pemohon:
					pemohon_obj = self.get_pemohon(tdp_pt_obj.pemohon.id)
				perusahaan_obj = {}
				legalitas_list = {}
				if tdp_pt_obj.perusahaan:
					perusahaan_obj = self.get_perusahaan(tdp_pt_obj.perusahaan.id)
					legalitas_list = self.get_legalitas(tdp_pt_obj.perusahaan.id)
				data = {'success':True, 'pemohon': pemohon_obj, 'perusahaan':perusahaan_obj, 'legalitas': legalitas_list, 'pengajuan_obj':pengajuan_obj, 'skizin_obj':skizin_obj, 'detil_tdp_obj':detil_tdp_obj}
				return CORSHttpResponse(json.dumps(data))


	def get_tdp_po(self, request, **kwargs):
		data = {'success':False}
		id_pengajuan = request.GET['id_pengajuan']
		if id_pengajuan and id_pengajuan is not "":
			tdp_po_list = DetilTDP.objects.get(id=id_pengajuan)
			detil_tdp_po = {}
			if tdp_po_list:
				pemohon_obj = {}
				if tdp_po_list.pemohon:
					pemohon_obj = self.get_pemohon(tdp_po_list.pemohon.id)
				perusahaan_obj = {}
				legalitas_list = {}
				if tdp_po_list.perusahaan:
					perusahaan_obj = self.get_perusahaan(tdp_po_list.perusahaan.id)
					legalitas_list = self.get_legalitas(tdp_po_list.perusahaan.id)
				data = {'success':True, 'pemohon': pemohon_obj, 'perusahaan':perusahaan_obj, 'legalitas': legalitas_list}
				return CORSHttpResponse(json.dumps(data))

class AccountsResource(CORSModelResource):
	class Meta:
		queryset = Account.objects.all()
		authentication = ApiKeyAuthentication()
		allowed_methods = ['get', 'post']
		resource_name = 'akun'
		# excludes = ['password', 'verified_at',]
		fields = ['nama_lengkap']
		
	def prepend_urls(self):
		return [
			url(r"^account/request-user/$", self.wrap_view('request_user'), name="api_request_user"),
			url(r"^account/request-menu/$", self.wrap_view('get_request_menu'), name="api_get_request_menu"),
			url(r"^pengajuanizin/verifikasi-pengajuan/$", self.wrap_view('api_verifikasi_pengajuan'), name="api_verifikasi_pengajuan"),
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
		groups = []
		if user_.is_superuser:
			jabatan = 'Superuser'
		else:
			pegawai_obj = Pegawai.objects.filter(id=user_.id).last()
			if pegawai_obj:
				if pegawai_obj.jabatan:
					jabatan = pegawai_obj.jabatan.nama_jabatan
				groups = pegawai_obj.groups.all().values('name')

		data = {'data':{'nama_lengkap':user_.nama_lengkap, 'gelar_depan': user_.gelar_depan, 'gelar_belakang': user_.gelar_belakang, 'foto': user_.get_foto(), 'jabatan':jabatan, 'groups':list(groups), 'get_full_name': user_.get_full_name()}}
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

	def api_verifikasi_pengajuan(self, request, **kwargs):
		self.is_authenticated(request)
		# print request.user
		data = {'success':False, 'pesan': 'Terjadi kesalahan, Data tidak ditemukan.'}
		id_pengajuan = request.GET['id_pengajuan']
		if id_pengajuan:
			try:
				pengajuan_obj = PengajuanIzin.objects.get(id=id_pengajuan)
				if pengajuan_obj:
					skizin_obj = pengajuan_obj.skizin_set.last()
					groups_list = request.user.groups.all()
					if skizin_obj:
						if groups_list.filter(name='Kadin') or request.user.is_superuser:
							if pengajuan_obj.status == 2 and skizin_obj.status == 4:
								# print request.user.get_full_name()
								skizin_obj.status = 9
								if pengajuan_obj.kelompok_jenis_izin:
									if pengajuan_obj.kelompok_jenis_izin.kode == "503.08":
										skizin_obj.status = 12 # Bupati
										pengajuan_obj.status = 12
										pengajuan_obj.save()
								skizin_obj.nama_pejabat = request.user.get_full_name()
								skizin_obj.nip_pejabat = request.user.username
								skizin_obj.jabatan_pejabat = "Kepala Dinas DPMPTSP"
								skizin_obj.keterangan = "Pembina Tk.l"
								skizin_obj.save()
								riwayat_obj = Riwayat(
									sk_izin_id = skizin_obj.id ,
									pengajuan_izin_id = pengajuan_obj.id,
									created_by_id = request.user.id,
									keterangan = "Kadin Verified (Izin)"
								)
								riwayat_obj.save()
								data = {'success':True, 'pesan': 'Berhasil, Pangajuan berhasil diverifikasi.'}
							elif pengajuan_obj.status == 2 and skizin_obj.status == 12:
								# print "Pengajuan sudah terverifikasi"
								data = {'success':False, 'pesan': 'Terjadi kesalahan, Pengajuan sudah terverifikasi.'}
						elif groups_list.filter(name='Bupati') or request.user.is_superuser:
							# print "masuk"
							if pengajuan_obj.status == 12 and skizin_obj.status == 12:
								skizin_obj.status = 9 # Verified
								skizin_obj.save()
								riwayat_obj = Riwayat(
									sk_izin_id = skizin_obj.id ,
									pengajuan_izin_id = pengajuan_obj.id,
									created_by_id = request.user.id,
									keterangan = "Bupati Verified (Izin)"
								)
								riwayat_obj.save()
								data = {'success':True, 'pesan': 'Berhasil, Pangajuan berhasil diverifikasi.'}
						else:
							data = {'success': False, 'pesan': 'Terjadi kesalahan, Anda tidak punya hak akses untuk memverifikasi.'}
			except ObjectDoesNotExist:
				pass
		return CORSHttpResponse(json.dumps(data))

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
				try:
					apikey_ = ApiKey.objects.get(user=user)
				except ObjectDoesNotExist:
					apikey_ = ApiKey(
						user = user
						)
					apikey_.save()
					apikey_.key = apikey_.generate_key()
					apikey_.save()
				# apikey_.user = user
				# apikey_.key = str(uuid.uuid4())
				# apikey_.save()
				# apikey_.key = apikey_.generate_key()
				# apikey_.save()
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