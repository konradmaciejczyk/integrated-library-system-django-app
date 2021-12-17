from django.db import models

class Condition(models.Model):
    name = models.CharField(max_length=7, verbose_name="Item's condition")

    def __str__(self):
        return self.name

class Availability(models.Model):
    name = models.CharField(max_length=23, verbose_name="Item's availability")

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50, verbose_name="Author's first and last name")

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=100, verbose_name="Publisher's name")

    def __str__(self):
        return self.name


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
    cover = models.ImageField(default="default_cover.jpg", upload_to="covers")

    def __str__(self):
        return self.author.name + ' - ' + self.title