from visualize.models import County, Geo, Item, Station
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
