from mobile.cors import CORSModelResource
from izin.models import Kendaraan, DetilIUA, DetilIzinParkirIsidentil, DataAnggotaParkir

class KendaraanRecource(CORSModelResource):
	class Meta:
		queryset = Kendaraan.objects.all()
		# excludes = ['id','jenis_izin', 'kode', 'keterangan', 'masa_berlaku', 'standart_waktu', 'biaya', 'resource_uri']
		# fields = ['Kendaraan', 'kode']

class DetilIUARecource(CORSModelResource):
	class Meta:
		queryset = DetilIUA.objects.all()

class DataAnggotaParkirRecource(CORSModelResource):
	class Meta:
		queryset = DataAnggotaParkir.objects.all()

class DetilIzinParkirIsidentilRecource(CORSModelResource):
	class Meta:
		queryset = DetilIzinParkirIsidentil.objects.all()