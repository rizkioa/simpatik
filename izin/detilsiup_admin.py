import base64
import json
from datetime import date
from django.http import Http404
from django.db.models import Q
from django.contrib import admin
from django.core.urlresolvers import reverse, resolve
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404
from mobile.cors import CORSHttpResponse
from izin.models import PengajuanIzin, DetilSIUP, DetilReklame, DetilTDP, DetilIUJK, DetilIMB, DetilHO, DetilHuller, Pemohon, Syarat, SKIzin, Riwayat, JenisIzin
from perusahaan.models import Perusahaan, KBLI
from accounts.models import NomorIdentitasPengguna
from izin.utils import formatrupiah, detil_pengajuan_siup_view, terbilang
from izin import models as app_models
from izin.izin_forms import SKIzinForm
from kepegawaian.models import Pegawai

class DetilSIUPAdmin(admin.ModelAdmin):
	list_display = ('get_no_pengajuan', 'pemohon', 'get_kelompok_jenis_izin','jenis_permohonan', 'status')
	search_fields = ('no_izin', 'pemohon__nama_lengkap')
	# fieldsets = [
	# 	('Detil SIUP',	{'fields':['pemohon', 'get_no_pengajuan']}),
	# ]
	# 
	# def get_fieldsets(self, request, obj = None):
	# 	if request.user.is_superuser:
	# 		add_fieldsets = (
	# 			(None, {
	# 				'classes': ('wide',),
	# 				'fields': ('get_no_pengajuan', 'get_kelompok_jenis_izin')
	# 				})
	# 			)

	def get_kelompok_jenis_izin(self, obj):
		return obj.kelompok_jenis_izin
	get_kelompok_jenis_izin.short_description = "Izin Pengajuan"

	def get_no_pengajuan(self, obj):
		no_pengajuan = mark_safe("""
			<a href="%s" > %s </a>
			""" % ("#", obj.no_pengajuan ))
		split_ = obj.no_pengajuan.split('/')
		# print split_
		if split_[0] == 'SIUP':
			no_pengajuan = mark_safe("""
				<a href="%s" target="_blank"> %s </a>
				""" % (reverse('admin:izin_detilsiup_change', args=(obj.id,)), obj.no_pengajuan ))
		return no_pengajuan
	get_no_pengajuan.short_description = "No. Pengajuan"

	def get_fieldsets(self, request, obj=None):
		fields = ('pemohon', 'kelompok_jenis_izin', 'jenis_permohonan', 'no_pengajuan', 'no_izin', 'nama_kuasa', 'no_identitas_kuasa', 'telephone_kuasa', 'berkas_tambahan', 'perusahaan', 'berkas_foto', 'berkas_npwp_pemohon', 'berkas_npwp_perusahaan', 'legalitas', 'kbli', 'kelembagaan', 'bentuk_kegiatan_usaha', 'jenis_penanaman_modal', 'kekayaan_bersih', 'total_nilai_saham', 'presentase_saham_nasional', 'presentase_saham_asing')
		fields_admin = ('status', 'created_by', 'verified_by', 'rejected_by')
		fields_edit = ('pemohon', 'kelompok_jenis_izin', 'jenis_permohonan', 'nama_kuasa', 'no_identitas_kuasa', 'telephone_kuasa', 'berkas_tambahan', 'perusahaan', 'berkas_foto', 'berkas_npwp_pemohon', 'berkas_npwp_perusahaan', 'legalitas', 'kbli', 'kelembagaan', 'bentuk_kegiatan_usaha', 'jenis_penanaman_modal', 'kekayaan_bersih', 'total_nilai_saham', 'presentase_saham_nasional', 'presentase_saham_asing')
		if obj:
			if request.user.is_superuser:
				add_fieldsets = (
					# ('Pemohon', {
					# 	'classes': ('wide',),
					# 	'fields': ('pemohon',),
					# 	}),
					('Detil SIUP', {
						'classes': ('wide',),
						'fields': fields+fields_admin
						}),
				)
			elif request.user.groups.filter(name='Operator') or request.user.groups.filter(name='Kabid') or request.user.groups.filter(name='Kadin') or request.user.groups.filter(name='Pembuat Surat') or request.user.groups.filter(name='Penomoran'):
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': fields_edit
						}),
				)
			else:
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': fields_edit+('no_pengajuan',)
						}),
					)
		else:
			pass
		return add_fieldsets

	def get_readonly_fields(self, request, obj=None):
		rf = ('pemohon', 'kelompok_jenis_izin', 'jenis_permohonan', 'no_pengajuan', 'no_izin', 'nama_kuasa', 'no_identitas_kuasa', 'telephone_kuasa', 'berkas_tambahan', 'perusahaan', 'berkas_foto', 'berkas_npwp_pemohon', 'berkas_npwp_perusahaan', 'legalitas', 'kbli', 'kelembagaan', 'bentuk_kegiatan_usaha', 'jenis_penanaman_modal', 'kekayaan_bersih', 'total_nilai_saham', 'presentase_saham_nasional', 'presentase_saham_asing')
		rf_admin = ('status', 'created_by', 'verified_by', 'rejected_by')
		rf_superuser = (None,)
		# if request.user.is_superuser:
		# 	return rf
		if request.user.groups.filter(name='Penomoran'):
			rf = ('no_pengajuan')
			return rf
		elif request.user.groups.filter(name='Operator'):
			rf = rf_admin
		elif request.user.groups.filter(name='Kabid') or request.user.groups.filter(name='Kadin') or request.user.groups.filter(name='Pembuat Surat') or request.user.groups.filter(name='Penomoran'):
			rf = rf + rf_admin
		else:
			return rf_superuser
		return rf

	def ajax_dashboard(self, request):
		tahun_sekarang = date.today().year
		pemohon = len(Pemohon.objects.all())
		perusahaan = len(Perusahaan.objects.all())
		pengajuan_selesai = len(PengajuanIzin.objects.filter(status=1))
		pengajuan_proses = len(PengajuanIzin.objects.filter(~Q(status=1) and ~Q(status=6) and ~Q(status=11)))
		# pengajuan_proses = len(PengajuanIzin.objects.filter(status=1))
		pengajuan_siup = len(DetilSIUP.objects.filter(Q(created_at__year=tahun_sekarang) and ~Q(status=11)))
		pengajuan_reklame = len(DetilReklame.objects.filter(Q(created_at__year=tahun_sekarang) and ~Q(status=11)))
		pengajuan_tdp = len(DetilTDP.objects.filter(Q(created_at__year=tahun_sekarang) and ~Q(status=11)))
		pengajuan_uijk = len(DetilIUJK.objects.filter(Q(created_at__year=tahun_sekarang) and ~Q(status=11)))
		pengajuan_imb = len(DetilIMB.objects.filter(Q(created_at__year=tahun_sekarang) and ~Q(status=11)))
		pengajuan_ho = len(DetilHO.objects.filter(Q(created_at__year=tahun_sekarang) and ~Q(status=11)))
		pengajuan_huller = len(DetilHuller.objects.filter(Q(created_at__year=tahun_sekarang) and ~Q(status=11)))
		data = { 'success': True, 'pemohon': pemohon, 'perusahaan': perusahaan, 'pengajuan_selesai': pengajuan_selesai, 'pengajuan_proses': pengajuan_proses, 'pengajuan_siup': pengajuan_siup, 'pengajuan_reklame': pengajuan_reklame, 'pengajuan_tdp': pengajuan_tdp, 'pengajuan_uijk':pengajuan_uijk, 'pengajuan_imb':pengajuan_imb, 'pengajuan_ho':pengajuan_ho, 'pengajuan_huller':pengajuan_huller }
		return CORSHttpResponse(json.dumps(data))

	def ajax_load_pengajuan_siup(self, request, id_pengajuan_):
		data = ""
		if id_pengajuan_:
			pengajuan_list = PengajuanIzin.objects.filter(id=id_pengajuan_)

		return HttpResponse(json.dumps(data))

	def view_pengajuan_siup(self, request, id_pengajuan_izin_):
		extra_context = {}
		skizin_ = SKIzin.objects.filter(pengajuan_izin_id=id_pengajuan_izin_).last()
		if skizin_:
			skizinform = SKIzinForm(instance=skizin_)
			extra_context.update({'form_skizin': skizinform })
			if request.POST:
				# print request.POST
				print str(skizinform['body_html'])
				# skizin_.body_html = str(skizinform['body_html'])
				# skizin_.save()
				# if skizinform.is_valid():
				# 	print skizinform.data['body_html']
				# 	p = skizinform.save(commit=False)
				# 	p.save()
				# else:
				# 	print str(skizinform.errors)
			else:
				print 'sss'

		return detil_pengajuan_siup_view(request, id_pengajuan_izin_, extra_context)

	def detil_siup_view(self, request, id_pengajuan_izin_):
		extra_context = {'detilsiup': 'detilsiup'}
		return detil_pengajuan_siup_view(request, id_pengajuan_izin_, extra_context)

	def cetak_bukti_admin(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			pengajuan = get_object_or_404(PengajuanIzin, id=id_pengajuan_izin_)
			k = pengajuan.kelompok_jenis_izin
			if k.kode == "TDP-PT" or k.kode == "TDP-CV" or k.kode == "TDP-FIRMA" or k.kode == "TDP-PERORANGAN" or k.kode == "TDP-BUL" or k.kode == "TDP-KOPERASI":
				objects_ = getattr(app_models, 'DetilTDP')
			elif k.kode == 'TDUP':
				objects_ = getattr(app_models, 'DetilTDUP')
			else:
				objects_ = getattr(app_models, 'DetilSIUP')


			pengajuan_ = get_object_or_404(objects_, id=id_pengajuan_izin_)
			extra_context.update({'pengajuan': pengajuan_ })
		template = loader.get_template("front-end/include/formulir_siup/cetak_bukti_pendaftaran_admin.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	# def cek_apikey(self, apikey, username):
	# 	# from izin.detilsiup_admin import cek_apikey
	# 	respon = False
	# 	if apikey and username:
	# 		try:
	# 			accounts_obj = Pegawai.objects.get(username=username)
	# 			if accounts_obj.api_key:
	# 				if accounts_obj.api_key.key:
	# 					# print accounts_obj.api_key.key
	# 					# print apikey
	# 					if str(accounts_obj.api_key.key) == str(apikey):
	# 						respon = True
	# 		except ObjectDoesNotExist:
	# 			pass
	# 	return respon

	def cetak_siup_pdf(self, request, id_pengajuan):
		from izin.utils import render_to_pdf, cek_apikey
		extra_context = {}
		username = request.GET.get('username')
		apikey = request.GET.get('api_key')
		cek = cek_apikey(apikey, username)
		if cek == True:
			if id_pengajuan:
				try:
					pengajuan_ = DetilSIUP.objects.get(id=id_pengajuan)
					extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
					extra_context.update({'pengajuan': pengajuan_ })
					extra_context.update({'foto': pengajuan_.pemohon.berkas_foto.all().last()})
					# kelembagaan = pengajuan_.kelembagaan.kelembagaan.upper()
					# extra_context.update({'kelembagaan': kelembagaan })
					if pengajuan_.kekayaan_bersih:
						kekayaan_ = pengajuan_.kekayaan_bersih.replace('.', '')
						terbilang_ = terbilang(int(kekayaan_))
						extra_context.update({'terbilang': str(terbilang_) })
						extra_context.update({ 'kekayaan_bersih': "Rp "+str(pengajuan_.kekayaan_bersih) })
					skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan ).last()
					if skizin_:
						extra_context.update({'skizin': skizin_ })
						extra_context.update({'skizin_status': skizin_.status })
					kepala_ =  Pegawai.objects.filter(jabatan__nama_jabatan="Kepala Dinas").last()
					if kepala_:
						extra_context.update({'kepala_dinas': kepala_ })
						extra_context.update({'nip_kepala_dinas': kepala_.nomoridentitaspengguna_set.last() })
				except ObjectDoesNotExist:
					raise Http404
			else:
				raise Http404
		else:
			raise Http404
		# else:
		# 	raise Http404
		response = render_to_pdf("front-end/include/formulir_siup/cetak_skizin_siup_pdf.html", "Cetak Bukti SIUP", extra_context, request)
		return response


	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilSIUPAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^ajax-dashboard/$', self.ajax_dashboard, name='ajax_dashboard'),
			url(r'^cetak-siup-pdf/(?P<id_pengajuan>[0-9]+)/$', self.cetak_siup_pdf, name='cetak_siup_pdf'),
			url(r'^ajax-load-pengajuan-siup/(?P<id_pengajuan_>[0-9]+)/$', self.admin_site.admin_view(self.ajax_load_pengajuan_siup), name='ajax_load_pengajuan_siup'),
			url(r'^view-pengajuan-siup/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_siup), name='view_pengajuan_siup'),
			url(r'^detil-siup-view/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.detil_siup_view), name='detil_siup_view'),
			url(r'^cetak-bukti-pendaftaran-admin/(?P<id_pengajuan_izin_>[0-9]+)/$', self.admin_site.admin_view(self.cetak_bukti_admin), name='cetak_bukti_admin'),
			)
		return my_urls + urls

admin.site.register(DetilSIUP, DetilSIUPAdmin)