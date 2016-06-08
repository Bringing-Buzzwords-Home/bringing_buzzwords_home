import operator
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .models import County, GuardianCounted, Geo, Item, Station, Crime
from .utilities import states
from .utilities import get_state_deaths, get_state_deaths_over_time, make_state_categories, get_county_deaths, counties_list
from django.db.models import Sum, Func, Count, F


def index(request):
    state_list = sorted(states.items(), key=operator.itemgetter(1))
    context = {'states': state_list}
    return render(request, "visualize/index.html", context)


def state(request, state):
    state_deaths = get_state_deaths(state)
    category_data, categories = make_state_categories(state)
    twenty_fourteen_violent = Crime.objects.filter(year='2014-01-01', state=states[state]).aggregate(Sum('violent_crime'))['violent_crime__sum']
    twenty_fourteen_property = Crime.objects.filter(year='2014-01-01', state=states[state]).aggregate(Sum('property_crime'))['property_crime__sum']
    ten_thirty_three_total = Item.objects.filter(state=state).aggregate(Sum('Total_Value'))['Total_Value__sum']
    twenty_fifteen_kills = GuardianCounted.objects.filter(state=county).count()
    twenty_fifteen_population = County.objects.filter(state = states[state]).aggregate(Sum('pop_est_2015'))['pop_est_2015__sum']
    context = {'state': state,
               'state_num': state_deaths['twenty_fifteen_state_deaths'],
               'average': state_deaths['twenty_fifteen_avg_deaths'],
               'long_state_name': states[state],
               'counties_list': counties_list(state),
               'categories': categories,
               'twenty_fourteen_violent': twenty_fourteen_violent,
               'twenty_fourteen_property': twenty_fourteen_property,
               'twenty_fifteen_kills': twenty_fifteen_kills,
               'ten_thirty_three_total': ten_thirty_three_total,
               'twenty_fifteen_population': twenty_fifteen_population,
               }
    return render(request, "visualize/state.html", context)


def state_json(request, state):
    state_deaths = get_state_deaths(state)
    category_data, categories = make_state_categories(state)
    data = {'state_deaths': [dict(key='State Deaths', values=[dict(label=key, value=value) for key, value in state_deaths.items()])],
            'deaths_over_time': get_state_deaths_over_time(state),
            'category_data': category_data}
    return HttpResponse(json.dumps(data), content_type='application/json')

def county(request, county):
    twenty_fourteen_violent = Crime.objects.filter(year='2014-01-01', county=county).aggregate(Sum('violent_crime'))['violent_crime__sum']
    twenty_fourteen_property = Crime.objects.filter(year='2014-01-01', county=county).aggregate(Sum('property_crime'))['property_crime__sum']
    ten_thirty_three_total = Item.objects.filter(county=county).aggregate(Sum('Total_Value'))['Total_Value__sum']
    twenty_fifteen_kills = GuardianCounted.objects.filter(county=county).count()
    county_obj = County.objects.get(id=county)
    crimes_list = list(Crime.objects.filter(county=county))
    context = {'county': county,
               'county_obj': county_obj,
               'crimes_list': crimes_list,
               'twenty_fourteen_violent': twenty_fourteen_violent,
               'twenty_fourteen_property': twenty_fourteen_property,
               'twenty_fifteen_kills': twenty_fifteen_kills,
               'ten_thirty_three_total': ten_thirty_three_total
    }
    return render(request, "visualize/county.html", context)
