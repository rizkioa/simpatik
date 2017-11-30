from accounts.models import Account, IdentitasPribadi, NomorIdentitasPengguna, HakAkses
from accounts.account_admin import AccountAdmin

from django.contrib import admin
# from django.contrib.auth.models import Group
# Register your models here.


# admin.site.unregister(Group)
class HakAksesAdmin(admin.ModelAdmin):
	list_display = ('name', 'keterangan')

admin.site.register(HakAkses, HakAksesAdmin)


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

