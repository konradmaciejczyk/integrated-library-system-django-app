from django.db import models
from django.db.models.fields.related import ForeignKey
from accounts.models import User, Citizenship, Occupation, IDType
from worker_side.models import Book, Movie, SoundRecording
from django.utils import timezone

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    borrows_max = models.SmallIntegerField(verbose_name="Max amount of borrowed items")
    current_borrows = models.SmallIntegerField(verbose_name="Current amount of borrowed items", default=0)
    date_of_birth = models.DateField(verbose_name="Date of birth")
    citizenship = models.ForeignKey(Citizenship, default=226, verbose_name="Citizenship", on_delete=models.CASCADE)
    occupation = models.ForeignKey(Occupation, default=4, on_delete=models.CASCADE, verbose_name="Occupation")
    corr_address = models.CharField(max_length=50, verbose_name="Correspondence address")
    id_type = models.ForeignKey(IDType, on_delete=models.CASCADE, verbose_name="ID type")
    id_number = models.CharField(max_length=15, verbose_name="ID number")
    registration_date = models.DateTimeField(default=timezone.now, verbose_name="Registration date")

    def __str__(self):
        return f'{self.user}'

class Status(models.Model):
    name = models.CharField(max_length=18, verbose_name="Order status")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Statuses"

class BookOrder(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    item = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Book")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Order placed at")
    status = ForeignKey(Status, on_delete=models.SET_NULL, null=True, verbose_name="Book order status")

    def __str__(self):
        return "{} (ID: {}) by {} (E-mail: {})".format(self.item.title, self.item.id, self.client.user.first_name + self.client.user.last_name, self.client.user.email)

class MovieOrder(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    item = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Movie")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Order placed at")
    status = ForeignKey(Status, on_delete=models.SET_NULL, null=True, verbose_name="Movie order status")

    def __str__(self):
        return "{} (ID: {}) by {} (E-mail: {})".format(self.item.title, self.item.id, self.client.user.first_name + self.client.user.last_name, self.client.user.email)

class SoundRecordingOrder(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    item = models.ForeignKey(SoundRecording, on_delete=models.CASCADE, verbose_name="Sound recording")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Order placed at")
    status = ForeignKey(Status, on_delete=models.SET_NULL, null=True, verbose_name="Sound recording order status")

    def __str__(self):
        return "{} (ID: {}) by {} (E-mail: {})".format(self.item.title, self.item.id, self.client.user.first_name + " " + self.client.user.last_name, self.client.user.email)