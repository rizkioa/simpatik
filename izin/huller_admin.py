import base64, datetime
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, resolve
from django.shortcuts import get_object_or_404
from izin.models import DetilHuller, Syarat, SKIzin, Riwayat,MesinPerusahaan,DetilSk
from kepegawaian.models import Pegawai
from accounts.models import NomorIdentitasPengguna

class DetilHullerAdmin(admin.ModelAdmin):
	list_display = ('id','get_no_pengajuan', 'pemohon', 'get_kelompok_jenis_izin','jenis_permohonan', 'status')
	search_fields = ('no_izin', 'pemohon__nama_lengkap')

	def get_kelompok_jenis_izin(self, obj):
		return obj.kelompok_jenis_izin
	get_kelompok_jenis_izin.short_description = "Izin Pengajuan"

	def get_no_pengajuan(self, obj):
		no_pengajuan = mark_safe("""
			<a href="%s" target="_blank"> %s </a>
			""" % ("#", obj.no_pengajuan ))
		split_ = obj.no_pengajuan.split('/')
		# print split_
		if split_[0] == 'ITNH':
			no_pengajuan = mark_safe("""
				<a href="%s" target="_blank"> %s </a>
				""" % (reverse('admin:izin_informasitanah_change', args=(obj.id,)), obj.no_pengajuan ))
		return no_pengajuan
	get_no_pengajuan.short_description = "No. Pengajuan"


	def get_readonly_fields(self, request, obj=None):
		rf = ('verified_by', 'verified_at', 'created_by', 'created_at', 'updated_at')
		if obj:
			if not request.user.is_superuser:
				rf = rf+('status',)
		return rf

	def get_fieldsets(self, request, obj = None):
		if obj or request.user.is_superuser:
			add_fieldsets = (
				(None, {
					'classes': ('wide',),
					'fields': ('pemohon','perusahaan',)
					}
				),
				('Detail Izin', {'fields': ('kelompok_jenis_izin', 'jenis_permohonan','no_pengajuan', 'no_izin','legalitas')}),
				('Detail Kuasa', {'fields': ('nama_kuasa','no_identitas_kuasa','telephone_kuasa',) }),
				('Detail Huller', {'fields': ('pemilik_badan_usaha','pemilik_nama_perorangan','pemilik_alamat','pemilik_desa','pemilik_kewarganegaraan','pemilik_nama_badan_usaha','pengusaha_badan_usaha','pengusaha_nama_perorangan','pengusaha_alamat','pengusaha_desa','pengusaha_kewarganegaraan','pengusaha_nama_badan_usaha','hubungan_pemilik_pengusaha','kapasitas_potensial_giling_beras_per_jam','kapasitas_potensial_giling_beras_per_tahun') }),
				('Berkas & Keterangan', {'fields': ('berkas_tambahan', 'keterangan',)}),

				('Lain-lain', {'fields': ('status', 'created_by', 'created_at', 'verified_by', 'verified_at', 'updated_at')}),
			)

		else:
			add_fieldsets = (
				(None, {
					'classes': ('wide',),
					'fields': ('pemohon','perusahaan',)
					}
				),
				('Detail Izin', {'fields': ('kelompok_jenis_izin', 'jenis_permohonan','no_pengajuan', 'no_izin','legalitas')}),
				('Detail Kuasa', {'fields': ('nama_kuasa','no_identitas_kuasa','telephone_kuasa',) }),
				('Detail Huller', {'fields': ('pemilik_badan_usaha','pemilik_nama_perorangan','pemilik_alamat','pemilik_desa','pemilik_kewarganegaraan','pemilik_nama_badan_usaha','pengusaha_badan_usaha','pengusaha_nama_perorangan','pengusaha_alamat','pengusaha_desa','pengusaha_kewarganegaraan','pengusaha_nama_badan_usaha','hubungan_pemilik_pengusaha','kapasitas_potensial_giling_beras_per_jam','kapasitas_potensial_giling_beras_per_tahun') }),
				('Berkas & Keterangan', {'fields': ('berkas_tambahan', 'keterangan',)}),
			)
		return add_fieldsets

	def view_pengajuan_huller(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			# pengajuan_ = DetilHuller.objects.get(id=id_pengajuan_izin_)
			pengajuan_ = get_object_or_404(DetilHuller, id=id_pengajuan_izin_)
			data_mesin = MesinPerusahaan.objects.filter(detil_huller=id_pengajuan_izin_)

			try:
				motor_bensin = data_mesin.get(mesin_huller__mesin_huller="Motor Bensin")
				motor_diesel = data_mesin.get(mesin_huller__mesin_huller="Motor Diesel")
				diesel_generating_set = data_mesin.get(mesin_huller__mesin_huller="Diesel Generating Set")
				rubber_roll = data_mesin.get(mesin_huller__mesin_huller="Rubber Roll / Roll Karet")
				flash_type = data_mesin.get(mesin_huller__mesin_huller="Flash Type / Type Banting")
				gedogan = data_mesin.get(mesin_huller__mesin_huller="Gedogan")
				dimple_plate = data_mesin.get(mesin_huller__mesin_huller="Dimple Plate")
				screen = data_mesin.get(mesin_huller__mesin_huller="Screen")
				mesin_slip_horisontal = data_mesin.get(mesin_huller__mesin_huller="Mesin Slip Horizontal")
				mesin_slip_vertikal = data_mesin.get(mesin_huller__mesin_huller="Mesin Slip Vertikal")
				paddy_cleaner = data_mesin.get(mesin_huller__mesin_huller="Paddy Cleaner / Pembersih Gabah (Blower)")
				mesin_polis = data_mesin.get(mesin_huller__mesin_huller="Mesin Polis Brushe")
				grader = data_mesin.get(mesin_huller__mesin_huller="Grader / Mesin Pemisah")
				kualitas = data_mesin.get(mesin_huller__mesin_huller="Kualitas")
			except ObjectDoesNotExist:
				motor_bensin = ""
				motor_diesel = ""
				diesel_generating_set = ""
				rubber_roll = ""
				flash_type = ""
				gedogan = ""
				dimple_plate = ""
				screen = ""
				mesin_slip_horisontal = ""
				mesin_slip_vertikal = ""
				paddy_cleaner = ""
				mesin_polis = ""
				grader = ""
				kualitas = ""

				alamat_ = ""
				alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.pemohon.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
				nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all().last()
				extra_context.update({'nomor_identitas': nomor_identitas_ })
				nomor = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id)
				if nomor.exists():
					nomor = nomor.filter(jenis_identitas_id=1)
					if nomor.exists():
						ktp_ = nomor.last()
						extra_context.update({'cookie_file_ktp': ktp_.berkas })
				# try:
				# 	ktp_ = NomorIdentitasPengguna.objects.get(user_id=pengajuan_.pemohon.id)
				# 	extra_context.update({'cookie_file_ktp': ktp_.berkas })
				# except ObjectDoesNotExist:
				# 	pass
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({'alamat_perusahaan': alamat_perusahaan_ })
				extra_context.update({'perusahaan': pengajuan_.perusahaan})

				legalitas_pendirian = pengajuan_.perusahaan.legalitas_set.filter(berkas__keterangan="akta pendirian").last()
				legalitas_perubahan = pengajuan_.perusahaan.legalitas_set.filter(berkas__keterangan="akta perubahan").last()
				extra_context.update({ 'legalitas_pendirian': legalitas_pendirian })
				extra_context.update({ 'legalitas_perubahan': legalitas_perubahan })
					

			extra_context.update({ 'motor_bensin': motor_bensin })
			extra_context.update({ 'motor_diesel': motor_diesel })
			extra_context.update({ 'diesel_generating_set': diesel_generating_set })
			extra_context.update({ 'rubber_roll': rubber_roll })
			extra_context.update({ 'flash_type': flash_type })
			extra_context.update({ 'gedogan': gedogan })
			extra_context.update({ 'dimple_plate': dimple_plate })
			extra_context.update({ 'screen': screen })
			extra_context.update({ 'mesin_slip_horisontal': mesin_slip_horisontal })
			extra_context.update({ 'mesin_slip_vertikal': mesin_slip_vertikal })
			extra_context.update({ 'paddy_cleaner': paddy_cleaner })
			extra_context.update({ 'mesin_polis': mesin_polis })
			extra_context.update({ 'grader': grader })
			extra_context.update({ 'kualitas': kualitas })

			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})
			extra_context.update({'status': pengajuan_.status})
			extra_context.update({'pengajuan': pengajuan_})
			encode_pengajuan_id = (str(pengajuan_.id))
			extra_context.update({'pengajuan_id': encode_pengajuan_id})
			#+++++++++++++ page logout ++++++++++
			extra_context.update({'has_permission': True })
			#+++++++++++++ end page logout ++++++++++

			banyak = len(DetilHuller.objects.all())
			extra_context.update({'banyak': banyak})
			syarat_ = Syarat.objects.filter(jenis_izin__jenis_izin__kode="reklame")
			extra_context.update({'syarat': syarat_})
			try:
				skizin_ = SKIzin.objects.get(pengajuan_izin_id = id_pengajuan_izin_ )
				if skizin_:
					extra_context.update({'skizin': skizin_ })
					extra_context.update({'skizin_status': skizin_.status })
			except ObjectDoesNotExist:
				pass
			try:
				riwayat_ = Riwayat.objects.filter(pengajuan_izin_id = id_pengajuan_izin_).order_by('created_at')
				if riwayat_:
					extra_context.update({'riwayat': riwayat_ })
			except ObjectDoesNotExist:
				pass
		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_huller.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_sk_izin_huller(self, request, id_pengajuan_izin_, salinan_=None):
		extra_context = {}
		# id_pengajuan_izin_ = base64.b64decode(id_pengajuan_izin_)
		# print id_pengajuan_izin_
		if id_pengajuan_izin_:
			extra_context.update({'salinan': salinan_})
			pengajuan_ = DetilHuller.objects.get(id=id_pengajuan_izin_)
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})

			nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
			extra_context.update({'nomor_identitas': nomor_identitas_ })
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'pengajuan': pengajuan_ })
			extra_context.update({'foto': pengajuan_.pemohon.berkas_foto.all().last()})
			try:
				skizin_ = SKIzin.objects.get(pengajuan_izin_id = id_pengajuan_izin_ )
				if skizin_:
					extra_context.update({'skizin': skizin_ })
					extra_context.update({'skizin_status': skizin_.status })
			except ObjectDoesNotExist:
				pass
			try:
				kepala_ =  Pegawai.objects.get(jabatan__nama_jabatan="Kepala Dinas")
				if kepala_:
					extra_context.update({'gelar_depan': kepala_.gelar_depan })
					extra_context.update({'nama_kepala_dinas': kepala_.nama_lengkap })
					extra_context.update({'nip_kepala_dinas': kepala_.nomoridentitaspengguna_set.last() })

			except ObjectDoesNotExist:
				pass
			try:
				sk_imb_ = DetilSk.objects.get(pengajuan_izin__id = id_pengajuan_izin_ )
				if sk_imb_:
					extra_context.update({'sk_imb': sk_imb_ })
			except ObjectDoesNotExist:
				pass

			try:
				data_mesin = MesinPerusahaan.objects.filter(detil_huller=id_pengajuan_izin_)
				motor_bensin = data_mesin.get(mesin_huller__mesin_huller="Motor Bensin")
				motor_diesel = data_mesin.get(mesin_huller__mesin_huller="Motor Diesel")
				diesel_generating_set = data_mesin.get(mesin_huller__mesin_huller="Diesel Generating Set")
				rubber_roll = data_mesin.get(mesin_huller__mesin_huller="Rubber Roll / Roll Karet")
				flash_type = data_mesin.get(mesin_huller__mesin_huller="Flash Type / Type Banting")
				gedogan = data_mesin.get(mesin_huller__mesin_huller="Gedogan")
				dimple_plate = data_mesin.get(mesin_huller__mesin_huller="Dimple Plate")
				screen = data_mesin.get(mesin_huller__mesin_huller="Screen")
				mesin_slip_horisontal = data_mesin.get(mesin_huller__mesin_huller="Mesin Slip Horizontal")
				mesin_slip_vertikal = data_mesin.get(mesin_huller__mesin_huller="Mesin Slip Vertikal")
				paddy_cleaner = data_mesin.get(mesin_huller__mesin_huller="Paddy Cleaner / Pembersih Gabah (Blower)")
				mesin_polis = data_mesin.get(mesin_huller__mesin_huller="Mesin Polis Brushe")
				grader = data_mesin.get(mesin_huller__mesin_huller="Grader / Mesin Pemisah")
				kualitas = data_mesin.get(mesin_huller__mesin_huller="Kualitas")
				
				extra_context.update({'data_mesin': data_mesin })
				extra_context.update({'motor_bensin': motor_bensin })
				extra_context.update({'motor_diesel': motor_diesel })
				extra_context.update({'diesel_generating_set': diesel_generating_set })
				extra_context.update({'rubber_roll': rubber_roll })
				extra_context.update({'flash_type': flash_type })
				extra_context.update({'gedogan': gedogan })
				extra_context.update({'dimple_plate': dimple_plate })
				extra_context.update({'screen': screen })
				extra_context.update({'mesin_slip_horisontal': mesin_slip_horisontal })
				extra_context.update({'mesin_slip_vertikal': mesin_slip_vertikal })
				extra_context.update({'paddy_cleaner': paddy_cleaner })
				extra_context.update({'mesin_polis': mesin_polis })
				extra_context.update({'grader': grader })
				extra_context.update({'kualitas': kualitas })
			except ObjectDoesNotExist:
				pass
			# try:
			# 	retribusi_ = DetilPembayaran.objects.get(pengajuan_izin__id = id_pengajuan_izin_)
			# 	if retribusi_:
			# 		n = int(retribusi_.jumlah_pembayaran.replace(".", ""))
			# 		terbilang_ = terbilang(n)
			# 		extra_context.update({'retribusi': retribusi_ })
			# 		extra_context.update({'terbilang': terbilang_ })
			# except ObjectDoesNotExist:
			# 	pass
		template = loader.get_template("front-end/include/formulir_huller/cetak_sk_izin_huller.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilHullerAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^cetak-sk-izin-huller/(?P<id_pengajuan_izin_>[0-9]+)/$', self.admin_site.admin_view(self.cetak_sk_izin_huller), name='cetak_sk_izin_huller'),
			url(r'^cetak-sk-izin-huller/(?P<id_pengajuan_izin_>[0-9]+)/(?P<salinan_>\w+)$', self.admin_site.admin_view(self.cetak_sk_izin_huller), name='cetak_sk_izin_huller'),
			url(r'^view-pengajuan-penggilingan-padi-huller/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_huller), name='view_pengajuan_huller'),
			# url(r'^cetak-bukti-pendaftaran-admin/(?P<id_pengajuan_izin_>[0-9]+)/$', self.admin_site.admin_view(self.cetak_bukti_admin_reklame), name='cetak_bukti_admin_reklame'),
			)
		return my_urls + urls

admin.site.register(DetilHuller, DetilHullerAdmin)