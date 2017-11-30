from django import forms
from django.forms import ModelForm
from izin.models import Izin, Pemohon,KekayaanDanSaham
from perusahaan.models import Perusahaan, AktaNotaris


class IzinPemohonForm(forms.ModelForm):
	pemohon = forms.ModelChoiceField(label='Pilih Pemohon', queryset=Pemohon.objects.none(), required=False)
	# pemohon = forms.CharField(label="Pilih Pemohon",required=True,widget=forms.TextInput(attrs={'placeholder': 'Ketik Nama Pemohon....'}))
	perusahaan = forms.ModelChoiceField(label='Pilih Perusahaan', queryset=Perusahaan.objects.none(), required=False)

	class Meta:
		model = Izin
		fields = ('pemohon','perusahaan')
