import operator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import County, GuardianCounted, Geo, Item, Station
from .utilities import draw_state_deaths, states, draw_state_categories


def index(request):
    state_list = sorted(states.items(), key=operator.itemgetter(1))
    context = {'states': state_list}
    return render(request, "visualize/index.html", context)


def state(request, state):
    state_num, average = draw_state_deaths(state)
    draw_state_categories(state)
    context = {'state': state, 'state_num': state_num, 'average': average,
               'long_state_name': states[state]}
    return render(request, "visualize/state.html", context)
