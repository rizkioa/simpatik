from django import forms


from izin.models import PaketPekerjaan, DetilIUJK, AnggotaBadanUsaha

class PaketPekerjaanForm(forms.ModelForm):

	class Meta:
		model = PaketPekerjaan
		fields = ('nama_paket_pekerjaan','klasifikasi_usaha','tahun','nilai_paket_pekerjaan')


class DetilIUJKForm(forms.ModelForm):
	"""docstring for DetilIUJKForm"""

	class Meta:
		model = DetilIUJK
		fields = ('perusahaan', 'jenis_iujk')

class DataAnggotaForm(forms.ModelForm):
	"""docstring for DataAnggotaForm"""
	class Meta:
		model = AnggotaBadanUsaha
		fields = ('nama', )
		
		
