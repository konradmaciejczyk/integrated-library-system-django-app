from django import forms
# Konrad Maciejczyk, 2021-2022
from django import forms

from worker_side.models import Author

class SearchForm(forms.Form):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'name': 'title'
    }))

    author = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'name': 'author'
    }))

    book = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'name':'book',
    }))

    movie = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'name':'movie',
    }))

    sr = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'name':'sr',
    }))

    not_available = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'name':'n_a',
    }))




