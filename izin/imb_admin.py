import base64, datetime
from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, resolve
from django.http import Http404, HttpResponseForbidden

from izin.models import DetilIMB, Syarat, SKIzin, Riwayat,DetilSk,DetilPembayaran,Survey,DetilBangunanIMB,SertifikatTanah
from kepegawaian.models import Pegawai,UnitKerja
from accounts.models import NomorIdentitasPengguna

from izin.utils import*

import math
from decimal import *
import locale, datetime

locale.setlocale(locale.LC_ALL,'id_ID.UTF-8')

class DetilIMBAdmin(admin.ModelAdmin):
	list_display = ('get_no_pengajuan', 'pemohon', 'get_kelompok_jenis_izin','jenis_permohonan', 'status')
	search_fields = ('no_izin', 'pemohon__nama_lengkap')

	def get_kelompok_jenis_izin(self, obj):
		return obj.kelompok_jenis_izin
	get_kelompok_jenis_izin.short_description = "Izin Pengajuan"

	def get_no_pengajuan(self, obj):
		no_pengajuan = mark_safe("""
			<a href="%s" target="_blank"> %s </a>
			""" % ("#", obj.no_pengajuan ))
		split_ = obj.no_pengajuan.split('/')
		# print split_
		if split_[0] == 'IMB':
			no_pengajuan = mark_safe("""
				<a href="%s" target="_blank"> %s </a>
				""" % (reverse('admin:izin_detilimb_change', args=(obj.id,)), obj.no_pengajuan ))
		return no_pengajuan
	get_no_pengajuan.short_description = "No. Pengajuan"


	def get_readonly_fields(self, request, obj=None):
		rf = ('verified_by', 'verified_at', 'created_by', 'created_at', 'updated_at')
		if obj:
			if not request.user.is_superuser:
				rf = rf+('status',)
		return rf

	def get_fieldsets(self, request, obj = None):
		if obj or request.user.is_superuser:
			add_fieldsets = (
				(None, {
					'classes': ('wide',),
					'fields': ('pemohon',)
					}
				),
				('Detail Izin', {'fields': ('kelompok_jenis_izin', 'jenis_permohonan','no_pengajuan', 'no_izin','legalitas')}),
				('Detail Kuasa', {'fields': ('nama_kuasa','no_identitas_kuasa','telephone_kuasa',) }),
				('Detail IMB', {'fields': ('bangunan','luas_bangunan','panjang','jumlah_bangunan','luas_tanah','no_surat_tanah','tanggal_surat_tanah','lokasi','desa','status_hak_tanah','kepemilikan_tanah','klasifikasi_jalan','ruang_milik_jalan','ruang_pengawasan_jalan','total_biaya','luas_bangunan_lama','no_imb_lama','tanggal_imb_lama','batas_utara','batas_timur','batas_selatan','batas_barat')}),
				('Berkas & Keterangan', {'fields': ('berkas_tambahan', 'keterangan',)}),

				('Lain-lain', {'fields': ('status', 'created_by', 'created_at', 'verified_by', 'verified_at', 'updated_at')}),
			)
		else:
			add_fieldsets = (
				(None, {
					'classes': ('wide',),
					'fields': ('pemohon',)
					}
				),
				('Detail Izin', {'fields': ('kelompok_jenis_izin', 'jenis_permohonan','no_pengajuan', 'no_izin','legalitas')}),
				('Detail Kuasa', {'fields': ('nama_kuasa','no_identitas_kuasa','telephone_kuasa',) }),
				('Detail IMB', {'fields': ('bangunan','luas_bangunan','panjang','jumlah_bangunan','luas_tanah','no_surat_tanah','tanggal_surat_tanah','lokasi','desa','status_hak_tanah','kepemilikan_tanah','klasifikasi_jalan','ruang_milik_jalan','ruang_pengawasan_jalan','total_biaya','luas_bangunan_lama','no_imb_lama','tanggal_imb_lama','batas_utara','batas_timur','batas_selatan','batas_barat')}),
				('Berkas & Keterangan', {'fields': ('berkas_tambahan', 'keterangan',)}),
			)
		return add_fieldsets

	def view_pengajuan_imb_umum(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			extra_context.update({'skpd_list' : UnitKerja.objects.all() })

			queryset_ = Survey.objects.filter(pengajuan__id=id_pengajuan_izin_)
			# pengajuan_ = DetilIMB.objects.get(id=id_pengajuan_izin_)
			pengajuan_ = get_object_or_404(DetilIMB, id=id_pengajuan_izin_)
			extra_context.update({'survey_pengajuan' : pengajuan_.survey_pengajuan.all().last() })

			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
				nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all().last()
				extra_context.update({'nomor_identitas': nomor_identitas_ })
				# if pengajuan_.parameter_bangunan:
				# 	fungsi_bangunan = pengajuan_.parameter_bangunan.filter(parameter="Fungsi Bangunan")
				# 	detil_parameter = fungsi_bangunan.last()
				# 	if detil_parameter:
				# 		detil_ = detil_parameter.detil_parameter
						
				# 		extra_context.update({'detil_': detil_})
				try:
					ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id).last()
					extra_context.update({'cookie_file_ktp': ktp_.berkas })
				except ObjectDoesNotExist:
					pass
			if pengajuan_.desa:
				letak_ = pengajuan_.lokasi + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
			else:
				letak_ = ""
			# extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})
			pengajuan_id = pengajuan_.id
			extra_context.update({'letak_pemasangan': letak_})
			extra_context.update({'klasifikasi_jalan': JENIS_LOKASI_USAHA })
			extra_context.update({'rumija': RUMIJA })
			extra_context.update({'ruwasja': RUWASJA })
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})
			extra_context.update({'status': pengajuan_.status})
			extra_context.update({'pengajuan': pengajuan_})
			# encode_pengajuan_id = (str(pengajuan_.id))
			extra_context.update({'pengajuan_id': pengajuan_id })
			#+++++++++++++ page logout ++++++++++
			extra_context.update({'has_permission': True })
			#+++++++++++++ end page logout ++++++++++

			# lama_pemasangan = pengajuan_.tanggal_akhir-pengajuan_.tanggal_mulai
			# print lama_pemasangan
			banyak = len(DetilIMB.objects.all())
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
					# print s.survey_iujk.all()
			except ObjectDoesNotExist:
				s = ''

			extra_context.update({'survey': s })

			# SURVEY

			try:
				sk_imb_ = DetilSk.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
				if sk_imb_:
					extra_context.update({'sk_imb': sk_imb_ })
			except ObjectDoesNotExist:
				pass
				# print "WASEM"

	  		sertifikat_tanah_list = SertifikatTanah.objects.filter(pengajuan_izin=pengajuan_id)

	  		extra_context.update({'sertifikat_tanah_list': sertifikat_tanah_list})

			try:
				detil_bangunan_ = DetilBangunanIMB.objects.filter(detil_izin_imb=pengajuan_,parameter_bangunan__parameter="Fungsi Bangunan").last()
				if detil_bangunan_:
					fungsi_bangunan = detil_bangunan_.parameter_bangunan.filter(parameter="Fungsi Bangunan")
					detil_parameter = fungsi_bangunan.last()
					# print detil_parameter.detil_parameter
					if detil_parameter:
						detil_ = detil_parameter.detil_parameter
						extra_context.update({'detil_': detil_})
			except ObjectDoesNotExist:
				pass

		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_imb_umum.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_sk_imb_umum(self, request, id_pengajuan_izin_, salinan_=None):
		extra_context = {}
		# id_pengajuan_izin_ = base64.b64decode(id_pengajuan_izin_)
		# print id_pengajuan_izin_
		if id_pengajuan_izin_:
			extra_context.update({'salinan': salinan_})
			# pengajuan_ = DetilIMB.objects.get(id=id_pengajuan_izin_)
			pengajuan_ = get_object_or_404(DetilIMB, id=id_pengajuan_izin_)
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
				
			letak_ = pengajuan_.lokasi + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
			ukuran_ = "Lebar = "+str(int(pengajuan_.luas_bangunan))+" M, Tinggi = "+str(int(pengajuan_.luas_tanah))+" M"  

			extra_context.update({'ukuran': ukuran_})
			extra_context.update({'letak_pemasangan': letak_})
			nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
			extra_context.update({'nomor_identitas': nomor_identitas_ })
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'pengajuan': pengajuan_ })
			extra_context.update({'foto': pengajuan_.pemohon.berkas_foto.all().last()})
			try:
				skizin_ = SKIzin.objects.get(pengajuan_izin_id = id_pengajuan_izin_ )
				if skizin_:
					extra_context.update({'skizin': skizin_ })
					extra_context.update({'skizin_status': skizin_.status })
			except ObjectDoesNotExist:
				pass
			try:
				kepala_ =  Pegawai.objects.get(jabatan__nama_jabatan="Kepala Dinas")
				if kepala_:
					extra_context.update({'gelar_depan': kepala_.gelar_depan })
					extra_context.update({'nama_kepala_dinas': kepala_.nama_lengkap })
					extra_context.update({'nip_kepala_dinas': kepala_.nomoridentitaspengguna_set.last() })

			except ObjectDoesNotExist:
				pass
			try:
				sk_imb_ = DetilSk.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
				if sk_imb_:
					extra_context.update({'sk_imb': sk_imb_ })
			except ObjectDoesNotExist:
				pass
			try:
				retribusi_ = DetilPembayaran.objects.filter(pengajuan_izin__id = id_pengajuan_izin_).last()
				if retribusi_:
					j = retribusi_.jumlah_pembayaran.replace(".", "")
					if int(j) != 0:
						# j = retribusi_.jumlah_pembayaran.replace(".", "")
						p = j.replace(",", ".")
						q = math.ceil(float(p))
						n = int(str(q).replace(".0", ""))
						terbilang_ = terbilang(n)
					else:
						n = int(retribusi_.jumlah_pembayaran)
						terbilang_ = terbilang(n)	
					extra_context.update({'retribusi': n })
					extra_context.update({'terbilang': terbilang_ })
			except ObjectDoesNotExist:
				pass
			try:
				detil_bangunan_ = DetilBangunanIMB.objects.filter(detil_izin_imb=pengajuan_)
				bk_1 = detil_bangunan_.filter(detil_bangunan_imb__kode="BK23").last()
				if bk_1:
					extra_context.update({'bk_1': bk_1 })
				if detil_bangunan_:
					
			  		total_luas_tanah_detil = pengajuan_.luas_bangunan
			  		for x in detil_bangunan_:
			  			if x.total_luas != None:
			  				if x.satuan_luas != "M2" or x.satuan_luas != "M&sup2;":
					  			total_luas_tanah_detil = Decimal(total_luas_tanah_detil)+x.total_luas

					# detil_total_luas_keseluruhan = ", Luas Keseluruhan = "+str(total_luas_tanah_detil)+" "+mark_safe("M&sup2;")
					 		
				  	detil_ = str(pengajuan_.luas_bangunan)+""+mark_safe(" M&sup2;")
				  	for x in detil_bangunan_:
				  		if x.detil_bangunan_imb.nama_bangunan == "Gedung":
				  			detil_ = detil_
				  		else:
				  			if x.satuan_luas == "M1":
				  				satuan = "M&sup1;"
				  			elif x.satuan_luas == "M2":
				  				satuan = "M&sup2;"
				  			else:
				  				satuan = x.satuan_luas				  			
				  			detil_ = detil_ +", "+str(x.detil_bangunan_imb.nama_bangunan)+" : "+str(x.total_luas)+" "+mark_safe(satuan)
				  	# + " ,  ".join( if x.detil_bangunan_imb.nama_bangunan == "Gedung" str(x.detil_bangunan_imb.nama_bangunan)+" : "+str(x.total_luas)+" "+mark_safe(x.satuan_luas) )+", Luas Keseluruhan = "+str(total_luas_tanah_detil)+" "+mark_safe("M&sup2;")
			  		extra_context.update({'detil_bangunan': detil_ })
					# extra_context.update({'detil_bangunan': detil_bangunan_ })

			except ObjectDoesNotExist:
				pass

	  		sertifikat_tanah_list = SertifikatTanah.objects.filter(pengajuan_izin=pengajuan_)

	  		if sertifikat_tanah_list.exists():
		  		total_luas_tanah = 0
		  		for x in sertifikat_tanah_list:
		  			total_luas_tanah = Decimal(total_luas_tanah)+x.luas_sertifikat_petak
		  		if sertifikat_tanah_list.count() > 1:
		  			extra_context.update({'luas_sertifikat_tanah_list': ", ".join(str(x.luas_sertifikat_petak)+" "+mark_safe("M&sup2;") for x in sertifikat_tanah_list)})
		  		else:
		  			extra_context.update({'luas_sertifikat_tanah_list': ", ".join(str(x.luas_sertifikat_petak)+" "+mark_safe("M&sup2;") for x in sertifikat_tanah_list)})

		  		if x.tahun_sertifikat:
		  			tahun_sertifikat_ = " Tanggal "+ x.tahun_sertifikat.strftime('%d %B %Y')
		  		else:
		  			tahun_sertifikat_ = '-'
		  		
		  		if x.tahun_sertifikat:
			  		extra_context.update({'sertifikat_tanah_list': ", ".join(x.no_sertifikat_petak +" Tanggal "+ x.tahun_sertifikat.strftime('%d %B %Y') for x in sertifikat_tanah_list)})
			  	else:
			  	 	extra_context.update({'sertifikat_tanah_list': ", ".join(x.no_sertifikat_petak for x in sertifikat_tanah_list)})
		  	else:
		  		extra_context.update({'sertifikat_tanah_list': pengajuan_.no_surat_tanah +" Tanggal "+ pengajuan_.tanggal_surat_tanah.strftime('%d %B %Y')})
		  		extra_context.update({'luas_sertifikat_tanah_list': str(pengajuan_.luas_tanah)+" "+mark_safe("M&sup2;")})

		template = loader.get_template("front-end/include/imb_umum/cetak_sk_imb_umum.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def view_pengajuan_imb_perumahan(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			extra_context.update({'skpd_list' : UnitKerja.objects.all() })

			queryset_ = Survey.objects.filter(pengajuan__id=id_pengajuan_izin_)
			# pengajuan_ = DetilIMB.objects.get(id=id_pengajuan_izin_)
			pengajuan_ = get_object_or_404(DetilIMB, id=id_pengajuan_izin_)
			extra_context.update({'survey_pengajuan' : pengajuan_.survey_pengajuan.all().last() })
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.pemohon.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
				nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all().last()
				extra_context.update({'nomor_identitas': nomor_identitas_ })
				try:
					ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id).last()
					extra_context.update({'cookie_file_ktp': ktp_.berkas })
				except ObjectDoesNotExist:
					pass
				letak_ = ''
				if pengajuan_.lokasi:
					letak_ = pengajuan_.lokasi + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
			# extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})
			pengajuan_id = pengajuan_.id
			extra_context.update({'letak_pemasangan': letak_})
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})
			extra_context.update({'status': pengajuan_.status})
			extra_context.update({'pengajuan': pengajuan_})
			# encode_pengajuan_id = (str(pengajuan_.id))
			extra_context.update({'pengajuan_id': pengajuan_id })
			#+++++++++++++ page logout ++++++++++
			extra_context.update({'has_permission': True })
			#+++++++++++++ end page logout ++++++++++

			# lama_pemasangan = pengajuan_.tanggal_akhir-pengajuan_.tanggal_mulai
			# print lama_pemasangan
			banyak = len(DetilIMB.objects.all())
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
			except ObjectDoesNotExist:
				s = ''

			extra_context.update({'survey': s })
			try:
				detil_bangunan_ = DetilBangunanIMB.objects.filter(detil_izin_imb=pengajuan_,parameter_bangunan__parameter="Fungsi Bangunan").last()
				if detil_bangunan_:
					fungsi_bangunan = detil_bangunan_.parameter_bangunan.filter(parameter="Fungsi Bangunan")
					detil_parameter = fungsi_bangunan.last()
					# print detil_parameter.detil_parameter
					if detil_parameter:
						detil_ = detil_parameter.detil_parameter
						extra_context.update({'detil_': detil_})
			except ObjectDoesNotExist:
				pass

		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_imb_perumahan.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_sk_imb_perumahan(self, request, id_pengajuan_izin_, salinan_=None):
		extra_context = {}
		# id_pengajuan_izin_ = base64.b64decode(id_pengajuan_izin_)
		# print id_pengajuan_izin_
		if id_pengajuan_izin_:
			extra_context.update({'salinan': salinan_})
			# pengajuan_ = DetilIMB.objects.get(id=id_pengajuan_izin_)
			pengajuan_ = get_object_or_404(DetilIMB, id=id_pengajuan_izin_)
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.pemohon.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
			# if pengajuan_.perusahaan:
			# 	if pengajuan_.perusahaan.desa:
			# 		alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
			# 		extra_context.update({'alamat_perusahaan': alamat_perusahaan_})
			# 	extra_context.update({'perusahaan': pengajuan_.perusahaan })
			letak_ = pengajuan_.lokasi + ", Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())
			ukuran_ = "Lebar = "+str(int(pengajuan_.luas_bangunan))+" M, Tinggi = "+str(int(pengajuan_.luas_tanah))+" M"  

			extra_context.update({'ukuran': ukuran_})
			extra_context.update({'letak_pemasangan': letak_})
			nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
			extra_context.update({'nomor_identitas': nomor_identitas_ })
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'pengajuan': pengajuan_ })
			extra_context.update({'foto': pengajuan_.pemohon.berkas_foto.all().last()})
			try:
				skizin_ = SKIzin.objects.get(pengajuan_izin_id = id_pengajuan_izin_ )
				if skizin_:
					extra_context.update({'skizin': skizin_ })
					extra_context.update({'skizin_status': skizin_.status })
			except ObjectDoesNotExist:
				pass
			try:
				kepala_ =  Pegawai.objects.get(jabatan__nama_jabatan="Kepala Dinas")
				if kepala_:
					extra_context.update({'gelar_depan': kepala_.gelar_depan })
					extra_context.update({'nama_kepala_dinas': kepala_.nama_lengkap })
					extra_context.update({'nip_kepala_dinas': kepala_.nomoridentitaspengguna_set.last() })

			except ObjectDoesNotExist:
				pass
			try:
				sk_imb_ = DetilSk.objects.get(pengajuan_izin__id = id_pengajuan_izin_ )
				if sk_imb_:
					extra_context.update({'sk_imb': sk_imb_ })
			except ObjectDoesNotExist:
				pass
			try:
				retribusi_ = DetilPembayaran.objects.filter(pengajuan_izin__id = id_pengajuan_izin_).last()
				if retribusi_:
					j = retribusi_.jumlah_pembayaran.replace(".", "")
					if int(j) != 0:
						n = int(retribusi_.jumlah_pembayaran.replace(".", ""))
						terbilang_ = terbilang(n)
					else:
						n = int(retribusi_.jumlah_pembayaran)
						terbilang_ = terbilang(n)
					extra_context.update({'retribusi': retribusi_ })
					extra_context.update({'terbilang': terbilang_ })
			except ObjectDoesNotExist:
				pass
		template = loader.get_template("front-end/include/formulir_imb_perumahan/cetak_sk_imb_perumahan.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_skizin_imb_umum_pdf(self, request, id_pengajuan):
		from izin.utils import render_to_pdf, cek_apikey
		extra_context = {}
		username = request.GET.get('username')
		apikey = request.GET.get('api_key')
		cek = cek_apikey(apikey, username)
		if cek == True:
			if id_pengajuan:
				# extra_context.update({'salinan': salinan_})
				# pengajuan_ = DetilIMB.objects.get(id=id_pengajuan_izin_)
				pengajuan_ = get_object_or_404(DetilIMB, id=id_pengajuan)
				alamat_ = ""
				alamat_perusahaan_ = ""
				if pengajuan_.pemohon:
					if pengajuan_.pemohon.desa:
						alamat_ = str(pengajuan_.pemohon.alamat)+", "+pengajuan_.pemohon.desa.lokasi_lengkap()
						extra_context.update({'alamat_pemohon': alamat_})
					extra_context.update({'pemohon': pengajuan_.pemohon})
				letak_ = ""
				if pengajuan_.lokasi:
					letak_ = pengajuan_.lokasi+", "
				if pengajuan_.desa:
					letak_ = pengajuan_.desa.lokasi_lengkap()
				ukuran_ = "Lebar = "+str(int(pengajuan_.luas_bangunan))+" M, Tinggi = "+str(int(pengajuan_.luas_tanah))+" M"  

				extra_context.update({'ukuran': ukuran_})
				extra_context.update({'letak_pemasangan': letak_})
				nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
				extra_context.update({'nomor_identitas': nomor_identitas_ })
				extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
				extra_context.update({'pengajuan': pengajuan_ })
				extra_context.update({'foto': pengajuan_.pemohon.berkas_foto.all().last()})
				try:
					skizin_ = SKIzin.objects.get(pengajuan_izin_id = id_pengajuan)
					if skizin_:
						extra_context.update({'skizin': skizin_ })
						extra_context.update({'skizin_status': skizin_.status })
				except ObjectDoesNotExist:
					pass
				try:
					kepala_ =  Pegawai.objects.get(jabatan__nama_jabatan="Kepala Dinas")
					if kepala_:
						extra_context.update({'gelar_depan': kepala_.gelar_depan })
						extra_context.update({'nama_kepala_dinas': kepala_.nama_lengkap })
						extra_context.update({'nip_kepala_dinas': kepala_.nomoridentitaspengguna_set.last() })

				except ObjectDoesNotExist:
					pass
				try:
					sk_imb_ = DetilSk.objects.get(pengajuan_izin_id = id_pengajuan )
					if sk_imb_:
						extra_context.update({'sk_imb': sk_imb_ })
				except ObjectDoesNotExist:
					pass
				try:
					retribusi_ = DetilPembayaran.objects.filter(pengajuan_izin__id = id_pengajuan).last()
					if retribusi_:
						n = int(retribusi_.jumlah_pembayaran.replace(".", ""))
						terbilang_ = terbilang(n)
						extra_context.update({'retribusi': retribusi_ })
						extra_context.update({'terbilang': terbilang_ })
				except ObjectDoesNotExist:
					pass
				try:
					detil_bangunan_ = DetilBangunanIMB.objects.filter(detil_izin_imb=pengajuan_)
					bk_1 = detil_bangunan_.filter(detil_bangunan_imb__kode="BK23").last()
					if bk_1:
						extra_context.update({'bk_1': bk_1 })
					if detil_bangunan_:
						extra_context.update({'detil_bangunan': detil_bangunan_ })
				except ObjectDoesNotExist:
					pass
			else:
				raise Http404
		else:
			return HttpResponseForbidden()
		return render(request, "front-end/include/imb_umum/cetak_skizin_imb_umum_pdf.html", extra_context)
		
	def cetak_skizin_imb_perumahan_pdf(self, request, id_pengajuan):
		from izin.utils import render_to_pdf, cek_apikey
		extra_context = {}
		username = request.GET.get('username')
		apikey = request.GET.get('api_key')
		cek = cek_apikey(apikey, username)
		if cek == True:
			if id_pengajuan:
				# extra_context.update({'salinan': salinan_})
				# pengajuan_ = DetilIMB.objects.get(id=id_pengajuan_izin_)
				pengajuan_ = get_object_or_404(DetilIMB, id=id_pengajuan)
				alamat_ = ""
				alamat_perusahaan_ = ""
				if pengajuan_.pemohon:
					if pengajuan_.pemohon.desa:
						alamat_ = str(pengajuan_.pemohon.alamat)+", "+pengajuan_.pemohon.desa.lokasi_lengkap()
						extra_context.update({'alamat_pemohon': alamat_})
					extra_context.update({'pemohon': pengajuan_.pemohon})
				letak_ = ""
				if pengajuan_.lokasi:
					letak_ = pengajuan_.lokasi+", "
				if pengajuan_.desa:
					letak_ = pengajuan_.desa.lokasi_lengkap()
				ukuran_ = "Lebar = "+str(int(pengajuan_.luas_bangunan))+" M, Tinggi = "+str(int(pengajuan_.luas_tanah))+" M"  

				extra_context.update({'ukuran': ukuran_})
				extra_context.update({'letak_pemasangan': letak_})
				nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
				extra_context.update({'nomor_identitas': nomor_identitas_ })
				extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
				extra_context.update({'pengajuan': pengajuan_ })
				extra_context.update({'foto': pengajuan_.pemohon.berkas_foto.all().last()})
				try:
					skizin_ = SKIzin.objects.get(pengajuan_izin_id = id_pengajuan)
					if skizin_:
						extra_context.update({'skizin': skizin_ })
						extra_context.update({'skizin_status': skizin_.status })
				except ObjectDoesNotExist:
					pass
				try:
					kepala_ =  Pegawai.objects.get(jabatan__nama_jabatan="Kepala Dinas")
					if kepala_:
						extra_context.update({'gelar_depan': kepala_.gelar_depan })
						extra_context.update({'nama_kepala_dinas': kepala_.nama_lengkap })
						extra_context.update({'nip_kepala_dinas': kepala_.nomoridentitaspengguna_set.last() })

				except ObjectDoesNotExist:
					pass
				try:
					sk_imb_ = DetilSk.objects.get(pengajuan_izin_id = id_pengajuan )
					if sk_imb_:
						extra_context.update({'sk_imb': sk_imb_ })
				except ObjectDoesNotExist:
					pass
				try:
					retribusi_ = DetilPembayaran.objects.filter(pengajuan_izin__id = id_pengajuan).last()
					if retribusi_:
						n = int(retribusi_.jumlah_pembayaran.replace(".", ""))
						terbilang_ = terbilang(n)
						extra_context.update({'retribusi': retribusi_ })
						extra_context.update({'terbilang': terbilang_ })
				except ObjectDoesNotExist:
					pass
				try:
					detil_bangunan_ = DetilBangunanIMB.objects.filter(detil_izin_imb=pengajuan_)
					bk_1 = detil_bangunan_.filter(detil_bangunan_imb__kode="BK23").last()
					if bk_1:
						extra_context.update({'bk_1': bk_1 })
					if detil_bangunan_:
						extra_context.update({'detil_bangunan': detil_bangunan_ })
				except ObjectDoesNotExist:
					pass
			else:
				raise Http404
		else:
			# raise Http404
			return HttpResponseForbidden()
		return render(request, "front-end/include/formulir_imb_perumahan/cetak_skizin_imb_perumahan_pdf.html", extra_context)
		

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilIMBAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^cetak-sk-imb-umum/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.cetak_sk_imb_umum), name='cetak_sk_imb_umum'),
			url(r'^cetak-sk-imb-umum/(?P<id_pengajuan_izin_>[0-9]+)/(?P<salinan_>\w+)/$', self.admin_site.admin_view(self.cetak_sk_imb_umum), name='cetak_sk_imb_umum'),
			url(r'^cetak-sk-imb-perumahan/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.cetak_sk_imb_perumahan), name='cetak_sk_imb_perumahan'),
			url(r'^cetak-sk-imb-perumahan/(?P<id_pengajuan_izin_>[0-9]+)/(?P<salinan_>\w+)/$', self.admin_site.admin_view(self.cetak_sk_imb_perumahan), name='cetak_sk_imb_perumahan'),
			url(r'^view-pengajuan-imb-umum/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_imb_umum), name='view_pengajuan_imb_umum'),
			url(r'^view-pengajuan-imb-perumahan/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_imb_perumahan), name='view_pengajuan_imb_perumahan'),
			url(r'^cetak-skizin-imb-umum-pdf/(?P<id_pengajuan>[0-9]+)/$', self.cetak_skizin_imb_umum_pdf, name='cetak_skizin_imb_umum_pdf'),
			url(r'^cetak-skizin-imb-perumahan-pdf/(?P<id_pengajuan>[0-9]+)/$', self.cetak_skizin_imb_perumahan_pdf, name='cetak_skizin_imb_perumahan_pdf'),

			)
		return my_urls + urls

admin.site.register(DetilIMB, DetilIMBAdmin)