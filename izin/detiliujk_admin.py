from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from izin.models import DetilIUJK, SKIzin, Riwayat, Syarat, Survey, Klasifikasi, Subklasifikasi
from izin.utils import formatrupiah, JENIS_PERMOHONAN
from accounts.models import NomorIdentitasPengguna
from kepegawaian.models import UnitKerja, Pegawai


class DetilIUJKAdmin(admin.ModelAdmin):

	
	
	def view_pengajuan_iujk(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			extra_context.update({'skpd_list' : UnitKerja.objects.all() })
			h = Group.objects.filter(name="Cek Lokasi")
			if h.exists():
				h = h.last()
			h = h.user_set.all()
			extra_context.update({'pegawai_list' : h })

			g = Group.objects.filter(name="Tim Teknis")
			if g.exists():
				g = g.last()
			p = g.user_set.all()
			extra_context.update({'pegawai_all' : p })
			extra_context.update({'jenis_permohonan' : JENIS_PERMOHONAN })
			pengajuan_ = DetilIUJK.objects.get(id=id_pengajuan_izin_)

			extra_context.update({'survey_pengajuan' : pengajuan_.survey_pengajuan.all().last() })

			queryset_ = Survey.objects.filter(pengajuan__id=id_pengajuan_izin_)
			if queryset_.exists():
				queryset_ = queryset_.last()
				detilbap = queryset_.survey_detilbap.all()
				if detilbap.exists():
					detil = detilbap.last()
					extra_context.update({'detilbap': detil })
					data_bap = {
						'bangunan_kantor': detil.bangunan_kantor,
						'ruang_direktur': detil.ruang_direktur,
						'ruang_staf': detil.ruang_staf,
						'ruang_meja_kursi_derektur': detil.ruang_meja_kursi_derektur,
						'ruang_meja_kursi_staff_administrasi': detil.ruang_meja_kursi_staff_administrasi,
						'ruang_meja_kursi_staff_teknis': detil.ruang_meja_kursi_staff_teknis,
						'komputer': detil.komputer,
						'lemari': detil.lemari,
						'papan_nama_klasifikasi_k1_k2': detil.papan_nama_klasifikasi_k1_k2,
						'papan_nama_klasifikasi_mb': detil.papan_nama_klasifikasi_mb,
						'papan_nama_ada_nama_perusahaan': detil.papan_nama_ada_nama_perusahaan,
						'papan_nama_ada_telp': detil.papan_nama_ada_telp,
						'papan_nama_ada_alamat': detil.papan_nama_ada_alamat,
						'papan_nama_ada_npwp': detil.papan_nama_ada_npwp,
						'papan_nama_ada_nama_anggota_asosiasi': detil.papan_nama_ada_nama_anggota_asosiasi
						}
				
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
				nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
				ktp_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(jenis_identitas_id=1).last()
				paspor_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(jenis_identitas_id=2).last()
				extra_context.update({'ktp': ktp_ })
				extra_context.update({'paspor': paspor_ })
				extra_context.update({'nomor_identitas': nomor_identitas_ })
				try:
					ktp_ = NomorIdentitasPengguna.objects.get(user_id=pengajuan_.pemohon.id, jenis_identitas__id=1)
					extra_context.update({'cookie_file_ktp': ktp_.berkas })
				except ObjectDoesNotExist:
					pass
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_perusahaan': alamat_perusahaan_ })
				extra_context.update({'perusahaan': pengajuan_.perusahaan})
				legalitas_pendirian = pengajuan_.legalitas.filter(~Q(jenis_legalitas_id=2)).last()
				legalitas_perubahan = pengajuan_.legalitas.filter(jenis_legalitas_id=2).last()
				extra_context.update({ 'legalitas_pendirian': legalitas_pendirian })
				extra_context.update({ 'legalitas_perubahan': legalitas_perubahan })

			# if pengajuan_.status == 8:
			try:
				try:
					s = Survey.objects.get(pengajuan=pengajuan_)
				except Survey.MultipleObjectsReturned:
					s = Survey.objects.filter(pengajuan=pengajuan_).last()
					print s.survey_iujk.all()
			except ObjectDoesNotExist:
				s = ''

			extra_context.update({'survey': s })
			extra_context.update({'id_unit_kerja': 11}) # 11 Untuk Pembangunan
				
			
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})
			extra_context.update({'status': pengajuan_.status})
			extra_context.update({'pengajuan': pengajuan_})
			#+++++++++++++ page logout ++++++++++
			extra_context.update({'has_permission': True })
			#+++++++++++++ end page logout ++++++++++
			banyak = len(DetilIUJK.objects.all())
			extra_context.update({'banyak': banyak})
			syarat_ = Syarat.objects.filter(jenis_izin__jenis_izin__kode="SIUP")
			extra_context.update({'syarat': syarat_})
			kekayaan_bersih = int(0)
			extra_context.update({'kekayaan_bersih': formatrupiah(kekayaan_bersih)})
			total_nilai_saham = int(0)
			extra_context.update({'total_nilai_saham': formatrupiah(total_nilai_saham)})

			try:
				skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
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

			# if request.POST:
			# 	btn = request.POST.get('simpan')
			# 	if btn == 'tambahkan_survey':
			# 		pass
		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_iujk.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_bukti_admin_iujk(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			pengajuan_ = DetilIUJK.objects.get(id=id_pengajuan_izin_)
			extra_context.update({'pengajuan': pengajuan_ })
		template = loader.get_template("front-end/include/formulir_siup/cetak_bukti_pendaftaran_admin.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def option_klasifikasi(self, request):
		klasifikasi_list = Klasifikasi.objects.all()
		
		id_pengajuan = request.POST.get('pengajuan', None)	
		if id_pengajuan and not id_pengajuan is "":
			d = DetilIUJK.objects.get(pengajuanizin_ptr_id=id_pengajuan)
			# print d.jenis_iujk
			klasifikasi_list = klasifikasi_list.filter(jenis_iujk=d.jenis_iujk)
		pilihan = "<option value=''>-- Pilih Klasifikasi --</option>"
		print klasifikasi_list
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in klasifikasi_list)));

	def option_subklasifikasi(self, request):
		subklasifikasi_list = Subklasifikasi.objects.all()
	
		klasifikasi = request.POST.get('klasifikasi', None)	
		if klasifikasi and not klasifikasi is "":
			subklasifikasi_list = subklasifikasi_list.filter(klasifikasi_id=klasifikasi)
		pilihan = "<option value=''>-- Pilih Sub Klasifikasi --</option>"
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in subklasifikasi_list)));

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilIUJKAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^option-klasifikasi/$', self.option_klasifikasi, name='option_klasifikasi'),
			url(r'^option-subklasifikasi/$', self.option_subklasifikasi, name='option_subklasifikasi'),
			url(r'^cetak-bukti-pendaftaran-admin/(?P<id_pengajuan_izin_>[0-9]+)/$', self.admin_site.admin_view(self.cetak_bukti_admin_iujk), name='cetak_bukti_admin_iujk'),
			url(r'^view-pengajuan-iujk/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_iujk), name='view_pengajuan_iujk'),
			)
		return my_urls + urls

admin.site.register(DetilIUJK, DetilIUJKAdmin)



admin.site.register(Klasifikasi)


admin.site.register(Subklasifikasi)
