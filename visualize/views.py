from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Sum
from .models import County, GuardianCounted, Geo, Item, Station
from .utilities import states
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def index(request):
    return render(request, "visualize/index.html")


def state(request, state):
    twenty_fifteen = GuardianCounted.objects.filter(
        date__year=2015)
    twenty_sixteen = GuardianCounted.objects.filter(
        date__year=2016)

    us_population = County.objects.aggregate(total=Sum('population'))
    state_population = County.objects.filter(
        state=states[state]).aggregate(total=Sum('population'))

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

    fifteen = plt.bar([0, 1, 2, 3], [twenty_fifteen_state_deaths,
                                     twenty_fifteen_avg_deaths,
                                     twenty_fifteen_state_per_capita,
                                     twenty_fifteen_per_capita])
    plt.ylabel('People Killed by Police')
    plt.title('2015 Killings by Police in the US')
    plt.xticks([0, 1, 2, 3], ('{} Deaths'.format(state),
                              'Average Deaths Per State',
                              '{} Deaths Per Capita'.format(state),
                              'US Deaths Per Capita'))
    plt.savefig('static/visualize/{}.png'.format(state))

    context = {'state': state}
    return render(request, "visualize/state.html", context)
