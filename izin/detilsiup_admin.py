from django.contrib import admin
from django.core.urlresolvers import reverse, resolve
from izin.models import DetilSIUP
from django.utils.safestring import mark_safe

class DetilSIUPAdmin(admin.ModelAdmin):
	list_display = ('get_no_pengajuan', 'pemohon', 'get_kelompok_jenis_izin','jenis_permohonan', 'status')
	search_fields = ('no_izin', 'pemohon__nama_lengkap')

	def get_kelompok_jenis_izin(self, obj):
		return obj.kelompok_jenis_izin
	get_kelompok_jenis_izin.short_description = "Izin Pengajuan"

	def get_no_pengajuan(self, obj):
		no_pengajuan = mark_safe("""
			<a href="%s" target="_blank"> %s </a>
			""" % ("#", obj.no_pengajuan ))
		split_ = obj.no_pengajuan.split('/')
		# print split_
		if split_[0] == 'SIUP':
			no_pengajuan = mark_safe("""
				<a href="%s" target="_blank"> %s </a>
				""" % (reverse('admin:izin_detilsiup_change', args=(obj.id,)), obj.no_pengajuan ))
		return no_pengajuan
	get_no_pengajuan.short_description = "No. Pengajuan"

	def get_fieldsets(self, request, obj=None):
		fields = ('pemohon', 'kelompok_jenis_izin', 'jenis_permohonan', 'no_pengajuan', 'no_izin', 'nama_kuasa', 'no_identitas_kuasa', 'telephone_kuasa', 'berkas_tambahan', 'perusahaan', 'berkas_foto', 'berkas_npwp_pemohon', 'berkas_npwp_perusahaan', 'legalitas', 'kbli', 'kelembagaan', 'produk_utama', 'bentuk_kegiatan_usaha', 'jenis_penanaman_modal', 'kekayaan_bersih', 'total_nilai_saham', 'presentase_saham_nasional', 'presentase_saham_asing')
		fields_admin = ('status', 'created_by', 'verified_by', 'rejected_by')
		if obj:
			if request.user.is_superuser:
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': fields+fields_admin
						}),
				)
			elif request.user.groups.filter(name='Operator') or request.user.groups.filter(name='Kabid') or request.user.groups.filter(name='Kadin') or request.user.groups.filter(name='Pembuat Surat') or request.user.groups.filter(name='Penomoran'):
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': fields
						}),
				)
			else:
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': ('no_pengajuan',)
						}),
					)
		else:
			pass
		return add_fieldsets

	def get_readonly_fields(self, request, obj=None):
		rf = ('pemohon', 'kelompok_jenis_izin', 'jenis_permohonan', 'no_pengajuan', 'no_izin', 'nama_kuasa', 'no_identitas_kuasa', 'telephone_kuasa', 'berkas_tambahan', 'perusahaan', 'berkas_foto', 'berkas_npwp_pemohon', 'berkas_npwp_perusahaan', 'legalitas', 'kbli', 'kelembagaan', 'produk_utama', 'bentuk_kegiatan_usaha', 'jenis_penanaman_modal', 'kekayaan_bersih', 'total_nilai_saham', 'presentase_saham_nasional', 'presentase_saham_asing')
		rf_admin = ('status', 'created_by', 'verified_by', 'rejected_by')
		rf_superuser = (None,)
		# if request.user.is_superuser:
		# 	return rf
		if request.user.groups.filter(name='Penomoran'):
			rf = ('no_pengajuan')
			return rf
		elif request.user.groups.filter(name='Operator'):
			rf = rf_admin
		elif request.user.groups.filter(name='Kabid') or request.user.groups.filter(name='Kadin') or request.user.groups.filter(name='Pembuat Surat') or request.user.groups.filter(name='Penomoran'):
			rf = rf + rf_admin
		else:
			return rf_superuser
		return rf

admin.site.register(DetilSIUP, DetilSIUPAdmin)