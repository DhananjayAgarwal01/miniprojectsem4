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
            'image_path': forms.FileInput(attrs={'accept': 'image/*'})
        }
        
    def clean_image_path(self):
        image = self.cleaned_data.get('image_path')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('Image file too large. Size should not exceed 5 MB.')
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError('File type not supported. Please upload an image file.')
        return image
        
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError('Quantity must be at least 1.')
        return quantity

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