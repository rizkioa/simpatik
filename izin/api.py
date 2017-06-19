from mobile.cors import CORSModelResource
from izin.models import Kendaraan, DetilIUA, DetilIzinParkirIsidentil, DataAnggotaParkir, Pemohon, KategoriKendaraan, DetilHO, MerkTypeKendaraan, SKIzin, PengajuanIzin
from mobile.api import KelompokJenisIzinRecource, JenisPermohonanIzinResource, KepegawaianResource
from tastypie import fields
from perusahaan.api import PerusahaanResource
from master.api import BerkasResource
from tastypie.resources import ALL_WITH_RELATIONS, ALL
from tastypie.authentication import SessionAuthentication, ApiKeyAuthentication, BasicAuthentication

class SKIzinResource(CORSModelResource):
	pengajuan_izin_id = fields.IntegerField(attribute="pengajuan_izin__id", null=True, blank=True)
	class Meta:
		queryset = SKIzin.objects.all()
		fields = ['id', 'status', 'pengajuan_izin_id']
		filtering = {
			'pengajuan_izin_id' : ['contains'],
			'pengajuan_izin': ALL,
		}

class PemohonResource(CORSModelResource):
	class Meta:
		queryset = Pemohon.objects.all()
		# allowed_methods = ['get']
		# fields = ['id', 'nama_lengkap']

class MerkTypeKendaraanResource(CORSModelResource):
	class Meta:
		queryset = MerkTypeKendaraan.objects.all()

class KendaraanResource(CORSModelResource):
	merk_kendaraan = fields.ToOneField(MerkTypeKendaraanResource, 'merk_kendaraan', full = True)
	iua_id = fields.IntegerField(attribute="iua__id", null=True, blank=True)
	class Meta:
		# authentication = ApiKeyAuthentication()
		queryset = Kendaraan.objects.all()
		fields = ['id', 'nomor_kendaraan', 'nomor_uji_berkala', 'merk_kendaraan', 'berat_diperbolehkan', 'nomor_rangka', 'nomor_mesin', 'tahun_pembuatan', 'keterangan', 'iua_id']
		filtering = {
			'iua_id': ['contains'],
			# 'status': ALL,
		}

class KategoriKendaraanRecource(CORSModelResource):
	class Meta:
		queryset = KategoriKendaraan.objects.all()

class DetilHOResource(CORSModelResource):
	class Meta:
		queryset = DetilHO.objects.all()

class DetilIUAResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True)
	kelompok_jenis_izin = fields.ToOneField(KelompokJenisIzinRecource, 'kelompok_jenis_izin', full = True)
	verified_by = fields.ToOneField(KepegawaianResource, 'verified_by', full=True, null=True)
	created_by = fields.ToOneField(KepegawaianResource, 'created_by', full=True, null=True)
	jenis_permohonan = fields.ToOneField(JenisPermohonanIzinResource, 'jenis_permohonan', full=True, null=True)
	perusahaan = fields.ToOneField(PerusahaanResource, 'perusahaan', full = True)
	kategori_kendaraan = fields.ToOneField(KategoriKendaraanRecource, 'kategori_kendaraan', full = True)
	detil_izin_ho = fields.ToOneField(DetilHOResource, 'detil_izin_ho', full = True, null=True, blank=True)
	berkas_tambahan = fields.OneToManyField(BerkasResource, 'berkas_tambahan', full=True, null=True, blank=True)
	class Meta:
		# authentication = ApiKeyAuthentication()
		queryset = DetilIUA.objects.all()
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
		fields = ['id', 'no_pengajuan', 'pemohon', 'kelompok_jenis_izin', 'created_at', 'created_by', 'verified_at', 'verified_by', 'jenis_permohonan', 'status']
		authentication = ApiKeyAuthentication()
		filtering = {
			'no_pengajuan': ['contains'],
			# 'status': ALL,
		}
