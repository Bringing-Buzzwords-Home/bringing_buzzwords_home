# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
from django.core.exceptions import ObjectDoesNotExist
from .models import County, GuardianCounted, Item, Crime
import csv
import datetime
from operator import itemgetter
from django.db.models import Sum, Func, Count, F
import numpy as np
# import seaborn
# import pandas as pd




class Extract(Func):
    """
    Performs extraction of `what_to_extract` from `*expressions`.

    Arguments:
        *expressions (string): Only single value is supported, should be field name to
                               extract from.
        what_to_extract (string): Extraction specificator.

    Returns:
        class: Func() expression class, representing 'EXTRACT(`what_to_extract` FROM `*expressions`)'.
    """

    function = 'EXTRACT'
    template = '%(function)s(%(what_to_extract)s FROM %(expressions)s)'


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

numbered_months = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                   5: 'May', 6: 'June', 7: 'July', 8: 'August',
                   9: 'September', 10: 'October', 11: 'November',
                   12: 'December'}

months = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
          'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
          'October': 10, 'November': 11, 'December': 12}

colors = ['#3d40a2', '#d64d4d']

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
            except (ValueError, IndexError, ObjectDoesNotExist):
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
    handle_guardian_counted_csv('data/thecounted-data/the-counted-2015.csv',
                                months)
    handle_guardian_counted_csv('data/thecounted-data/the-counted-2016.csv',
                                months)


def remove_none_from_categories(category_list):
    for num, category in enumerate(category_list):
        if bool(category['Category']) is False:
            del category_list[num]
            break
    return category_list



def compare_category_lists(category_list, state_category_list):
    state_categories = [x['Category'] for x in state_category_list]
    for num, category in enumerate(category_list):
        if category['Category'] not in state_categories:
            state_category_list.insert(num, {'Category': category['Category'],
                                             'pk__count': 0})
    return state_category_list


def make_state_categories(state):
    item_categories = Item.objects.values('Category').annotate(Count('pk'))
    category_list = list(item_categories)
    category_list = sorted(remove_none_from_categories(category_list), key=itemgetter('Category'))

    state_item_categories = Item.objects.filter(state=state).values('Category').annotate(Count('pk'))
    state_category_list = list(state_item_categories)
    state_category_list = sorted(remove_none_from_categories(state_category_list), key=itemgetter('Category'))
    state_category_list = compare_category_lists(category_list, state_category_list)

    counts = [x['pk__count'] for x in category_list]
    state_counts = [x['pk__count'] for x in state_category_list]
    categories = [x['Category'] for x in category_list]

    x_label = 'Items'
    title = 'Number of Items Donated in the 1033 Program'
    category_data = [{'key': 'Items Nationwide',
                      'values': [dict(label=category, y=count, x=num) for category, count, num in zip(categories, counts, list(range(len(categories))))],
                      'color': '#3d40a2'},
                     {'key': '{} Items'.format(states[state]),
                      'values': [dict(label=category, y=count, x=num) for category, count, num in zip(categories, state_counts, list(range(len(categories))))],
                      'color': '#d64d4d'}]
    return category_data, categories


# def draw_state_categories(state):
#     category_data = make_state_categories(state)
#
#     y_pos = np.arange(len(category_data['categories']))
#     width = .50
#     national = plt.barh(y_pos, category_data['counts'], width, align='center', log=True)
#     state_plot = plt.barh(y_pos+width, category_data['state_counts'], width, align='center', color='red', log=True)
#     plt.yticks(y_pos, category_data['categories'])
#     plt.xlabel(category_data['x_label'])
#     plt.title(category_data['title'])
#     plt.legend((national[0], state_plot[0]), ('National', states[state]))
#     plt.savefig('visualize/static/visualize/items-{}.png'.format(state))
#     plt.close()


def get_state_deaths(state):
    twenty_fifteen = GuardianCounted.objects.filter(date__year=2015)
    twenty_sixteen = GuardianCounted.objects.filter(date__year=2016)

    us_population = County.objects.aggregate(total=Sum('pop_est_2015'))
    state_population = County.objects.filter(
        state=states[state]).aggregate(total=Sum('pop_est_2015'))

    twenty_fifteen_state_deaths = twenty_fifteen.filter(state=state).count()
    twenty_sixteen_state_deaths = twenty_sixteen.filter(state=state).count()
    twenty_fifteen_deaths = twenty_fifteen.count()
    twenty_sixteen_deaths = twenty_sixteen.count()
    twenty_fifteen_avg_deaths = twenty_fifteen_deaths / 50
    twenty_sixteen_avg_deaths = twenty_sixteen_deaths / 50
    twenty_fifteen_state_per_capita = twenty_fifteen_state_deaths / state_population['total']
    twenty_sixteen_state_per_capita = twenty_sixteen_state_deaths / state_population['total']
    twenty_fifteen_per_capita = twenty_fifteen_deaths / us_population['total']
    twenty_sixteen_per_capita = twenty_sixteen_deaths / us_population['total']
    state_deaths = {'twenty_fifteen_state_deaths': twenty_fifteen_state_deaths,
                    'twenty_fifteen_avg_deaths': twenty_fifteen_avg_deaths}
    return state_deaths


def compare_ordered_months(ordered_months, state_ordered_months):
    if len(ordered_months) != len(state_ordered_months):
        for num, month in enumerate(ordered_months):
            try:
                if month['year'] == state_ordered_months[num]['year'] and month['month'] == state_ordered_months[num]['month']:
                    continue
                else:
                    state_ordered_months.insert(num, {'year': month['year'],
                                                      'month': month['month'],
                                                      'pk__count': 0})
            except IndexError:
                state_ordered_months.insert(num, {'year': month['year'],
                                                  'month': month['month'],
                                                  'pk__count': 0})
    return state_ordered_months

def make_jstimestamp_from_string(string):
    month_year = datetime.datetime.strptime(string, '%B %Y')
    return month_year.timestamp() * 1000.0


def get_state_deaths_over_time(state):
    guardian_month_dict = GuardianCounted.objects.annotate(
        year=Extract(F('date'), what_to_extract='year'),
        month=Extract(F('date'), what_to_extract='month')).values(
            'year', 'month').annotate(Count('pk'))
    state_month_dict = GuardianCounted.objects.filter(state=state).annotate(
        year=Extract(F('date'), what_to_extract='year'),
        month=Extract(F('date'), what_to_extract='month')).values(
            'year', 'month').annotate(Count('pk'))
    ordered_months = sorted(guardian_month_dict,
                            key=lambda k: (k['year'], k['month']))
    state_ordered_months = sorted(state_month_dict,
                                  key=lambda k: (k['year'], k['month']))
    month_list = ["{} {}".format(numbered_months[x['month']], int(x['year']))
                  for x in ordered_months]

    state_ordered_months = compare_ordered_months(ordered_months, state_ordered_months)
    deaths_per_month = [x['pk__count'] for x in ordered_months]
    state_deaths_per_month = [x['pk__count'] for x in state_ordered_months]
    deaths_over_time = [{'key': 'Average National Deaths Per Month',
                         'values': [dict(x=make_jstimestamp_from_string(month), y=(deaths / 51)) for month, deaths in zip(month_list, deaths_per_month)],
                         'color': '#3d40a2'},
                        {'key': '{} Deaths Per Month'.format(states[state]),
                         'values': [dict(x=make_jstimestamp_from_string(month), y=deaths) for month, deaths in zip(month_list, state_deaths_per_month)],
                         'color': '#d64d4d'}]
    return deaths_over_time

# def draw_state_deaths(state):
#     state_deaths = get_state_deaths(state)
#     deaths_over_time = get_state_deaths_over_time(state)
#     plt.bar([0, 1], [state_deaths['twenty_fifteen_state_deaths'], state_deaths['twenty_fifteen_avg_deaths']])
#     plt.ylabel('People Killed by Police')
#     plt.title('2015 Killings by Police in {} and the US'.format(states[state]))
#     plt.xticks([0, 1], ('{} Deaths'.format(states[state]),
#                         'Average Deaths Per State'))
#     plt.savefig('visualize/static/visualize/2015{}.png'.format(state))
#     plt.close()
#
#     months_nums = range(len(deaths_over_time['ordered_months']))
#     national = plt.plot(months_nums, deaths_over_time['deaths_per_month'])
#     state_plot = plt.plot(months_nums, deaths_over_time['state_deaths_per_month'], 'r')
#     plt.ylabel('People Killed by Police')
#     plt.title('Deaths in 2015 and 2016 By Month')
#     plt.xticks(months_nums, deaths_over_time['month_list'], rotation=25)
#     plt.legend((national[0], state_plot[0]), ('National', states[state]))
#     plt.savefig('visualize/static/visualize/{}-line.png'.format(state))
#     plt.close()
#     return state_deaths

def remove_periods_commas(pd_object):
    if type(pd_object) == str:
        new_string = pd_object.strip()
        if ',' in new_string:
            new_string = new_string.replace(',', '')
        if '.' in new_string:
            new_string = new_string.replace('.', '')
        if new_string:
            return new_string
        else:
            return 0
    else:
        return pd_object


def populate_crime_from_csv():
    crime_csv = pd.read_csv('data/DC_model_csv/visualize_crime.csv')
    column_dict = {'population': 0, 'violent_crime': 0,
                   'murder_manslaughter': 0, 'rape_revised_def': 0,
                   'rape_legacy_def': 0, 'robbery': 0, 'aggravated_assault': 0,
                   'property_crime': 0, 'burglary': 0, 'larceny_theft': 0,
                   'motor_vehicle_theft': 0, 'arson': 0}
    crime_csv.fillna(value=column_dict, inplace=True)
    for index, row in crime_csv.iterrows():
        if pd.isnull(row['county_id']):
            county_obj = None
        else:
            try:
                county_obj = County.objects.get(id=row['county_id'])
            except ObjectDoesNotExist:
                county_obj = None
        try:
            csv_violent_crime = int(remove_periods_commas(row['violent_crime']))
        except AttributeError:
            csv_violent_crime = row['violent_crime']
        try:
            csv_rape_legacy_def = int(remove_periods_commas(row['rape_legacy_def']))
        except AttributeError:
            csv_rape_legacy_def = row['rape_legacy_def']
        try:
            csv_arson = int(remove_periods_commas(row['arson']))
        except AttributeError:
            csv_arson = row['arson']
        new_crime = Crime(population=int(row['population']),
                          year=datetime.date(year=row['year'],
                                             month=1,
                                             day=1),
                          state=row['state'],
                          city=row['city'],
                          violent_crime=csv_violent_crime,
                          murder_manslaughter=row['murder_manslaughter'],
                          rape_revised_def=int(row['rape_revised_def']),
                          rape_legacy_def=csv_rape_legacy_def,
                          robbery=int(remove_periods_commas(row['robbery'])),
                          aggravated_assault=int(remove_periods_commas(row['aggravated_assault'])),
                          property_crime=int(remove_periods_commas(row['property_crime'])),
                          burglary=int(remove_periods_commas(row['burglary'])),
                          larceny_theft=int(remove_periods_commas(row['larceny_theft'])),
                          motor_vehicle_theft=int(remove_periods_commas(row['motor_vehicle_theft'])),
                          arson=csv_arson,
                          county=county_obj)
        new_crime.save()


def item_categories():
    # apps, schema_editor <-- function arguments for migration function def.
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



def get_county_deaths(county):
    counties = list(County.objects.filter(state = county.state))
    twenty_fifteen = GuardianCounted.objects.filter(date__year=2015, county=county)
    twenty_sixteen = GuardianCounted.objects.filter(date__year=2016, county=county)

    county_population = (County.objects.get(id=county)).pop_est_2015
    state_population = (County.objects.filter(state=county.state)).aggregate(total=Sum('pop_est_2015'))

    twenty_fifteen_county_deaths = twenty_fifteen.filter(county=county).count()
    twenty_sixteen_county_deaths = twenty_sixteen.filter(county=county).count()
    twenty_fifteen_deaths = twenty_fifteen.count()
    twenty_sixteen_deaths = twenty_sixteen.count()

    twenty_fifteen_avg_deaths = twenty_fifteen_deaths / len(counties)
    twenty_sixteen_avg_deaths = twenty_sixteen_deaths / len(counties)
    twenty_fifteen_state_per_capita = twenty_fifteen_state_deaths / state_population['total']
    twenty_sixteen_state_per_capita = twenty_sixteen_state_deaths / state_population['total']
    twenty_fifteen_county_per_capita = twenty_fifteen_deaths / county_population
    twenty_sixteen_county_per_capita = twenty_sixteen_deaths / county_population
    state_deaths = {'twenty_fifteen_state_deaths': twenty_fifteen_state_deaths,
                    'twenty_fifteen_county_deaths': twenty_fifteen_county_deaths}
    return county_deaths


def counties_list(state):
    counties = list(County.objects.filter(state=states[state]))
    return counties


def compare_ordered_years(national_ordered, state_ordered):
    if len(national_ordered) != len(state_ordered):
        for num, year in enumerate(national_ordered):
            try:
                if year['year'] == state_ordered[num]['year']:
                    continue
                else:
                    state_ordered.insert(num, {'year': year['year'],
                                               'Total_Value__sum': 0.0})
            except IndexError:
                state_ordered.insert(num, {'year': year['year'],
                                           'Total_Value__sum': 0.0})
    return state_ordered


def get_dollars_donated_by_year(state):
    national_money = Item.objects.annotate(year=Extract(F('Ship_Date'), what_to_extract='year')).values('year').annotate(Sum('Total_Value'))
    state_money = Item.objects.filter(state=state).annotate(year=Extract(F('Ship_Date'), what_to_extract='year')).values('year').annotate(Sum('Total_Value'))
    national_ordered = sorted(national_money, key=itemgetter('year'))
    state_ordered = sorted(state_money, key=itemgetter('year'))
    state_ordered = compare_ordered_years(national_ordered, state_ordered)
    year_list = ['{}'.format(int(x['year'])) for x in national_ordered]
    national_money_years = [x['Total_Value__sum'] for x in national_ordered]
    state_money_years = [x['Total_Value__sum'] for x in state_ordered]
    dollars_by_year = [{'key': 'Average Dollar Value Donated Nationally',
                        'values': [dict(x=num, y=(float(amount) / 51), label=year) for year, amount, num in zip(year_list, national_money_years, list(range(len(year_list))))],
                        'color': '#3d40a2'},
                       {'key': '{} Dollars Per Year'.format(states[state]),
                        'values': [dict(x=num, y=float(amount)) for year, amount, num in zip(year_list, state_money_years, list(range(len(year_list))))],
                        'color': '#d64d4d'}]

    return dollars_by_year
