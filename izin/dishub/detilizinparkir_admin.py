# from django.contrib import admin
# from django.http import HttpResponse
# from django.utils.safestring import mark_safe
# from django.shortcuts import get_object_or_404
# from django.template import RequestContext, loader
# from accounts.models import NomorIdentitasPengguna
# from kepegawaian.models import Pegawai, UnitKerja
# from izin.models import DetilIzinParkirIsidentil , Syarat, SKIzin, Riwayat, Survey, DetilSk

# class DetilIzinParkirIsidentilAdmin(admin.ModelAdmin):
# 	def view_pengajuan_izin_parkir(self, request, id_pengajuan_izin_):
# 		extra_context = {}
# 		if id_pengajuan_izin_:
# 			extra_context.update({'title': 'Proses Pengajuan'})
# 			pengajuan_ = DetilIzinParkirIsidentil.objects.get_object_or_404(id=id_pengajuan_izin_)
# 			alamat_ = ""
# 			alamat_perusahaan_ = ""
# 			if pengajuan_.pemohon:
# 				if pengajuan_.pemohon.desa:
# 					alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.pemohon.desa.kecamatan.kabupaten.nama_kabupaten.title())
# 					extra_context.update({'alamat_pemohon': alamat_})
# 				extra_context.update({'pemohon': pengajuan_.pemohon})
# 				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
# 				nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all().last()
# 				extra_context.update({'nomor_identitas': nomor_identitas_ })
# 				try:
# 					try:
# 						ktp_ = NomorIdentitasPengguna.objects.get(user_id=pengajuan_.pemohon.id)
# 					except MultipleObjectsReturned:
# 						ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id).order_by('id').first()
# 					extra_context.update({'cookie_file_ktp': ktp_.berkas })
# 				except ObjectDoesNotExist:
# 					pass
# 			if pengajuan_.perusahaan:
# 				if pengajuan_.perusahaan.desa:
# 					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
# 					extra_context.update({'alamat_perusahaan': alamat_perusahaan_ })
# 				extra_context.update({'perusahaan': pengajuan_.perusahaan})

# 				legalitas_pendirian = pengajuan_.perusahaan.legalitas_set.filter(berkas__keterangan="akta pendirian").last()
# 				legalitas_perubahan = pengajuan_.perusahaan.legalitas_set.filter(berkas__keterangan="akta perubahan").last()
# 				legalitas_list = pengajuan_.perusahaan.legalitas_set.all()
# 				extra_context.update({ 'legalitas_pendirian': legalitas_pendirian, 'legalitas_perubahan': legalitas_perubahan, 'legalitas_list': legalitas_list })
# 			rincian = pengajuan_.rincian_sub_jenis
# 			pengajuan_id = pengajuan_.id
# 			lokasi_usaha_pariwisata = ''
# 			if pengajuan_.lokasi_usaha_pariwisata:
# 				lokasi_usaha_pariwisata = str(pengajuan_.lokasi_usaha_pariwisata) + ', Ds. ' +str(pengajuan_.desa_lokasi)+', Kec. '+str(pengajuan_.desa_lokasi.kecamatan)+', '+str(pengajuan_.desa_lokasi.kecamatan.kabupaten)+', Prov. '+str(pengajuan_.desa_lokasi.kecamatan.kabupaten.provinsi)
# 			extra_context.update({'pengajuan': pengajuan_, 'rincian': rincian, 'status': pengajuan_.status, 'created_at': pengajuan_.created_at, 'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin, 'lokasi_usaha_pariwisata': lokasi_usaha_pariwisata})

# 			# UNTUK SURVEY
# 			from django.contrib.auth.models import Group

# 			extra_context.update({'skpd_list' : UnitKerja.objects.all() })

# 			h = Group.objects.filter(name="Cek Lokasi")
# 			if h.exists():
# 				h = h.last()
# 			h = h.user_set.all()
# 			extra_context.update({'pegawai_list' : h })

# 			try:
# 				try:
# 					s = Survey.objects.get(pengajuan=pengajuan_)
# 				except Survey.MultipleObjectsReturned:
# 					s = Survey.objects.filter(pengajuan=pengajuan_).last()
# 					# print s.survey_iujk.all()
# 				print s.survey_reklame_ho.all()
# 				extra_context.update({'detilbap': s.survey_reklame_ho.all().last() })
# 			except ObjectDoesNotExist:
# 				s = ''

# 			extra_context.update({'survey': s })
# 			# END UNTUK SURVEY

# 			extra_context.update({'pengajuan_id': pengajuan_id })
# 			#+++++++++++++ page logout ++++++++++
# 			extra_context.update({'has_permission': True })
# 			#+++++++++++++ end page logout ++++++++++

# 			# lama_pemasangan = pengajuan_.tanggal_akhir-pengajuan_.tanggal_mulai
# 			# print lama_pemasangan
# 			# banyak = len(DetilTDUP.objects.all())
# 			# extra_context.update({'banyak': banyak})
# 			syarat_ = Syarat.objects.filter(jenis_izin__jenis_izin__kode="reklame")
# 			extra_context.update({'syarat': syarat_})
# 			try:
# 				skizin_ = SKIzin.objects.get(pengajuan_izin_id = id_pengajuan_izin_ )
# 				if skizin_:
# 					extra_context.update({'skizin': skizin_ })
# 					extra_context.update({'skizin_status': skizin_.status })
# 			except ObjectDoesNotExist:
# 				pass
# 			try:
# 				riwayat_ = Riwayat.objects.filter(pengajuan_izin_id = id_pengajuan_izin_).order_by('created_at')
# 				if riwayat_:
# 					extra_context.update({'riwayat': riwayat_ })
# 			except ObjectDoesNotExist:
# 				pass
# 		template = loader.get_template("admin/izin/pengajuanizin/dishub/view_izin_parkir.html")
# 		ec = RequestContext(request, extra_context)
# 		return HttpResponse(template.render(ec))

# 		def get_urls(self):
# 			from django.conf.urls import patterns, url
# 			urls = super(DetilIzinParkirIsidentilAdmin, self).get_urls()
# 			my_urls = patterns('',
# 				url(r'^parkir/$', self.admin_site.admin_view(self.view_pengajuan_izin_parkir), name='view_pengajuan_izin_parkir'),
# 				# url(r'^cetak-tdup-asli/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.cetak_tdup_asli), name='cetak_tdup_asli'),
# 				# url(r'^option-jenis-usaha/$', self.option_jenis_usaha, name='option_jenis_usaha'),
# 				# url(r'^option-sub-jenis-usaha/$', self.option_sub_jenis_usaha, name='option_sub_jenis_usaha'),
# 				# url(r'^ajax-save-izin-lain/$', self.ajax_save_izin_lain, name='ajax_save_izin_lain'),
# 				# url(r'^load-izin-lain/(?P<pengajuan_id>[0-9]+)$', self.load_izin_lain, name='load_izin_lain'),
# 				)
# 		return my_urls + urls

# admin.site.register(DetilIzinParkirIsidentil, DetilIzinParkirIsidentilAdmin)