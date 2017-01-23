from django import forms
from izin.models import DetilTDP, IzinLain
from perusahaan.models import Legalitas, DataPimpinan, PemegangSaham, Perusahaan
from master.models import Berkas

class DataUmumPerusahaanPTForm(forms.ModelForm):
	class Meta:
		model = DetilTDP
		fields = ('status_perusahaan', 'bentuk_kerjasama', 'jumlah_bank', 'nasabah_utama_bank_1', 'nasabah_utama_bank_2', 'jenis_penanaman_modal', 'tanggal_pendirian', 'tanggal_mulai_kegiatan', 'jangka_waktu_berdiri', 'merek_dagang', 'no_merek_dagang', 'pemegang_hak_cipta', 'no_hak_cipta', 'pemegang_hak_paten' , 'no_hak_paten')

class DataKegiatanPTForm(forms.ModelForm):
	class Meta:
		model = DetilTDP
		fields = ('kegiatan_usaha_pokok', 'omset_per_tahun', 'total_aset', 'jumlah_karyawan_wni', 'jumlah_karyawan_wna', 'kapasitas_mesin_terpasang', 'satuan_kapasitas_mesin_terpasang', 'kapasitas_produksi_per_tahun', 'satuan_kapasitas_produksi_per_tahun', 'presentase_kandungan_produk_lokal', 'presentase_kandungan_produk_import', 'jenis_pengecer', 'kedudukan_kegiatan_usaha', 'jenis_perusahaan') 

class LegalitasForm(forms.ModelForm):
	class Meta:
		model = Legalitas
		fields = ('nama_notaris', 'alamat', 'telephone', 'nomor_pengesahan', 'tanggal_pengesahan' )

class DataPimpinanForm(forms.ModelForm):
	class Meta:
		model = DataPimpinan
		fields = ('kedudukan', 'nama_lengkap', 'tempat_lahir', 'tanggal_lahir', 'alamat', 'telephone', 'hp', 'email', 'kewarganegaraan', 'tanggal_menduduki_jabatan', 'jumlah_saham_dimiliki', 'jumlah_saham_disetor', 'kedudukan_diperusahaan_lain', 'nama_perusahaan_lain', 'alamat_perusahaan_lain', 'kode_pos_perusahaan_lain', 'telepon_perusahaan_lain', 'tanggal_menduduki_jabatan_perusahaan_lain')

	def clean_email(self):
		return self.cleaned_data['email'] or None

class PemegangSahamForm(forms.ModelForm):
	class Meta:
		model = PemegangSaham
		fields = ('nama_lengkap', 'alamat', 'telephone', 'kewarganegaraan', 'npwp', 'jumlah_saham_dimiliki', 'jumlah_saham_disetor')

class IzinLainForm(forms.ModelForm):
	class Meta:
		model = IzinLain
		fields = ('kelompok_jenis_izin', 'no_izin', 'dikeluarkan_oleh', 'tanggal_dikeluarkan', 'masa_berlaku')

class PerusahaanCabangForm(forms.ModelForm):

	class Meta:
		model = Perusahaan
		fields = ('nomor_tdp', 'nama_perusahaan', 'alamat_perusahaan', 'desa', 'kode_pos', 'telepon', 'fax', 'status_perusahaan', 'kegiatan_usaha')

class BerkasForm(forms.ModelForm):
	class Meta:
		model = Berkas
		fields = ('berkas',)

class RincianPerusahaanForm(forms.ModelForm):
	class Meta:
		model = DetilTDP
		fields = ('modal_dasar', 'modal_ditempatkan', 'modal_disetor', 'banyaknya_saham', 'nilai_nominal_per_saham')

class RincianKoperasiForm(forms.ModelForm):
	class Meta:
		model = DetilTDP
		fields = ('modal_sendiri_simpanan_pokok', 'modal_sendiri_simpanan_wajib', 'modal_sendiri_dana_cadangan', 'modal_sendiri_hibah', 'modal_pinjaman_anggota', 'modal_pinjaman_koperasi_lain', 'modal_pinjaman_bank', 'modal_pinjaman_lainnya', 'jumlah_anggota', 'jenis_koperasi', 'bentuk_koperasi')