from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import NomorIdentitasPengguna

from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon, JenisReklame
from perusahaan.models import BentukKegiatanUsaha, JenisPenanamanModal, Kelembagaan, KBLI, JenisLegalitas
from izin.models import PengajuanIzin, JenisPermohonanIzin, KelompokJenisIzin, Pemohon, DetilReklame

def formulir_reklame(request):
	extra_context={}
	if 'id_kelompok_izin' in request.COOKIES.keys():
		extra_context.update({'title': 'Reklame Baru'})
		negara = Negara.objects.all()
		kecamatan = Kecamatan.objects.filter(kabupaten_id=1083)
		jenis_pemohon = JenisPemohon.objects.all()
		bentuk_kegiatan_usaha_list = BentukKegiatanUsaha.objects.all()
		jenis_penanaman_modal_list = JenisPenanamanModal.objects.all()
		kelembagaan_list = Kelembagaan.objects.all()
		kbli_list = KBLI.objects.all()
		# produk_utama_list = ProdukUtama.objects.all()
		jenis_legalitas_list = JenisLegalitas.objects.all()
		reklame_jenis_list = JenisReklame.objects.all()

		jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=request.COOKIES['id_kelompok_izin']) # Untuk SIUP
		extra_context.update({'negara': negara})
		extra_context.update({'kecamatan': kecamatan})
		extra_context.update({'jenis_pemohon': jenis_pemohon})
		# print request.COOKIES
		extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})
		extra_context.update({'bentuk_kegiatan_usaha_list': bentuk_kegiatan_usaha_list})
		extra_context.update({'jenis_penanaman_modal_list': jenis_penanaman_modal_list})
		extra_context.update({'kelembagaan_list': kelembagaan_list})
		extra_context.update({'kbli_list': kbli_list})
		# extra_context.update({'produk_utama_list': produk_utama_list})
		extra_context.update({'jenis_legalitas_list': jenis_legalitas_list})
		extra_context.update({'reklame_jenis_list': reklame_jenis_list})
		# +++++++++++++++++++ jika cookie pengajuan ada dan di refrash +++++++++++++++++
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan'] != "":
				try:
					pengajuan_ = DetilReklame.objects.get(id=request.COOKIES['id_pengajuan'])
					alamat_ = ""
					alamat_perusahaan_ = ""
					if pengajuan_.pemohon:
						if pengajuan_.pemohon.desa:
							alamat_ = str(pengajuan_.pemohon.alamat)+", "+str(pengajuan_.pemohon.desa)+", Kec. "+str(pengajuan_.pemohon.desa.kecamatan)+", "+str(pengajuan_.pemohon.desa.kecamatan.kabupaten)
							extra_context.update({ 'alamat_pemohon_konfirmasi': alamat_ })
						extra_context.update({ 'pemohon_konfirmasi': pengajuan_.pemohon })
						extra_context.update({'cookie_file_foto': pengajuan_.pemohon.berkas_foto.all().last()})
						ktp_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=1).last()
						extra_context.update({ 'ktp': ktp_ })
						paspor_ = NomorIdentitasPengguna.objects.filter(user_id=pengajuan_.pemohon.id, jenis_identitas_id=2).last()
						extra_context.update({ 'paspor': paspor_ })
						extra_context.update({'cookie_file_ktp': ktp_.berkas })
					if pengajuan_.perusahaan:
						if pengajuan_.perusahaan.desa:
							alamat_perusahaan_ = str(pengajuan_.perusahaan.alamat_perusahaan)+", "+str(pengajuan_.perusahaan.desa)+", Kec. "+str(pengajuan_.perusahaan.desa.kecamatan)+", "+str(pengajuan_.perusahaan.desa.kecamatan.kabupaten)
							extra_context.update({ 'alamat_perusahaan_konfirmasi': alamat_perusahaan_ })
						extra_context.update({ 'perusahaan_konfirmasi': pengajuan_.perusahaan })
					
					extra_context.update({ 'no_pengajuan_konfirmasi': pengajuan_.no_pengajuan })
					extra_context.update({ 'jenis_permohonan_konfirmasi': pengajuan_.jenis_permohonan })
					extra_context.update({ 'pengajuan_': pengajuan_ })
					panjang = str(int(pengajuan_.panjang))
					lebar = str(int(pengajuan_.lebar))
					sisi = str(int(pengajuan_.sisi))
					ukuran_ = panjang+"x"+lebar+"x"+sisi
					extra_context.update({ 'panjang': panjang })
					extra_context.update({ 'lebar': lebar })
					extra_context.update({ 'sisi': sisi })
					extra_context.update({ 'ukuran': ukuran_ })

					if pengajuan_.tanggal_mulai:
						awal = pengajuan_.tanggal_mulai
					else:
						awal = 0
					if pengajuan_.tanggal_akhir:
						akhir = pengajuan_.tanggal_akhir
					else:
						akhir = 0
					
					selisih = akhir-awal
					if selisih != 0:
						extra_context.update({ 'selisih': selisih.days })
					else:
						extra_context.update({ 'selisih': selisih })
					
					if pengajuan_.desa:
						letak_ = pengajuan_.letak_pemasangan + ", Desa "+str(pengajuan_.desa) + ", Kec. "+str(pengajuan_.desa.kecamatan)+", "+ str(pengajuan_.desa.kecamatan.kabupaten)
					else:
						letak_ = ""
					berkas_1 = pengajuan_.berkas_tambahan.filter(keterangan="Gambar Kontruksi Pemasangan Reklame").last()
					extra_context.update({ 'berkas_1': berkas_1 })
					berkas_2 = pengajuan_.berkas_tambahan.filter(keterangan="Gambar Foto Lokasi Pemasangan Reklame").last()
					extra_context.update({ 'berkas_2': berkas_2 })
					berkas_3 = pengajuan_.berkas_tambahan.filter(keterangan="Gambar Denah Lokasi Pemasangan Rekalame").last()
					extra_context.update({ 'berkas_3': berkas_3 })
					berkas_4 = pengajuan_.berkas_tambahan.filter(keterangan="Surat Ketetapan Pajak Daerah (SKPD)").last()
					extra_context.update({ 'berkas_4': berkas_4 })
					berkas_5 = pengajuan_.berkas_tambahan.filter(keterangan="Surat Setoran Pajak Daerah (SSPD)").last()
					extra_context.update({ 'berkas_5': berkas_5 })
					berkas_6 = pengajuan_.berkas_tambahan.filter(keterangan="Rekomendasi dari Kantor SATPOL PP").last()
					extra_context.update({ 'berkas_6': berkas_6 })
					berkas_7 = pengajuan_.berkas_tambahan.filter(keterangan="Berita Acara Perusahaan(BAP) Tim Perizinan").last()
					extra_context.update({ 'berkas_7': berkas_7 })
					berkas_8 = pengajuan_.berkas_tambahan.filter(keterangan="Surat Perjanjian Kesepakatan").last()
					extra_context.update({ 'berkas_8': berkas_8 })
					berkas_9 = pengajuan_.berkas_tambahan.filter(keterangan="Berkas Tambahan").last()
					extra_context.update({ 'berkas_9': berkas_9 })

					extra_context.update({ 'letak': letak_ })
				except ObjectDoesNotExist:
					pass
		template = loader.get_template("admin/izin/izin/form_wizard_reklame.html")
		ec = RequestContext(request, extra_context)
		response = HttpResponse(template.render(ec))
		if 'id_pengajuan' in request.COOKIES.keys():
			if request.COOKIES['id_pengajuan'] != "0":
				if pengajuan_.pemohon:
					response.set_cookie(key='id_pemohon', value=pengajuan_.pemohon.id)
				if pengajuan_.perusahaan:
					response.set_cookie(key='id_perusahaan', value=pengajuan_.perusahaan.id)
				if ktp_:
					response.set_cookie(key='nomor_ktp', value=ktp_)
		return response
	else:
		messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
		return HttpResponseRedirect(reverse('admin:add_wizard_izin'))