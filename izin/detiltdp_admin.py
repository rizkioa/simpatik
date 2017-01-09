import datetime
import base64
from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, resolve
from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404

from accounts.models import NomorIdentitasPengguna
from izin.models import DetilTDP, Syarat, SKIzin, Riwayat, IzinLain
from perusahaan.models import DataPimpinan, PemegangSaham, Perusahaan

class DetilTDPAdmin(admin.ModelAdmin):
	list_display = ('get_no_pengajuan', 'pemohon', 'get_kelompok_jenis_izin')

	def get_kelompok_jenis_izin(self, obj):
		return obj.kelompok_jenis_izin
	get_kelompok_jenis_izin.short_description = "Izin Pengajuan"

	def get_no_pengajuan(self, obj):
		no_pengajuan = mark_safe("""
			<a href="%s" target="_blank"> %s </a>
			""" % ("#", obj.no_pengajuan ))
		split_ = obj.no_pengajuan.split('/')
		# print split_
		if split_[0] == 'TDP':
			no_pengajuan = mark_safe("""
				<a href="%s" target="_blank"> %s </a>
				""" % (reverse('admin:izin_detiltdp_change', args=(obj.id,)), obj.no_pengajuan ))
		return no_pengajuan
	get_no_pengajuan.short_description = "No. Pengajuan"

	def view_pengajuan_tdp_pt(self, request, id_pengajuan_izin_):
		extra_context = {}
		extra_context.update({'has_permission': True })
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			pengajuan_ = DetilTDP.objects.get(id=id_pengajuan_izin_)
			alamat_ = ""
			alamat_perusahaan_ = ""
			pemohon_ = pengajuan_.pemohon
			perusahaan_ = pengajuan_.perusahaan
			if pengajuan_:
				ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pemohon_.id, jenis_identitas_id=1).last()
				paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pemohon_.id, jenis_identitas_id=2).last()
				alamat_ = str(pemohon_.alamat)+", Ds. "+str(pemohon_.desa)+", Kec. "+str(pemohon_.desa.kecamatan)+", "+str(pemohon_.desa.kecamatan.kabupaten)
				alamat_perusahaan_ = str(perusahaan_.alamat_perusahaan)+", Ds. "+str(perusahaan_.desa)+", Kec. "+str(perusahaan_.desa.kecamatan)+", "+str(perusahaan_.desa.kecamatan.kabupaten)
				legalitas_ = perusahaan_.legalitas_set.all()
				izin_lain_ = IzinLain.objects.filter(pengajuan_izin_id=pengajuan_.id)
				data_pimpinan_ = DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id)
				pemegang_saham_ = PemegangSaham.objects.filter(pengajuan_izin_id=pengajuan_.id)
				perusahaan_cabang_ = Perusahaan.objects.filter(perusahaan_induk_id=perusahaan_.id)
				wni = 0
				if pengajuan_.jumlah_karyawan_wni:
					wni = pengajuan_.jumlah_karyawan_wni
				wna = 0
				if pengajuan_.jumlah_karyawan_wna:
					wna = pengajuan_.jumlah_karyawan_wna
				jumlah_karyawan = int(wni)+int(wna)
				print jumlah_karyawan
				extra_context.update({'pengajuan':pengajuan_, 'pemohon': pemohon_, 'alamat_pemohon': alamat_, 'perusahaan':perusahaan_, 'alamat_perusahaan':alamat_perusahaan_, 'ktp':ktp_, 'paspor':paspor_, 'status': pengajuan_.status, 'legalitas':legalitas_, 'izin_lain':izin_lain_, 'data_pimpinan':data_pimpinan_, 'pemegang_saham':pemegang_saham_, 'perusahaan_cabang':perusahaan_cabang_, 'jumlah_karyawan':jumlah_karyawan})
				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
				riwayat_ = Riwayat.objects.filter(pengajuan_izin_id = id_pengajuan_izin_).order_by('created_at')
				if riwayat_:
					extra_context.update({'riwayat': riwayat_ })
				skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
				if skizin_:
					extra_context.update({'skizin': skizin_, 'skizin_status': skizin_.status })
		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_tdp_pt.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_tdp_pt_asli(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			# pengajuan_ = DetilTDP.objects.get_object_or_404(id=id_pengajuan_izin_)
			pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_izin_)
			legalitas_1 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=3).last()
			# print legalitas_1.tanggal_pengesahan
			legalitas_2 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=4).last()
			legalitas_3 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=6).last()
			skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
			
			if skizin_:
				extra_context.update({'skizin': skizin_ })
			masa_berlaku = ''
			if skizin_:
				masa_berlakua = skizin_.created_at + relativedelta(years=5)
				masa_berlaku = masa_berlakua.strftime('%d-%m-%Y')
			extra_context.update({'pengajuan': pengajuan_ , 'legalitas_1':legalitas_1, 'legalitas_2':legalitas_2, 'legalitas_3':legalitas_3, 'masa_berlaku':masa_berlaku})
		template = loader.get_template("front-end/include/formulir_tdp_pt/cetak_tdp_pt_asli.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def view_pengajuan_tdp_cv(self, request, id_pengajuan_izin_):
		extra_context = {}
		extra_context.update({'has_permission': True })
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			pengajuan_ = DetilTDP.objects.get(id=id_pengajuan_izin_)
			alamat_ = ""
			alamat_perusahaan_ = ""
			pemohon_ = pengajuan_.pemohon
			perusahaan_ = pengajuan_.perusahaan
			if pengajuan_:
				ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pemohon_.id, jenis_identitas_id=1).last()
				paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pemohon_.id, jenis_identitas_id=2).last()
				alamat_ = str(pemohon_.alamat)+", Ds. "+str(pemohon_.desa)+", Kec. "+str(pemohon_.desa.kecamatan)+", "+str(pemohon_.desa.kecamatan.kabupaten)
				alamat_perusahaan_ = str(perusahaan_.alamat_perusahaan)+", Ds. "+str(perusahaan_.desa)+", Kec. "+str(perusahaan_.desa.kecamatan)+", "+str(perusahaan_.desa.kecamatan.kabupaten)
				legalitas_ = perusahaan_.legalitas_set.all()
				izin_lain_ = IzinLain.objects.filter(pengajuan_izin_id=pengajuan_.id)
				data_pimpinan_ = DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id)
				pemegang_saham_ = PemegangSaham.objects.filter(pengajuan_izin_id=pengajuan_.id)
				perusahaan_cabang_ = Perusahaan.objects.filter(perusahaan_induk_id=perusahaan_.id)
				wni = 0
				if pengajuan_.jumlah_karyawan_wni:
					wni = pengajuan_.jumlah_karyawan_wni
				wna = 0
				if pengajuan_.jumlah_karyawan_wna:
					wna = pengajuan_.jumlah_karyawan_wna
				jumlah_karyawan = int(wni)+int(wna)
				print jumlah_karyawan
				extra_context.update({'pengajuan':pengajuan_, 'pemohon': pemohon_, 'alamat_pemohon': alamat_, 'perusahaan':perusahaan_, 'alamat_perusahaan':alamat_perusahaan_, 'ktp':ktp_, 'paspor':paspor_, 'status': pengajuan_.status, 'legalitas':legalitas_, 'izin_lain':izin_lain_, 'data_pimpinan':data_pimpinan_, 'pemegang_saham':pemegang_saham_, 'perusahaan_cabang':perusahaan_cabang_, 'jumlah_karyawan':jumlah_karyawan})
				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
				riwayat_ = Riwayat.objects.filter(pengajuan_izin_id = id_pengajuan_izin_).order_by('created_at')
				if riwayat_:
					extra_context.update({'riwayat': riwayat_ })
				skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
				if skizin_:
					extra_context.update({'skizin': skizin_, 'skizin_status': skizin_.status })
		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_tdp_cv.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_tdp_cv_asli(self, request, id_pengajuan_izin_):
		
		extra_context = {}
		if id_pengajuan_izin_:
			# pengajuan_ = DetilTDP.objects.get_object_or_404(id=id_pengajuan_izin_)
			pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_izin_)
			legalitas_1 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=3).last()
			# print legalitas_1.tanggal_pengesahan
			legalitas_2 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=4).last()
			legalitas_3 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=6).last()
			skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
			
			if skizin_:
				extra_context.update({'skizin': skizin_ })
			masa_berlaku = ''
			if skizin_:
				masa_berlakua = skizin_.created_at + relativedelta(years=5)
				masa_berlaku = masa_berlakua.strftime('%d-%m-%Y')
			extra_context.update({'pengajuan': pengajuan_ , 'legalitas_1':legalitas_1, 'legalitas_2':legalitas_2, 'legalitas_3':legalitas_3, 'masa_berlaku':masa_berlaku})
		template = loader.get_template("front-end/include/formulir_tdp_cv/cetak_tdp_cv_asli.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))


	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilTDPAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^view-pengajuan-tdp-pt/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_tdp_pt), name='view_pengajuan_tdp_pt'),
			url(r'^view-pengajuan-tdp-cv/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_tdp_cv), name='view_pengajuan_tdp_cv'),
			url(r'^cetak-tdp-pt-asli/(?P<id_pengajuan_izin_>[0-9 A-Za-z_\-=]+)$', self.admin_site.admin_view(self.cetak_tdp_pt_asli), name='cetak_tdp_pt_asli'),
			url(r'^cetak-tdp-cv-asli/(?P<id_pengajuan_izin_>[0-9 A-Za-z_\-=]+)$', self.admin_site.admin_view(self.cetak_tdp_cv_asli), name='cetak_tdp_cv_asli'),
			)
		return my_urls + urls

admin.site.register(DetilTDP, DetilTDPAdmin)