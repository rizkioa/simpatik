from mobile.cors import CORSModelResource, CORSHttpResponse
from models import *
from tastypie.authentication import ApiKeyAuthentication
from tastypie.resources import ALL_WITH_RELATIONS, ALL
from tastypie import fields
from izin.api import PemohonResource

class PeralatanLaboratoriumResource(CORSModelResource):
	laboratorium_id = fields.CharField(attribute="laboratorium__id", null=True, blank=True)
	class Meta:
		queryset = PeralatanLaboratorium.objects.all()
		filtering = {
			'id': ALL,
			'laboratorium_id': ALL,
		}

class BangunanLaboratoriumResource(CORSModelResource):
	laboratorium_id = fields.CharField(attribute="laboratorium__id", null=True, blank=True)
	nama_jenis_bangunan = fields.CharField(attribute="jenis_kelengkapan_bangunan__nama_jenis_kelengkapan_bangunan", null=True, blank=True)
	class Meta:
		queryset = BangunanLaboratorium.objects.all()
		filtering = {
			'id': ALL,
			'laboratorium_id': ALL,
		}

class ApotekResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True, null=True)
	kelompok_jenis_izin = fields.CharField(attribute="kelompok_jenis_izin__kelompok_jenis_izin", null=True, blank=True)
	jenis_permohonan = fields.CharField(attribute="jenis_permohonan__jenis_permohonan_izin", null=True, blank=True)
	sarana = fields.CharField(attribute="sarana__nama_sarana", null=True, blank=True)
	class Meta:
		queryset = Apotek.objects.all()
		authentication = ApiKeyAuthentication()
		allowed_methods = ['get', 'put']
		filtering = {
			'id': ALL,
		}

class SaranaResource(CORSModelResource):
	class Meta:
		queryset = Sarana.objects.all()
		filtering = {
			'id': ALL,
		}

class TokoObatResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True, null=True)
	kelompok_jenis_izin = fields.CharField(attribute="kelompok_jenis_izin__kelompok_jenis_izin", null=True, blank=True)
	jenis_permohonan = fields.CharField(attribute="jenis_permohonan__jenis_permohonan_izin", null=True, blank=True)
	class Meta:
		queryset = TokoObat.objects.all()
		authentication = ApiKeyAuthentication()
		allowed_methods = ['get', 'put']
		filtering = {
			'id': ALL,
		}

class LaboratoriumResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True, null=True)
	kelompok_jenis_izin = fields.CharField(attribute="kelompok_jenis_izin__kelompok_jenis_izin", null=True, blank=True)
	jenis_permohonan = fields.CharField(attribute="jenis_permohonan__jenis_permohonan_izin", null=True, blank=True)
	class Meta:
		queryset = Laboratorium.objects.all()
		authentication = ApiKeyAuthentication()
		allowed_methods = ['get', 'put']
		filtering = {
			'id': ALL,
		}

class OptikalResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True, null=True)
	kelompok_jenis_izin = fields.CharField(attribute="kelompok_jenis_izin__kelompok_jenis_izin", null=True, blank=True)
	jenis_permohonan = fields.CharField(attribute="jenis_permohonan__jenis_permohonan_izin", null=True, blank=True)
	class Meta:
		queryset = Optikal.objects.all()
		authentication = ApiKeyAuthentication()
		allowed_methods = ['get', 'put']
		filtering = {
			'id': ALL,
		}

class MendirikanKlinikResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True, null=True)
	kelompok_jenis_izin = fields.CharField(attribute="kelompok_jenis_izin__kelompok_jenis_izin", null=True, blank=True)
	jenis_permohonan = fields.CharField(attribute="jenis_permohonan__jenis_permohonan_izin", null=True, blank=True)
	lokasi_lengkap = fields.CharField(attribute="desa__lokasi_lengkap", null=True, blank=True)
	class Meta:
		queryset = MendirikanKlinik.objects.all()
		authentication = ApiKeyAuthentication()
		allowed_methods = ['get', 'put']
		filtering = {
			'id': ALL,
		}

class OperasionalKlinikResource(CORSModelResource):
	pemohon = fields.ToOneField(PemohonResource, 'pemohon', full = True, null=True)
	kelompok_jenis_izin = fields.CharField(attribute="kelompok_jenis_izin__kelompok_jenis_izin", null=True, blank=True)
	jenis_permohonan = fields.CharField(attribute="jenis_permohonan__jenis_permohonan_izin", null=True, blank=True)
	lokasi_lengkap = fields.CharField(attribute="desa__lokasi_lengkap", null=True, blank=True)
	class Meta:
		queryset = OperasionalKlinik.objects.all()
		authentication = ApiKeyAuthentication()
		allowed_methods = ['get', 'put']
		filtering = {
			'id': ALL,
		}



