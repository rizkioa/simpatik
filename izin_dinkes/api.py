from mobile.cors import CORSModelResource, CORSHttpResponse
from models import *
from tastypie.resources import ALL_WITH_RELATIONS, ALL
from tastypie import fields

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