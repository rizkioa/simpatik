import json, datetime, base64
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
from perusahaan.models import DataPimpinan, PemegangSaham, Perusahaan, Legalitas

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
			extra_context.update({'title': 'Proses Pengajuan Persero Terbatas (PT)'})
			pengajuan_ = DetilTDP.objects.get(id=id_pengajuan_izin_)
			alamat_ = ""
			alamat_perusahaan_ = ""
			pemohon_ = pengajuan_.pemohon
			perusahaan_ = pengajuan_.perusahaan
			legalitas_ = {}
			legalitas_pendirian = {}
			legalitas_perubahan = {}
			legalitas_3 = {}
			legalitas_4 = {}
			legalitas_6 = {}
			legalitas_7 = {}
			perusahaan_cabang_ = {}
			if pengajuan_:
				ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pemohon_.id, jenis_identitas_id=1).last()
				paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pemohon_.id, jenis_identitas_id=2).last()
				alamat_ = str(pemohon_.alamat)+", Ds. "+str(pemohon_.desa)+", Kec. "+str(pemohon_.desa.kecamatan)+", "+str(pemohon_.desa.kecamatan.kabupaten)
				if perusahaan_:
					alamat_perusahaan_ = str(perusahaan_.alamat_perusahaan)+", Ds. "+str(perusahaan_.desa)+", Kec. "+str(perusahaan_.desa.kecamatan)+", "+str(perusahaan_.desa.kecamatan.kabupaten)
					legalitas_ = perusahaan_.legalitas_set.all()
					legalitas_pendirian = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=1).last()
					legalitas_perubahan = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=2).last()
					legalitas_3 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=3).last()
					legalitas_4 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=4).last()
					legalitas_6 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=6).last()
					legalitas_7 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=7).last()
				izin_lain_ = IzinLain.objects.filter(pengajuan_izin_id=pengajuan_.id)
				data_pimpinan_ = DataPimpinan.objects.filter(detil_tdp_id=pengajuan_.id)
				pemegang_saham_ = PemegangSaham.objects.filter(pengajuan_izin_id=pengajuan_.id)
				if perusahaan_:
					perusahaan_cabang_ = Perusahaan.objects.filter(perusahaan_induk_id=perusahaan_.id)
				wni = 0
				if pengajuan_.jumlah_karyawan_wni:
					wni = pengajuan_.jumlah_karyawan_wni
				wna = 0
				if pengajuan_.jumlah_karyawan_wna:
					wna = pengajuan_.jumlah_karyawan_wna
				jumlah_karyawan = int(wni)+int(wna)
				# print jumlah_karyawan
				extra_context.update({'pengajuan':pengajuan_, 'pemohon': pemohon_, 'alamat_pemohon': alamat_, 'perusahaan':perusahaan_, 'alamat_perusahaan':alamat_perusahaan_, 'ktp':ktp_, 'paspor':paspor_, 'status': pengajuan_.status, 'legalitas':legalitas_, 'izin_lain':izin_lain_, 'data_pimpinan':data_pimpinan_, 'pemegang_saham':pemegang_saham_, 'perusahaan_cabang':perusahaan_cabang_, 'jumlah_karyawan':jumlah_karyawan, 'legalitas_pendirian':legalitas_pendirian, 'legalitas_perubahan':legalitas_perubahan, 'legalitas_3':legalitas_3, 'legalitas_4':legalitas_4, 'legalitas_6':legalitas_6, 'legalitas_7':legalitas_7})
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
			pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_izin_)
			legalitas_1 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=3).last()
			# print legalitas_1.tanggal_pengesahan
			legalitas_2 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=4).last()
			legalitas_3 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=6).last()
			skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
			alamat_ = str(pengajuan_.perusahaan.alamat_perusahaan) + "Ds." + str(pengajuan_.perusahaan.desa.nama_desa) + ", Kec." +str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan) + ", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten)
			if skizin_:
				extra_context.update({'skizin': skizin_ })
			masa_berlaku = ''
			if skizin_:
				masa_berlakua = skizin_.created_at + relativedelta(years=5)
				masa_berlaku = masa_berlakua.strftime('%d-%m-%Y')
			extra_context.update({'pengajuan': pengajuan_ , 'legalitas_1':legalitas_1, 'legalitas_2':legalitas_2, 'legalitas_3':legalitas_3, 'masa_berlaku':masa_berlaku, 'alamat': alamat_})
		template = loader.get_template("front-end/include/formulir_tdp_pt/cetak_tdp_pt_asli.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def view_pengajuan_tdp_cv(self, request, id_pengajuan_izin_):
		extra_context = {}
		extra_context.update({'has_permission': True })
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan TDP Persekutuan Komenditer (CV)'})
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
			alamat_ = str(pengajuan_.perusahaan.alamat_perusahaan) + "Ds." + str(pengajuan_.perusahaan.desa.nama_desa) + ", Kec." +str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan) + ", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten)
			if skizin_:
				extra_context.update({'skizin': skizin_ })
			masa_berlaku = ''
			if skizin_:
				masa_berlakua = skizin_.created_at + relativedelta(years=5)
				masa_berlaku = masa_berlakua.strftime('%d-%m-%Y')
			extra_context.update({'pengajuan': pengajuan_ , 'legalitas_1':legalitas_1, 'legalitas_2':legalitas_2, 'legalitas_3':legalitas_3, 'masa_berlaku':masa_berlaku, 'alamat': alamat_})
		template = loader.get_template("front-end/include/formulir_tdp_cv/cetak_tdp_cv_asli.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def view_pengajuan_tdp_perorangan(self, request, id_pengajuan_izin_):
		extra_context = {}
		extra_context.update({'has_permission': True })
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan TDP Perorangan (PO)'})
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
				if pengajuan_.jenis_permohonan_id == 1:
					masa_berlaku = ''
					if pengajuan_.created_at:
						masa_berlaku_ = pengajuan_.created_at + relativedelta(years=5)
						masa_berlaku = masa_berlaku_.strftime('%d-%m-%Y')
						extra_context.update({'masa_berlaku':masa_berlaku})
				extra_context.update({'pengajuan':pengajuan_, 'pemohon': pemohon_, 'alamat_pemohon': alamat_, 'perusahaan':perusahaan_, 'alamat_perusahaan':alamat_perusahaan_, 'ktp':ktp_, 'paspor':paspor_, 'status': pengajuan_.status, 'legalitas':legalitas_, 'izin_lain':izin_lain_, 'data_pimpinan':data_pimpinan_, 'pemegang_saham':pemegang_saham_, 'perusahaan_cabang':perusahaan_cabang_, 'jumlah_karyawan':jumlah_karyawan})
				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
				riwayat_ = Riwayat.objects.filter(pengajuan_izin_id = id_pengajuan_izin_).order_by('created_at')
				if riwayat_:
					extra_context.update({'riwayat': riwayat_ })
				skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
				if skizin_:
					extra_context.update({'skizin': skizin_, 'skizin_status': skizin_.status })
		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_tdp_perorangan.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_tdp_perorangan_asli(self, request, id_pengajuan_izin_):
		
		extra_context = {}
		if id_pengajuan_izin_:
			# pengajuan_ = DetilTDP.objects.get_object_or_404(id=id_pengajuan_izin_)
			pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_izin_)
			legalitas_1 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=3).last()
			# print legalitas_1.tanggal_pengesahan
			legalitas_2 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=4).last()
			legalitas_3 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=6).last()
			skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
			alamat_ = str(pengajuan_.perusahaan.alamat_perusahaan) + "Ds." + str(pengajuan_.perusahaan.desa.nama_desa) + ", Kec." +str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan) + ", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten)
			if skizin_:
				extra_context.update({'skizin': skizin_ })
			masa_berlaku = ''
			if skizin_:
				masa_berlaku_ = skizin_.created_at + relativedelta(years=5)
				masa_berlaku = masa_berlaku_.strftime('%d-%m-%Y')

			extra_context.update({'pengajuan': pengajuan_ , 'legalitas_1':legalitas_1, 'legalitas_2':legalitas_2, 'legalitas_3':legalitas_3, 'masa_berlaku':masa_berlaku, 'alamat': alamat_})
		template = loader.get_template("front-end/include/formulir_tdp_po/cetak_tdp_po_asli.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def view_pengajuan_tdp_firma(self, request, id_pengajuan_izin_):
		extra_context = {}
		extra_context.update({'has_permission': True })
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan TDP Firma'})
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
				extra_context.update({'pengajuan':pengajuan_, 'pemohon': pemohon_, 'alamat_pemohon': alamat_, 'perusahaan':perusahaan_, 'alamat_perusahaan':alamat_perusahaan_, 'ktp':ktp_, 'paspor':paspor_, 'status': pengajuan_.status, 'legalitas':legalitas_, 'izin_lain':izin_lain_, 'data_pimpinan':data_pimpinan_, 'pemegang_saham':pemegang_saham_, 'perusahaan_cabang':perusahaan_cabang_, 'jumlah_karyawan':jumlah_karyawan})
				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
				riwayat_ = Riwayat.objects.filter(pengajuan_izin_id = id_pengajuan_izin_).order_by('created_at')
				if riwayat_:
					extra_context.update({'riwayat': riwayat_ })
				skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
				if skizin_:
					extra_context.update({'skizin': skizin_, 'skizin_status': skizin_.status })
		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_tdp_firma.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_tdp_firma_asli(self, request, id_pengajuan_izin_):
		
		extra_context = {}
		if id_pengajuan_izin_:
			# pengajuan_ = DetilTDP.objects.get_object_or_404(id=id_pengajuan_izin_)
			pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_izin_)
			legalitas_1 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=3).last()
			# print legalitas_1.tanggal_pengesahan
			legalitas_2 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=4).last()
			legalitas_3 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=6).last()
			skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
			alamat_ = str(pengajuan_.perusahaan.alamat_perusahaan) + "Ds." + str(pengajuan_.perusahaan.desa.nama_desa) + ", Kec." +str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan) + ", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten)
			if skizin_:
				extra_context.update({'skizin': skizin_ })
			masa_berlaku = ''
			if skizin_:
				masa_berlakua = skizin_.created_at + relativedelta(years=5)
				masa_berlaku = masa_berlakua.strftime('%d-%m-%Y')
			extra_context.update({'pengajuan': pengajuan_ , 'legalitas_1':legalitas_1, 'legalitas_2':legalitas_2, 'legalitas_3':legalitas_3, 'masa_berlaku':masa_berlaku, 'alamat': alamat_})
		template = loader.get_template("front-end/include/formulir_tdp_firma/cetak_tdp_firma_asli.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def view_pengajuan_tdp_bul(self, request, id_pengajuan_izin_):
		extra_context = {}
		extra_context.update({'has_permission': True })
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan TDP Badan Usaha Lainnya (BUL)'})
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
				# print jumlah_karyawan
				legalitas_pendirian = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=1).last()
				extra_context.update({'pengajuan':pengajuan_, 'pemohon': pemohon_, 'alamat_pemohon': alamat_, 'perusahaan':perusahaan_, 'alamat_perusahaan':alamat_perusahaan_, 'ktp':ktp_, 'paspor':paspor_, 'status': pengajuan_.status, 'legalitas':legalitas_, 'izin_lain':izin_lain_, 'data_pimpinan':data_pimpinan_, 'pemegang_saham':pemegang_saham_, 'perusahaan_cabang':perusahaan_cabang_, 'jumlah_karyawan':jumlah_karyawan, 'legalitas_pendirian':legalitas_pendirian})
				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
				riwayat_ = Riwayat.objects.filter(pengajuan_izin_id = id_pengajuan_izin_).order_by('created_at')
				if riwayat_:
					extra_context.update({'riwayat': riwayat_ })
				skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
				if skizin_:
					extra_context.update({'skizin': skizin_, 'skizin_status': skizin_.status })
		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_tdp_bul.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def view_pengajuan_tdp_koperasi(self, request, id_pengajuan_izin_):
		extra_context = {}
		extra_context.update({'has_permission': True })
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan TDP Koperasi'})
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
				# print jumlah_karyawan
				legalitas_pendirian = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=1).last()
				legalitas_perubahan = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=2).last()
				legalitas_8 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=8).last()
				legalitas_9 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=9).last()
				extra_context.update({'pengajuan':pengajuan_, 'pemohon': pemohon_, 'alamat_pemohon': alamat_, 'perusahaan':perusahaan_, 'alamat_perusahaan':alamat_perusahaan_, 'ktp':ktp_, 'paspor':paspor_, 'status': pengajuan_.status, 'legalitas':legalitas_, 'izin_lain':izin_lain_, 'data_pimpinan':data_pimpinan_, 'pemegang_saham':pemegang_saham_, 'perusahaan_cabang':perusahaan_cabang_, 'jumlah_karyawan':jumlah_karyawan, 'legalitas_pendirian':legalitas_pendirian, 'legalitas_perubahan':legalitas_perubahan, 'legalitas_8':legalitas_8, 'legalitas_9':legalitas_9})
				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
				riwayat_ = Riwayat.objects.filter(pengajuan_izin_id = id_pengajuan_izin_).order_by('created_at')
				if riwayat_:
					extra_context.update({'riwayat': riwayat_ })
				skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
				if skizin_:
					extra_context.update({'skizin': skizin_, 'skizin_status': skizin_.status })
		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_tdp_koperasi.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_tdp_bul_asli(self, request, id_pengajuan_izin_):
		
		extra_context = {}
		if id_pengajuan_izin_:
			pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_izin_)
			legalitas_1 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=3).last()
			# print legalitas_1.tanggal_pengesahan
			legalitas_2 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=4).last()
			legalitas_3 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=6).last()
			skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
			alamat_ = str(pengajuan_.perusahaan.alamat_perusahaan) + "Ds." + str(pengajuan_.perusahaan.desa.nama_desa) + ", Kec." +str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan) + ", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten)
			if skizin_:
				extra_context.update({'skizin': skizin_ })
			masa_berlaku = ''
			if skizin_:
				masa_berlakua = skizin_.created_at + relativedelta(years=5)
				masa_berlaku = masa_berlakua.strftime('%d-%m-%Y')
			extra_context.update({'pengajuan': pengajuan_ , 'legalitas_1':legalitas_1, 'legalitas_2':legalitas_2, 'legalitas_3':legalitas_3, 'masa_berlaku':masa_berlaku, 'alamat': alamat_
				})
		template = loader.get_template("front-end/include/formulir_tdp_bul/cetak_tdp_bul_asli.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_tdp_koperasi_asli(self, request, id_pengajuan_izin_):
		
		extra_context = {}
		if id_pengajuan_izin_:
			pengajuan_ = get_object_or_404(DetilTDP, id=id_pengajuan_izin_)
			legalitas_1 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=3).last()
			# print legalitas_1.tanggal_pengesahan
			legalitas_2 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=4).last()
			legalitas_3 = pengajuan_.perusahaan.legalitas_set.filter(jenis_legalitas_id=6).last()
			skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
			alamat_ = str(pengajuan_.perusahaan.alamat_perusahaan) + "Ds." + str(pengajuan_.perusahaan.desa.nama_desa) + ", Kec." +str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan) + ", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten)
			if skizin_:
				extra_context.update({'skizin': skizin_ })
			masa_berlaku = ''
			if skizin_:
				masa_berlakua = skizin_.created_at + relativedelta(years=5)
				masa_berlaku = masa_berlakua.strftime('%d-%m-%Y')
			extra_context.update({'pengajuan': pengajuan_ , 'legalitas_1':legalitas_1, 'legalitas_2':legalitas_2, 'legalitas_3':legalitas_3, 'masa_berlaku':masa_berlaku, 'alamat': alamat_})
		template = loader.get_template("front-end/include/formulir_tdp_bul/cetak_tdp_koperasi_asli.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def edit_skizin_tdp(self, request):
		if request.POST:
			id_pengajuan_izin = request.POST.get('id_pengajuan_izin')
			pengajuan_ = DetilTDP.objects.filter(id=id_pengajuan_izin).last()
			if pengajuan_:
				produk_utama = request.POST.get('produk_utama')
				status_waralaba = request.POST.get('status_waralaba')
				status_perusahaan = request.POST.get('status_perusahaan', None)
				# # save pengajuan
				pengajuan_.produk_utama = produk_utama
				pengajuan_.status_waralaba = status_waralaba
				# # save skizin
				status_pendaftaran = request.POST.get('status_pendaftaran')
				status_pembaharuan_ke = request.POST.get('status_pembaharuan_ke')
				if pengajuan_.jenis_permohonan.id == 1:
					masa_berlaku_ = pengajuan_.created_at + relativedelta(years=5)
					masa_berlaku = masa_berlaku_.strftime('%Y-%m-%d')
				else:
					if request.POST.get('masa_berlaku'):
						masa_berlaku = request.POST.get('masa_berlaku')
						masa_berlaku = datetime.datetime.strptime(masa_berlaku, '%d-%m-%Y').strftime('%Y-%m-%d')
				
				try:
					skizin = SKIzin.objects.get(pengajuan_izin=pengajuan_)
					skizin.status_perusahaan = status_perusahaan
					skizin.status_pendaftaran = status_pendaftaran
					skizin.status_pembaharuan_ke = status_pembaharuan_ke
					skizin.masa_berlaku_izin = masa_berlaku
					skizin.status = 11
				except ObjectDoesNotExist:
					skizin = SKIzin(pengajuan_izin_id=pengajuan_.id,status_pendaftaran=status_pendaftaran, status_pembaharuan_ke=status_pembaharuan_ke, masa_berlaku_izin=masa_berlaku, status=11, status_perusahaan=status_perusahaan)

				pengajuan_.save()
				skizin.save()
				data = {'success': True, 'pesan': 'Proses Selesai.'}
			else:
				data = {'success': False, 'pesan': 'Proses Selesai.'}
		else:
			data = {'success': False, 'pesan': 'Proses Selesai.'}
		response = HttpResponse(json.dumps(data))
		return response

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilTDPAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^view-pengajuan-tdp-pt/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_tdp_pt), name='view_pengajuan_tdp_pt'),
			url(r'^view-pengajuan-tdp-cv/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_tdp_cv), name='view_pengajuan_tdp_cv'),
			url(r'^view-pengajuan-tdp-firma/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_tdp_firma), name='view_pengajuan_tdp_firma'),
			url(r'^view-pengajuan-tdp-perorangan/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_tdp_perorangan), name='view_pengajuan_tdp_perorangan'),
			url(r'^view-pengajuan-tdp-bul/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_tdp_bul), name='view_pengajuan_tdp_bul'),
			url(r'^view-pengajuan-tdp-koperasi/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_tdp_koperasi), name='view_pengajuan_tdp_koperasi'),
			url(r'^cetak-tdp-pt-asli/(?P<id_pengajuan_izin_>[0-9 A-Za-z_\-=]+)$', self.admin_site.admin_view(self.cetak_tdp_pt_asli), name='cetak_tdp_pt_asli'),
			url(r'^cetak-tdp-cv-asli/(?P<id_pengajuan_izin_>[0-9 A-Za-z_\-=]+)$', self.admin_site.admin_view(self.cetak_tdp_cv_asli), name='cetak_tdp_cv_asli'),
			url(r'^cetak-tdp-perorangan-asli/(?P<id_pengajuan_izin_>[0-9 A-Za-z_\-=]+)$', self.admin_site.admin_view(self.cetak_tdp_perorangan_asli), name='cetak_tdp_perorangan_asli'),
			url(r'^cetak-tdp-firma-asli/(?P<id_pengajuan_izin_>[0-9 A-Za-z_\-=]+)$', self.admin_site.admin_view(self.cetak_tdp_firma_asli), name='cetak_tdp_firma_asli'),
			url(r'^cetak-tdp-bul-asli/(?P<id_pengajuan_izin_>[0-9 A-Za-z_\-=]+)$', self.admin_site.admin_view(self.cetak_tdp_bul_asli), name='cetak_tdp_bul_asli'),
			url(r'^cetak-tdp-koperasi-asli/(?P<id_pengajuan_izin_>[0-9 A-Za-z_\-=]+)$', self.admin_site.admin_view(self.cetak_tdp_koperasi_asli), name='cetak_tdp_koperasi_asli'),
			url(r'^edit-skizin-tdp/$', self.admin_site.admin_view(self.edit_skizin_tdp), name='edit_skizin_tdp'),
			)
		return my_urls + urls

admin.site.register(DetilTDP, DetilTDPAdmin)