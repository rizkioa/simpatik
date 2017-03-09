# from tastypie.resources import ModelResource
from izin.models import PengajuanIzin
from cors import CORSModelResource

class PengajuanIzinResource(CORSModelResource):
	class Meta:
		queryset = PengajuanIzin.objects.all()
		allowed_methods = ['get']