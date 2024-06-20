# storage/forms.py
from django import forms
from .models import ModelWithFileField

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = ModelWithFileField
        fields = [
            'file_field',
            ]
