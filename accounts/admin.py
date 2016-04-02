from accounts.models import Account, IdentitasPribadi, SKPD, Bidang, Jabatan, NomorIdentitasPengguna, Pegawai
from accounts.account_admin import AccountAdmin

from django.contrib import admin


# Register your models here.


admin.site.register(Account, AccountAdmin)

class IdentitasPribadiAdmin(admin.ModelAdmin):
	list_display = ('nama_lengkap','tanggal_lahir','telephone','alamat')
	list_filter = ('nama_lengkap','tanggal_lahir','alamat')
	search_fields = ('nama_lengkap','tanggal_lahir','alamat')

admin.site.register(IdentitasPribadi,IdentitasPribadiAdmin)

class SKPDAdmin(admin.ModelAdmin):
	list_display = ('kode_satker','nama_skpd','kepala','plt')
	list_filter = ('nama_skpd','kepala','plt')
	search_fields = ('kode_satker','nama_skpd','kepala')

admin.site.register(SKPD,SKPDAdmin)

class BidangAdmin(admin.ModelAdmin):
	list_display = ('nama_bidang','kepala','plt','keterangan')
	list_filter = ('nama_bidang','kepala','plt')
	search_fields = ('nama_bidang','kepala','plt')

admin.site.register(Bidang,BidangAdmin)

class NomorIdentitasPenggunaAdmin(admin.ModelAdmin):
	list_display = ('nomor','user','jenis_identitas')
	list_filter = ('nomor','user','jenis_identitas')
	search_fields = ('nomor','user','jenis_identitas')

admin.site.register(NomorIdentitasPengguna, NomorIdentitasPenggunaAdmin)

class JabatanAdmin(admin.ModelAdmin):
	list_display = ('nama_jabatan','keterangan')
	list_filter = ('nama_jabatan',)

admin.site.register(Jabatan, JabatanAdmin)

class PegawaiAdmin(admin.ModelAdmin):
	list_display = ('skpd','bidang','jabatan')
	list_filter = ('skpd','bidang','jabatan')
	search_fields = ('skpd','bidang','jabatan')

admin.site.register(Pegawai,PegawaiAdmin)
