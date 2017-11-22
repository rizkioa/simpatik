from django.contrib import admin
from izin_dinkes.models import *

# Register your models here.



class ApotekAdmin(admin.ModelAdmin):
	list_display = ('nama_apotek', 'no_telepon', 'alamat_sarana')
admin.site.register(Apotek, ApotekAdmin)