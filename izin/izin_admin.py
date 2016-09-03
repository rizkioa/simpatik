from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils.safestring import mark_safe

from izin.models import PengajuanIzin, JenisIzin, KelompokJenisIzin, Syarat
from izin.controllers.siup import add_wizard_siup, formulir_siup

import json

class IzinAdmin(admin.ModelAdmin):
	list_display = ('pemohon','kelompok_jenis_izin','jenis_permohonan','status', 'button_cetak_pendaftaran')

	def button_cetak_pendaftaran(self, obj):
		btn = mark_safe("""
			<a href="%s" target="_blank"><i class="fa fa-file-pdf-o"></i></a>
			""" % reverse('admin:print_out_pendaftaran', kwargs={'id_pengajuan_izin_': obj.id}))
		return btn
	button_cetak_pendaftaran.short_description = "Cetak Pendafaran"

	def pendaftaran_selesai(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Pengajuan Selesai'})
			pengajuan_ = PengajuanIzin.objects.get(id=id_pengajuan_izin_)
			extra_context.update({'pemohon': pengajuan_.pemohon})
			extra_context.update({'id_pengajuan': pengajuan_.id})
			extra_context.update({'jenis_pemohon': pengajuan_.pemohon.jenis_pemohon})
			extra_context.update({'alamat_pemohon': str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)})
			extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})


		# template = loader.get_template("admin/izin/izin/add_wizard.html")
		template = loader.get_template("admin/izin/izin/pengajuan_baru_selesai.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def print_out_pendaftaran(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Pengajuan Selesai'})
			pengajuan_ = PengajuanIzin.objects.get(id=id_pengajuan_izin_)
			extra_context.update({'pemohon': pengajuan_.pemohon})
			nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
			extra_context.update({'nomor_identitas': nomor_identitas_ })
			extra_context.update({'jenis_pemohon': pengajuan_.pemohon.jenis_pemohon})
			extra_context.update({'alamat_pemohon': str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)})
			extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})

			syarat_ = Syarat.objects.filter(jenis_izin__id=pengajuan_.id)
			extra_context.update({'syarat': syarat_})

		# template = loader.get_template("admin/izin/izin/add_wizard.html")
		template = loader.get_template("admin/izin/izin/cetak_bukti_pendaftaran.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def option_namaizin(self, request):	
		jenis_izin = request.POST.get('param', None)
		if jenis_izin:
			jenisizin_list = JenisIzin.objects.filter(jenis_izin=jenis_izin)
		else:
			jenisizin_list = JenisIzin.objects.none()
		pilihan = "<option></option>"
		response = {
			"count": 0,
			"data": pilihan+"".join(x.as_option() for x in jenisizin_list)
		}

		return HttpResponse(json.dumps(response))
		# return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in jenisizin_list)));

		# pilihan = """
		# <option value=1>SIUP</option>
		# <option>HO</option>
		# <option>SIPA</option>
		# <option>Izin Pertambangan</option>
		# <option>TDP</option>
		# """
		# return HttpResponse(mark_safe(pilihan));

	def option_kelompokjenisizin(self, request):
		kode_jenis_izin = request.POST.get('param', None)
		if kode_jenis_izin:
			kelompokjenisizin_list = KelompokJenisIzin.objects.filter(jenis_izin__kode=kode_jenis_izin)
		else:
			kelompokjenisizin_list = KelompokJenisIzin.objects.none()
		pilihan = "<option></option>"
		response = {
			"count": len(kelompokjenisizin_list),
			"data": pilihan+"".join(x.as_option() for x in kelompokjenisizin_list)
		}

		return HttpResponse(json.dumps(response))
		# return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in kelompokjenisizin_list)));

		# pilihan = """
		# <option value=1>SIUP</option>
		# <option>HO</option>
		# <option>SIPA</option>
		# <option>Izin Pertambangan</option>
		# <option>TDP</option>
		# """
		# return HttpResponse(mark_safe(pilihan));

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(IzinAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^wizard/add/$', self.admin_site.admin_view(add_wizard_siup), name='add_wizard_izin'),
			url(r'^option/izin/$', self.admin_site.admin_view(self.option_namaizin), name='option_namaizin'),
			url(r'^option/kelompokizin/$', self.admin_site.admin_view(self.option_kelompokjenisizin), name='option_kelompokjenisizin'),
			url(r'^wizard/add/proses/siup/$', self.admin_site.admin_view(formulir_siup), name='izin_proses_siup'),
			url(r'^pendaftaran/(?P<id_pengajuan_izin_>[0-9]+)/$', self.admin_site.admin_view(self.pendaftaran_selesai), name='pendaftaran_selesai'),
			url(r'^pendaftaran/(?P<id_pengajuan_izin_>[0-9]+)/cetak$', self.admin_site.admin_view(self.print_out_pendaftaran), name='print_out_pendaftaran'),
			)
		return my_urls + urls

	def save_model(self, request, obj, form, change):
		# clean the nomor_identitas
		obj.create_by = request.user
		obj.save()

admin.site.register(PengajuanIzin, IzinAdmin)
