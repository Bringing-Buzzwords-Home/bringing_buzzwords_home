from .models import County, GuardianCounted
import csv
import datetime
from django.db.models import Sum, Func, Count, F
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn


class Extract(Func):
    """
    Performs extraction of `what_to_extract` from `*expressions`.

    Arguments:
        *expressions (string): Only single value is supported, should be field name to
                               extract from.
        what_to_extract (string): Extraction specificator.

    Returns:
        class: Func() expression class, representing 'EXTRACT(`what_to_extract` FROM `*expressions`)'.
    """

    function = 'EXTRACT'
    template = '%(function)s(%(what_to_extract)s FROM %(expressions)s)'


states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
        }

numbered_months = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                   5: 'May', 6: 'June', 7: 'July', 8: 'August',
                   9: 'September', 10: 'October', 11: 'November',
                   12: 'December'}

months = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
          'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
          'October': 10, 'November': 11, 'December': 12}


def handle_guardian_counted_csv(csv_path, months):
    with open(csv_path) as f:
        counted_reader = csv.DictReader(f)
        for row in counted_reader:
            try:
                person_age = int(row['age'])
            # if age is unknown, age will be NULL in the db
            except ValueError:
                person_age = None
            counted = GuardianCounted(name=row['name'],
                                      age=person_age,
                                      gender=row['gender'],
                                      race_ethnicity=row['raceethnicity'],
                                      date=datetime.date(
                                        year=int(row['year']),
                                        month=months[row['month']],
                                        day=int(row['day'])),
                                      street_address=row['streetaddress'],
                                      city=row['city'],
                                      state=row['state'],
                                      classification=row['classification'],
                                      law_enforcement_agency=row['lawenforcementagency'],
                                      armed=row['armed'])
            counted.save()


def guardian_pop(months):
    handle_guardian_counted_csv('data/thecounted-data/the-counted-2015.csv',
                                months)
    handle_guardian_counted_csv('data/thecounted-data/the-counted-2016.csv',
                                months)


def draw_state_deaths(state):
    guardian_month_dict = GuardianCounted.objects.annotate(
        year=Extract(F('date'), what_to_extract='year'),
        month=Extract(F('date'), what_to_extract='month')).values(
            'year', 'month').annotate(Count('pk'))
    state_month_dict = GuardianCounted.objects.filter(state=state).annotate(
        year=Extract(F('date'), what_to_extract='year'),
        month=Extract(F('date'), what_to_extract='month')).values(
            'year', 'month').annotate(Count('pk'))
    ordered_months = sorted(guardian_month_dict,
                            key=lambda k: (k['year'], k['month']))
    state_ordered_months = sorted(state_month_dict,
                                  key=lambda k: (k['year'], k['month']))
    month_list = ["{}{}".format(numbered_months[x['month']], x['year']) for
                  x in ordered_months]

    if len(ordered_months) != len(state_ordered_months):
        for num, month in enumerate(ordered_months):
            try:
                if month['year'] == state_ordered_months[num]['year'] and month['month'] == state_ordered_months[num]['month']:
                    continue
                else:
                    state_ordered_months.insert(num, {'year': month['year'],
                                                      'month': month['month'],
                                                      'pk__count': 0})
            except IndexError:
                state_ordered_months.insert(num, {'year': month['year'],
                                                  'month': month['month'],
                                                  'pk__count': 0})
    deaths_per_month = [x['pk__count'] for x in ordered_months]
    state_deaths_per_month = [x['pk__count'] for x in state_ordered_months]

    twenty_fifteen = GuardianCounted.objects.filter(date__year=2015)
    twenty_sixteen = GuardianCounted.objects.filter(date__year=2016)

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

    plt.bar([0, 1], [twenty_fifteen_state_deaths, twenty_fifteen_avg_deaths])
    plt.ylabel('People Killed by Police')
    plt.title('2015 Killings by Police in {} and the US'.format(states[state]))
    plt.xticks([.5, 1.5], ('{} Deaths'.format(states[state]),
                           'Average Deaths Per State'))
    plt.savefig('visualize/static/visualize/2015{}.png'.format(state))
    plt.close()

    months_nums = range(len(ordered_months))
    national = plt.plot(months_nums, deaths_per_month)
    state_plot = plt.plot(months_nums, state_deaths_per_month, 'r')
    plt.ylabel('People Killed by Police')
    plt.title('Deaths in 2015 and 2016 By Month')
    plt.xticks(months_nums, month_list)
    plt.legend((national[0], state_plot[0]), ('National', states[state]))
    plt.savefig('visualize/static/visualize/{}-line.png'.format(state))
    plt.close()
    return twenty_fifteen_state_deaths, twenty_fifteen_avg_deaths
