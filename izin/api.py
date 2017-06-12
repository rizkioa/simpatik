from mobile.cors import CORSModelResource
from izin.models import Kendaraan, DetilIUA, DetilIzinParkirIsidentil, DataAnggotaParkir, Pemohon, KategoriKendaraan, DetilHO
from mobile.api import KelompokJenisIzinRecource, JenisPermohonanIzinResource, KepegawaianResource
from tastypie import fields
from perusahaan.api import PerusahaanResource

class PemohonResource(CORSModelResource):
	class Meta:
		queryset = Pemohon.objects.all()
		# allowed_methods = ['get']
		# fields = ['id', 'nama_lengkap']

class KendaraanRecource(CORSModelResource):
	class Meta:
		# authentication = ApiKeyAuthentication()
		queryset = Kendaraan.objects.all()
		# excludes = ['id','jenis_izin', 'kode', 'keterangan', 'masa_berlaku', 'standart_waktu', 'biaya', 'resource_uri']
		# fields = ['Kendaraan', 'kode']

class KategoriKendaraanRecource(CORSModelResource):
	class Meta:
		queryset = KategoriKendaraan.objects.all()

class DetilHORecource(CORSModelResource):
	class Meta:
		queryset = DetilHO.objects.all()

class DetilIUARecource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True)
	kelompok_jenis_izin = fields.ToOneField(KelompokJenisIzinRecource, 'kelompok_jenis_izin', full = True)
	verified_by = fields.ToOneField(KepegawaianResource, 'verified_by', full=True, null=True)
	created_by = fields.ToOneField(KepegawaianResource, 'created_by', full=True, null=True)
	jenis_permohonan = fields.ToOneField(JenisPermohonanIzinResource, 'jenis_permohonan', full=True, null=True)
	perusahaan = fields.ToOneField(PerusahaanResource, 'perusahaan', full = True)
	kategori_kendaraan = fields.ToOneField(KategoriKendaraanRecource, 'kategori_kendaraan', full = True)
	detil_izin_ho = fields.ToOneField(DetilHORecource, 'detil_izin_ho', full = True)
	class Meta:
		# authentication = ApiKeyAuthentication()
		queryset = DetilIUA.objects.all()
		fields = ['id', 'no_pengajuan', 'pemohon', 'kelompok_jenis_izin', 'created_at', 'created_by', 'verified_at', 'verified_by', 'jenis_permohonan', 'status', 'perusahaan', 'nilai_investasi', 'kategori_kendaraan', 'detil_izin_ho']

class DataAnggotaParkirRecource(CORSModelResource):
	class Meta:
		queryset = DataAnggotaParkir.objects.all()

class DetilIzinParkirIsidentilResource(CORSModelResource):
	class Meta:
		queryset = DetilIzinParkirIsidentil.objects.all()