from django.contrib import admin

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from izin.siup_forms import IzinPemohonForm
from izin.models import Pemohon,Izin
from perusahaan.models import Perusahaan

from django.template import RequestContext, loader
from django.http import HttpResponse
import datetime

class IzinAdmin(admin.ModelAdmin):
	list_display = ('pendaftaran','pembaharuan','perusahaan','pemohon','status')
	list_filter = ('pendaftaran','pembaharuan','created_at')
	filter_horizontal = ('jenis_gangguan', 'jenis_kegiatan_pembangunan','parameter_bgunan',)
	# change_form_template = 'admin/change_form.html'

	@method_decorator(user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Front Desk').exists()))
	def add_form_siup(self, request):
		
		# pemohon_list = Pemohon.objects.filter(status=1)
		# created_by = request.user
		# if request.method == 'POST': # If the form has been submitted...
  # #        # Redirect to a 'success' page
		form_izin_pemohon = IzinPemohonForm(False)
			
		if request.method == 'POST':
			form_izin_pemohon = IzinPemohonForm(False, request.POST)
			
			if form_izin_pemohon.is_valid():
				# pemohon = form_izin_pemohon.cleaned_data['pemohon']
				# perusahaan = form_izin_perusahaan.cleaned_data['perusahaan']
				p = Pemohon.objects.get(pk=request.POST['pemohon'])
				q = Perusahaan.objects.get(pk=request.POST['perusahaan'])
				# print p
				# print q
				# request.POST['perusahaan']
				# untuk menyimpan ke DB
				izin_pemohon = form_izin_pemohon.save(commit=False)
				izin_perusahaan = form_izin_pemohon.save(commit=False)
				# no_pendaftaran = form_izin_pemohon.save(commit=False)


				# a = datetime.date.today()
				# b = a.strftime("%m%d%y")
				# print b
				# c = '00'
				max_id = Izin.objects.latest('pendaftaran').pendaftaran
				d = max_id + 1
				# print max_id
				# e = d.pendaftaran
				# f = b + c 
				# a = 0
				# for x in range (1,999):
					# f = int(f) + 1
					# print (f)
					
					
				pendaftaran = d
				print pendafataran

				# print pendaftaran
				# print perusahaan

				izin_pemohon.pemohon = p
				izin_perusahaan.perusahaan = q
				izin_perusahaan.pendaftaran = pendaftaran 
				# print izin_perusahaan.pendaftaran
				# print izin_pemohon.pemohon
				# print izin_perusahaan.perusahaan
				# print izin_perusahaan.perusahaan
				# izin_perusahaan.save()
				# izin_pemohon.save()
				# print izin_pemohon
				# print izin_perusahaan
				# form_izin_pemohon = IzinPemohonForm(False)
				# form_izin_perusahaan = IzinPerusahaanForm(False)

		extra_context = {'title' : 'FORMULIR SIUP'}
		extra_context.update({'form_izin_pemohon' : form_izin_pemohon })

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

	def save_model(self, request, obj, form, change):
		# clean the nomor_identitas
		print request.user
		obj.create_by = request.user
		# try:
		# max_id = Izin.objects.latest('pendaftaran').pendaftaran
		# except pendaftaran.DoesNoExist:
		# 	max_id = 9

		# obj.pendaftaran = max_id + 1
			# datetime = datetime.datetime.now()
		obj.save()