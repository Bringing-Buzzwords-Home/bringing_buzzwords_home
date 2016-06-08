import operator
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import County, GuardianCounted, Geo, Item, Station, Crime, State
from .utilities import states, get_dollars_donated_by_year, get_categories_per_capita
from .utilities import get_state_deaths, get_state_deaths_over_time, make_state_categories
from .utilities import get_state_crime, get_county_deaths, counties_list
from rest_framework import viewsets
from .serializers import StateSerializer


class StateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = State.objects.all().order_by('state')
    serializer_class = StateSerializer


def index(request):
    state_list = sorted(states.items(), key=operator.itemgetter(1))
    context = {'states': state_list}
    return render(request, "visualize/index.html", context)


def state(request, state):
    state_deaths = get_state_deaths(state)
    category_data, categories = make_state_categories(state)
    context = {'state': state,
               'state_num': state_deaths['twenty_fifteen_state_deaths'],
               'average': state_deaths['twenty_fifteen_avg_deaths'],
               'long_state_name': states[state],
               'counties_list': counties_list(state),
               'categories': categories}
    return render(request, "visualize/state.html", context)


def state_json(request, state):
    state_deaths = get_state_deaths(state)
    category_data, categories = make_state_categories(state)
    data = {'state_deaths': [dict(key='State Deaths', values=[dict(label=key, value=value) for key, value in state_deaths.items()])],
            'deaths_over_time': get_state_deaths_over_time(state),
            'category_data': category_data,
            'categories_per_capita': get_categories_per_capita(state, category_data),
            'dollars_by_year': get_dollars_donated_by_year(state),
            'state_crime': get_state_crime(state)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def county(request, county):
    county_obj = County.objects.get(id=county)
    crimes_list = list(Crime.objects.filter(county=county))
    context = {'county': county,
               'county_obj': county_obj,
               'crimes_list': crimes_list,
    }
    return render(request, "visualize/county.html", context)
