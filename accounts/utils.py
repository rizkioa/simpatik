
STATUS = (
	(1, 'Active'),
	(2, 'Inactive'),
	(3, 'Blocked'),
	(4, 'Submitted'),
	(5, 'Archive'),
)

# Status Data : 
# 1. Active: Data Transaksi
# 2. Inactive: Data diinputkan oleh staff dan perlu diverifikasi sama admin
# 3. Blocked: Data tidak dapat dipakai sampai admin mengubahnya ke status yg lain
# 4. Submitted: Sudah tidak dapat diubah sama sekali, untuk mengubahnya harus menggunakan surat resmi kepada admin
# 5. Archive: pemindahan data ke sistem archive

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