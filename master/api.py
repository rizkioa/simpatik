from mobile.cors import CORSModelResource
from tastypie import fields
from models import Berkas, ParameterBangunan, BangunanJenisKontruksi, JenisKontruksi

class BerkasResource(CORSModelResource):
	# get_file_url = fields.CharField(attribute="get_file_url", null=True, blank=True)
	class Meta:
		queryset = Berkas.objects.all()
		fields = ['id', 'nama_berkas', 'berkas', 'no_berkas', 'keterangan']

class ParameterBangunanResource(CORSModelResource):
	class Meta:
		queryset = ParameterBangunan.objects.all()

class JenisKontruksiResource(CORSModelResource):
	class Meta:
		queryset = JenisKontruksi.objects.all()

class BangunanJenisKontruksiResource(CORSModelResource):
	jenis_kontruksi = fields.ToOneField(JenisKontruksiResource, 'jenis_kontruksi', full = True, null=True)
	class Meta:
		queryset = BangunanJenisKontruksi.objects.all()