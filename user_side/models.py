from django.db import models


class Readers(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    corr_address = models.CharField(max_length=50)
    # date_of_birth = models.DateField()
    citizenship = models.CharField(max_length=30)
    id_card = models.CharField(max_length=30)
    phone_num = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    borrows_limit = models.PositiveIntegerField()
    borrows_left = models.PositiveIntegerField()
    # date_of_join = models.DateField()
    account_locked = models.BooleanField()

    def __str__(self):
        return self.name + self.surname



