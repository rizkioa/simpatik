from django.contrib import admin
from perusahaan.models import JenisPerusahaan, KBLI, JenisPenanamanModal, StatusPerusahaan, JenisKerjasama, JenisBadanUsaha, Perusahaan, JenisKedudukan, DataPimpinan, JenisKegiatanUsaha, JenisPengecer, KegiatanUsaha, DataRincianPerusahaan, PemegangSahamLain, Kelembagaan, ProdukUtama, JenisMesin, MesinHuller, MesinPerusahaan, AktaNotaris, JenisModalKoprasi, ModalKoprasi, NilaiModal, LokasiUnitProduksi
from perusahaan.perusahaan_admin import PerusahaanAdmin
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.utils.decorators import method_decorator
from django.template import RequestContext, loader
from django.contrib.auth.decorators import user_passes_test
from perusahaan.forms import AktaNotarisForm,PerusahaanForm
from django.forms.formsets import formset_factory, BaseFormSet


# Register your models here.

admin.site.register(JenisPenanamanModal)

class JenisPerusahaanAdmin(admin.ModelAdmin):
	list_display = ('jenis_perusahaan',)
	search_fields = ('jenis_perusahaan',)

admin.site.register(JenisPerusahaan, JenisPerusahaanAdmin)

class KBLIAdmin(admin.ModelAdmin):
	list_display = ('kode_kbli','nama_kbli')
	search_fields = ('nama_kbli',)

admin.site.register(KBLI, KBLIAdmin)

admin.site.register(Perusahaan, PerusahaanAdmin)

admin.site.register(JenisKedudukan)

class DataPimpinanAdmin(admin.ModelAdmin):
	list_display = ('nama_lengkap','perusahaan','kedudukan','tanggal_menduduki_jabatan','kedudukan_diperusahaan_lain','nama_perusahaan_lain')
	list_filter = ('kedudukan','nama_lengkap')
	search_fields = ('nama_lengkap','kedudukan')

admin.site.register(DataPimpinan, DataPimpinanAdmin)

class JenisKegiatanUsahaAdmin(admin.ModelAdmin):
	list_display = ('jenis_kegiatan_usaha',)
	list_filter = ('jenis_kegiatan_usaha',)

admin.site.register(JenisKegiatanUsaha, JenisKegiatanUsahaAdmin)

class DataRincianPerusahaanAdmin(admin.ModelAdmin):
	list_display = ('perusahaan', 'omset_per_tahun', 'total_aset', 'kapasitas_mesin_terpasang','jenis_kegiatan',)
	search_fields = ('perusahaan', 'jenis_kegiatan', 'omset_per_tahun','total_aset', 'kapasitas_mesin_terpasang')
	list_filter = ('perusahaan','jenis_kegiatan','omset_per_tahun')
	ordering = ('id',)

admin.site.register(DataRincianPerusahaan, DataRincianPerusahaanAdmin)

class KelembagaanAdmin(admin.ModelAdmin):
	list_display = ('nama_kelembagaan',)
	search_fields = ('nama_kelembagaan',)

admin.site.register(Kelembagaan, KelembagaanAdmin)

class PemegangSahamaLainAdmin(admin.ModelAdmin):
	list_display = ('perusahaan','npwp','jumlah_saham_dimiliki','jumlah_modal_disetor')
	list_filter = ('perusahaan','jumlah_saham_dimiliki')
	search_fields = ('npwp','perusahaan')

admin.site.register(PemegangSahamLain, PemegangSahamaLainAdmin)

class MesinPerusahaanAdmin(admin.ModelAdmin):
	list_display = ('mesin','tipe','PK','merk')
	list_filter = ('tipe','merk')
	search_fields = ('mesin','tipe', 'PK', 'merk')

admin.site.register(MesinPerusahaan, MesinPerusahaanAdmin)

class AktaNotarisAdmin(admin.ModelAdmin):
	list_display = ('perusahaan','no_akta','tanggal_akta','jenis_akta')
	list_filter = ('perusahaan','no_akta','tanggal_akta')
	search_fields = ('perusahaan','no_akta','tanggal_akta','jenis_akta')

	@method_decorator(user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Front Desk').exists()))
	def add_form_legaliatas(self, request):
		# pemohon_list = Pemohon.objects.filter(status=1)
	    class RequiredFormSet(BaseFormSet):
	        def __init__(self, *args, **kwargs):
	            super(RequiredFormSet, self).__init__(*args, **kwargs)
	            for form in self.forms:
	                form.empty_permitted = False
	    AktaNotarisFormSet = formset_factory(AktaNotarisForm, max_num=10, formset=RequiredFormSet)
	    if request.method == 'POST': # If the form has been submitted...
	        perusahaan_form = PerusahaanForm(request.POST) # A form bound to the POST data
	        # Create a formset from the submitted data
	        akta_notaris_formset = AktaNotarisFormSet(request.POST, request.FILES)

	        if perusahaan_form.is_valid() and akta_notaris_formset.is_valid():
	            perusahaan_list = perusahaan_form.save()
	            for form in akta_notaris_formset.forms:
	                akta_notaris_item = form.save(commit=False)
	                akta_notaris_item.list = perusahaan_list
	                akta_notaris_item.save()
	            return HttpResponseRedirect('thanks') # Redirect to a 'success' page
	    else:
	        perusahaan_form = PerusahaanForm()
	        akta_notaris_formset = AktaNotarisFormSet()

		extra_context = {'title' : 'Legalitas'}
		# form_legalitas_perusahaan = AktaNotarisForm()
		extra_context.update({'perusahaan_form': perusahaan_form,
		         'akta_notaris_formset': akta_notaris_formset,})
		template = loader.get_template("admin/perusahaan/aktanotaris/form_legalitas.html")
		ec = RequestContext(request, extra_context)

		return HttpResponse(template.render(ec))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(AktaNotarisAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^legalitas/add/$', self.admin_site.admin_view(self.add_form_legaliatas), name='add_form_legaliatas'),
			)
		return my_urls + urls

	def add_view(self, request, form_url='', extra_context={}):
		# if request.user.groups.filter(name='Front Desk').exists():
		# self.change_form_template = 'admin/change_form.html'

		return super(AktaNotarisAdmin, self).add_view(request,form_url, extra_context=extra_context)

	# def get_urls(self):
	# 	from django.conf.urls import patterns, url
	# 	urls = super(AktaNotarisAdmin, self).get_urls()
	# 	my_urls = patterns('',
	# 		url(r'^ajax/legalitas/(?P<aktanotaris_id>\w+)/$', self.admin_site.admin_view(self.ajax_legalitas_perusahaan), name='ajax_legalitas_perusahaan'),
	# 		)
	# 	return my_urls + urls

admin.site.register(AktaNotaris, AktaNotarisAdmin)

class ProdukUtamaAdmin(admin.ModelAdmin):
	list_display = ('perusahaan','kelembagaan','barang_jasa_utama')
	list_filter = ('barang_jasa_utama',)

admin.site.register(ProdukUtama, ProdukUtamaAdmin)

class MesinHullerAdmin(admin.ModelAdmin):
	list_display = ('jenis','mesin_huller')

admin.site.register(MesinHuller, MesinHullerAdmin)

class ModalKoprasiAdmin(admin.ModelAdmin):
	list_display = ('jenis_modal','modal_koprasi')

admin.site.register(ModalKoprasi, ModalKoprasiAdmin)

class NilaiModalAdmin(admin.ModelAdmin):
	list_display = ('perusahaan','modal', 'nilai')

admin.site.register(NilaiModal, NilaiModalAdmin)

class NilaiModalAdmin(admin.ModelAdmin):
	list_display = ('perusahaan','desa', 'alamat')

admin.site.register(LokasiUnitProduksi)

admin.site.register(JenisPengecer)
admin.site.register(KegiatanUsaha)
admin.site.register(StatusPerusahaan)
admin.site.register(JenisKerjasama)
admin.site.register(JenisBadanUsaha)
admin.site.register(JenisMesin)
admin.site.register(JenisModalKoprasi)
