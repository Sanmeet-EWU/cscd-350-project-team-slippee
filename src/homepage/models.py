from django.db import models


class Homepage(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone = models.IntegerField(null=True)
# Create your models here.
