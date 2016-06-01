from visualize.models import County, Geo, Item, Station
import glob
import pandas as pd
from data.popcountlist import *
import requests
import us
from datetime import datetime



states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
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
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
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
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
        }




def county_pop():
    count = 1
while count < 3221:
    county = poplist[count]
    loc_list = (county[1]).split(",")
    pop = County(population=county[0],
        county_name=loc_list[0],
        state=loc_list[1],
        FIPS_state=county[2],
        FIPS_county=county[3]
        )
    count+=1
    pop.save()


def geo_pop():
    df = pd.read_csv('data/zip_code_database.csv',index_col=None, header=0)

if row['country'] == 'US':
for index, row in df.iterrows():
    try:
        if row['country'] == 'US' and row['state'] in states:
            print(row['state'])
            state = row['state']
            state = ' ' + states[state]
            print(state)
            geo = Geo(zip_code=row['zip'], county_name=row['county'],
                city=row['primary_city'], state=row['state'],
                county=County.objects.get(county_name=row['county'], state=state))
            geo.save()
    except:
        pass




def station_pop():
stations = Item.objects.order_by().values_list('station_name', flat=True).distinct()
for station in stations:
    r = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key=AIzaSyB8HQrjyVgQCJv9vcXKy_zB7ALgwl2jk7E'.format(station))
    r = r.json()
    zip_code = r['results'][0]['formatted_address'][-20:-15]
    geo_obj = Geo.objects.get(zip_code=zip_code)
    station_info = Station(
        station_name = station,
        address = r['results'][0]['formatted_address'],
        lat = r['results'][0]['geometry']['location']['lat'],
        lng = r['results'][0]['geometry']['location']['lng'],
        goog_id_num = r['results'][0]['place_id'],
        county = geo_obj.county)
    station_info.save()

    except:
        station_info = Station(
            station_name = station)


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
    
    item = Item(state=row['State'], station_name=row['Station Name (LEA)'],
                NSN=row['NSN'], Item_Name=row['Item Name'], Quantity=row['Quantity'],
                UI=row['UI'], Acquisition_Value=acquisition_Value, DEMIL_Code=row['DEMIL Code'],
                DEMIL_IC=row['DEMIL IC'], Ship_Date=row['Ship Date'], county=County.objects.get(county_name='Autauga County'))
    item.save()


    station_obj = Station.objects.get(station_name=row['Station Name (LEA)'])
    county_obj = station_obj.county
