from mobile.cors import CORSModelResource, CORSHttpResponse
from izin.models import *
from mobile.api import KelompokJenisIzinRecource, JenisPermohonanIzinResource, KepegawaianResource
from tastypie import fields
from perusahaan.api import PerusahaanResource, KBLIResource, LegalitasResource
from master.api import BerkasResource, ParameterBangunanResource, BangunanJenisKontruksiResource, DesaResource
from tastypie.resources import ALL_WITH_RELATIONS, ALL
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from django.conf.urls import url
import json, datetime
from izin.utils import cek_apikey

class BerkasTerkalitIzin(CORSModelResource):
	berkas_terkait_izin = fields.OneToManyField(BerkasResource, 'berkas_terkait_izin', full=True, null=True, blank=True)
	class Meta:
		queryset = PengajuanIzin.objects.all()
		fields = ['id', 'berkas_terkait_izin']
		filtering = {
			'id': ALL,
		}

class SKIzinResource(CORSModelResource):
	pengajuan_izin_id = fields.IntegerField(attribute="pengajuan_izin__id", null=True, blank=True)
	masa_berlaku = fields.CharField(attribute="get_masa_berlaku_izin", null=True, blank=True)
	class Meta:
		queryset = SKIzin.objects.all()
		fields = ['id', 'status', 'pengajuan_izin_id', 'masa_berlaku', 'status_pembaharuan_ke', 'nip_pejabat', 'jabatan_pejabat', 'nama_pejabat']
		filtering = {
			'pengajuan_izin_id' : ['contains'],
			'pengajuan_izin': ALL,
		}
		authentication = ApiKeyAuthentication()


	def prepend_urls(self):
		return [
			url(r"^skizin/get-skizin/$", self.wrap_view('get_skizin_'), name="api_skizin_get_skizin"),
			]

	def get_skizin_(self, request, **kwargs):
		id_pengajuan = request.GET['id_pengajuan']
		data = {}
		if id_pengajuan:
			skizin_obj = SKIzin.objects.filter(pengajuan_izin_id=id_pengajuan).last()
			if skizin_obj:
				data = skizin_obj.as_json()
		return CORSHttpResponse(json.dumps(data))

class PemohonResource(CORSModelResource):
	ktp = fields.CharField(attribute="get_ktp", null=True, blank=True)
	paspor = fields.CharField(attribute="get_paspor", null=True, blank=True)
	lokasi_lengkap = fields.CharField(attribute="desa__lokasi_lengkap", null=True, blank=True)
	jenis_pemohon = fields.CharField(attribute="jenis_pemohon__jenis_pemohon", null=True, blank=True)
	class Meta:
		queryset = Pemohon.objects.all()
		excludes = ['is_active', 'is_admin', 'is_superuser', 'updated_at', 'username', 'verified_at', 'status', 'last_login', 'password', 'rejected_at', 'created_at']
		# allowed_methods = ['get']
		# fields = ['id', 'nama_lengkap']
		filtering = {
			'nama_lengkap': ALL,
			# 'status': ALL,
		}

class MerkTypeKendaraanResource(CORSModelResource):
	class Meta:
		queryset = MerkTypeKendaraan.objects.all()

class KendaraanResource(CORSModelResource):
	merk_kendaraan = fields.ToOneField(MerkTypeKendaraanResource, 'merk_kendaraan', full = True, null=True)
	pengajuan_izin_id = fields.IntegerField(attribute="pengajuan_izin__id", null=True, blank=True)
	berkas_stnk = fields.ToOneField(BerkasResource, 'berkas_stnk', full=True, null=True, blank=True)
	berkas_kartu_pengawasan = fields.ToOneField(BerkasResource, 'berkas_kartu_pengawasan', full=True, null=True, blank=True)
	class Meta:
		# authentication = ApiKeyAuthentication()
		queryset = Kendaraan.objects.all()
		# fields = ['id', 'nomor_kendaraan', 'nomor_uji_berkala', 'merk_kendaraan', 'berat_diperbolehkan', 'nomor_rangka', 'nomor_mesin', 'tahun_pembuatan', 'keterangan', 'pengajuan_izin_id', 'berkas_stnk', 'berkas_kartu_pengawasan']
		filtering = {
			'pengajuan_izin_id': ['contains'],
		}

class KategoriKendaraanRecource(CORSModelResource):
	class Meta:
		queryset = KategoriKendaraan.objects.all()

class DetilHOResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True, null=True)
	perusahaan = fields.ToOneField(PerusahaanResource, 'perusahaan', full = True, null=True)
	kelompok_jenis_izin = fields.CharField(attribute="kelompok_jenis_izin__kelompok_jenis_izin", null=True, blank=True)
	jenis_permohonan = fields.CharField(attribute="jenis_permohonan__jenis_permohonan_izin", null=True, blank=True)
	lokasi_lengkap = fields.CharField(attribute="desa__lokasi_lengkap", null=True, blank=True)
	class Meta:
		queryset = DetilHO.objects.all()

class DetilIUAResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True)
	kelompok_jenis_izin = fields.ToOneField(KelompokJenisIzinRecource, 'kelompok_jenis_izin', full = True)
	verified_by = fields.ToOneField(KepegawaianResource, 'verified_by', full=True, null=True)
	created_by = fields.ToOneField(KepegawaianResource, 'created_by', full=True, null=True)
	jenis_permohonan = fields.ToOneField(JenisPermohonanIzinResource, 'jenis_permohonan', full=True, null=True)
	perusahaan = fields.ToOneField(PerusahaanResource, 'perusahaan', full = True)
	kategori_kendaraan = fields.ToOneField(KategoriKendaraanRecource, 'kategori_kendaraan', full = True, null=True)
	detil_izin_ho = fields.ToOneField(DetilHOResource, 'detil_izin_ho', full = True, null=True, blank=True)
	berkas_tambahan = fields.OneToManyField(BerkasResource, 'berkas_tambahan', full=True, null=True, blank=True)
	class Meta:
		# authentication = ApiKeyAuthentication()
		authorization = Authorization()
		queryset = DetilIUA.objects.all()
		allowed_methods = ['get', 'put']
		fields = ['id', 'no_pengajuan', 'pemohon', 'kelompok_jenis_izin', 'created_at', 'created_by', 'verified_at', 'verified_by', 'jenis_permohonan', 'status', 'perusahaan', 'nilai_investasi', 'kategori_kendaraan', 'berkas_tambahan']

class DataAnggotaParkirResource(CORSModelResource):
	class Meta:
		queryset = DataAnggotaParkir.objects.all()

class DetilIzinParkirIsidentilResource(CORSModelResource):
	class Meta:
		queryset = DetilIzinParkirIsidentil.objects.all()

class PengajuanIzinAllResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True)
	kelompok_jenis_izin = fields.ToOneField(KelompokJenisIzinRecource, 'kelompok_jenis_izin', full = True)
	verified_by = fields.ToOneField(KepegawaianResource, 'verified_by', full=True, null=True)
	created_by = fields.ToOneField(KepegawaianResource, 'created_by', full=True, null=True)
	jenis_permohonan = fields.ToOneField(JenisPermohonanIzinResource, 'jenis_permohonan', full=True, null=True)
	class Meta:
		queryset = PengajuanIzin.objects.all()
		fields = ['id', 'no_pengajuan', 'pemohon', 'kelompok_jenis_izin', 'created_at', 'created_by', 'verified_at', 'verified_by', 'jenis_permohonan', 'status', 'updated_at']
		authentication = ApiKeyAuthentication()
		allowed_methods = ['get', 'put']
		filtering = {
			'id': ALL,
			"no_pengajuan" : ALL,
			"pemohon" : ALL_WITH_RELATIONS,
		}

	def get_object_list(self, request):
		data = super(PengajuanIzinAllResource, self).get_object_list(request)
		data = data.order_by('-updated_at')
		return data

class DetilTDPResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True, null=True)
	perusahaan = fields.ToOneField(PerusahaanResource, 'perusahaan', full = True, null=True)
	kelompok_jenis_izin = fields.CharField(attribute="kelompok_jenis_izin__kelompok_jenis_izin", null=True, blank=True)
	jenis_permohonan = fields.CharField(attribute="jenis_permohonan__jenis_permohonan_izin", null=True, blank=True)
	status_perusahaan = fields.CharField(attribute="status_perusahaan__status_perusahaan", null=True, blank=True)
	jenis_badan_usaha = fields.CharField(attribute="jenis_badan_usaha__jenis_badan_usaha", null=True, blank=True)
	bentuk_kerjasama = fields.CharField(attribute="bentuk_kerjasama__bentuk_kerjasama", null=True, blank=True)
	jenis_penanaman_modal = fields.CharField(attribute="jenis_penanaman_modal__jenis_penanaman_modal", null=True, blank=True)
	desa_unit_produksi = fields.CharField(attribute="desa_unit_produksi__lokasi_lengkap", null=True, blank=True)
	kegiatan_usaha_pokok = fields.ToManyField(KBLIResource, 'kegiatan_usaha_pokok', full = True, null=True)
	jenis_pengecer = fields.CharField(attribute="jenis_pengecer__jenis_pengecer", null=True, blank=True)
	jenis_perusahaan = fields.CharField(attribute="jenis_perusahaan__jenis_perusahaan", null=True, blank=True)
	jenis_koperasi = fields.CharField(attribute="jenis_koperasi__jenis_koperasi", null=True, blank=True)
	bentuk_koperasi = fields.CharField(attribute="bentuk_koperasi__bentuk_koperasi", null=True, blank=True)
	# legalitas = fields.ToManyField(LegalitasResource, '', full = True, null=True)
	masa_berlaku = fields.CharField(attribute="get_masa_berlaku", null=True, blank=True)

	class Meta:
		queryset = DetilTDP.objects.all()
		limit = 10
		authentication = ApiKeyAuthentication()
		filtering = {
			"no_pengajuan" : ALL,
			"pemohon" : ALL_WITH_RELATIONS,
		}

class IzinLainResource(CORSModelResource):
	pengajuan_izin_id = fields.IntegerField(attribute="pengajuan_izin__id", null=True, blank=True)
	kelompok_jenis_izin = fields.CharField(attribute="kelompok_jenis_izin__kelompok_jenis_izin", null=True, blank=True)
	class Meta:
		queryset = IzinLain.objects.all()
		filtering = {
			'pengajuan_izin_id': ['contains'],
		}
		excludes = ['updated_at', 'verified_at', 'status', 'rejected_at', 'created_at']

class DetilReklameResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True, null=True)
	perusahaan = fields.ToOneField(PerusahaanResource, 'perusahaan', full = True, null=True)
	kelompok_jenis_izin = fields.CharField(attribute="kelompok_jenis_izin__kelompok_jenis_izin", null=True, blank=True)
	jenis_permohonan = fields.CharField(attribute="jenis_permohonan__jenis_permohonan_izin", null=True, blank=True)
	jenis_reklame = fields.CharField(attribute="jenis_reklame__jenis_reklame", null=True, blank=True)
	tipe_reklame = fields.CharField(attribute="tipe_reklame__jenis_tipe_reklame", null=True, blank=True)
	lokasi_lengkap = fields.CharField(attribute="desa__lokasi_lengkap", null=True, blank=True)

	class Meta:
		queryset = DetilReklame.objects.all()
		limit = 10
		authentication = ApiKeyAuthentication()

class DetilReklameIzinResource(CORSModelResource):
	detil_reklame_id = fields.IntegerField(attribute="detil_reklame__id", null=True, blank=True)
	tipe_reklame = fields.CharField(attribute="tipe_reklame__jenis_tipe_reklame", null=True, blank=True)
	lokasi_lengkap = fields.CharField(attribute="desa__lokasi_lengkap", null=True, blank=True)

	class Meta:
		queryset = DetilReklameIzin.objects.all()
		filtering = {
			'detil_reklame_id': ['contains']
		}
		authentication = ApiKeyAuthentication()

class DetilIMBPapanReklameResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True, null=True)
	perusahaan = fields.ToOneField(PerusahaanResource, 'perusahaan', full = True, null=True)
	kelompok_jenis_izin = fields.CharField(attribute="kelompok_jenis_izin__kelompok_jenis_izin", null=True, blank=True)
	jenis_permohonan = fields.CharField(attribute="jenis_permohonan__jenis_permohonan_izin", null=True, blank=True)
	lokasi_lengkap = fields.CharField(attribute="desa__lokasi_lengkap", null=True, blank=True)

	class Meta:
		queryset = DetilIMBPapanReklame.objects.all()
		authentication = ApiKeyAuthentication()

class DetilIMBResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True, null=True)
	kelompok_jenis_izin = fields.CharField(attribute="kelompok_jenis_izin__kelompok_jenis_izin", null=True, blank=True)
	jenis_permohonan = fields.CharField(attribute="jenis_permohonan__jenis_permohonan_izin", null=True, blank=True)
	lokasi_lengkap = fields.CharField(attribute="desa__lokasi_lengkap", null=True, blank=True)
	parameter_bangunan = fields.ToManyField(ParameterBangunanResource, 'parameter_bangunan', full = True, null=True)
	jenis_bangunan = fields.ToOneField(BangunanJenisKontruksiResource, 'jenis_bangunan', full=True, null=True)

	class Meta:
		queryset = DetilIMB.objects.all()
		# authentication = ApiKeyAuthentication()

class InformasiKekayaanDaerahResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True, null=True)
	perusahaan = fields.ToOneField(PerusahaanResource, 'perusahaan', full = True, null=True)
	kelompok_jenis_izin = fields.CharField(attribute="kelompok_jenis_izin__kelompok_jenis_izin", null=True, blank=True)
	jenis_permohonan = fields.CharField(attribute="jenis_permohonan__jenis_permohonan_izin", null=True, blank=True)
	lokasi_lengkap = fields.CharField(attribute="desa__lokasi_lengkap", null=True, blank=True)
	desa = fields.ToOneField(DesaResource, 'desa', full = True, null=True)
	
	class Meta:
		queryset = InformasiKekayaanDaerah.objects.all()

class DetilHullerResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True, null=True)
	perusahaan = fields.ToOneField(PerusahaanResource, 'perusahaan', full = True, null=True)
	kelompok_jenis_izin = fields.CharField(attribute="kelompok_jenis_izin__kelompok_jenis_izin", null=True, blank=True)
	jenis_permohonan = fields.CharField(attribute="jenis_permohonan__jenis_permohonan_izin", null=True, blank=True)
	pemilik_desa_lokasi_lengkap = fields.CharField(attribute="pemilik_desa__lokasi_lengkap", null=True, blank=True)
	pengusaha_desa_lokasi_lengkap = fields.CharField(attribute="pengusaha_desa__lokasi_lengkap", null=True, blank=True)
	
	class Meta:
		queryset = DetilHuller.objects.all()

class JenisMesinResource(CORSModelResource):
	class Meta:
		queryset = JenisMesin.objects.all()
		filtering = {
			"id" : ['contains'],
		}

class MesinHullerResource(CORSModelResource):
	jenis_mesin = fields.ToOneField(JenisMesinResource, 'jenis_mesin', full=True, null=True)
	class Meta:
		queryset = MesinHuller.objects.all()
		filtering = {
			"jenis_mesin" : ALL_WITH_RELATIONS,
		}

class MesinPerusahaanResource(CORSModelResource):
	detil_huller_id = fields.CharField(attribute="detil_huller__id", null=True, blank=True)
	mesin_huller = fields.ToOneField(MesinHullerResource, "mesin_huller", full=True, null=True, blank=True)
	class Meta:
		queryset = MesinPerusahaan.objects.all()
		filtering = {
			'detil_huller_id': ['contains'],
			"mesin_huller" : ALL_WITH_RELATIONS,
		}

class InformasiTanahResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True, null=True)
	perusahaan = fields.ToOneField(PerusahaanResource, 'perusahaan', full = True, null=True)
	kelompok_jenis_izin = fields.CharField(attribute="kelompok_jenis_izin__kelompok_jenis_izin", null=True, blank=True)
	jenis_permohonan = fields.CharField(attribute="jenis_permohonan__jenis_permohonan_izin", null=True, blank=True)
	lokasi_lengkap = fields.CharField(attribute="desa__lokasi_lengkap", null=True, blank=True)
	
	class Meta:
		queryset = InformasiTanah.objects.all()

class SertifikatTanahResource(CORSModelResource):
	informasi_tanah_id = fields.IntegerField(attribute="informasi_tanah__id", null=True, blank=True)
	class Meta:
		queryset = SertifikatTanah.objects.all()
		filtering = {
			"informasi_tanah_id" : ['contains'],
		}

class PenggunaanTanahIPPTUsahaResource(CORSModelResource):
	informasi_tanah_id = fields.IntegerField(attribute="informasi_tanah__id", null=True, blank=True)
	class Meta:
		queryset = PenggunaanTanahIPPTUsaha.objects.all()
		filtering = {
			"informasi_tanah_id" : ['contains'],
		}

class PerumahanYangDimilikiIPPTUsahaResource(CORSModelResource):
	informasi_tanah_id = fields.IntegerField(attribute="informasi_tanah__id", null=True, blank=True)
	class Meta:
		queryset = PerumahanYangDimilikiIPPTUsaha.objects.all()
		filtering = {
			"informasi_tanah_id" : ['contains'],
		}

class DetilIUJKResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True, null=True)
	perusahaan = fields.ToOneField(PerusahaanResource, 'perusahaan', full = True, null=True)
	kelompok_jenis_izin = fields.CharField(attribute="kelompok_jenis_izin__kelompok_jenis_izin", null=True, blank=True)
	kualifikasi = fields.CharField(attribute="kualifikasi__nama_kualifikasi", null=True, blank=True)
	class Meta:
		queryset = DetilIUJK.objects.all()

class KlasifikasiResource(CORSModelResource):
	class Meta:
		queryset = Klasifikasi.objects.all()

class SubklasifikasiResource(CORSModelResource):
	kualifikasi = fields.ToOneField(KlasifikasiResource, 'kualifikasi', full = True, null=True)
	class Meta:
		queryset = Subklasifikasi.objects.all()

class PaketPekerjaanResource(CORSModelResource):
	detil_iujk_id = fields.IntegerField(attribute="detil_iujk__id", null=True, blank=True)
	sub_kualifikasi = fields.ToOneField(SubklasifikasiResource, 'sub_kualifikasi', full = True, null=True)
	class Meta:
		queryset = PaketPekerjaan.objects.all()
		filtering = {
			"detil_iujk_id" : ['contains'],
		}

class AnggotaBadanUsaha(CORSModelResource):
	detil_iujk_id = fields.IntegerField(attribute="detil_iujk__id", null=True, blank=True)
	berkas_tambahan = fields.OneToManyField(BerkasResource, 'berkas_tambahan', full=True, null=True, blank=True)
	class Meta:
		queryset = AnggotaBadanUsaha.objects.all()
		filtering = {
			"detil_iujk_id" : ['contains'],
			"jenis_anggota_badan" : ['contains'],
		}

class DetilPembayaranResource(CORSModelResource):
	# kode = fields.CharField(attribute="kode", null=True, blank=True)
	class Meta:
		queryset = DetilPembayaran.objects.all()
		authentication = ApiKeyAuthentication()
		filtering = {
			"kode": ALL,
		}

	def prepend_urls(self):
		return [
			url(r"^retribusi/cek/$", self.wrap_view('cek_retribusi'), name="api__retribusi__cek_retribusi"),
			url(r"^retribusi/update/$", self.wrap_view('update_retribusi'), name="api__retribusi__update_retribusi"),
			url(r"^retribusi/reversal/$", self.wrap_view('reversal_retribusi'), name="api__retribusi__reversal_retribusi"),
			]

	def cek_retribusi(self, request, **kwargs):
		data = {'success': False, 'pesan': 'Terjadi Kesalahan. Retribusi tidak ditemukan atau tidak ada dalam daftar disistem SIMPATIK.'}
		kode = request.GET.get('kode')
		username = request.GET.get('username')
		api_key = request.GET.get('api_key')
		cek = cek_apikey(api_key, username)
		if cek == True:
			if kode:
				try:
					retribusi_obj = DetilPembayaran.objects.get(kode=kode)
					if retribusi_obj.tanggal_deadline > datetime.date.today():
						nama_pemohon = ""
						if retribusi_obj.pengajuan_izin:
							if retribusi_obj.pengajuan_izin.pemohon:
								nama_pemohon = retribusi_obj.pengajuan_izin.pemohon.nama_lengkap
						tanggal_bayar = None
						if retribusi_obj.tanggal_deadline:
							tanggal_deadline = retribusi_obj.tanggal_deadline.strftime("%d-%m-%Y")
						bank = ""
						if retribusi_obj.bank_pembayaran:
							bank = retribusi_obj.bank_pembayaran.nama_bank
						total_bayar = None
						if retribusi_obj.jumlah_pembayaran:
							total_bayar = int(retribusi_obj.jumlah_pembayaran.replace(".", ""))
						data = {'success': True, 'pesan': 'Sukses. Retribusi berhasil diload.', 'kode': int(retribusi_obj.kode), 'nomor_kwitansi': retribusi_obj.nomor_kwitansi, 'pemohon': nama_pemohon, "peruntukan": retribusi_obj.peruntukan, 'tanggal_bayar': tanggal_bayar, 'tanggal_deadline': tanggal_deadline, 'total_bayar': total_bayar ,'bank': bank, 'terbayar': retribusi_obj.terbayar}
					else:
						data = {'success': False, 'pesan': 'Terjadi Kesalahan, Retribusi telah melewati batas pembayaran.'}
				except DetilPembayaran.DoesNotExist:
					pass
		else:
			data = {'success': False, 'pesan': 'Terjadi Kesalahan. Anda tidak memiliki akses di SIMPATIK.'}
		return CORSHttpResponse(json.dumps(data))

	def update_retribusi(self, request, **kwargs):
		data = {'success': False, 'pesan': 'Terjadi Kesalahan. Retribusi tidak ditemukan atau tidak ada dalam daftar disistem SIMPATIK.'}
		kode = request.GET.get('kode')
		username = request.GET.get('username')
		api_key = request.GET.get('api_key')
		cek = cek_apikey(api_key, username)
		if cek == True:
			if kode:
				try:
					retribusi_obj = DetilPembayaran.objects.get(kode=kode)
					if retribusi_obj.terbayar == False:
						retribusi_obj.pengajuan_izin.status = 2
						retribusi_obj.pengajuan_izin.save()
						retribusi_obj.tanggal_bayar = datetime.datetime.now()
						retribusi_obj.terbayar = True
						retribusi_obj.save()
						skizin_obj = retribusi_obj.pengajuan_izin.skizin_set.last()
						skizin_obj.status = 9
						skizin_obj.save()
						data = {'success': True, 'pesan': 'Berhasil. Pembayaran dengan nomor pembayaran '+retribusi_obj.kode+' telah berhasil terbayar.'}
					else:
						data = {'success': False, 'pesan': 'Gagal. Pembayaran dengan nomor pembayaran '+retribusi_obj.kode+' sudah terbayar.'}
					"""Melakukan pengupdatean status pengajuan izin untuk proses selanjutnya"""
				except DetilPembayaran.DoesNotExist:
					pass
		else:
			data = {'success': False, 'pesan': 'Terjadi Kesalahan. Anda tidak memiliki akses di SIMPATIK.'}
		return CORSHttpResponse(json.dumps(data))

	def reversal_retribusi(self, request, **kwargs):
		data = {'success': False, 'pesan': 'Terjadi Kesalahan. Retribusi tidak ditemukan atau tidak ada dalam daftar disistem SIMPATIK.'}
		kode = request.GET.get('kode')
		username = request.GET.get('username')
		api_key = request.GET.get('api_key')
		cek = cek_apikey(api_key, username)
		if cek == True:
			if kode:
				try:
					retribusi_obj = DetilPembayaran.objects.get(kode=kode)
					if retribusi_obj.terbayar == True:
						retribusi_obj.pengajuan_izin.status = 5
						retribusi_obj.pengajuan_izin.save()
						retribusi_obj.tanggal_bayar = None
						retribusi_obj.terbayar = False
						retribusi_obj.save()
						data = {'success': True, 'pesan': 'Berhasil. Pembayaran dengan nomor pembayaran '+retribusi_obj.kode+' telah berhasil direset.'}
					else:
						data = {'success': False, 'pesan': 'Gagal. Pembayaran dengan nomor pembayaran '+retribusi_obj.kode+' sudah direset.'}
				except DetilPembayaran.DoesNotExist:
					pass
		else:
			data = {'success': False, 'pesan': 'Terjadi Kesalahan. Anda tidak memiliki akses di SIMPATIK.'}
		return CORSHttpResponse(json.dumps(data))