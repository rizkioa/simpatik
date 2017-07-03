from models import Perusahaan, KBLI, Legalitas, DataPimpinan, PemegangSaham
from mobile.cors import CORSModelResource
from tastypie import fields
from tastypie.authentication import SessionAuthentication, ApiKeyAuthentication, BasicAuthentication

class PerusahaanResource(CORSModelResource):
	lokasi_lengkap = fields.CharField(attribute="desa__lokasi_lengkap", null=True, blank=True)
	perusahaan_induk_id = fields.IntegerField(attribute="perusahaan_induk__id", null=True, blank=True)
	class Meta:
		queryset = Perusahaan.objects.all()
		authentication = ApiKeyAuthentication()
		excludes = ['created_at', 'updated_at', 'verified_at', 'rejected_at']
		filtering = {
			'perusahaan_induk_id': ['contains'],
		}

class KBLIResource(CORSModelResource):
	class Meta:
		queryset = KBLI.objects.all()
		authentication = ApiKeyAuthentication()
		excludes = ['created_at', 'updated_at', 'verified_at']

class LegalitasResource(CORSModelResource):
	perusahaan_id = fields.IntegerField(attribute="perusahaan__id", null=True, blank=True)
	jenis_legalitas = fields.CharField(attribute="jenis_legalitas__jenis_legalitas", null=True, blank=True)
	class Meta:
		queryset = Legalitas.objects.all()
		authentication = ApiKeyAuthentication()
		filtering = {
			'perusahaan_id': ['contains'],
			# 'status': ALL,
		}
		# excludes = ['created_at', 'updated_at', 'verified_at']

class DataPimpinanResource(CORSModelResource):
	pengajuan_izin_id = fields.IntegerField(attribute="detil_tdp__id", null=True, blank=True)
	kedudukan = fields.CharField(attribute="kedudukan__kedudukan_pimpinan", null=True, blank=True)
	class Meta:
		queryset = DataPimpinan.objects.all()
		filtering = {
			'pengajuan_izin_id': ['contains'],
		}
		# excludes = ['updated_at', 'verified_at', 'status', 'rejected_at', 'created_at']

class PemegangSahamResource(CORSModelResource):
	pengajuan_izin_id = fields.IntegerField(attribute="detil_tdp__id", null=True, blank=True)
	class Meta:
		queryset = PemegangSaham.objects.all()
		filtering = {
			'pengajuan_izin_id': ['contains'],
		}