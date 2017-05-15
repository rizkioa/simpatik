from izin.models import Pemohon
from perusahaan.models import Perusahaan
from django.core.exceptions import ObjectDoesNotExist

def load_pemohon(request, id_pemohon):
	data = {}
	if id_pemohon and is not "":
		try:
			pemohon_obj = Pemohon.objects.get(id=id_pemohon)
			data = pemohon_obj.as_json()
		except ObjectDoesNotExist:
			data = {}
	return data

def load_perusahaan(request, id_perusahaan):
	data = {}
	if id_perusahaan:
		try:
			perusahaan_obj = Perusahaan.objects.get(id=id_perusahaan)
			data = perusahaan_obj.as_json()
		except ObjectDoesNotExist:
			data = {}
	return data