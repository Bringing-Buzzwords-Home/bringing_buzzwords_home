from django.db import models

# Create your models here.
class County(models.Model):
    population = models.IntegerField()
    county_name = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    FIPS_state = models.CharField(max_length=300)
    FIPS_county = models.CharField(max_length=300)

    def __str__(self):
        return self.county_name

class Geo(models.Model):
    zip_code = models.CharField(max_length=300)
    county_name = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    county = models.ForeignKey(County, on_delete=models.CASCADE)

    def __str__(self):
        return self.county_name

class Item(models.Model):
    state = models.CharField(max_length=200)
    station_name = models.CharField(max_length=200)
    NSN = models.CharField(max_length=200)
    Item_Name = models.CharField(max_length=200)
    Quantity = models.IntegerField()
    UI = models.CharField(max_length=200)
    Acquisition_Value = models.CharField(max_length=200)
    DEMIL_Code = models.CharField(max_length=200)
    DEMIL_IC = models.CharField(max_length=200)
    Ship_Date = models.CharField(max_length=200)
    county = models.ForeignKey(County, on_delete=models.CASCADE)


    def __str__(self):
        return self.Item_Name

class Station(models.Model):
    station_name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    lat = models.CharField(max_length=300)
    lng = models.CharField(max_length=300)
    goog_id_num = models.CharField(max_length=300)
    county = models.ForeignKey(County, on_delete=models.CASCADE)

    def __str__(self):
        return self.station_name
