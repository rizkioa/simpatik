import datetime
import base64
from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, resolve

from accounts.models import NomorIdentitasPengguna
from izin.models import DetilTDP, Syarat, SKIzin, Riwayat

class DetilTDPAdmin(admin.ModelAdmin):
	list_display = ('get_no_pengajuan', 'pemohon', 'get_kelompok_jenis_izin')

	def get_kelompok_jenis_izin(self, obj):
		return obj.kelompok_jenis_izin
	get_kelompok_jenis_izin.short_description = "Izin Pengajuan"

	def get_no_pengajuan(self, obj):
		no_pengajuan = mark_safe("""
			<a href="%s" target="_blank"> %s </a>
			""" % ("#", obj.no_pengajuan ))
		split_ = obj.no_pengajuan.split('/')
		# print split_
		if split_[0] == 'TDP':
			no_pengajuan = mark_safe("""
				<a href="%s" target="_blank"> %s </a>
				""" % (reverse('admin:izin_detiltdp_change', args=(obj.id,)), obj.no_pengajuan ))
		return no_pengajuan
	get_no_pengajuan.short_description = "No. Pengajuan"

	def view_pengajuan_tdp_pt(self, request, id_pengajuan_izin_):
		extra_context = {}
		extra_context.update({'has_permission': True })
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			pengajuan_ = DetilTDP.objects.get(id=id_pengajuan_izin_)
			alamat_ = ""
			alamat_perusahaan_ = ""
			pemohon_ = pengajuan_.pemohon
			perusahaan_ = pengajuan_.perusahaan
			if pengajuan_:
				ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pemohon_.id, jenis_identitas_id=1).last()
				paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pemohon_.id, jenis_identitas_id=2).last()
				alamat_ = str(pemohon_.alamat)+", Ds. "+str(pemohon_.desa)+", Kec. "+str(pemohon_.desa.kecamatan)+", "+str(pemohon_.desa.kecamatan.kabupaten)
				alamat_perusahaan_ = str(perusahaan_.alamat_perusahaan)+", Ds. "+str(perusahaan_.desa)+", Kec. "+str(perusahaan_.desa.kecamatan)+", "+str(perusahaan_.desa.kecamatan.kabupaten)
				
				extra_context.update({'pengajuan':pengajuan_, 'pemohon': pemohon_, 'alamat_pemohon': alamat_, 'perusahaan':perusahaan_, 'alamat_perusahaan':alamat_perusahaan_, 'ktp':ktp_, 'paspor':paspor_, 'status': pengajuan_.status})
				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
				riwayat_ = Riwayat.objects.filter(pengajuan_izin_id = id_pengajuan_izin_).order_by('created_at')
				if riwayat_:
					extra_context.update({'riwayat': riwayat_ })
				skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
				if skizin_:
					extra_context.update({'skizin': skizin_, 'skizin_status': skizin_.status })
		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_tdp_pt.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))


	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilTDPAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^view-pengajuan-tdp-pt/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_tdp_pt), name='view_pengajuan_tdp_pt'),
			)
		return my_urls + urls

admin.site.register(DetilTDP, DetilTDPAdmin)