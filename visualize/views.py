from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import County, GuardianCounted, Geo, Item, Station
from .utilities import draw_state_deaths



def index(request):
    return render(request, "visualize/index.html")


def state(request, state):
    state_num, average = draw_state_deaths(state)
    context = {'state': state, 'state_num': state_num, 'average': average}
    return render(request, "visualize/state.html", context)
