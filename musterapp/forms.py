from django import forms
from .models import Pattern

class VectorForm(forms.Form):
    vectorfile = forms.FileField(
        label='Select the vectorized pattern',
        help_text='only .svg is supported'
    )

class TagForm(forms.ModelForm):
    class Meta:
        model = Pattern
        fields = ["tags"]
