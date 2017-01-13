from django import forms
from izin.utils import JENIS_IZIN
from izin.models import Pemohon, KelompokJenisIzin, JenisIzin, DetilSIUP, DetilReklame, DetilIMBPapanReklame, Survey,DetilIMB,InformasiKekayaanDaerah,DetilHO,InformasiTanah,DetilHuller,MesinPerusahaan,MesinHuller,PenggunaanTanahIPPTUsaha,PerumahanYangDimilikiIPPTUsaha
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
		fields = ( 'jenis_pemohon', 'nama_lengkap', 'tempat_lahir', 'alamat','tanggal_lahir','telephone','hp','kewarganegaraan','desa','email','pekerjaan', 'status')

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
		fields = ('jenis_reklame', 'judul_reklame', 'panjang', 'lebar', 'sisi','jumlah', 'letak_pemasangan', 'desa', 'tanggal_mulai', 'tanggal_akhir')

class LegalitasPerusahaanForm(forms.ModelForm):
	"""docstring for LegalitasAktaPerusahaanForm"""
	class Meta:
		model = Legalitas
		fields = ('nama_notaris','alamat','telephone', 'nomor_pengesahan','tanggal_pengesahan', 'nomor_akta', 'tanggal_akta')

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


class SurveyForm(forms.ModelForm):
	class Meta:
		model = Survey
		fields = ('deadline_survey',)

class PengajuanIMBReklameForm(forms.ModelForm):
	"""docstring for PengajuanSiupForm"""
	class Meta:
		model = DetilIMBPapanReklame
		fields = ('jenis_papan_reklame','lebar','tinggi','jumlah','klasifikasi_jalan','lokasi_pasang','desa','batas_utara','batas_timur','batas_selatan','batas_barat')

class DetilIMBForm(forms.ModelForm):

	class Meta:
		model = DetilIMB
		fields = ('bangunan','luas_bangunan','jumlah_bangunan','luas_tanah','no_surat_tanah','tanggal_surat_tanah','lokasi','desa','status_hak_tanah','kepemilikan_tanah','luas_bangunan_lama','no_imb_lama','tanggal_imb_lama')

class ParameterBangunanForm(forms.ModelForm):
	"""docstring for UploadBerkasPendukungForm"""
	class Meta:
		model = DetilIMB
		fields = ('parameter_bangunan','total_biaya')

class IdentifikasiJalanForm(forms.ModelForm):
	"""docstring for UploadBerkasPendukungForm"""
	class Meta:
		model = DetilIMB
		fields = ('klasifikasi_jalan','ruang_milik_jalan','ruang_pengawasan_jalan')

class InformasiKekayaanDaerahForm(forms.ModelForm):
	class Meta:
		model = InformasiKekayaanDaerah
		fields = ('lokasi','desa','lebar','panjang','penggunaan')

class DetilHOForm(forms.ModelForm):
	class Meta:
		model = DetilHO
		fields = ('perkiraan_modal','tujuan_gangguan','alamat','desa','bahan_baku_dan_penolong','proses_produksi','jenis_produksi','kapasitas_produksi','jumlah_tenaga_kerja','jumlah_mesin','merk_mesin','daya','kekuatan','luas_ruang_tempat_usaha','luas_lahan_usaha','jenis_lokasi_usaha','jenis_bangunan','jenis_gangguan')

class InformasiTanahForm(forms.ModelForm):
	"""docstring for InformasiTanahForm"""
	class Meta:
		model = InformasiTanah
		fields = ('no_surat_kuasa','tanggal_surat_kuasa','alamat','desa','luas','status_tanah','no_sertifikat_petak','luas_sertifikat_petak','atas_nama_sertifikat_petak','no_persil','klas_persil','atas_nama_persil','penggunaan_sekarang','rencana_penggunaan')

class DetilHullerForm(forms.ModelForm):
	"""docstring for DetilHullerForm"""
	class Meta:
		model = DetilHuller
		fields = ('pemilik_badan_usaha','pemilik_nama_perorangan','pemilik_alamat','pemilik_desa','pemilik_kewarganegaraan','pemilik_nama_badan_usaha','hubungan_pemilik_pengusaha','pengusaha_badan_usaha','pengusaha_nama_perorangan','pengusaha_alamat','pengusaha_desa','pengusaha_kewarganegaraan','pengusaha_nama_badan_usaha')
class DeilHllerKapaSitasPotensialForm(forms.ModelForm):
	"""docstring for DeilHllerKapaSitasPotensialForm"""
	class Meta:
		model = DetilHuller
		fields = ('kapasitas_potensial_giling_beras_per_jam','kapasitas_potensial_giling_beras_per_tahun')
		
class MesinHullerForm(forms.ModelForm):
	"""docstring for MesinHullerForm"""
	class Meta:
		model = MesinHuller
		fields = ('jenis_mesin','mesin_huller','keterangan')

class MesinPerusahaanForm(forms.ModelForm):
	"""docstring for MesinPerusahaanForm"""
	detil_huller = forms.ModelChoiceField(label="Detil Huller", queryset=DetilHuller.objects.none(), required=False )
	mesin_huller = forms.ModelChoiceField(label="Mesin Huller", queryset=MesinHuller.objects.none(), required=False )
	class Meta:
		model = MesinPerusahaan
		fields = ('detil_huller','mesin_huller','type_model','pk_mesin','buatan','jumlah_unit','kapasitas')
		
class InformasiTanahIPPTUsahaForm(forms.ModelForm):
	"""docstring for InformasiTanahIPPTUsahaForm"""
	class Meta:
		model = InformasiTanah
		fields = ('no_surat_kuasa','tanggal_surat_kuasa','alamat','desa','luas','status_tanah','no_sertifikat_petak','luas_sertifikat_petak','atas_nama_sertifikat_petak','no_persil','klas_persil','atas_nama_persil','rencana_penggunaan','batas_utara','batas_timur','batas_selatan','batas_barat','tanah_negara_belum_dikuasai','tanah_kas_desa_belum_dikuasai','tanah_hak_pakai_belum_dikuasai','tanah_hak_guna_bangunan_belum_dikuasai','tanah_hak_milik_sertifikat_belum_dikuasai','tanah_adat_belum_dikuasai','pemegang_hak_semula_dari_tanah_belum_dikuasai','tanah_belum_dikuasai_melalui','tanah_negara_sudah_dikuasai','tanah_kas_desa_sudah_dikuasai','tanah_hak_pakai_sudah_dikuasai','tanah_hak_guna_bangunan_sudah_dikuasai','tanah_hak_milik_sertifikat_sudah_dikuasai','tanah_adat_sudah_dikuasai','pemegang_hak_semula_dari_tanah_sudah_dikuasai','tanah_sudah_dikuasai_melalui','jumlah_tanah_belum_dikuasai','jumlah_tanah_sudah_dikuasai')

class RencanaPembangunanIPPTUsahaForm(forms.ModelForm):
	"""docstring for RencanaPembangunanIPPTUsahaForm"""
	class Meta:
		model = InformasiTanah
		fields = ('tipe1','tipe2','tipe3','gudang1','gudang2','gudang3','luas_tipe1','luas_tipe2','luas_tipe3','luas_lapangan','luas_kantor','luas_saluran','luas_taman','pematangan_tanah_tahap1','pematangan_tanah_tahap2','pematangan_tanah_tahap3','pembangunan_gedung_tahap1','pembangunan_gedung_tahap2','pembangunan_gedung_tahap3','jangka_waktu_selesai')

class RencanaPembiayanDanPemodalanIPPTUsahaForm(forms.ModelForm):
	"""docstring for RencanaPembiayanDanPemodalanIPPTUsahaForm"""
	class Meta:
		model = InformasiTanah
		fields = ('modal_tetap_tanah','modal_tetap_bangunan','modal_tetap_mesin','modal_tetap_angkutan','modal_tetap_inventaris','modal_tetap_lainnya','modal_kerja_bahan','modal_kerja_gaji','modal_kerja_alat_angkut','modal_kerja_lainnya','modal_dasar','modal_ditetapkan','modal_disetor','modal_bank_pemerintah','modal_bank_swasta','modal_lembaga_non_bank','modal_pihak_ketiga','modal_pinjaman_luar_negeri','saham_indonesia','saham_asing')

class PenggunaanTanahIPPTUsahaForm(forms.ModelForm):
	"""docstring for PenggunaanTanahIPPTUsahaForm"""
	class Meta:
		model = PenggunaanTanahIPPTUsaha
		fields = ('nama_penggunaan','ukuran_penggunaan',)

class PerumahanYangDimilikiIPPTUsahaForm(forms.ModelForm):
	"""docstring for PerumahanYangDimilikiIPPTUsahaForm"""
	class Meta:
		model = PerumahanYangDimilikiIPPTUsaha
		fields = ('nama_perumahan','luas_tanah','status_tanah','desa')













