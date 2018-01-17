from django.contrib import admin
from izin_dinkes.models import *
from tokoobat_admin import TokoObatAdmin
from apotek_admin import ApotekAdmin
from optikal_admin import OptikalAdmin
from mendirikan_klinik_admin import MendirikanKlinikAdmin
from operasional_klinik_admin import OperasionalKlinikAdmin

# Register your models here.



admin.site.register(Apotek, ApotekAdmin)
admin.site.register(Sarana)
admin.site.register(JenisKlinik)

class LaboratoriumAdmin(admin.ModelAdmin):
	list_display = ('klasifikasi_laboratorium', 'nama_laboratorium', 'alamat_laboratorium', 'penanggung_jawab_teknis')

class PengunduranApotekerAdmin(admin.ModelAdmin):
	list_display = ('nama_apotek', 'nama_apoteker', 'tanggal_lahir')
	
admin.site.register(Laboratorium, LaboratoriumAdmin)
admin.site.register(TokoObat, TokoObatAdmin)
admin.site.register(Optikal, OptikalAdmin)
admin.site.register(MendirikanKlinik, MendirikanKlinikAdmin)
admin.site.register(OperasionalKlinik, OperasionalKlinikAdmin)
admin.site.register(PengunduranApoteker, PengunduranApotekerAdmin)
