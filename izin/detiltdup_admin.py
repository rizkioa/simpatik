from django.contrib import admin
from izin.models import DetilTDUP, SubJenisBidangUsaha
import json
from django.http import HttpResponse
from django.utils.safestring import mark_safe

class DetilTDUPAdmin(admin.ModelAdmin):

	def option_sub_jenis_bidang_usaha(self, request):
		select = request.POST.get('select')
		select = eval(select)
		# bidang_usaha = []
		# if request.POST.get('bidang_usaha'):
		bidang_usaha = request.POST.getlist('bidang_usaha[]')
		print bidang_usaha
		# print request.POST.getlist('value[]')
		subjenis_list = SubJenisBidangUsaha.objects.filter(bidang_usaha_pariwisata_id__in=bidang_usaha)
		# print subjenis_list
		if len(select) > 0:
			subjenis_list = subjenis_list.exclude(id__in=select)
		print subjenis_list
		pilihan = '<option></option>'
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in subjenis_list)));


	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilTDUPAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^option-sub-jenis-bidang-usaha$', self.option_sub_jenis_bidang_usaha, name='option_sub_jenis_bidang_usaha'),

			)
		return my_urls + urls

admin.site.register(DetilTDUP, DetilTDUPAdmin)