import operator
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import County, GuardianCounted, Geo, Item, Station, Crime
from .utilities import draw_state_deaths, states, draw_state_categories
from .utilities import get_state_deaths, get_state_deaths_over_time, make_state_categories, get_county_deaths, counties_list


def index(request):
    state_list = sorted(states.items(), key=operator.itemgetter(1))
    context = {'states': state_list}
    return render(request, "visualize/index.html", context)


def state(request, state):
    state_deaths = draw_state_deaths(state)
    draw_state_categories(state)
    context = {'state': state,
               'state_num': state_deaths['twenty_fifteen_state_deaths'],
               'average': state_deaths['twenty_fifteen_avg_deaths'],
               'long_state_name': states[state],
               'counties_list': counties_list(state)}
    return render(request, "visualize/state.html", context)


def state_json(request, state):
    data = {'state_deaths': get_state_deaths(state),
            'deaths_over_time': get_state_deaths_over_time(state),
            'category_data': make_state_categories(state)}
    return HttpResponse(json.dumps(data), content_type='application/json')

def county(request, county):
    county_obj = County.objects.get(id=county)
    crimes_list = list(Crime.objects.filter(county=county))
    county_items = (Item.objects.filter(county=county.id, category='Assault rifle')).aggregate(total=Sum('quantity'))
    context = {'county': county,
               'county_obj':county_obj,
               'crimes_list':crimes_list,
               'county_items':county_items
    }
    return render(request, "visualize/county.html", context)
