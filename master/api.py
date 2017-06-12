from mobile.cors import CORSModelResource
from tastypie import fields
from models import Berkas

class BerkasResource(CORSModelResource):
	get_file_url = fields.CharField(attribute="get_file_url", null=True, blank=True)
	class Meta:
		queryset = Berkas.objects.all()
		fields = ['id', 'nama_berkas', 'berkas', 'no_berkas', 'keterangan', 'get_file_url']