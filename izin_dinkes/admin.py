from django.contrib import admin
from izin_dinkes.models import *
from tokoobat_admin import TokoObatAdmin

# Register your models here.



class ApotekAdmin(admin.ModelAdmin):
	list_display = ('nama_apotek', 'no_telepon', 'alamat_sarana')
admin.site.register(Apotek, ApotekAdmin)

class LaboratoriumAdmin(admin.ModelAdmin):
	list_display = ('klasifikasi_laboratorium', 'nama_laboratorium', 'alamat_laboratorium', 'penanggung_jawab_teknis')
	
admin.site.register(Laboratorium, LaboratoriumAdmin)
admin.site.register(TokoObat, TokoObatAdmin)
