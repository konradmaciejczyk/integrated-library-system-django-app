# Konrad Maciejczyk, 2021 -2022
from django import forms
from django.db.models.base import Model
from django.db.models.fields.files import ImageField
from django.forms import ModelForm
from django.forms.forms import DeclarativeFieldsMetaclass
from django.forms.widgets import ClearableFileInput
from accounts.models import Citizenship, Gender, IDType, Occupation, User
from worker_side.models import Author, Availability, Book, Condition, Publisher
from user_side.models import Client
from django.db import transaction
import string, random
import re

def get_borrows_limit(occupation, citizenship):
    """Auxillary function, that detreminates (basing on client's occupation and citizenship) 
    client's upper limit of items,that can be borrowed at the same time.

    Parameters:
    occupation: (string) id of record in Occupation table
    citizenship: (string) id of record in Citizenship table
    
    Returns:
    Int(2, 5, 10)
    """

    if citizenship == 164 and occupation in (1, 2): #polish student/academic teacher
        return 10
    elif citizenship != 164 and occupation in (1, 2): #foreign student
        return 5
    elif citizenship != 164 and occupation == 2: #foreign teacher
        return 10
    elif citizenship == 164 and occupation == 3: #person nor student or academic teacher
        return 5
    else: #foreign person nor student or academic teacher
        return 2

password_generator = lambda N: ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
password_generator.__doc__ = "A function, that generate random string of N values.\n\nParameters:\nN: (int) string length\n\nReturns:\nString"

def vaildate_users_form(data):
    """Function that validates registration form.

    Parameters:
    data: (dict) dictionary of values from form

    Returns:
    None (Asserts ValidationError when form is invalid)
    """

    try:#citizenship, occupation, gender, id_type
        assert(data['citizenship'] in range(1, 226) and data['id_type'] in range(1, 3) and data['gender'] in range(1, 4) and data['occupation'] in range(1, 4))
        #first_name, last_name
        assert(data['first_name'].isalpha() and data['last_name'].isalpha())
        #data_of_birth, id_number, corr_address
        assert(data['date_of_birth'] and len(data['id_number']) > 4 and len(data['corr_address']) > 9)
        #phone_number
        assert(re.match(r'\+[1-9]{1}[0-9]{7,14}$', data['phone_number']))  
    except:
        raise forms.ValidationError("Form filled with invalid values")


class ClientRegistrationForm(ModelForm):
    date_of_birth = forms.DateField(required=True)
    citizenship = forms.IntegerField(required=True)
    occupation = forms.IntegerField(required=True)
    corr_address = forms.CharField(required=True)
    gender = forms.IntegerField(required=True)
    id_type = forms.IntegerField(required=True)
    id_number = forms.CharField(required=True)


    class Meta():
        model = User
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'citizenship',
        'id_type', 'id_number', 'email', 'phone_number', 'corr_address', 'occupation']

    @transaction.atomic
    def save(self):
        vaildate_users_form(self.cleaned_data)
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email'].lower()
        user.phone_number = self.cleaned_data['phone_number']
        password=password_generator(8)
        user.set_password(password)
        user.save()

        client = user
        date_of_birth = self.cleaned_data['date_of_birth']

        citizenship = Citizenship.objects.get(id=self.cleaned_data["citizenship"])
        occupation = Occupation.objects.get(id=self.cleaned_data["occupation"])
        id_type = IDType.objects.get(id=self.cleaned_data["id_type"])
        gender = Gender.objects.get(id=self.cleaned_data["gender"])
        corr_address = self.cleaned_data['corr_address']
        id_number = self.cleaned_data["id_number"]

        Client.objects.create(user=client, borrows_max = get_borrows_limit(self.cleaned_data['occupation'], self.cleaned_data['citizenship']), date_of_birth = date_of_birth,
        citizenship = citizenship, occupation = occupation, corr_address = corr_address, id_type = id_type, id_number = id_number, gender = gender)
        
        return password

class AddBookForm(forms.Form):  
    isbn = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter ISBN', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter ISBN";', 'name': 'isbn', 'id': 'isbn', 'autocomplete': 'off'})
    )  
    author = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter author\'s name', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter author\'s name";', 'name': 'author', 'id': 'author', 'list': 'authors_list', 'autocomplete': 'off'})
    )
    title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter book\'s title', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter book\'s title";', 'name': 'title', 'id': 'title', 'autocomplete': 'off'})
    )
    full_title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter book\'s full title', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter book\'s full title";', 'name': 'full_title', 'id': 'full_title', 'autocomplete': 'off'})
    )
    pub_year = forms.IntegerField(required=False, widget=forms.NumberInput(
        attrs={'placeholder': 'Enter year of publication', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter year of publication";', 'name': 'pub_year', 'id': 'pub_year', 'autocomplete': 'off', 'min': '1'})
    )
    publisher = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter publisher\'s name', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter publisher\'s name";', 'name': 'publisher', 'id': 'publisher', 'autocomplete': 'off', 'list': 'publishers_list'})
    )

    description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': 'Enter book\'s description', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter book\'s description";', 'name': 'description', 'id': 'description', 'autocomplete': 'off'})
    )
    condition = forms.IntegerField(required=True, widget=forms.Select(
        attrs={'name': 'condition', 'id': 'condition', 'autocomplete': 'off'})
    )
    availability = forms.IntegerField(required=True, widget=forms.Select(
        attrs={'name': 'availability', 'id': 'availability', 'autocomplete': 'off'})
    )
    cover = forms.ImageField(required=False, widget=ClearableFileInput(
        attrs={'id': 'cover', 'name': 'cover', 'autocomplete': 'off'})
    )
    
    @transaction.atomic
    def save(self):
        isbn = self.cleaned_data["isbn"] 

        author = None
        try:
            author = Author.objects.get(name=self.cleaned_data['author'])
        except:
            author = Author.objects.create(name=self.cleaned_data['author'])

        title = self.cleaned_data['title']
        full_title = self.cleaned_data['full_title']
        pub_year = self.cleaned_data['pub_year']

        publisher = None
        try:
            publisher = Publisher.objects.get(name=self.cleaned_data['publisher']) 
        except:
            publisher = Publisher.objects.create(name=self.cleaned_data['publisher'])


        description = self.cleaned_data['description']
        condition = Condition.objects.get(id=self.cleaned_data['condition'])
        availability = Availability.objects.get(id=self.cleaned_data['availability'])
        cover = self.cleaned_data['cover']

        Book.objects.create(isbn=isbn, author=author, title=title, full_title=full_title, pub_year=pub_year, publisher=publisher, description=description,
        condition=condition, availability=availability, cover=cover)


        return True