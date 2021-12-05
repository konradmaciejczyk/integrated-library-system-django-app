from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password, **other_fields):
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



class Gender(models.Model):
    name = CharField(max_length=7, verbose_name="Gender/Sex")

    def __str__(self):
        return self.name

class Citizenship(models.Model):
    name = CharField(max_length=33, verbose_name="Citizenship")

    def __str__(self):
        return self.name

class IDType(models.Model):
    name = CharField(max_length=8, verbose_name="Identity document type")

    def __str__(self):
        return self.name

class Occupation(models.Model):
    name = CharField(max_length=16, verbose_name="Occupation")

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=40, verbose_name="First name")
    last_name = models.CharField(max_length=40, verbose_name="Last name")
    email = models.EmailField(max_length=30, verbose_name="E-mail address", unique=True, primary_key=True)
    phone_number = models.CharField(max_length=15, verbose_name="Phone number")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    borrows_max = models.SmallIntegerField(verbose_name="Max amount of borrowed items")
    current_borrows = models.SmallIntegerField(verbose_name="Current amount of borrowed items", default=0)
    date_of_birth = models.DateField(verbose_name="Date of birth")
    citizenship = models.ForeignKey(Citizenship, default=226, verbose_name="Citizenship", on_delete=models.CASCADE)
    occupation = models.ForeignKey(Occupation, default=4, on_delete=models.CASCADE, verbose_name="Occupation")
    corr_address = models.CharField(max_length=50, verbose_name="Correspondence address")
    id_type = models.ForeignKey(IDType, on_delete=models.CASCADE, verbose_name="ID type")
    id_number = models.CharField(max_length=15, verbose_name="ID number")
    gender = models.ForeignKey(Gender, default=4, verbose_name="Gender", on_delete=models.CASCADE)    

    def __str__(self):
        return f'{self.user}'
