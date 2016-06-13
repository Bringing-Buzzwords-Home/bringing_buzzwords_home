import operator
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import County, GuardianCounted, Geo, Item, Station, Crime, State
from .utilities import states, get_dollars_donated_by_year, format_money
from .utilities import get_state_deaths, get_state_deaths_over_time, make_state_categories
from .utilities import get_state_crime, get_county_deaths, create_counties_list
from .utilities import create_county_crime, make_per_capita_guns, state_abbrev
from .utilities import get_categories_per_capita, format_integer
from rest_framework import viewsets
from .serializers import StateSerializer
from django.db.models import Sum, Func, Count, F
from nvd3 import *
from django.utils.safestring import mark_safe


class StateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = State.objects.all().order_by('state')
    serializer_class = StateSerializer


def index(request):
    state_list = sorted(states.items(), key=operator.itemgetter(1))
    context = {'states': state_list}
    return render(request, "visualize/index.html", context)


def state(request, state):
    state = state.upper()
    state_obj = get_object_or_404(State, state=state)
    state_deaths = get_state_deaths(state)
    category_data, categories = make_state_categories(state)
    ten_thirty_three_total = Item.objects.filter(state=state).aggregate(Sum('Total_Value'))['Total_Value__sum']
    twenty_fifteen_kills = GuardianCounted.objects.filter(state=county).count()
    twenty_fifteen_population = County.objects.filter(state=states[state]).aggregate(Sum('pop_est_2015'))['pop_est_2015__sum']
    context = {'state': state,
               'state_num': state_deaths['2015 {} Fatal Encounters'.format(states[state])],
               'average': state_deaths['2015 Average Fatal Encounters'],
               'long_state_name': states[state],
               'counties_list': create_counties_list(state),
               'categories': categories,
               'twenty_fourteen_violent': format_integer(state_obj.total_violent_crime),
               'twenty_fourteen_property': format_integer(state_obj.total_property_crime),
               'twenty_fifteen_kills': twenty_fifteen_kills,
               'ten_thirty_three_total': format_money(ten_thirty_three_total),
               'twenty_fifteen_population': format_integer(twenty_fifteen_population),
               }
    return render(request, "visualize/state.html", context)


def state_json(request, state):
    state_deaths = get_state_deaths(state)
    category_data, category_nums = make_state_categories(state)
    per_capita_guns, per_capita_nums = make_per_capita_guns(state)
    data = {'state_deaths': [dict(key='State Deaths', values=[dict(label=key, value=value) for key, value in state_deaths.items()])],
            'deaths_over_time': get_state_deaths_over_time(state),
            'category_data': category_data,
            'categories_per_capita': get_categories_per_capita(state, category_data),
            'dollars_by_year': get_dollars_donated_by_year(state),
            'state_crime': get_state_crime(state),
            'per_capita_rifles': per_capita_guns,
            'per_capita_nums': per_capita_nums,
            'category_nums': category_nums}
    return HttpResponse(json.dumps(data), content_type='application/json')


def county(request, county):
    county_obj = County.objects.get(id=county)
    total_num_counties_in_country = 3112
    state = state_abbrev[county_obj.state]
    state_obj = State.objects.get(state=state)
    num_counties_in_state = len(County.objects.filter(state=county_obj.state))

    twenty_fourteen_violent = int(Crime.objects.filter(year='2014-01-01', county=county).aggregate(Sum('violent_crime'))['violent_crime__sum'])
    twenty_fourteen_property = int(Crime.objects.filter(year='2014-01-01', county=county).aggregate(Sum('property_crime'))['property_crime__sum'])
    ten_thirty_three_total = int(Item.objects.filter(county=county).aggregate(Sum('Total_Value'))['Total_Value__sum'])
    twenty_fifteen_kills = int(GuardianCounted.objects.filter(county=county, date__year=2015).count())
    county_crime = [twenty_fourteen_violent, twenty_fourteen_property]
    crimes_list = list(Crime.objects.filter(county=county))


    county_twenty_fourteen_violent_state_avg = int((state_obj.total_violent_crime)/num_counties_in_state)
    county_twenty_fourteen_property_state_avg = int((state_obj.total_property_crime)/num_counties_in_state)
    state_ten_thirty_three_county_avg = ((state_obj.total_military_dollars)/num_counties_in_state)
    state_county_deaths_avg = float((state_obj.total_deaths_twentyfifteen)/num_counties_in_state)


    county_twenty_fourteen_violent_country_avg = int(State.objects.all().aggregate(Sum('total_violent_crime'))['total_violent_crime__sum']/total_num_counties_in_country)
    county_twenty_fourteen_property_country_avg = int(State.objects.all().aggregate(Sum('total_property_crime'))['total_property_crime__sum']/total_num_counties_in_country)
    county_ten_thirty_three_country_avg = float(State.objects.all().aggregate(Sum('total_military_dollars'))['total_military_dollars__sum']/total_num_counties_in_country)
    county_twenty_fifteen_fatalities_country_avg = float(State.objects.all().aggregate(Sum('total_deaths_twentyfifteen'))['total_deaths_twentyfifteen__sum']/total_num_counties_in_country)



    national_values = [{'x': 0,
                        'y': county_twenty_fourteen_violent_country_avg,
                        'label': 'Violent Crime'},
                       {'x': 1,
                        'y': county_twenty_fourteen_property_country_avg,
                        'label': 'Property Crime'}]
    state_values = [{'x': 0,
                     'y': county_twenty_fourteen_violent_state_avg,
                     'label': 'Violent Crime'},
                    {'x': 1,
                     'y': county_twenty_fourteen_property_state_avg,
                     'label': 'Property Crime'}]
    county_values = [{'x': 0,
                     'y': twenty_fourteen_violent,
                     'label': 'Violent Crime'},
                    {'x': 1,
                     'y': twenty_fourteen_property,
                     'label': 'Property Crime'}]


    average_state_crime = [{'key': 'Average State Crime', 'values': national_values},{'key': '{} Crime'.format(states[state]),'values': state_values}, {'key': '{} Crime'.format(county_obj.county_name), 'values': county_values}]

    national_values_deaths = [{'x': 0,
                        'y': county_twenty_fifteen_fatalities_country_avg,
                        'label': 'Deadly Encounters'}]
    state_values_deaths = [{'x': 0,
                     'y': state_county_deaths_avg,
                     'label': 'Deadly Encounters'}]
    county_values_deaths = [{'x': 0,
                     'y': twenty_fifteen_kills,
                     'label': 'Deadly Encounters'}]


    average_deaths = [{'key': 'Average County Fatal Encounters in US', 'values': national_values_deaths}, {'key': '{} Average County Fatal Encounters'.format(states[state]),'values': state_values_deaths}, {'key': '{} Fatal Encounters'.format(county_obj.county_name), 'values': county_values_deaths}]

    national_value_military_avg= [{'x': 0,
                        'y': county_ten_thirty_three_country_avg,
                        'label': 'Military Equpment Value'}]
    state_value_military_avg = [{'x': 0,
                     'y': state_ten_thirty_three_county_avg,
                     'label': 'Military Equpment Value'}]
    county_value_military_avg= [{'x': 0,
                     'y': ten_thirty_three_total,
                     'label': 'Military Equpment Value'}]


    average_military_value = [{'key': 'Average US County', 'values': national_value_military_avg}, {'key': 'Average County in {}'.format(states[state]),'values': state_value_military_avg}, {'key': '{}'.format(county_obj.county_name), 'values': county_value_military_avg}]

    context = {
        'military_value': mark_safe(json.dumps(average_military_value)),
        'state_crime': mark_safe(json.dumps(average_state_crime)),
        'average_deaths': mark_safe(json.dumps(average_deaths)),
        'county': county,
        'county_obj': county_obj,
        'crimes_list': crimes_list,
        'twenty_fourteen_violent': format_integer(twenty_fourteen_violent),
        'twenty_fourteen_property': format_integer(twenty_fourteen_property),
        'twenty_fifteen_kills': format_integer(twenty_fifteen_kills),
        'ten_thirty_three_total': format_money(ten_thirty_three_total),
        'counties_list': create_counties_list(state),
        'county_pop_twenty_fifteen': format_integer(county_obj.pop_est_2015)
        }
    return render(request, "visualize/county.html", context)


def about(request):
    return render(request, "visualize/about.html")
