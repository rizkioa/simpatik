from django.contrib import admin
from models import DetilPembayaran, PengajuanIzin
from django.shortcuts import get_object_or_404, render
import pdfkit, datetime, os
from django.template import RequestContext, loader
from django.http import HttpResponse
from izin.utils import terbilang, get_model_detil

class DetilPembayaranAdmin(admin.ModelAdmin):
	list_display = ('kode', 'nomor_kwitansi', 'pengajuan_izin', 'peruntukan', 'jumlah_pembayaran', 'get_bank', 'terbayar', 'created_at')

	def cetak_skrd(self, request, obj_id):
		detil_pembayaran_obj = get_object_or_404(DetilPembayaran, id=obj_id)
		terbilang_jumlah = ""
		if detil_pembayaran_obj.jumlah_pembayaran:
			terbilang_jumlah = terbilang(int(detil_pembayaran_obj.jumlah_pembayaran.replace(".", "")))
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
		detil_pembayaran_obj = get_object_or_404(DetilPembayaran, kode=nomor)
		terbilang_jumlah = ""
		if detil_pembayaran_obj.jumlah_pembayaran:
			terbilang_jumlah = terbilang(int(detil_pembayaran_obj.jumlah_pembayaran.replace(".", "")))
		extra_context={}
		extra_context.update({
			'detil':detil_pembayaran_obj,
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

	def get_bank(self, obj):
		bank_ = "-"
		if obj.bank_pembayaran:
			bank_ = obj.bank_pembayaran.nama_bank
		return bank_
	get_bank.short_description = 'Bank'

	def suit_cell_attributes(self, obj, column):
		class_attr = ''
		if column in ['terbayar',]:
			class_attr += 'text-center'
		return {'class': class_attr }

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilPembayaranAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^(?P<obj_id>[0-9]+)/cetak-skrd$', self.admin_site.admin_view(self.cetak_skrd), name='detil_pembayaran__cetak_skrd'),
			url(r'^(?P<nomor>[0-9]+)/cetak-pembayaran$', self.cetak_pembayaran, name='detil_pembayaran__cetak_pembayaran'),
			)
		return my_urls + urls

