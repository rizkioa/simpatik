from django import forms
from master.models import Desa
from perusahaan.models import AktaNotaris, Perusahaan,ProdukUtama,KegiatanUsaha,KBLI
from perusahaan.utils import AKTA
from django.forms import ModelForm

class PerusahaanForm(ModelForm):
	nama_perusahaan = forms.CharField(label="Alamat Perusahaan", required=False,)
	alamat_perusahaan = forms.CharField(label="Alamat Perusahaan", required=False,)
	desa = forms.ModelChoiceField(label="Desa", queryset=Desa.objects.none(), required=False,)
	telepon = forms.CharField(label="Telepon", required=False,)

	class Meta:
		model = Perusahaan
		fields = ('perusahaan_induk','perusahaan_lama','nomor_tdp','nama_perusahaan','nama_grup','alamat_perusahaan','desa','lt','lg','kode_pos','telepon','fax','email','npwp','berkas_npwp','penanggung_jawab','status_perusahaan','kegiatan_usaha','keterangan')

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