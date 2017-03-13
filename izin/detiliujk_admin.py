from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe


from izin.models import DetilIUJK, SKIzin, Riwayat, Syarat, Survey, Klasifikasi, Subklasifikasi, PengajuanIzin
from izin.utils import formatrupiah, JENIS_PERMOHONAN, formatrupiah
from accounts.models import NomorIdentitasPengguna
from kepegawaian.models import UnitKerja, Pegawai


class DetilIUJKAdmin(admin.ModelAdmin):

	def view_pengajuan_iujk(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			extra_context.update({'skpd_list' : UnitKerja.objects.all() })
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
			# SURVEY
			h = Group.objects.filter(name="Cek Lokasi")
			if h.exists():
				h = h.last()
			h = h.user_set.all()
			extra_context.update({'pegawai_list' : h })

			try:
				try:
					s = Survey.objects.get(pengajuan=pengajuan_)
				except Survey.MultipleObjectsReturned:
					s = Survey.objects.filter(pengajuan=pengajuan_).last()
					print s.survey_iujk.all()
			except ObjectDoesNotExist:
				s = ''

			extra_context.update({'survey': s })
			# extra_context.update({'id_unit_kerja': 11}) # 11 Untuk Pembangunan
			# SURVEY	
			
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

	def cetak_iujk_asli(self, request, id_pengajuan_izin_):

		extra_context = {}

		from django.template import Context, Template
		from master.models import Template as tpls
		from dateutil.relativedelta import relativedelta

		pengajuan_ = get_object_or_404(DetilIUJK, id=id_pengajuan_izin_)
		unit_kerja = get_object_or_404(UnitKerja, id=72)
		skizin_ = get_object_or_404(SKIzin, pengajuan_izin_id=id_pengajuan_izin_)

		tpl = tpls.objects.get(kelompok_jenis_izin__kode="IUJK")

		extra_context.update({'html':tpl.body_html})
		extra_context.update({'pengajuan': pengajuan_})
		extra_context.update({'nomor': pengajuan_.no_izin})
		extra_context.update({'skizin_status': skizin_.status})

		paket = pengajuan_.paket_pekerjaan_iujk.all()

		kla = []
		tr = ''
		no = 0
		total_ = len(paket)
		css = 'hidden-border-tr'
		for p in paket:
			total_ = total_ - 1
			# print total_
			if total_ == 0:
				css = ''
			tr += '<tr style="border: 1px solid black;" class="'+css+'">'
			if p.subklasifikasi.klasifikasi in kla:
				tr += '<td style="border: 1px solid black;"></td>'
				tr += '<td style="border: 1px solid black;"></td>'
			else:
				k = p.subklasifikasi.klasifikasi
				no = no+1
				tr += '<td style="border: 1px solid black;">'+str(no)+'.</td>'
				tr += '<td style="border: 1px solid black;">'+str(k)+'</td>'			
				kla.append(p.subklasifikasi.klasifikasi)
			tahun = '0'
			if p.tahun:
				tahun = str(p.tahun)
			tr += '<td style="border: 1px solid black;">'+str(p.subklasifikasi)+'</td>'
			tr += '<td style="border: 1px solid black;">'+str(p.nama_paket_pekerjaan)+'</td>'
			tr += '<td style="border: 1px solid black;">'+tahun+'</td>'
			if p.nilai_paket_pekerjaan is None or p.nilai_paket_pekerjaan == 0:
				nilai_paket = 0
			else:
				nilai_paket = formatrupiah(p.nilai_paket_pekerjaan)
			tr += '<td style="border: 1px solid black;">'+str(nilai_paket)+'</td>'
			
			if p.keterangan is None or p.keterangan == '-':
				keterangan = ''
			else:
				keterangan = p.keterangan	
			tr += '<td style="border: 1px solid black;">'+str(keterangan)+'</td>'
			tr += '</tr>'


		# print tr
		extra_context.update({'klasifikasi_tr': mark_safe(tr) })

		template = loader.get_template("front-end/include/formulir_iujk/cetak_iujk.html")
		ec = RequestContext(request, extra_context)
		# print template.render(ec)

		

		direktur = pengajuan_.anggota_badan_iujk.filter(jenis_anggota_badan="Direktur / Penanggung Jawab Badan Usaha")
		if direktur.exists():
			direktur_bu = direktur.last()
			direktur = direktur_bu.nama
			
		else:
			direktur = ''
			
		no_pjt_bu = '0'
		teknis = pengajuan_.anggota_badan_iujk.filter(jenis_anggota_badan="Penanggung Jawab Teknik Badan Usaha")
		if teknis.exists():
			teknis_ = teknis.last()
			teknis = teknis_.nama
			if teknis_.no_pjt_bu:
				no_pjt_bu = str(teknis_.no_pjt_bu)
		else:
			teknis = ''
			no_pjt_bu = ''

				

		subject_template = template.render(ec)
		extra_context.update({'nomor': pengajuan_.no_izin})
		extra_context.update({'nama_badan_usaha': pengajuan_.perusahaan})
		extra_context.update({'alamat': pengajuan_.perusahaan.alamat_perusahaan})
		extra_context.update({'desa': pengajuan_.perusahaan.desa})
		extra_context.update({'kecamatan': pengajuan_.perusahaan.desa.kecamatan})
		extra_context.update({'kabupaten': pengajuan_.perusahaan.desa.kecamatan.kabupaten})
		extra_context.update({'provinsi': pengajuan_.perusahaan.desa.kecamatan.kabupaten.provinsi})
		extra_context.update({'telp': pengajuan_.perusahaan.telepon})
		extra_context.update({'direktur': direktur})
		extra_context.update({'npwp': pengajuan_.perusahaan.npwp})
		extra_context.update({'kualifikasi': pengajuan_.kualifikasi })
		extra_context.update({'penanggung_jawab_teknis': teknis})
		extra_context.update({'no_pjt_bu': no_pjt_bu})

		
		li = ''
		for x in list(set(kla)):
			k =  "<li>"+str(x)+"</li>"
			li += k
		# for x in paket:
		# 	if x.subklasifikasi.klasifikasi in kla:

		# 		k = ''
		# 	else:
		# 		k = "<li>"+str(x.subklasifikasi.klasifikasi)+"</li>"
		# 	
		# li += k

		extra_context.update({'klasifikasi': mark_safe(li) })

		masa_berlaku = skizin_.created_at+relativedelta(years=3)
		masa_berlaku = masa_berlaku.strftime('%d-%m-%Y')
		extra_context.update({'masa_berlaku': masa_berlaku})
		extra_context.update({'tanggal': skizin_.created_at.strftime('%d-%m-%Y')})
		extra_context.update({'satker': unit_kerja})
		extra_context.update({'kepala': unit_kerja.kepala.get_full_name})
		extra_context.update({'jabatan': "Pembina Tingkat I"})
		extra_context.update({'nip': "NIP. "+str(unit_kerja.kepala.username)})
		extra_context.update({'pengajuan': pengajuan_ })

		template = Template(subject_template).render(Context(extra_context))
		return HttpResponse(template)

		
	def option_klasifikasi(self, request):
		klasifikasi_list = Klasifikasi.objects.all()
		
		id_pengajuan = request.POST.get('pengajuan', None)	
		if id_pengajuan and not id_pengajuan is "":
			d = DetilIUJK.objects.get(pengajuanizin_ptr_id=id_pengajuan)
			# print d.jenis_iujk
			klasifikasi_list = klasifikasi_list.filter(jenis_iujk=d.jenis_iujk)
		pilihan = "<option value=''>-- Pilih Klasifikasi --</option>"
		# print klasifikasi_list
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in klasifikasi_list)));

	def option_subklasifikasi(self, request):
		subklasifikasi_list = Subklasifikasi.objects.all()
	
		klasifikasi = request.POST.get('klasifikasi', None)	
		if klasifikasi and not klasifikasi is "":
			subklasifikasi_list = subklasifikasi_list.filter(klasifikasi_id=klasifikasi)
		pilihan = "<option value=''>-- Pilih Sub Klasifikasi --</option>"
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in subklasifikasi_list)));

	def option_pegawai(self, request):
		pegawai_list = Pegawai.objects.all()
	
		unit_kerja_id = request.POST.get('unit_kerja', None)	
		if unit_kerja_id and not unit_kerja_id is "":
			pegawai_list = pegawai_list.filter(unit_kerja_id=unit_kerja_id, groups__name="Tim Teknis")
		pilihan = "<option value=''>-- Pilih Pegawai --</option>"
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in pegawai_list)));

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilIUJKAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^cetak-iujk/(?P<id_pengajuan_izin_>[0-9]+)/$', self.admin_site.admin_view(self.cetak_iujk_asli), name='cetak_iujk_asli'),
			url(r'^option-klasifikasi/$', self.option_klasifikasi, name='option_klasifikasi'),
			url(r'^option-subklasifikasi/$', self.option_subklasifikasi, name='option_subklasifikasi'),
			url(r'^option-pegawai/$', self.option_pegawai, name='option_pegawai'),
			url(r'^cetak-bukti-pendaftaran-admin/(?P<id_pengajuan_izin_>[0-9]+)/$', self.admin_site.admin_view(self.cetak_bukti_admin_iujk), name='cetak_bukti_admin_iujk'),
			url(r'^view-pengajuan-iujk/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_iujk), name='view_pengajuan_iujk'),
			)
		return my_urls + urls

admin.site.register(DetilIUJK, DetilIUJKAdmin)
admin.site.register(Klasifikasi)
admin.site.register(Subklasifikasi)