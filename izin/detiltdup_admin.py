import json
from django.contrib import admin
from django.http import HttpResponse
from django.http import Http404
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from accounts.models import NomorIdentitasPengguna
from kepegawaian.models import Pegawai, UnitKerja
from izin.models import DetilTDUP , Syarat, SKIzin, Riwayat, Survey, DetilSk, DetilPembayaran, BidangUsahaPariwisata, JenisUsahaPariwisata, SubJenisUsahaPariwisata, IzinLainTDUP

def get_jenis_usaha(request):
	jenis_usaha_list = JenisUsahaPariwisata.objects.all()
	id_bidang_usaha = request.POST.get('bidang_usaha_pariwisata', None)	
	if id_bidang_usaha and not id_bidang_usaha is "":
		jenis_usaha_list = jenis_usaha_list.filter(bidang_usaha_pariwisata__id=id_bidang_usaha)

	return jenis_usaha_list

def get_sub_jenis_usaha(request):
	sub_jenis_usaha_list = SubJenisUsahaPariwisata.objects.all()
	id_jenis_usaha = request.POST.get('jenis_usaha_pariwisata', None)	
	if id_jenis_usaha and not id_jenis_usaha is "":
		sub_jenis_usaha_list = sub_jenis_usaha_list.filter(jenis_usaha_pariwisata__id=id_jenis_usaha)

	return sub_jenis_usaha_list

class DetilTDUPAdmin(admin.ModelAdmin):

	def view_pengajuan_izin_tdup(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			# pengajuan_ = DetilTDUP.objects.get(id=id_pengajuan_izin_)
			pengajuan_ = get_object_or_404(DetilTDUP, id=id_pengajuan_izin_)
			alamat_ = ""
			alamat_perusahaan_ = ""
			pengurusbadanusaha_list = pengajuan_.pengurusbadanusaha_set.all()
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
				legalitas_list = pengajuan_.perusahaan.legalitas_set.all()
				extra_context.update({ 'legalitas_pendirian': legalitas_pendirian, 'legalitas_perubahan': legalitas_perubahan, 'legalitas_list': legalitas_list })
			rincian = pengajuan_.rincian_sub_jenis
			pengajuan_id = pengajuan_.id
			lokasi_usaha_pariwisata = ''
			if pengajuan_.lokasi_usaha_pariwisata:
				lokasi_usaha_pariwisata = str(pengajuan_.lokasi_usaha_pariwisata) + ', Ds. ' +str(pengajuan_.desa_lokasi)+', Kec. '+str(pengajuan_.desa_lokasi.kecamatan)+', '+str(pengajuan_.desa_lokasi.kecamatan.kabupaten)+', Prov. '+str(pengajuan_.desa_lokasi.kecamatan.kabupaten.provinsi)
			extra_context.update({'pengajuan': pengajuan_, 'rincian': rincian, 'status': pengajuan_.status, 'created_at': pengajuan_.created_at, 'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin, 'lokasi_usaha_pariwisata': lokasi_usaha_pariwisata})

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
			# END UNTUK SURVEY

			izinlaintdup_list = IzinLainTDUP.objects.filter(detil_tdup_id=pengajuan_.id)

			extra_context.update({
				'pengajuan_id': pengajuan_id,
				'pengurusbadanusaha_list': pengurusbadanusaha_list,
				'izinlaintdup_list': izinlaintdup_list
				 })
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

	def cetak_tdup_asli(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			pengajuan_ = get_object_or_404(DetilTDUP, id=id_pengajuan_izin_)
			legalitas_1 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=1).last()
			# print legalitas_1.tanggal_pengesahan
			legalitas_2 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=2).last()
			skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
			alamat_ = str(pengajuan_.perusahaan.alamat_perusahaan) + ", Ds." + str(pengajuan_.perusahaan.desa.nama_desa) + ", Kec." +str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan) + ", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten)
			lokasi_usaha_pariwisata = str(pengajuan_.lokasi_usaha_pariwisata) + ', Ds. ' +str(pengajuan_.desa_lokasi)+', Kec. '+str(pengajuan_.desa_lokasi.kecamatan)+', '+str(pengajuan_.desa_lokasi.kecamatan.kabupaten)+', Prov. '+str(pengajuan_.desa_lokasi.kecamatan.kabupaten.provinsi)
			if skizin_:
				extra_context.update({'skizin': skizin_ })
			masa_berlaku = ''
			if skizin_:
				masa_berlakua = skizin_.created_at + relativedelta(years=5)
				masa_berlaku = masa_berlakua.strftime('%d-%m-%Y')
			izinlaintdup_list = IzinLainTDUP.objects.filter(detil_tdup_id=pengajuan_.id)
			pengurusbadanusaha_list = pengajuan_.pengurusbadanusaha_set.all()
			extra_context.update({'pengajuan': pengajuan_ , 'legalitas_1':legalitas_1, 'legalitas_2':legalitas_2, 'masa_berlaku':masa_berlaku, 'alamat': alamat_, 'lokasi_usaha_pariwisata': lokasi_usaha_pariwisata, 'izinlaintdup': izinlaintdup_list, 'pengurusbadanusaha_list':pengurusbadanusaha_list})
		template = loader.get_template("front-end/include/formulir_tdup/cetak_tdup_asli.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_tdup_pdf(self, request, id_pengajuan):
		from izin.utils import render_to_pdf
		extra_context = {}
		if id_pengajuan:
			pengajuan_ = get_object_or_404(DetilTDUP, id=id_pengajuan)
			legalitas_1 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=1).last()
			# print legalitas_1.tanggal_pengesahan
			legalitas_2 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=2).last()
			skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan ).last()
			masa_berlaku = ''
			if skizin_:
				extra_context.update({'skizin': skizin_ })
				masa_berlakua = skizin_.created_at + relativedelta(years=5)
				masa_berlaku = masa_berlakua.strftime('%d-%m-%Y')
			izinlaintdup_list = IzinLainTDUP.objects.filter(detil_tdup_id=pengajuan_.id)
			pengurusbadanusaha_list = pengajuan_.pengurusbadanusaha_set.all()
			extra_context.update({'pengajuan': pengajuan_ , 'legalitas_1':legalitas_1, 'legalitas_2':legalitas_2, 'masa_berlaku':masa_berlaku, 'izinlaintdup': izinlaintdup_list, 'pengurusbadanusaha_list':pengurusbadanusaha_list})
		else:
			raise Http404
		return render_to_pdf("front-end/include/formulir_tdup/cetak_skizin_tdup_pdf.html", "Cetak Bukti SIUP", extra_context, request)

	def option_jenis_usaha(self, request):
		jenis_usaha_list = get_jenis_usaha(request)
		pilihan = "<option></option>"
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in jenis_usaha_list)));

	def option_sub_jenis_usaha(self, request):
		sub_jenis_usaha_list = get_sub_jenis_usaha(request)
		pilihan = "<option></option>"
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in sub_jenis_usaha_list)));

	def ajax_save_izin_lain(self, request):
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan'] != '':
				if 'id_kelompok_izin' in request.COOKIES.keys():
					nomor_izin = request.POST.get('nomor_izin')
					tanggal_izin = request.POST.get('tanggal_izin')
					izin_lain_, created = IzinLainTDUP.objects.get_or_create(detil_tdup_id = request.COOKIES['id_pengajuan'])
					izin_lain_.nomor_izin = nomor_izin
					izin_lain_.tanggal_izin = tanggal_izin
					izin_lain_.save()

					data = {'success': True, 'pesan': 'Data Usaha Pariwisata berhasil tersimpan.'}
					data = json.dumps(data)
					response = HttpResponse(data) 
				else:
					data = {'success': False, 'pesan': 'Data Kelompok Jenis Izin tidak ditemukan/data kosong.'}
					data = json.dumps(data)
					response = HttpResponse(data)
			else:
				data = {'success': False, 'pesan': 'Data Pengajuan tidak ditemukan/data kosong.'}
				data = json.dumps(data)
				response = HttpResponse(data)
		else:
			data = {'success': False, 'pesan': 'Data Pengajuan tidak ditemukan/data kosong.'}
			data = json.dumps(data)
			response = HttpResponse(data)
		return response

	def load_izin_lain(self, request, pengajuan_id):
		data = []
		if pengajuan_id:
			i = IzinLainTDUP.objects.filter(detil_tdup_id=pengajuan_id)
			data = [obj.as_json() for obj in i]
		
		response = HttpResponse(json.dumps(data), content_type="application/json")
		return response

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilTDUPAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^view-pengajuan-tdup/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_izin_tdup), name='view_pengajuan_izin_tdup'),
			url(r'^cetak-tdup-asli/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.cetak_tdup_asli), name='cetak_tdup_asli'),
			url(r'^option-jenis-usaha/$', self.option_jenis_usaha, name='option_jenis_usaha'),
			url(r'^option-sub-jenis-usaha/$', self.option_sub_jenis_usaha, name='option_sub_jenis_usaha'),
			url(r'^ajax-save-izin-lain/$', self.ajax_save_izin_lain, name='ajax_save_izin_lain'),
			url(r'^load-izin-lain/(?P<pengajuan_id>[0-9]+)$', self.load_izin_lain, name='load_izin_lain'),
			url(r'^cetak-tdup-pdf/(?P<id_pengajuan>[0-9]+)$', self.cetak_tdup_pdf, name='cetak_tdup_pdf'),
			)
		return my_urls + urls

admin.site.register(DetilTDUP, DetilTDUPAdmin)