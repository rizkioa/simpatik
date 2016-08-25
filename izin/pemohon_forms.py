from django import forms
from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa
from izin.models import Pemohon
from django.core.urlresolvers import reverse

class PemohonForm(forms.ModelForm):
	negara = forms.ModelChoiceField(label="Negara", queryset=Negara.objects.all(),)
	provinsi = forms.ModelChoiceField(label="Provinsi", help_text="Pilih Negara dulu.", queryset=Provinsi.objects.none(), widget=forms.Select(attrs={'disabled': 'disabled'}))
	kabupaten = forms.ModelChoiceField(label="Kabupaten / Kota", help_text="Pilih Provinsi dulu.", queryset=Kabupaten.objects.none(), widget=forms.Select(attrs={'disabled': 'disabled'}))
	kecamatan = forms.ModelChoiceField(label="Kecamatan", help_text="Pilih Kabupaten / Kota dulu.", queryset=Kecamatan.objects.none(), widget=forms.Select(attrs={'disabled': 'disabled'}))
	desa = forms.ModelChoiceField(label="Desa / Kelurahan", help_text="Pilih Kecamatan dulu.", queryset=Desa.objects.none(), widget=forms.Select(attrs={'disabled': 'disabled'}))

	def __init__(self, *args, **kwargs):
		super(PemohonForm, self).__init__(*args, **kwargs)

		if self.request.user.has_perm('master.add_negara') or self.request.user.has_perm('master.change_negara'):
			self.fields['negara'].help_text = {}
			if self.request.user.has_perm('master.add_negara'):
				self.fields['negara'].help_text.update({'add_code': '<a id="add_id_negara" class="related-widget-wrapper-link add-related" href="'+reverse('admin:master_negara_add')+'?_to_field=id&_popup=1"><img width="10" height="10" alt="Tambah" src="/static/admin/img/icon_addlink.gif"></a>'})
			if self.request.user.has_perm('master.change_negara'):
				self.fields['negara'].help_text.update({'change_code': '<a id="change_id_negara" class="related-widget-wrapper-link change-related" title="Change selected Negara" data-href-template="/admin/master/negara/__fk__/?_to_field=id&_popup=1"><img width="10" height="10" alt="Ubah" src="/static/admin/img/icon_changelink.gif"></a>'})
				
		if self.request.user.has_perm('master.add_provinsi') or self.request.user.has_perm('master.change_provinsi'):
			self.fields['provinsi'].help_text = {}
			if self.request.user.has_perm('master.add_provinsi'):
				self.fields['provinsi'].help_text.update({'add_code': '<a id="add_id_provinsi" class="related-widget-wrapper-link add-related" href="'+reverse('admin:master_provinsi_add')+'?_to_field=id&_popup=1"><img width="10" height="10" alt="Tambah" src="/static/admin/img/icon_addlink.gif"></a>'})
			if self.request.user.has_perm('master.change_provinsi'):
				self.fields['provinsi'].help_text.update({'change_code': '<a id="change_id_provinsi" class="related-widget-wrapper-link change-related" title="Change selected Provinsi" data-href-template="/admin/master/provinsi/__fk__/?_to_field=id&_popup=1"><img width="10" height="10" alt="Ubah" src="/static/admin/img/icon_changelink.gif"></a>'})

		if self.request.user.has_perm('master.add_kabupaten') or self.request.user.has_perm('master.change_kabupaten'):
			self.fields['kabupaten'].help_text = {}
			if self.request.user.has_perm('master.add_kabupaten'):
				self.fields['kabupaten'].help_text.update({'add_code': '<a id="add_id_kabupaten" class="related-widget-wrapper-link add-related" href="'+reverse('admin:master_kabupaten_add')+'?_to_field=id&_popup=1"><img width="10" height="10" alt="Tambah" src="/static/admin/img/icon_addlink.gif"></a>'})
			if self.request.user.has_perm('master.change_kabupaten'):
				self.fields['kabupaten'].help_text.update({'change_code': '<a id="change_id_kabupaten" class="related-widget-wrapper-link change-related" title="Change selected Kabupaten" data-href-template="/admin/master/kabupaten/__fk__/?_to_field=id&_popup=1"><img width="10" height="10" alt="Ubah" src="/static/admin/img/icon_changelink.gif"></a>'})

		if self.request.user.has_perm('master.add_kecamatan') or self.request.user.has_perm('master.change_kecamatan'):
			self.fields['kecamatan'].help_text = {}
			if self.request.user.has_perm('master.add_kecamatan'):
				self.fields['kecamatan'].help_text.update({'add_code': '<a id="add_id_kecamatan" class="related-widget-wrapper-link add-related" href="'+reverse('admin:master_kecamatan_add')+'?_to_field=id&_popup=1"><img width="10" height="10" alt="Tambah" src="/static/admin/img/icon_addlink.gif"></a>'})
			if self.request.user.has_perm('master.change_kecamatan'):
				self.fields['kecamatan'].help_text.update({'change_code': '<a id="change_id_kecamatan" class="related-widget-wrapper-link change-related" title="Change selected Kecamatan" data-href-template="/admin/master/kecamatan/__fk__/?_to_field=id&_popup=1"><img width="10" height="10" alt="Ubah" src="/static/admin/img/icon_changelink.gif"></a>'})

		if self.request.user.has_perm('master.add_desa') or self.request.user.has_perm('master.change_desa'):
			self.fields['desa'].help_text = {}
			if self.request.user.has_perm('master.add_desa'):
				self.fields['desa'].help_text.update({'add_code': '<a id="add_id_desa" class="related-widget-wrapper-link add-related" href="'+reverse('admin:master_desa_add')+'?_to_field=id&_popup=1"><img width="10" height="10" alt="Tambah" src="/static/admin/img/icon_addlink.gif"></a>'})
			if self.request.user.has_perm('master.change_desa'):
				self.fields['desa'].help_text.update({'change_code': '<a id="change_id_desa" class="related-widget-wrapper-link change-related" title="Change selected Desa" data-href-template="/admin/master/desa/__fk__/?_to_field=id&_popup=1"><img width="10" height="10" alt="Ubah" src="/static/admin/img/icon_changelink.gif"></a>'})

		negara = self.request.POST.get('negara', None)
		if negara:
			self.fields['provinsi'].widget = forms.Select()
			self.fields['provinsi'].queryset = Provinsi.objects.filter(negara__id=negara)
			provinsi = self.request.POST.get('provinsi', None)
			if provinsi:
				self.fields['provinsi'].initial = provinsi
				self.fields['kabupaten'].widget = forms.Select()
				self.fields['kabupaten'].queryset = Kabupaten.objects.filter(provinsi__id=provinsi)
				kabupaten = self.request.POST.get('kabupaten', None)
				if kabupaten:
					self.fields['kabupaten'].initial = kabupaten
					self.fields['kecamatan'].widget = forms.Select()
					self.fields['kecamatan'].queryset = Kecamatan.objects.filter(kabupaten__id=kabupaten)
					kecamatan = self.request.POST.get('kecamatan', None)
					if kecamatan:
						self.fields['kecamatan'].initial = kecamatan
						self.fields['desa'].widget = forms.Select()
						self.fields['desa'].queryset = Desa.objects.filter(kecamatan__id=kecamatan)
						desa = self.request.POST.get('desa', None)
						if desa:
							self.fields['desa'].initial = desa

		if self.instance.pk and self.instance.desa:
			self.fields['negara'].initial = self.instance.desa.kecamatan.kabupaten.provinsi.negara
			self.fields['provinsi'].queryset = Provinsi.objects.filter(negara__id=self.instance.desa.kecamatan.kabupaten.provinsi.negara.id)
			self.fields['provinsi'].widget.attrs = {}
			self.fields['provinsi'].initial = self.instance.desa.kecamatan.kabupaten.provinsi

			self.fields['kabupaten'].queryset = Kabupaten.objects.filter(provinsi__id=self.instance.desa.kecamatan.kabupaten.provinsi.id)
			self.fields['kabupaten'].widget.attrs = {}
			self.fields['kabupaten'].initial = self.instance.desa.kecamatan.kabupaten

			self.fields['kecamatan'].queryset = Kecamatan.objects.filter(kabupaten__id=self.instance.desa.kecamatan.kabupaten.id)
			self.fields['kecamatan'].widget.attrs = {}
			self.fields['kecamatan'].initial = self.instance.desa.kecamatan

			self.fields['desa'].queryset = Desa.objects.filter(kecamatan__id=self.instance.desa.kecamatan.id)
			self.fields['desa'].widget.attrs = {}
			self.fields['desa'].initial = self.instance.desa
	
	class Meta:
		model = Pemohon
		fields = '__all__'

	def clean_email(self):
		return self.cleaned_data['email'] or None