from django.db import models


class GuardianDeaths(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=30)
    race_ethnicity = models.CharField(max_length=30)
    date = models.DateField()
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    classification = models.CharField(max_length=255)
    law_enforcement_agency = models.CharField(max_length=255)
    armed = models.CharField(max_length=100)
