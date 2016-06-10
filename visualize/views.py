import operator
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import County, GuardianCounted, Geo, Item, Station, Crime, State
from .utilities import states, get_dollars_donated_by_year, get_categories_per_capita
from .utilities import get_state_deaths, get_state_deaths_over_time, make_state_categories
from .utilities import get_state_crime, get_county_deaths, counties_list
from .utilities import create_county_crime, make_per_capita_assault_rifles
from rest_framework import viewsets
from .serializers import StateSerializer
from django.db.models import Sum, Func, Count, F
from nvd3 import *



class StateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = State.objects.all().order_by('state')
    serializer_class = StateSerializer



def index(request):
    state_list = sorted(states.items(), key=operator.itemgetter(1))
    context = {'states': state_list}
    return render(request, "visualize/index.html", context)


def state(request, state):
    state = state.upper()
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
            'category_data': category_data,
            'categories_per_capita': get_categories_per_capita(state, category_data),
            'dollars_by_year': get_dollars_donated_by_year(state),
            'state_crime': get_state_crime(state),
            'per_capita_rifles': make_per_capita_assault_rifles(state)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def county(request, county):
    twenty_fourteen_violent = Crime.objects.filter(year='2014-01-01', county=county).aggregate(Sum('violent_crime'))['violent_crime__sum']
    twenty_fourteen_property = Crime.objects.filter(year='2014-01-01', county=county).aggregate(Sum('property_crime'))['property_crime__sum']
    ten_thirty_three_total = Item.objects.filter(county=county).aggregate(Sum('Total_Value'))['Total_Value__sum']
    twenty_fifteen_kills = GuardianCounted.objects.filter(county=county).count()
    county_obj = County.objects.get(id=county)
    crimes_list = list(Crime.objects.filter(county=county))

    xdata = ['Property Crime', 'Violent Crime']
    ydata = [twenty_fourteen_property, twenty_fourteen_violent]
    chartdata = {'x': xdata, 'y': ydata}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'
    chart = multiBarChart(width=500, height=400, x_axis_format=None)
    xdata_mbar = ['Violent Crime', 'Property Crime']
    ydata1_mbar = [Crime.objects.filter(year='2014-01-01', county=county).aggregate(Sum('violent_crime'))['violent_crime__sum'], Crime.objects.filter(year='2014-01-01', county=county).aggregate(Sum('property_crime'))['property_crime__sum']]
    ydata2_mbar = [Crime.objects.filter(year='2014-01-01').aggregate(Sum('violent_crime'))['violent_crime__sum'], Crime.objects.filter(year='2014-01-01').aggregate(Sum('property_crime'))['property_crime__sum']]
    chart.add_serie(name="Serie 1", y=ydata1_mbar, x=xdata_mbar)
    chart.add_serie(name="Serie 2", y=ydata2_mbar, x=xdata_mbar)
    multibarchart_container = 'piechart_container'

    extra_serie_line = {}
    xdata_line = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    ydata_line = [3, 5, 7, 8, 3, 5, 3, 5, 7, 6, 3, 1]
    chartdata_line = {
        'x': xdata_line,
        'name1': 'series 1', 'y1': ydata_line, 'extra1': extra_serie_line,
    }
    charttype_line = "lineChart"
    chartcontainer_line = 'linechart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        },
        'chart':chart,
        'xdata_mbar': xdata_mbar,
        'ydata1_mbar': ydata1_mbar,
        'ydata2_mbar': ydata2_mbar,
        'multibarchart_container': multibarchart_container,
        'county': county,
        'county_obj': county_obj,
        'crimes_list': crimes_list,
        'twenty_fourteen_violent': twenty_fourteen_violent,
        'twenty_fourteen_property': twenty_fourteen_property,
        'twenty_fifteen_kills': twenty_fifteen_kills,
        'ten_thirty_three_total': ten_thirty_three_total,
        'charttype_line': charttype_line,
        'chartdata_line': chartdata_line,
        'chartcontainer_line': chartcontainer_line,
    }
    return render(request, "visualize/county.html", data)
