import json
from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from accounts.models import NomorIdentitasPengguna
from kepegawaian.models import Pegawai, UnitKerja
from izin.models import DetilTDUP , Syarat, SKIzin, Riwayat, Survey, DetilSk, DetilPembayaran

class DetilTDUPAdmin(admin.ModelAdmin):

	def view_pengajuan_izin_tdup(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			pengajuan_ = DetilTDUP.objects.get(id=id_pengajuan_izin_)
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
				try:
					try:
						ktp_ = NomorIdentitasPengguna.objects.get(user_id=pengajuan_.pemohon.id)
					except MultipleObjectsReturned:
						ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id).order_by('id').first()
					extra_context.update({'cookie_file_ktp': ktp_.berkas })
				except ObjectDoesNotExist:
					pass
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({'alamat_perusahaan': alamat_perusahaan_ })
				extra_context.update({'perusahaan': pengajuan_.perusahaan})

				legalitas_pendirian = pengajuan_.perusahaan.legalitas_set.filter(berkas__keterangan="akta pendirian").last()
				legalitas_perubahan = pengajuan_.perusahaan.legalitas_set.filter(berkas__keterangan="akta perubahan").last()
				extra_context.update({ 'legalitas_pendirian': legalitas_pendirian })
				extra_context.update({ 'legalitas_perubahan': legalitas_perubahan })
			letak_ = pengajuan_.lokasi_usaha_pariwisata + ", Desa "+str(pengajuan_.desa_lokasi) + ", Kec. "+str(pengajuan_.desa_lokasi.kecamatan)+", "+ str(pengajuan_.desa_lokasi.kecamatan.kabupaten)
			# extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})
			pengajuan_id = pengajuan_.id
			extra_context.update({'letak': letak_})
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})
			extra_context.update({'status': pengajuan_.status})
			extra_context.update({'pengajuan': pengajuan_})
			# encode_pengajuan_id = (str(pengajuan_.id))


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
				print s.survey_reklame_ho.all()
				extra_context.update({'detilbap': s.survey_reklame_ho.all().last() })
			except ObjectDoesNotExist:
				s = ''

			extra_context.update({'survey': s })
			# END UNTUK SURVEY

			extra_context.update({'pengajuan_id': pengajuan_id })
			#+++++++++++++ page logout ++++++++++
			extra_context.update({'has_permission': True })
			#+++++++++++++ end page logout ++++++++++

			# lama_pemasangan = pengajuan_.tanggal_akhir-pengajuan_.tanggal_mulai
			# print lama_pemasangan
			banyak = len(DetilTDUP.objects.all())
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
		template = loader.get_template("admin/izin/pengajuanizin/view_izin_tdup.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	# def get_provinsi(request):
	# 	provinsi_list = Provinsi.objects.all()
		
	# 	id_negara = request.POST.get('negara', None)	
	# 	if id_negara and not id_negara is "":
	# 		provinsi_list = provinsi_list.filter(negara__id=id_negara)
	# 	nama_provinsi = request.POST.get('nama_provinsi', None)
	# 	if nama_provinsi and not nama_provinsi is "":
	# 		provinsi_list = provinsi_list.filter(nama_provinsi=nama_provinsi)

	# 	return provinsi_list

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilTDUPAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^view-pengajuan-tdup/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_izin_tdup), name='view_pengajuan_izin_tdup'),

			)
		return my_urls + urls

admin.site.register(DetilTDUP, DetilTDUPAdmin)