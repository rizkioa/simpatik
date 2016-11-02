
STATUS = (
	(1, 'Active'),
	(2, 'Inactive'),
	(3, 'Blocked'),
	(4, 'Submitted'),
	(5, 'Archive'),
	(6, 'Draft'),
	(7, 'Rejected'),
	(8, 'Survey'),
	(9, 'Verified'),
	(10, 'Regitered'),
	(11, 'Insert'),
)

# Status Data : 
# 1. Active: Ketika izin selesai
# 2. Inactive: Kalo tidak ada survey kabid mengubah status dari Submitted ke Inactive
# 3. Blocked: 
# 4. Submitted: Operator mengubah Draft ke Submitted
# 5. Archive: 
# 6. Draft: default
# 7. Rejected:
# 8. Survey: Dan jika ada survey mengubah status Submitted ke Survey dan jika Survey selesai kabid merubah status menjadi Inactive
# 9. Verified:
# 10. Regitered:
# 
# Status Data surat:
# 1. Surat dibuat default status Draft
# 2. kabid merubah status Draft ke Submitted
# 3. 

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