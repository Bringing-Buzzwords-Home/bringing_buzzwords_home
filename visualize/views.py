from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import County, GuardianCounted, Geo, Item, Station


def index(request):
    return render(request, "visualize/index.html")


def state(request, state):
    context = {'state': state}
    return render(request, "visualize/state.html", context)
