from django import forms
from izin_dinkes.models import Apotek, TokoObat, Laboratorium, PeralatanLaboratorium, Optikal, MendirikanKlinik, OperasionalKlinik, PenutupanApotek
class ApotekForm(forms.ModelForm):
	class Meta:
		model = Apotek
		fields = ('nama_apotek', 'no_stra', 'no_sipa', 'alamat_apotek', 'desa', 'no_telepon', 'sarana', 'nama_pemilik_sarana', 'alamat_sarana', 'npwp')

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

class OptikalForm(forms.ModelForm):
	class Meta:
		model = Optikal
		fields = ('nama_optikal', 'nama_pemilik_perusahaan', 'jenis_badan_usaha', 'alamat_usaha', 'no_telepon', 'jenis_kegiatan_usaha', 'lokasi_kegiatan_usaha', 'luas_tanah_bangunan')

class MendirikanKlinikForm(forms.ModelForm):
	class Meta:
		model = MendirikanKlinik
		fields = ('nama_klinik', 'alamat_klinik', 'desa', 'no_telepon')

class OperasionalKlinikForm(forms.ModelForm):
	class Meta:
		model = OperasionalKlinik
		fields = ('nama_klinik', 'alamat_klinik', 'desa', 'no_telepon')

class PenutupanApotekForm(forms.ModelForm):
	class Meta:
		model = PenutupanApotek
		fields = ('nama_apotek', 'alamat_apotek', 'no_telepon', 'no_sia', 'nama_pemilik_sarana', 'alamat_sarana')