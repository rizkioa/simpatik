from mobile.cors import CORSModelResource, CORSHttpResponse
from izin.models import Kendaraan, DetilIUA, DetilIzinParkirIsidentil, DataAnggotaParkir, Pemohon, KategoriKendaraan, DetilHO, MerkTypeKendaraan, SKIzin, PengajuanIzin, DetilTDP, IzinLain, DetilReklame, DetilReklameIzin, DetilIMBPapanReklame, DetilIMB, InformasiKekayaanDaerah, DetilHuller, InformasiTanah, SertifikatTanah
from izin.models import Kendaraan, DetilIUA, DetilIzinParkirIsidentil, DataAnggotaParkir, Pemohon, KategoriKendaraan, DetilHO, MerkTypeKendaraan, SKIzin, PengajuanIzin, DetilTDP, IzinLain, DetilReklame, DetilReklameIzin, DetilIMBPapanReklame, DetilIMB, InformasiKekayaanDaerah, DetilHuller, DetilIUJK
from izin.models import Kendaraan, DetilIUA, DetilIzinParkirIsidentil, DataAnggotaParkir, Pemohon, KategoriKendaraan, DetilHO, MerkTypeKendaraan, SKIzin, PengajuanIzin, DetilTDP, IzinLain, DetilReklame, DetilReklameIzin, DetilIMBPapanReklame, DetilIMB, InformasiKekayaanDaerah, DetilHuller, InformasiTanah, SertifikatTanah, PenggunaanTanahIPPTUsaha, PerumahanYangDimilikiIPPTUsaha
from izin.models import Kendaraan, DetilIUA, DetilIzinParkirIsidentil, DataAnggotaParkir, Pemohon, KategoriKendaraan, DetilHO, MerkTypeKendaraan, SKIzin, PengajuanIzin, DetilTDP, IzinLain, DetilReklame, DetilReklameIzin, DetilIMBPapanReklame, DetilIMB, InformasiKekayaanDaerah, DetilHuller, InformasiTanah, SertifikatTanah, PenggunaanTanahIPPTUsaha, PerumahanYangDimilikiIPPTUsaha, JenisMesin, MesinHuller, MesinPerusahaan
from mobile.api import KelompokJenisIzinRecource, JenisPermohonanIzinResource, KepegawaianResource
from tastypie import fields
from perusahaan.api import PerusahaanResource, KBLIResource, LegalitasResource
from master.api import BerkasResource, ParameterBangunanResource, BangunanJenisKontruksiResource, DesaResource
from tastypie.resources import ALL_WITH_RELATIONS, ALL
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from django.conf.urls import url
import json

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
		filtering = {
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