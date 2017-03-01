from tastypie.resources import ModelResource
from izin.models import PengajuanIzin

class PengajuanIzinResource(ModelResource):
	class Meta:
		queryset = PengajuanIzin.objects.all()
		allowed_methods = ['get']