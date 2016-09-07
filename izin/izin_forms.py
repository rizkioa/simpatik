from django import forms

from izin.utils import JENIS_IZIN
from izin.models import Pemohon, KelompokJenisIzin, JenisIzin
from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa
from accounts.models import NomorIdentitasPengguna
from perusahaan.models import Perusahaan

EMPTY_JENIS_IZIN = (('', 'Select an Option'),)+JENIS_IZIN

class PengajuanBaruForm(forms.Form):
	jenis_izin = forms.ChoiceField(choices=EMPTY_JENIS_IZIN, label='Jenis Izin', initial='jenis_izin')
	nama_izin = forms.ModelChoiceField(label='Nama Izin', queryset=JenisIzin.objects.none(), initial='nama_izin')
	kelompok_jenis_izin = forms.ModelChoiceField(label='', queryset=KelompokJenisIzin.objects.none(), initial='klmpk_izin')

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(PengajuanBaruForm, self).__init__(*args, **kwargs)

		if self.request.POST:
			nama_izin = self.request.POST.get('nama_izin', None)
			if nama_izin:
				self.fields['kelompok_jenis_izin'].queryset = KelompokJenisIzin.objects.filter(jenis_izin__id=nama_izin)




class PemohonForm(forms.ModelForm):
	"""docstring for PemohonForm"""

	def __init__(self, *args, **kwargs):
		super(PemohonForm, self).__init__(*args, **kwargs)
		# self.fields['desa'].required = True
		self.fields['alamat'].required = True
		self.fields['telephone'].required = True

	class Meta:
		model = Pemohon
		fields = ('jenis_pemohon', 'nama_lengkap', 'tempat_lahir', 'alamat','tanggal_lahir','telephone','hp','kewarganegaraan','desa','email','pekerjaan')

	def clean_email(self):
		return self.cleaned_data['email'] or None


class PerusahaanForm(forms.ModelForm):
	"""docstring for PerusahaaanForm"""

	class Meta:
		model = Perusahaan
		fields = ('nama_perusahaan', 'nama_grup','alamat_perusahaan','desa','kode_pos','telepon','fax','email','npwp')


		
