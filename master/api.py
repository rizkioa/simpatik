from mobile.cors import CORSModelResource
from tastypie import fields
from models import Berkas, ParameterBangunan, BangunanJenisKontruksi, JenisKontruksi, Desa

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

class DesaResource(CORSModelResource):
	id_kecamatan = fields.CharField(attribute="kecamatan__id", null=True, blank=True)
	id_kabupaten = fields.CharField(attribute="kecamatan__kabupaten__id", null=True, blank=True)
	id_provinsi = fields.CharField(attribute="kecamatan__kabupaten__provinsi__id", null=True, blank=True)
	id_negara = fields.CharField(attribute="kecamatan__kabupaten__provinsi__negara__id", null=True, blank=True)
	class Meta:
		queryset = Desa.objects.all()
		limit = 20
		fields = ['id', 'id_kecamatan', 'id_kabupaten', 'id_provinsi', 'id_negara']