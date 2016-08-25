from django import forms

from izin.utils import JENIS_IZIN
from izin.models import Pemohon
from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa


EMPTY_JENIS_IZIN = (('', 'Select an Option'),)+JENIS_IZIN

class PengajuanBaruForm(forms.Form):
	jenis_izin = forms.ChoiceField(choices=EMPTY_JENIS_IZIN, label='Jenis Izin', initial='jenis_izin')
	nama_izin = forms.ChoiceField(label='Nama Izin', initial='nama_izin')
	# kelompok_jenis_izin = forms.ChoiceField(label='')



class PemohonForm(forms.ModelForm):
	"""docstring for PemohonForm"""

	class Meta:
		model = Pemohon
		fields = ('jenis_pemohon', 'nama_lengkap', 'tempat_lahir', 'alamat',)

	def clean_email(self):
		return self.cleaned_data['email'] or None