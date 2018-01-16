import base64, datetime
from django.contrib import admin
from django.contrib.auth.models import Group
from izin.models import DetilIMBPapanReklame, Syarat, SKIzin, Riwayat, DetilSk, DetilPembayaran, Survey, BankPembayaran
from kepegawaian.models import Pegawai,UnitKerja
from accounts.models import NomorIdentitasPengguna
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, resolve
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseForbidden
from izin.utils import *

class DetilIMBPapanReklameAdmin(admin.ModelAdmin):
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
		if split_[0] == 'IMB Reklame':
			no_pengajuan = mark_safe("""
				<a href="%s" target="_blank"> %s </a>
				""" % (reverse('admin:izin_detilimbpapanreklame_change', args=(obj.id,)), obj.no_pengajuan ))
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
					'fields': ('pemohon','perusahaan')
					}
				),
				('Detail Izin', {'fields': ('kelompok_jenis_izin', 'jenis_permohonan','no_pengajuan', 'no_izin','legalitas')}),
				('Detail Kuasa', {'fields': ('nama_kuasa','no_identitas_kuasa','telephone_kuasa',) }),
				('Detail IMB Papan Reklame', {'fields': ('jenis_papan_reklame','lebar','tinggi','lokasi_pasang','desa','batas_utara','batas_timur','batas_selatan','batas_barat') }),
				('Berkas & Keterangan', {'fields': ('berkas_tambahan', 'keterangan',)}),

				('Lain-lain', {'fields': ('status', 'created_by', 'created_at', 'verified_by', 'verified_at', 'updated_at')}),
			)
		else:
			add_fieldsets = (
				(None, {
					'classes': ('wide',),
					'fields': ('pemohon','perusahaan')
					}
				),
				('Detail Izin', {'fields': ('kelompok_jenis_izin', 'jenis_permohonan','no_pengajuan', 'no_izin','legalitas')}),
				('Detail Kuasa', {'fields': ('nama_kuasa','no_identitas_kuasa','telephone_kuasa',) }),
				('Detail IMB Papan Reklame', {'fields': ('jenis_papan_reklame','lebar','tinggi','lokasi_pasang','desa','batas_utara','batas_timur','batas_selatan','batas_barat') }),
				('Berkas & Keterangan', {'fields': ('berkas_tambahan', 'keterangan',)}),
			)
		return add_fieldsets


	def view_pengajuan_imb_reklame(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan IMB Reklame'})
			pengajuan_ = get_object_or_404(DetilIMBPapanReklame, id=id_pengajuan_izin_)
			extra_context.update({'skpd_list' : UnitKerja.objects.all() })
			extra_context.update({'survey_pengajuan' : pengajuan_.survey_pengajuan.last()})
			extra_context.update({'pengajuan': pengajuan_})
			extra_context.update({'has_permission': True })
			banyak = DetilIMBPapanReklame.objects.count()
			extra_context.update({'banyak': banyak})
			syarat_ = Syarat.objects.filter(jenis_izin__jenis_izin__kode="reklame")
			extra_context.update({'syarat': syarat_})
			skizin_ = pengajuan_.skizin_set.last()
			extra_context.update({'skizin': skizin_ })
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
			except Survey.DoesNotExist:
				s = ''

			extra_context.update({'survey': s })

			if pengajuan_.status == 5:
				import datetime
				tahun = datetime.date.today().strftime("%Y")
				jumlah_data = int(DetilPembayaran.objects.filter(tanggal_dibuat__year=tahun).count())+1
				# nomor_kwitansi = get_nomor_kwitansi("974/"+str(jumlah_data),str(pengajuan_.id)+"/DPMPTSP")
				nomor_kwitansi = get_nomor_kwitansi("974", str(jumlah_data), "DPMPTSP")
				kode = generate_kode_bank_jatim(jumlah_data)
				bank_list = BankPembayaran.objects.filter(aktif=True)
				total_biaya = ""
				if total_biaya:
					total_biaya = formatrupiah(total_biaya)
				# if pengajuan_.detilbangunanimb_set.last().total_biaya_detil:
				# 	total_biaya = int(float(pengajuan_.detilbangunanimb_set.last().total_biaya_detil))
				extra_context.update({
					'kode': kode,
					'bank_pembayaran': bank_list,
					'nomor_kwitansi': nomor_kwitansi,
					'peruntukan': "IZIN MENDIRIKAN BANGUNAN (IMB) REKLAME",
					'total_biaya': total_biaya
					})
			extra_context.update({
				'detil_pembayaran': pengajuan_.detilpembayaran_set.last()
				})

		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_imb_reklame.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_sk_imb_reklame(self, request, id_pengajuan_izin_, salinan_=None):
		extra_context = {}
		# id_pengajuan_izin_ = base64.b64decode(id_pengajuan_izin_)
		# print id_pengajuan_izin_
		if id_pengajuan_izin_:
			extra_context.update({'salinan': salinan_})
			# pengajuan_ = DetilIMBPapanReklame.objects.get(id=id_pengajuan_izin_)
			pengajuan_ = get_object_or_404(DetilIMBPapanReklame, id=id_pengajuan_izin_)
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.pemohon.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({'alamat_perusahaan': alamat_perusahaan_})
				extra_context.update({'perusahaan': pengajuan_.perusahaan })
			letak_ = pengajuan_.lokasi_pasang +", Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())
			ukuran_ = "Lebar = "+str(int(pengajuan_.lebar))+" M, Tinggi = "+str(int(pengajuan_.tinggi))+" M"  
			jumlah_ = str(int(pengajuan_.jumlah))
			klasifikasi_ = pengajuan_.klasifikasi_jalan

			extra_context.update({'jumlah': jumlah_ })
			extra_context.update({'klasifikasi_jalan': klasifikasi_ })
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
			except DetilSk.DoesNotExist:
				pass
			try:
				retribusi_ = DetilPembayaran.objects.filter(pengajuan_izin__id = id_pengajuan_izin_).last()
				if retribusi_:
					if retribusi_.jumlah_pembayaran and retribusi_.jumlah_pembayaran is not None:
						n = int(retribusi_.jumlah_pembayaran.replace(".", ""))
						terbilang_ = terbilang(n)
						extra_context.update({'terbilang': terbilang_ })
					extra_context.update({'retribusi': retribusi_ })
			except ObjectDoesNotExist:
				pass
		template = loader.get_template("front-end/include/formulir_imb_reklame/cetak_sk_imb_reklame.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_skizin_imb_reklame_pdf(self, request, id_pengajuan):
		from izin.utils import render_to_pdf, cek_apikey
		extra_context = {}
		username = request.GET.get('username')
		apikey = request.GET.get('api_key')
		cek = cek_apikey(apikey, username)
		if cek == True:
			if id_pengajuan:
				pengajuan_ = get_object_or_404(DetilIMBPapanReklame, id=id_pengajuan)
				alamat_ = ""
				alamat_perusahaan_ = ""
				if pengajuan_.pemohon:
					if pengajuan_.pemohon.desa:
						alamat_ = str(pengajuan_.pemohon.alamat)+", "+pengajuan_.pemohon.desa.lokasi_lengkap()
						extra_context.update({'alamat_pemohon': alamat_})
					extra_context.update({'pemohon': pengajuan_.pemohon})
				if pengajuan_.perusahaan:
					if pengajuan_.perusahaan.desa:
						alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
						extra_context.update({'alamat_perusahaan': alamat_perusahaan_})
					extra_context.update({'perusahaan': pengajuan_.perusahaan })
				letak_ = ""
				if pengajuan_.lokasi_pasang:
					letak_ = pengajuan_.lokasi+", "
				if pengajuan_.desa:
					letak_ = pengajuan_.desa.lokasi_lengkap()
				ukuran_ = "Lebar = "+str(int(pengajuan_.lebar))+" M, Tinggi = "+str(int(pengajuan_.tinggi))+" M"  
				jumlah_ = pengajuan_.jumlah
				klasifikasi_ = pengajuan_.klasifikasi_jalan

				extra_context.update({'jumlah': jumlah_ })
				extra_context.update({'klasifikasi_jalan': klasifikasi_ })
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
					sk_imb_ = DetilSk.objects.get(pengajuan_izin__id = id_pengajuan)
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
			else:
				raise Http404
		else:
			# raise Http404
			return HttpResponseForbidden()
		return render(request, "front-end/include/formulir_imb_reklame/cetak_skizin_imb_reklame_pdf.html", extra_context)


	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilIMBPapanReklameAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^cetak-sk-imb-reklame/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.cetak_sk_imb_reklame), name='cetak_sk_imb_reklame'),
			url(r'^cetak-sk-imb-reklame/(?P<id_pengajuan_izin_>[0-9]+)/(?P<salinan_>\w+)$', self.admin_site.admin_view(self.cetak_sk_imb_reklame), name='cetak_sk_imb_reklame'),
			url(r'^view-pengajuan-imb-reklame/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_imb_reklame), name='view_pengajuan_imb_reklame'),
			url(r'^cetak-skizin-imb-reklame-pdf/(?P<id_pengajuan>[0-9]+)/$', self.cetak_skizin_imb_reklame_pdf, name='cetak_skizin_imb_reklame_pdf'),

			)
		return my_urls + urls

admin.site.register(DetilIMBPapanReklame, DetilIMBPapanReklameAdmin)



















