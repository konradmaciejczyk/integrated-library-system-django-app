# Generated by Django 3.2.8 on 2021-12-06 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='E-mail address'),
        ),
    ]