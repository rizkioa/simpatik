

def get_title_verifikasi(request, pengajuan_obj, skizin_obj):
	title_verifikasi = ""
	if request.user.groups.filter(name="Operator"):
		if pengajuan_obj.status == 11 or pengajuan_obj.status == 6 or pengajuan_obj.status == 4:
			title_verifikasi = "Validasi Persyaratan"
	if request.user.groups.filter(name="Kabid"):
		if pengajuan_obj.status == 2 and skizin_obj.status == 6  or skizin_obj.status == 4:
			title_verifikasi = "Verifikasi Draf Izin Kabid"
		elif pengajuan_obj.status == 4:
			title_verifikasi = "Verifikasi Kabid Pelayanan Perizinan"
	if request.user.groups.filter(name="Pembuat Surat"):
		if skizin_obj == None and pengajuan_obj.status == 2:
			title_verifikasi = "Pembuatan Draft SKIzin"
	if request.user.groups.filter(name="Kadin"):
		if pengajuan_obj.status == 2 and skizin_obj.status == 4 or skizin_obj.status == 9:
			title_verifikasi = "Verifikasi Draf Izin Kadin"
	if request.user.groups.filter(name="Penomoran"):
		if pengajuan_obj.status == 2 and skizin_obj.status == 9 or skizin_obj.status == 10:
			title_verifikasi = "Registrasi Izin (Penomoran Izin)"
	if request.user.groups.filter(name="Cetak"):
		if pengajuan_obj.status == 2 and skizin_obj.status == 10 or skizin_obj.status == 2:
			title_verifikasi = "Cetak Izin"
	if request.user.groups.filter(name="Selesai"):
		if pengajuan_obj.status == 2 and skizin_obj.status == 2:
			title_verifikasi = "Stample SK Izin"
	return title_verifikasi