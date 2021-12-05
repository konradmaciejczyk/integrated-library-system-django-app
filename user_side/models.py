from django.db import models
from accounts.models import User, Citizenship, Occupation, IDType, Gender

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
