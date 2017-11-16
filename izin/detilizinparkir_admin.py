from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.template import RequestContext, loader
from accounts.models import NomorIdentitasPengguna
from kepegawaian.models import Pegawai, UnitKerja
from django.core.exceptions import ObjectDoesNotExist
from izin.models import DetilIzinParkirIsidentil, DataAnggotaParkir, Syarat, SKIzin, Riwayat, Survey, DetilSk

class DetilIzinParkirIsidentilAdmin(admin.ModelAdmin):
	list_display = ('pemohon', 'jenis_permohonan', 'status')

	def view_pengajuan_izin_parkir(self, request, id_pengajuan):
		extra_context = {}
		if id_pengajuan:
			extra_context.update({'title': 'Proses Pengajuan Izin Parkir'})
			pengajuan_ = get_object_or_404(DetilIzinParkirIsidentil, id=id_pengajuan)
			data_anggota_list = DataAnggotaParkir.objects.filter(izin_parkir_isidentil_id=pengajuan_.id)
			riwayat_list = Riwayat.objects.filter(pengajuan_izin_id=pengajuan_.id)
			extra_context.update({'pengajuan': pengajuan_, "data_anggota":data_anggota_list, 'pengajuan_id': pengajuan_.id, 'riwayat':riwayat_list})
		# 	#+++++++++++++ page logout ++++++++++
			extra_context.update({'has_permission': True })
		# 	#+++++++++++++ end page logout ++++++++++

			# UNTUK SURVEY
			from django.contrib.auth.models import Group

			extra_context.update({'skpd_list' : UnitKerja.objects.all() })

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
					# print s.survey_iujk.all()
				# print s.survey_reklame_ho.all()
				extra_context.update({'detilbap': s.survey_reklame_ho.all().last() })
			except ObjectDoesNotExist:
				s = ''

			extra_context.update({'survey': s })

			banyak = len(DataAnggotaParkir.objects.all())
			extra_context.update({'banyak': banyak})

			syarat_ = Syarat.objects.filter(jenis_izin__jenis_izin__kode="reklame")
			extra_context.update({'syarat': syarat_})
			try:
				skizin_ = SKIzin.objects.get(pengajuan_izin_id = pengajuan_.id )
				if skizin_:
					extra_context.update({'skizin': skizin_ })
					extra_context.update({'skizin_status': skizin_.status })
			except ObjectDoesNotExist:
				pass

		template = loader.get_template("admin/izin/pengajuanizin/dishub/view_izin_parkir.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilIzinParkirIsidentilAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^view-pengajuan-izin-parkir/(?P<id_pengajuan>[0-9]+)/$', self.admin_site.admin_view(self.view_pengajuan_izin_parkir), name='view_pengajuan_izin_parkir'),
			# url(r'^cetak-tdup-asli/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.cetak_tdup_asli), name='cetak_tdup_asli'),
			# url(r'^option-jenis-usaha/$', self.option_jenis_usaha, name='option_jenis_usaha'),
			# url(r'^option-sub-jenis-usaha/$', self.option_sub_jenis_usaha, name='option_sub_jenis_usaha'),
			# url(r'^ajax-save-izin-lain/$', self.ajax_save_izin_lain, name='ajax_save_izin_lain'),
			# url(r'^load-izin-lain/(?P<pengajuan_id>[0-9]+)$', self.load_izin_lain, name='load_izin_lain'),
			)
		return my_urls + urls

admin.site.register(DetilIzinParkirIsidentil, DetilIzinParkirIsidentilAdmin)