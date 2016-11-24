from django import forms
from izin.utils import JENIS_IZIN
from izin.models import Pemohon, KelompokJenisIzin, JenisIzin, DetilSIUP, DetilReklame
from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, Berkas
from accounts.models import NomorIdentitasPengguna
from perusahaan.models import Perusahaan, Legalitas

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
		fields = ('jabatan_pemohon', 'jenis_pemohon', 'nama_lengkap', 'tempat_lahir', 'alamat','tanggal_lahir','telephone','hp','kewarganegaraan','desa','email','pekerjaan', 'status')

	def clean_email(self):
		return self.cleaned_data['email'] or None


class PerusahaanForm(forms.ModelForm):
	"""docstring for PerusahaaanForm"""

	class Meta:
		model = Perusahaan
		fields = ('nama_perusahaan', 'nama_grup','alamat_perusahaan','desa','kode_pos','telepon','fax','email','npwp')

	def clean_email(self):
		return self.cleaned_data['email'] or None

class PengajuanSiupForm(forms.ModelForm):
	"""docstring for PengajuanSiupForm"""
	class Meta:
		model = DetilSIUP
		fields = ('kbli','kelembagaan','bentuk_kegiatan_usaha','jenis_penanaman_modal', 'presentase_saham_nasional','presentase_saham_asing')

class PengajuanReklameForm(forms.ModelForm):
	"""docstring for PengajuanSiupForm"""
	class Meta:
		model = DetilReklame
		fields = ('jenis_reklame', 'judul_reklame', 'panjang', 'lebar', 'sisi', 'letak_pemasangan', 'desa', 'tanggal_mulai', 'tanggal_akhir')

class LegalitasPerusahaanForm(forms.ModelForm):
	"""docstring for LegalitasAktaPerusahaanForm"""
	class Meta:
		model = Legalitas
		fields = ('nama_notaris','alamat','telephone','nomor_pengesahan','tanggal_pengesahan', 'nomor_akta', 'tanggal_akta')

class LegalitasPerusahaanPerubahanForm(forms.ModelForm):
	"""docstring for LegalitasAktaPerubahanPerusahaanForm"""
	# nama_notaris_perubahan = forms.CharField(initial='nama_notaris_perubahan')
	# alamat_notaris_perubahan = forms.CharField(initial='alamat_notaris_perubahan')
	# telephone_notaris_perubahan = forms.CharField(initial='telephone_notaris_perubahan')
	# nomor_akta_perubahan = forms.CharField(initial='nomor_akta_perubahan')
	# tanggal_akta_perubahan = forms.DateField(input_formats=['%d-%m-%Y'])
	# nomor_pengesahan_perubahan = forms.CharField(initial='nomor_pengesahan_perubahan')
	# tanggal_pengesahan_perubahan = forms.DateField(input_formats=['%d-%m-%Y'])

	class Meta:
		model = Legalitas
		fields = ('nama_notaris','alamat','telephone','nomor_pengesahan', 'tanggal_pengesahan')


class UploadBerkasFotoForm(forms.ModelForm):
	"""docstring for UploadBerkasFotoForm"""
	class Meta:
		model = Berkas
		fields = ('berkas',)

class UploadBerkasKTPForm(forms.ModelForm):
	"""docstring for UploadBerkasKTPForm"""
	class Meta:
		model = Berkas
		fields = ('berkas',)

class UploadBerkasNPWPPribadiForm(forms.ModelForm):
	"""docstring for UploadBerkasNPWPPribadiForm"""
	class Meta:
		model = Berkas
		fields = ('berkas',)

class UploadBerkasNPWPPerusahaanForm(forms.ModelForm):
	"""docstring for UploadBerkasNPWPPerusahaanForm"""
	class Meta:
		model = Berkas
		fields = ('berkas',)

class UploadBerkasAktaPendirianForm(forms.ModelForm):
	"""docstring for UploadBerkasAktaPendirianForm"""
	class Meta:
		model = Berkas
		fields = ('berkas',)

class UploadBerkasAktaPerubahanForm(forms.ModelForm):
	"""docstring for UploadBerkasAktaPerubahanForm"""
	class Meta:
		model = Berkas
		fields = ('berkas',)
		
class UploadBerkasPendukungForm(forms.ModelForm):
	"""docstring for UploadBerkasPendukungForm"""
	class Meta:
		model = Berkas
		fields = ('berkas',)

class UploadBerkasPenolakanIzinForm(forms.ModelForm):
	"""docstring for UploadBerkasPendukungForm"""
	class Meta:
		model = Berkas
		fields = ('berkas',)
