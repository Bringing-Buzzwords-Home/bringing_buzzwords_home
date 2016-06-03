from visualize.models import County, Geo, Item, Station, GuardianCounted
import glob
import pandas as pd
from data.popcountlist import *
import requests
import numpy as np
from datetime import datetime
import json

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
        }


def county_pop():
    for row in poplist:
        loc_list = (row[1]).split(", ")
        pop = County(population=row[0],
            county_name=loc_list[0],
            state=loc_list[1],
            FIPS=row[2]+row[3]
            )
        pop.save()


def geo_pop(states):
    with open('data/zip2fips.json', encoding='utf-8') as f:
        fips_dict = json.loads(f.read())
    df = pd.read_csv('data/zip_code_database.csv',index_col=None, header=0, dtype={'zip': str})
    for index, row in df.iterrows():
        try:
            if (row['state'] in states) and (row['country'] == 'US'):
                state = row['state']
                print(state)
                state = states[state]
                print(state)
                geo = Geo(zip_code=row['zip'],
                    city=row['primary_city'], state=row['state'],
                    )
                geo.save()
        except:
            geo = Geo(zip_code=row['zip'],
                city=row['primary_city'], state=row['state'])
            geo.save()
            pass





def items_pop():
    path ='data/policeitems'
    allFiles = glob.glob(path + "/*.csv")
    frame = pd.DataFrame()
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_,index_col=None, header=0)
        list_.append(df)
    frame = pd.concat(list_)
    for index, row in frame.iterrows():
        acquisition_Value = row['Acquisition Value']
        acquisition_Value = acquisition_Value[1:-3]
        acquisition_Value = acquisition_Value.replace(",", "")
        date_string = row['Ship Date']
        datetime_obj = datetime.strptime(date_string, '%b %d, %Y %I:%M:%S %p')
        item = Item(state=row['State'], station_name=row['Station Name (LEA)'],
                    NSN=row['NSN'], Item_Name=row['Item Name'], Quantity=row['Quantity'],
                    UI=row['UI'], Acquisition_Value=acquisition_Value, DEMIL_Code=row['DEMIL Code'],
                    DEMIL_IC=row['DEMIL IC'], Ship_Date=date_string)
        item.save()


# station_obj = Station.objects.get(station_name=row['Station Name (LEA)'])
# county_obj = station_obj.county


def station_pop():
    df = pd.read_csv('data/police_police.csv',index_col=None, header=0)
    for index, row in df.iterrows():
        station_info = Station(
            station_name = row['station_name'],
            address = row['address'],
            lat = row['lat'],
            lng = row['lng'],
            goog_id_num = row['goog_id_num'])
        station_info.save()
        # except:
        #     station_info = Station(
        #     station_name = row['station_name'])
        #     station_info.save()


counties = County.objects.all()
for county in counties:
    try:
        address_info = county.county_name
        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&sensor=true&key=AIzaSyAXFVf8VWCuK1kzQicEazzMlCPPku2DHyQ'.format(address_info))
        r = r.json()
        print(r)
        add_comp=r['results'][0]['address_components']
        for comp in add_comp:
            if comp['types'] == ['administrative_area_level_2', 'political']:
                county_goog = comp['long_name']
                print(county_goog)
                county.google_county_name = county_goog
                county.save()
                print('success')
    except:
        print('fail')


stations = Station.objects.all()
for station in stations:
    if station.address[-23:-21] not in states:
        continue
    station_state = states[station.address[-23:-21]]
    try:
        address_info = station.address[-20:-15]
        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&sensor=true&key=AIzaSyAXFVf8VWCuK1kzQicEazzMlCPPku2DHyQ'.format(address_info))
        r = r.json()
        print(r)
        add_comp=r['results'][0]['address_components']
        for comp in add_comp:
            if comp['types'] == ['administrative_area_level_2', 'political']:
                county_goog = comp['long_name']
                print(county_goog)
                print('api success #1')
        county_obj = County.objects.get(google_county_name=county_goog, state=station_state)
        station.county = county_obj
        station.save()
        print('FK assignment success #1')
    except:
        print('fail')
        try:
            for comp in add_comp:
                if comp['types'] == ['locality', 'political']:
                    address_info = comp['long_name'] + ' ' + station_state
                    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&sensor=true&key=AIzaSyAXFVf8VWCuK1kzQicEazzMlCPPku2DHyQ'.format(address_info))
                    r = r.json()
                    print(r)
                    add_comp=r['results'][0]['address_components']
                    for comp in add_comp:
                        if comp['types'] == ['administrative_area_level_2', 'political']:
                            county_goog = comp['long_name']
                            print(county_goog)
                            print('api success #2')
                    county_obj = County.objects.get(google_county_name=county_goog, state=station_state)
                    station.county = county_obj
                    station.save()
                    print('FK assignment success #2')
        except:
            print('epic fail')


guardian = GuardianCounted.objects.all()
for guard in guardian:
    try:
        if (guard.state in states):
            address_info = guard.city + ' ' + guard.state
            print(address_info)
            r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&sensor=true&key=AIzaSyB8HQrjyVgQCJv9vcXKy_zB7ALgwl2jk7E'.format(address_info))
            r = r.json()
            print(r)
        add_comp=r['results'][0]['address_components']
        for comp in add_comp:
            if comp['types'] == ['administrative_area_level_2', 'political']:
                county_goog = comp['long_name']
                print(county_goog)
                print('api success #1')
        county_obj = County.objects.get(google_county_name=county_goog, state=states[guard.state])
        guard.county = county_obj
        guard.save()
        print('FK assignment success #1')
    except:
        print('fail')
        try:
            for comp in add_comp:
                if comp['types'] == ['locality', 'political']:
                    address_info = comp['long_name'] + ' ' + station_state
                    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&sensor=true&key=AIzaSyAXFVf8VWCuK1kzQicEazzMlCPPku2DHyQ'.format(address_info))
                    r = r.json()
                    print(r)
                    add_comp=r['results'][0]['address_components']
                    for comp in add_comp:
                        if comp['types'] == ['administrative_area_level_2', 'political']:
                            county_goog = comp['long_name']
                            print(county_goog)
                            print('api success #2')
                    county_obj = County.objects.get(google_county_name=county_goog, state=states[guard.state])
                    guard.county = county_obj
                    guard.save()
                    print('FK assignment success #2')
        except:
            print('epic fail')

items = Item.objects.all()
for item in items:
    station = Station.objects.get(station_name=item.station_name)
    item.county = station.county
    item.save()
