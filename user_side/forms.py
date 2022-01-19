# Konrad Maciejczyk, 2021-2022
from django import forms
from django import forms
from accounts.models import User
from user_side.models import Client

class SearchForm(forms.Form):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={
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

    on_site = forms.ChoiceField(required=False, choices=(('5', '5'), ('10', '10'), ('25', '25')), label="Items on list", widget=forms.Select(attrs={
        'name': 'on_site'
    }))

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone_number']

class UpdateClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['corr_address']




