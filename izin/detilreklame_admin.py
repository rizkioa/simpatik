from django.contrib import admin
from izin.models import DetilReklame, Syarat, SKIzin, Riwayat, Survey,DetilPembayaran,DetilReklameIzin
from kepegawaian.models import Pegawai, UnitKerja
from accounts.models import NomorIdentitasPengguna
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
from django.http import HttpResponse
import base64
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, resolve
import datetime
import collections
from izin.utils import*

class DetilReklameAdmin(admin.ModelAdmin):
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
		if split_[0] == 'Reklame':
			no_pengajuan = mark_safe("""
				<a href="%s" target="_blank"> %s </a>
				""" % (reverse('admin:izin_detilreklame_change', args=(obj.id,)), obj.no_pengajuan ))
		return no_pengajuan
	get_no_pengajuan.short_description = "No. Pengajuan"

	def get_readonly_fields(self, request, obj=None):
		rf = ('verified_by', 'verified_at', 'created_by', 'created_at', 'updated_at')
		if obj:
			if not request.user.is_superuser:
				rf = rf+('status',)
		return rf

	def get_fieldsets(self, request, obj = None):
		if obj or request.user.is_superuser:
			add_fieldsets = (
				(None, {
					'classes': ('wide',),
					'fields': ('pemohon',)
					}
				),
				('Detail Izin', {'fields': ('kelompok_jenis_izin', 'jenis_permohonan','no_pengajuan', 'no_izin','legalitas')}),
				('Detail Kuasa', {'fields': ('nama_kuasa','no_identitas_kuasa','telephone_kuasa',) }),
				
				('Detail Reklame', {'fields': ('perusahaan','jenis_reklame','judul_reklame','jumlah','panjang','lebar','sisi','letak_pemasangan','desa',('tanggal_mulai','tanggal_akhir'),'lt','lg') }),
				
				('Berkas & Keterangan', {'fields': ('berkas_tambahan', 'keterangan',)}),

				('Lain-lain', {'fields': ('status', 'created_by', 'created_at', 'verified_by', 'verified_at', 'updated_at')}),
			)
		else:
			add_fieldsets = (
				(None, {
					'classes': ('wide',),
					'fields': ('pemohon',)
					}
				),
				('Detail Izin', {'fields': ('kelompok_jenis_izin', 'jenis_permohonan','no_pengajuan', 'no_izin','legalitas')}),
				('Detail Kuasa', {'fields': ('nama_kuasa','no_identitas_kuasa','telephone_kuasa',) }),
				('Detail Reklame', {'fields': ('perusahaan','jenis_reklame','judul_reklame','jumlah','panjang','lebar','sisi','letak_pemasangan','desa',('tanggal_mulai','tanggal_akhir'),'lt','lg') }),
				('Berkas & Keterangan', {'fields': ('berkas_tambahan', 'keterangan',)}),
			)
		return add_fieldsets

	def view_pengajuan_reklame(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			extra_context.update({'pegawai_list' : Pegawai.objects.filter(unit_kerja_id=72) })
			pengajuan_ = DetilReklame.objects.get(id=id_pengajuan_izin_)
			detil_reklame_list = DetilReklameIzin.objects.filter(detil_reklame_id=id_pengajuan_izin_)
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.pemohon.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
				extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
				nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all().last()
				extra_context.update({'nomor_identitas': nomor_identitas_ })
				try:
					try:
						ktp_ = NomorIdentitasPengguna.objects.get(user_id=pengajuan_.pemohon.id)
					except NomorIdentitasPengguna.MultipleObjectsReturned:
						ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id).last()
					extra_context.update({'cookie_file_ktp': ktp_.berkas })
				except ObjectDoesNotExist:
					pass
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({'alamat_perusahaan': alamat_perusahaan_ })
				extra_context.update({'perusahaan': pengajuan_.perusahaan})

				legalitas_pendirian = pengajuan_.perusahaan.legalitas_set.filter(berkas__keterangan="akta pendirian").last()
				legalitas_perubahan = pengajuan_.perusahaan.legalitas_set.filter(berkas__keterangan="akta perubahan").last()
				extra_context.update({ 'legalitas_pendirian': legalitas_pendirian })
				extra_context.update({ 'legalitas_perubahan': legalitas_perubahan })

			extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})

			# UNTUK SURVEY
			from django.contrib.auth.models import Group

			extra_context.update({'skpd_list' : UnitKerja.objects.all() })

			h = Group.objects.filter(name="Cek Lokasi")
			if h.exists():
				h = h.last()
			h = h.user_set.all()
			extra_context.update({'pegawai_list' : h })

			try:
				try:
					s = Survey.objects.get(pengajuan=pengajuan_)
				except Survey.MultipleObjectsReturned:
					s = Survey.objects.filter(pengajuan=pengajuan_).last()
					# print s.survey_iujk.all()
				print s.survey_reklame_ho.all()
				extra_context.update({'detilbap': s.survey_reklame_ho.all().last() })
			except ObjectDoesNotExist:
				s = ''

			extra_context.update({'survey': s })
			# END UNTUK SURVEY

			
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})
			extra_context.update({'status': pengajuan_.status})
			extra_context.update({'detil_reklame_list': detil_reklame_list})
			extra_context.update({'pengajuan': pengajuan_})
			encode_pengajuan_id = (str(pengajuan_.id))
			extra_context.update({'pengajuan_id': encode_pengajuan_id})
			#+++++++++++++ page logout ++++++++++
			extra_context.update({'has_permission': True })
			#+++++++++++++ end page logout ++++++++++
			if pengajuan_.tanggal_mulai and pengajuan_.tanggal_akhir:
				tanggal_mulai = pengajuan_.tanggal_mulai
				tanggal_akhir = pengajuan_.tanggal_akhir

				jumlah_lama =  tanggal_akhir-tanggal_mulai
				extra_context.update({'jumlah_lama': jumlah_lama})

			# lama_pemasangan = pengajuan_.tanggal_akhir-pengajuan_.tanggal_mulai
			# print lama_pemasangan
			banyak = len(DetilReklame.objects.all())
			extra_context.update({'banyak': banyak})
			syarat_ = Syarat.objects.filter(jenis_izin__jenis_izin__kode="reklame")
			extra_context.update({'syarat': syarat_})
			try:
				skizin_ = SKIzin.objects.get(pengajuan_izin_id = id_pengajuan_izin_ )
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
		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_reklame.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_reklame_asli(self, request, id_pengajuan_izin_):
		extra_context = {}
		# id_pengajuan_izin_ = base64.b64decode(id_pengajuan_izin_)
		# print id_pengajuan_izin_
		if id_pengajuan_izin_:
			pengajuan_ = DetilReklame.objects.get(id=id_pengajuan_izin_)
			detail_list = DetilReklameIzin.objects.filter(detil_reklame_id=id_pengajuan_izin_).values_list('tipe_reklame__jenis_tipe_reklame', flat=True)
			detil_reklame_list = [item for item, count in collections.Counter(detail_list).items() if count >= 1]	
			alamat_ = ""
			alamat_perusahaan_ = ""
			if pengajuan_.pemohon:
				if pengajuan_.pemohon.desa:
					alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.pemohon.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({'alamat_pemohon': alamat_})
				extra_context.update({'pemohon': pengajuan_.pemohon})
			if pengajuan_.perusahaan:
				if pengajuan_.perusahaan.desa:
					alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
					extra_context.update({'alamat_perusahaan': alamat_perusahaan_})
				extra_context.update({'perusahaan': pengajuan_.perusahaan })
			nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
			extra_context.update({'nomor_identitas': nomor_identitas_ })
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'pengajuan': pengajuan_ })
			extra_context.update({'foto': pengajuan_.pemohon.berkas_foto.all().last()})
			if pengajuan_.desa:
				letak_ = pengajuan_.letak_pemasangan + ",Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())
			else:
				letak_ = pengajuan_.letak_pemasangan
			
			if pengajuan_.panjang:
				panjang_ = '{0:f}'.format(pengajuan_.panjang)
				p = panjang_.split(".")[1]
				if p == "00":
					panjang_ = ("%.0f" % pengajuan_.panjang)
				else:
					panjang_ = pengajuan_.panjang
				extra_context.update({'panjang_': panjang_})
			if pengajuan_.lebar:
				lebar_ = '{0:f}'.format(pengajuan_.lebar)
				l = lebar_.split(".")[1]
				if l == "00":
					lebar_ = ("%.0f" % pengajuan_.lebar)
				else:
					lebar_ = pengajuan_.lebar
				extra_context.update({'lebar_': lebar_})
			if pengajuan_.sisi:
				sisi_ = '{0:f}'.format(pengajuan_.sisi)
				s = sisi_.split(".")[1]
				if s == "00":
					sisi_ = ("%.0f" % pengajuan_.sisi)
				else:
					sisi_ = pengajuan_.sisi
				extra_context.update({'sisi_': sisi_})
				
			extra_context.update({'detil_reklame_list': detil_reklame_list})	
			extra_context.update({'letak_pemasangan': letak_})
			if pengajuan_.tanggal_mulai and pengajuan_.tanggal_akhir:
				tanggal_mulai = pengajuan_.tanggal_mulai
				tanggal_akhir = pengajuan_.tanggal_akhir

				jumlah_lama =  tanggal_akhir-tanggal_mulai
				extra_context.update({'jumlah_lama': jumlah_lama})
			try:
				skizin_ = SKIzin.objects.get(pengajuan_izin_id = id_pengajuan_izin_ )
				if skizin_:
					extra_context.update({'skizin': skizin_ })
					extra_context.update({'skizin_status': skizin_.status })
			except ObjectDoesNotExist:
				pass
			try:
				kepala_ =  Pegawai.objects.get(jabatan__nama_jabatan="Kepala Dinas")
				if kepala_:
					extra_context.update({'gelar_depan': kepala_.gelar_depan })
					extra_context.update({'nama_kepala_dinas': kepala_.nama_lengkap })
					extra_context.update({'nip_kepala_dinas': kepala_.nomoridentitaspengguna_set.last() })

			except ObjectDoesNotExist:
				pass
			try:
				retribusi_ = DetilPembayaran.objects.get(pengajuan_izin__id = id_pengajuan_izin_)
				if retribusi_:
					n = int(retribusi_.jumlah_pembayaran.replace(".", ""))
					terbilang_ = terbilang(n)
					extra_context.update({'retribusi': retribusi_ })
					extra_context.update({'terbilang': terbilang_ })
					extra_context.update({'retribusi_': retribusi_ })
					
			except ObjectDoesNotExist:
				pass
			# print pengajuan_.kbli.nama_kbli.all()
			# print pengajuan_.produk_utama
		template = loader.get_template("front-end/include/formulir_reklame/cetak_reklame_asli.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def cetak_bukti_admin_reklame(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			pengajuan_ = DetilReklame.objects.get(id=id_pengajuan_izin_)
			detil_reklame_list = DetilReklameIzin.objects.filter(detil_reklame_id=id_pengajuan_izin_)
			if pengajuan_.perusahaan != '':
				alamat_ = ""
				alamat_perusahaan_ = ""
				if pengajuan_.pemohon:
					if pengajuan_.pemohon.desa:
						alamat_ = str(pengajuan_.pemohon.alamat)+", Desa "+str(pengajuan_.pemohon.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.pemohon.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.pemohon.desa.kecamatan.kabupaten.nama_kabupaten.title())
						extra_context.update({ 'alamat_pemohon': alamat_ })
					extra_context.update({ 'pemohon': pengajuan_.pemohon })
					paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
					ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
					extra_context.update({ 'paspor': paspor_ })
					extra_context.update({ 'ktp': ktp_ })
				if pengajuan_.perusahaan:
					if pengajuan_.perusahaan.desa:
						alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", Desa "+str(pengajuan_.perusahaan.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.perusahaan.desa.kecamatan.kabupaten.nama_kabupaten.title())
						extra_context.update({ 'alamat_perusahaan': alamat_perusahaan_ })
					extra_context.update({ 'perusahaan': pengajuan_.perusahaan })
					syarat = Syarat.objects.filter(jenis_izin__jenis_izin__id="3")
				if pengajuan_.desa:
					letak_ = pengajuan_.letak_pemasangan + ",Desa "+str(pengajuan_.desa.nama_desa.title()) + ", Kec. "+str(pengajuan_.desa.kecamatan.nama_kecamatan.title())+", "+ str(pengajuan_.desa.kecamatan.kabupaten.nama_kabupaten.title())
				else:
					letak_ = pengajuan_.letak_pemasangan

				if pengajuan_.panjang:
					panjang_ = '{0:f}'.format(pengajuan_.panjang)
					p = panjang_.split(".")[1]
					if p == "00":
						panjang_ = ("%.0f" % pengajuan_.panjang)
					else:
						panjang_ = pengajuan_.panjang
					extra_context.update({'panjang_': panjang_})
				if pengajuan_.lebar:
					lebar_ = '{0:f}'.format(pengajuan_.lebar)
					l = lebar_.split(".")[1]
					if l == "00":
						lebar_ = ("%.0f" % pengajuan_.lebar)
					else:
						lebar_ = pengajuan_.lebar
					extra_context.update({'lebar_': lebar_})
				if pengajuan_.sisi:
					sisi_ = '{0:f}'.format(pengajuan_.sisi)
					s = sisi_.split(".")[1]
					if s == "00":
						sisi_ = ("%.0f" % pengajuan_.sisi)
					else:
						sisi_ = pengajuan_.sisi
					extra_context.update({'sisi_': sisi_})

				if pengajuan_.tanggal_mulai:
					awal = pengajuan_.tanggal_mulai
				else:
					awal = 0
				if pengajuan_.tanggal_akhir:
					akhir = pengajuan_.tanggal_akhir
				else:
					akhir = 0
				
				selisih = akhir-awal
				extra_context.update({'title': 'Proses Pengajuan'})
				# extra_context.update({'ukuran': ukuran_})
				extra_context.update({'letak_pemasangan': letak_})
				extra_context.update({'detil_reklame_list': detil_reklame_list})
				if pengajuan_.tanggal_mulai:
					extra_context.update({'selisih': selisih.days})
				else:
					extra_context.update({'selisih': selisih})
				extra_context.update({ 'pengajuan': pengajuan_ })
				extra_context.update({ 'syarat': syarat })
				extra_context.update({ 'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin })
			extra_context.update({ 'created_at': pengajuan_.created_at })
		template = loader.get_template("front-end/include/formulir_reklame/cetak_bukti_pendaftaran.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(DetilReklameAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^cetak-reklame-asli/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.cetak_reklame_asli), name='cetak_reklame_asli'),
			url(r'^view-pengajuan-reklame/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_reklame), name='view_pengajuan_reklame'),
			url(r'^cetak-bukti-pendaftaran-admin/(?P<id_pengajuan_izin_>[0-9]+)/$', self.admin_site.admin_view(self.cetak_bukti_admin_reklame), name='cetak_bukti_admin_reklame'),
			)
		return my_urls + urls

admin.site.register(DetilReklame, DetilReklameAdmin)