from django.core.exceptions import ObjectDoesNotExist
from .models import GuardianCounted, County, Item
import csv
import datetime
import pandas as pd


months = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
          'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
          'October': 10, 'November': 11, 'December': 12}

county_csv_path = 'data/DC_model_csv/visualize_county.csv'
xl_path = 'data/DISP_AllStatesAndTerritories_160401.xlsx'


def populate_item_from_xl(xl_path):
    item_df = pd.read_csv('data/DC_model_csv/visualize_item.csv')
    military_equipment = {}
    with pd.ExcelFile(xl_path) as xls:
        for sheet in xls.sheet_names:
            military_equipment[sheet] = pd.read_excel(xls, sheet)

    for state in military_equipment:
        for index, row in military_equipment[state].iterrows():
            total_value = row['Quantity'] * row['Acquisition Value']
            #date_string = row['Ship Date']
            #datetime_obj = datetime.strptime(date_string, '%b %d, %Y %I:%M:%S %p')
            try:
                place = item_df[(item_df['state'] == row['State']) & (item_df['station_name'] == row['Station Name (LEA)']) & (item_df['NSN'] == row['NSN'])]
                county_id = int(place['county_id'][place.index[0]])
                county_obj = County.objects.get(id=county_id)
            except (ValueError, ObjectDoesNotExist):
                county_obj = None
            item = Item(state=row['State'],
                        station_name=row['Station Name (LEA)'],
                        NSN=row['NSN'], Item_Name=row['Item Name'],
                        Quantity=row['Quantity'],
                        UI=row['UI'], Acquisition_Value=row['Acquisition Value'],
                        DEMIL_Code=row['DEMIL Code'],
                        DEMIL_IC=row['DEMIL IC'], Ship_Date=row['Ship Date'],
                        county=county_obj, Total_Value=total_value)
            item.save()


def populate_county_from_csv(county_csv_path):
    with open(county_csv_path) as f:
        county_reader = csv.DictReader(f)
        for row in county_reader:
            if row['state'] != 'Puerto Rico':
                try:
                    twenty_fourteen = int(row['pop_est_2014'])
                except ValueError:
                    twenty_fourteen = None
                try:
                    twenty_thirteen = int(row['pop_est_2013'])
                except ValueError:
                    twenty_thirteen = None
                try:
                    twenty_twelve = int(row['pop_est_2012'])
                except ValueError:
                    twenty_twelve = None
                try:
                    twenty_eleven = int(row['pop_est_2011'])
                except ValueError:
                    twenty_eleven = None
                try:
                    twenty_ten = int(row['pop_est_2010'])
                except ValueError:
                    twenty_ten = None
                try:
                    twenty_nine = int(row['pop_est_2009'])
                except ValueError:
                    twenty_nine = None
                try:
                    twenty_eight = int(row['pop_est_2008'])
                except ValueError:
                    twenty_eight = None
                try:
                    twenty_seven = int(row['pop_est_2007'])
                except ValueError:
                    twenty_seven = None
                try:
                    twenty_six = int(row['pop_est_2006'])
                except ValueError:
                    twenty_six = None
                try:
                    twenty_five = int(row['pop_est_2005'])
                except ValueError:
                    twenty_five = None
                try:
                    twenty_four = int(row['pop_est_2004'])
                except ValueError:
                    twenty_four = None
                try:
                    twenty_three = int(row['pop_est_2003'])
                except ValueError:
                    twenty_three = None
                try:
                    twenty_two = int(row['pop_est_2002'])
                except ValueError:
                    twenty_two = None
                try:
                    twenty_one = int(row['pop_est_2001'])
                except ValueError:
                    twenty_one = None
                try:
                    twenty = int(row['pop_est_2000'])
                except ValueError:
                    twenty = None

                new_county = County(id=row['id'],
                                    pop_est_2015=row['pop_est_2015'],
                                    county_name=row['county_name'],
                                    state=row['state'],
                                    FIPS=row['FIPS'],
                                    google_county_name=row['google_county_name'],
                                    pop_est_2014=twenty_fourteen,
                                    pop_est_2013=twenty_thirteen,
                                    pop_est_2012=twenty_twelve,
                                    pop_est_2011=twenty_eleven,
                                    pop_est_2010=twenty_ten,
                                    pop_est_2009=twenty_nine,
                                    pop_est_2008=twenty_eight,
                                    pop_est_2007=twenty_seven,
                                    pop_est_2006=twenty_six,
                                    pop_est_2005=twenty_five,
                                    pop_est_2004=twenty_four,
                                    pop_est_2003=twenty_three,
                                    pop_est_2002=twenty_two,
                                    pop_est_2001=twenty_one,
                                    pop_est_2000=twenty)
                new_county.save()


def handle_guardian_counted_csv(csv_path, months):
    guardian_csv = pd.read_csv('data/DC_model_csv/visualize_guardiancounted.csv')
    with open(csv_path) as f:
        counted_reader = csv.DictReader(f)
        for row in counted_reader:
            try:
                person_age = int(row['age'])
            # if age is unknown, age will be NULL in the db
            except ValueError:
                person_age = None
            try:
                place = guardian_csv[(guardian_csv['state'] == row['state']) & (guardian_csv['name'] == row['name']) & (guardian_csv['city'] == row['city'])]
                county_id = place['county_id'][place.index[0]]
                county_obj = County.objects.get(id=county_id)
            except (ValueError, ObjectDoesNotExist):
                county_obj = None
            counted = GuardianCounted(name=row['name'],
                                      age=person_age,
                                      gender=row['gender'],
                                      race_ethnicity=row['raceethnicity'],
                                      date=datetime.date(
                                        year=int(row['year']),
                                        month=months[row['month']],
                                        day=int(row['day'])),
                                      street_address=row['streetaddress'],
                                      city=row['city'],
                                      state=row['state'],
                                      classification=row['classification'],
                                      law_enforcement_agency=row['lawenforcementagency'],
                                      armed=row['armed'],
                                      county=county_obj)
            counted.save()


def guardian_pop(months):
    handle_guardian_counted_csv('data/thecounted-data/the-counted-2015.csv', months)
    handle_guardian_counted_csv('data/thecounted-data/the-counted-2016.csv', months)


def populate_crime_from_csv():
    with open('data/DC_model_csv/visualize_crime.csv') as f:
        crime_reader = csv.DictReader(f)
        for row in crime_reader:
            if row['county_id'] == '':
                county_obj = None
            else:
                try:
                    county_obj = County.objects.get(id=row['county_id'])
                except ObjectDoesNotExist:
                    county_obj = None
            

def item_categories(apps, schema_editor):
    items = Item.objects.all()
    for item in items:
        if item.Item_Name in ['AIRCRAFT, ROTARY WING',
                              'AIRCRAFT, FIXED WING',
                              'AIRPLANE,CARGO-TRANSPORT',
                              'AIRPLANE,UTILITY U8F'
                              ]:

            item.Category = 'Aircraft'
            item.save()

        elif item.Item_Name in ['HELICOPTER,SEARCH AND RESCUE',
                                'HELICOPTER,FLIGHT TRAINER',
                                'HELICOPTER,FLIGHT TRAINER TH55A',
                                'HELICOPTER,MEDEVAC ',
                                'HELICOPTER,OBSERVATION',
                                'HELICOPTER,SEARCH AND RESCUE',
                                'HELICOPTER,UTILITY'
                                ]:

            item.Category = 'Helicopter'
            item.save()

        elif item.Item_Name in ['RIFLE',
                                'RIFLE,5.56 MILLIMETER',
                                'RIFLE,7.62 MILLIMETER',
                                'SIMULATED,M16A2 RIFLE,5.56MM',
                                'SIMULATED,M16A4-203 RIFLE W-GRENADE LAUNCHER,5.56MM-40MM',
                                'GUNS, THROUGH 30MM',
                                'SIMULATED,M4-203 RIFLE W-GRENADE LAUNCHER,5.56MM-40MM',
                                ]:

            item.Category = "Assualt Rifle"
            item.save()

        elif item.Item_Name in ['SMALL CRAFT BOAT',
                                'BOAT,INFLATABLE    ',
                                'BOAT,LANDING,INFLATABLE',
                                'BOAT,PERSONNEL',
                                'BOAT,PICKET',
                                'BOAT,RECONNAISSANCE,PNEUMATIC',
                                'BOAT,RIGID INFLATABLE',
                                'BOAT,RIGID RAIDING',
                                'BOAT,SEMI-VEE      ',
                                'BOAT,UTILITY',
                                'MOTORBOAT',
                                'BOAT,RIGID RAIDING',
                                ]:

            item.Category = "Boat"
            item.save()

        elif item.Item_Name in ["EOD ROBOT",
                                "ROBOT,EXPLOSIVE ORDNANCE DISPO",
                                "ROBOT,EXPLOSIVE ORDNANCE DISPOSAL",
                                'PACKBOT 510 WITH FASTAC REMOTELY CONTROLLED VEHICLE',
                                'UNMANNED VEHICLE',
                                'ROBOT,EXPLOSIVE,SPE',
                                ]:

            item.Category = "Bomb-Disposal Robot"
            item.save()

        elif item.Item_Name in ['ALL TERRAIN VEHICLE WHEELED',
                                'ALL TERRAIN VEHICLE, 4 WHEEL',
                                'ALL TERRAIN VEHICLE, AG/BVUS',
                                ]:

            item.Category = 'ATV'
            item.save()

        elif item.Item_Name == 'MINE RESISTANT VEHICLE':
            item.Category = 'Mine Resistant Vehicle'
            item.save()

        elif item.Item_Name in ['ONLY COMPLETE COMBAT/ASSAULT/TACTICAL WHEELED VEHICLES',
                                'LIGHT ARMORED VEHICLE',
                                'FAST ATTACK VEHICLE',
                                'PASSENGER MOTOR VEHICLES',
                                'UTILITY VEHICLE,4WD',
                                'UTILITY VEHICLE',
                                'UTILITY VEHICLE,ALL-TERRAIN',
                                'UTILITY VEHICLE,OFF ROAD',
                                'SPECIAL PURPOSE VEHICLE',
                                ]:

            item.Category = 'Assault/Tactical Vehicle'
            item.save()

        elif item.Item_Name in ['MACHETE,RIGID HANDLE',
                                'BAYONET-KNIFE',
                                'HOOK KNIFE,RESCUE  ',
                                'Knife',
                                'KNIFE,COMBAT',
                                'KNIFE,COMBAT,WITH SHEATH',
                                "KNIFE,CRAFTSMAN'S",
                                "KNIFE,CRAFTSMANS",
                                "KNIFE,FIELD MESS",
                                'KNIFE,FIXED,CAMO   ',
                                'KNIFE,GENERAL SURGICAL',
                                'KNIFE,HOT TIP,ELECTRIC',
                                'KNIFE,HUNTING',
                                'KNIFE,POCKET',
                                'KNIFE,RESCUE       ',
                                'SCABBARD,BAYONET-KNIFE',
                                'SWITCH,KNIFE',
                                "KNIFE,STRAP CUTTING,FIREMAN'S",
                                ]:

            item.Category = 'Machete/Bayonnet/Knife'
            item.save()

        elif item.Item_Name in ["PISTOL,CALIBER .38 SPECIAL,AUTOMATIC",
                                "PISTOL,CALIBER .45,AUTOMATIC",
                                "PISTOL, 40CAL, GLOCK GEN 3",
                                ]:

            item.Category = 'Pistol'
            item.save()

        elif item.Item_Name in ['SHOTGUN,12 GAGE',
                                'SHOTGUN,12 GAGE,RIOT TYPE',
                                ]:

            item.Category = "Shotgun"
            item.save()
