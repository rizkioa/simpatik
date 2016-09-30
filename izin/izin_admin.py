from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils.safestring import mark_safe

from izin.models import PengajuanIzin, JenisIzin, KelompokJenisIzin, Syarat, DetilSIUP
from izin.controllers.siup import add_wizard_siup, formulir_siup, cetak

import json

class IzinAdmin(admin.ModelAdmin):
	list_display = ('get_no_pengajuan', 'get_tanggal_pengajuan', 'get_kelompok_jenis_izin', 'pemohon','jenis_permohonan', 'get_status_proses','status', 'button_cetak_pendaftaran')
	list_filter = ('kelompok_jenis_izin',)
	search_fields = ('no_izin', 'pemohon__nama_lengkap')

	def changelist_view(self, request, extra_context={}):
		izin = KelompokJenisIzin.objects.all()
		extra_context.update({'izin': izin})
		return super(IzinAdmin, self).changelist_view(request, extra_context=extra_context)

	def get_fieldsets(self, request, obj=None):
		fields = ('pemohon', 'kelompok_jenis_izin', 'jenis_permohonan', 'no_pengajuan', 'no_izin', 'nama_kuasa', 'no_identitas_kuasa', 'telephone_kuasa', 'berkas_tambahan', 'perusahaan', 'berkas_foto', 'berkas_npwp_pemohon', 'berkas_npwp_perusahaan', 'legalitas', 'kbli', 'kelembagaan', 'produk_utama', 'bentuk_kegiatan_usaha', 'jenis_penanaman_modal', 'kekayaan_bersih', 'total_nilai_saham', 'presentase_saham_nasional', 'presentase_saham_asing')
		fields_admin = ('status', 'created_by', 'created_at', 'verified_by', 'verified_at', 'rejected_by', 'rejected_at')
		if obj:
			if request.user.is_superuser:
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': fields+fields_admin
						}),
				)
			elif request.user.groups.filter(name='Operator') or request.user.groups.filter(name='Kabid'):
				add_fieldsets = (
					(None, {
						'classes': ('wide',),
						'fields': fields
						}),
				)
		else:
			pass
		return add_fieldsets

	def get_perusahaan(self, obj):
		return "Perusaahaan Maju Mundur"
	get_perusahaan.short_description = "Perusahaan"

	def get_status_proses(self, obj):
		return "%s\n%s" % (obj.created_at.strftime("%d/%m/%y"), "Pengajuan Dibuat")
	get_status_proses.short_description = "Tgl & Status Proses"

	def get_kelompok_jenis_izin(self, obj):
		return obj.kelompok_jenis_izin
	get_kelompok_jenis_izin.short_description = "Izin Pengajuan"

	def get_tanggal_pengajuan(self, obj):
		return obj.created_at
	get_tanggal_pengajuan.short_description = "Tgl. Pengajuan"

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

	def button_cetak_pendaftaran(self, obj):
		btn = mark_safe("""
			<a href="%s" target="_blank" class="btn btn-success btn-rounded-20 btn-ef btn-ef-5 btn-ef-5a mb-10"><i class="fa fa-cog"></i> <span>Proses</span> </a>
			""" % reverse('admin:view_pengajuan_siup', kwargs={'id_pengajuan_izin_': obj.id}))
			# reverse('admin:print_out_pendaftaran', kwargs={'id_pengajuan_izin_': obj.id})
		return btn
	button_cetak_pendaftaran.short_description = "Aksi"

	def pendaftaran_selesai(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Pengajuan Selesai'})
			pengajuan_ = PengajuanIzin.objects.get(id=id_pengajuan_izin_)
			extra_context.update({'pemohon': pengajuan_.pemohon})
			extra_context.update({'id_pengajuan': pengajuan_.id})
			extra_context.update({'jenis_pemohon': pengajuan_.pemohon.jenis_pemohon})
			extra_context.update({'alamat_pemohon': str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)})
			extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})


		template = loader.get_template("admin/izin/izin/pengajuan_baru_selesai.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def print_out_pendaftaran(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Pengajuan Selesai'})
			pengajuan_ = PengajuanIzin.objects.get(id=id_pengajuan_izin_)
			extra_context.update({'pemohon': pengajuan_.pemohon})
			nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
			extra_context.update({'nomor_identitas': nomor_identitas_ })
			extra_context.update({'jenis_pemohon': pengajuan_.pemohon.jenis_pemohon})
			alamat_ = ""
			if pengajuan_.pemohon.desa:
				alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
			extra_context.update({'alamat_pemohon': alamat_})
			extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})

			syarat_ = Syarat.objects.filter(jenis_izin__id=pengajuan_.id)
			extra_context.update({'syarat': syarat_})

		# template = loader.get_template("admin/izin/izin/add_wizard.html")
		template = loader.get_template("admin/izin/izin/cetak_bukti_pendaftaran.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def view_pengajuan_siup(self, request, id_pengajuan_izin_):
		extra_context = {}
		if id_pengajuan_izin_:
			extra_context.update({'title': 'Proses Pengajuan'})
			pengajuan_ = PengajuanIzin.objects.get(id=id_pengajuan_izin_)
			extra_context.update({'pemohon': pengajuan_.pemohon})
			nomor_identitas_ = pengajuan_.pemohon.nomoridentitaspengguna_set.all()
			extra_context.update({'nomor_identitas': nomor_identitas_ })
			extra_context.update({'jenis_pemohon': pengajuan_.pemohon.jenis_pemohon})
			alamat_ = ""
			if pengajuan_.pemohon.desa:
				alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", Kab./Kota "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
			extra_context.update({'alamat_pemohon': alamat_})
			extra_context.update({'jenis_permohonan': pengajuan_.jenis_permohonan})
			extra_context.update({'kelompok_jenis_izin': pengajuan_.kelompok_jenis_izin})
			extra_context.update({'created_at': pengajuan_.created_at})
			extra_context.update({'status': pengajuan_.status})
			extra_context.update({'pengajuan': pengajuan_})
			#+++++++++++++ page logout ++++++++++
			extra_context.update({'has_permission': True })
			#+++++++++++++ end page logout ++++++++++
			syarat_ = Syarat.objects.filter(jenis_izin__jenis_izin__kode="SIUP")
			extra_context.update({'syarat': syarat_})

		template = loader.get_template("admin/izin/pengajuanizin/view_pengajuan_siup.html")
		ec = RequestContext(request, extra_context)
		return HttpResponse(template.render(ec))

	def option_namaizin(self, request):	
		jenis_izin = request.POST.get('param', None)
		if jenis_izin:
			jenisizin_list = JenisIzin.objects.filter(jenis_izin=jenis_izin)
		else:
			jenisizin_list = JenisIzin.objects.none()
		pilihan = "<option></option>"
		response = {
			"count": 0,
			"data": pilihan+"".join(x.as_option() for x in jenisizin_list)
		}

		return HttpResponse(json.dumps(response))
		# return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in jenisizin_list)));

		# pilihan = """
		# <option value=1>SIUP</option>
		# <option>HO</option>
		# <option>SIPA</option>
		# <option>Izin Pertambangan</option>
		# <option>TDP</option>
		# """
		# return HttpResponse(mark_safe(pilihan));

	def option_kelompokjenisizin(self, request):
		kode_jenis_izin = request.POST.get('param', None)
		if kode_jenis_izin:
			kelompokjenisizin_list = KelompokJenisIzin.objects.filter(jenis_izin__kode=kode_jenis_izin)
		else:
			kelompokjenisizin_list = KelompokJenisIzin.objects.none()
		pilihan = "<option></option>"
		response = {
			"count": len(kelompokjenisizin_list),
			"data": pilihan+"".join(x.as_option() for x in kelompokjenisizin_list)
		}

		return HttpResponse(json.dumps(response))
		# return HttpResponse(mark_safe(pilihan+"".join(x.as_option() for x in kelompokjenisizin_list)));

		# pilihan = """
		# <option value=1>SIUP</option>
		# <option>HO</option>
		# <option>SIPA</option>
		# <option>Izin Pertambangan</option>
		# <option>TDP</option>
		# """
		# return HttpResponse(mark_safe(pilihan));
	
	def aksi_detil_siup(self, request):
		id_detil_siup = request.POST.get('id_detil_siup', None)
		try:
			obj = DetilSIUP.objects.get(id=id_detil_siup)
			if request.POST.get('aksi', None) and request.user.has_perm('izin.change_detilsiup') or request.user.is_superuser or request.user.groups.filter(name='Admin Sistem'):
				if request.POST.get('aksi') == '_submit_operator':
					obj.status = 4
					obj.save()
					response = {
						"success": True,
						"pesan": "Izin berhasih di verifikasi.",
						"redirect": '',
					}
				elif request.POST.get('aksi') == '_submit_kabid':
					obj.status = 5
					obj.save()
					response = {
						"success": True,
						"pesan": "Izin berhasih di verifikasi.",
						"redirect": '',
					}
				else:
					response = {
						"success": False,
						"pesan": "Anda tidak memiliki hak akses untuk memverifikasi izin.",
					}
			else:
				response = {
					"success": False,
					"pesan": "Anda tidak memiliki hak akses untuk memverifikasi izin.",
				}
		except ObjectDoesNotExist:
			response = {
					"success": False,
					"pesan": "Terjadi kesalahan, detil siup tidak ada dalam daftar.",
				}
		return HttpResponse(json.dumps(response))


	def get_urls(self):
		from django.conf.urls import patterns, url
		urls = super(IzinAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^wizard/add/$', self.admin_site.admin_view(add_wizard_siup), name='add_wizard_izin'),
			url(r'^option/izin/$', self.admin_site.admin_view(self.option_namaizin), name='option_namaizin'),
			url(r'^option/kelompokizin/$', self.admin_site.admin_view(self.option_kelompokjenisizin), name='option_kelompokjenisizin'),
			url(r'^wizard/add/proses/siup/$', self.admin_site.admin_view(formulir_siup), name='izin_proses_siup'),
			url(r'^pendaftaran/(?P<id_pengajuan_izin_>[0-9]+)/$', self.admin_site.admin_view(cetak), name='pendaftaran_selesai'),
			url(r'^pendaftaran/(?P<id_pengajuan_izin_>[0-9]+)/cetak$', self.admin_site.admin_view(self.print_out_pendaftaran), name='print_out_pendaftaran'),
			url(r'^view-pengajuan-siup/(?P<id_pengajuan_izin_>[0-9]+)$', self.admin_site.admin_view(self.view_pengajuan_siup), name='view_pengajuan_siup'),
			url(r'^aksi/$', self.admin_site.admin_view(self.aksi_detil_siup), name='aksi_detil_siup'),
			)
		return my_urls + urls

	def suit_cell_attributes(self, obj, column):
		if column in ['button_cetak_pendaftaran']:
			return {'class': 'text-center'}
		else:
			return None

	def save_model(self, request, obj, form, change):
		# clean the nomor_identitas
		obj.create_by = request.user
		obj.save()

admin.site.register(PengajuanIzin, IzinAdmin)
admin.site.register(DetilSIUP )