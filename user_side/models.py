from django.db import models


class Client(models.Model):
    # genders=(
    #     ('male', "Male"), ('female', "Female"), ("diverse", "Diverse")
    # )

    # id_cards_types = (
    #     ('passport', 'Passport'), ('id card', 'ID Card')
    # )

    # occupation = (
    #     ('student', 'Student'), ('academic teacher', 'Academic Teacher'), ('other', 'Other')
    # )

    first_name = models.CharField(max_length=40, verbose_name="First name")
    last_name = models.CharField(max_length=40, verbose_name="Last name/Surname")
    # gender = models.CharField(max_length=7, choices=genders, verbose_name="Sex/Gender")
    # date_of_birth = models.DateField(verbose_name="Date of birth")
    # citizenship = models.CharField(max_length=30, verbose_name="Citizenship")
    # id_card_type = models.CharField(max_length=8, choices=id_cards_types, verbose_name="Type of ID document")
    # id_card = models.CharField(max_length=30, verbose_name="ID document number")
    # email = models.EmailField(verbose_name="E-mail address")
    # phone_num = models.CharField(max_length=15, verbose_name="Phone number")
    # corr_address = models.CharField(max_length=50, verbose_name="Correspondance address")
    # occupation = models.CharField(max_length=16, verbose_name="Occupation")   
    # borrows_limit = models.PositiveSmallIntegerField(verbose_name="User's maximum borrows at the same time")
    # borrows_left = models.PositiveSmallIntegerField(verbose_name="Current amount of borrowed items by user")
    # date_of_join = models.DateTimeField(auto_now_add=True, verbose_name="Date of account created")
    # account_locked = models.BooleanField(default=False, verbose_name="Is user's account suspended?")
    # is_password_default = models.BooleanField(default=False, verbose_name="Has user changed it's auto generated password?")

    def __str__(self):
        return self.first_name + ' ' + self.last_name 



