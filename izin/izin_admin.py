from django.contrib import admin

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from izin.siup_forms import IzinPemohonForm, IzinPerusahaanForm
from izin.models import Pemohon
from perusahaan.models import Perusahaan

from django.template import RequestContext, loader
from django.http import HttpResponse

class IzinAdmin(admin.ModelAdmin):
	list_display = ('pendaftaran','pembaharuan','status')
	list_filter = ('pendaftaran','pembaharuan','created_at')
	filter_horizontal = ('jenis_gangguan', 'jenis_kegiatan_pembangunan','parameter_bgunan',)
	# change_form_template = 'admin/change_form.html'

	@method_decorator(user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Front Desk').exists()))
	def add_form_siup(self, request):
		
		# pemohon_list = Pemohon.objects.filter(status=1)

		extra_context = {'title' : 'FORMULIR SIUP'}
		form_izin_pemohon = IzinPemohonForm()
		form_izin_perusahaan = IzinPerusahaanForm()
		extra_context.update({'form_izin_pemohon' : form_izin_pemohon})
		template = loader.get_template("admin/izin/izin/form_wizard.html")
		ec = RequestContext(request, extra_context)

		return HttpResponse(template.render(ec))
		# return super(IzinAdmin, self).add_view(request,'', extra_context=extra_context)
		
	@method_decorator(user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Front Desk').exists()))
	def change_form_izin(self, request, id_izin):
		extra_context = {}
		pass

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(IzinAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^wizard/add/$', self.admin_site.admin_view(self.add_form_siup), name='add_form_siup'),
			url(r'^wizard/(?P<id_izin>\w+)/$', self.admin_site.admin_view(self.change_form_izin), name='change_form_izin'),
			)
		return my_urls + urls

	def add_view(self, request, form_url='', extra_context={}):
		# if request.user.groups.filter(name='Front Desk').exists():
		# self.change_form_template = 'admin/change_form.html'

		return super(IzinAdmin, self).add_view(request,form_url, extra_context=extra_context)