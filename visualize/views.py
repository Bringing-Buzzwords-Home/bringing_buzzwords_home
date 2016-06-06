import operator
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import County, GuardianCounted, Geo, Item, Station
from .utilities import states, draw_state_categories
from .utilities import get_state_deaths, get_state_deaths_over_time, make_state_categories


def index(request):
    state_list = sorted(states.items(), key=operator.itemgetter(1))
    context = {'states': state_list}
    return render(request, "visualize/index.html", context)


def state(request, state):
    state_deaths = get_state_deaths(state)
    draw_state_categories(state)
    context = {'state': state,
               'state_num': state_deaths['twenty_fifteen_state_deaths'],
               'average': state_deaths['twenty_fifteen_avg_deaths'],
               'long_state_name': states[state]}
    return render(request, "visualize/state.html", context)


def state_json(request, state):
    state_deaths = get_state_deaths(state)
    deaths_over_time = get_state_deaths_over_time(state)
    data = {'state_deaths': [dict(key='State Deaths', values=[dict(label=key, value=value) for key, value in state_deaths.items()])],
            'deaths_over_time': deaths_over_time,
            'category_data': make_state_categories(state)}
    return HttpResponse(json.dumps(data), content_type='application/json')
