from django.contrib import admin
from perusahaan.models import JenisPerusahaan, KBLI, JenisPenanamanModal, JenisBadanUsaha, Perusahaan, BentukKegiatanUsaha, Kelembagaan, Legalitas, JenisLegalitas, BentukKerjasama, StatusPerusahaan, KedudukanKegiatanUsaha, JenisPengecer, JenisKedudukan
from perusahaan.perusahaan_admin import PerusahaanAdmin
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.utils.decorators import method_decorator
from django.template import RequestContext, loader
from django.contrib.auth.decorators import user_passes_test
# from perusahaan.forms import AktaNotarisForm,PerusahaanForm
from django.forms.formsets import formset_factory, BaseFormSet


# Register your models here.

class JenisLegalitasAdmin(admin.ModelAdmin):
	list_display = ('jenis_legalitas','keterangan')

class LegalitasAdmin(admin.ModelAdmin):
	list_display = ('perusahaan','jenis_legalitas')
	# search_fields = ('jenis_perusahaan',)

class JenisPerusahaanAdmin(admin.ModelAdmin):
	list_display = ('jenis_perusahaan',)
	search_fields = ('jenis_perusahaan',)

class KBLIAdmin(admin.ModelAdmin):
	list_display = ('kode_kbli','nama_kbli', 'versi')
	search_fields = ('nama_kbli',)
	actions = ('get_export_csv',)

	def get_export_csv(modeladmin, request, queryset):
		import csv
		from django.utils.encoding import smart_str
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=kbli.csv'
		writer = csv.writer(response, csv.excel)
		response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
		writer.writerow([
			smart_str(u"ID"),
			smart_str(u"Kode KBLI"),
			smart_str(u"Nama KBLI"),
			smart_str(u"Versi"),
		])
		for obj in queryset:
			writer.writerow([
				smart_str(obj.pk),
				smart_str(obj.kode_kbli),
				smart_str(obj.nama_kbli),
				smart_str(obj.versi),
			])
		return response
	get_export_csv.short_description = u"Export CSV"

class KelembagaanAdmin(admin.ModelAdmin):
	list_display = ('kelembagaan','keterangan')
	search_fields = ('kelembagaan',)

admin.site.register(BentukKegiatanUsaha)
admin.site.register(JenisBadanUsaha)
admin.site.register(BentukKerjasama)
admin.site.register(StatusPerusahaan)
admin.site.register(KedudukanKegiatanUsaha)
admin.site.register(JenisPengecer)
admin.site.register(JenisKedudukan)
admin.site.register(JenisPenanamanModal)
admin.site.register(JenisLegalitas, JenisLegalitasAdmin)
admin.site.register(Legalitas, LegalitasAdmin)
admin.site.register(JenisPerusahaan, JenisPerusahaanAdmin)
admin.site.register(KBLI, KBLIAdmin)
admin.site.register(Perusahaan, PerusahaanAdmin)
admin.site.register(Kelembagaan, KelembagaanAdmin)

# class DataPimpinanAdmin(admin.ModelAdmin):
# 	list_display = ('nama_lengkap','perusahaan','kedudukan','tanggal_menduduki_jabatan','kedudukan_diperusahaan_lain','nama_perusahaan_lain')
# 	list_filter = ('kedudukan','nama_lengkap')
# 	search_fields = ('nama_lengkap','kedudukan')

# admin.site.register(DataPimpinan, DataPimpinanAdmin)

# class JenisKegiatanUsahaAdmin(admin.ModelAdmin):
# 	list_display = ('jenis_kegiatan_usaha',)
# 	list_filter = ('jenis_kegiatan_usaha',)

# admin.site.register(JenisKegiatanUsaha, JenisKegiatanUsahaAdmin)

# class DataRincianPerusahaanAdmin(admin.ModelAdmin):
# 	list_display = ('perusahaan', 'omset_per_tahun', 'total_aset', 'kapasitas_mesin_terpasang','jenis_kegiatan',)
# 	search_fields = ('perusahaan', 'jenis_kegiatan', 'omset_per_tahun','total_aset', 'kapasitas_mesin_terpasang')
# 	list_filter = ('perusahaan','jenis_kegiatan','omset_per_tahun')
# 	ordering = ('id',)

# admin.site.register(DataRincianPerusahaan, DataRincianPerusahaanAdmin)

# class PemegangSahamaLainAdmin(admin.ModelAdmin):
# 	list_display = ('perusahaan','npwp','jumlah_saham_dimiliki','jumlah_modal_disetor')
# 	list_filter = ('perusahaan','jumlah_saham_dimiliki')
# 	search_fields = ('npwp','perusahaan')

# admin.site.register(PemegangSahamLain, PemegangSahamaLainAdmin)

# class MesinPerusahaanAdmin(admin.ModelAdmin):
# 	list_display = ('mesin','tipe','PK','merk')
# 	list_filter = ('tipe','merk')
# 	search_fields = ('mesin','tipe', 'PK', 'merk')

# admin.site.register(MesinPerusahaan, MesinPerusahaanAdmin)

# class AktaNotarisAdmin(admin.ModelAdmin):
# 	list_display = ('perusahaan','no_akta','tanggal_akta','jenis_akta')
# 	list_filter = ('perusahaan','no_akta','tanggal_akta')
# 	search_fields = ('perusahaan','no_akta','tanggal_akta','jenis_akta')

# 	@method_decorator(user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Front Desk').exists()))
# 	def add_form_legaliatas(self, request):
# 		# pemohon_list = Pemohon.objects.filter(status=1)
# 	    class RequiredFormSet(BaseFormSet):
# 	        def __init__(self, *args, **kwargs):
# 	            super(RequiredFormSet, self).__init__(*args, **kwargs)
# 	            for form in self.forms:
# 	                form.empty_permitted = False
# 	    AktaNotarisFormSet = formset_factory(AktaNotarisForm, max_num=10, formset=RequiredFormSet)
# 	    if request.method == 'POST': # If the form has been submitted...
# 	        perusahaan_form = PerusahaanForm(request.POST) # A form bound to the POST data
# 	        # Create a formset from the submitted data
# 	        akta_notaris_formset = AktaNotarisFormSet(request.POST, request.FILES)

# 	        if perusahaan_form.is_valid() and akta_notaris_formset.is_valid():
# 	            perusahaan_list = perusahaan_form.save()
# 	            for form in akta_notaris_formset.forms:
# 	                akta_notaris_item = form.save(commit=False)
# 	                akta_notaris_item.list = perusahaan_list
# 	                akta_notaris_item.save()
# 	            return HttpResponseRedirect('thanks') # Redirect to a 'success' page
# 	    else:
# 	        perusahaan_form = PerusahaanForm()
# 	        akta_notaris_formset = AktaNotarisFormSet()

# 		extra_context = {'title' : 'Legalitas'}
# 		# form_legalitas_perusahaan = AktaNotarisForm()
# 		extra_context.update({'perusahaan_form': perusahaan_form,
# 		         'akta_notaris_formset': akta_notaris_formset,})
# 		template = loader.get_template("admin/perusahaan/aktanotaris/form_legalitas.html")
# 		ec = RequestContext(request, extra_context)

# 		return HttpResponse(template.render(ec))

# 	def get_urls(self):
# 		from django.conf.urls import patterns, url
# 		urls = super(AktaNotarisAdmin, self).get_urls()
# 		my_urls = patterns('',
# 			url(r'^legalitas/add/$', self.admin_site.admin_view(self.add_form_legaliatas), name='add_form_legaliatas'),
# 			)
# 		return my_urls + urls

# 	def add_view(self, request, form_url='', extra_context={}):
# 		# if request.user.groups.filter(name='Front Desk').exists():
# 		# self.change_form_template = 'admin/change_form.html'

# 		return super(AktaNotarisAdmin, self).add_view(request,form_url, extra_context=extra_context)

	# def get_urls(self):
	# 	from django.conf.urls import patterns, url
	# 	urls = super(AktaNotarisAdmin, self).get_urls()
	# 	my_urls = patterns('',
	# 		url(r'^ajax/legalitas/(?P<aktanotaris_id>\w+)/$', self.admin_site.admin_view(self.ajax_legalitas_perusahaan), name='ajax_legalitas_perusahaan'),
	# 		)
	# 	return my_urls + urls

# admin.site.register(AktaNotaris, AktaNotarisAdmin)

# class ProdukUtamaAdmin(admin.ModelAdmin):
# 	list_display = ('barang_jasa_utama', 'keterangan')
# 	list_filter = ('barang_jasa_utama',)

# admin.site.register(ProdukUtama, ProdukUtamaAdmin)

# class MesinHullerAdmin(admin.ModelAdmin):
# 	list_display = ('jenis','mesin_huller')

# admin.site.register(MesinHuller, MesinHullerAdmin)

# class ModalKoprasiAdmin(admin.ModelAdmin):
# 	list_display = ('jenis_modal','modal_koprasi')

# admin.site.register(ModalKoprasi, ModalKoprasiAdmin)

# class NilaiModalAdmin(admin.ModelAdmin):
# 	list_display = ('perusahaan','modal', 'nilai')

# admin.site.register(NilaiModal, NilaiModalAdmin)