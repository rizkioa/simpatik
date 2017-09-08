from django.contrib import admin
from models import PengaduanIzin

class PengaduanIzinAdmin(admin.ModelAdmin):
	list_display = ('no_ktp', 'nama_lengkap', 'no_telp', 'email', 'kelompok_jenis_izin', 'isi_pengdauan')
admin.site.register(PengaduanIzin, PengaduanIzinAdmin)