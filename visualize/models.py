from django.db import models


class County(models.Model):
    population = models.IntegerField()
    county_name = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    FIPS_state = models.CharField(max_length=300)
    FIPS_county = models.CharField(max_length=300)

    def __str__(self):
        return self.county_name


class GuardianDeaths(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=30)
    race_ethnicity = models.CharField(max_length=30)
    date = models.DateField()
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    classification = models.CharField(max_length=255)
    law_enforcement_agency = models.CharField(max_length=255)
    armed = models.CharField(max_length=100)
    county = models.ForeignKey('County', null=True, on_delete=models.CASCADE)
