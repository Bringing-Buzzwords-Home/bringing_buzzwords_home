from .models import County, GuardianCounted
import csv
import datetime
from django.db.models import Sum
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


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
    plt.savefig('visualize/static/visualize/{}.png'.format(state))
    plt.close()
    return twenty_fifteen_state_deaths, twenty_fifteen_avg_deaths
