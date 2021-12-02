from django.db import models
from django.db.models.deletion import SET, SET_NULL
from django.utils.timezone import now

class Gender(models.Model):
    name = models.CharField(max_length=7, default="Male")

    def __str__(self):
        return self.name

class IDDocumentType(models.Model):
    name = models.CharField(max_length=8, default="ID Card")

    def __str__(self):
        return self.name
    
class Citizenship(models.Model):
    name = models.CharField(max_length=33, verbose_name="Citizenship", default="Polish")

    def __str__(self):
        return self.name

class Occupation(models.Model):
    name = models.CharField(max_length=16, verbose_name="Occupation", default='Other')

    def __str__(self):
        return self.name


class Client(models.Model):
    first_name = models.CharField(max_length=40, verbose_name="First name", default="Jan")
    last_name = models.CharField(max_length=40, verbose_name="Last name/Surname", default="Kowalski")
    gender = models.ForeignKey(Gender, verbose_name="Sex/Gender", default=1, null=True, on_delete=SET_NULL)
    date_of_birth = models.DateField(verbose_name="Date of birth", default=now)
    citizenship = models.ForeignKey(Citizenship, verbose_name="Citizenship", default=300, null=True, on_delete=SET_NULL)
    id_doc_type = models.ForeignKey(IDDocumentType, default=1, null=True, on_delete=SET_NULL, verbose_name="Type of ID document")
    id_card = models.CharField(max_length=30, null=True, default=1, verbose_name="ID document number")
    email = models.EmailField(verbose_name="E-mail address", default="unknown@unknow.com")
    phone_num = models.CharField(max_length=15, verbose_name="Phone number", default="+48 123456789")
    corr_address = models.CharField(max_length=50, verbose_name="Correspondance address", default="221B Baker St., London, U.K.")
    occupation = models.ForeignKey(Occupation, default=3, null=True, on_delete=SET_NULL, verbose_name="Occupation")   
    # borrows_limit = models.PositiveSmallIntegerField(verbose_name="User's maximum borrows at the same time")
    # borrows_left = models.PositiveSmallIntegerField(verbose_name="Current amount of borrowed items by user")
    # date_of_join = models.DateTimeField(auto_now_add=True, verbose_name="Date of account created")
    # account_locked = models.BooleanField(default=False, verbose_name="Is user's account suspended?")
    # is_password_default = models.BooleanField(default=False, verbose_name="Has user changed it's auto generated password?")

    def __str__(self):
        return self.first_name + ' ' + self.last_name 





