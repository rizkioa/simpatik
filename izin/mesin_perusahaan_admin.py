from django.contrib import admin
from izin.models import MesinPerusahaan, Syarat, SKIzin, Riwayat
from kepegawaian.models import Pegawai
from accounts.models import NomorIdentitasPengguna
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
from django.http import HttpResponse
import base64
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, resolve
import datetime

class MesinPerusahaanAdmin(admin.ModelAdmin):
	list_display = ('detil_huller','mesin_huller', 'type_model','kapasitas', 'pk_mesin','buatan', 'jumlah_unit')
	search_fields = ('detil_huller','mesin_huller', 'type_model','kapasitas', 'pk_mesin','buatan', 'jumlah_unit')

	def get_readonly_fields(self, request, obj=None):
		rf = ('verified_by', 'verified_at', 'created_by', 'created_at', 'updated_at')
		if obj:
			if not request.user.is_superuser:
				rf = rf+('status',)
		return rf

	def get_fieldsets(self, request, obj = None):
		if obj or request.user.is_superuser:
			add_fieldsets = (
				(None, {
					'classes': ('wide',),
					'fields': ('detil_huller','mesin_huller',)
					}
				),
				('Detail Izin', {'fields': ('type_model','kapasitas', 'pk_mesin','buatan', 'jumlah_unit')}),
				('Lain-lain', {'fields': ('status', 'created_by', 'created_at', 'verified_by', 'verified_at', 'updated_at')}),
			)

		else:
			add_fieldsets = (
				(None, {
					'classes': ('wide',),
					'fields': ('detil_huller','mesin_huller',)
					}
				),
				('Detail Izin', {'fields': ('type_model','kapasitas', 'pk_mesin','buatan', 'jumlah_unit')}),
				('Lain-lain', {'fields': ('status', 'created_by', 'created_at', 'verified_by', 'verified_at', 'updated_at')}),
			)
		return add_fieldsets

admin.site.register(MesinPerusahaan, MesinPerusahaanAdmin)