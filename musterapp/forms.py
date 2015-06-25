from django import forms

class VectorForm(forms.Form):
    vectorfile = forms.FileField(
        label='Select the vectorized pattern',
        help_text='only .svg is supported'
    )
