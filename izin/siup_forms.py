from django import forms
from izin.models import Izin, Pemohon
from perusahaan.models import Perusahaan

class IzinPemohonForm(forms.ModelForm):
	pemohon = forms.ModelChoiceField(label='Pilih Pemohon', queryset=Pemohon.objects.none(), required=False)
	# pemohon = forms.CharField(label="Pilih Pemohon",required=True,widget=forms.TextInput(attrs={'placeholder': 'Ketik Nama Pemohon....'}))
	class Meta:
		model = Izin
		fields = ('pemohon',)

class IzinPerusahaanForm(forms.ModelForm):
	perusahaan = forms.ModelChoiceField(label='Pilih Perusahaan', queryset=Perusahaan.objects.none(), required=False)

	class Meta:
		model = Perusahaan
		fields = ('nama_perusahaan',)
