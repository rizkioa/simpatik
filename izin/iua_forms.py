from django import forms
from izin.models import DetilIUA, Kendaraan

class DetaiIUAForm(forms.ModelForm):
	class Meta:
		model = DetilIUA
		fields = ('nilai_investasi', 'keterangan')

class DataKendaraanForm(forms.ModelForm):
	class Meta:
		model = Kendaraan
		fields = ('nomor_kendaraan', 'nomor_uji_berkala', 'merk_kendaraan', 'berat_diperbolehkan', 'nomor_rangka', 'nomor_mesin', 'tahun_pembuatan', 'keterangan')