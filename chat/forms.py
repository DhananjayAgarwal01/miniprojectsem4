from django import forms
from .models import Donation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['item_name', 'description', 'category', 'quantity', 'condition', 'image_path']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Field('item_name', css_class='form-control'),
            Field('description', css_class='form-control'),
            Field('category', css_class='form-select'),
            Field('quantity', css_class='form-control'),
            Field('condition', css_class='form-select'),
            Field('image_path', css_class='form-control'),
            Submit('submit', 'Create Donation', css_class='btn btn-primary w-100')
        ) 