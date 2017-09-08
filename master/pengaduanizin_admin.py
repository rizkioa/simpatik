from django.contrib import admin
from models import PengaduanIzin
from django.utils.safestring import mark_safe


class PengaduanIzinAdmin(admin.ModelAdmin):
	list_display = ('no_ktp', 'nama_lengkap', 'kelompok_jenis_izin', 'detil')

	def detil(self, obj):
		return mark_safe('<a class="btn btn-xs btn-info" tittle="Lihat Detil">Lihat Detil</a>')
	detil.short_description = 'Aksi'
admin.site.register(PengaduanIzin, PengaduanIzinAdmin)