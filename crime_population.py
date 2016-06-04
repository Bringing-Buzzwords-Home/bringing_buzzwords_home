from visualize.models import County, Geo, Item, Station, GuardianCounted, Crime
import glob
import pandas as pd
from data.popcountlist import *
import requests
import numpy as np
from datetime import datetime
import json
import csv

state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

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
df = pd.read_csv('data/FBI-crime/table_8_2014.csv',index_col=None, header=0, )
for index, row in df.iterrows():
    state_check = str(row[0]).title()
    if state_check in state_abbrev:
        state = state_check
    city_crime = Crime(
    year='2014',
    state=state,
    city=row[1],
    population=row[2],
    violent_crime=row[3],
    murder_manslaughter=row[4],
    rape_revised_def=row[5],
    rape_legacy_def=row[6],
    robbery=row[7],
    aggravated_assault=row[8],
    property_crime=row[9],
    burglary=row[10],
    larceny_theft=row[11],
    motor_vehicle_theft=row[12],
    arson=row[13],
    )
    city_crime.save()


df = pd.read_csv('data/FBI-crime/table_8_2013.csv',index_col=None, header=0, )
for index, row in df.iterrows():
    state_check = str(row[0]).title()
    if state_check in state_abbrev:
        state = state_check
    city_crime = Crime(
    year='2013',
    state=state,
    city=row[1],
    population=row[2],
    violent_crime=row[3],
    murder_manslaughter=row[4],
    rape_revised_def=row[5],
    rape_legacy_def=row[6],
    robbery=row[7],
    aggravated_assault=row[8],
    property_crime=row[9],
    burglary=row[10],
    larceny_theft=row[11],
    motor_vehicle_theft=row[12],
    arson=row[13],
    )
    city_crime.save()


df = pd.read_csv('data/FBI-crime/table_8_2012.csv',index_col=None, header=0, )
for index, row in df.iterrows():
    state_check = str(row[0]).title()
    if state_check in state_abbrev:
        state = state_check
    city_crime = Crime(
    year='2012',
    state=state,
    city=row[1],
    population=row[2],
    violent_crime=row[3],
    murder_manslaughter=row[4],
    rape_legacy_def=row[5],
    robbery=row[6],
    aggravated_assault=row[7],
    property_crime=row[8],
    burglary=row[9],
    larceny_theft=row[10],
    motor_vehicle_theft=row[11],
    arson=row[12],
    )
    city_crime.save()


df = pd.read_csv('data/FBI-crime/table_8_2011.csv',index_col=None, header=0, )
for index, row in df.iterrows():
    state_check = str(row[0]).title()
    if state_check in state_abbrev:
        state = state_check
    city_crime = Crime(
    year='2011',
    state=state,
    city=row[1],
    population=row[2],
    violent_crime=row[3],
    murder_manslaughter=row[4],
    rape_legacy_def=row[5],
    robbery=row[6],
    aggravated_assault=row[7],
    property_crime=row[8],
    burglary=row[9],
    larceny_theft=row[10],
    motor_vehicle_theft=row[11],
    arson=row[12],
    )
    city_crime.save()


df = pd.read_csv('data/FBI-crime/table_8_2010.csv',index_col=None, header=0, )
for index, row in df.iterrows():
    state_check = str(row[0]).title()
    if state_check in state_abbrev:
        state = state_check
    city_crime = Crime(
    year='2010',
    state=state,
    city=row[1],
    population=row[2],
    violent_crime=row[3],
    murder_manslaughter=row[4],
    rape_legacy_def=row[5],
    robbery=row[6],
    aggravated_assault=row[7],
    property_crime=row[8],
    burglary=row[9],
    larceny_theft=row[10],
    motor_vehicle_theft=row[11],
    arson=row[12],
    )
    city_crime.save()

df = pd.read_csv('data/FBI-crime/table_8_2009.csv',index_col=None, header=0, )
for index, row in df.iterrows():
    state_check = str(row[0]).title()
    if state_check in state_abbrev:
        state = state_check
    city_crime = Crime(
    year='2009',
    state=state,
    city=row[1],
    population=row[2],
    violent_crime=row[3],
    murder_manslaughter=row[4],
    rape_legacy_def=row[5],
    robbery=row[6],
    aggravated_assault=row[7],
    property_crime=row[8],
    burglary=row[9],
    larceny_theft=row[10],
    motor_vehicle_theft=row[11],
    arson=row[12],
    )
    city_crime.save()

df = pd.read_csv('data/FBI-crime/table_8_2008.csv',index_col=None, header=0, )
for index, row in df.iterrows():
    state_check = str(row[0]).title()
    if state_check in state_abbrev:
        state = state_check
    city_crime = Crime(
    year='2008',
    state=state,
    city=row[1],
    population=row[2],
    violent_crime=row[3],
    murder_manslaughter=row[4],
    rape_legacy_def=row[5],
    robbery=row[6],
    aggravated_assault=row[7],
    property_crime=row[8],
    burglary=row[9],
    larceny_theft=row[10],
    motor_vehicle_theft=row[11],
    arson=row[12],
    )
    city_crime.save()


df = pd.read_csv('data/FBI-crime/table_8_2007.csv',index_col=None, header=0, )
for index, row in df.iterrows():
    state_check = str(row[0]).title()
    if state_check in state_abbrev:
        state = state_check
    city_crime = Crime(
    year='2007',
    state=state,
    city=row[1],
    population=row[2],
    violent_crime=row[3],
    murder_manslaughter=row[4],
    rape_legacy_def=row[5],
    robbery=row[6],
    aggravated_assault=row[7],
    property_crime=row[8],
    burglary=row[9],
    larceny_theft=row[10],
    motor_vehicle_theft=row[11],
    arson=row[12],
    )
    city_crime.save()

df = pd.read_csv('data/FBI-crime/table_8_2006.csv',index_col=None, header=0, )
for index, row in df.iterrows():
    state_check = str(row[0]).title()
    if state_check in state_abbrev:
        state = state_check
    city_crime = Crime(
    year='2006',
    state=state,
    city=row[1],
    population=row[2],
    violent_crime=row[3],
    murder_manslaughter=row[4],
    rape_legacy_def=row[5],
    robbery=row[6],
    aggravated_assault=row[7],
    property_crime=row[8],
    burglary=row[9],
    larceny_theft=row[10],
    motor_vehicle_theft=row[11],
    arson=row[12],
    )
    city_crime.save()



crimes = Crime.objects.all()

for crime in crimes:
    try:
        if (crime.state in state_abbrev):
            address_info = crime.city + ' ' + crime.state
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
        county_obj = County.objects.get(google_county_name=county_goog, state=crime.state)
        crime.county = county_obj
        crime.save()
        print('FK assignment success #1')
    except:
        print('fail')
