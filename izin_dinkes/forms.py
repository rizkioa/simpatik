from django import forms
from izin.utils import JENIS_IZIN
from izin_dinkes.models import Apotek
from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, Berkas
from accounts.models import NomorIdentitasPengguna
from perusahaan.models import Perusahaan, Legalitas
from ckeditor.widgets import CKEditorWidget

EMPTY_JENIS_IZIN = (('', 'Select an Option'),)+JENIS_IZIN

class ApotekForm(forms.ModelForm):
	class Meta:
		model = Apotek
		fields = ('nama_apotek', 'alamat_apotek', 'no_telepon', 'sarana', 'nama_pemilik_sarana', 'alama_sarana', 'npwp')