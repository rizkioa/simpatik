from django.contrib import admin
from models import DetilPembayaran, PengajuanIzin
from django.shortcuts import get_object_or_404, render
import pdfkit, datetime, os
from django.template import RequestContext, loader
from django.http import HttpResponse
from izin.utils import terbilang, get_model_detil
from django.core.urlresolvers import reverse, resolve
from django.utils.safestring import mark_safe
from izin.models import KelompokJenisIzin, BankPembayaran

class DetilPembayaranAdmin(admin.ModelAdmin):
	list_display = ('kode', 'nomor_kwitansi', 'pengajuan_izin', 'peruntukan', 'jumlah_pembayaran', 'get_bank', 'terbayar',  'piutang', 'created_at')
	search_fields = ('nomor_kwitansi', 'kode', 'pengajuan_izin__pemohon__nama_lengkap', 'pengajuan_izin__no_pengajuan', 'nama_pemohon', 'nama_perusahaan')
	list_filter = ('terbayar', 'piutang', 'bank_pembayaran')
	ordering = ('-tanggal_dibuat',)

	def get_fieldsets(self, request, obj=None):
		fields = ('kode', 'nomor_kwitansi', 'jumlah_pembayaran', 'peruntukan', 'bank_pembayaran', 'nama_pemohon', 'nama_perusahaan', 'alamat_usaha' , 'tanggal_dibuat', 'piutang', 'terbayar')
		fields_admin = ('pengajuan_izin', 'status', 'created_by', 'verified_by', 'rejected_by')
		add_fieldsets = ()
		if request.user.is_superuser:
			add_fieldsets = (
				(None, {
					'classes': ('wide',),
					'fields': fields+fields_admin
					}),
			)
		elif request.user.groups.filter(name='Kasir'):
			add_fieldsets = (
				(None, {
					'classes': ('wide',),
					'fields': fields
					}),
			)
		return add_fieldsets

	def cetak_skrd(self, request, obj_id):
		detil_pembayaran_obj = get_object_or_404(DetilPembayaran, id=obj_id)
		terbilang_jumlah = ""
		detilpengajuan_obj = None
		if detil_pembayaran_obj.jumlah_pembayaran:
			terbilang_jumlah = terbilang(int(detil_pembayaran_obj.jumlah_pembayaran.split(",")[0].replace(".", "")))
		if detil_pembayaran_obj.pengajuan_izin:
			if detil_pembayaran_obj.pengajuan_izin.kelompok_jenis_izin:
				objects_ = get_model_detil(detil_pembayaran_obj.pengajuan_izin.kelompok_jenis_izin.kode)
				detilpengajuan_obj = objects_.objects.get(id=detil_pembayaran_obj.pengajuan_izin.id)
		extra_context={}
		extra_context.update({
			'detil':detil_pembayaran_obj,
			'detilpengajuan_obj': detilpengajuan_obj,
			'terbilang_jumlah': terbilang_jumlah
			})
		context_dict = "Cetak Kwitansi "
		options = {
				'page-width': '21.5cm',
				'page-height': '9cm',
				'margin-top': '0.3cm',
				'margin-bottom': '0cm',
				'margin-right': '0.5cm',
				'margin-left': '0.5cm',
				'encoding': "UTF-8",
				'custom-header' : [
					('Accept-Encoding', 'gzip')
				],
				'no-outline': None
			}
		template = loader.get_template("front-end/cetak/cetak_skrd.html")
		context = RequestContext(request, extra_context)
		html = template.render(context)
		date_time = datetime.datetime.now().strftime("%Y-%B-%d %H:%M:%S")
		attachment_file_name = context_dict+'['+str(date_time)+'].pdf'
		output_file_name = 'files/media/'+str(attachment_file_name)
		pdfkit.from_string(html, output_file_name, options=options)
		pdf = open(output_file_name)
		response = HttpResponse(pdf.read(), content_type='application/pdf')
		response['Content-Disposition'] = 'filename='+str(attachment_file_name)
		pdf.close()
		os.remove(output_file_name)  # remove the locally created pdf file.
		return response

	def cetak_pembayaran(self, request, nomor):
		try:
			detil_pembayaran_obj = get_object_or_404(DetilPembayaran, kode=nomor)
		except DetilPembayaran.MultipleObjectsReturned:
			detilpengajuan_obj = DetilPembayaran.objects.filter(kode=nomor).last()
		terbilang_jumlah = ""
		if detil_pembayaran_obj.jumlah_pembayaran:
			terbilang_jumlah = terbilang(int(detil_pembayaran_obj.jumlah_pembayaran.split(",")[0].replace(".", "")))
		extra_context={}
		extra_context.update({
			'detil':detil_pembayaran_obj,
			'terbilang_jumlah': terbilang_jumlah,
			'total_bayar': int(detil_pembayaran_obj.jumlah_pembayaran.split(",")[0].replace(".", ""))
			})
		context_dict = "Cetak Kwitansi "
		options = {
				'page-width': '21.5cm',
				'page-height': '9cm',
				'margin-top': '0.3cm',
				'margin-bottom': '0cm',
				'margin-right': '0.5cm',
				'margin-left': '0.5cm',
			}
		template = loader.get_template("front-end/cetak/cetak_pembayaran.html")
		context = RequestContext(request, extra_context)
		html = template.render(context)
		date_time = datetime.datetime.now().strftime("%Y-%B-%d %H:%M:%S")
		attachment_file_name = context_dict+'['+str(date_time)+'].pdf'
		output_file_name = 'files/media/'+str(attachment_file_name)
		pdfkit.from_string(html, output_file_name, options=options)
		pdf = open(output_file_name)
		response = HttpResponse(pdf.read(), content_type='application/pdf')
		response['Content-Disposition'] = 'filename='+str(attachment_file_name)
		pdf.close()
		os.remove(output_file_name)  # remove the locally created pdf file.
		return response

	def get_cetak(self, obj):
		link_cetak_skrd = "#"
		link_cetak_bukti = "#"
		if obj.id:
			link_cetak_skrd = reverse('admin:detil_pembayaran__cetak_skrd', kwargs={'obj_id': obj.id})
		if obj.kode:
			link_cetak_bukti = reverse('admin:detil_pembayaran__cetak_pembayaran', kwargs={'nomor': obj.kode})
		btn = mark_safe("""
			<a href="%s" target="_blank" class="btn btn-success btn-rounded btn-ef btn-ef-5 btn-ef-5a mb-10"><i class="fa fa-cog fa-spin"></i> <span>Cetak SKRD</span> </a>
			<a href="%s" target="_blank" class="btn btn-primary btn-rounded btn-ef btn-ef-5 btn-ef-5a mb-10"><i class="fa fa-cog fa-spin"></i> <span>Cetak Bukti</span> </a>
			""" % (link_cetak_skrd, link_cetak_bukti))
		return btn
	get_cetak.short_description = 'Aksi'

	def get_pemohon(self, obj):
		nama_pemohon = None
		if obj.pengajuan_izin:
			if obj.pengajuan_izin.pemohon:
				nama_pemohon = obj.pengajuan_izin.pemohon.nama_lengkap
		else:
			nama_pemohon = obj.nama_pemohon
		return nama_pemohon
	get_pemohon.short_description = 'Pemohon'

	def get_bank(self, obj):
		bank_ = "-"
		if obj.bank_pembayaran:
			bank_ = obj.bank_pembayaran.nama_bank
		return bank_
	get_bank.short_description = 'Bank'

	def get_tanggal_dibuat(self, obj):
		tanggal_dibuat = "-"
		if obj.tanggal_dibuat:
			tanggal_dibuat = obj.tanggal_dibuat.strftime("%d-%m-%Y")
		return tanggal_dibuat
	get_tanggal_dibuat.short_description = "Tanggal Dibuat"

	def get_tanggal_bayar(self, obj):
		tanggal_bayar = "-"
		if obj.tanggal_bayar:
			tanggal_bayar = obj.tanggal_bayar.strftime("%d-%m-%Y")
		return tanggal_bayar
	get_tanggal_bayar.short_description = "Tanggal Dibayar"

	def get_jumlah_pembayaran(self, obj):
		jumlah_pembayaran = "-"
		if obj.jumlah_pembayaran:
			jumlah_pembayaran = "Rp. "+obj.jumlah_pembayaran
		return jumlah_pembayaran
	get_jumlah_pembayaran.short_description = "Jumlah Pembayaran"

	def get_jenis_izin(self, obj):
		jenis_izin = "-"
		if obj.pengajuan_izin:
			if obj.pengajuan_izin.kelompok_jenis_izin:
				jenis_izin = obj.pengajuan_izin.kelompok_jenis_izin
		return jenis_izin
	get_jenis_izin.short_description = "Jenis Izin"

	def suit_cell_attributes(self, obj, column):
		class_attr = ''
		if column in ['terbayar', 'piutang']:
			class_attr += 'text-center'
		return {'class': class_attr }

	def changelist_view(self, request, extra_context={}):
		self.request = request
		extra_context = {
			'title': 'Pembayaran Retribusi' 
		}	
		return super(DetilPembayaranAdmin, self).changelist_view(request, extra_context=extra_context)

	def pembayaran_piutang(self, request, extra_context={}):
		self.request = request
		extra_context.update({
			'title': "Daftar Pembayaran Piutang",
			})
		return super(DetilPembayaranAdmin, self).changelist_view(request, extra_context=extra_context)

	def get_list_display(self, request):
		func_view, func_view_args, func_view_kwargs = resolve(request.path)
		if func_view.__name__ == 'pembayaran_piutang':
			return ('kode', 'nomor_kwitansi', 'nama_pemohon', 'nama_perusahaan', 'get_jumlah_pembayaran', 'terbayar')
		else:
			return ('kode', 'nomor_kwitansi', 'get_pemohon', 'get_jenis_izin', 'get_jumlah_pembayaran', 'get_tanggal_dibuat', 'get_tanggal_bayar', 'terbayar', 'piutang', 'get_cetak')

	def get_queryset(self, request):
		func_view, func_view_args, func_view_kwargs = resolve(request.path)
		qs = super(DetilPembayaranAdmin, self).get_queryset(request)
		if func_view.__name__ == 'pembayaran_piutang':
			qs = qs.filter(piutang=True)
		return qs

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilPembayaranAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^(?P<obj_id>[0-9]+)/cetak-skrd$', self.admin_site.admin_view(self.cetak_skrd), name='detil_pembayaran__cetak_skrd'),
			url(r'^(?P<nomor>[0-9]+)/cetak-pembayaran$', self.cetak_pembayaran, name='detil_pembayaran__cetak_pembayaran'),
			url(r'^piutang/$', self.admin_site.admin_view(self.pembayaran_piutang), name='detil_pembayaran__view_piutang'),
			)
		return my_urls + urls

	# def save_model(self, request, obj, form, change):
		# # clean the nomor_identitas
		# from utils import generate_kode_bank_jatim
		# # print request.POST.get("piutang")
		# # if request.POST.get("piutang") == "on":
		# tahun = datetime.date.today().strftime("%Y")
		# if not obj.id:
		# 	jumlah_data = int(DetilPembayaran.objects.filter(tanggal_dibuat__year=tahun).count())+1
		# 	obj.kode = generate_kode_bank_jatim(jumlah_data)
		# 	tanggal_dibuat = datetime.date.today()
		# obj.save()