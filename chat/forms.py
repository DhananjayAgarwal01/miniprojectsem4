from django import forms
from .models import Donation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['item_name', 'description', 'category', 'quantity', 'condition']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'] = forms.ImageField(required=False, widget=forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'}))
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': '', 'enctype': 'multipart/form-data'}
        self.helper.layout = Layout(
            Field('item_name', css_class='form-control'),
            Field('description', css_class='form-control'),
            Field('category', css_class='form-select'),
            Field('quantity', css_class='form-control'),
            Field('condition', css_class='form-select'),
            Field('image', css_class='form-control'),
            Submit('submit', 'Create Donation', css_class='btn btn-primary w-100')
        )
        
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('Image file too large. Size should not exceed 5 MB.')
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError('File type not supported. Please upload an image.')
        return image
        
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError('Quantity must be at least 1.')
        return quantity