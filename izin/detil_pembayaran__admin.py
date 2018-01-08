from django.contrib import admin
from models import DetilPembayaran, PengajuanIzin
from django.shortcuts import get_object_or_404, render
import pdfkit, datetime, os
from django.template import RequestContext, loader
from django.http import HttpResponse

class DetilPembayaranAdmin(admin.ModelAdmin):
	list_display = ('nomor_kwitansi', 'pengajuan_izin', 'peruntukan', 'jumlah_pembayaran', 'get_bank')

	def cetak_kwitansi(self, request, obj_id):
		detil_pembayaran_obj = get_object_or_404(DetilPembayaran, id=obj_id)
		extra_context={}
		extra_context.update({
			'detil':detil_pembayaran_obj
			})
		context_dict = "Cetak Kwitansi "
		options = {
				'page-width': '21.1cm',
				'page-height': '10cm',
				'margin-top': '1cm',
				'margin-bottom': '1cm',
				'margin-right': '1.5cm',
				'margin-left': '1.5cm',
			}
		template = loader.get_template("front-end/cetak_kwitansi.html")
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


	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilPembayaranAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^(?P<obj_id>[0-9]+)/cetak-bukti$', self.admin_site.admin_view(self.cetak_kwitansi), name='detil_pembayaran__cetak_kwitansi'),
			)
		return my_urls + urls

