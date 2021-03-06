from django.db import models


class County(models.Model):
    pop_est_2015 = models.IntegerField()
    county_name = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    FIPS = models.CharField(max_length=300)
    google_county_name = models.CharField(max_length=300, null=True)
    pop_est_2014 = models.IntegerField(null=True)
    pop_est_2013 = models.IntegerField(null=True)
    pop_est_2012 = models.IntegerField(null=True)
    pop_est_2011 = models.IntegerField(null=True)
    pop_est_2010 = models.IntegerField(null=True)
    pop_est_2009 = models.IntegerField(null=True)
    pop_est_2008 = models.IntegerField(null=True)
    pop_est_2007 = models.IntegerField(null=True)
    pop_est_2006 = models.IntegerField(null=True)
    pop_est_2005 = models.IntegerField(null=True)
    pop_est_2004 = models.IntegerField(null=True)
    pop_est_2003 = models.IntegerField(null=True)
    pop_est_2002 = models.IntegerField(null=True)
    pop_est_2001 = models.IntegerField(null=True)
    pop_est_2000 = models.IntegerField(null=True)


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
    Acquisition_Value = models.DecimalField(decimal_places=2, max_digits=50)
    Total_Value = models.DecimalField(decimal_places=2, max_digits=50)
    Category = models.CharField(max_length=200)
    DEMIL_Code = models.CharField(max_length=200)
    DEMIL_IC = models.CharField(max_length=200)
    Ship_Date = models.DateTimeField()
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


class Crime(models.Model):
    year = models.DateField()
    state = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    population = models.IntegerField()
    violent_crime = models.IntegerField()
    murder_manslaughter = models.IntegerField()
    rape_revised_def = models.IntegerField()
    rape_legacy_def = models.IntegerField()
    robbery = models.IntegerField()
    aggravated_assault = models.IntegerField()
    property_crime = models.IntegerField()
    burglary = models.IntegerField()
    larceny_theft = models.IntegerField()
    motor_vehicle_theft = models.IntegerField()
    arson = models.IntegerField()
    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True)


class State(models.Model):
    state = models.CharField(max_length=2, null=True)
    total_military_dollars = models.FloatField()
    total_deaths_twentyfifteen = models.IntegerField()
    total_violent_crime = models.IntegerField(null=True)
    total_property_crime = models.IntegerField(null=True)
    total_population_twentyfifteen = models.IntegerField()
