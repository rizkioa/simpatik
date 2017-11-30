from django import forms
from izin_dinkes.models import Apotek, TokoObat, Laboratorium, PeralatanLaboratorium

class ApotekForm(forms.ModelForm):
	class Meta:
		model = Apotek
		fields = ('nama_apotek', 'alamat_apotek', 'desa', 'no_telepon', 'sarana', 'nama_pemilik_sarana', 'alamat_sarana', 'npwp')

class TokoObatForm(forms.ModelForm):
	class Meta:
		models = TokoObat
		fields = ('nama_toko_obat', 'nama_ttk_penanggung_jawab', 'alamat_ttk', 'alamat_tempat_usaha')

class LaboratoriumForm(forms.ModelForm):
	class Meta:
		models = Laboratorium
		fields = ('klasifikasi_laboratorium', 'nama_laboratorium', 'alamat_laboratorium', 'penanggung_jawab_teknis')

class PeralatanLaboratoriumForm(forms.ModelForm):
	class Meta:
		models = PeralatanLaboratorium
		fields = ('jenis_peralatan', 'jumlah', 'keterangan')