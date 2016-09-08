
STATUS = (
	(1, 'Active'),
	(2, 'Inactive'),
	(3, 'Blocked'),
	(4, 'Submitted'),
	(5, 'Archive'),
	(6, 'Draft'),
	(7, 'Rejected'),
)

# Status Data : 
# 1. Active: Data Transaksi
# 2. Inactive: Data diinputkan oleh staff dan perlu diverifikasi sama admin
# 3. Blocked: Data tidak dapat dipakai sampai admin mengubahnya ke status yg lain
# 4. Submitted: Sudah tidak dapat diubah sama sekali, untuk mengubahnya harus menggunakan surat resmi kepada admin
# 5. Archive: pemindahan data ke sistem archive
# 6. Draft: 
# 7. Rejected:

def get_status_color(obj):
	warna = ""
	if obj.status == 2:
		warna = ' warning'
	elif obj.status == 4:
		warna = ' danger'
	elif obj.status == 5:
		warna = ' success'
	elif obj.status == 6:
		warna = ' info'
	return warna

def api_val(data):
	if not data:
		return None
	if data == '':
		return None
	if data == 'None':
		return None
	return data

#Kurang Foto
def save_sync_siabjo(user, data):

	return True