# Konrad Maciejczyk, 2021 -2022
from django import forms
from django.forms import ModelForm
from django.forms.widgets import ClearableFileInput
from accounts.models import Citizenship, IDType, Occupation, User
from worker_side.models import Author, Availability, Book, Condition, Director, Publisher, Movie, Screenwriter, SoundRecording
from user_side.models import Client
from django.db import transaction
import string, random
import re

def get_borrows_limit(occupation):
    """Auxillary function, that detreminates (basing on client's occupation) 
    client's upper limit of items,that can be borrowed at the same time.

    Parameters:
    occupation: (string) id of record in Occupation table
    citizenship: (string) id of record in Citizenship table
    
    Returns:
    Int(2, 5, 10)
    """

    if occupation in (1, 2): #student/academic teacher
        return 10
    elif occupation == 3: #person nor student or academic teacher
        return 5

password_generator = lambda N: ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
password_generator.__doc__ = "A function, that generate random string of N values.\n\nParameters:\nN: (int) string length\n\nReturns:\nString"

def vaildate_users_form(data):
    """Function that validates registration form.

    Parameters:
    data: (dict) dictionary of values from form

    Returns:
    None (Asserts ValidationError when form is invalid)
    """

    try:#citizenship, occupation, id_type
        assert(data['citizenship'] in range(1, 226) and data['id_type'] in range(1, 3) and data['occupation'] in range(1, 4))
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
    id_type = forms.IntegerField(required=True)
    id_number = forms.CharField(required=True)


    class Meta():
        model = User
        fields = ['first_name', 'last_name', 'date_of_birth', 'citizenship',
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
        corr_address = self.cleaned_data['corr_address']
        id_number = self.cleaned_data["id_number"]

        client = Client.objects.create(user=client, borrows_max = get_borrows_limit(self.cleaned_data['occupation']), date_of_birth = date_of_birth,
        citizenship = citizenship, occupation = occupation, corr_address = corr_address, id_type = id_type, id_number = id_number)
        
        data_to_summary = {
            'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'phone_number': user.phone_number, 'password': password, 'date_of_birth': client.date_of_birth, 'occupation': client.occupation.name, 'corr_address': client.corr_address, 'id_type':client.id_type.name, 'id_number': client.id_number, 'citizenship': client.citizenship.name, 'borrows_max': client.borrows_max, 'registration_date': client.registration_date
        }


        return data_to_summary

class AddBookForm(forms.Form):  
    isbn = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter ISBN', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter ISBN";', 'name': 'isbn', 'id': 'isbn', 'autocomplete': 'off', 'autofocus': 'on'})
    )  
    author = forms.CharField(required=False, widget=forms.TextInput(
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
        new_item, new_publisher = False, False
        book = Book()

        book.isbn = self.cleaned_data["isbn"]

        book.title = self.cleaned_data['title']
        book.full_title = self.cleaned_data['full_title']
        book.pub_year = self.cleaned_data['pub_year']

        publisher = None
        try:
            publisher = Publisher.objects.get(name=self.cleaned_data['publisher']) 
        except:
            if self.cleaned_data['publisher'] != "":
                new_publisher = self.cleaned_data['publisher']
                publisher = Publisher.objects.create(name=self.cleaned_data['publisher'])
            else:
                publisher = None

        book.publisher = publisher
        book.description = self.cleaned_data['description']
        book.condition = Condition.objects.get(id=self.cleaned_data['condition'])
        book.availability = Availability.objects.get(id=self.cleaned_data['availability'])

        cover = self.cleaned_data['cover'] 
        if(cover != None):
            book.cover = cover
        
        book.save()

        authors = self.cleaned_data['author'].split(',') 
        new_authors = []

        for author in authors:
            try:
                author = Author.objects.filter(name=author)[0]
                book.author.add(author)
            except:
                if author != "":
                    new_authors.append(author)
                    author = Author.objects.create(name=author)
                    book.author.add(author)
                else:
                    author = None  

        new_item = True
        authors = ", ".join([author.name for author in book.author.all()])
        data_to_summary = {
          'item_info': {
                'type': 'book', 'id': book.id, 'title': book.title, 'author': authors if authors is not "" else "author(s) unknown", 'full_title': book.full_title, 'publisher': book.publisher if book.publisher else "publisher unknown", 'pub_year': book.pub_year if book.pub_year else "publication year unknow", 'isbn': book.isbn, 'description': book.description, 'condition': book.condition.name, 'availability': book.availability, 'cover': book.cover
          },
          'operations':{
              'new_item': new_item,
              'new_authors': new_authors,
              'new_publisher': new_publisher
          }
        }
        return data_to_summary

class AddMovieForm(forms.Form): 
    director = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter director\'s name', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter author\'s name";', 'name': 'author', 'id': 'author', 'list': 'authors_list', 'autocomplete': 'off', 'autofocus': 'on'})
    )
    screenwriter = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter screenwriter\'s name', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter screenwriter\'s name";', 'name': 'screenwriter', 'id': 'screenwriter', 'list': 'screenwriters_list', 'autocomplete': 'off'})
    )
    title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter movie\'s/film\'s title', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter movie\'s/film\'s title";', 'name': 'title', 'id': 'title', 'autocomplete': 'off'})
    )
    full_title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter movie\'s/film\'s full title', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter movie\'s/film\'s full title";', 'name': 'full_title', 'id': 'full_title', 'autocomplete': 'off'})
    )
    pub_year = forms.IntegerField(required=False, widget=forms.NumberInput(
        attrs={'placeholder': 'Enter year of release', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter year of release";', 'name': 'pub_year', 'id': 'pub_year', 'autocomplete': 'off', 'min': '1'})
    )
    description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': 'Enter movie\'s/film\'s description', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter movie\'s/film\'s description";', 'name': 'description', 'id': 'description', 'autocomplete': 'off'})
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
        new_directors, new_screenwriters = [], []

        movie = Movie()
        movie.title = self.cleaned_data['title']
        movie.full_title = self.cleaned_data['full_title']
        movie.pub_year = self.cleaned_data['pub_year']
        movie.description = self.cleaned_data['description']
        movie.condition = Condition.objects.get(id=self.cleaned_data['condition'])
        movie.availability = Availability.objects.get(id=self.cleaned_data['availability'])

        cover = self.cleaned_data['cover'] 
        if(cover != None):
            movie.cover = cover

        movie.save()

        directors = self.cleaned_data['director'].split(",")
        for director in directors:
            try:
                director = Director.objects.filter(name=director)[0]
                movie.director.add(director)
            except:
                if director != "":
                    new_directors.append(director)
                    director = Director.objects.create(name=director)
                    movie.director.add(director)
                else:
                    director = None

        screenwriters = self.cleaned_data['screenwriter'].split(",")
        for screenwriter in screenwriters:
            try:
                screenwriter = Screenwriter.objects.filter(name=screenwriter)[0]
                movie.screenwriter.add(screenwriter)
            except:
                if screenwriter != "":
                    new_screenwriters.append(screenwriter)
                    screenwriter = Screenwriter.objects.create(name=screenwriter)
                    movie.screenwriter.add(screenwriter)
                else:
                    screenwriter = None
                    
        new_item = True

        director = ", ".join([director.name for director in movie.director.all()])
        screenwriter = ", ".join([screenwriter.name for screenwriter in movie.screenwriter.all()])
        data_to_summary = {
          'item_info': {
                'type': 'movie', 'id': movie.id, 'title': movie.title, 'director': director if director else "director(s) unknown", 'screenwriter': screenwriter if screenwriter else "screenwriter(s) unknown", 'full_title': movie.full_title, 'release_year': movie.pub_year if movie.pub_year else "release year unknown", 'description': movie.description, 'condition': movie.condition.name, 'availability': movie.availability, 'cover': movie.cover
          },
          'operations':{
              'new_item': new_item,
              'new_directors': new_directors,
              'new_screenwriters': new_screenwriters,
          }
        }
        return data_to_summary

class AddSoundRecordingForm(forms.Form): 
    title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter title', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter title";', 'name': 'title', 'id': 'title', 'autocomplete': 'off', 'autofocus': 'on'})
    )

    author = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter author\'s name', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter author\'s name";', 'name': 'author', 'id': 'author', 'list': 'authors_list', 'autocomplete': 'off'})
    )

    full_title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter full title', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter full title";', 'name': 'full_title', 'id': 'full_title', 'autocomplete': 'off'})
    )

    cast = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter information about cast', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter information about cast";', 'name': 'cast', 'id': 'cast', 'autocomplete': 'off'})
    )

    pub_year = forms.IntegerField(required=False, widget=forms.NumberInput(
        attrs={'placeholder': 'Enter year of release', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter year of release";', 'name': 'pub_year', 'id': 'pub_year', 'autocomplete': 'off', 'min': '1'})
    )
    publisher = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter publisher\'s name', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter publisher\'s name";', 'name': 'publisher', 'id': 'publisher', 'autocomplete': 'off', 'list': 'publishers_list'})
    )
    description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': 'Enter description', 'onfocus': 'this.placeholder="";', 'onblur':'this.placeholder = "Enter description";', 'name': 'description', 'id': 'description', 'autocomplete': 'off'})
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
        new_item, new_publisher, new_authors = False, [], []

        sound_recording = SoundRecording()

        sound_recording.title = self.cleaned_data['title']
        sound_recording.full_title = self.cleaned_data['full_title']
        sound_recording.pub_year = self.cleaned_data['pub_year']
        sound_recording.cast = self.cleaned_data['cast']
        sound_recording.description = self.cleaned_data['description']
        sound_recording.condition = Condition.objects.get(id=self.cleaned_data['condition'])
        sound_recording.availability = Availability.objects.get(id=self.cleaned_data['availability'])

        cover = self.cleaned_data['cover']

        if(cover != None):
            sound_recording.cover = self.cleaned_data['cover'] 

        
        publisher = None
        try:
            publisher = Publisher.objects.get(name=self.cleaned_data['publisher']) 
        except:
            if self.cleaned_data['publisher'] != "":
                new_publisher = self.cleaned_data['publisher']
                publisher = Publisher.objects.create(name=self.cleaned_data['publisher'])
            else:
                publisher = None

        sound_recording.publisher = publisher

        sound_recording.description = self.cleaned_data['description']
        sound_recording.condition = Condition.objects.get(id=self.cleaned_data['condition'])
        sound_recording.availability = Availability.objects.get(id=self.cleaned_data['availability'])

        sound_recording.save()
        authors = self.cleaned_data['author'].split(',') 
        for author in authors:
            try:
                author = Author.objects.filter(name=author)[0]
                sound_recording.author.add(author)
            except:
                if author != "":
                    new_authors.append(author)
                    author = Author.objects.create(name=author)
                    sound_recording.author.add(author)
                else:
                    author = None
           
        new_item = True

        authors = ", ".join([author.name for author in sound_recording.author.all()])

        data_to_summary = {
          'item_info': {
                'type': 'sound recording', 'id': sound_recording.id, 'title': sound_recording.title, 'cast': sound_recording.cast if sound_recording.cast else "cast unknown", 'full_title': sound_recording.full_title, 'pub_year': sound_recording.pub_year if sound_recording.pub_year else 'publication year unknown', 'description': sound_recording.description, 'condition': sound_recording.condition.name, 'availability': sound_recording.availability, 'cover': sound_recording.cover, 'publisher': sound_recording.publisher.name if sound_recording.publisher else "publisher unknown", 'author': author if author else 'author unknown'
          },
          'operations':{
              'new_item': new_item,
              'new_authors': new_authors,
              'new_publisher': new_publisher
          }
        }
        return data_to_summary

class ModifyAuthorForm(forms.Form):
    id = forms.CharField(required=True)
    author = forms.CharField(required=True)

    def save(self):
        item = Author.objects.get(id=self.cleaned_data['id'])
        item.name = self.cleaned_data['author']
        item.save()

class ModifyDirectorForm(forms.Form):
    id = forms.CharField(required=True)
    author = forms.CharField(required=True)

    def save(self):
        item = Director.objects.get(id=self.cleaned_data['id'])
        item.name = self.cleaned_data['author']
        item.save()

class ModifyScreenwriterForm(forms.Form):
    id = forms.CharField(required=True)
    author = forms.CharField(required=True)

    def save(self):
        item = Screenwriter.objects.get(id=self.cleaned_data['id'])
        item.name = self.cleaned_data['author']
        item.save()

class ModifyPublisherForm(forms.Form):
    id = forms.CharField(required=True)
    author = forms.CharField(required=True)

    def save(self):
        item = Publisher.objects.get(id=self.cleaned_data['id'])
        item.name = self.cleaned_data['author']
        item.save()

class ModifyBookForm(forms.Form):
    id = forms.CharField(required=True)
    isbn = forms.CharField(required=False)  
    author = forms.CharField(required=False)
    title = forms.CharField(required=True)
    full_title = forms.CharField(required=True)
    pub_year = forms.IntegerField(required=False)
    publisher = forms.CharField(required=False)
    description = forms.CharField(required=False)
    condition = forms.IntegerField(required=True)
    availability = forms.IntegerField(required=True)
    cover = forms.ImageField(required=False)
    no_cover = forms.BooleanField(required=False)
   
    def save(self):
        book = Book.objects.get(id=self.cleaned_data['id'])
        
        book.isbn = self.cleaned_data["isbn"]
        book.title = self.cleaned_data['title']
        book.full_title = self.cleaned_data['full_title']
        book.pub_year = self.cleaned_data['pub_year']

        publisher = None
        try:
            publisher = Publisher.objects.get(name=self.cleaned_data['publisher']) 
        except:
            if self.cleaned_data['publisher'] != "":
                publisher = Publisher.objects.create(name=self.cleaned_data['publisher'])
            else:
                publisher = None

        book.publisher = publisher
        book.description = self.cleaned_data['description']
        book.condition = Condition.objects.get(id=self.cleaned_data['condition'])
        book.availability = Availability.objects.get(id=self.cleaned_data['availability'])

        cover = self.cleaned_data['cover'] 
        if(cover != None):
            book.cover = cover
        
        book.save()

        book.author.clear()
        authors = self.cleaned_data['author'].split(',') 
        for author in authors:
            try:
                author = Author.objects.filter(name=author)[0]
                book.author.add(author)
            except:
                if author != "":
                    author = Author.objects.create(name=author)
                    book.author.add(author)
                else:
                    author = None

class ModifySoundRecordingForm(forms.Form):
    id = forms.CharField(required=True)
    title = forms.CharField(required=True)
    author = forms.CharField(required=False)
    full_title = forms.CharField(required=True)
    cast = forms.CharField(required=False)
    pub_year = forms.IntegerField(required=False)
    publisher = forms.CharField(required=False)
    description = forms.CharField(required=False)

    condition = forms.IntegerField(required=True)
    availability = forms.IntegerField(required=True)
    cover = forms.ImageField(required=False)
    
    @transaction.atomic
    def save(self):
        sound_recording = SoundRecording.objects.get(id=self.cleaned_data['id'])

        sound_recording.title = self.cleaned_data['title']
        sound_recording.full_title = self.cleaned_data['full_title']
        sound_recording.pub_year = self.cleaned_data['pub_year']
        sound_recording.cast = self.cleaned_data['cast']
        sound_recording.description = self.cleaned_data['description']
        sound_recording.condition = Condition.objects.get(id=self.cleaned_data['condition'])
        sound_recording.availability = Availability.objects.get(id=self.cleaned_data['availability'])

        cover = self.cleaned_data['cover']
        if(cover != None):
            sound_recording.cover = self.cleaned_data['cover'] 
        
        publisher = None
        try:
            publisher = Publisher.objects.get(name=self.cleaned_data['publisher']) 
        except:
            if self.cleaned_data['publisher'] != "":
                publisher = Publisher.objects.create(name=self.cleaned_data['publisher'])
            else:
                publisher = None

        sound_recording.publisher = publisher

        sound_recording.description = self.cleaned_data['description']
        sound_recording.condition = Condition.objects.get(id=self.cleaned_data['condition'])
        sound_recording.availability = Availability.objects.get(id=self.cleaned_data['availability'])

        sound_recording.save()
        authors = self.cleaned_data['author'].split(',') 

        sound_recording.author.clear()
        for author in authors:
            try:
                author = Author.objects.filter(name=author)[0]
                sound_recording.author.add(author)
            except:
                if author != "":
                    author = Author.objects.create(name=author)
                    sound_recording.author.add(author)
                else:
                    author = None

class ModifyMovieForm(forms.Form):
    id = forms.CharField(required=True)
    director = forms.CharField(required=False)
    screenwriter = forms.CharField(required=False)
    title = forms.CharField(required=True)
    full_title = forms.CharField(required=True)
    pub_year = forms.IntegerField(required=False)
    description = forms.CharField(required=False)
    condition = forms.IntegerField(required=True)
    availability = forms.IntegerField(required=True)
    cover = forms.ImageField(required=False)
    
    @transaction.atomic
    def save(self):
        movie = Movie.objects.get(id=self.cleaned_data['id'])

        movie.title = self.cleaned_data['title']
        movie.full_title = self.cleaned_data['full_title']
        movie.pub_year = self.cleaned_data['pub_year']
        movie.description = self.cleaned_data['description']
        movie.condition = Condition.objects.get(id=self.cleaned_data['condition'])
        movie.availability = Availability.objects.get(id=self.cleaned_data['availability'])

        cover = self.cleaned_data['cover'] 
        if(cover != None):
            movie.cover = cover

        movie.save()
        movie.director.clear()
        directors = self.cleaned_data['director'].split(",")
        for director in directors:
            try:
                director = Director.objects.filter(name=director)[0]
                movie.director.add(director)
            except:
                if director != "":
                    director = Director.objects.create(name=director)
                    movie.director.add(director)
                else:
                    director = None

        movie.screenwriter.clear()
        screenwriters = self.cleaned_data['screenwriter'].split(",")
        for screenwriter in screenwriters:
            try:
                screenwriter = Screenwriter.objects.filter(name=screenwriter)[0]
                movie.screenwriter.add(screenwriter)
            except:
                if screenwriter != "":
                    screenwriter = Screenwriter.objects.create(name=screenwriter)
                    movie.screenwriter.add(screenwriter)
                else:
                    screenwriter = None



