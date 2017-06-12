from models import Perusahaan
from mobile.cors import CORSModelResource

class PerusahaanResource(CORSModelResource):
	class Meta:
		queryset = Perusahaan.objects.all()