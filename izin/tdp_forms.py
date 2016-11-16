from django import forms
from izin.models import DetilTDP, RincianPerusahaan
from perusahaan.models import Legalitas

class DataUmumPerusahaanPTForm(forms.ModelForm):
	class Meta:
		model = DetilTDP
		fields = ('status_perusahaan', 'jenis_badan_usaha', 'bentuk_kerjasama', 'jumlah_bank', 'nasabah_utama_bank_1', 'nasabah_utama_bank_2', 'jenis_penanaman_modal', 'tanggal_pendirian', 'tanggal_mulai_kegiatan', 'merek_dagang', 'no_merek_dagang', 'pemegang_hak_cipta', 'no_hak_cipta', 'pemegang_hak_paten' , 'no_hak_paten')

# class DataUmumPerusahaanPTKantorCabangForm(forms.ModelForm):
# 	class Meta:
# 		model = DetilTDP
# 		fields = ('')

class DataKegiatanPTForm(forms.ModelForm):
	class Meta:
		model = DetilTDP
		fields = ('kegiatan_usaha_pokok', 'kegiatan_usaha_lain_1', 'kegiatan_usaha_lain_2', 'komoditi_produk_pokok', 'komoditi_produk_lain_1', 'komoditi_produk_lain_2', 'omset_per_tahun', 'total_aset', 'jumlah_karyawan_wni', 'jumlah_karyawan_wna', 'kapasitas_mesin_terpasang', 'satuan_kapasitas_mesin_terpasang', 'kapasitas_produksi_per_tahun', 'satuan_kapasitas_produksi_per_tahun', 'prosentase_kandungan_produk_lokal', 'prosentase_kandungan_produk_import', 'jenis_pengecer', 'kedudukan_kegiatan_usaha', 'jenis_perusahaan') 

class RincianPerusahaanForm(forms.ModelForm):
	class Meta:
		model = RincianPerusahaan
		fields = ('model_dasar', 'model_ditempatkan', 'model_disetor', 'banyaknya_saham', 'nilai_nominal_per_saham')

class LegalitasForm(forms.ModelForm):
	class Meta:
		model = Legalitas
		fields = ('nama_notaris', 'alamat', 'telephone', 'nomor_pengesahan', 'tanggal_pengesahan' )