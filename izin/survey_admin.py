import json, drest
from django.contrib import admin, messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, resolve
from django.template import RequestContext, loader
from datetime import datetime
from daterange_filter.filter import DateRangeFilter

from izin.models import Survey, DetilIUJK, Riwayat, PengajuanIzin, DetilReklame
from izin.izin_forms import SurveyForm
from izin.survey_form import RekomendasiForm, DetilForm, BerkasForm, BAPReklameHOForm
from izin.utils import get_nomor_pengajuan
from kepegawaian.models import Pegawai, UnitKerja, NotifikasiTelegram
from kepegawaian.views import kirim_notifikasi_telegram
from master.models import Kecamatan
from perusahaan.models import Perusahaan
from pembangunan.models import AnggotaTim
from izin.utils import send_email_notifikasi, get_kode_izin, get_appmodels_based_kode_jenis, get_model_detil

from izin_dinkes.views_dinkes import post_pengajuanizin_dinkes


class KecamatanFilter(admin.SimpleListFilter):
	title = 'Kecamatan'
	parameter_name = 'kecamatan'

	def lookups(self, request, model_admin):
		countries = []
		qs = Kecamatan.objects.filter(kabupaten__provinsi__kode='35', kabupaten__kode='06')
		for c in qs:
			countries.append([c.id, c.nama_kecamatan])
		return countries

	def queryset(self, request, queryset):
		if self.value():
			return queryset.filter(pengajuan__perusahaan__desa__kecamatan__id__exact=self.value())
		else:
			return queryset

class SurveyAdmin(admin.ModelAdmin):
	# list_display = ('no_survey','get_pengajuan', 'get_pemohon' , 'get_perusahaan', 'get_perusahaan_lokasi' , 'deadline_survey', 'get_koordinator_survey','skpd' ,'get_aksi')
	list_filter = (KecamatanFilter,('deadline_survey', DateRangeFilter),('tanggal_survey', DateRangeFilter))
	search_fields = ('no_survey','pengajuan__no_pengajuan')

	def get_list_display(self, request):
		list_display = ('no_survey','get_no_pengajuan', 'get_pemohon' , 'get_perusahaan', 'get_perusahaan_lokasi' , 'deadline_survey',)
		if request.user.is_superuser:
			list_display = list_display+('get_koordinator_survey', )
		elif request.user.groups.filter(name="Admin SKPD"):
			list_display = list_display+('get_koordinator_survey','get_aksi',)
		else:
			list_display = list_display+('get_aksi',)

		return list_display



	def get_fieldsets(self, request, obj=None):
		field_user = ('keterangan_tambahan', )
		field_admin = ('no_survey', 'pengajuan','skpd','kelompok_jenis_izin','permohonan','tanggal_survey','deadline_survey','keterangan_tambahan','no_berita_acara','tanggal_berita_acara_dibuat','tanggal_berita_acara_diverifkasi')

		if obj:
			if request.user.is_superuser:
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': field_admin+('status',)
						}),
				)
			else:
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': field_user
						}),
				)
		else:
			add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': field_admin+('status',)
						}),
				)

		return add_fieldsets


	def get_koordinator_survey(self, obj):
		qs = obj.survey_iujk.filter(koordinator=True).last()
		return qs
	get_koordinator_survey.short_description = "Koordinator"

	
	def get_pengajuan(self, obj):
		return obj.pengajuan.kelompok_jenis_izin
	get_pengajuan.short_description = "Jenis Pengajuan"

	def get_no_pengajuan(self, obj):
		return obj.pengajuan.no_pengajuan
	get_no_pengajuan.short_description = "No. Pengajuan"

	def get_perusahaan(self, obj):
		perusahaan_ = ''
		kode_ijin = get_kode_izin(obj)
		if get_model_detil(kode_ijin):
			objects_ = get_model_detil(kode_ijin)
			if objects_:
				pengajuan_ = objects_.objects.get(id=obj.pengajuan.id)
				if pengajuan_.kelompok_jenis_izin.kode not in ['ITO', 'IAP', 'IOP', 'IPA', 'ILB']:
					perusahaan_ = pengajuan_.perusahaan
		return perusahaan_
	get_perusahaan.short_description = "Perusahaan"

	def get_perusahaan_lokasi(self, obj):
		kec = ''
		kode_ijin = get_kode_izin(obj)
		if get_model_detil(kode_ijin):
			objects_ = get_model_detil(kode_ijin)

			if objects_:
				pengajuan_ = objects_.objects.get(id=obj.pengajuan.id)
				if pengajuan_.kelompok_jenis_izin.kode not in ['ITO', 'IAP', 'IOP', 'IPA', 'ILB']:
					perusahaan_ = pengajuan_.perusahaan
					if pengajuan_.perusahaan:	
						if pengajuan_.perusahaan.desa:
							kec = pengajuan_.perusahaan.desa.kecamatan
		return kec
	get_perusahaan_lokasi.short_description = "Kec. Lokasi"

	def get_pemohon(self, obj):
		return obj.pengajuan.pemohon
	get_pemohon.short_description = "Pemohon"

	def get_aksi(self, obj):
		aksi = ''
		status = obj.status
		kode_ijin = get_kode_izin(obj)
		# print kode_ijin
		reverse_ = "#"
		if kode_ijin == "IUJK":
			reverse_ = reverse('admin:cek_kelengkapan', args=(obj.pengajuan.id, obj.id ))
		elif kode_ijin == "503.03.01/" or kode_ijin == "503.02/": # Rerklame permanen dan HO
			reverse_ = reverse('admin:cek_kelengkapan_reklame_ho', args=(obj.id, ))
		elif kode_ijin == "TDUP":
			reverse_ = reverse('admin:cek_kelengkapan_pengajuan_tdup', args=(obj.id, ))
		elif kode_ijin == "ITO":
			reverse_ = reverse('admin:cek_kelengkapan_pengajuan_toko_obat', args=(obj.id, ))
		elif kode_ijin == "IAP":
			reverse_ = reverse('admin:cek_kelengkapan_pengajuan_apotek', args=(obj.id, ))
		elif kode_ijin == "IOP":
			reverse_ = reverse('admin:cek_kelengkapan_pengajuan_optikal', args=(obj.id, ))
		elif kode_ijin == "ILB":
			reverse_ = reverse('admin:cek_kelengkapan_pengajuan_laboratorium', args=(obj.id, ))
		elif kode_ijin == "IPA":
			reverse_ = reverse('admin:cek_kelengkapan_pengajuan_penutupan_apotek', args=(obj.id, ))
		elif kode_ijin == "IMK":
			reverse_ = reverse('admin:cek_kelengkapan_pengajuan_mendirikan_klinik', args=(obj.id, ))
		elif kode_ijin == "IOK":
			reverse_ = reverse('admin:cek_kelengkapan_pengajuan_operasional_klinik', args=(obj.id, ))
		elif kode_ijin == "503.07/":
			reverse_ = reverse('admin:cek_kelengkapan_pengajuan_izin_lokasi', args=(obj.id, ))
		elif kode_ijin == "503.01.06/":
			reverse_ = reverse('admin:cek_kelengkapan_pengajuan_izin_lokasi', args=(obj.id, ))
		elif kode_ijin == "503.01.04/":
			reverse_ = reverse('admin:cek_kelengkapan_pengajuan_izin_lokasi', args=(obj.id, ))
		elif kode_ijin == "503.01.05/":
			reverse_ = reverse('admin:cek_kelengkapan_pengajuan_izin_lokasi', args=(obj.id, ))
		elif kode_ijin == "HULLER":
			reverse_ = reverse('admin:cek_kelengkapan_pengajuan_izin_lokasi', args=(obj.id, ))
		if status == 4 or status == 8:
			aksi = mark_safe("""
				<a href="%s" data-toggle='tooltip' data-container='body' data-original-title='Lihat Detail' > %s </a>
				""" % (reverse_, '<i class="fa fa-circle-o-notch"></i>' ))
		if status == 1:
			aksi = mark_safe("""
				<a href="%s" data-toggle='tooltip' data-container='body' data-original-title='Lihat Detail' > %s </a>
				""" % (reverse_, '<i class="fa fa-external-link"></i>' ))
		
		return aksi
	get_aksi.short_description = "Aksi"

	def changelist_view(self, request, extra_context={}):
		self.request = request
		extra_context.update({'kecamatan': Kecamatan.objects.filter(kabupaten__provinsi__kode='35', kabupaten__kode='06') })
		extra_context.update({'perusahaan': Perusahaan.objects.all() })
		# return self.changelist_view(request, extra_context)
		return super(SurveyAdmin, self).changelist_view(request, extra_context=extra_context)

	def view_cek_kelengkapan_pengajuan_tdup(self, request, id_survey):
		extra_context = {}
		extra_context.update({'has_permission': True })

		# queryset_ = self.get_queryset(request)
		# queryset_ =  queryset_.filter(pk=id_survey)
		queryset_ =  Survey.objects.filter(pk=id_survey)
		if queryset_.exists():
			queryset_ = queryset_.last()

			extra_context.update({ 'qs' : queryset_ })
			extra_context.update({ 'pengajuan' : queryset_.pengajuan })
			extra_context.update({ 'pemohon' : queryset_.pengajuan.pemohon })

			kode_ijin = get_kode_izin(queryset_)
			if get_model_detil(kode_ijin):
				objects_ = get_model_detil(kode_ijin)

			if objects_:
				pengajuan_ = objects_.objects.get(id=queryset_.pengajuan.id)
				# perusahaan_ = pengajuan_.perusahaan

				# extra_context.update({ 'perusahaan': perusahaan_ })
				extra_context.update({ 'pengajuan': pengajuan_ })

			try:
				status = queryset_.survey_iujk.get(pegawai=request.user)
				status = status.koordinator
			except ObjectDoesNotExist:
				status = False

			extra_context.update({ 'status_user': status })

			rekom = queryset_.survey_rekomendiasi.filter(created_by=request.user)

			if rekom.exists():
				rekom = rekom.last()
				extra_context.update({'rekom': rekom })
				data_rekom = { 'rekomendasi': rekom.rekomendasi }

			detilbap = queryset_.survey_reklame_ho.all()
			if detilbap.exists():
				detil = detilbap.first()
				extra_context.update({'detilbap': detil })
				data_bap = {
					'kondisi_lahan_usaha':detil.kondisi_lahan_usaha,
					'luas_tempat_usaha': detil.luas_tempat_usaha,
					'jumlah_mesin': detil.jumlah_mesin,
					'daya_kekuatan_mesin': detil.daya_kekuatan_mesin,
					'jenis_bangunan': detil.jenis_bangunan,
					'sebelah_utara': detil.sebelah_utara,
					'sebelah_timur': detil.sebelah_timur,
					'sebelah_selatan': detil.sebelah_selatan,
					'sebelah_barat': detil.sebelah_barat,
					'klasifikasi_jalan': detil.klasifikasi_jalan,
					}
				

			try:
				try:
					rekomendasiform = RekomendasiForm(instance=rekom, prefix="rekom")
				except AttributeError as e:
					rekomendasiform = RekomendasiForm(prefix="rekom")
			except UnboundLocalError, e:
				rekomendasiform = RekomendasiForm(prefix="rekom")

			extra_context.update({'form_rekomendasi': rekomendasiform })
				
			
			try:
				try:
					bapreklamehoform = BAPReklameHOForm(instance=detil, prefix="BAP")
				except AttributeError as e:
					bapreklamehoform = BAPReklameHOForm(prefix="BAP")
			except UnboundLocalError, e:
				bapreklamehoform = BAPReklameHOForm(prefix="BAP")
				
			extra_context.update({'form_detil': bapreklamehoform })
			
			extra_context.update({'form_berkas': BerkasForm })

			if request.POST:
				get_pegawai_skpd = Pegawai.objects.get(pk=request.user.id)
				btn = request.POST.get('simpan')
				if detilbap:
					form_detil = BAPReklameHOForm(request.POST, instance=detil, prefix="BAP")
				else:
					form_detil = BAPReklameHOForm(request.POST, prefix="BAP")

				if rekom:
					form_rekom = RekomendasiForm(request.POST, instance=rekom, prefix="rekom")
				else:
					form_rekom = RekomendasiForm(request.POST, prefix="rekom")

				# FORM BERKAS
				form_berkas = BerkasForm(request.POST, request.FILES)
				b = None
				if form_berkas.is_valid():
					b = form_berkas.save(commit=False)
					b.nama_berkas = 'Berkas Rekomendasi dgn No. Survey '+str(queryset_.no_survey)
					b.keterangan = b.nama_berkas
					b.save()

				if btn == 'submit':
					# print form_rekom.has_changed()
					# print form_detil.has_changed()
					if form_detil.is_valid() and form_rekom.is_valid():

						# DETIL BAP
						form_detil = form_detil.save(commit=False)
						form_detil.survey_iujk = queryset_
						form_detil.survey_id = id_survey
						form_detil.status = 1

						# FORM REKOMENDASI
						form_rekom = form_rekom.save(commit=False)
						form_rekom.survey_iujk = queryset_
						form_rekom.unit_kerja = get_pegawai_skpd.unit_kerja
						form_rekom.created_by_id = request.user.id
						form_rekom.status = 1
						form_rekom.berkas = b

						r = Riwayat.objects.filter(pengajuan_izin=queryset_.pengajuan).last()
						sent_ = 0
						if r.created_by:
							try:
								creadted_obj = Pegawai.objects.get(id=request.user.id)
								emailto = creadted_obj.email
								if creadted_obj.notifikasi_email:
									if emailto:
										subject = "Berita Acara Telah dibuat ["+str(queryset_.pengajuan.no_pengajuan)+"]"
										html_content = str(get_pegawai_skpd)+"-"+str(get_pegawai_skpd.unit_kerja)+" Telah mengisi berita acara."
										sent_ = send_email_notifikasi(emailto, subject, html_content)
										# print sent_
								if creadted_obj.notifikasi_telegram:
									try:
										noti = NotifikasiTelegram.objects.get(pegawai=r.created_by)
										kirim_notifikasi_telegram(noti.chat_id, "Berita Acara Telah dibuat ["+str(queryset_.pengajuan.no_pengajuan)+"] oleh "+str(request.user), "Proses Pembuatan Rekomendasi", request.user)
									except NotifikasiTelegram.DoesNotExist:
										pass
							except ObjectDoesNotExist:
								pass
						if sent_ == 1:
							messages.success(request, str(queryset_.no_survey)+" Berhasil Di Simpan dan Berhasil Kirim Email Notifikasi")
						else:
							messages.success(request, str(queryset_.no_survey)+" Berhasil Disimpan")
							
						form_detil.save()
						form_rekom.save()
						return HttpResponseRedirect(reverse('admin:izin_survey_changelist'))
					else:
						extra_context.update({'form_detil': form_detil })
						extra_context.update({'form_rekomendasi': form_rekom })
						messages.error(request, "Penyimpanan gagal, Perbaiki kesalahan dibawah.")
				elif btn == 'draft':
					# print form_rekom.has_changed()
					# print form_detil.has_changed()
					from pembangunan.models import Rekomendasi, BAPReklameHO
					if rekom:
						rekom.rekomendasi = request.POST.get('rekom-rekomendasi')
						rekom.berkas = b
						rekom.save()
					else:
						Rekomendasi.objects.create(
							unit_kerja=get_pegawai_skpd.unit_kerja,
							survey_iujk=queryset_, 
							rekomendasi=request.POST.get('rekom-rekomendasi'),
							created_by=request.user,
							status = 6,
							berkas=b)

					if request.POST.get('BAP-kondisi_lahan_usaha'):
						kondisi = request.POST.get('BAP-kondisi_lahan_usaha')
					else:
						kondisi = None

					if request.POST.get('BAP-jenis_bangunan'):
						jenis = request.POST.get('BAP-jenis_bangunan')
					else:
						jenis = None

					if request.POST.get('BAP-klasifikasi_jalan'):
						klasifikasi = request.POST.get('BAP-klasifikasi_jalan')
					else:
						klasifikasi = None

					# CEK APAKAH KOORDINATOR
					if status : 
						if detilbap:
							detil.kondisi_lahan_usaha = kondisi
							detil.luas_tempat_usaha = request.POST.get('BAP-luas_tempat_usaha')
							detil.jumlah_mesin = request.POST.get('BAP-jumlah_mesin')
							detil.daya_kekuatan_mesin = request.POST.get('BAP-daya_kekuatan_mesin')
							detil.jenis_bangunan = jenis
							detil.sebelah_utara = request.POST.get('BAP-sebelah_utara')
							detil.sebelah_timur = request.POST.get('BAP-sebelah_timur')
							detil.sebelah_selatan = request.POST.get('BAP-sebelah_selatan')
							detil.sebelah_barat = request.POST.get('BAP-sebelah_barat')
							detil.klasifikasi_jalan = klasifikasi
							detil.save()
						else:
							BAPReklameHO.objects.create(
								survey = queryset_,
								kondisi_lahan_usaha = kondisi,
								luas_tempat_usaha = request.POST.get('BAP-luas_tempat_usaha'),
								jumlah_mesin = request.POST.get('BAP-jumlah_mesin'),
								daya_kekuatan_mesin = request.POST.get('BAP-daya_kekuatan_mesin'),
								jenis_bangunan = jenis, 
								sebelah_utara = request.POST.get('BAP-sebelah_utara'),
								sebelah_timur = request.POST.get('BAP-sebelah_timur'),
								sebelah_selatan = request.POST.get('BAP-sebelah_selatan'),
								sebelah_barat = request.POST.get('BAP-sebelah_barat'),
								klasifikasi_jalan = klasifikasi,
								created_by= request.user,
								status = 6
								)

					messages.success(request, str(queryset_.no_survey)+" Berhasil disimpan sebagai draft")
					return HttpResponseRedirect(reverse('admin:cek_kelengkapan_reklame_ho', args=[queryset_.id]))


			template = loader.get_template("admin/pembangunan/cek_kelengkapan_tdup.html")
			ec = RequestContext(request, extra_context)
			return HttpResponse(template.render(ec))
		else:
			raise Http404

	def view_cek_kelengkapan_pengajuan_izin_lokasi(self, request, id_survey):
		extra_context = {}
		extra_context.update({'has_permission': True })

		# queryset_ = self.get_queryset(request)
		# queryset_ =  queryset_.filter(pk=id_survey)
		queryset_ =  Survey.objects.filter(pk=id_survey)
		if queryset_.exists():
			queryset_ = queryset_.last()

			extra_context.update({ 'qs_survey' : queryset_ })
			extra_context.update({ 'pengajuan' : queryset_.pengajuan })
			extra_context.update({ 'pemohon' : queryset_.pengajuan.pemohon })

			kode_ijin = get_kode_izin(queryset_)
			if get_appmodels_based_kode_jenis(kode_ijin):
				objects_ = get_appmodels_based_kode_jenis(kode_ijin)

			if objects_:
				pengajuan_ = objects_.objects.get(id=queryset_.pengajuan.id)
				try:
					perusahaan_ = pengajuan_.perusahaan
					extra_context.update({ 'perusahaan': perusahaan_ })
				except ObjectDoesNotExist:
					pass


			try:
				status = queryset_.survey_iujk.get(pegawai=request.user)
				status = status.koordinator
			except ObjectDoesNotExist:
				status = False

			extra_context.update({ 'status_user': status })

			rekom = queryset_.survey_rekomendiasi.filter(created_by=request.user)

			if rekom.exists():
				rekom = rekom.last()
				extra_context.update({'rekom': rekom })
				data_rekom = { 'rekomendasi': rekom.rekomendasi }

			detilbap = queryset_.survey_reklame_ho.all()
			if detilbap.exists():
				detil = detilbap.first()
				extra_context.update({'detilbap': detil })
				data_bap = {
					'kondisi_lahan_usaha':detil.kondisi_lahan_usaha,
					'luas_tempat_usaha': detil.luas_tempat_usaha,
					'jumlah_mesin': detil.jumlah_mesin,
					'daya_kekuatan_mesin': detil.daya_kekuatan_mesin,
					'jenis_bangunan': detil.jenis_bangunan,
					'sebelah_utara': detil.sebelah_utara,
					'sebelah_timur': detil.sebelah_timur,
					'sebelah_selatan': detil.sebelah_selatan,
					'sebelah_barat': detil.sebelah_barat,
					'klasifikasi_jalan': detil.klasifikasi_jalan,
					}
				

			try:
				try:
					rekomendasiform = RekomendasiForm(instance=rekom, prefix="rekom")
				except AttributeError as e:
					rekomendasiform = RekomendasiForm(prefix="rekom")
			except UnboundLocalError, e:
				rekomendasiform = RekomendasiForm(prefix="rekom")

			extra_context.update({'form_rekomendasi': rekomendasiform })
				
			
			try:
				try:
					bapreklamehoform = BAPReklameHOForm(instance=detil, prefix="BAP")
				except AttributeError as e:
					bapreklamehoform = BAPReklameHOForm(prefix="BAP")
			except UnboundLocalError, e:
				bapreklamehoform = BAPReklameHOForm(prefix="BAP")
				
			extra_context.update({'form_detil': bapreklamehoform })
			
			extra_context.update({'form_berkas': BerkasForm })

			if request.POST:
				get_pegawai_skpd = Pegawai.objects.get(pk=request.user.id)
				btn = request.POST.get('simpan')
				if detilbap:
					form_detil = BAPReklameHOForm(request.POST, instance=detil, prefix="BAP")
				else:
					form_detil = BAPReklameHOForm(request.POST, prefix="BAP")

				if rekom:
					form_rekom = RekomendasiForm(request.POST, instance=rekom, prefix="rekom")
				else:
					form_rekom = RekomendasiForm(request.POST, prefix="rekom")

				# FORM BERKAS
				form_berkas = BerkasForm(request.POST, request.FILES)
				b = None
				if form_berkas.is_valid():
					b = form_berkas.save(commit=False)
					b.nama_berkas = 'Berkas Rekomendasi dgn No. Survey '+str(queryset_.no_survey)
					b.keterangan = b.nama_berkas
					b.save()

				if btn == 'submit':
					# print form_rekom.has_changed()
					# print form_detil.has_changed()
					if form_detil.is_valid() and form_rekom.is_valid():

						# DETIL BAP
						form_detil = form_detil.save(commit=False)
						form_detil.survey_iujk = queryset_
						form_detil.survey_id = id_survey
						form_detil.status = 1

						# FORM REKOMENDASI
						form_rekom = form_rekom.save(commit=False)
						form_rekom.survey_iujk = queryset_
						form_rekom.unit_kerja = get_pegawai_skpd.unit_kerja
						form_rekom.created_by_id = request.user.id
						form_rekom.status = 1
						form_rekom.berkas = b

						r = Riwayat.objects.filter(pengajuan_izin=queryset_.pengajuan).last()
						sent_ = 0
						if r.created_by:
							try:
								creadted_obj = Pegawai.objects.get(id=r.created_by_id)
								emailto = creadted_obj.email
								if creadted_obj.notifikasi_email:
									if emailto:
										subject = "Berita Acara Telah dibuat ["+str(queryset_.pengajuan.no_pengajuan)+"]"
										html_content = str(get_pegawai_skpd)+"-"+str(get_pegawai_skpd.unit_kerja)+" Telah mengisi berita acara."
										sent_ = send_email_notifikasi(emailto, subject, html_content)
										# print sent_
								if creadted_obj.notifikasi_telegram:
									try:
										noti = NotifikasiTelegram.objects.get(pegawai=r.created_by)
										kirim_notifikasi_telegram(noti.chat_id, "Berita Acara Telah dibuat ["+str(queryset_.pengajuan.no_pengajuan)+"] oleh "+str(request.user), "Proses Pembuatan Rekomendasi", request.user)
									except NotifikasiTelegram.DoesNotExist:
										pass
							except ObjectDoesNotExist:
								pass
						if sent_ == 1:
							messages.success(request, str(queryset_.no_survey)+" Berhasil Di Simpan dan Berhasil Kirim Email Notifikasi")
						else:
							messages.success(request, str(queryset_.no_survey)+" Berhasil Disimpan")
							
						form_detil.save()
						form_rekom.save()
						return HttpResponseRedirect(reverse('admin:izin_survey_changelist'))
					else:
						extra_context.update({'form_detil': form_detil })
						extra_context.update({'form_rekomendasi': form_rekom })
						messages.error(request, "Penyimpanan gagal, Perbaiki kesalahan dibawah.")
				elif btn == 'draft':
					# print form_rekom.has_changed()
					# print form_detil.has_changed()
					from pembangunan.models import Rekomendasi, BAPReklameHO
					if rekom:
						rekom.rekomendasi = request.POST.get('rekom-rekomendasi')
						rekom.berkas = b
						rekom.save()
					else:
						Rekomendasi.objects.create(
							unit_kerja=get_pegawai_skpd.unit_kerja,
							survey_iujk=queryset_, 
							rekomendasi=request.POST.get('rekom-rekomendasi'),
							created_by=request.user,
							status = 6,
							berkas=b)

					if request.POST.get('BAP-kondisi_lahan_usaha'):
						kondisi = request.POST.get('BAP-kondisi_lahan_usaha')
					else:
						kondisi = None

					if request.POST.get('BAP-jenis_bangunan'):
						jenis = request.POST.get('BAP-jenis_bangunan')
					else:
						jenis = None

					if request.POST.get('BAP-klasifikasi_jalan'):
						klasifikasi = request.POST.get('BAP-klasifikasi_jalan')
					else:
						klasifikasi = None

					# CEK APAKAH KOORDINATOR
					if status : 
						if detilbap:
							print "MASUK SINI"
							detil.kondisi_lahan_usaha = kondisi
							detil.luas_tempat_usaha = request.POST.get('BAP-luas_tempat_usaha')
							detil.jumlah_mesin = request.POST.get('BAP-jumlah_mesin')
							detil.daya_kekuatan_mesin = request.POST.get('BAP-daya_kekuatan_mesin')
							detil.jenis_bangunan = jenis
							detil.sebelah_utara = request.POST.get('BAP-sebelah_utara')
							detil.sebelah_timur = request.POST.get('BAP-sebelah_timur')
							detil.sebelah_selatan = request.POST.get('BAP-sebelah_selatan')
							detil.sebelah_barat = request.POST.get('BAP-sebelah_barat')
							detil.klasifikasi_jalan = klasifikasi
							detil.save()
						else:
							BAPReklameHO.objects.create(
								survey = queryset_,
								kondisi_lahan_usaha = kondisi,
								luas_tempat_usaha = request.POST.get('BAP-luas_tempat_usaha'),
								jumlah_mesin = request.POST.get('BAP-jumlah_mesin'),
								daya_kekuatan_mesin = request.POST.get('BAP-daya_kekuatan_mesin'),
								jenis_bangunan = jenis, 
								sebelah_utara = request.POST.get('BAP-sebelah_utara'),
								sebelah_timur = request.POST.get('BAP-sebelah_timur'),
								sebelah_selatan = request.POST.get('BAP-sebelah_selatan'),
								sebelah_barat = request.POST.get('BAP-sebelah_barat'),
								klasifikasi_jalan = klasifikasi,
								created_by= request.user,
								status = 6
								)

					messages.success(request, str(queryset_.no_survey)+" Berhasil disimpan sebagai draft")
					return HttpResponseRedirect(reverse('admin:cek_kelengkapan_pengajuan_izin_lokasi', args=[queryset_.id]))


			template = loader.get_template("admin/pembangunan/cek_kelengkapan_izin_lokasi.html")
			# print template
			ec = RequestContext(request, extra_context)
			return HttpResponse(template.render(ec))
		else:
			raise Http404

	def view_cek_kelengkapan_pengajuan_reklame_ho(self, request, id_survey):
		extra_context = {}
		extra_context.update({'has_permission': True })

		# queryset_ = self.get_queryset(request)
		# queryset_ =  queryset_.filter(pk=id_survey)
		queryset_ =  Survey.objects.filter(pk=id_survey)
		if queryset_.exists():
			queryset_ = queryset_.last()

			extra_context.update({ 'qs_survey' : queryset_ })
			extra_context.update({ 'pengajuan' : queryset_.pengajuan })
			extra_context.update({ 'pemohon' : queryset_.pengajuan.pemohon })

			kode_ijin = get_kode_izin(queryset_)
			if get_appmodels_based_kode_jenis(kode_ijin):
				objects_ = get_appmodels_based_kode_jenis(kode_ijin)

			if objects_:
				pengajuan_ = objects_.objects.get(id=queryset_.pengajuan.id)
				perusahaan_ = pengajuan_.perusahaan

				extra_context.update({ 'perusahaan': perusahaan_ })

			try:
				status = queryset_.survey_iujk.get(pegawai=request.user)
				status = status.koordinator
			except ObjectDoesNotExist:
				status = False

			extra_context.update({ 'status_user': status })

			rekom = queryset_.survey_rekomendiasi.filter(created_by=request.user)

			if rekom.exists():
				rekom = rekom.last()
				extra_context.update({'rekom': rekom })
				data_rekom = { 'rekomendasi': rekom.rekomendasi }

			detilbap = queryset_.survey_reklame_ho.all()
			if detilbap.exists():
				detil = detilbap.first()
				extra_context.update({'detilbap': detil })
				data_bap = {
					'kondisi_lahan_usaha':detil.kondisi_lahan_usaha,
					'luas_tempat_usaha': detil.luas_tempat_usaha,
					'jumlah_mesin': detil.jumlah_mesin,
					'daya_kekuatan_mesin': detil.daya_kekuatan_mesin,
					'jenis_bangunan': detil.jenis_bangunan,
					'sebelah_utara': detil.sebelah_utara,
					'sebelah_timur': detil.sebelah_timur,
					'sebelah_selatan': detil.sebelah_selatan,
					'sebelah_barat': detil.sebelah_barat,
					'klasifikasi_jalan': detil.klasifikasi_jalan,
					}
				

			try:
				try:
					rekomendasiform = RekomendasiForm(instance=rekom, prefix="rekom")
				except AttributeError as e:
					rekomendasiform = RekomendasiForm(prefix="rekom")
			except UnboundLocalError, e:
				rekomendasiform = RekomendasiForm(prefix="rekom")

			extra_context.update({'form_rekomendasi': rekomendasiform })
				
			
			try:
				try:
					bapreklamehoform = BAPReklameHOForm(instance=detil, prefix="BAP")
				except AttributeError as e:
					bapreklamehoform = BAPReklameHOForm(prefix="BAP")
			except UnboundLocalError, e:
				bapreklamehoform = BAPReklameHOForm(prefix="BAP")
				
			extra_context.update({'form_detil': bapreklamehoform })
			
			extra_context.update({'form_berkas': BerkasForm })

			if request.POST:
				get_pegawai_skpd = Pegawai.objects.get(pk=request.user.id)
				btn = request.POST.get('simpan')
				if detilbap:
					form_detil = BAPReklameHOForm(request.POST, instance=detil, prefix="BAP")
				else:
					form_detil = BAPReklameHOForm(request.POST, prefix="BAP")

				if rekom:
					form_rekom = RekomendasiForm(request.POST, instance=rekom, prefix="rekom")
				else:
					form_rekom = RekomendasiForm(request.POST, prefix="rekom")

				# FORM BERKAS
				form_berkas = BerkasForm(request.POST, request.FILES)
				b = None
				if form_berkas.is_valid():
					b = form_berkas.save(commit=False)
					b.nama_berkas = 'Berkas Rekomendasi dgn No. Survey '+str(queryset_.no_survey)
					b.keterangan = b.nama_berkas
					b.save()

				if btn == 'submit':
					# print form_rekom.has_changed()
					# print form_detil.has_changed()
					if form_detil.is_valid() and form_rekom.is_valid():

						# DETIL BAP
						form_detil = form_detil.save(commit=False)
						form_detil.survey_iujk = queryset_
						form_detil.survey_id = id_survey
						form_detil.status = 1

						# FORM REKOMENDASI
						form_rekom = form_rekom.save(commit=False)
						form_rekom.survey_iujk = queryset_
						form_rekom.unit_kerja = get_pegawai_skpd.unit_kerja
						form_rekom.created_by = request.user
						form_rekom.status = 1
						form_rekom.berkas = b

						r = Riwayat.objects.filter(pengajuan_izin=queryset_.pengajuan).last()
						sent_ = 0
						if r.created_by:
							emailto = r.created_by.email
							if r.created_by.notifikasi_email:
								if emailto:
									subject = "Berita Acara Telah dibuat ["+str(queryset_.pengajuan.no_pengajuan)+"]"
									html_content = str(get_pegawai_skpd)+"-"+str(get_pegawai_skpd.unit_kerja)+" Telah mengisi berita acara."
									sent_ = send_email_notifikasi(emailto, subject, html_content)
									# print sent_
							if r.created_by.notifikasi_telegram:
								try:
									noti = NotifikasiTelegram.objects.get(pegawai=r.created_by)
									kirim_notifikasi_telegram(noti.chat_id, "Berita Acara Telah dibuat ["+str(queryset_.pengajuan.no_pengajuan)+"] oleh "+str(request.user), "Proses Pembuatan Rekomendasi", request.user)
								except NotifikasiTelegram.DoesNotExist:
									pass
						if sent_ == 1:
							messages.success(request, str(queryset_.no_survey)+" Berhasil Di Simpan dan Berhasil Kirim Email Notifikasi")
						else:
							messages.success(request, str(queryset_.no_survey)+" Berhasil Disimpan")
							
						form_detil.save()
						form_rekom.save()
						return HttpResponseRedirect(reverse('admin:izin_survey_changelist'))
					else:
						extra_context.update({'form_detil': form_detil })
						extra_context.update({'form_rekomendasi': form_rekom })
						messages.error(request, "Penyimpanan gagal, Perbaiki kesalahan dibawah.")
				elif btn == 'draft':
					# print form_rekom.has_changed()
					# print form_detil.has_changed()
					from pembangunan.models import Rekomendasi, BAPReklameHO
					if rekom:
						rekom.rekomendasi = request.POST.get('rekom-rekomendasi')
						rekom.berkas = b
						rekom.save()
					else:
						Rekomendasi.objects.create(
							unit_kerja=get_pegawai_skpd.unit_kerja,
							survey_iujk=queryset_, 
							rekomendasi=request.POST.get('rekom-rekomendasi'),
							created_by=request.user,
							status = 6,
							berkas=b)

					if request.POST.get('BAP-kondisi_lahan_usaha'):
						kondisi = request.POST.get('BAP-kondisi_lahan_usaha')
					else:
						kondisi = None

					if request.POST.get('BAP-jenis_bangunan'):
						jenis = request.POST.get('BAP-jenis_bangunan')
					else:
						jenis = None

					if request.POST.get('BAP-klasifikasi_jalan'):
						klasifikasi = request.POST.get('BAP-klasifikasi_jalan')
					else:
						klasifikasi = None

					# CEK APAKAH KOORDINATOR
					if status : 
						if detilbap:
							print "MASUK SINI"
							detil.kondisi_lahan_usaha = kondisi
							detil.luas_tempat_usaha = request.POST.get('BAP-luas_tempat_usaha')
							detil.jumlah_mesin = request.POST.get('BAP-jumlah_mesin')
							detil.daya_kekuatan_mesin = request.POST.get('BAP-daya_kekuatan_mesin')
							detil.jenis_bangunan = jenis
							detil.sebelah_utara = request.POST.get('BAP-sebelah_utara')
							detil.sebelah_timur = request.POST.get('BAP-sebelah_timur')
							detil.sebelah_selatan = request.POST.get('BAP-sebelah_selatan')
							detil.sebelah_barat = request.POST.get('BAP-sebelah_barat')
							detil.klasifikasi_jalan = klasifikasi
							detil.save()
						else:
							BAPReklameHO.objects.create(
								survey = queryset_,
								kondisi_lahan_usaha = kondisi,
								luas_tempat_usaha = request.POST.get('BAP-luas_tempat_usaha'),
								jumlah_mesin = request.POST.get('BAP-jumlah_mesin'),
								daya_kekuatan_mesin = request.POST.get('BAP-daya_kekuatan_mesin'),
								jenis_bangunan = jenis, 
								sebelah_utara = request.POST.get('BAP-sebelah_utara'),
								sebelah_timur = request.POST.get('BAP-sebelah_timur'),
								sebelah_selatan = request.POST.get('BAP-sebelah_selatan'),
								sebelah_barat = request.POST.get('BAP-sebelah_barat'),
								klasifikasi_jalan = klasifikasi,
								created_by= request.user,
								status = 6
								)

					messages.success(request, str(queryset_.no_survey)+" Berhasil disimpan sebagai draft")
					return HttpResponseRedirect(reverse('admin:cek_kelengkapan_reklame_ho', args=[queryset_.id]))


			template = loader.get_template("admin/pembangunan/cek_kelengkapan_reklame_ho.html")
			ec = RequestContext(request, extra_context)
			return HttpResponse(template.render(ec))
		else:
			raise Http404

	def view_cek_kelengkapan_pengajuan(self, request, id_pengajuan_izin_, id_survey):
		extra_context = {}
		extra_context.update({'has_permission': True })

		queryset_ = Survey.objects.filter(id=id_survey)

		if queryset_.exists():
		# try:

			queryset_ = queryset_.last()
			pegawai = Pegawai.objects.all()

			get_iujk = DetilIUJK.objects.filter(id=id_pengajuan_izin_)

			if get_iujk.exists():
				get_iujk = get_iujk.last()

				extra_context.update({ 'pegawai' : pegawai })
				extra_context.update({ 'qs' : queryset_ })
				try:
					status = queryset_.survey_iujk.get(pegawai_id=request.user.id)
					status = status.koordinator
				except ObjectDoesNotExist:
					status = False
				extra_context.update({ 'status_user': status })
				# print queryset_
				extra_context.update({ 'tanggal_survey': queryset_.tanggal_survey })
				extra_context.update({ 'deadline_survey': queryset_.deadline_survey })
				if queryset_.pengajuan:
					extra_context.update({ 'pengajuan': queryset_.pengajuan })

					if queryset_.pengajuan.pemohon:
						extra_context.update({ 'pemohon': queryset_.pengajuan.pemohon })

						if queryset_.pengajuan.pemohon.desa:
							pemohon = queryset_.pengajuan.pemohon
							alamat_ = str(pemohon.alamat)+", Ds. "+str(pemohon.desa)+", Kec. "+str(pemohon.desa.kecamatan)+", "+str(pemohon.desa.kecamatan.kabupaten)
							extra_context.update({ 'alamat': alamat_ })

						if get_iujk.perusahaan:
							perusahaan = get_iujk.perusahaan
							extra_context.update({ 'perusahaan': perusahaan })
							if perusahaan.desa:
								alamat_ = str(perusahaan.alamat_perusahaan)+", Ds. "+str(perusahaan.desa)+", Kec. "+str(perusahaan.desa.kecamatan)+", "+str(perusahaan.desa.kecamatan.kabupaten)
								extra_context.update({ 'alamat_perusahaan': alamat_ })
				# print queryset_.survey_rekomendiasi.all()
				rekom = queryset_.survey_rekomendiasi.filter(created_by=request.user)

				if rekom.exists():
					rekom = rekom.last()
					extra_context.update({'rekom': rekom })
					data_rekom = { 'rekomendasi': rekom.rekomendasi }

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
					

				try:
					extra_context.update({'form_rekomendasi': RekomendasiForm(data_rekom) })
				except UnboundLocalError, e:
					extra_context.update({'form_rekomendasi': RekomendasiForm })
				
				try:
					extra_context.update({'form_detil': DetilForm(data_bap) })
				except UnboundLocalError, e:
					extra_context.update({'form_detil': DetilForm })
				
				extra_context.update({'form_berkas': BerkasForm })
				if request.POST:
					btn = request.POST.get('simpan')
					if detilbap:
						form_detil = DetilForm(request.POST, instance=detil)
					else:
						form_detil = DetilForm(request.POST)

					if form_detil.is_valid():
						d = form_detil.save(commit=False)
						d.survey_iujk_id = queryset_.id


						if rekom:
							form = RekomendasiForm(request.POST, instance=rekom)
						else:
							form = RekomendasiForm(request.POST)

						if form.is_valid():
							f = form.save(commit=False)
							f.survey_iujk_id = queryset_.id

							get_pegawai_skpd = Pegawai.objects.get(pk=request.user.id)
							f.unit_kerja = get_pegawai_skpd.unit_kerja

							f.created_by = request.user

							form_berkas = BerkasForm(request.POST, request.FILES)
							if form_berkas.is_valid():
								b = form_berkas.save(commit=False)
								b.nama_berkas = 'Berkas Rekomendasi dgn No. Survey '+str(queryset_.no_survey)
								b.keterangan = b.nama_berkas
								b.save()

								f.berkas = b

							if btn == 'submit':
								# queryset_.status = 1
								d.status = 1
								f.status = 1
								r = Riwayat.objects.filter(pengajuan_izin_id=id_pengajuan_izin_).last()
								sent_ = 0
								if r.created_by:
									try:
										creadted_obj = Pegawai.objects.get(id=r.created_by_id)
										emailto = r.created_by.email
										if creadted_obj.notifikasi_email:
											if emailto:
												subject = "Berita Acara Telah dibuat ["+str(queryset_.pengajuan.no_pengajuan)+"]"
												html_content = "Silahkan buka akun anda atau klik link berikut <a href='http://"+str(request.META['HTTP_HOST'])+"/admin/izin/detiliujk/view-pengajuan-iujk/"+str(id_pengajuan_izin_)+"'>Berita Acara</a> <br> <img src='http://simpatik.kedirikab.go.id:8889/static/images/wwa.png' style='background-color: darkgrey;'>"
												sent_ = send_email_notifikasi(emailto, subject, html_content)
												print sent_
										if creadted_obj.notifikasi_telegram:
											try:
												noti = NotifikasiTelegram.objects.get(pegawai=r.created_by)
												kirim_notifikasi_telegram(noti.chat_id, "Berita Acara Telah dibuat ["+str(queryset_.pengajuan.no_pengajuan)+"] oleh "+str(request.user), "Proses Pembuatan Rekomendasi", request.user)
											except NotifikasiTelegram.DoesNotExist:
												pass
									except ObjectDoesNotExist:
										messages.error(request, "Data pegawai tidak ditemukan.")
										
								if sent_ == 1:
									messages.success(request, "Berhasil Di Simpan dan Berhasil Kirim Email Notifikasi")
								else:
									messages.success(request, "Berhasil Disimpan")

								if status:
									d.save()
								f.save()
								
								queryset_.save()
								return HttpResponseRedirect(reverse('admin:survey_selesai'))
							elif btn == 'draft':
								d.status = 6
								f.status = 6
								if status:
									d.save()
								# print "HALO"
								f.save()
								
								# queryset_.save()
								messages.success(request, "Berhasil Disimpan Sebagai Draft")
								return HttpResponseRedirect(reverse('admin:izin_survey_changelist'))
						else:
							# pass
							messages.error(request, "Rekomendasi Tidak Boleh Kosong")
					else:
						# pass
						messages.error(request, "Rekomendasi dan Detil BAP harus diisi")
						# queryset_.update(status=1)

					return HttpResponseRedirect(reverse('admin:cek_kelengkapan', args=[id_pengajuan_izin_, id_survey]))
					

			# messages.error(request)
			# return HttpResponseRedirect(reverse('admin:cek_kelengkapan', args=[id_pengajuan_izin_]))

			else:
				# print "alsdjfhalks"
				raise Http404

		# except ObjectDoesNotExist:
		else:
			# print "alsdjfhalks"
			raise Http404

		template = loader.get_template("admin/pembangunan/cek_kelengkapan.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))
		
	def surveyselesai(self, request, extra_context={}):
		extra_context.update({'title': 'Survey Izin Selesai'})
		self.request = request
		return self.changelist_view(request, extra_context)

	def surveyproses(self, request, extra_context={}):
		extra_context.update({'title': 'Survey Izin'})
		self.request = request
		return self.changelist_view(request, extra_context)

	def get_list_display_links(self, request, list_display):
		if request.user.is_superuser:
			list_display_links = ('no_survey', )
		else:
			list_display_links = (None)
		return list_display_links

	def has_add_permission(self, request):
		if request.user.is_superuser:
			return True
		return False

	def get_queryset(self, request):
		func_view, func_view_args, func_view_kwargs = resolve(request.path)
		qs = super(SurveyAdmin, self).get_queryset(request)
		# print request.user.pegawai.unit_kerja

		if request.user.groups.filter(name="Tim Teknis"):
			a = AnggotaTim.objects.filter(pegawai=request.user)
			if a.exists():
				a = a.values_list('survey_iujk')
				qs = qs.filter(id__in=a)
			# SIMPATIK-PEMBANGUNAN BELUM DITAMBAHI INI
			else:
				qs = qs.none()
			# SAMPAI SINI
		elif request.user.groups.filter(name="Admin SKPD"):
			a = AnggotaTim.objects.filter(pegawai__unit_kerja=request.user.pegawai.unit_kerja)
			if a.exists():
				a = a.values_list('survey_iujk')
				qs = qs.filter(id__in=a)
			# SIMPATIK-PEMBANGUNAN BELUM DITAMBAHI INI
			else:
				qs = qs.none()

		if func_view.__name__ == self.surveyselesai.__name__:
			qs = qs.filter(status=1)
		elif func_view.__name__ == self.surveyproses.__name__:
			qs = qs.filter(~Q(status=1))

		return qs

	def save_survey_ajax(self, request):
		frm = SurveyForm(request.POST)
		# print "#########masuk"
		pengajuan_id_ = request.POST.get('pengajuan_id')
		# id_unit_kerja = request.POST.get('id_unit_kerja')
		# unit_kerja = UnitKerja.objects.get(pk=id_unit_kerja)
		if frm.is_valid():
			p = frm.save(commit=False)
			p.no_survey = get_nomor_pengajuan('SURVEY')
			p.pengajuan_id = pengajuan_id_
			p.tanggal_survey = datetime.now()
			# p.skpd = unit_kerja
			p.status = 4
			p.created_by_id = request.user.id
			# p.kelompok_jenis_izin_id = request.POST.get('kelompok_jenis_izin_id')
			p.save()
			# print "#####################################"
			# print "#####################################"
			# print "#####################################"

			# ANGGOTA TIM
			at = AnggotaTim(
					survey_iujk= p,
					pegawai_id= request.POST.get('pegawai'),
					koordinator= True
				)
			at.save()

			# RIWAYAT
			riwayat_ = Riwayat(
						pengajuan_izin_id = pengajuan_id_,
						created_by_id = request.user.id,
						keterangan = "Mengirim Ke Koordinator Tim Teknis "+str(at.pegawai),
						alasan=''
					)
			riwayat_.save()

			# SAVE PENGAJUAN TIDAK DI PAKAI
			# pengajuan = DetilIUJK.objects.get(id=pengajuan_id_)
			# pengajuan.status = 8
			# pengajuan.save()



			data = {'success': True, 
				'pesan': 'Data Survey Berhasil Disimpan. Notifikasi dikirim ke '+str(at.pegawai),
			}
			data = json.dumps(data)
			response = HttpResponse(data)
		else:
			data = frm.errors.as_json()
			response = HttpResponse(data)

		return response

	def delete_survey_ajax(self, request):
		id_survey = request.POST.get('id')
		if id_survey:
			try:
				survey = Survey.objects.get(id=id_survey)
				data = {'success': True, 
				'pesan': 'Data Survey '+str(survey)+' Berhasil Dihapus.',
				
				}
				riwayat_ = Riwayat(
						pengajuan_izin = survey.pengajuan,
						created_by = request.user,
						keterangan = "Survey Dibatalkan oleh "+str(request.user),
						alasan=''
					)
				riwayat_.save()

				survey.delete()
				
			except Survey.DoesNotExist:
				data = {'success': False, 
				'pesan': 'Survey Tidak ditemukan.',
				}
		else:
			data = {'success': False, 
			'pesan': 'Survey Tidak Ada.',
			}

		data = json.dumps(data)
		response = HttpResponse(data)

		return response

	def send_survey(self, request):
		id_pengajuan = request.POST.get('id')
		if id_pengajuan:
			try:
				survey = Survey.objects.filter(pengajuan__id=id_pengajuan)
				pengajuan = DetilIUJK.objects.get(id=id_pengajuan)
				
				for s in survey:
					s.status = 4
					s.save()
					# print "ok"

				pengajuan.status = 8
				pengajuan.save()

				

				data = {'success': True, 
				'pesan': 'Survey berhasil dikirim',
				}

			except Survey.DoesNotExist:
				data = {'success': False, 
				'pesan': 'Survey Tidak ditemukan.',
				}
		else:
			data = {'success': False, 
			'pesan': 'Pengajuan Tidak Terdaftar.',
			}

		data = json.dumps(data)
		response = HttpResponse(data)

		return response

	def do_survey(self, request, id_survey):
		from smtplib import SMTPAuthenticationError
		if id_survey:
			try:
				s = Survey.objects.get(pk=id_survey)
				s.status = 8
				
				
				for n in s.survey_iujk.all():
					subject = "Undangan Cek Lokasi"
					html_content = "<p>Anda Diundang untuk melakukan survey dengan nomor Survey <strong>"+str(s.no_survey)+"</strong> dan nomor pengajuan izin <strong>"+str(s.pengajuan.no_pengajuan)+"</strong>, batas akhir survey tanggal "+str(s.deadline_survey)+". Berikut adalah Anggota Tim Teknis</p>"
					html_content += '''<table border="1" style="border-collapse: collapse;" class="table table-striped table-bordered table-hover table-condensed">
									<thead>
									  <tr>
										  <th scope="col" class="">NIP</th>
										  <th scope="col" class="">NAMA</th>
									  </tr>
									</thead>'''
					html_content += "<tbody>"
					for p in s.survey_iujk.all():
						html_content += '''
								<tr>
								  <td>{0}</td>
								  <td>{1}</td>
								</tr>'''.format(p.pegawai.username, p.pegawai.unit_kerja)
					html_content += "</tbody></table>"
					html_content += "<p>Untuk informasi lebih lanjut silahkan hubungi Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu (DPM-PTSP) Kab. Kediri</p>"
					if not n.koordinator:
						# print "sending "+str(n.pegawai.email)
						try:
							sent_ = send_email_notifikasi(n.pegawai.email, subject, html_content)
						except SMTPAuthenticationError:
							data = {'success': False, 
							'pesan': 'Survey gagal mengirim email dikirim',
							}
							return HttpResponse(json.dumps(data))
				s.save()

				pengajuan = s.pengajuan
				pengajuan_obj = pengajuan
				kode_kelompok_izin = pengajuan.kelompok_jenis_izin.kode
				push_survey = None
				if kode_kelompok_izin in ['IAP', 'ITO', 'ILB', 'IOP', 'IPA', 'IMK', 'IOK']:
					# print pengajuan.id
					push_survey = post_pengajuanizin_dinkes(pengajuan.id)
					# send_email_html('ryanxxrizki@gmail.com', 'Surat Rekomendasi Memerlukan Survey ', pengajuan_obj, 'admin/email_template/send_email_rekom_dinkes.html')
					data = {'success': True, 
					'pesan': 'Survey dan Rekomendasi Dinkes berhasil dikirim',
					}
				else:
					push_survey = 200 #success
					data = {'success': True, 
					'pesan': 'Survey berhasil dikirim',
					}
				if push_survey:
					if push_survey == 200:
						pengajuan.status = 8
						pengajuan.save()
					elif push_survey == 201: #objects is exist
						data = {'success': False, 'pesan': 'Data Survey sudah ada di Dinkes.',}
					else:
						data = {'success': False, 'pesan': 'Survey gagal mengirim.',}
				else:
					data = {'success': False, 'pesan': 'Survey gagal mengirim.',}

			except Survey.DoesNotExist:
				data = {'success': False, 
				'pesan': 'Survey Tidak ditemukan.',
				}
		else:
			data = {'success': False, 
			'pesan': 'Pengajuan Tidak Terdaftar.',
			}

		return HttpResponse(json.dumps(data))

	def suit_cell_attributes(self, obj, column):
		if column in ['get_aksi',]:
			return {'class': 'text-center'}
		elif column in ['get_koordinator_survey']:
			return {'data-toggle': 'tooltip', 'data-container': 'body', 'data-original-title': 'Anggota Survey : %s ' % ", ".join(str(x.pegawai) for x in obj.survey_iujk.all().exclude(koordinator=True) )}
		else:
			return None

	def send_detil_pengajuan(self, request, id_pengajuan):
		if id_pengajuan:
			try:
				pengajuan_obj = PengajuanIzin.objects.get(id=id_pengajuan)
				try:
					try:
						api = drest.api.TastyPieAPI('http://127.0.0.1:8889/api/v1/')
						api.auth('dishub', 'jgHwLBYweHsfKSZiJHfmIQ2L5KZDNh4J')
						api.request.add_header('X-CSRFToken', '{{csrf_token}}')
						api.request.add_header('Content-Type', 'application/json')
						data_izin = dict(
							id=pengajuan_obj.id,
							pemohon=pengajuan_obj.pemohon.nama_lengkap,
							jenis_pengajuan=pengajuan_obj.jenis_permohonan.jenis_permohonan,
							perusahaan=pengajuan_obj.perusahaan.nama_perusahaan,
							no_pengajuan=pengajuan_obj.no_pengajuan,
							tgl_pengajuan=pengajuan_obj.created_at.strftime('%d-%m-%Y')
						)
						response = api.izin.post(data_izin)
						print response
						if response.status in (200, 201, 202):
							print "OK"
					except drest.exc.dRestAPIError as e:
						print e.msg
				except drest.exc.dRestRequestError as e:
					print e.msg
			except ObjectDoesNotExist:
				print "Data tidak ditemukan"

	def send_detil_pengajuan_without_perusahaan(self, request, id_pengajuan):
		if id_pengajuan:
			try:
				pengajuan_obj = PengajuanIzin.objects.get(id=id_pengajuan)
				try:
					try:
						api = drest.api.TastyPieAPI('http://127.0.0.1:8889/api/v1/')
						api.auth('dishub', 'jgHwLBYweHsfKSZiJHfmIQ2L5KZDNh4J')
						api.request.add_header('X-CSRFToken', '{{csrf_token}}')
						api.request.add_header('Content-Type', 'application/json')
						data_izin = dict(
							id=pengajuan_obj.id,
							pemohon=pengajuan_obj.pemohon.nama_lengkap,
							jenis_pengajuan=pengajuan_obj.jenis_permohonan.jenis_permohonan,
							# perusahaan=pengajuan_obj.perusahaan.nama_perusahaan,
							no_pengajuan=pengajuan_obj.no_pengajuan,
							tgl_pengajuan=pengajuan_obj.created_at.strftime('%d-%m-%Y')
						)
						response = api.izin.post(data_izin)
						print response
						if response.status in (200, 201, 202):
							print "OK"
					except drest.exc.dRestAPIError as e:
						print e.msg
				except drest.exc.dRestRequestError as e:
					print e.msg
			except ObjectDoesNotExist:
				print "Data tidak ditemukan"


	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(SurveyAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^survey-save-ajax/$', self.save_survey_ajax, name="save_survey_ajax" ),
			url(r'^survey-delete-ajax/$', self.delete_survey_ajax, name="delete_survey_ajax" ),
			url(r'^survey-sending/$', self.send_survey, name="send_survey" ),
			url(r'^do-survey/(?P<id_survey>[0-9]+)$', self.admin_site.admin_view(self.do_survey), name="lakukan_survey" ),
			url(r'^laporan-survey/$', self.admin_site.admin_view(self.surveyselesai), name='survey_selesai'),
			url(r'^daftar-survey/$', self.admin_site.admin_view(self.surveyproses), name='survey_proses'),
			url(r'^survey-cek-kelengkapan/(?P<id_pengajuan_izin_>[0-9]+)/(?P<id_survey>[0-9]+)$', self.view_cek_kelengkapan_pengajuan, name="cek_kelengkapan" ),
			url(r'^survey-cek-kelengkapan-reklame-ho/(?P<id_survey>[0-9]+)$', self.view_cek_kelengkapan_pengajuan_reklame_ho, name="cek_kelengkapan_reklame_ho" ),
			url(r'^survey-cek-kelengkapan-tdup/(?P<id_survey>[0-9]+)$', self.view_cek_kelengkapan_pengajuan_tdup, name="cek_kelengkapan_pengajuan_tdup" ),
			url(r'^survey-cek-kelengkapan-toko-obat/(?P<id_survey>[0-9]+)$', self.view_cek_kelengkapan_pengajuan_tdup, name="cek_kelengkapan_pengajuan_toko_obat" ),
			url(r'^survey-cek-kelengkapan-apotek/(?P<id_survey>[0-9]+)$', self.view_cek_kelengkapan_pengajuan_tdup, name="cek_kelengkapan_pengajuan_apotek" ),
			url(r'^survey-cek-kelengkapan-optikal/(?P<id_survey>[0-9]+)$', self.view_cek_kelengkapan_pengajuan_tdup, name="cek_kelengkapan_pengajuan_optikal" ),
			url(r'^survey-cek-kelengkapan-laboratorium/(?P<id_survey>[0-9]+)$', self.view_cek_kelengkapan_pengajuan_tdup, name="cek_kelengkapan_pengajuan_laboratorium" ),
			url(r'^survey-cek-kelengkapan-penutupan-apotek/(?P<id_survey>[0-9]+)$', self.view_cek_kelengkapan_pengajuan_tdup, name="cek_kelengkapan_pengajuan_penutupan_apotek" ),
			url(r'^survey-cek-kelengkapan-mendirikan-klinik/(?P<id_survey>[0-9]+)$', self.view_cek_kelengkapan_pengajuan_tdup, name="cek_kelengkapan_pengajuan_mendirikan_klinik" ),
			url(r'^survey-cek-kelengkapan-operasional-klinik/(?P<id_survey>[0-9]+)$', self.view_cek_kelengkapan_pengajuan_tdup, name="cek_kelengkapan_pengajuan_operasional_klinik" ),
			url(r'^survey-cek-kelengkapan-izin-lokasi/(?P<id_survey>[0-9]+)$', self.view_cek_kelengkapan_pengajuan_izin_lokasi, name="cek_kelengkapan_pengajuan_izin_lokasi" ),
			)
		return my_urls + urls

	# def __init__(self, *args, **kwargs):
	# 	super(SurveyAdmin, self).__init__(*args, **kwargs)
	# 	self.list_display_links = (None, )

admin.site.register(Survey, SurveyAdmin)