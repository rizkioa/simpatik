from django import forms
from izin.models import DetilIzinParkirIsidentil, DataAnggotaParkir

class DetilIzinParkirIsidentilForm(forms.ModelForm):
	class Meta:
		model = DetilIzinParkirIsidentil
		fields = ('jenis_penitipan', 'lebar_penitipan', 'panjang_penitipan', 'desa', 'alamat', 'tanggal_pelaksanaan_parkir', 'waktu_mulai', 'waktu_berakhir', 'jumlah_anggota_parkir', 'batas_utara', 'batas_timur', 'batas_selatan', 'batas_barat')

class DataAnggotaParkirForm(forms.ModelForm):
	class Meta:
		model = DataAnggotaParkir
		fields = ('nomor_ktp', 'nama_lengkap', 'tanggal_lahir', 'alamat', 'telephone', 'keterangan')