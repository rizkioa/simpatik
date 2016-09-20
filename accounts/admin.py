from accounts.models import Account, IdentitasPribadi, NomorIdentitasPengguna
from accounts.account_admin import AccountAdmin

from django.contrib import admin

# Register your models here.


admin.site.register(Account, AccountAdmin)

class IdentitasPribadiAdmin(admin.ModelAdmin):
	list_display = ('nama_lengkap','tanggal_lahir','telephone','alamat')
	list_filter = ('nama_lengkap','tanggal_lahir','alamat')
	search_fields = ('nama_lengkap','tanggal_lahir','alamat')

admin.site.register(IdentitasPribadi,IdentitasPribadiAdmin)

class NomorIdentitasPenggunaAdmin(admin.ModelAdmin):
	list_display = ('nomor','user','jenis_identitas')
	list_filter = ('nomor','user','jenis_identitas')
	search_fields = ('nomor','user','jenis_identitas')

admin.site.register(NomorIdentitasPengguna, NomorIdentitasPenggunaAdmin)
