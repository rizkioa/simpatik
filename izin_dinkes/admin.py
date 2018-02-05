from django.contrib import admin
from izin_dinkes.models import *
from tokoobat_admin import TokoObatAdmin
from apotek_admin import ApotekAdmin
from optikal_admin import OptikalAdmin
from mendirikan_klinik_admin import MendirikanKlinikAdmin
from operasional_klinik_admin import OperasionalKlinikAdmin
from laboratorium_admin import LaboratoriumAdmin
from penutupan_apotek import PenutupanApotekAdmin

# Register your models here.



admin.site.register(Apotek, ApotekAdmin)
admin.site.register(Sarana)
admin.site.register(JenisKlinik)
admin.site.register(Laboratorium, LaboratoriumAdmin)
admin.site.register(PenutupanApotek, PenutupanApotekAdmin)
admin.site.register(TokoObat, TokoObatAdmin)
admin.site.register(Optikal, OptikalAdmin)
admin.site.register(MendirikanKlinik, MendirikanKlinikAdmin)
admin.site.register(OperasionalKlinik, OperasionalKlinikAdmin)
admin.site.register(PengunduranApoteker)
