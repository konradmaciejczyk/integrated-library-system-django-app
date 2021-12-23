from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from re import match

class Citizenship(models.Model):
    name = models.CharField(max_length=33, verbose_name="Citizenship")

    def __str__(self):
        return self.name

class IDType(models.Model):
    name = models.CharField(max_length=8, verbose_name="Identity document type")

    def __str__(self):
        return self.name

class Occupation(models.Model):
    name = models.CharField(max_length=16, verbose_name="Occupation")

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):

    def validate(self, data):
        """Function that validates registration form.

        Parameters:
        data: (dict) dictionary of values from form

        Returns:
        None (Asserts ValidationError when form is invalid)
        """

        try:#citizenship, occupation, gender, id_type
            #first_name, last_name
            assert(data['first_name'].isalpha() and data['last_name'].isalpha())
            #phone_number
            assert(match(r'\+[1-9]{1}[0-9]{7,14}$', data['phone_number']))  
        except:
            raise ValueError("Invalid information!")
            
    def create_user(self, email, first_name, last_name, phone_number, password, **other_fields):

        self.validate({'first_name': first_name, "last_name": last_name, "phone_number": phone_number})

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, phone_number=phone_number, **other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, first_name, last_name, phone_number, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email=email, first_name=first_name, last_name=last_name, phone_number=phone_number, password=password, **other_fields)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=40, verbose_name="First name")
    last_name = models.CharField(max_length=40, verbose_name="Last name")
    email = models.EmailField(max_length=50, verbose_name="E-mail address", unique=True, primary_key=True)
    phone_number = models.CharField(max_length=15, verbose_name="Phone number")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
