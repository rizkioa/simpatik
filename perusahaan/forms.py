from django import forms
from perusahaan.models import AktaNotaris, Perusahaan,ProdukUtama,KegiatanUsaha,KBLI
from perusahaan.utils import AKTA
from django.forms import ModelForm

class PerusahaanForm(ModelForm):
	class Meta:
		model = Perusahaan
		fields = "__all__"

class AktaNotarisForm(ModelForm):
	# perusahaan = forms.ModelChoiceField(queryset=Perusahaan.objects.all(), label='Perusahaan')
	# no_akta = forms.CharField(max_length=255, label='No Akta')
	# tanggal_akta = forms.DateField( label='Tanggal Akta')
	# no_pengesahan = forms.CharField(max_length=255, label='No Pengesahan')
	# tanggal_pengesahan = forms.DateField(label='Tanggal Pengesahan',required=True)
	# jenis_akta = forms.CharField(max_length=20, label='Jenis Akta',
	# 							widget=forms.Select(choices=AKTA))
	class Meta:
		model = AktaNotaris
		exclude = ('Perusahaan',)


class BarangJasaForm(ModelForm):
	class Meta:
		model = KegiatanUsaha
		exclude = ('kegiatan_usaha','nama_kbli','barang_jasa_utama')