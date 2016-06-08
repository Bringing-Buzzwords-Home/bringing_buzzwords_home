import operator
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import County, GuardianCounted, Geo, Item, Station, Crime, State
from .utilities import states, get_dollars_donated_by_year, get_categories_per_capita
from .utilities import get_state_deaths, get_state_deaths_over_time, make_state_categories
from .utilities import get_state_crime, get_county_deaths, counties_list
from .utilities import create_county_crime
from rest_framework import viewsets
from .serializers import StateSerializer
from django.db.models import Sum, Func, Count, F



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
            'state_crime': get_state_crime(state)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def county(request, county):
    twenty_fourteen_violent = Crime.objects.filter(year='2014-01-01', county=county).aggregate(Sum('violent_crime'))['violent_crime__sum']
    twenty_fourteen_property = Crime.objects.filter(year='2014-01-01', county=county).aggregate(Sum('property_crime'))['property_crime__sum']
    ten_thirty_three_total = Item.objects.filter(county=county).aggregate(Sum('Total_Value'))['Total_Value__sum']
    twenty_fifteen_kills = GuardianCounted.objects.filter(county=county).count()
    county_obj = County.objects.get(id=county)
    crimes_list = list(Crime.objects.filter(county=county))
    county_crime_bar = create_county_crime(county)
    xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
    chartdata = {'x': xdata, 'y': ydata}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'
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
       'county': county,
       'county_obj': county_obj,
       'crimes_list': crimes_list,
       'twenty_fourteen_violent': twenty_fourteen_violent,
       'twenty_fourteen_property': twenty_fourteen_property,
       'twenty_fifteen_kills': twenty_fifteen_kills,
       'ten_thirty_three_total': ten_thirty_three_total,
       'county_crime_bar': county_crime_bar,}
    return render(request, "visualize/county.html", data)
