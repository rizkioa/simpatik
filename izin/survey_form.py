from django import forms
from ckeditor.widgets import CKEditorWidget

from pembangunan.models import Rekomendasi, DetilBAP
from master.models import Berkas

class RekomendasiForm(forms.ModelForm):
	rekomendasi = forms.CharField(widget=CKEditorWidget())

	class Meta:
		model = Rekomendasi
		fields = ('rekomendasi',)

class DetilForm(forms.ModelForm):
	"""docstring for DetilForm"""
	class Meta:
		model = DetilBAP
		# fields = '__all__'
		exclude = ['keterangan','survey_iujk', 'status', 'created_at', 'updated_at', 'created_by', 'rejected_by','verified_by']

class BerkasForm(forms.ModelForm):
	"""docstring for DetilForm"""
	class Meta:
		model = Berkas
		fields = ('berkas',)
		