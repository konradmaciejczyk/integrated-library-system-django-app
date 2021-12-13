from django.db import models

class Condition(models.Model):
    name = models.CharField(max_length=7, verbose_name="Item condition")

class Availability(models.Model):
    name = models.CharField(max_length=23, verbose_name="Item availability")

class Author(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Item availability")
    last_name = models.CharField(max_length=50, verbose_name="Item availability")

class Publisher(models.Model):
    name = models.CharField(max_length=100, verbose_name="Publisher name")


class Book(models.Model):
    isbn = models.CharField(max_length=13, null=True, verbose_name="ISBN")
    title = models.CharField(max_length=100, verbose_name="Title")
    full_title = models.CharField(max_length=150, verbose_name="Full title")
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, verbose_name="Author")
    pub_year = models.SmallIntegerField(null=True, verbose_name="Publication year")
    publisher = models.ForeignKey(Publisher, null=True, on_delete=models.SET_NULL, verbose_name="Publisher")
    description = models.CharField(max_length=200, verbose_name="Description")
    condition = models.ForeignKey(Condition, null=True, on_delete=models.SET_NULL)
    availability = models.ForeignKey(Availability, null=True, on_delete=models.SET_NULL, verbose_name="Availability status")