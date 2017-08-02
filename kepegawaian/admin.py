from django.contrib import admin, messages
from mptt.admin import MPTTModelAdmin
from django.http import HttpResponse, Http404
from django.utils.safestring import mark_safe
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from datetime import datetime
from django.http import HttpResponseRedirect
from django.db.models import Q

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
	# list_filter = ('nama_unit_kerja',)
	search_fields = ('nama_unit_kerja', 'keterangan')

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
			list_display = ('pegawai', 'uuid','chat_id', 'status_verifikasi', 'status', 'verified_at', 'verified_by' )
		else:
			list_display = ('pegawai', 'status_verifikasi', 'verified_at', 'verifikasi_manual' )

		return list_display

	def verifikasi_manual(self, obj):
		str_aksi = '<a class="btn btn-xs btn-info" data-toggle="tooltip" data-container="body" data-original-title="Tes Kirim Pesan ke %s" href="%s"><i style="margin: 0px;" class="fa fa-location-arrow"></i></a>' % (obj.pegawai, reverse('admin:tes_telegram', kwargs={'chat_id': obj.chat_id }))
		if obj.status_verifikasi:
			return mark_safe(str_aksi)
		else:
			
			return mark_safe(str_aksi+'<a class="btn btn-xs btn-success" data-toggle="tooltip" data-container="body" data-original-title="Verifikasi %s" href="%s"><i style="margin: 0px;" class="icon-login"></i></a>' % (obj.pegawai, reverse('admin:verifikasi_telegram', kwargs={'uuid': obj.uuid })))
	verifikasi_manual.short_description = 'Aksi'

	def get_fieldsets(self, request, obj=None):
		field_user = ('keterangan', )
		field_admin = ('pegawai','chat_id', 'status_verifikasi', 'status', 'verified_by')

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
		if request.user.groups.filter(name="Admin SKPD"):
			qs = qs.filter(pegawai__unit_kerja=request.user.pegawai.unit_kerja)
		elif request.user.groups.filter(name="Tim Teknis"):
			qs = qs.filter(pegawai=request.user)
		elif request.user.is_superuser:
			qs = qs
		else:
			qs = qs.None()

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
					pesan = 'Halo, '+str(k.pegawai.get_full_name())+'.'
					kirim_notifikasi_telegram(chat_id, pesan, 'Melakukan tes koneksi melalui website, dilakukan oleh '+str(request.user)+'.', request.user)
					messages.info(request, "Tunggu beberapa saat kemudian silahkan cek Smartphone Anda")

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
		if column in ['status_verifikasi', 'kirim_notifikasi', 'verifikasi_manual']:
			return {'class': 'text-center'}
		else:
			return None


admin.site.register(NotifikasiTelegram, NotifikasiTelegramAdmin)


class LogTelegramAdmin(admin.ModelAdmin):

	list_display = ['kepada','proses', 'pesan', 'keterangan', 'created_at', 'get_aksi','created_by']


	def get_tgl(self, obj):
		return obj.created_at
	get_tgl.short_description = "Tanggal Dibuat"
	get_tgl.admin_order_field = "created_at"

	def get_aksi(self, obj):
		str_aksi = ""
		if not obj.status_terkirim and obj.kepada:
			str_aksi = '<a class="btn btn-xs btn-info" data-toggle="tooltip" data-container="body" data-original-title="Gagal, Klik untuk Kirim Ulang %s" href="%s"><i style="margin: 0px;" class="fa fa-location-arrow"></i></a>' % (obj.kepada, reverse('admin:kirimulangtelegram', kwargs={'kepada': obj.kepada.username }))
		elif not obj.status_terkirim:
			str_aksi = '<i class="fa fa-ban" data-toggle="tooltip" data-container="body" data-original-title="Gagal" style="color: #ff0000;"></i>'
		elif obj.status_terkirim:
			str_aksi = '<i class="fa fa-check-circle" data-toggle="tooltip" data-container="body" data-original-title="Terkirim" style="color: #44ad41;"></i>'


		return mark_safe(str_aksi)
	get_aksi.short_description = "Status"
	get_aksi.admin_order_field = "status_terkirim"


	def kirim_ulang(self, request, kepada):
		import telebot
		from django.conf import settings
		bot = telebot.TeleBot(settings.TELGRAM_API_TOKEN)
		if kepada:
			try:
				n = NotifikasiTelegram.objects.get(pegawai__username=kepada)
				log = LogTelegram.objects.get(kepada=n.pegawai, status_terkirim=False)
				try:
					bot.send_message(n.chat_id, log.pesan)
					messages_user = "Pengiriman ulang selesai"
				except Exception as e:
					messages_user = "Pengiriman gagal API "+str(e.result.reason)+" error kode : "+str(e.result.status_code)

				if log.keterangan != "":
					keterangan = str(log.keterangan)+", Melakukan pegiriman ulang"
				else:
					keterangan = "Melakukan pegiriman ulang"
				log.keterangan = keterangan
				log.status_terkirim = True
				log.save()
				
				messages.info(request, messages_user)
			except NotifikasiTelegram.DoesNotExist:
				pass
		return HttpResponseRedirect(reverse('admin:kepegawaian_logtelegram_changelist'))


	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		if request.user.is_superuser:
			return True
		return False

	def get_fieldsets(self, request, obj=None):
		field_user = ('')
		field_admin = ('kepada','proses', 'pesan', 'status_terkirim', 'keterangan', 'created_by')

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

		return add_fieldsets

	def get_list_display_links(self, request, list_display):
		if request.user.is_superuser:
			list_display_links = ('kepada', )
		else:
			list_display_links = (None)
		return list_display_links

	def suit_cell_attributes(self, obj, column):
		if column in ['status_terkirim', 'get_aksi']:
			return {'class': 'text-center'}
		else:
			return None

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(LogTelegramAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^kirimulang-telegram/(?P<kepada>\w+)$', self.admin_site.admin_view(self.kirim_ulang), name='kirimulangtelegram'),
			)
		return my_urls + urls

	def get_queryset(self, request):
		qs = super(LogTelegramAdmin, self).get_queryset(request)
		if request.user.groups.filter(Q(name="Admin SKPD") | Q(name="Tim Teknis")):
			qs = qs.filter(created_by=request.user)
		elif request.user.is_superuser:
			qs = qs
		else:
			qs = qs.None()

		return qs

admin.site.register(LogTelegram, LogTelegramAdmin)