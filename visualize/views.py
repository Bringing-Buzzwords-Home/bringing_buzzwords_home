import operator
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import County, GuardianCounted, Geo, Item, Station, Crime, State
from .utilities import states, get_dollars_donated_by_year, format_money
from .utilities import get_state_deaths, get_state_deaths_over_time, make_state_categories
from .utilities import get_state_violent_crime, get_county_deaths, create_counties_list
from .utilities import create_county_crime, make_per_capita_guns, state_abbrev
from .utilities import get_categories_per_capita, format_integer, get_state_property_crime
from .utilities import get_prop_crime_data, get_prop_crime_data_per_cap, format_float
from .utilities import get_viol_crime_data, get_viol_crime_data_per_cap, get_fatal_encounters
from .utilities import get_fatal_encounters_per_cap, get_military_value
from .utilities import get_military_value_per_cap
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
    state_obj = get_object_or_404(State, state=state)
    state_deaths = get_state_deaths(state)
    category_data, category_nums = make_state_categories(state)
    per_capita_guns, per_capita_nums = make_per_capita_guns(state)
    avg_violent_crime, per_capita_violent_crime = get_state_violent_crime(state_obj)
    avg_property_crime, per_capita_property_crime = get_state_property_crime(state_obj)
    data = {'state_deaths': [dict(key='State Deaths', values=[dict(label=key, value=value) for key, value in state_deaths.items()])],
            'deaths_over_time': get_state_deaths_over_time(state),
            'category_data': category_data,
            'categories_per_capita': get_categories_per_capita(state, category_data),
            'dollars_by_year': get_dollars_donated_by_year(state),
            'avg_violent_crime': avg_violent_crime,
            'per_capita_violent_crime': per_capita_violent_crime,
            'per_capita_rifles': per_capita_guns,
            'per_capita_nums': per_capita_nums,
            'category_nums': category_nums,
            'avg_property_crime': avg_property_crime,
            'per_capita_property_crime': per_capita_property_crime}
    return HttpResponse(json.dumps(data), content_type='application/json')


def county(request, county):
    county_obj = County.objects.get(id=county)
    total_num_counties_in_country = 3112
    state = state_abbrev[county_obj.state]
    state_obj = State.objects.get(state=state)
    num_counties_in_state = len(County.objects.filter(state=county_obj.state))
    county_pop = county_obj.pop_est_2015
    state_pop = (State.objects.get(state=state)).total_population_twentyfifteen
    us_population = State.objects.all().aggregate(Sum('total_population_twentyfifteen'))['total_population_twentyfifteen__sum']
    county_violent = int(Crime.objects.filter(year='2014-01-01', county=county).aggregate(Sum('violent_crime'))['violent_crime__sum'])
    county_property = int(Crime.objects.filter(year='2014-01-01', county=county).aggregate(Sum('property_crime'))['property_crime__sum'])
    county_military_value = int(Item.objects.filter(county=county).aggregate(Sum('Total_Value'))['Total_Value__sum'])
    county_fatal_encounters = int(GuardianCounted.objects.filter(county=county, date__year=2015).count())
    county_crime = [county_violent, county_property]
    average_state_crime_prop = get_prop_crime_data(state, county_obj, total_num_counties_in_country,
                            state_obj, num_counties_in_state, county)

    average_state_crime_prop_per_cap = get_prop_crime_data_per_cap(
                            county_property, state, county_obj, us_population,
                            state_pop, county_pop, state_obj)

    average_state_crime_viol = get_viol_crime_data(state, county_obj, total_num_counties_in_country,
                            state_obj, num_counties_in_state, county)


    average_state_crime_viol_per_cap = get_viol_crime_data_per_cap(
                            county_violent, state, county_obj, us_population,
                            state_pop, county_pop, state_obj)


    average_fatal_encounters = get_fatal_encounters(state, county_obj, total_num_counties_in_country,
                            state_obj, num_counties_in_state, county)


    average_fatal_encounters_per_cap = get_fatal_encounters_per_cap(county_fatal_encounters, us_population,
                            state_pop, state, county_obj, state_obj, county_pop)


    average_military_value = get_military_value(state, county_obj, total_num_counties_in_country,
                            state_obj, num_counties_in_state, county)

    average_military_value_per_cap  = get_military_value_per_cap(us_population, state_pop, county_pop,
                                    county_military_value, state_obj, county_obj, state)
    context = {
        'military_value': mark_safe(json.dumps(average_military_value)),
        'military_value_per_cap': mark_safe(json.dumps(average_military_value_per_cap)),
        'prop_crime': mark_safe(json.dumps(average_state_crime_prop)),
        "prop_crime_per_cap": mark_safe(json.dumps(average_state_crime_prop_per_cap)),
        'viol_crime': mark_safe(json.dumps(average_state_crime_viol)),
        "viol_crime_per_cap": mark_safe(json.dumps(average_state_crime_viol_per_cap)),
        'average_fatal_encounters': mark_safe(json.dumps(average_fatal_encounters)),
        'average_fatal_encounters_per_cap': mark_safe(json.dumps(average_fatal_encounters_per_cap)),
        'county': county,
        'county_obj': county_obj,
        'twenty_fourteen_violent': format_integer(county_violent),
        'twenty_fourteen_property': format_integer(county_property),
        'twenty_fifteen_kills': format_integer(county_fatal_encounters),
        'ten_thirty_three_total': format_money(county_military_value),
        'counties_list': create_counties_list(state),
        'county_pop_twenty_fifteen': format_integer(county_obj.pop_est_2015),
        'state_abbrev': state,
        }
    return render(request, "visualize/county.html", context)


def about(request):
    return render(request, "visualize/about.html")
