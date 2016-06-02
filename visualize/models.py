from django.db import models


class County(models.Model):
    population = models.IntegerField()
    county_name = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    FIPS = models.CharField(max_length=300)

    def __str__(self):
        return self.county_name


class GuardianCounted(models.Model):
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

    def __str__(self):
        return "{}, Age: {}, Location: {},{}".format(self.name, self.age,
                                                     self.city, self.state)

class Geo(models.Model):
    zip_code = models.TextField()
    city = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.county_name


class Item(models.Model):
    state = models.CharField(max_length=200)
    station_name = models.CharField(max_length=200)
    NSN = models.CharField(max_length=200)
    Item_Name = models.CharField(max_length=200)
    Quantity = models.IntegerField()
    UI = models.CharField(max_length=200)
    Acquisition_Value = models.IntegerField()
    DEMIL_Code = models.CharField(max_length=200)
    DEMIL_IC = models.CharField(max_length=200)
    Ship_Date = models.CharField(max_length=200)
    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.Item_Name


class Station(models.Model):
    station_name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    lat = models.CharField(max_length=300)
    lng = models.CharField(max_length=300)
    goog_id_num = models.CharField(max_length=300)
    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.station_name
