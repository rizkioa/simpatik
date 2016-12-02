from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.template import RequestContext, loader
from django.http import HttpResponse

from izin.models import DetilIUJK, SKIzin, Riwayat, Syarat
from accounts.models import NomorIdentitasPengguna
from izin.utils import formatrupiah


class DetilIUJKAdmin(admin.ModelAdmin):

	
	
	def view_pengajuan_siup(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			pengajuan_ = DetilIUJK.objects.get(id=id_pengajuan_izin_)
			
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
				nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
				ktp_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(jenis_identitas_id=1).last()
				paspor_ = pengajuan_.pemohon.nomoridentitaspengguna_set.filter(jenis_identitas_id=2).last()
				extra_context.update({'ktp': ktp_ })
				extra_context.update({'paspor': paspor_ })
				extra_context.update({'nomor_identitas': nomor_identitas_ })
				try:
					ktp_ = NomorIdentitasPengguna.objects.get(user_id=pengajuan_.pemohon.id, jenis_identitas__id=1)
					extra_context.update({'cookie_file_ktp': ktp_.berkas })
				except ObjectDoesNotExist:
					pass
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
					extra_context.update({'alamat_perusahaan': alamat_perusahaan_ })
				extra_context.update({'perusahaan': pengajuan_.perusahaan})
				legalitas_pendirian = pengajuan_.legalitas.filter(~Q(jenis_legalitas_id=2)).last()
				legalitas_perubahan = pengajuan_.legalitas.filter(jenis_legalitas_id=2).last()
				extra_context.update({ 'legalitas_pendirian': legalitas_pendirian })
				extra_context.update({ 'legalitas_perubahan': legalitas_perubahan })
			
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})
			extra_context.update({'status': pengajuan_.status})
			extra_context.update({'pengajuan': pengajuan_})
			#+++++++++++++ page logout ++++++++++
			extra_context.update({'has_permission': True })
			#+++++++++++++ end page logout ++++++++++
			banyak = len(DetilIUJK.objects.all())
			extra_context.update({'banyak': banyak})
			syarat_ = Syarat.objects.filter(jenis_izin__jenis_izin__kode="SIUP")
			extra_context.update({'syarat': syarat_})
			kekayaan_bersih = int(0)
			extra_context.update({'kekayaan_bersih': formatrupiah(kekayaan_bersih)})
			total_nilai_saham = int(0)
			extra_context.update({'total_nilai_saham': formatrupiah(total_nilai_saham)})

			try:
				skizin_ = SKIzin.objects.filter(pengajuan_izin_id = id_pengajuan_izin_ ).last()
				if skizin_:
					extra_context.update({'skizin': skizin_ })
					extra_context.update({'skizin_status': skizin_.status })
			except ObjectDoesNotExist:
				pass
			try:
				riwayat_ = Riwayat.objects.filter(pengajuan_izin_id = id_pengajuan_izin_).order_by('created_at')
				if riwayat_:
					extra_context.update({'riwayat': riwayat_ })
			except ObjectDoesNotExist:
				pass
		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_iujk.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilIUJKAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^view-pengajuan-iujk/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_siup), name='view_pengajuan_iujk'),
			)
		return my_urls + urls

admin.site.register(DetilIUJK, DetilIUJKAdmin)