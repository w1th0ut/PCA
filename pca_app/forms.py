from django import forms
from .models import UploadImage

class ImageUploadForm(forms.ModelForm):
    k_value = forms.IntegerField(min_value=1, max_value=100, label='K value')

    class Meta:
        model = UploadImage
        fields = ('image', 'k_value')
