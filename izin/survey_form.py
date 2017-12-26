from django import forms
from ckeditor.widgets import CKEditorWidget

from pembangunan.models import Rekomendasi, DetilBAP, BAPReklameHO
from master.models import Berkas

class RekomendasiForm(forms.ModelForm):
	rekomendasi = forms.CharField(widget=CKEditorWidget())

	class Meta:
		model = Rekomendasi
		fields = ('rekomendasi',)


class BerkasForm(forms.ModelForm):
	"""docstring for DetilForm"""
	class Meta:
		model = Berkas
		fields = ('berkas',)

class DetilForm(forms.ModelForm):
	"""docstring for DetilForm"""
	class Meta:
		model = DetilBAP
		# fields = '__all__'
		exclude = ['keterangan','survey_iujk', 'status', 'created_at', 'updated_at', 'created_by', 'rejected_by','verified_by']

class BAPReklameHOForm(forms.ModelForm):
	"""docstring for ClassName"""

	# sebelah_barat = forms.CharField()
	# sebelah_timur = forms.CharField()

	def __init__(self, *args, **kwargs):
		super(BAPReklameHOForm, self).__init__(*args, **kwargs)
		# self.fields['sebelah_barat'].required = True 

		# for key in self.fields:
		# 	self.fields[key].required = False 
	class Meta:
		model = BAPReklameHO
		# fields = '__all__'
		exclude = ['keterangan','survey', 'status', 'created_at', 'updated_at', 'created_by', 'rejected_by','verified_by']
		