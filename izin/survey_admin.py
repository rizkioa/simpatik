from django.contrib import admin, messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, HttpResponseRedirect
import json
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, resolve
from django.template import RequestContext, loader
from datetime import datetime

from daterange_filter.filter import DateRangeFilter

from izin.models import Survey, DetilIUJK, Riwayat
from izin.izin_forms import SurveyForm
from izin.survey_form import RekomendasiForm, DetilForm, BerkasForm
from izin.utils import get_nomor_pengajuan
from kepegawaian.models import Pegawai, UnitKerja
from master.models import Kecamatan
from perusahaan.models import Perusahaan
from pembangunan.models import AnggotaTim
from izin.utils import send_email_notifikasi

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
			list_display = list_display+('skpd',)
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
			pass

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
		iujk = DetilIUJK.objects.get(pengajuan_ptr_id=obj.id)
		return iujk.pengajuan.perusahaan
	get_perusahaan.short_description = "Perusahaan"

	def get_perusahaan_lokasi(self, obj):
		if obj.pengajuan.perusahaan.desa:
			return obj.pengajuan.perusahaan.desa.kecamatan
	get_perusahaan_lokasi.short_description = "Kec. Lokasi"

	def get_pemohon(self, obj):
		return obj.pengajuan.pemohon
	get_pemohon.short_description = "Pemohon"

	def get_aksi(self, obj):
		aksi = ''
		status = obj.status
		if status == 4 or status == 8:
			aksi = mark_safe("""
				<a href="%s" title='Proses'> %s </a>
				""" % (reverse('admin:cek_kelengkapan', args=(obj.pengajuan.id, obj.id )), '<i class="fa fa-circle-o-notch"></i>' ))
		if status == 1:
			aksi = mark_safe("""
				<a href="%s" title='Lihat'> %s </a>
				""" % (reverse('admin:cek_kelengkapan', args=(obj.pengajuan.id, obj.id )), '<i class="fa fa-external-link"></i>' ))
		
		return aksi
	get_aksi.short_description = "Aksi"

	def changelist_view(self, request, extra_context={}):
		self.request = request
		extra_context.update({'kecamatan': Kecamatan.objects.filter(kabupaten__provinsi__kode='35', kabupaten__kode='06') })
		extra_context.update({'perusahaan': Perusahaan.objects.all() })
		return super(SurveyAdmin, self).changelist_view(request, extra_context=extra_context)

	def view_cek_kelengkapan_pengajuan(self, request, id_pengajuan_izin_, id_survey):
		extra_context = {}
		extra_context.update({'has_permission': True })
		# print request.user
		# queryset_ = self.get_queryset(request)
		queryset_ = Survey.objects.filter(id=id_survey)
		try:
			queryset_ = queryset_.get(pengajuan__id=id_pengajuan_izin_)

			pegawai = Pegawai.objects.all()
			# if not request.user.is_superuser:
			# 	get_pegawai_skpd = Pegawai.objects.get(pk=request.user.id)
			# 	if get_pegawai_skpd.unit_kerja:
			# 		pegawai = pegawai.filter(unit_kerja=get_pegawai_skpd.unit_kerja)
			# 	else:
			# 		pegawai = pegawai.filter(unit_kerja__nama_unit_kerja='PEMBANGUNAN')

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

					if queryset_.pengajuan.perusahaan:
						perusahaan = queryset_.pengajuan.perusahaan
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
								emailto = r.created_by.email
								print emailto
								subject = "Berita Acara Telah dibuat ["+str(queryset_.pengajuan.no_pengajuan)+"]"
								html_content = "Silahkan buka akun anda atau klik link berikut <a href='http://"+str(request.META['HTTP_HOST'])+"/admin/izin/detiliujk/view-pengajuan-iujk/"+str(id_pengajuan_izin_)+"'>Berita Acara</a> <br> <img src='http://simpatik.kedirikab.go.id:8889/static/images/wwa.png' style='background-color: darkgrey;'>"
								sent_ = send_email_notifikasi(emailto, subject, html_content)
								print sent_
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


		except ObjectDoesNotExist:
			raise Http404

		template = loader.get_template("admin/pembangunan/cek_kelengkapan.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))
		
	def surveyselesai(self, request, extra_context={}):
		self.request = request
		# izin = KelompokJenisIzin.objects.all()
		# extra_context.update({'izin': izin})
		return super(SurveyAdmin, self).changelist_view(request, extra_context=extra_context)

	def has_add_permission(self, request):
		if request.user.is_superuser:
			return True
		return False

	def get_queryset(self, request):
		func_view, func_view_args, func_view_kwargs = resolve(request.path)
		qs = super(SurveyAdmin, self).get_queryset(request)
		# print request.user.pegawai.unit_kerja
		# if not request.user.is_superuser:
		# 	qs = qs.filter(skpd=request.user.pegawai.unit_kerja)

		if func_view.__name__ == 'surveyselesai':
			qs = qs.filter(status=1)
		else:
			qs = qs.filter(~Q(status=1))

		return qs

	def save_survey_ajax(self, request):
		frm = SurveyForm(request.POST)
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
			# p.kelompok_jenis_izin_id = request.POST.get('kelompok_jenis_izin_id')
			p.save()

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

			# SAVE PENGAJUAN
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
						print "sending "+str(n.pegawai.email)
						sent_ = send_email_notifikasi(n.pegawai.email, subject, html_content)
						print sent_
				s.save()

				pengajuan = DetilIUJK.objects.get(id=s.pengajuan.id)
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

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(SurveyAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^survey-save-ajax/$', self.save_survey_ajax, name="save_survey_ajax" ),
			url(r'^survey-delete-ajax/$', self.delete_survey_ajax, name="delete_survey_ajax" ),
			url(r'^survey-sending/$', self.send_survey, name="send_survey" ),
			url(r'^do-survey/(?P<id_survey>[0-9]+)$', self.admin_site.admin_view(self.do_survey), name="lakukan_survey" ),
			url(r'^survey-cek-kelengkapan/(?P<id_pengajuan_izin_>[0-9]+)/(?P<id_survey>[0-9]+)$', self.view_cek_kelengkapan_pengajuan, name="cek_kelengkapan" ),
			url(r'^laporan-survey/$', self.admin_site.admin_view(self.surveyselesai), name='survey_selesai'),
			)
		return my_urls + urls

admin.site.register(Survey, SurveyAdmin)