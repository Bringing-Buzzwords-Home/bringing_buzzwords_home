from .models import GuardianDeaths
import csv
import datetime
from visualize.models import Item

months = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
          'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
          'October': 10, 'November': 11, 'December': 12}


def handle_guardian_counted_csv(csv_path, months):
    with open(csv_path) as f:
        counted_reader = csv.DictReader(f)
        for row in counted_reader:
            try:
                person_age = int(row['age'])
            # if age is unknown, age will be NULL in the db
            except ValueError:
                person_age = None
            counted = GuardianDeaths(name=row['name'],
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
                                     armed=row['armed'])
            counted.save()


def guardian_pop(months):
    handle_guardian_counted_csv('data/thecounted-data/the-counted-2015.csv', months)
    handle_guardian_counted_csv('data/thecounted-data/the-counted-2016.csv', months)


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
