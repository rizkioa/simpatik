from django.contrib import admin, messages
from mptt.admin import MPTTModelAdmin
from django.http import HttpResponse, Http404
from django.utils.safestring import mark_safe
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from datetime import datetime
from django.http import HttpResponseRedirect

from kepegawaian.pegawai_admin import PegawaiAdmin
from kepegawaian.forms import BidangStrukturalForm
from kepegawaian.models import *
from kepegawaian.views import kirim_notifikasi_telegram
# Register your models here.

class JenisUnitKerjaAdmin(MPTTModelAdmin):
	mptt_level_indent = 20
	list_display = ('jenis_unit_kerja', 'keterangan', 'jenis_unit_kerja_induk' )

class UnitKerjaAdmin(MPTTModelAdmin):
	mptt_level_indent = 20
	list_display = ('nama_unit_kerja', 'keterangan', 'jenis_unit_kerja', 'unit_kerja_induk' )

class BidangStrukturalAdmin(MPTTModelAdmin):
	mptt_level_indent = 20
	list_display = ('nama_bidang', 'keterangan', 'unit_kerja', 'bidang_induk' )
	list_filter = ('unit_kerja', )
	form = BidangStrukturalForm

	def get_form(self, request, obj=None, **kwargs):
		form = super(BidangStrukturalAdmin, self).get_form(request, obj, **kwargs)
		form.request = request
		return form
		
	def option_bidangstruktural(self, request):		
		bidangstruktural_list = BidangStruktural.objects.all()
		unit_kerja = request.POST.get('unit_kerja', None)
		if unit_kerja:
			bidangstruktural_list = bidangstruktural_list.filter(unit_kerja__id=unit_kerja)
		else:
			bidangstruktural_list = BidangStruktural.objects.none()
		pilihan = "<option></option>"
		return HttpResponse(mark_safe(pilihan+"".join(x.as_option(True) for x in bidangstruktural_list)));

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(BidangStrukturalAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^option/$', self.admin_site.admin_view(self.option_bidangstruktural), name='option_bidangstruktural'),
			)
		return my_urls + urls

admin.site.register(JenisUnitKerja, JenisUnitKerjaAdmin)
admin.site.register(UnitKerja, UnitKerjaAdmin)
admin.site.register(BidangStruktural, BidangStrukturalAdmin)
admin.site.register(Pegawai, PegawaiAdmin)
admin.site.register(Jabatan)



class NotifikasiTelegramAdmin(admin.ModelAdmin):

	def get_list_display(self, request):
		if request.user.is_superuser:
			list_display = ('pegawai', 'uuid','chat_id', 'status_verifikasi', 'kirim_notifikasi', 'status', 'verified_at', 'verified_by' )
		else:
			list_display = ('pegawai', 'status_verifikasi', 'kirim_notifikasi', 'verified_at', 'verifikasi_manual' )

		return list_display

	def verifikasi_manual(self, obj):
		str_aksi = '<a class="btn btn-xs btn-success" title="Verifikasi %s" href="%s"><i style="margin: 0px;" class="icon-login"></i></a>' % (obj.pegawai, reverse('admin:tes_telegram', kwargs={'chat_id': obj.chat_id }))
		if obj.status_verifikasi:
			return mark_safe(str_aksi)
		else:
			
			return mark_safe(str_aksi+'<a class="btn btn-xs btn-success" title="Verifikasi %s" href="%s"><i style="margin: 0px;" class="icon-login"></i></a>' % (obj.pegawai, reverse('admin:verifikasi_telegram', kwargs={'uuid': obj.uuid })))
	verifikasi_manual.short_description = 'Aksi'

	def get_fieldsets(self, request, obj=None):
		field_user = ('kirim_notifikasi', 'keterangan')
		field_admin = ('pegawai', 'uuid','chat_id', 'status_verifikasi', 'status' )

		if obj:
			if request.user.is_superuser:
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': field_admin
						}),
				)
			else:
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': field_user
						}),
				)
		else:
			pass

		return add_fieldsets

	def get_queryset(self, request):
		qs = super(NotifikasiTelegramAdmin, self).get_queryset(request)

		if not request.user.is_superuser:
			qs = qs.filter(pegawai=request.user)

		return qs

	def verifikasi_telegram(self, request, uuid=None):
		extra_context = {}
		try:
			p = NotifikasiTelegram.objects.get(uuid=uuid, pegawai=request.user)
			extra_context.update({ 'pegawai': p.pegawai.get_full_name })
			if p.status_verifikasi == False:
				p.status = 1
				p.status_verifikasi = True
				p.verified_by = request.user
				p.verified_at = datetime.now()
				p.save()
				extra_context.update({ 'pesan': "Verifikasi Notifikasi Telgram berhasil" })
			else:
				extra_context.update({ 'pesan': "Notifikasi Telegram sudah aktif" })
			
		except NotifikasiTelegram.DoesNotExist:
			raise Http404

		template = loader.get_template("admin/kepegawaian/notifikasitelegram/verifikasi_telegram.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def tes_telegram(self, request, chat_id=None):
		if chat_id:
			p = self.get_queryset(request)
			p = p.filter(chat_id=chat_id)
			if p.exists():
				for k in p:
					pesan = 'Halo... '+str(k.pegawai.get_full_name)
					kirim_notifikasi_telegram(chat_id, pesan)
					messages.success(request, "Tunggu beberapa saat kemudian silahkan cek Smartphone Anda")

		return HttpResponseRedirect(reverse('admin:kepegawaian_notifikasitelegram_changelist'))


	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(NotifikasiTelegramAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^(?P<uuid>[0-9a-z-]+)/verifikasi/$', self.admin_site.admin_view(self.verifikasi_telegram), name='verifikasi_telegram'),
			url(r'^tes-telegram/(?P<chat_id>[0-9]+)$', self.admin_site.admin_view(self.tes_telegram), name='tes_telegram'),
			)
		return my_urls + urls

	def suit_cell_attributes(self, obj, column):
		if column in ['status_verifikasi', 'kirim_notifikasi']:
			return {'class': 'text-center'}
		else:
			return None


admin.site.register(NotifikasiTelegram, NotifikasiTelegramAdmin)